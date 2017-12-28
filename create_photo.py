#!/usr/bin/env python

import os
import sys

# Script must be run from Pictures directory on NAS

try:
    year = sys.argv[1]
except IndexError:
    print("Usage: create_photo.py <year>")
    sys.exit(255)

os.mkdir(year)
os.chdir(year)

DIR_LIST = ["AstroImaging", "Astronomy", "Astronomy_Raw", "Astronomy_Tif", "Other", "Panorama", "Photos"]
for pdir in DIR_LIST:
    os.mkdir(pdir)

for i in range(12):
    os.mkdir(os.path.join("Photos", "{:02d}".format(i + 1)))
