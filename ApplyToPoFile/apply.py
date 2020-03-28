#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018-2020 Jordi Mas i Hernandez <jmas@softcatala.org>
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
from opennmt import OpenNMT

import polib
from shutil import copyfile
import logging
import os
from optparse import OptionParser



def _clean_string(result):
    CHARS = (
        '_', '&', '~',  # Accelerators.
        ':', ',', '...', u'…'  # Punctuations.
    )
    for c in CHARS:
        result = result.replace(c, '')

    return result.strip()

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
        dest='po_file',
        help='PO File to translate'
    )

    (options, args) = parser.parse_args()
    if options.po_file is None:  # if filename is not given
        parser.error('PO file not given')
    return options.model_name, options.po_file

def main():

    init_logging(True)

    print("Applies a OpenNMT model to translate a PO file")
    model_name, input_filename = read_parameters()
    target_filename = input_filename + "-ca.po"
    copyfile(input_filename, target_filename)

    openNMT = OpenNMT()
    
    po_file = polib.pofile(target_filename)
    translated = 0
    errors = 0
    for entry in po_file:

        if entry.translated():
            logging.debug('Already translated: ' + str(entry.msgid))
            continue

        if 'fuzzy' in entry.flags:
            continue

        src = _clean_string(entry.msgid)

        try:
            tgt = openNMT.translate(model_name, src)

            add = True
            
            if add:
                translated = translated + 1
                entry.msgstr = tgt
                entry.tcomment = "Imported from NMT"
                entry.flags.append('fuzzy')

                logging.debug('Source: ' + str(entry.msgid))
                logging.debug('Target: ' + str(tgt))

            if translated % 500 == 0:
                print(translated)
                po_file.save(target_filename)
        
        except Exception as e:
            errors = errors + 1

    po_file.save(target_filename)

    print("Sentences translated: {0}".format(translated))
    print("Sentences unable to translate {0} (NMT errors)".format(errors))


if __name__ == "__main__":
    main()
