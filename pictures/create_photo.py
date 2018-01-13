#!/usr/bin/env python

# Script must be run in a place where the NAS directories photo and
# Picture_Backup are mounted

import os
import sys

DIR_LIST = ["AstroImaging", "Astronomy_Raw", "Astronomy_Tif", "Other", "Panorama"]
MAIN_DIR = "photo"
BACKUP_DIR = "Picture_Backup"

try:
    year = sys.argv[1]
except IndexError:
    print("Usage: create_photo.py <year>")
    sys.exit(255)

if not (os.path.exists(MAIN_DIR) and os.path.exists(BACKUP_DIR)):
    print("Please change to the location where photo and Picture_Backup are both mounted.")
    sys.exit(254)

os.chdir(BACKUP_DIR)
os.mkdir(year)
os.chdir(year)

for pdir in DIR_LIST:
    os.mkdir(pdir)

os.chdir(os.path.join("../../", MAIN_DIR))
os.mkdir(year)
os.chdir(year)

for i in range(12):
    os.mkdir("{:02d}".format(i + 1))
