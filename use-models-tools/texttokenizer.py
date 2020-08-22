#!/usr/bin/env python3
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

from __future__ import print_function

class TextTokenizer:

    def __init__(self):
        self.abbreviations = ['Mr.', 'Mrs.']
        self.lengths = []

        for i in range(0, len(self.abbreviations)):
            self.abbreviations[i] = self.abbreviations[i].lower()
            self.lengths.append(len(self.abbreviations[i]))

    def is_an_abbreviation(self, sentence, pos, length):
        for i in range(0, len(self.abbreviations)):
            abbrev_length = self.lengths[i]
            if self.lengths[i] > pos:
                continue

            if sentence[pos - abbrev_length + 1: pos + 1].lower() == self.abbreviations[i]:
                return True

        return False

    def tokenize(self, sentence):
        strings = []
        translate = []
        start = 0
        pos = 1

        length = len(sentence)
        for i in range(0, length):
            pos = i
            c = sentence[i]
            if c == '.' and self.is_an_abbreviation(sentence, i, length) is False:
                string = sentence[start:i+1]
                strings.append(string)
                translate.append(True)
                start = i + 1

            if c == '\n' or c == '\r':
                if start < i:
                    string = sentence[start:i+1]
                    strings.append(string)
                    translate.append(True)

                string = sentence[i]
                strings.append(string)
                translate.append(False)
                start = i + 1
     
        if start < pos:
            string = sentence[start:pos+1]
            strings.append(string)
            translate.append(True)
        
    #    for i in range(0, len(strings)):
    #        print("{0}->'{1}':{2}".format(i, strings[i], translate[i]))

        return strings, translate

    def sentence_from_tokens(self, sentences, translate, translated):
        num_sentences = len(sentences)
        translation = ''
        for i in range(0, num_sentences):
            if translate[i] is True:
                translation += translated[i] + " "
            else:
                translation += sentences[i]

        return translation.strip()
