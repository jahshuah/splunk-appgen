#!/usr/bin/env python

"""
Description:
An app generator/scaffolding tool for Splunk applications

"""
__author__ = "Joshua Hart"
__version__ = 1.0
__status__ = "beta"

import os
import sys
import argparse
import tarfile

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def main():
    # Pass the app name to the script via command line arguments
    parser = argparse.ArgumentParser(description='Packaging tool for Splunk applications')
    parser.add_argument(
        '-f',
        '--filename',
        nargs=1,
        required=True,
        help='Destination name of the file with either a .tgz or .spl extension.',
        metavar='APP_NAME'
    )
    parser.add_argument(
        '-t',
        '--target-dir',
        nargs=1,
        required=True,
        help='Directory to package up.',
        metavar='TARGET_DIRECTORY'
    )
    args = parser.parse_args()
    filename = args.filename[0]
    target_dir = args.target_dir[0]

    # Make the archive file
    make_tarfile(filename, target_dir)

if __name__ == '__main__':
    main()
