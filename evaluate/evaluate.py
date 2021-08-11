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
from optparse import OptionParser

def get_bleu(reference_file, hypotesis_file):
    if reference_file is None or hypotesis_file is None:
        return 0

    if not os.path.exists(reference_file):
        #print(f"File '{reference_file}' not found")
        return 0

    if not os.path.exists(hypotesis_file):
        #print(f"File '{hypotesis_file}' not found")
        return 0

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

def get_nist(reference_file, hypotesis_file):
    if not os.path.exists(reference_file):
#        print(f"File '{reference_file}' not found")
        return 0

    if not os.path.exists(hypotesis_file):
#        print(f"File '{hypotesis_file}' not found")
        return 0

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

    if bleu == 0 or nist == 0:
        return

    if len(engine) >= 8:
        print(f"{engine}\t\t{bleu:.2f}\t{nist:.2f}")
    else:
        print(f"{engine}\t\t\t{bleu:.2f}\t{nist:.2f}")

def _evaluate(datasets, source_language, target_language, language_pair):

    print("Translation engine\tBLEU\tNIST")
    print(f"Language pair: {language_pair}")
    engines = ["Apertium", "Yandex", "Google", "nmt-softcatala"]
    for ds in datasets:
        print("-- " + ds[0])

        for engine in engines:
            reference_file = ds[1].format(source_language, target_language, engine.lower(), target_language)
            hypotesis_file = ds[2].format(source_language, target_language, engine.lower(), target_language)
            show_score_line(engine, reference_file, hypotesis_file)

def _inference(datasets, source_language, target_language):

    if source_language == "en" and target_language == "ca":
        model = "eng-cat"
    elif source_language == "ca" and target_language == "en":
        model = "cat-eng"
    elif source_language == "de" and target_language == "ca":
        model = "deu-cat"
    elif source_language == "ca" and target_language == "de":
        model = "cat-deu"
    else:
        print(f"Unknown translation model {source_language}, {target_language}")
        exit(0)

    engine = "nmt-softcatala"
    for ds in datasets:
        print("-- " + ds[0])

        source_file = ds[1].format(source_language, target_language, engine.lower(), source_language)
        hypotesis_file = ds[2].format(source_language, target_language, engine.lower(), target_language)
#        cmd = f'docker run -it -v "$(pwd)":/srv/files/ --env CTRANSLATE_BEAM_SIZE=2 --env COMMAND_LINE="-f {source_file} -t {hypotesis_file} -m {model}" --rm use-models-tools --name use-models-tools'
        cmd = f'python3 ../use-models-tools/model-to-txt.py -x ../models/ -f {source_file} -t {hypotesis_file} -m {model}'
        print(cmd)
        os.system(cmd)

def read_parameters():
    parser = OptionParser()

    parser.add_option(
        '-l',
        '--language-pair',
        type='string',
        action='store',
        dest='lang_pair',
        default = '',
        help='Language pair to evaluate (e.g. en-ca)'
    )

    parser.add_option(
        '-i',
        '--inference',
        action="store_true",
        dest='inference',
        default='false',
        help='Translate opennmt dataset to evaluate later new results'
    )

    (options, args) = parser.parse_args()

    if options.inference == True and len(options.lang_pair) == 0:
        print("Inference option needs a language pair")
        exit(1)

    return options.lang_pair, options.inference


def main():

    lang_pair, inference = read_parameters()

    datasets_en_ca = \
        [\
            ['Sleepyhollow', 'input/sleepyhollow-{0}-{1}.{3}',
                 'translated/sleepyhollow-{0}-{1}-{2}.{3}' ],

            ['Tatoeba', 'input/tatoeba-{0}-{1}.{3}',
                 'translated/tatoeba-{0}-{1}-{2}.{3}' ],

            ['SC Users', 'input/sc-users-{0}-{1}.{3}',
                'translated/sc-users-{0}-{1}-{2}.{3}'],

            ['Fedalist', 'input/federalist-{0}-{1}.{3}',
                'translated/federalist-{0}-{1}-{2}.{3}']
        ]

    datasets_de_ca = \
        [\
            ['Tatoeba', 'input/tatoeba-{0}-{1}.{1}',
                 'translated/tatoeba-{0}-{1}-{2}.{3}'],

            ['Ubuntu', 'input/ubuntu-{0}-{1}.{1}',
                 'translated/ubuntu-{0}-{1}-{2}.{3}'],

        ]

    datasets_ca_de = \
        [\
            ['Ubuntu', 'input/ubuntu-{1}-{0}.{1}',
                 'translated/ubuntu-{1}-{0}-{2}.{3}']
        ]

    if inference is True:
        if lang_pair == 'en-ca':
            _inference(datasets_en_ca, "en", "ca")

        if lang_pair == 'de-ca':
            _inference(datasets_de_ca, "de", "ca")

        if lang_pair == 'ca-de':
            _inference(datasets_ca_de, "ca", "de")
    else:
        print("Eval")
        if len(lang_pair) == 0 or lang_pair == 'en-ca':
            _evaluate(datasets_en_ca, "en", "ca", "English > Catalan")

        if len(lang_pair) == 0 or lang_pair == 'de-ca':
            _evaluate(datasets_de_ca, "de", "ca", "German > Catalan")

        if len(lang_pair) == 0 or lang_pair == 'ca-de':
            _evaluate(datasets_ca_de, "ca", "de", "Catalan > German")

if __name__ == "__main__":
    main()
