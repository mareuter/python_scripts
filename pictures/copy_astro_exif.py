#!/usr/bin/env python

import argparse
import csv
import os
import subprocess

from PIL import ExifTags, Image

CSV_FILE = "temp.csv"
EXIF_TAGS = [ExifTags.Base.ApertureValue, ExifTags.Base.DateTimeOriginal, ExifTags.Base.ExposureTime, ExifTags.Base.FNumber,
             ExifTags.Base.Flash, ExifTags.Base.FocalLength, ExifTags.Base.ISO, ExifTags.Base.Make, ExifTags.Base.Model,
             ExifTags.Base.ShutterSpeedValue]
FILE_EXTS = ["jpg", "tif", "tiff"]
VERSION = "1.0.0"


def make_description():
    result = []
    result.append("This program takes a set of TIF and/or JPEG images, a set")
    result.append("of corresponding CR2 (RAW) images, retrieves the EXIF")
    result.append("information from the RAW files, writes it to a CSV file")
    result.append("and then imports it into the TIF and/or JPEG files. The")
    result.append("script uses the exiftool program. It is assumed that the")
    result.append("TIF and/or JPEG files reside in the same directory.")
    return " ".join(result)


def run(opts):
    if opts.raw is not None:
        raw_dir = opts.raw
    else:
        raw_dir = "."
    raw_files = [f for f in os.listdir(raw_dir) if f.endswith("CR2")]

    for raw_file in raw_files:
        image = Image.open(os.path.join(opts.raw, raw_file))
        im = image.getexif().get_ifd(34665)
        image.close()
        new_tags = [k for k in im if k in EXIF_TAGS]
        new_info = [v for k, v in im.items() if k in EXIF_TAGS]

        if opts.debug:
            print(new_tags)
            print(new_info)

        file_head = raw_file.split('.')[0]
        for extension in FILE_EXTS:
            ifile = "{}.{}".format(file_head, extension)
            if os.path.exists(ifile):
                write_csv(new_tags, new_info, ifile)
                print(ifile)
                cmd = ["exiftool", "-csv={}".format(CSV_FILE), "-overwrite_original", ifile]
                if opts.debug:
                    print(cmd)
                output = subprocess.check_output(cmd)
                if opts.debug:
                    print(output)
                os.remove(CSV_FILE)


def write_csv(tags, info, sfile):
    wtags = ["SourceFile"] + tags
    winfo = [sfile] + info

    with open(CSV_FILE, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(wtags)
        writer.writerow(winfo)


if __name__ == "__main__":
    default_format = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=make_description(), formatter_class=default_format)

    parser.add_argument("-d", "--debug", dest="debug", action="store_true",
                        help="Debug the program.")
    parser.add_argument("-r", "--raw", dest="raw",
                        help="Provide a separate path to RAW files.")
    parser.add_argument("--version", action="version",
                        version="%(prog)s {}".format(VERSION))
    parser.set_defaults(debug=False)

    args = parser.parse_args()
    run(args)
