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

import yaml
import os

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def _clean_localized(result):
    original = result
    mapping = {
                '’' : '\'',
                'à' : 'à',
                'í' : 'í',
                'ó' : 'ó',
                'è' : 'è',
                'ò' : 'ò',
                'ú' : 'ú',
              }

    for char in mapping.keys():
        result = result.replace(char, mapping[char])

    cleaned = original != result
    return result, cleaned


def split_in_six_files(src_filename, tgt_filename):

    pairs = set()
    number_validation = 3000
    number_test = 3007 # number_test != number_validation

    strings = 0
    duplicated = 0

    print("Split src and tgt files in 6 files for training, text and validation")

    total_lines = file_len(src_filename)
    validation_each = round(total_lines / number_validation)
    test_each = round(total_lines / number_test)

    if test_each == validation_each:
        print("test_each ({0}) and validation_each  ({0}) cannot be equal".format(test_each, validation_each))
        return
        
    with open("src-val.txt", "w") as source_val,\
        open("tgt-val.txt", "w") as target_val,\
        open("src-test.txt", "w") as source_test,\
        open("tgt-test.txt", "w") as target_test,\
        open("src-train.txt", "w") as source_train,\
        open("tgt-train.txt", "w") as target_train,\
        open(src_filename, "r") as read_source,\
        open(tgt_filename, "r") as read_target:


        print("total_lines {0}".format(total_lines))
        print("number_validation {0}".format(number_validation))
        print("number_test {0}".format(number_test))
        print("validation_each {0}".format(validation_each))
        print("test_each {0}".format(test_each))

        clean = 0
        while True:

            src = read_source.readline()
            trg = read_target.readline()

            if not (src and trg):
                break;

            trg, cleaned = _clean_localized(trg)

            pair = src + trg
            if pair in pairs:
                duplicated = duplicated + 1
                continue
            else:
                pairs.add(pair)

            if cleaned:
                clean = clean + 1

            if strings % validation_each == 0:
                source = source_val
                target = target_val
            elif strings % test_each == 0:
                source = source_test
                target = target_test
            else:
                source = source_train
                target = target_train

            source.write(src)
            target.write(trg)
            strings = strings + 1

    pclean = clean * 100 / strings
    pduplicated = duplicated * 100 / strings
    print(f"Strings: {strings}, duplicated {duplicated} ({pduplicated:.2f}%)")
    print(f"Cleaned acute accents: {clean} ({pclean:.2f}%)")

def append_lines_from_file(src_filename, trg_file):
    lines = 0
    with open(src_filename, 'r') as tf:
        line = tf.readline()
        while line:
            lines += 1
            trg_file.write(line)
            line = tf.readline()

    print("Appended {0} lines from {1}".format(lines, src_filename))
    return lines

def read_configuration():

    with open("corpus.yml", 'r') as stream:
        content = yaml.safe_load(stream)

    sources = content['source_files']
    targets = content['target_files']

    if len(sources) != len(targets):
        print("Different number of sources and targets")
        exit()

    return sources, targets
    

def join_multiple_sources_and_target_into_two_files(src_filename, tgt_filename):

    src_lines = 0
    trg_lines = 0

    sources, targets = read_configuration()

    print("Join multiple files in two src and tgt files")
    with open(src_filename, "w") as tf_source,\
         open(tgt_filename, "w") as tf_target:

        print("**Sources")
        for source in sources:
            src_lines += append_lines_from_file(source, tf_source)

        print("**Targets")
        for target in targets:
            trg_lines += append_lines_from_file(target, tf_target)

    print("src lines: " + str(src_lines))
    print("trg lines: " + str(trg_lines))


def main():

    print("Joins several corpus and creates a final train, validation and test dataset")

    single_src = 'src.txt'
    single_tgt = 'tgt.txt'
    join_multiple_sources_and_target_into_two_files(single_src, single_tgt)
    split_in_six_files(single_src, single_tgt)
    os.remove(single_src)
    os.remove(single_tgt)

if __name__ == "__main__":
    main()
