import argparse
import json
import os
import pathlib
import subprocess as sp

import encoders

TOPLEVEL_DIR = pathlib.Path("~/DosGames").expanduser()
GAMES_DIR = TOPLEVEL_DIR / "hdd/GAMES"
FLOPPY_DIR = TOPLEVEL_DIR / "floppy"
CDROM_DIR = TOPLEVEL_DIR / "cdrom"
CONFIG_DIR = TOPLEVEL_DIR / "config"

RETROPIE_DIR = pathlib.Path("~/").expanduser() / "RetroPie" / "roms" / "pc"
NEW_CONFIG_DIR = TOPLEVEL_DIR / "setup" / "conf"
DBS_DIR = "/opt/retropie/emulators/dosbox-staging/bin/dosbox \\"

DEFAULT_RUNNER = "dosbox"
DEFAULT_PROFILE = "default.conf"

GAME_INFORMATION = "game_information.json"


def main(opts):

    games = None
    with open(GAME_INFORMATION) as ifile:
        games = json.load(ifile, object_hook=encoders.decode_game_information)
   
    try:
        game = [x for x in games if x.key == opts.game_key][0]
    except IndexError:
        raise RuntimeError(f"{opts.game_key} cannot be found!")

    use_media = game.media is not None
    if use_media:
        if game.media_type == "floppy":
            media_drive = "A"
            media_directory = FLOPPY_DIR
            media_option = "-t floppy"
        if game.media_type == "cdrom":
            media_drive = "D"
            media_directory = CDROM_DIR
            media_option = "-t iso"

    cmd = []
    cmd.append(DEFAULT_RUNNER)
    cmd.append("-conf")
    cmd.append(CONFIG_DIR / DEFAULT_PROFILE)
    cmd.append("-conf")
    cmd.append(CONFIG_DIR / "larger-window.conf")
    if game.extra_profiles is not None:
        for extra_profile in game.extra_profiles:
            cmd.append("-conf")
            cmd.append(CONFIG_DIR / extra_profile)
    if use_media:
        media_list = " ".join([str(media_directory / x) for x in game.media])
        cmd.append("-c")
        cmd.append(f"\"IMGMOUNT {media_drive} {media_list} {media_option}\"")
    cmd.append("-c")
    cmd.append(f"MOUNT C {GAMES_DIR}")
    if game.media_only:
        cmd.append("-c")
        cmd.append(f"{media_drive}:")
    else:
        cmd.append("-c")
        cmd.append("C:")
        cmd.append("-c")
        cmd.append(f"CD C:\{game.directory}")
    cmd.append("-c")
    cmd.append(game.executable)
    if opts.exit:
        cmd.append("-c")
        cmd.append("EXIT")

    if opts.debug:
        print(" ".join([str(x) for x in cmd]))
    if not opts.write:
        proc = sp.run(cmd, capture_output=True)
        if opts.debug:
            for line in proc.stdout.decode().split(os.linesep):
                print(line)
    else:
        script_name = game.full_name.replace("'", "")
        script = pathlib.Path(RETROPIE_DIR / f"{script_name}.sh")
        conf_file = NEW_CONFIG_DIR / f"{game.key.lower()}.conf"
        with script.open("w") as sfile:
            sfile.write("#!/bin/bash" + os.linesep)
            sfile.write(DBS_DIR + os.linesep)
            sfile.write(f"-conf {str(conf_file)}" + os.linesep)
        script.chmod(0o755)

        with conf_file.open("w") as cfile:
            cfile.write("[autoexec]" + os.linesep)
            for x in cmd[1:]:
                print(x, type(x))
                if x in ["-c", "-conf"]:
                    continue
                try:
                    if x.suffix == ".conf":
                        continue
                except AttributeError:
                    pass
                if "C:\\" in x:
                    x = x[:3] + x[6:]
                cfile.write(str(x) + os.linesep)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("game_key")

    parser.add_argument("--exit", dest="exit", action="store_true")
    parser.add_argument("--debug", dest="debug", action="store_true")
    parser.add_argument("--write", dest="write", action="store_true")

    args = parser.parse_args()
    main(args)
