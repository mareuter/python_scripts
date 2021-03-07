import argparse
import pathlib


def main(opts):
    cur_dir = pathlib.Path(".")
    picture_files = cur_dir.glob("*.cr2")
    for picture_file in picture_files:
        fix_filename = "".join([opts.pic_type, picture_file.name.split(opts.pic_type)[1]])
        # print(fix_filename)
        picture_file.rename(pathlib.Path(fix_filename))


if __name__ == '__main__':
    description = ["Fix astroberry filenames. Run this in the needed directory."]

    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("pic_type", help="The picture type to fix the filename.")

    args = parser.parse_args()

    main(args)
