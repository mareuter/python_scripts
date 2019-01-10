#!/usr/bin/env python

import argparse
import csv
import os
import pyexifinfo
import subprocess

CSV_FILE = "temp.csv"
SINGLE_EXIF_TAGS = ['EXIF:ApertureValue', 'EXIF:FNumber', 'EXIF:Flash', 'EXIF:FocalLength',
                    'EXIF:ISO', 'EXIF:Make', 'EXIF:Model', 'EXIF:ShutterSpeedValue']
MULTI_EXIF_TAGS = ['EXIF:DateTimeOriginal', 'EXIF:ExposureTime']
FILE_EXTS = ["jpg", "tif", "tiff"]
VERSION = "1.0.0"


def make_description():
    result = []
    result.append("This program takes a set of TIF and/or JPEG images, a path")
    result.append("to the set of selected files, a set of corresponding CR2")
    result.append("(RAW) images, retrieves the EXIF information from the RAW")
    result.append("files that correspond to the selected set, writes it to a")
    result.append("CSV file and then imports it into the TIF and/or JPEG ")
    result.append("files. The script uses the exiftool program. It is assumed")
    result.append("that the TIF and/or JPEG files reside in the same")
    result.append("directory.")
    return " ".join(result)


def run(opts):
    selected_files = [f for f in os.listdir(opts.selected) if os.path.isfile(os.path.join(opts.selected, f))]
    selected_heads = ["_".join(f.split("_")[:2]) for f in selected_files if not f.startswith(".")]

    raw_files = [f for f in os.listdir(opts.raw) if f.endswith("CR2")]
    new_info = None
    if opts.debug:
        print(selected_heads)
        print(raw_files)
    images_dates = []
    exposure_times = []

    for raw_file in raw_files:
        is_raw_selected = False
        for selected_head in selected_heads:
            if selected_head in raw_file:
                is_raw_selected = True
                break

        if not is_raw_selected:
            continue
        print(raw_file)
        im = pyexifinfo.information(os.path.join(opts.raw, raw_file))
        # Take information that doesn't change per image from the first available.
        if new_info is None:
            new_info = {k: v for k, v in im.items() if k in SINGLE_EXIF_TAGS}
            if opts.debug:
                print(new_info)
        images_dates.append(im[MULTI_EXIF_TAGS[0]])
        exposure_times.append(im[MULTI_EXIF_TAGS[1]])

    if opts.debug:
        print(images_dates)
        print(exposure_times)

    new_info[MULTI_EXIF_TAGS[1]] = sum(exposure_times)
    new_info[MULTI_EXIF_TAGS[0]] = min(images_dates)
    if opts.debug:
        print(new_info)

    pic_file_head = opts.pic_file.split('.')[0]
    for extension in FILE_EXTS:
        ifile = "{}.{}".format(pic_file_head, extension)
        if os.path.exists(ifile):
            write_csv(list(new_info.keys()), list(new_info.values()), ifile)
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
    parser.add_argument("-r", "--raw", dest="raw", required=True,
                        help="Provide a path to RAW files.")
    parser.add_argument("-s", "--selected", dest="selected", required=True,
                        help="Provide a path to the selected files.")
    parser.add_argument("--version", action="version",
                        version="%(prog)s {}".format(VERSION))
    parser.add_argument("pic_file", help="Picture file for EXIF data insertion.")
    parser.set_defaults(debug=False)

    args = parser.parse_args()
    run(args)
