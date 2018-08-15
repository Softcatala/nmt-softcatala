#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Jordi Mas i Hernandez <jmas@softcatala.org>
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
import tensorflow as tf
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
import polib
from shutil import copyfile
import re
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

def parse_translation_result(result):
    lengths = tf.make_ndarray(result.outputs["length"])[0]
    hypotheses = tf.make_ndarray(result.outputs["tokens"])[0]

    # Only consider the first hypothesis (the best one).
    best_hypothesis = hypotheses[0]
    best_length = lengths[0]
    return best_hypothesis[0:best_length - 1] # Ignore </s>

def translate(stub, model_name, tokens, timeout=5.0):
    length = len(tokens)

    request = predict_pb2.PredictRequest()
    request.model_spec.name = model_name
    request.inputs["tokens"].CopyFrom(
        tf.make_tensor_proto([tokens], shape=(1, length)))
    request.inputs["length"].CopyFrom(
        tf.make_tensor_proto([length], shape=(1,)))

    return stub.Predict.future(request, timeout)

def _translate_sentence(stub, model_name, source):

    batch_tokens = list(source.split(' '))

    futures = []
    future = translate(stub, model_name, batch_tokens, timeout=100)
    futures.append(future)

    for tokens, future in zip(batch_tokens, futures):
        result = parse_translation_result(future.result())
 
    translated = ''
    cnt = 0
    last = len(result)
    for token in list(result):
        translated += str(token, encoding="utf8")
        cnt = cnt + 1
        if cnt < last:
            translated += ' '
       
    # Fixes https://github.com/OpenNMT/OpenNMT-tf/issues/188
    translated = re.sub("<\/s>","", translated)
    return translated

def _translate_sentence_with_tags(stub, model_name, source):
    '''
        OpenNMT models cannot process XML tags properly (they get translated)
        If a setences has tags, we split the text as translate them as individual
        segments.

        For example, 'Hello <b>world</b>' will generate two translations
        requests 'hello' and 'world'
    '''
    regex = re.compile(r"\<(.*?)\>", re.VERBOSE)
    matches = list(regex.finditer(source))

    if len(matches) == 0:
        return _translate_sentence(stub, model_name, source)

    result = ''
    pos = 0
    for match in matches:
        result += _translate_sentence(stub, model_name, source[pos:match.start()])
        result += source[match.start():match.end()]
        pos = match.end()

    result += _translate_sentence(stub, model_name, source[pos:])
    return result

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
        default='',
        help='PO File to translate'
    )

    (options, args) = parser.parse_args()
    return options.model_name, options.po_file

def main():

    init_logging(True)

    print("Applies a OpenNMT model to translate a PO file")
    model_name, input_filename = read_parameters()
    target_filename = input_filename + "-ca.po"
    copyfile(input_filename, target_filename)

    channel = implementations.insecure_channel('localhost', 9000)
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

    po_file = polib.pofile(target_filename)
    translated = 0
    errors = 0
    for entry in po_file:

        if entry.translated():
            logging.debug('Already translated: ' + str(entry.msgid))
            continue

        src = _clean_string(entry.msgid)

        add = True
        try:
            tgt = _translate_sentence_with_tags(stub, model_name, src)
        except Exception as e:
            logging.error(str(e))
            logging.error("Processing: {0}".format(src))
            add = False
            errors = errors + 1

        if add:
            translated = translated + 1
            entry.msgstr = tgt
            entry.flags.append('fuzzy')

            logging.debug('Source: ' + str(entry.msgid))
            logging.debug('Target: ' + str(tgt))

        po_file.save(target_filename)

    print("Sentences translated: {0}".format(translated))
    print("Sentences unable to translate {0} (NMT errors)".format(errors))


if __name__ == "__main__":
    main()
