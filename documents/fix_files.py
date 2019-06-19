from datetime import datetime
import os
import sys

try:
    dirname = sys.argv[1]
except IndexError:
    print("python fix_files.py <directory name>")
    sys.exit(65)

files = os.listdir(dirname)
for file in files:
    if not file.endswith(".CSV"):
        continue
    channel_file = os.path.join(dirname, file)
    os.chmod(channel_file, 0o644)

    lines = None
    with open(channel_file) as ifile:
        lines = ifile.readlines()
        last_line = lines[-1]

    values = last_line.split(",")
    mdate = datetime.strptime(values[0], "%Y/%m/%d %H:%M")
    stinfo = os.stat(channel_file)
    os.utime(channel_file, (stinfo.st_atime, mdate.timestamp()))
