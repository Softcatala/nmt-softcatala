#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018-2021 Jordi Mas i Hernandez <jmas@softcatala.org>
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
import datetime
import polib
from shutil import copyfile
import os
from optparse import OptionParser
import logging
from .ctranslate import CTranslate

def init_logging(del_logs):
    logfile = 'model-to-po.log'

    if del_logs and os.path.isfile(logfile):
        os.remove(logfile)

    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    logger.addHandler(hdlr)
    logger.setLevel(logging.WARNING)

def _clean_string(result):
    CHARS = (
        '_', '&', '~',  # Accelerators.
    )
    for c in CHARS:
        result = result.replace(c, '')

    return result.strip()


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
        '--po-file',
        type='string',
        action='store',
        dest='po_file',
        help='PO File to translate'
    )

    parser.add_option(
        '-t',
        '--translated-file',
        type='string',
        action='store',
        dest='translated_file',
        default='',
        help='Name of the translated file'
    )

    parser.add_option(
        '-x',
        '--models',
        type='string',
        action='store',
        dest='models_path',
        default='',
        help='Path the model directory'
    )

    (options, args) = parser.parse_args()
    if options.po_file is None:  # if filename is not given
        parser.error('PO file not given')

    return options.model_name, options.po_file, options.translated_file,\
           options.models_path

def _translate(openNMT, src_org):
    src = _clean_string(src_org)
    tgt = openNMT.translate_parallel(src)
    # Models do not return \n, add it the translated sentece to save the postediting
    if src_org.endswith("\n") and not tgt.endswith("\n"):
        tgt += "\n"

    return tgt

def main():

    print("Applies a OpenNMT model to translate a PO file")
    start_time = datetime.datetime.now()

    init_logging(True)
    model_name, input_filename, target_filename, models_path = read_parameters()

    if len(target_filename) == 0:
        target_filename = input_filename + "-ca.po"

    copyfile(input_filename, target_filename)

    print(f"{models_path} - {model_name}")
    openNMT = CTranslate(models_path, model_name)
    po_file = polib.pofile(target_filename)
    translated = 0
    errors = 0
    for entry in po_file:

        if entry.translated():
            continue

        if 'fuzzy' in entry.flags or entry.obsolete:
            continue

        try:
            if len(entry.msgid_plural) > 0:
                tgt = _translate(openNMT, entry.msgid)
                tgt_plural = _translate(openNMT, entry.msgid_plural)
                entry.msgstr_plural[0] = tgt
                entry.msgstr_plural[1] = tgt_plural
            else:
                tgt = _translate(openNMT, entry.msgid)
                entry.msgstr = tgt

            translated = translated + 1
            entry.flags.append('fuzzy')

            if translated % 500 == 0:
                print(translated)
                po_file.save(target_filename)
        
        except Exception as e:
            logging.error(str(e))
            logging.error("Processing: {0}".format(entry.msgid))
            errors = errors + 1

    po_file.save(target_filename)

    print("Sentences translated: {0}".format(translated))
    print("Sentences unable to translate: {0} (NMT errors)".format(errors))
    print("Time used: {0}".format(str(datetime.datetime.now() - start_time)))


if __name__ == "__main__":
    main()
