#!/usr/bin/env python
import pathlib
import shutil
import sys

if len(sys.argv) < 3:
    print("Usage: copy_dos_games.py <src> <destination>")
    sys.exit(255)

source_dir = pathlib.Path(sys.argv[1])
destination_dir = pathlib.Path(sys.argv[2])

if not destination_dir.exists():
    print(f"Destination directory: {destination_dir} does not exist!")
    sys.exit(254)

for ipath in source_dir.rglob("*"):
    # print(ipath)
    if ipath.is_file():
        opath = destination_dir / ipath.name.upper()
        print(opath)
        shutil.copyfile(ipath, opath)

    if ipath.is_dir():
        print(f"Directory found: {ipath}")
