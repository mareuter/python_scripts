import argparse
import pathlib
import subprocess as sp

GAMES_DIR = pathlib.Path.home() / "DosGames"
CONFIG_DIR = GAMES_DIR / "config"
FLOPPY_DIR = GAMES_DIR / "floppy"
CDROM_DIR = GAMES_DIR / "cdrom"
TEST_DIR = GAMES_DIR / "test"
RUNNERS = {
    "dosbox-x": {
        "config": CONFIG_DIR / "dosbox-x.reference.conf",
        "exec_path": "flatpak run com.dosbox_x.DOSBox-X"
    },
    "dosbox": {
        "config": CONFIG_DIR / "dosbox-0.74-3.conf"
    },
    "dosbox-staging": {
        "config": CONFIG_DIR / "dosbox-staging.conf",
        "exec_path": "/opt/retropie/emulators/dosbox-staging/bin/dosbox"
    }
}


def main(opts: argparse.Namespace) -> None:
    if opts.media_type == "floppy":
        media_drive = "A"
        media_directory = FLOPPY_DIR
        media_option = "-t floppy"
    if opts.media_type == "cdrom":
        media_drive = "D"
        media_directory = CDROM_DIR
        media_option = "-t iso"

    try:
        runner = RUNNERS[opts.runner]["exec_path"]
    except KeyError:
        runner = opts.runner

    if opts.verbose:
        print(opts.media)

    if "*" in opts.media:
        files = sorted([f":{str(x)}" for x in media_directory.glob(opts.media)])
    else:
        files = [f":{str(media_directory / opts.media)}"]

    media_line = []
    media_line.append(f"IMGMOUNT {media_drive}")
    media_line.extend(files)
    media_line.append(media_option)

    cmd = []
    if type(runner) == list:
        cmd.extend(runner)
    else:
        cmd.append(runner)
    cmd.append("-conf")
    cmd.append(str(RUNNERS[opts.runner]["config"]))
    cmd.append("-set ver=6.22")
    cmd.append("-c")
    cmd.append(f'"{" ".join(media_line)}"')
    cmd.append("-c")
    cmd.append(f'"MOUNT C {TEST_DIR}"')
    cmd.append("-c")
    cmd.append("A:")

    if opts.verbose:
        print(" ".join(cmd))

    with sp.Popen(" ".join(cmd), stdout=sp.PIPE, stderr=sp.STDOUT, text=True, shell=True) as proc:
        for stdout_line in iter(proc.stdout.readline, ""):
            print(stdout_line.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("media_type", choices=["floppy", "cdrom"], help="Set the media type")
    parser.add_argument("media", help="List or glob of images.")
    parser.add_argument("-r", "--runner", default="dosbox-x", choices=["dosbox", "dosbox-x", "dosbox-staging"], help="Pick the runner.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase script verbosity.")

    args = parser.parse_args()
    main(args)