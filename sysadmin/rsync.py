#!/usr/bin/env python
import argparse
import os
import subprocess as sp

OPTIONS = {
    1: "video/",
    2: "photo/",
    3: "Picture_Backup/",
    4: "homes/mareuter/Photos/",
}


def run_cmd(command, as_lines=False):
    """Run a command via subprocess::run.

    Parameters
    ----------
    command : `list`
        The command to run.
    as_lines : `bool`, optional
        Return the output as a list instead of a string.

    Returns
    -------
    str or list
        The output from the command.
    """
    output = sp.run(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    decoded_output = output.stdout.decode("utf-8")
    if as_lines:
        return decoded_output.split(os.linesep)
    else:
        return decoded_output[:-1]


def main(opts):
    old_dir = os.getcwd()
    os.chdir(os.path.join(os.path.expanduser("~/"), "Backup"))

    print("Directories to backup:")
    for index, directory in OPTIONS.items():
        print(f"{index}: {directory}")
    indexes = input("Enter indexes (comma separated for multiple:")
    directories = [OPTIONS[int(x)] for x in indexes.split(",")]

    for directory in directories:
        to_dir = os.path.join("/Volumes", directory, "")
        if not os.path.exists(to_dir):
            print(f"Please mount {to_dir} before rsync. Skipping.")
            continue

        cmd = [
            "rsync",
            "-rptlDv",
            "--exclude-from=rsync_ignore.txt",
            directory,
            to_dir,
        ]
        print(" ".join(cmd))
        if not opts.no_run:
            print(run_cmd(cmd))

    os.chdir(old_dir)


if __name__ == "__main__":
    description = ["Run rsync backups for various directories."]
    parser = argparse.ArgumentParser(
        description=" ".join(description),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--no-run", action="store_true", help="Do not run the command.")

    args = parser.parse_args()
    main(args)
