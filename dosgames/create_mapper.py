import argparse
import json
import os
import pathlib


def find_mapping(key: str, mapping: dict, controller: str) -> list | None:
    cmap = None
    for key_map in mapping:
        if key_map["key"]["name"] == key:
            cmap = key_map["key"][controller]
            break
    return cmap


def main(opts: argparse.Namespace) -> None:
    with opts.mapper.open() as mfile:
        mapper_lines = mfile.readlines()
    controller_config = json.loads(pathlib.Path(f"{opts.controller}.json").read_text())
    game_key_map = json.loads(opts.game_mapping.read_text())["actions"]

    new_mapper = opts.mapper.parent / opts.controller / opts.game_mapping.name
    new_mapper = new_mapper.with_suffix(".map")

    game_keys = [x["key"]["name"] for x in game_key_map]

    game_mapper = []
    for mapper_line in mapper_lines:
        try:
            map_key, values = mapper_line.strip().split(maxsplit=1)
        except ValueError:
            map_key = mapper_line.strip()
        if map_key in game_keys:
            new_mapper_line = [map_key]
            controller_map = find_mapping(map_key, game_key_map, opts.controller)
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
    parser.add_argument(
        "game_mapping", type=pathlib.Path, help="Key mapping file for game."
    )

    args = parser.parse_args()
    main(args)
