#!/usr/bin/env python
import argparse
import contextlib
import pathlib

SCRIPTS = {
    "pictures": [
        "create_astroimg.py",
        "create_photo.py",
        "rename_pics.py"
    ],
    "movies": [
        "rename_movies.py"
    ],
    "sysadmin": [
        "rsync.py",
        "sorted_du.py"
    ]
}


def main(opts: argparse.Namespace) -> None:
    user_home = pathlib.Path("~").expanduser()
    user_bin = user_home / "bin"

    with contextlib.chdir(user_bin):
        for directory, scripts in SCRIPTS.items():
            for script in scripts:
                link = user_home / opts.git_dir / "python_scripts" / directory / script
                pathlib.Path(script).symlink_to(link)


if __name__ == '__main__':
    description = ["Link scripts into user bin directory."]
    parser = argparse.ArgumentParser(
        description=" ".join(description),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-git-dir", type=pathlib.Path, default=pathlib.Path("git/me"), help="Alternate git location."
    )

    args = parser.parse_args()
    main(args)
