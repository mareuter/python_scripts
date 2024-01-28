import datetime
import pathlib
import shutil
import sys

MEMORY_CARD_MOUNT = pathlib.Path("/Volumes/NO NAME")


def make_dir_and_copy_data(year: int) -> pathlib.Path | None:
    card_data_dir = MEMORY_CARD_MOUNT / "HISTORY"
    data_files = list(card_data_dir.glob(f"{year}*.CSV"))
    if not len(data_files):
        return None

    date_dir = pathlib.Path(str(year))
    if not date_dir.exists():
        date_dir.mkdir()

    dirs = [int(x.name) for x in date_dir.iterdir() if x.is_dir()]
    try:
        next_int = max(dirs) + 1
    except ValueError:
        next_int = 1
    next_dir = f"{next_int:02d}"
    data_dir = date_dir / next_dir
    data_dir.mkdir()
    for data_file in data_files:
        shutil.copy2(data_file, data_dir)

    return data_dir


def main() -> list[pathlib.Path]:
    if not MEMORY_CARD_MOUNT.exists():
        print("Please insert memory card into computer.")
        sys.exit(254)

    data_directories: list[pathlib.Path] = []

    now = datetime.datetime.now()
    now_year = now.year
    past_year = now_year - 1

    data_directories.append(make_dir_and_copy_data(now_year))
    data_directories.append(make_dir_and_copy_data(past_year))

    return data_directories
