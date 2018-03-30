#!/usr/bin/env python

###############################################################################
#
# Author: Michael Reuter
# Date: March 30, 2018
#
# Script to rename movie files by looking at the file creation time.
#
###############################################################################

import argparse
from datetime import datetime
import os

VERSION = "1.0.0"


def make_description():
    result = []
    result.append("This program renames movie files based on the creation ")
    result.append("date of the file. The format is video_YYYYMMDD_HHMMSS.xxx.")
    return " ".join(result)


def check_filename(filename):
    return filename.lower().endswith('.mov')


def run(opts):
    for ifile in os.listdir('.'):
        if os.path.isfile(ifile) and check_filename(ifile):
            if opts.debug:
                print(ifile)
            stinfo = os.stat(ifile)
            dt = datetime.fromtimestamp(stinfo.st_mtime)
            datetime_tag = dt.strftime("%Y%m%d_%H%M%S")
            ofilename = "video_{}.{}".format(datetime_tag,
                                             ifile.split('.')[-1])
            if opts.debug:
                print(ofilename)
            else:
                os.rename(ifile, ofilename)
                os.chmod(ofilename, 0o644)


if __name__ == "__main__":
    default_format = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=make_description(),
                                     formatter_class=default_format)

    parser.add_argument("-d", "--debug", dest="debug", action="store_true",
                        help="Debug the program.")
    parser.add_argument("--version", action="version",
                        version="%(prog)s {}".format(VERSION))
    parser.set_defaults(debug=False, full=False)

    args = parser.parse_args()
    run(args)
