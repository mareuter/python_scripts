#!/usr/bin/env python
import calendar
from datetime import datetime, timedelta
import sys

INPUT_DATE_FORMAT = "%Y/%m/%d"
OUTPUT_DATE_FORMAT = "%Y/%m"
ONE_DAY = timedelta(days=1)

if len(sys.argv) < 5:
    print("Usage: tax_split.py <begin date> <end date> <separate> <tax>")
    sys.exit(255)

begin_date = datetime.strptime(sys.argv[1], INPUT_DATE_FORMAT)
end_date = datetime.strptime(sys.argv[2], INPUT_DATE_FORMAT)
is_separate = bool(sys.argv[3])
try:
    tax = float(sys.argv[4])
except ValueError:
    tax = eval(sys.argv[4])

if not is_separate:
    begin_date += ONE_DAY

t = (begin_date.year, begin_date.month)
end_of_month = datetime(t[0], t[1], calendar.monthrange(t[0], t[1])[1])

total_days = (end_date - begin_date).days + 1
begin_month_days = (end_of_month - begin_date).days + 1
end_month_days = total_days - begin_month_days

fraction = begin_month_days / total_days
begin_month_tax = fraction * tax
end_month_tax = tax - begin_month_tax

begin_month_tax_str = f"{begin_month_tax:.2f}"
end_month_tax_str = f"{end_month_tax:.2f}"
tax_str = f"{(float(begin_month_tax_str) + float(end_month_tax_str)):.2f}"
original_tax_str = f"{tax:.2f}"

try:
    assert original_tax_str == tax_str
except AssertionError:
    print(f"Original tax: {original_tax_str}")
    print(f"Calculated sum: {tax_str}")
    raise

print(f"{begin_date.strftime(OUTPUT_DATE_FORMAT)} Tax: ${begin_month_tax_str}")
print(f"{end_date.strftime(OUTPUT_DATE_FORMAT)} Tax: ${end_month_tax_str}")
