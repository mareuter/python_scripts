import argparse
import os
import pathlib
import subprocess as sp


def main(opts):
    TOPLEVEL_DIR = pathlib.Path("~/DosGames").expanduser()
    GAMES_DIR = TOPLEVEL_DIR / "hdd/GAMES"
    CONFIG_DIR = TOPLEVEL_DIR / "config"

    DEFAULT_RUNNER = "dosbox"
    DEFAULT_PROFILE = "default.conf"

    basic_games = GAMES_DIR / "BASGAMES"
    game_listing = {}
    for i, basic_game in enumerate(basic_games.iterdir()):
        game_listing[i + 1] = basic_game.name
    for index, game in game_listing.items():
        if index < 10:
            spacing = "  "
        else:
            spacing = " "
        print(f"{index}:{spacing}{game}")
    game_index = int(input("Pick index of game to play: "))
    bas_game = game_listing[game_index]

    cmd = []
    cmd.append(DEFAULT_RUNNER)
    cmd.append("-conf")
    cmd.append(CONFIG_DIR / DEFAULT_PROFILE)
    cmd.append("-conf")
    cmd.append(CONFIG_DIR / "larger-window.conf")
    cmd.append("-c")
    cmd.append(f"MOUNT C {GAMES_DIR}")
    cmd.append("-c")
    cmd.append("C:")
    cmd.append("-c")
    cmd.append("CD BASGAMES")
    cmd.append("-c")
    cmd.append(f"C:\PROGRAMS\BASICA.EXE {game_listing[game_index]}")
    if opts.exit:
        cmd.append("-c")
        cmd.append("EXIT")

    proc = sp.run(cmd, capture_output=True)
    if opts.debug:
        for line in proc.stdout.decode().split(os.linesep):
            print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--exit", dest="exit", action="store_true")
    parser.add_argument("--debug", dest="debug", action="store_true")

    args = parser.parse_args()
    main(args)
