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
import os
from texttokenizer import TextTokenizer
import ctranslate2
import pyonmttok

class CTranslate():

    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer_source = None
        self.tokenizer_target = None
        self.translator = ctranslate2.Translator(model_name)


    def _translate_request(self, batch_text, timeout):
        batch_input = [self.tokenizer_source.tokenize(text)[0] for text in batch_text]

        result = self.translator.translate_batch(batch_input, return_scores = False)
        tokens = result[0][0]['tokens']
        tokens = [tokens]
        batch_output = [self.tokenizer_target.detokenize(prediction) for prediction in tokens]
        return batch_output

    def _translate_sentence(self, text):
        _default = 60.0
        output = self._translate_request([text], timeout=_default)
        return output[0]

    def translate(self, text):
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
