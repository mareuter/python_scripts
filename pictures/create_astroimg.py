#!/usr/bin/env python
import argparse
import os

# Script should be run from directory where image directory is to be made.

BASE_DIRS = ["Darks", "Flats", "Lights"]
EXTRA_DIRS = ["Aligned", "Calibrated", "Calibrated/Flats", "Calibrated/Lights", "CosCor",
              "Demosaiced", "Masters", "Processed", "Saved"]


def make_image_dirs(dir_list):
    for pdir in dir_list:
        os.mkdir(pdir)

def main(opts):

    if not opts.astroberry:
        os.mkdir(opts.image_dir)
    os.chdir(opts.image_dir)

    if not opts.astroberry:
        make_image_dirs(BASE_DIRS)
    else:
        for idir in BASE_DIRS:
            os.rename(idir[:-1], idir)
    make_image_dirs(EXTRA_DIRS)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("image_dir", help="Specify the image directory.")
    parser.add_argument("--astroberry", action="store_true",
                        help="Run script differently for astroberry acquired photos.")

    args = parser.parse_args()
    main(args)
