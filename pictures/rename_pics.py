#!/usr/bin/env python

###############################################################################
#
# Author: Michael Reuter
# Date: April 20, 2025
#
# Script to rename picture files by reading the EXIF tags.
#
###############################################################################

import argparse
from datetime import datetime
import os

from PIL import ExifTags, Image

VERSION = "2.0.0"


def make_description():
    result = []
    result.append("This program renames picture files based on the date")
    result.append("contained within the EXIF information. The default")
    result.append("format is a hex value for the month followed by a two")
    result.append("digit number for the date. Thes original 4 digit picture")
    result.append("is left alone. An option can be used to make the string")
    result.append("YYYYMMDD.")
    return " ".join(result)


def rename_pic(ifilename, opt, label="I"):
    image = Image.open(ifilename)
    im = image.getexif().get_ifd(34665)
    image.close()
    pic_time = im[ExifTags.Base.DateTimeOriginal]
    dt = datetime.strptime(pic_time, "%Y:%m:%d %H:%M:%S")
    if label == "I":
        tag = f"{dt.year}{dt.month:02d}{dt.day:02d}" if opt.full else f"{dt.month:X}{dt.day:02d}"
        ofilename = "{}{}{}".format(label, tag.upper(), ifilename.split('_')[-1])
    else:
        if opt.full:
            tag = f"{dt.year}{dt.month:02d}{dt.day:02d}{dt.hour:02d}{dt.minute:02d}{dt.second:02d}"
        else:
            tag = f"{dt.month:X}{dt.day:02d}{dt.hour:02d}{dt.minute:02d}{dt.second:02d}"
        ofilename = "{}{}.{}".format(label, tag.upper(), ifilename.split('.')[-1])
    if opt.debug:
        print(ofilename)
    else:
        os.rename(ifilename, ofilename)
        os.chmod(ofilename, 0o644)


def check_filename(filename):
    return filename.lower().endswith('.jpg') or \
           filename.lower().endswith('.tif') or \
           filename.lower().endswith('.tiff') or \
           filename.lower().endswith('.cr2')


def run(opts):
    for pfile in os.listdir('.'):
        if os.path.isfile(pfile) and check_filename(pfile):
            if opts.debug:
                print(pfile)
            if pfile.startswith('IMG'):
                rename_pic(pfile, opts)
            elif pfile[0].isdigit() or pfile.startswith("Photo"):
                rename_pic(pfile, opts, label="V")
            else:
                print(f"Don't know how to handle {pfile}")


if __name__ == "__main__":
    default_format = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=make_description(),
                                     formatter_class=default_format)

    parser.add_argument("-d", "--debug", dest="debug", action="store_true",
                        help="Debug the program.")
    parser.add_argument("-f", "--full", dest="full", action="store_true",
                        help="Make tag YYYYMMDD.")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {VERSION}")
    parser.set_defaults(debug=False, full=False)

    args = parser.parse_args()
    run(args)
