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
from opennmt import OpenNMT
import pyonmttok


def init_logging(del_logs):
    logfile = 'model-to-text.log'

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
        help='Model name'
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

    (options, args) = parser.parse_args()
    if options.txt_file is None:
        parser.error('TXT file not given')

    if options.translated_file is None:
        parser.error('Translate file not given')

    return options.model_name, options.txt_file, options.translated_file

def main():

    start_time = datetime.datetime.now()
    init_logging(True)
    openNMT = OpenNMT()
    openNMT.tokenizer_source = pyonmttok.Tokenizer(mode="none", sp_model_path="en_m.model")
    openNMT.tokenizer_target = pyonmttok.Tokenizer(mode="none", sp_model_path="ca_m.model")

    print("Applies an OpenNMT model to translate a TXT file")
    print("Requieres a TensorFlow server answeering '{0}'".format(openNMT.server))
    model_name, input_filename, translated_file = read_parameters()
    target_filename_review = "translated-review.txt"

    with open(input_filename, 'r') as tf_en, open(translated_file, 'w') as tf_ca, open(target_filename_review, 'w') as tf_ca_review:
        en_strings = tf_en.readlines()
    
        translated = 0
        errors = 0

        for src in en_strings:
            src = src.replace('\n', '')

            try:
                tgt = openNMT.translate(model_name, src)
            except Exception as e:
                logging.error(str(e))
                logging.error("Processing: {0}".format(src))
                errors = errors + 1
                tf_ca.write("{0}\n".format("Error"))
                continue

            translated = translated + 1
            tf_ca.write("{0}\n".format(tgt))
            tf_ca_review.write("{0}\n{1}\n\n".format(src, tgt))
            logging.debug('Source: ' + str(src))
            logging.debug('Target: ' + str(tgt))

    print("Sentences translated: {0}".format(translated))
    print("Sentences unable to translate {0} (NMT errors)".format(errors))
    print("Time used {0}".format(str(datetime.datetime.now() - start_time)))

if __name__ == "__main__":
    main()
