import argparse
import json
import os
import pathlib
import subprocess as sp

import encoders

TOPLEVEL_DIR = pathlib.Path("~/DosGames").expanduser()
CONFIG_DIR = TOPLEVEL_DIR / "setup" / "conf"

RUNNERS = {
    "dosbox-x": {
        "exec_path": "flatpak run com.dosbox_x.DOSBox-X"
    },
    "dosbox": {
    },
    "dosbox-staging": {
        "exec_path": "/opt/retropie/emulators/dosbox-staging/bin/dosbox"
    }
}

GAME_INFORMATION = "game_information.json"


def main(opts):

    games = None
    with open(GAME_INFORMATION) as ifile:
        games = json.load(ifile, object_hook=encoders.decode_game_information)

    try:
        game = [x for x in games if x.key == opts.game_key][0]
    except IndexError:
        raise RuntimeError(f"{opts.game_key} cannot be found!") from None

    try:
        exec_path = RUNNERS[opts.runner]['exec_path']
        runner = exec_path.split() if " " in exec_path else exec_path
    except KeyError:
        runner = opts.runner

    cmd = []
    cmd.extend(runner) if isinstance(runner, list) else cmd.append(runner)
    cmd.append("-conf")
    cmd.append(str(CONFIG_DIR / f"{game.key.lower()}.conf"))

    if opts.debug:
        print(" ".join([str(x) for x in cmd]))

    proc = sp.run(cmd, capture_output=True)
    if opts.debug:
        for line in proc.stdout.decode().split(os.linesep):
            print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("game_key")
    parser.add_argument("-r", "--runner", default="dosbox-x",
                        choices=["dosbox", "dosbox-x", "dosbox-staging"], help="Pick the runner.")
    parser.add_argument("--debug", dest="debug", action="store_true")

    args = parser.parse_args()
    main(args)
