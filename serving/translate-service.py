#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
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
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

from flask import Flask, request, Response
import json
import logging
import os
import pyonmttok


app = Flask(__name__)


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
    print(text)
    tokenizer = pyonmttok.Tokenizer("conservative")
    _default=10.0
    output = translate(stub, model_name, [text], tokenizer, timeout=_default)
    print(output[0])
    return output[0]



@app.route('/translate/', methods=['GET'])
def translate_api():
    text = request.args.get('text')

    channel = grpc.insecure_channel("%s:%d" % ('localhost', 8500))
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    model_name = 'eng-cat'

    translated = _translate_sentence(stub, model_name, text)

    result = {}
    result['text'] = text
    result['translated'] = translated
    return json_answer(json.dumps(result, indent=4, separators=(',', ': ')))

def json_answer(data):
    resp = Response(data, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp



if __name__ == '__main__':
    app.debug = True
    app.run()
