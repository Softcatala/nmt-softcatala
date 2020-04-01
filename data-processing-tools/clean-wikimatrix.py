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
from langua import Predict
    
def main():

    print("Wikimatrix corpus clean up. Removes non Catalan strings")

    start_time = datetime.datetime.now()
    source_en_file = 'input/WikiMatrix.en-ca.txt.en'
    source_ca_file = 'input/WikiMatrix.en-ca.txt.ca'
    clean_en_file = 'clean/wikimatrix-en.txt'
    clean_ca_file = 'clean/wikimatrix-ca.txt'
    log_file = 'wikimatrix.log'

    strings = 0
    discarded = 0
    
    with open(source_en_file, 'r') as tf_source_en_file:
        source_en_lines = tf_source_en_file.readlines()

    with open(source_ca_file, 'r') as tf_source_ca_file:
        source_ca_lines = tf_source_ca_file.readlines()

    len_source_en_lines = len(source_en_lines)
    len_source_ca_lines = len(source_ca_lines)

    if len_source_en_lines != len_source_ca_lines:
        print("Files of different lengths {0}, {1}".format(len_source_en_lines, len_source_ca_lines))
        return

    with open(clean_en_file, 'w') as tf_clean_en_file, open(clean_ca_file, 'w') as tf_clean_ca_file,\
         open(log_file, 'w') as tf_log_file:

        for i in range(0, len_source_en_lines):
            src = source_en_lines[i]
            trg = source_ca_lines[i]

            try:
                p = Predict()
                source_lang = p.get_lang(src)
                target_lang = p.get_lang(trg)

            except Exception as e:
                print("Error:" + str(e))
                continue

            if source_lang != 'en' or target_lang != 'ca':
                tf_log_file.write("Source language '{0}', target language '{1}'\n".format(source_lang, target_lang))
                tf_log_file.write("s: {0}\n".format(src.replace('\n', '')))
                tf_log_file.write("t: {0}\n\n".format(trg.replace('\n', '')))
                discarded = discarded + 1
                continue

            if i % 5000 == 0:
                print("{0} ({1:.2f}%)".format(i, 100 * i / len_source_en_lines))
                break
                
            tf_clean_en_file.write("{0}".format(src))
            tf_clean_ca_file.write("{0}".format(trg))
            strings = strings + 1

    print("Wrote {0} ({1:.2f}%) strings discarded {2} ({3:.2f}%)".format(strings,
         100 * strings / len_source_en_lines, discarded, 100 * discarded / len_source_en_lines))
    print("Time used {0}".format(str(datetime.datetime.now() - start_time)))  

if __name__ == "__main__":
    main()
