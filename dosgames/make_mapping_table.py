import argparse
import json
import pathlib

from prettytable import MARKDOWN, PrettyTable


def main(opts: argparse.Namespace) -> None:
    game_key_map = json.loads(opts.game_mapping.read_text())
    print(f"{game_key_map['game']} Mapping for {opts.controller}")
    print()

    table = PrettyTable()
    if opts.markdown:
        table.set_style(MARKDOWN)
    table.field_names = ["Action", "Controller"]
    table.align["Action"] = "l"
    table.align["Controller"] = "l"

    rows = []
    for action in game_key_map["actions"]:
        action_name = action["name"]
        action_map = action["key"][opts.controller]
        rows.append([action_name, ", ".join(action_map)])
    table.add_rows(rows)

    print(table)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("game_mapping", type=pathlib.Path,
                        help="The mapping file with the game configuration.")
    parser.add_argument("controller", help="The controller type for the table.")
    parser.add_argument("-m", "--markdown", action="store_true", help="Format table in Markdown.")

    args = parser.parse_args()
    main(args)
