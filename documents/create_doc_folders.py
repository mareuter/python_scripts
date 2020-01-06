#!/usr/bin/env python
# Script must be run in a place where the NAS directory Documents/Financial is
# mounted

import argparse
import os
import sys

SERVICES_DIRS = ['Comcast', 'OV_Water', 'SW_Gas', 'TEP']
RECEIPT_DIRS = ['Purchases', 'Purchases_NoTax', 'TempStore']
MAIN_DIR = 'Old_Receipts'


def main(opts):

    if not os.path.exists(MAIN_DIR):
        print('Please change to the location to where Documents/Financial is mounted.')
        sys.exit(255)

    year = str(opts.year)
    os.chdir(MAIN_DIR)
    os.mkdir(year)
    os.chdir(year)

    for directory in (SERVICES_DIRS + RECEIPT_DIRS):
        os.mkdir(directory)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Create folders for old receipts.')

    parser.add_argument('year', type=int, help='Provide the year to create the directories in.')

    args = parser.parse_args()

    main(args)
