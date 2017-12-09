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

def rename_pic(ifilename, opt, label="I"):
    im = pyexifinfo.information(ifilename)
    pic_time = im["EXIF:DateTimeOriginal"]
    dt = datetime.strptime(pic_time, "%Y:%m:%d %H:%M:%S")
    if label == "I":
        if opt.full:
            tag = "{}{:02d}{:02d}".format(dt.year, dt.month, dt.day)
        else:
            tag = "{:X}{:02d}".format(dt.month, dt.day)
        ofilename = "{}{}{}".format(label, tag.upper(), ifilename.split('_')[-1])
    else:
        if opt.full:
            tag = "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(dt.year, dt.month,
                                                            dt.day, dt.hour,
                                                            dt.minute, dt.second)
        else:
            tag = "{:X}{:02d}{:02d}{:02d}{:02d}".format(dt.month, dt.day, dt.hour,
                                                        dt.minute, dt.second)
        ofilename = "{}{}.{}".format(label, tag.upper(), ifilename.split('.')[-1])
    if opt.debug:
        print(ofilename)
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
            if opts.debug:
                print(pfile)
            if pfile.startswith('IMG'):
                rename_pic(pfile, opts)
            elif pfile[0].isdigit() or pfile.startswith("Photo"):
                rename_pic(pfile, opts, label="V")
            else:
                print("Don't know how to handle {}".format(pfile))

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
