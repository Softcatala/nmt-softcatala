#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import json
import polib
import re
import os
import fnmatch
from optparse import OptionParser

def read_parameters():
    parser = OptionParser()

    parser.add_option(
        '-s',
        '--source-file',
        type='string',
        action='store',
        dest='source_file',
        help='Source file (english)'
    )

    parser.add_option(
        '-r',
        '--reference-file',
        type='string',
        action='store',
        dest='reference_file',
        help='Reference translated file (previous translated file)'
    )

    parser.add_option(
        '-t',
        '--translation-file',
        type='string',
        action='store',
        dest='translated_file',
        help='New translated file'
    )

    parser.add_option(
        '-o',
        '--output-file',
        type='string',
        action='store',
        dest='output_file',
        help='Output file'
    )

    (options, args) = parser.parse_args()
    if options.source_file is None:  # if filename is not given
        parser.error('File not given')

    return options.source_file, options.reference_file, options.translated_file, options.output_file

def main():

    print("Compares English file against reference and new translation")

    equals = 0
    changed = 0

    source_file, reference_file, translated_file, output_file = read_parameters()

    fh_output_file = open(output_file, 'w')

    with open(source_file, 'r') as fh_source_file:
        source_lines = fh_source_file.read().splitlines()

    with open(reference_file, 'r') as fh_reference_file:
        reference_lines = fh_reference_file.read().splitlines()

    with open(translated_file, 'r') as fh_translated_file:
        translated_lines = fh_translated_file.read().splitlines()

    len_source_lines = len(source_lines)
    len_reference_file = len(reference_lines)
    len_translated_file = len(translated_lines)

    if (len_source_lines == len_reference_file == len_translated_file) == False:
        print ("Different line numbers. source {0}, reference {1}, translated {2}".format(
              len_source_lines, len_reference_file, len_translated_file))
        return

    for i in range(0, len(source_lines)):
        if reference_lines[i] != translated_lines[i]:
            changed += 1
            fh_output_file.write("{0}\t0\t0\t0\r{1}\t0\t0\t0\r{2}\t0\t0\t0\r\r".
                                 format(source_lines[i], reference_lines[i], translated_lines[i]))
        else:
            equals += 1

    equals_p = 100*equals/len_source_lines
    changed_p = 100*changed/len_source_lines
    print("String that are equal {0} ({1:.2f}%) changed {2} ({3:.2f}%)".format(equals, equals_p, changed, changed_p))
        

if __name__ == "__main__":
    main()
