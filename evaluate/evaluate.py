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

import nltk
import warnings
from nltk.translate import nist_score, bleu_score
warnings.filterwarnings("ignore")

def show_bleu(reference_file, hypotesis_file):
    cumulative_bleu_score = 0
    with open(reference_file, 'r') as tf_ref, open(hypotesis_file, 'r') as tf_hyp:
        lines_ref = tf_ref.read().splitlines()
        lines_hyp = tf_hyp.read().splitlines()
#        lines_ref = lines_ref[0:500]
#        lines_hyp = lines_hyp[0:500]

        len_ref = len(lines_ref)
        len_hyp = len(lines_hyp)
        if len_ref != len_hyp:
            print("Different number of lines in files: {0} (reference), {1} (hypotesis)".format(len_ref, len_hyp))
            return

        # Str -> to tokens
        strings_ref = []
        for i in range(0, len(lines_ref)):
            strings_ref.append([(lines_ref[i].split())])# Double list

        strings_hyp = []
        for i in range(0, len(lines_hyp)):
            strings_hyp.append(lines_hyp[i].split())

        bleu_score = nltk.translate.bleu_score.corpus_bleu(strings_ref, strings_hyp)
        print("** Bleu score (corpus): " + str(bleu_score))

        show_nist(reference_file, hypotesis_file)


def show_nist(reference_file, hypotesis_file):
    cumulative_bleu_score = 0
    with open(reference_file, 'r') as tf_ref, open(hypotesis_file, 'r') as tf_hyp:
        lines_ref = tf_ref.read().splitlines()
        lines_hyp = tf_hyp.read().splitlines()
#        lines_ref = lines_ref[0:500]
#        lines_hyp = lines_hyp[0:500]

        len_ref = len(lines_ref)
        len_hyp = len(lines_hyp)
        if len_ref != len_hyp:
            print("Different number of lines in files: {0} (reference), {1} (hypotesis)".format(len_ref, len_hyp))
            return

        # Str -> to tokens
        strings_ref = []
        for i in range(0, len(lines_ref)):
            strings_ref.append([(lines_ref[i].split())])# Double list

        strings_hyp = []
        for i in range(0, len(lines_hyp)):
            strings_hyp.append(lines_hyp[i].split())

        bleu_score = nist_score.corpus_nist(strings_ref, strings_hyp)
        print("** NIST score (corpus): " + str(bleu_score))

    
def main():
    datasets = \
        [\
            ['Sleepyhollow', 'input/sleepyhollow.en-ca.ca','translated/sleepyhollow-apertium-ca.txt',\
                 'translated/sleepyhollow-yandex-ca.txt', 'translated/sleepyhollow-google-ca.txt',\
                 'translated/sleepyhollow-opennmt-ca.txt' ],\
            ['Tatoeba', 'input/tatoeba.en-ca.ca','translated/tatoeba-apertium-ca.txt',
                 'translated/tatoeba-yandex-ca.txt','translated/tatoeba-google-ca.txt', \
                 'translated/tatoeba-opennmt-ca.txt'],\
        ]

    for ds in datasets:
        print(ds[0])
        print("*** Apertium (Softcatalà)")
        show_bleu(ds[1], ds[2])

        print("Yandex)")
        show_bleu(ds[1], ds[3])

        print("Google")
        show_bleu(ds[1], ds[4])

        print("OpenNMT")
        show_bleu(ds[1], ds[5])

if __name__ == "__main__":
    main()
