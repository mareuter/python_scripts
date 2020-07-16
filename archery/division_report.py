import argparse
from dataclasses import dataclass
from datetime import datetime
from operator import attrgetter
import os
import subprocess
import sys

from openpyxl import load_workbook

# Map the spreadsheet columns
FIRST_NAME = 3
LAST_NAME = 4
MENS_DIVISION = 48
WOMENS_DIVISION = 49


# Archer class
@dataclass
class Archer:
    first_name: str
    last_name: str
    divison_type: str
    divison_bow: str
    divison_class: str


# Reporting orders
DIVISION_TYPE_ORDER = ["Men's", "Women's"]
DIVISION_BOW_ORDER = ["Recurve", "Compound"]
DIVISION_CLASS_ORDER = [
    "Master",
    "Senior",
    "Junior",
    "Cadet",
    "Cub",
    "Bowman",
    "Yeoman",
]


DATE_INPUT_FORMAT = "%Y/%m/%d"
DATE_OUTPUT_FORMAT = "%B %d, %Y"
DATE_FILE_FORMAT = "%Y%m%d"


def main(opts):
    try:
        ifile = os.path.expanduser(os.path.expandvars(opts.report_file))
    except IndexError:
        print("Usage: division_report.py <Input Spreadsheet>")

    workbook = load_workbook(ifile)
    sheet = workbook.active

    archers = []
    for row in sheet.iter_rows(min_row=3, values_only=True):
        if row[FIRST_NAME] is None:
            continue
        if row[MENS_DIVISION] is not None:
            divison_type = "Men's"
            division = row[MENS_DIVISION]
        if row[WOMENS_DIVISION] is not None:
            divison_type = "Women's"
            division = row[WOMENS_DIVISION]

        divison_bow, divison_class = division.split()

        archers.append(
            Archer(
                first_name=row[FIRST_NAME].title(),
                last_name=row[LAST_NAME].title(),
                divison_type=divison_type,
                divison_bow=divison_bow,
                divison_class=divison_class,
            )
        )

    if opts.tournament is None:
        tournament = "Tournament"
    else:
        tournament = opts.tournament

    if opts.date is None:
        tournament_date = datetime.now()
    else:
        tournament_date = datetime.strptime(opts.date, DATE_INPUT_FORMAT)

    report_lines = []
    report_lines.append("---" + os.linesep)
    report_lines.append(f"title: {tournament}" + os.linesep)
    report_lines.append("..." + os.linesep)
    report_lines.append(f"{tournament_date.strftime(DATE_OUTPUT_FORMAT)}" + os.linesep)
    report_lines.append(os.linesep)

    report_lines.append(f"Number of Registered Archers: {len(archers)}" + os.linesep)
    report_lines.append(os.linesep)

    for dto in DIVISION_TYPE_ORDER:
        for dbo in DIVISION_BOW_ORDER:
            for dco in DIVISION_CLASS_ORDER:
                class_archers = []
                for archer in archers:
                    if (
                        archer.divison_type == dto
                        and archer.divison_bow == dbo
                        and archer.divison_class == dco
                    ):
                        class_archers.append(archer)
                if class_archers:
                    report_list = sorted(class_archers, key=attrgetter("last_name"))
                    report_lines.append(f"### {dto} {dbo} {dco}" + os.linesep)
                    for class_archer in report_list:
                        full_name = (
                            f"{class_archer.first_name} {class_archer.last_name}"
                        )
                        report_lines.append(f"{full_name}  " + os.linesep)
                    report_lines.append(os.linesep)

    values = [x.lower() for x in tournament.split(" ")]
    values.append(tournament_date.strftime(DATE_FILE_FORMAT))
    file_name = "_".join(values)

    markdown_file = f"{file_name}.md"
    with open(markdown_file, "w") as rfile:
        rfile.writelines(report_lines)

    pdf_file = markdown_file.split(".")[0] + ".pdf"

    subprocess.run(
        ["pandoc", "-s", "--pdf-engine", "weasyprint", "-o", pdf_file, markdown_file]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "report_file",
        help="The Excel spreadsheet containing the USA Archery information",
    )
    parser.add_argument(
        "-t",
        "--tournament",
        dest="tournament",
        help="The name of the archery tournament",
    )
    parser.add_argument(
        "-d",
        "--date",
        dest="date",
        help="The date of the tournament in YYYY/MM/DD format.",
    )

    args = parser.parse_args()

    main(args)
