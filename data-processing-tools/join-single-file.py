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

def _convert_newlines(result):
    original = result
    mapping = {
                u"\u2028" : '',
                u"\u2029" : '',
              }

    for char in mapping.keys():
        result = result.replace(char, mapping[char])

    cleaned = original != result
    return result, cleaned

def _has_dot_or_equivalent(text):
    t = text

    if t[-1:]== '.' or t[-1:] == '…' or t[-1:] == '?' or t[-1:] == '!':
        return True

    if t[-2:] == '.)' or t[-2:] == '."' or t[-2:] == '.\'':
        return True

    return False

def _process_dot(src, trg, dots):
    s = src.rstrip()
    t = trg.rstrip()

    if s[-1:] == '.' and _has_dot_or_equivalent(t) is False:
        src = src.rstrip()
        trg = trg.rstrip() + "."
        dots = dots + 1
    elif t[-1:] == '.' and _has_dot_or_equivalent(s) is False:
        trg = trg.rstrip()
        src = src.rstrip() + "."
        dots = dots + 1

    return src, trg, dots

def _is_sentence_len_good(src, trg):
    src = src.strip()
    trg = trg.strip()
    lsrc = len(src)
    ltrg = len(trg)

    if lsrc == 0 or ltrg == 0:
        return False

    MIN_CHARS = 50
    if max(lsrc, ltrg) > MIN_CHARS:
        if lsrc < ltrg:
           tmp = lsrc
           lsrc = ltrg
           ltrg = tmp

        diff = (lsrc - ltrg) / lsrc * 100
        if diff > 70:
            return False

    return True

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
    bad_length = 0
    dots = 0

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
                break

            if _is_sentence_len_good(src, trg) is False:
                bad_length = bad_length + 1
                continue

            src, cleaned = _convert_newlines(src)
            trg, cleaned = _convert_newlines(trg)
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

            src, trg, dots = _process_dot(src, trg, dots)

            source.write(src)
            target.write(trg)

            # Duplicate corpus in upper case to translate properly uppercase text
            source.write(src.upper())
            target.write(trg.upper())

            strings = strings + 1

    pduplicated = duplicated * 100 / strings
    pdots = dots * 100 / strings
    pclean = clean * 100 / strings
    pbad_length = bad_length * 100 / strings
    print(f"Strings: {strings}, duplicated {duplicated} ({pduplicated:.2f}%)")
    print(f"Cleaned acute accents: {clean} ({pclean:.2f}%)")
    print(f"Empty sentences or diff len too long: {bad_length} ({pbad_length:.2f}%)")
    print(f"Dots: {dots} ({pdots:.2f}%)")

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

    if src_lines != trg_lines:
        raise Exception(f"Source and target corpus have different lengths.")

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
