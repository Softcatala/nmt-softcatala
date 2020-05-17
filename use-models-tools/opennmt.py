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
import grpc
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
import pyonmttok
import os
from texttokenizer import TextTokenizer

class OpenNMT():

    ENV_NAME = 'OPENNMT_SERVER'

    def __init__(self):
        self.model_name = None
        self.channel = None
        self.stub = None
        self._server = self._get_default_server()
        self.tokenizer_source = None
        self.tokenizer_target = None

    def _get_default_server(self):
        if self.ENV_NAME in os.environ:
            server = os.environ[self.ENV_NAME]
        else:
            server = 'localhost:8500'

        return server

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, value):
        self._server = value

    def _pad_batch(self, batch_tokens):
        lengths = [len(tokens) for tokens in batch_tokens]
        max_length = max(lengths)
        for tokens, length in zip(batch_tokens, lengths):
            if max_length > length:
                tokens += [""] * (max_length - length)
        return batch_tokens, lengths, max_length

    def _extract_prediction(self, result):
        batch_lengths = tf.make_ndarray(result.outputs["length"])
        batch_predictions = tf.make_ndarray(result.outputs["tokens"])
        for hypotheses, lengths in zip(batch_predictions, batch_lengths):
            # Only consider the first hypothesis (the best one).
            best_hypothesis = hypotheses[0].tolist()
            best_length = lengths[0]
            if best_hypothesis[best_length - 1] == b"</s>":
                best_length -= 1
            yield best_hypothesis[:best_length]

    def _send_request(self, batch_tokens, timeout):
        batch_tokens, lengths, max_length = self._pad_batch(batch_tokens)
        batch_size = len(lengths)
        request = predict_pb2.PredictRequest()
        request.model_spec.name = self.model_name
        request.inputs["tokens"].CopyFrom(tf.make_tensor_proto(
            batch_tokens, dtype=tf.string, shape=(batch_size, max_length)))
        request.inputs["length"].CopyFrom(tf.make_tensor_proto(
            lengths, dtype=tf.int32, shape=(batch_size,)))
        return self.stub.Predict.future(request, timeout)

    def _translate_request(self, batch_text, timeout):
        batch_input = [self.tokenizer_source.tokenize(text)[0] for text in batch_text]
        future = self._send_request(batch_input, timeout=timeout)
        result = future.result()
        batch_output = [self.tokenizer_target.detokenize(prediction) for prediction in self._extract_prediction(result)]
        return batch_output

    def _translate_sentence(self, text):
        _default = 60.0
        output = self._translate_request([text], timeout=_default)
        return output[0]

    def translate(self, model_name, text):
        self.model_name = model_name
        self.channel = grpc.insecure_channel(self._server)
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(self.channel)
        translated = self._translate_sentence(text)
        return translated

    def _translate_split(self, sentence, i, model_name, results):
        if sentence.strip() == '':
            results[i] = ''
        else:
            results[i] = self.translate(model_name, sentence)


    def translate_splitted(self, model_name, text):
        tokenizer = TextTokenizer()
        sentences, translate = tokenizer.tokenize(text)

        num_sentences = len(sentences)
        threads = []
        results = ["" for x in range(num_sentences)]
        for i in range(num_sentences):
            if translate[i] is False:
                continue
            
            self._translate_split(sentences[i], i, model_name, results)

        return tokenizer.sentence_from_tokens(sentences, translate, results)

