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

import datetime
import numpy as np

'''
    Creates groups (e.g. 1 to 5K, 5K to 10K with data of the discards, to understand the distribution of discards
    across the dataset and the data it's sorted by confidence
'''
class Groups():

    TOTAL_GROUPS = 10

    def __init__(self, min_lines):
        self.groups = []
        self.size = 0
        self._create_groups(min_lines)

    def inc_discarted(self, index):
        group = self._find_group(index)
        discarted = self.groups[group]['discarded']
        self.groups[group]['discarded'] = discarted + 1

    def _create_groups(self, min_lines):
        self.size = int (min_lines / self.TOTAL_GROUPS)

        group = 0
        end = 0
        while group < self.TOTAL_GROUPS:
            start = end
            end = start + self.size

            data = {}
            data['start'] = start
            data['end'] = end
            data['discarded'] = 0
            self.groups.append(data)

            start = end + 1
            group = group + 1


    def _find_group(self, index):
        group = int(index / self.size)
        return group

    def to_string(self):
        s = ""
        for group in self.groups:
            start = group['start']
            end = group['end']
            discarded = group['discarded']
            p_discarded = 100* discarded / self.size
            s += f"Range {start} - {end} - discarded {discarded} ({p_discarded:.2f}%)\n"

        return s


def _get_levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return matrix[size_x - 1, size_y - 1]


    
def main():

    print("Filtes out wrong Wikimatrix translations by comparing the target corpus (ca) to our own translation (done by mt)")
    print("If the levenshtein distance between both is high, we discard the string from the corpus")

    #source_pattern = 'WikiMatrix.en-ca.txt'
    #reference = 'WikiMatrix_opennt.ca'
    source_pattern = '50000'
#    reference = 'WikiMatrix_opennt.ca'
    reference = '50000.ref'

    source_en_file = source_pattern + '.en'
    source_ca_file = source_pattern + '.ca'
    log_file = 'qualitymatrix.log'

    strings = 0
    discarded = 0
    
    with open(source_en_file, 'r') as tf_source_en_file, open(source_ca_file, 'r') as tf_source_ca_file,\
         open(reference, 'r') as tf_reference_file, open(log_file, 'w') as tf_log_file:

        source_en_lines = tf_source_en_file.readlines()
        source_ca_lines = tf_source_ca_file.readlines()
        reference_ca_lines = tf_reference_file.readlines()

        len_source_en_lines = len(source_en_lines)
        len_source_ca_lines = len(source_ca_lines)
        len_reference_ca_lines = len(reference_ca_lines)

        min_lines = min(len_source_en_lines, len_reference_ca_lines)

        groups = Groups(min_lines)

        i = 0
        while i < min_lines:

            src_en = source_en_lines[i]
            src_ca = source_ca_lines[i]
            ref_ca = reference_ca_lines[i]

            dist = _get_levenshtein(src_ca, ref_ca)
            max_len = max(len(src_ca), len(ref_ca))
            dist = dist / max_len

            if dist > 0.50:
                tf_log_file.write("{0}\n".format(src_en.replace('\n', '')))
                tf_log_file.write("{0}\n".format(src_ca.replace('\n', '')))
                tf_log_file.write("{0} - {1} - {2}\n\n".format(ref_ca.replace('\n', ''), i, dist))
                discarded = discarded + 1
                groups.inc_discarted(i)
            else:
                strings = strings + 1

            if i % 10000 == 0:
                print("{0} ({1:.2f}%)".format(i, 100 * i / min_lines))

            i = i + 1


        s = "Wrote {0} ({1:.2f}%) total strings discarded {2} ({3:.2f}%)".format(strings,
           100 * strings / len_source_en_lines, discarded, 100 * discarded / min_lines)
        print(s)
        tf_log_file.write("{0}\n".format(s))

        s = groups.to_string()
        print(s)
        tf_log_file.write("{0}\n".format(s))

if __name__ == "__main__":
    main()


