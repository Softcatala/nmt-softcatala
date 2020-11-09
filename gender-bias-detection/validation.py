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

import operator


def main():

    print("Read corpus and extracts sentences that match gender bias")

    terms = set()
    with open("gender-bias-terms.txt") as fp:
        while True: 
            term = fp.readline() 
      
            if not term:
                break

            term = term.replace("\n", "")
            #print(f'-{term}-')
            terms.add(term)

    word_sentences = {}
    word_frequencies = {}
    lines = 0
    with open("../training-sets/eng-cat/src-train.txt") as fp:
        while True:
            line = fp.readline()
            if not line:
                break

            lines = lines + 1
            words = line.split()
            for word in words:
                if word not in terms:
                    continue

                if word in word_frequencies:
                    frequency = word_frequencies[word] + 1
                else:
                    frequency = 1

                word_frequencies[word] = frequency

                if word in word_sentences:
                    sentences = word_sentences[word]
                else:
                    sentences = set()

                sentences.add(line)
                word_sentences[word] = sentences

    bias_sentences = 0
    with open("gender-bias-corpus.txt", "w+") as fp:
        for word in word_sentences.keys():
            fp.write(f"---- {word}\n\n")
            sentences = word_sentences[word]
            for sentence in sentences:
                fp.write(f"{sentence}\n")
                bias_sentences = bias_sentences + 1


    sorted_dict = sorted(word_frequencies.items(), key=operator.itemgetter(1), reverse=True)
    for stats in sorted_dict:
        word, count = stats
        print(f"word {word} - {count}")

    pbias_sentences = bias_sentences * 100 / lines
    print(f"Strings: {lines}, bias sentences {bias_sentences} ({pbias_sentences:.2f}%)")


  
if __name__ == "__main__":
    main()
