import argparse
import json
import os
import pathlib
import subprocess as sp

TOP_DIR = pathlib.Path("~/DosGames").expanduser()
CONFIG_DIR = TOP_DIR / "config"
RUNNER = "flatpak run com.dosbox_x.DOSBox-X"
MEDIA_OPTIONS = {
    "floppy": "-t floppy",
    "cdrom": "-t iso"
}


def main(opts: argparse.Namespace) -> None:

    media_config = []
    media_conf_file = None
    if opts.media is not None:
        with opts.media.open() as ifile:
            media = json.load(ifile)
            media_conf_file = pathlib.Path("media.conf")
            with media_conf_file.open("w") as ofile:
                ofile.write("[autoexec]" + os.linesep)
                for item in media["media"]:
                    media_drive = item["drive"]
                    media_type = item["type"]
                    media_option = MEDIA_OPTIONS[media_type]
                    media_list = " ".join([str(TOP_DIR / media_type / x) for x in item["files"]])
                    media_mount = f"IMGMOUNT {media_drive} {media_list} {media_option}"
                    ofile.write(media_mount + os.linesep)

        media_config.append("-conf")
        media_config.append(media_conf_file.name)

    cmd = RUNNER.split()

    cmd.extend(media_config)
    cmd.append("-conf")
    cmd.append(str(CONFIG_DIR / f"{opts.windows}.conf"))

    if opts.debug:
        print(cmd)

    proc = sp.run(cmd, capture_output=True)
    if opts.debug:
        for line in proc.stdout.decode().split(os.linesep):
            print(line)

    if media_conf_file is not None:
        media_conf_file.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("windows", help="The flavor of windows to run.")
    parser.add_argument("-m", "--media", type=pathlib.Path, help="Specify a file with media to mount.")
    parser.add_argument("--debug", dest="debug", action="store_true")

    args = parser.parse_args()
    main(args)
