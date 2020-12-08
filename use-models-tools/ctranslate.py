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
from preservemarkup import PreserveMarkup

class CTranslate():

    INTER_THREADS = 'CTRANSLATE_INTER_THREADS'
    INTRA_THREADS = 'CTRANSLATE_INTRA_THREADS'
    BEAM_SIZE = 'CTRANSLATE_BEAM_SIZE'
    USE_VMAP = 'CTRANSLATE_USE_VMAP'

    def __init__(self, model_path):
        self.model_path = model_path
        self.tokenizer_source = None
        self.tokenizer_target = None

        if self.INTER_THREADS in os.environ:
            inter_threads = int(os.environ[self.INTER_THREADS])
        else:
            inter_threads = 1

        if self.INTRA_THREADS in os.environ:
            intra_threads = int(os.environ[self.INTRA_THREADS])
        else:
            intra_threads = 4

        if self.BEAM_SIZE in os.environ:
            self.beam_size = int(os.environ[self.BEAM_SIZE])
        else:
            self.beam_size = 2

        if self.USE_VMAP in os.environ:
            self.use_vmap = True
        else:
            self.use_vmap = False

        print(f"inter_threads: {inter_threads}, intra_threads: {intra_threads}, beam_size {self.beam_size}, use_vmap {self.use_vmap}")
        self.translator = ctranslate2.Translator(model_path, inter_threads = inter_threads, intra_threads = intra_threads)


    def _translate_request(self, batch_text, timeout):
        batch_input = [self.tokenizer_source.tokenize(text)[0] for text in batch_text]

        result = self.translator.translate_batch(batch_input, return_scores = False, beam_size = self.beam_size, use_vmap = self.use_vmap)
        tokens = result[0][0]['tokens']
        tokens = [tokens]
        batch_output = [self.tokenizer_target.detokenize(prediction) for prediction in tokens]
        return batch_output

    def _translate_sentence(self, text):
        _default = 60.0

        preserve_markup = PreserveMarkup()
        markers, text = preserve_markup.create_markers_in_string(text)

#        print(f"input: '{text}'")
        output = self._translate_request([text], timeout=_default)
        translated = output[0]
#        print(f"pre-translated: '{translated}'")
        translated = preserve_markup.get_back_markup(translated, markers)
#        print(f"translated: '{translated}'")
        return translated


    def translate(self, text):
        translated = self._translate_sentence(text)
        return translated

    def _translate_split(self, sentence, i, results):
        if sentence.strip() == '':
            results[i] = ''
        else:
            results[i] = self.translate(sentence)


    def translate_splitted(self, text, language):
        tokenizer = TextTokenizer()
        sentences, translate = tokenizer.tokenize(text, language)

        num_sentences = len(sentences)
        threads = []
        results = ["" for x in range(num_sentences)]
        for i in range(num_sentences):
            if translate[i] is False:
                continue
            
            self._translate_split(sentences[i], i, results)

        return tokenizer.sentence_from_tokens(sentences, translate, results)
