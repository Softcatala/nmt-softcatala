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


def init_logging(del_logs):
    logfile = 'apply.log'

    if del_logs and os.path.isfile(logfile):
        os.remove(logfile)

    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    logger = logging.getLogger('')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(console)


def read_parameters():
    parser = OptionParser()

    parser.add_option(
        '-m',
        '--model_name',
        type='string',
        action='store',
        dest='model_name',
        default='1532515736',
        help='Model name'
    )

    parser.add_option(
        '-f',
        '--po-file',
        type='string',
        action='store',
        dest='txt_file',
        help='TXT File to translate'
    )

    (options, args) = parser.parse_args()
    if options.txt_file is None:  # if filename is not given
        parser.error('TXT file not given')
    return options.model_name, options.txt_file

def main():

    start_time = datetime.datetime.now()
    init_logging(True)

    print("Applies a OpenNMT model to translate a TXT file")
    print("Requieres run-model-server.sh to be executed first")
    model_name, input_filename = read_parameters()
    target_filename = "translated.txt"
    target_filename_review = "translated-review.txt"

    openNMT = OpenNMT()
    with open(input_filename, 'r') as tf_en, open(target_filename, 'w') as tf_ca, open(target_filename_review, 'w') as tf_ca_review:
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
            tf_ca_review.write("{0} - {1}\n".format(src, tgt))
            logging.debug('Source: ' + str(src))
            logging.debug('Target: ' + str(tgt))

    print("Sentences translated: {0}".format(translated))
    print("Sentences unable to translate {0} (NMT errors)".format(errors))
    print("Time used {0}".format(str(datetime.datetime.now() - start_time)))

if __name__ == "__main__":
    main()
