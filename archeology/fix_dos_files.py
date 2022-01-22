#!/usr/bin/env python
import pathlib
import sys


EXECUTABLES = ["BAT", "COM", "EXE"]


def process_dir(src_dir):
    for ipath in src_dir.iterdir():
        # print(ipath)
        if ipath.is_file():
            suffix = ipath.suffix.lstrip(".")
            # print(ipath, suffix)
            if suffix not in EXECUTABLES:
                ipath.chmod(0o644)

        if ipath.is_dir():
            # print(f"Directory found: {ipath}")
            process_dir(ipath)
    # print("Done process_dir")


def main():
    if len(sys.argv) < 2:
        print("Usage: fix_dos_files.py <dir>")
        sys.exit(255)

    source_dir = pathlib.Path(sys.argv[1])
    process_dir(source_dir)


if __name__ == '__main__':
    main()
