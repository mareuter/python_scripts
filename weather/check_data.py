import argparse
import os
import pathlib
import shutil

import constants

SPLIT_CHAR = b"\r\n"
EMPTY_LINE = b""
BAD_DATA_BYTE = b"\x00"
BAD_DATA_DIR = pathlib.Path("bad_data")


def main(
    input_file: pathlib.Path, copy_subdir: pathlib.Path, opts: argparse.Namespace
) -> None:
    found_bad_data = False
    good_lines = []
    bytes = input_file.read_bytes()
    byte_lines = bytes.split(SPLIT_CHAR)
    for byte_line in byte_lines:
        if byte_line == EMPTY_LINE:
            continue

        if opts.debug:
            print(byte_line)
        bad_byte_index = byte_line.find(BAD_DATA_BYTE)
        if bad_byte_index == -1:
            if opts.debug:
                print(byte_line)
            good_lines.append(byte_line.decode() + os.linesep)
        else:
            # Last bit of bad block has a good entry in it
            right_index = byte_line.rfind(BAD_DATA_BYTE) + 1
            good_lines.append(byte_line[right_index:].decode() + os.linesep)
            found_bad_data = True

    if opts.debug:
        print(good_lines)

    if found_bad_data:
        print(f"Bad data in {str(input_file)}")
        tmp_file = pathlib.Path("temp.csv")
        with tmp_file.open("w") as ofile:
            ofile.writelines(good_lines)

        copy_dir = constants.DATA_DIRECTORY / BAD_DATA_DIR / copy_subdir
        copy_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(input_file.name, copy_dir)
        tmp_file.rename(input_file)
    else:
        print(f"{str(input_file)} OK!")
