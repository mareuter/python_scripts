import csv
from datetime import datetime, timedelta
import os
import re
import sys

import pytz

CHANNEL_MATCH = re.compile(r'\d')
INPUT_DATE_FORMAT = "%Y/%m/%d %H:%M"
MEASUREMENTS = ["temperature", "humidity", "dewpoint", "heatIndex"]


def make_point(meas_time, meas_name, meas_value, channel):
    isostring = meas_time.isoformat()
    try:
        return {
            'time': isostring,
            'measurement': meas_name,
            'tags': {'channel': str(channel)},
            'fields': {'value': float(meas_value)}
        }
    except ValueError:
        return None


def main():
    try:
        ifilename = os.path.expanduser(os.path.expandvars(sys.argv[1]))
    except IndexError:
        print("Usage: ingest_data.py <path to data CSV file>")
        sys.exit(255)

    time_zone = pytz.timezone('US/Arizona')

    channel_number = int(CHANNEL_MATCH.findall(os.path.basename(ifilename))[-1])
    # print(channel_number)
    with open(ifilename) as ifile:
        rows = csv.reader(ifile)
        for i, row in enumerate(rows):
            # print(row)
            # print(row[0])
            if i == 0:
                # Skip the header
                continue
            measurement_time = datetime.strptime(row[0], INPUT_DATE_FORMAT)
            measurement_time += timedelta(seconds=channel_number)
            measurement_time = time_zone.localize(measurement_time)
            measurement_time_utc = measurement_time.astimezone(pytz.utc)
            for j in range(1, 5):
                value = row[j]
                measurement = MEASUREMENTS[j - 1]
                point = make_point(measurement_time_utc, measurement, value, channel_number)
                if point is not None:
                    pass
                    # print(point)
                else:
                    print(f"Bad value for {measurement} ({measurement_time})")


if __name__ == '__main__':
    main()
