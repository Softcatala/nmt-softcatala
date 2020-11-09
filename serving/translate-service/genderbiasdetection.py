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



def load_data():
    with open("gender-bias-terms.txt") as fp:
        while True:
            term = fp.readline()

            if not term:
                break

            term = term.replace("\n", "")
            terms.add(term)

    print("Loaded gender bias data")

terms = set()
load_data()

class GenderBiasDetection(object):

    def __init__(self, sentence):
        self.words = []
        self._compute(sentence)

    def _compute(self, sentence):
        chars_to_remove = ['.', '!', '?', ',', ':']

        for word in sentence.split():
            for char in chars_to_remove:
                word = word.replace(char, '')

            if word.lower() in terms:
                self.words.append(word)

    def has_bias(self):
        return len(self.words) > 0

    def get_words(self):
        return self.words

