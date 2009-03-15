#!/usr/bin/python

""" (UPDR) Ubuntu Package Dependency Resolver.

Given an Ubuntu package, identify all dependencies from the repository and get
a list of HREFs for those packages. This allows us to download the packages and
install them offline more easily.

Originally, this script only operated on the Universe repository, but this was
expanded because some common dependencies in the Main repository are not on
default install media, but would be required for offline installation.
"""

__author__ = "Rodney Jokerst"
__version__ = "1.0"
__date__ = "March 15, 2009"
__license__ = "GPL"

import re
import sys
import urllib
import time # for sleep
import random # for sleep time
from optparse import OptionParser # for command line options

parser = OptionParser()
parser.add_option("-p", "--package", help="Package to resolve dependencies of (i.e. ghex)", dest="package")
parser.add_option("-d", "--distribution", help="Distribution name (i.e. gutsy, hardy)", dest="distro")
parser.add_option("-a", "--architecture", help="Architecture (i.e. i386, amd64)", dest="arch")

# Parse command line args
(options, args) = parser.parse_args()

# Print help if we get no command-line arguements
if (len(sys.argv) <= 3):
  parser.print_help()
  exit(1)

base_url = "http://packages.ubuntu.com"
# Relative name in the format the website will return to us
root_package_name = "/" + options.distro + "/" + options.package


href_re = re.compile("a href=\"(\S+)\"")
full_href_re = re.compile("a href=\"(http:\S+/pool/\S+)\"")
distro_re = re.compile(options.distro)
dep_re = re.compile("<ul class=\"uldep\">")
ndep_re = re.compile("</ul>")
universe_re = re.compile(">universe<")

# List of all packages we have examined
all_packages = list()
# List of all dependency hrefs
all_hrefs = list()
# List of packages left to examine
packages_to_load = list()
packages_to_load.append(root_package_name)

start = False
end = False
universe = False

# Keep going until there are no packages left to load
while len(packages_to_load) > 0:

  # Remove first element of to-load list
  element = packages_to_load.pop(0)
  # Add this element to the list of all packages
  all_packages.append(element)

  print "Opening description page for package: " + element + " : " + (base_url + element)
  file = urllib.urlopen(base_url + element)

  for line in file:

    unv = universe_re.search(line)
    dep = dep_re.search(line)

    # First, look for the universe marker. We only care about packages from universe for now
    #if unv:
    universe = True

    # Wait until we find marker for start of dependencies section
    if universe and dep:
      start = True

    if start:
      href = href_re.search(line)
      ndep = ndep_re.search(line)

      if href:
	entry = href.group(1)

	# Make sure the package name matches the specified distro
	d = distro_re.search(entry)

	if d and not entry in all_packages and not entry in packages_to_load:
	  # Add any packages we have not already seen to the load list
	  packages_to_load.append(entry)
	  print "\tAdding " + entry + " to dependency list length now " + str(len(packages_to_load))

      if ndep:
	end = True
	start = False

  file.close()


  # Now that we are finished processing the package description, 
  # URL for the download page for the package
  package_name = element.split('/')[2]
  download_url = base_url + "/" + options.distro + "/" + options.arch + "/" + package_name + "/download"
  print "\tExamining download URL: " + download_url

  download = urllib.urlopen(download_url)

  for d in download:
    href = full_href_re.search(d)
    if href:
      entry = href.group(1)
      # Need to escape package name in case it has special characters
      # that would break our regular expression
      temp_re = re.compile(re.escape(package_name))
      if temp_re.search(entry):
	print "\tHREF: " + entry
	all_hrefs.append(entry)
	break

  download.close() 

  universe = False
  start = False
  end = False
  
  time.sleep(random.randrange(1,10))

print "Full dependency list:"
print all_packages
print "Full href list:"
for h in all_hrefs:
  print h
