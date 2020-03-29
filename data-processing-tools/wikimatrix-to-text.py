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

    
def clean_string(text):
    text = re.sub('[_&~]', '', text)
    text = re.sub('<[^>]*>', '', text) # Remove HTML tags
    return text

def main():

    print("Wikimatrix to text")

    txt_file = '/home/jordi/sc/wikimatrix/all.txt'
    txt_en_file = 'input/wikimatrix-en.txt'
    txt_ca_file = 'input/wikimatrix-ca.txt'
    strings = 0
    discarded = 0
    lines_ca = None
    
    with open(txt_file, 'r') as tf_txt_file:
        lines_ca = tf_txt_file.read().splitlines()

    with open(txt_en_file, 'w') as tf_en, open(txt_ca_file, 'w') as tf_ca:
        for line in lines_ca:

            split = line.split('\t')

            if len(split) != 3:
                print("Discarded (no tab):" + trg)
                discarded += 1
                continue

            src = split[2]
            trg = split[1]

            if 'anglès' in trg:
                print("Discarded:" + trg)
                discarded += 1
                continue

            tf_en.write("{0}\n".format(src))
            tf_ca.write("{0}\n".format(trg))
            strings = strings + 1

            #if strings >= 2000:
            #    break

    print("Wrote {0} strings (discarded {1})".format(strings, discarded))
        

if __name__ == "__main__":
    main()
