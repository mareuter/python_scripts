import argparse
import asyncio
import csv
from datetime import UTC, datetime, timedelta
import os
import pathlib
import re
from typing import NamedTuple
from zoneinfo import ZoneInfo

from aioinflux import FLOAT, MEASUREMENT, TAG, TIMESTR, InfluxDBClient, lineprotocol

CHANNEL_MATCH = re.compile(r"\d")
INPUT_DATE_FORMAT = "%Y/%m/%d %H:%M"
MEASUREMENTS = ["temperature", "humidity", "dewpoint", "heatIndex"]


@lineprotocol
class Measurement(NamedTuple):
    timestamp: TIMESTR
    measurement: MEASUREMENT
    channel: TAG
    value: FLOAT


def get_config_info(config_file):
    with config_file.expanduser().open() as cfile:
        host = cfile.readline().strip()
        username = cfile.readline().strip()
        password = cfile.readline().strip()
    return (host, username, password)


def make_point(meas_time, meas_name, meas_value, channel):
    isostring = meas_time.isoformat()
    try:
        return Measurement(
            timestamp=isostring,
            measurement=meas_name,
            channel=str(channel),
            value=float(meas_value),
        )
    except ValueError:
        return None


async def main(opts):
    ifilename = os.path.expanduser(os.path.expandvars(opts.temperature_data))

    time_zone = ZoneInfo("US/Arizona")

    channel_number = int(CHANNEL_MATCH.findall(os.path.basename(ifilename))[-1])
    # print(channel_number)
    config_info = get_config_info(opts.auth)
    async with InfluxDBClient(
        host=config_info[0],
        username=config_info[1],
        password=config_info[2],
        db="AmbientWeather",
    ) as client:
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
                measurement_time = measurement_time.astimezone(time_zone)
                measurement_time_utc = measurement_time.astimezone(UTC)
                for j in range(1, 5):
                    value = row[j]
                    measurement = MEASUREMENTS[j - 1]
                    point = make_point(
                        measurement_time_utc, measurement, value, channel_number
                    )
                    if point is not None:
                        if opts.debug:
                            if opts.verbose:
                                print(point)
                        else:
                            await client.write(point)
                    else:
                        print(
                            f"Bad value for channel {channel_number}: {measurement} ({measurement_time})"
                        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Insert temperature data into InfluxDB.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("temperature_data", help="Temperature data file.")
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="Check files for bad data (no DB write).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Print out the data point.",
    )
    parser.add_argument(
        "-a",
        "--auth",
        type=pathlib.Path,
        default=pathlib.Path("~/.auth/influxdb"),
        help="Provide the path to the ",
    )

    args = parser.parse_args()

    asyncio.run(main(args))
