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



class GenderBiasTermsLoader:
    _cached_terms = None

    @classmethod
    def load_terms(cls, file_path):
        if cls._cached_terms is None:
            with open(file_path, "r") as fp:
                cls._cached_terms = {line.strip() for line in fp if line.strip()}

        return cls._cached_terms

class GenderBiasDetectionFactory:
    @staticmethod
    def get(languages):
        if languages == 'eng-cat':
            return GenderBiasDetection()

        return None

class GenderBiasDetection(object):

    def __init__(self, terms_file_path="gender-bias-terms.txt"):
        self.terms = GenderBiasTermsLoader.load_terms(terms_file_path)

    def _compute(self, sentence):
        words = set()
        chars_to_remove = [".", "!", "?", ",", ":"]

        for word in sentence.split():
            for char in chars_to_remove:
                word = word.replace(char, "")

            word = word.lower()
            if word in self.terms and word not in words:
                words.add(word)

        return words

    def get_words(self, sentence):
        words = self._compute(sentence)
        return words
