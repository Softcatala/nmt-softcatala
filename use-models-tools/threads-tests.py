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
from threading import Thread

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


def translate_thread(sentence, openNMT, i, model_name, results):
    results[i] = openNMT.translate(model_name, sentence)
    print("{0} -> {1}".format(i, results[i]))

def threads(src, openNMT, times):
    start_time = datetime.datetime.now()
 
    num_threads = times
    threads = []
    results = ["" for x in range(num_threads)]
    for i in range(num_threads):
        print('Starting thread {0}'.format(i))
        process = Thread(target=translate_thread, args=[src, openNMT, i, 'eng-cat', results])
        process.start()
        threads.append(process)

    for process in threads:
        process.join()

    return str(datetime.datetime.now() - start_time)
#2.96
def loop(src, openNMT, times):
    start_time = datetime.datetime.now()
    for i in range(0, times):
        print(i)
        tgt = openNMT.translate('eng-cat', src)   
#    print(tgt)
    return str(datetime.datetime.now() - start_time)
    



def main():

    src = "But the US Constitution says the states maintain public order and safety"

    start_time = datetime.datetime.now()
    init_logging(True)
    times = 8
    openNMT = OpenNMT()
    openNMT.tokenizer_source = pyonmttok.Tokenizer(mode="none", sp_model_path="en_m.model")
    openNMT.tokenizer_target = pyonmttok.Tokenizer(mode="none", sp_model_path="ca_m.model")

    t_threads = threads(src, openNMT, times)
    t_loop = loop(src, openNMT, times)

    print("Time used threads {0}".format(t_threads))
    print("Time used loop {0}".format(t_loop))

if __name__ == "__main__":
    main()
