import re
import sys
import urllib
import time # for sleep
import random # for sleep time

if (len(sys.argv) <= 3):
  print "Usage: python extract-hrefs2.py ghex hardy amd64"
  exit(1)

# Command line args
package = sys.argv[1]
distro = sys.argv[2] # hardy
arch = sys.argv[3] # amd64 / i386

start = False
end = False
base_url = "http://packages.ubuntu.com"
# Relative name in the format the website will return to us
root_package_name = "/" + distro + "/" + package


href_re = re.compile("a href=\"(\S+)\"")
full_href_re = re.compile("a href=\"(http:\S+universe\S+)\"")
distro_re = re.compile(distro)
dep_re = re.compile("<ul class=\"uldep\">")
ndep_re = re.compile("</ul>")

# List of all packages we have examined
all_packages = list()
# List of all dependency hrefs
all_hrefs = list()
# List of packages left to examine
packages_to_load = list()
packages_to_load.append(root_package_name)

# Keep going until there are no packages left to load
while len(packages_to_load) > 0:
  # Remove first element of to-load list
  element = packages_to_load.pop(0)
  # Add this element to the list of all packages
  all_packages.append(element)

  print "Opening description page for package: " + element + " : " + (base_url + element)
  file = urllib.urlopen(base_url + element)

  for line in file:
    dep = dep_re.search(line)

    # Wait until we find marker for start of dependencies section
    if dep:
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
	  print "Adding " + entry + " to load list length now " + str(len(packages_to_load))
	  time.sleep(1)

	  # URL for the download page for the package
	  package_name = entry.split('/')[2]
	  download_url = base_url + "/" + distro + "/" + arch + "/" + package_name + "/download"
	  print "Downloading URL: " + download_url

	  download = urllib.urlopen(download_url)

	  for d in download:
	    href = full_href_re.search(d)
	    if href:
	      entry = href.group(1)
	      # Need to escape package name in case it has special characters
	      # that would break our regular expression
	      temp_re = re.compile(re.escape(package_name))
	      if temp_re.search(entry):
		print "HREF: " + entry
		all_hrefs.append(entry)
		break

	  download.close() 

      if ndep:
	end = True
	start = False

  file.close()
  time.sleep(random.randrange(1,10))

print "Full dependency list:"
print all_packages
print "Full href list:"
for h in all_hrefs:
  print h
