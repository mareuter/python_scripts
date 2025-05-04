import argparse
import os
import pathlib
import sys

import check_data
import constants
import copy_data


def main(opts: argparse.Namespace) -> None:
    if pathlib.Path.cwd() != constants.DATA_DIRECTORY:
        print(f"Please run from {str(constants.DATA_DIRECTORY)}")
        sys.exit(255)

    data_directories = copy_data.main()
    for data_directory in data_directories:
        if data_directory is None:
            continue
        print(f"Processing {str(data_directory)} directory")
        os.chdir(data_directory)

        for item in pathlib.Path.cwd().iterdir():
            if not item.is_file():
                continue
            check_data.main(item, data_directory, opts)

        os.chdir(constants.DATA_DIRECTORY)

    os.chdir(data_directories[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--debug", action="store_true", help="Print debugging.")

    args = parser.parse_args()

    main(args)
