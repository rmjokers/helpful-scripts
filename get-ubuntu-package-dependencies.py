import re
import sys
import urllib
import time # for sleep

if (len(sys.argv) <= 1):
  print "Usage: python extract-hrefs2.py ghex hardy amd64"
  exit(1)

package = sys.argv[1]
distro = sys.argv[2]
arch = sys.argv[3] # amd64 / i386

start = False
end = False
base_url = "http://packages.ubuntu.com"
name = "/" + distro + "/" + package
download_url = base_url + "/" + distro + "/" + arch + "/" + package + "/download"


href_re = re.compile("a href=\"(\S+)\"")
distro_re = re.compile(distro)
dep_re = re.compile("<ul class=\"uldep\">")
ndep_re = re.compile("</ul>")

toload = list()

toload.append(name)


while len(toload) > 0:
  element = toload.pop(0)

  print "Opening URL: " + (base_url + element)
  file = urllib.urlopen(base_url + element)

  for line in file:

    dep = dep_re.search(line)

    if dep:
      start = True

    if start:
      #hrefs = href_re.finditer(line, 1)
      href = href_re.search(line)
      ndep = ndep_re.search(line)

      #for href in hrefs:
      if href:
	entry = href.group(1)

	# Make sure the package name matches the specified distro
	d = distro_re.search(entry)

	if d and not entry in toload:
	  toload.append(entry)

      if ndep:
	end = True
	start = False

  file.close()
  time.sleep(1)

print toload
