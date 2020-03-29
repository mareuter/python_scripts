#!/usr/bin/env python
import pathlib
import shutil
import sys


def process_dir(src_dir, dest_dir):
    for ipath in src_dir.iterdir():
        # print(ipath)
        if ipath.is_file():
            opath = dest_dir / ipath.name.upper()
            print(opath)
            shutil.copyfile(ipath, opath)

        if ipath.is_dir():
            # print(f"Directory found: {ipath}")
            new_dest_dir = dest_dir / ipath.name.upper()
            new_dest_dir.mkdir()
            process_dir(ipath, new_dest_dir)
    # print("Done process_dir")


def main():
    if len(sys.argv) < 3:
        print("Usage: copy_dos_games.py <src> <destination>")
        sys.exit(255)

    source_dir = pathlib.Path(sys.argv[1])
    destination_dir = pathlib.Path(sys.argv[2])

    if not destination_dir.exists():
        print(f"Destination directory: {destination_dir} does not exist!")
        sys.exit(254)

    process_dir(source_dir, destination_dir)


if __name__ == '__main__':
    main()
