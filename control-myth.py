import curses
import sys
import socket

def restorescreen():
  curses.nocbreak()
  #curses.echo()
  curses.endwin()

def main():
  # Initialize the screen
  scrn = curses.initscr()
  # Accept key input immediately without waiting for Enter
  curses.cbreak()

  # properly interpret special characters
  scrn.keypad(1)

  # Clear the screen
  scrn.clear()

  scrn.refresh()

  while True:
    c = scrn.getch()
    scrn.clear()

    command = ""

    if c == 113: # q
      break
    elif c == 27:
      command = "escape"
    elif c == 32:
      command = "space"
    elif c == 10:
      command = "return"
    elif c == curses.KEY_DOWN:
      command = "down"
    elif c == curses.KEY_RIGHT:
      command = "right"
    elif c == curses.KEY_UP:
      command = "up"
    elif c == curses.KEY_LEFT:
      command = "left"
    elif c == curses.KEY_NPAGE:
      command = "pageup"
    elif c == curses.KEY_PPAGE:
      command = "pagedown"
    else:
      command = str(chr(c))

    scrn.addstr(command)
    #scrn.addch(c)
    scrn.refresh()

    if command:
      # Open a socket (TCP) and connect to Mythtv frontend
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect(("cube.local", 6546))
      #s.connect(("localhost", 6546))

      # Send key string plus key value
      s.send("key " + command + "\n")

      s.close()

  restorescreen()

try:
  main()
except:
  restorescreen()
