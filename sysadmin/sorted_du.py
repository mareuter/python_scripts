#!/usr/bin/env python
from operator import itemgetter
import os
import subprocess

BYTE_CONV = 1024
SIZE_SUFFIXES = ['B', 'K', 'M', 'G', 'T', 'P']


def get_human_size(byte_value):
    human_size = None
    try:
        multiplier = os.environ['BLOCKSIZE']
    except KeyError:
        multiplier = 512
    value = byte_value * multiplier
    suffix = None
    dval = None
    for i in range(len(SIZE_SUFFIXES)):
        if value == 0:
            dval = value
            suffix = 0
            break
        dval = value / (BYTE_CONV ** i)
        if dval < 1.0:
            dval = value / (BYTE_CONV ** (i - 1))
            suffix = i - 1
            break
        suffix = i
    if dval < 10.0 and dval > 0:
        dval_str = "{:.1f}".format(dval)
    else:
        dval_str = "{}".format(int(round(dval)))

    human_size = "{:>3s}{}".format(dval_str, SIZE_SUFFIXES[suffix])
    return human_size


p = subprocess.Popen(["du", "-d1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output = p.communicate()[0].decode('utf-8')
values = output.split(os.linesep)
dirs = []
total = 0
for value in values:
    # Skip the empty entry due to output conversion.
    if value == '':
        continue
    parts = value.split('\t')
    # Skip the directory total.
    if parts[1] == '.':
        total = int(parts[0])
        continue
    dirs.append((int(parts[0]), parts[1].lstrip('.').lstrip('/')))
sorted_dirs = sorted(dirs, key=itemgetter(0), reverse=True)

for dsize, dname in sorted_dirs:
    print("{}\t{}".format(get_human_size(dsize), dname))

print(f'{get_human_size(total)}\t.')
