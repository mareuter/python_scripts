import argparse
import json
from operator import attrgetter

import encoders

GAME_INFORMATION = "game_information.json"


def main(opts):
    games = None
    with open(GAME_INFORMATION) as ifile:
        games = json.load(ifile, object_hook=encoders.decode_game_information)

    sorted_games = sorted(games, key=attrgetter("key"))
    for sorted_game in sorted_games:
        print(sorted_game.listing())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    main(args)
