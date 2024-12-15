import argparse
from datetime import datetime
import os
import pathlib


def main(opts: argparse.Namespace) -> None:
    ffile: pathlib.Path = opts.file_to_fix.expanduser()
    mdate = datetime.strptime(opts.time_for_file, "%Y-%m-%dT%H:%M:%S")
    stinfo = ffile.stat()
    os.utime(ffile, (getattr(stinfo, f"st_{opts.stat_time}"), mdate.timestamp()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("file_to_fix", type=pathlib.Path, help="File to fix time.")
    parser.add_argument("time_for_file", type=str, help="Timestamp for file in YYY-MM-DDTHH:MM:SS")

    parser.add_argument("-s", "--stat-time", choices=["mtime", "ctime", "atime"], default="mtime",
                        help="Stat time property to fix.")

    args = parser.parse_args()

    main(args)
