#!/usr/bin/env python

import argparse
from datetime import datetime
import os

from PIL import ExifTags, Image

VERSION = "1.0.0"


def make_description():
    descr = []
    descr.append("This script determines the creation time from a picture's")
    descr.append("EXIF information and adjusts the picture's mtime")
    descr.append("attribute.")
    return " ".join(descr)


def check_filename(filename):
    return filename.lower().endswith('.jpg') or \
        filename.lower().endswith('.tif') or \
        filename.lower().endswith('.tiff') or \
        filename.lower().endswith('.cr2') or \
        filename.lower().endswith('.orf')


def run(opts):
    for pfile in os.listdir('.'):
        if os.path.isfile(pfile) and check_filename(pfile):
            if opts.debug:
                print(pfile)

            try:
                image = Image.open(pfile)
                im = image.getexif().get_ifd(34665)
                image.close()
                pic_time = im[ExifTags.Base.DateTimeOriginal]
                dt = datetime.strptime(pic_time, "%Y:%m:%d %H:%M:%S")

                stinfo = os.stat(pfile)
                os.utime(pfile, (stinfo.st_atime, dt.timestamp()))
            except KeyError:
                pass


if __name__ == "__main__":
    default_format = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=make_description(),
                                     formatter_class=default_format)

    parser.add_argument("-d", "--debug", dest="debug", action="store_true",
                        help="Debug the program.")
    parser.add_argument("--version", action="version",
                        version="%(prog)s {}".format(VERSION))
    parser.set_defaults(debug=False)

    args = parser.parse_args()
    run(args)
