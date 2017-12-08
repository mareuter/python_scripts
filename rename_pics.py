#!/usr/bin/env python

###############################################################################
#
# Author: Michael Reuter
# Date: December 1, 2017
#
# Script to rename picture files by reading the EXIF tags. 
#
# Uses pyexifinfo.
#
###############################################################################

VERSION="1.0.0"

from datetime import datetime
import pyexifinfo
import os

def make_description():
    result = []
    result.append("This program renames picture files based on the date")
    result.append("contained within the EXIF information. The default")
    result.append("format is a hex value for the month followed by a two")
    result.append("digit number for the date. Thes original 4 digit picture")
    result.append("is left alone. An option can be used to make the string")
    result.append("YYYYMMDD.")
    return " ".join(result)

def rename_pic(ifilename, opt):
    im = pyexivinfo.information(ifilename)
    dt = datetime.strptime("%Y:%m:%d %H:%M:%S", im["EXIF:CreateDate"])
    if opt.full:
        tag = "{}{:02d}{:02d}".format(dt.year, dt.month, dt.day)
    else:
        tag = "%x%02d" % (dt.month, dt.day)
    ofilename = "I%s%s" % (tag.upper(), ifilename.split('_')[-1])
    if opt.debug:
        print ofilename
    else:
        os.rename(ifilename, ofilename)
    os.chmod(ofilename, 0o644)

def check_filename(filename):
    return filename.lower().endswith('.jpg') or \
           filename.lower().endswith('.tif') or \
           filename.lower().endswith('.cr2')

def run(opts):
    for pfile in os.listdir('.'):
        if os.path.isfile(pfile) and check_filename(pfile):
            if pfile.startswith('IMG'):
                rename_pic(pfile, opts)

if __name__ == "__main__":
    import optparse
    
    parser = optparse.OptionParser("usage: %prog [options]",
                                   version=VERSION,
                                   description=make_description())

    parser.add_option("-d", "--debug", dest="debug", action="store_true",
                      help="Debug the program.")
    parser.add_option("-f", "--full", dest="full", action="store_true",
                      help="Make tag YYYYMMDD.")
    parser.set_defaults(debug=False, full=False)

    (options, args) = parser.parse_args()
    run(options)
