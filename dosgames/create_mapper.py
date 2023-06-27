import argparse
import json
import os
import pathlib


def main(opts: argparse.Namespace) -> None:
    with opts.mapper.open() as mfile:
        mapper_lines = mfile.readlines()
    controller_config = json.loads(pathlib.Path(f"{opts.controller}.json").read_text())
    game_key_map = json.loads(opts.game_mapping.read_text())[opts.controller] 

    new_mapper = opts.mapper.parent / opts.controller / opts.game_mapping.name
    new_mapper = new_mapper.with_suffix(".map")

    game_keys = list(game_key_map.keys())

    game_mapper = []
    for mapper_line in mapper_lines:
        try:
            map_key, values = mapper_line.strip().split(maxsplit=1)
        except ValueError:
            map_key = mapper_line.strip()
        if map_key in game_keys:
            new_mapper_line = [map_key]
            controller_map = game_key_map[map_key]["map"]
            for value in controller_map:
                new_mapper_line.append(f'"{controller_config[value]}"')
            new_mapper_line.append(values)
            game_mapper.append(" ".join(new_mapper_line) + os.linesep)
        else:
            game_mapper.append(mapper_line)

    new_mapper.parent.mkdir(parents=True, exist_ok=True)
    new_mapper.write_text("".join(game_mapper))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("controller", help="The controller for mapping.")
    parser.add_argument("mapper", type=pathlib.Path, help="Blank mapping file.")
    parser.add_argument("game_mapping", type=pathlib.Path, help="Key mapping file for game.")

    args = parser.parse_args()
    main(args)