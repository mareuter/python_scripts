#!/usr/bin/env python
# This program requires the use of the Pdftk server program.

import argparse
import os
import subprocess


def combine_files(opts):
    """Combine the odd and even pages intoa  single file.
    """
    cmd = ['pdftk']
    cmd.append('A={}'.format(opts.odd_pages))
    cmd.append('B={}'.format(opts.even_pages))
    cmd.append('shuffle')
    cmd.append('A{}'.format('end-1' if opts.reverse_odd else ''))
    cmd.append('B{}'.format('end-1' if opts.reverse_even else ''))
    cmd.append('output')
    cmd.append('{}'.format(opts.combined_file))

    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        print(str(proc.stdout.read()))


def delete_files(opts):
    """Delete the input files.
    """
    os.unlink(opts.odd_pages)
    os.unlink(opts.even_pages)


def get_description():
    """Make the program description.
    """
    descr = ['Combine odd and even pages from separately scanned documents']
    return os.linesep.join(descr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=get_description())
    parser.add_argument('-d', '--delete', action='store_true',
                        help='Delete the input files instead of combining them.')
    parser.add_argument('--re', dest='reverse_even', action='store_true',
                        help='Reverse direction of even pages.')
    parser.add_argument('--ro', dest='reverse_odd', action='store_true',
                        help='Reverse direction of odd pages.')
    parser.add_argument('odd_pages', type=str, help='Document name for the odd numbered pages.')
    parser.add_argument('even_pages', type=str, help='Document name for the even numbered pages.')
    parser.add_argument('combined_file', type=str, help='Document name for the combined file.')

    args = parser.parse_args()

    if args.delete:
        delete_files(args)
    else:
        combine_files(args)
