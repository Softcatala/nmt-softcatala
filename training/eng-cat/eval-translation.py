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
import re

def check_translation(src_filename, tgt_filename):

    unk = 0
    strings = 0
    error_tag = 0
    with open(src_filename, "r") as read_source, open(tgt_filename, "r") as read_target:
        while True:

            src = read_source.readline().lower()
            tgt = read_target.readline().lower()

            if not src or not tgt:
                break;

            if tgt.find("<unk>") >= 0:
                unk = unk + 1

            tags = re.findall("<[^>]*>", src)
            for tag in tags:
                if tgt.find(tag) == - 1:
                    error_tag = error_tag + 1
                    print(f"Tag error: {src} | {tgt}")

            strings = strings + 1

    print(f"Strings: {strings}, unk {unk}, error tags {error_tag}")

#    pclean = clean * 100 / strings
    #pduplicated = duplicated * 100 / strings
#    print(f"Cleaned acute accents: {clean} ({pclean:.2f}%)")

def main():

    print("Checks translation")
    check_translation('src-test.txt', 'predictions.txt')

if __name__ == "__main__":
    main()
