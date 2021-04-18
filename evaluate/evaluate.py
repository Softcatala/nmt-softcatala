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
import os
from nltk.translate import nist_score, bleu_score
warnings.filterwarnings("ignore")

def get_bleu(reference_file, hypotesis_file):
    if reference_file is None or hypotesis_file is None:
        return 0

    if not os.path.exists(reference_file):
        print(f"File '{reference_file}' not found")
        return 0

    if not os.path.exists(hypotesis_file):
        print(f"File '{hypotesis_file}' not found")
        return 0

    cumulative_bleu_score = 0
    with open(reference_file, 'r') as tf_ref, open(hypotesis_file, 'r') as tf_hyp:
        lines_ref = tf_ref.read().splitlines()
        lines_hyp = tf_hyp.read().splitlines()

        len_ref = len(lines_ref)
        len_hyp = len(lines_hyp)
        if len_ref != len_hyp:
            print("Different number of lines in files: {0} (reference), {1} (hypotesis)".format(len_ref, len_hyp))
            return 0

        # Str -> to tokens
        strings_ref = []
        for i in range(0, len(lines_ref)):
            strings_ref.append([(lines_ref[i].split())])# Double list

        strings_hyp = []
        for i in range(0, len(lines_hyp)):
            strings_hyp.append(lines_hyp[i].split())

        bleu = nltk.translate.bleu_score.corpus_bleu(strings_ref, strings_hyp)
        return bleu
 #       print("** Bleu score (corpus): " + str(bleu_score))
        

#        show_nist(reference_file, hypotesis_file)


def get_nist(reference_file, hypotesis_file):
    if not os.path.exists(reference_file):
        print(f"File '{reference_file}' not found")
        return 0

    if not os.path.exists(hypotesis_file):
        print(f"File '{hypotesis_file}' not found")
        return 0

    cumulative_bleu_score = 0
    with open(reference_file, 'r') as tf_ref, open(hypotesis_file, 'r') as tf_hyp:
        lines_ref = tf_ref.read().splitlines()
        lines_hyp = tf_hyp.read().splitlines()

        len_ref = len(lines_ref)
        len_hyp = len(lines_hyp)
        if len_ref != len_hyp:
            print("Different number of lines in files: {0} (reference), {1} (hypotesis)".format(len_ref, len_hyp))
            return 0

        # Str -> to tokens
        strings_ref = []
        for i in range(0, len(lines_ref)):
            strings_ref.append([(lines_ref[i].split())])# Double list

        strings_hyp = []
        for i in range(0, len(lines_hyp)):
            strings_hyp.append(lines_hyp[i].split())

        score = nist_score.corpus_nist(strings_ref, strings_hyp)
        return score

def show_score_line(engine, reference_file, hypotesis_file):
    bleu = get_bleu(reference_file, hypotesis_file)
    nist = get_nist(reference_file, hypotesis_file)

    if len(engine) >= 8:
        print(f"{engine}\t\t{bleu:.2f}\t{nist:.2f}")
    else:
        print(f"{engine}\t\t\t{bleu:.2f}\t{nist:.2f}")

def evaluate_eng_cat():

    language = 'ca'

    datasets = \
        [\
            ['Sleepyhollow', f'input/sleepyhollow.en-ca.{language}', f'translated/sleepyhollow-apertium-{language}.txt',\
                 f'translated/sleepyhollow-yandex-{language}.txt', f'translated/sleepyhollow-google-{language}.txt',\
                 f'translated/sleepyhollow-opennmt-{language}.txt' ],\
            ['Tatoeba', f'input/tatoeba.en-ca.{language}', f'translated/tatoeba-apertium-{language}.txt',
                 f'translated/tatoeba-yandex-{language}.txt', f'translated/tatoeba-google-{language}.txt', \
                 f'translated/tatoeba-opennmt-{language}.txt'],\

            ['SC Users', f'input/sc-users-{language}.txt', f'translated/sc-users-apertium-{language}.txt',
                 None, f'translated/sc-users-google-{language}.txt', \
                 f'translated/sc-users-opennmt-{language}.txt'],\

            ['Fedalist', f'input/federalist.en-{language}.ca', None,
                 'translated/federalist-yandex-ca.txt', f'translated/federalist-google-{language}.txt', \
                 f'translated/federalist-opennmt-ca.txt'],\
        ]

    print("Translation engine\tBLEU\tNIST")
    for ds in datasets:
        print("-- " + ds[0])

        if ds[2] != None:
            show_score_line("Apertium", ds[1], ds[2])

        if ds[3] != None:
            show_score_line("Yandex", ds[1], ds[3])

        if ds[4] != None:
            show_score_line("Google", ds[1], ds[4])

        if ds[5] != None:
            show_score_line("nmt-softcatala", ds[1], ds[5])



def evaluate_deu_cat():

    language = 'ca'

    datasets = \
        [\
            ['Tatoeba', f'input/tatoeba.ca-de.{language}', None,
                 'translated/tatoeba.ca-de-yandex-ca.txt', f'translated/tatoeba.ca-de-google-{language}.txt', \
                 'translated/tatoeba.ca-de.opennmt-ca.txt'],\

            ['Ubuntu', f'input/ubuntu.ca-de.{language}', None,
                 None, f'translated/ubuntu.ca-de-google-{language}.txt', \
                 f'translated/ubuntu.ca-de.opennmt-{language}.txt'],\
        ]

    print("Transalion engine\tBLEU\tNIST")
    for ds in datasets:
        print("-- " + ds[0])

        if ds[2] != None:
            show_score_line("Apertium", ds[1], ds[2])

        if ds[3] != None:
            show_score_line("Yandex", ds[1], ds[3])

        if ds[4] != None:
            show_score_line("Google", ds[1], ds[4])

        if ds[5] != None:
            show_score_line("nmt-softcatala", ds[1], ds[5])



def main():
    evaluate_deu_cat()
#    evaluate_eng_cat()


if __name__ == "__main__":
    main()
