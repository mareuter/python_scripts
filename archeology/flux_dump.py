#!/usr/bin/env python
import argparse
import pathlib
import subprocess as sp


def check_and_mkdir(dir: pathlib.Path) -> None:
    if not dir.exists():
        dir.mkdir()


def main(opts: argparse.Namespace) -> None:
    top_dir: pathlib.Path = pathlib.Path.cwd()
    dump_dir = opts.dump_dir
    check_and_mkdir(top_dir / dump_dir)

    if opts.subdir is not None:
        dump_dir = dump_dir / opts.subdir
        check_and_mkdir(top_dir / dump_dir)

    raw_dump_file = "DUMP00.0.raw"

    cmd = ["gw"]
    cmd.append("read")
    cmd.append(f"--drive {opts.drive}")
    cmd.append("--raw")
    cmd.append(f"{str(dump_dir / raw_dump_file)}")

    cmd_str = " ".join(cmd)
    if opts.verbose:
        print(cmd_str)

    with sp.Popen(
        cmd_str, stdout=sp.PIPE, stderr=sp.STDOUT, text=True, shell=True
    ) as proc:
        for stdout_line in iter(proc.stdout.readline, ""):
            print(stdout_line.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "drive", choices=["A", "B"], help="Select the drive letter to dump."
    )
    parser.add_argument(
        "dump_dir", type=pathlib.Path, help="Directory to dump flux files into."
    )
    parser.add_argument(
        "--subdir", type=pathlib.Path, help="Sub directory for multiple disks."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Add verbosity to program."
    )

    args = parser.parse_args()
    main(args)
