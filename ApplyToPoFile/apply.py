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
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

import polib
from shutil import copyfile
import re
import logging
import os
from optparse import OptionParser
import pyonmttok
import grpc

def pad_batch(batch_tokens):
  """Pads a batch of tokens."""
  lengths = [len(tokens) for tokens in batch_tokens]
  max_length = max(lengths)
  for tokens, length in zip(batch_tokens, lengths):
    if max_length > length:
      tokens += [""] * (max_length - length)
  return batch_tokens, lengths, max_length

def extract_prediction(result):
  """Parses a translation result.

  Args:
    result: A `PredictResponse` proto.

  Returns:
    A generator over the hypotheses.
  """
  batch_lengths = tf.make_ndarray(result.outputs["length"])
  batch_predictions = tf.make_ndarray(result.outputs["tokens"])
  for hypotheses, lengths in zip(batch_predictions, batch_lengths):
    # Only consider the first hypothesis (the best one).
    best_hypothesis = hypotheses[0].tolist()
    best_length = lengths[0]
    if best_hypothesis[best_length - 1] == b"</s>":
      best_length -= 1
    yield best_hypothesis[:best_length]

def send_request(stub, model_name, batch_tokens, timeout=5.0):
  """Sends a translation request.

  Args:
    stub: The prediction service stub.
    model_name: The model to request.
    tokens: A list of tokens.
    timeout: Timeout after this many seconds.

  Returns:
    A future.
  """
  batch_tokens, lengths, max_length = pad_batch(batch_tokens)
  batch_size = len(lengths)
  request = predict_pb2.PredictRequest()
  request.model_spec.name = model_name
  request.inputs["tokens"].CopyFrom(tf.make_tensor_proto(
      batch_tokens, dtype=tf.string, shape=(batch_size, max_length)))
  request.inputs["length"].CopyFrom(tf.make_tensor_proto(
      lengths, dtype=tf.int32, shape=(batch_size,)))
  return stub.Predict.future(request, timeout)

def translate(stub, model_name, batch_text, tokenizer, timeout=5.0):
  """Translates a batch of sentences.

  Args:
    stub: The prediction service stub.
    model_name: The model to request.
    batch_text: A list of sentences.
    tokenizer: The tokenizer to apply.
    timeout: Timeout after this many seconds.

  Returns:
    A generator over the detokenized predictions.
  """
  batch_input = [tokenizer.tokenize(text)[0] for text in batch_text]
  future = send_request(stub, model_name, batch_input, timeout=timeout)
  result = future.result()
  batch_output = [tokenizer.detokenize(prediction) for prediction in extract_prediction(result)]
  return batch_output


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


def _translate_sentence(stub, model_name, text):
    tokenizer = pyonmttok.Tokenizer("conservative")
    _default=10.0
    output = translate(stub, model_name, [text], tokenizer, timeout=_default)
    return output[0]

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

    channel = grpc.insecure_channel("%s:%d" % ('localhost', 8500))
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

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
            tgt = _translate_sentence_with_tags(stub, model_name, src)
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
