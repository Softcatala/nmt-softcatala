#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Jordi Mas i Hernandez <jmas@softcatala.org>
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

def _remove_accelerators(result):
    CHARS = (
        '_', '&', '~',  # Accelerators.
        ':', ',', '...', u'…'  # Punctuations.
    )
    for c in CHARS:
        result = result.replace(c, '')

    return result.strip()

def _remove_tags(text):
    clean = re.sub("<[^>]*>","", text)
    return clean

def _is_invalid(src, trg):
    if len(src) < 2 or len(trg) < 2:
        #print('Discard:' + entry.msgid + "->" + entry.msgstr)
        return True

    if '\n' in src or '\n' in trg:
        #print('Discard:' + entry.msgstr)
        return True

    if '%' in src or '%' in trg:
        #print('Discard:' + entry.msgstr)
        return True

    return False


def split_in_six_files(po_file):

    srcs = set()
    percentage_train = 90
    percentage_validation = 5
    cnt = 0
    pairs = 0

    with open("src-val.txt", "w") as source_val,\
        open("tgt-val.txt", "w") as target_val,\
        open("src-test.txt", "w") as source_test,\
        open("tgt-test.txt", "w") as target_test,\
        open("src-train.txt", "w") as source_train,\
        open("tgt-train.txt", "w") as target_train:

        input_po = polib.pofile(po_file)
        for entry in input_po:
            src = _remove_accelerators(entry.msgid)
            trg = _remove_accelerators(entry.msgstr)

            src = _remove_tags(src)
            trg = _remove_tags(trg)

            if _is_invalid(src, trg):
                continue

            if src in srcs:
                #print('Duplicated:' + src)
                continue

            srcs.add(src)
            pairs = pairs + 1

            if cnt < percentage_train:
                source = source_train
                target = target_train
            elif cnt < percentage_train + percentage_validation:
                source = source_val
                target = target_val
            else:
                source = source_test
                target = target_test

            source.write(src + "\n")
            target.write(trg + "\n")
            cnt = cnt + 1
            if cnt >= 100:
                cnt = 0

    print("Pairs: " + str(pairs))

def split_in_two_files(po_file):

    srcs = set()
    pairs = 0
    cnt = 0

    with open("src.txt", "w") as source,\
        open("tgt.txt", "w") as target:

        input_po = polib.pofile(po_file)
        for entry in input_po:
            src = _remove_accelerators(entry.msgid)
            trg = _remove_accelerators(entry.msgstr)

            src = _remove_tags(src)
            trg = _remove_tags(trg)

            if _is_invalid(src, trg):
                continue

            if src in srcs:
                #print('Duplicated:' + src)
                continue

            srcs.add(src)
            pairs = pairs + 1

            source.write(src + "\n")
            target.write(trg + "\n")
            cnt = cnt + 1

    print("Pairs: " + str(pairs))


def main():

    print("Converts from PO to OpenNMT text files sets")

    po_file = 'softcatala-tm.po'
    twoFiles = True
    print("Reading {0} and generating two files {1}".format(po_file, twoFiles))

    if twoFiles:
        split_in_two_files(po_file)
    else:
        split_in_six_files(po_file)

if __name__ == "__main__":
    main()
