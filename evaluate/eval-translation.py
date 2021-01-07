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
    html_tags = 0
    html_tags_error = 0
    formatters = 0
    error_formatters = 0
    comma = 0
    error_comma = 0


    with open(src_filename, "r") as read_source, open(tgt_filename, "r") as read_target:
        while True:

            src = read_source.readline().lower()
            tgt = read_target.readline().lower()

            if not src or not tgt:
                break

            if tgt.find("<unk>") >= 0:
                unk = unk + 1

            if src.find("%s") >= 0:
                formatters = formatters + 1
                if tgt.find("%s") == -1:
                    error_formatters = error_formatters + 1
                    #print(f"Tag error: {src} | {tgt}")

            if src.find(",") >= 0:
                comma = comma + 1
                if tgt.find(",") == -1:
                    error_comma = error_comma + 1

            if src.find("%d") >= 0:
                formatters = formatters + 1
                if tgt.find("%d") == -1:
                    error_formatters = error_formatters + 1
                   # print(f"Tag error: {src} | {tgt}")

            tags = re.findall("<[^>]*>", src)
            if len(tags) > 0:
                html_tags = html_tags + len(tags)

            for tag in tags:
                if tgt.find(tag) == - 1:
                    html_tags_error = html_tags_error + 1
                    print(f"Tag error: {src} | {tgt}")

            strings = strings + 1

    punk = unk * 100 / strings
    print(f"Strings: {strings}, unknowns: {unk} ({punk:.2f}%)")

    phtml_tags_error = html_tags_error * 100 / html_tags
    print(f"Html tags with error: {html_tags_error} ({phtml_tags_error:.2f}%)")

    perror_formatters = error_formatters * 100 / formatters
    print(f"String formatters with error: {error_formatters} ({perror_formatters:.2f}%)")

    perror_comma = error_comma * 100 / comma
    print(f"Missing commas (,): {error_comma} ({perror_comma:.2f}%)")

def main():

    print("Checks translation")
    check_translation('src-test-tags.txt', 'tgt-test-tags.txt')

if __name__ == "__main__":
    main()
