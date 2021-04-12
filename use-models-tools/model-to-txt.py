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

from __future__ import print_function
import logging
import os
import datetime
from optparse import OptionParser
from ctranslate import CTranslate
import pyonmttok
from threading import Thread

def init_logging(del_logs):
    logfile = 'model-to-txt.log'

    if del_logs and os.path.isfile(logfile):
        os.remove(logfile)

    import logging
    logger = logging.getLogger()

    hdlr = logging.FileHandler(logfile)
    logger.addHandler(hdlr)
    logger.setLevel(logging.WARNING)

def read_parameters():
    parser = OptionParser()

    parser.add_option(
        '-m',
        '--model_name',
        type='string',
        action='store',
        default='eng-cat',
        dest='model_name',
        help="Translation model name. For example 'eng-cat' or 'cat-eng'"
    )

    parser.add_option(
        '-f',
        '--txt-file',
        type='string',
        action='store',
        dest='txt_file',
        help='TXT File to translate'
    )

    parser.add_option(
        '-t',
        '--translated-file',
        type='string',
        action='store',
        dest='translated_file',
        help='Name of the translated file'
    )

    parser.add_option(
        '-p',
        '--tokenizer-models',
        type='string',
        action='store',
        dest='tokenizer_models',
        default='',
        help='Path to tokenizer SentencePiece models'
    )

    parser.add_option(
        '-x',
        '--translation-models',
        type='string',
        action='store',
        dest='translation_models',
        default='',
        help='Path to translation models'
    )

    parser.add_option(
        '-r',
        '--threads',
        type='int',
        action='store',
        dest='n_threads',
        default=1,
        help='Number of threads in the client side'
    )

    (options, args) = parser.parse_args()
    if options.txt_file is None:
        parser.error('TXT file not given')

    if options.translated_file is None:
        parser.error('Translate file not given')

    return options.model_name, options.txt_file, options.translated_file, options.tokenizer_models, options.translation_models, options.n_threads

def translate_thread(src, language, openNMT, translations, index, tf_ca):
    try:
        translations[index] = openNMT.translate_splitted(src, language)
    except Exception as e:
        translations[index] = "Error"
        logging.error(str(e))
        logging.error("Processing: {0}".format(src))
        #tf_ca.write("{0}\n".format("Error"))

def main():

    print("Applies an OpenNMT model to translate a TXT file")

    start_time = datetime.datetime.now()
    init_logging(True)
    model_name, input_filename, translated_file, tokenizer_models, translation_models, n_threads = read_parameters()
    print(f'Client threads: {n_threads}')

    model_path = os.path.join(translation_models, model_name)
    openNMT = CTranslate(model_path)

    if model_name == 'eng-cat':
        src_model_path = os.path.join(tokenizer_models, "en_m.model")
        tgt_model_path = os.path.join(tokenizer_models, "ca_m.model")
        language = 'English'
    elif model_name == 'cat-eng':
        src_model_path = os.path.join(tokenizer_models, "ca_m.model")
        tgt_model_path = os.path.join(tokenizer_models, "en_m.model")
        language = 'Catalan'
    elif model_name == 'deu-cat':
        src_model_path = os.path.join(tokenizer_models, "de_m.model")
        tgt_model_path = os.path.join(tokenizer_models, "ca_m.model")
        language = 'German'


    openNMT.tokenizer_source = pyonmttok.Tokenizer(mode="none", sp_model_path = src_model_path)
    openNMT.tokenizer_target = pyonmttok.Tokenizer(mode="none", sp_model_path = tgt_model_path)

    target_filename_review = "translated-review.txt"
    with open(input_filename, encoding='utf-8', mode='r', errors='ignore') as tf_en,\
         open(translated_file, encoding='utf-8', mode='w') as tf_ca,\
         open(target_filename_review, encoding='utf-8', mode='w') as tf_ca_review:

        en_strings = tf_en.readlines()
        len_en_strings = len(en_strings)
        translated = 0
        errors = 0

        i = 0
        while i < len_en_strings:

            threads = []
            sources = []
            translations = []
            num_threads = min(n_threads, len_en_strings - i)

            for t in range(0, num_threads):
                sources.append(en_strings[i + t].replace('\n', ''))
                translations.append("")

            for t in range(0, num_threads):
                src = sources[t]
                process = Thread(target=translate_thread, args=[sources[t], language, openNMT, translations, t, tf_ca])
                process.start()
                threads.append(process)
              
            for process in threads:
                process.join()

            for t in range(0, num_threads):
                i = i + 1
                translated = translated + 1
                if translated % 500 == 0:
                    print(translated)

                src = sources[t]
                tgt = translations[t]
                tf_ca.write("{0}\n".format(tgt))
                tf_ca_review.write("{0}\n{1}\n\n".format(src, tgt))
                logging.debug('Source: ' + str(src))
                logging.debug('Target: ' + str(tgt))

    print("Sentences translated: {0}".format(translated))
    print("Sentences unable to translate {0} (NMT errors)".format(errors))
    print("Time used {0}".format(str(datetime.datetime.now() - start_time)))

if __name__ == "__main__":
    main()
