#!/usr/bin/env python
import os
import sys

# Script should be run from directory where image directory is to be made.

try:
    img_dir = sys.argv[1]
except IndexError:
    print("Usage: create_astroimg.py <image directory>")
    sys.exit(255)

os.mkdir(img_dir)
os.chdir(img_dir)

DIR_LIST = ["Calibrated", "Darks", "Flats", "Lights", "Processed", "Saved"]
for pdir in DIR_LIST:
    os.mkdir(pdir)
