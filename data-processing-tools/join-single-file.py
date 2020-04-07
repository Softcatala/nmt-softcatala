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

import polib
import re
import yaml

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def split_in_six_files():

    srcs = set()
    number_validation = 3000
    number_test = 3001 # number_test != number_validation

    cnt = 0
    pairs = 0

    print("Split src and tgt files in 6 files for training, text and validation")

    total_lines = file_len("src.txt")
    validation_each = round(total_lines / number_validation)
    test_each = round(total_lines / number_test)

    if test_each == validation_each:
        print("test_each and validation_each cannot be equal")
        return
        

    with open("src-val.txt", "w") as source_val,\
        open("tgt-val.txt", "w") as target_val,\
        open("src-test.txt", "w") as source_test,\
        open("tgt-test.txt", "w") as target_test,\
        open("src-train.txt", "w") as source_train,\
        open("tgt-train.txt", "w") as target_train,\
        open("src.txt", "r") as read_source,\
        open("tgt.txt", "r") as read_target:

        src = read_source.readline()
        trg = read_target.readline()


        print("total_lines {0}".format(total_lines))
        print("number_validation {0}".format(number_validation))
        print("number_test {0}".format(number_test))
        print("validation_each {0}".format(validation_each))
        print("test_each {0}".format(test_each))

        while src and trg:
            pairs = pairs + 1

            if cnt % validation_each == 0:
                source = source_val
                target = target_val
            elif cnt % test_each == 0:
                source = source_test
                target = target_test
            else:
                source = source_train
                target = target_train

            source.write(src)
            target.write(trg)

            src = read_source.readline()
            trg = read_target.readline()
            cnt = cnt + 1


    print("Pairs: " + str(pairs))

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
    

def join_multiple_sources_and_target_into_two_files():

    src_lines = 0
    trg_lines = 0

    sources, targets = read_configuration()

    print("Join multiple files in two src and tgt files")
    with open("src.txt", "w") as tf_source,\
        open("tgt.txt", "w") as tf_target:

        for source in sources:
            src_lines += append_lines_from_file(source, tf_source)

        for source in sources:
            trg_lines += append_lines_from_file(source, tf_target)

    print("src lines: " + str(src_lines))
    print("trg lines: " + str(trg_lines))


def main():

    print("Joins several corpus and creates a final train, validation and test dataset")

    read_configuration()
    join_multiple_sources_and_target_into_two_files()
    split_in_six_files()

if __name__ == "__main__":
    main()
