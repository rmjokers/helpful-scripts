# Simple script to connect to mythtv frontend and control basic navigation from a remote system.

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

    if c == 113: # q breaks the while loop
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
    elif c == curses.KEY_NPAGE: # page up
      command = "pageup"
    elif c == curses.KEY_PPAGE: # page down
      command = "pagedown"
    elif c == 112: # p
      command = "p"
    elif c == 100: # d
      command = "d"
    elif c == 113: # q
      command = "q"
    elif c == 122: # z
      command = "z"
    scrn.addstr(command)
    #scrn.addch(c)
    scrn.refresh()

    # This is rather inefficient...perhaps we should keep the socket open?
    if command:
      # Open a socket (TCP) and connect to desk Mythtv frontend
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect(("cube.local", 6546))
      s.send("key " + command + "\n")
      s.close()

  restorescreen()

try:
  main()
except:
  restorescreen()
