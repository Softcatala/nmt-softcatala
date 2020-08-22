#!/usr/bin/env python
# -*- encoding: utf-8 -*-
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

import os
import datetime
import numpy as np

''' Based on the idea that source and target are almost identical when source is confused by target'''
class CheckSourceLanguage(object):

    FILE = "lang_detect.txt"

    def __init__(self, path, text, translated, languages):
        self.path = path
        self.text = text
        self.translated = translated
        self.languages = languages
        self.dist = None
        self.wrong = False

    def is_wrong(self):
        self._calculate_is_wrong_language()
        return self.wrong

    def _get_levenshtein(self, seq1, seq2):
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

    def _calculate_is_wrong_language(self):
        start_time = datetime.datetime.now()

        if len(self.text.split()) < 3:
            self.wrong = False
            return

        text = self.text.strip()
        translated = self.translated.strip()
        dist = self._get_levenshtein(text, translated)
        max_len = max(len(text), len(translated))
        self.dist = dist / max_len
        self.wrong = dist < 0.15

        if self.wrong:
            self._log(start_time)

    def _log(self, start_time):
        time_used = datetime.datetime.now() - start_time
        print(self.text)
        print(self.translated)
        saved_filename = os.path.join(self.path, self.FILE)
        with open(saved_filename, "a") as text_file:
            text_file.write(f'{self.languages} {self.text} - {self.translated} - {self.dist} {time_used}\n')
