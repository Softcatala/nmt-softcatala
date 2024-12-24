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

import re
import string

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

        if languages == 'eus-cat':
            return GenderBiasDetectionBasque()

        return None

class GenderBiasDetection(object):

    def __init__(self, terms_file_path="eng-gender-bias-terms.txt"):
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

class GenderBiasDetectionBasque(object):

    class Trie:

        class TrieNode:
            def __init__(self):
                self.children = {}
                self.label = None

        def __init__(self):
            self.dict = {}
            self.root = self.TrieNode()

        def insert(self, word, label):
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = self.TrieNode()
                node = node.children[char]
            node.label = label

        def has_prefix(self, word):
            # Careful, it just checks the first prefix.
            # Perhaps it is not a good idea : do that later
            node = self.root
            prefix = ""
            for char in word:
                if char in node.children:
                    node = node.children[char]
                    prefix = prefix + char
                    if node.label:
                        return prefix, node.label
                else:
                    break
            return False

    def __init__(self, terms = "eus-gender-bias-terms.tsv", regexs = "eus-regex.tsv"):
        self.words = list()
        self.terms = terms
        self.regexs = regexs

        self.prefixlist = self.Trie()
        self.suffixlist = dict()
        self.load_data(self.prefixlist)
        self.load_regexes(self.suffixlist)

    def load_data(self, prefixlist):
        with open(self.terms, "r") as fp:
            cnt = 0
            for line in fp:
                word, label = line.strip().split("\t")
                prefixlist.insert(word, label)
                cnt += 1

            print(f"load_data. Size: {cnt}")

    #  read regular expressions in a dictionary
    #  and compile them
    def load_regexes(self, suffixlist):
        with open(self.regexs, "r") as fp:
            cnt = 0
            for line in fp:
                try:
                    label, regex = line.strip().split("\t")
                except Exception as error:
                    print("Error reading suffix regex line starting " + line[:30] + "...")
                    exit()
                print(label)
                try:
                    suffixlist[label] = re.compile(
                        regex
                    )  # we will compile later for efficiency
    #                print(regex)
                    cnt += 1
                except Exception as error:
                    print("Found an error in the regex for suffix " + label + ":")
                    print(error)

            print(f"load_regexes: {cnt}")



    def _compute(self, sentence):
        # remove all punctuation using the string library        
        words = list()
        translator = str.maketrans("", "", string.punctuation)
        for word in sentence.split():
            word = word.translate(translator).lower()
            result = self.prefixlist.has_prefix(word)
            if result and word not in words:
                prefix, label = result
                suffix = word[len(prefix) :]  # get suffix
                if self.suffixlist[label].fullmatch(suffix):
                    words.append(word)

        return words

    def get_words(self, sentence):
        words = self._compute(sentence)
        return words

