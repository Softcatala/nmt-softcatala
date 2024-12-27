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
from .texttokenizer import TextTokenizer
import ctranslate2
import pyonmttok
from .preservemarkup import PreserveMarkup
import re
import logging
import unicodedata

class CTranslate():

    INTER_THREADS = 'CTRANSLATE_INTER_THREADS'
    INTRA_THREADS = 'CTRANSLATE_INTRA_THREADS'
    BEAM_SIZE = 'CTRANSLATE_BEAM_SIZE'
    USE_VMAP = 'CTRANSLATE_USE_VMAP'
    DEVICE = 'DEVICE'
    LANGUAGE_MATCH = "([a-z]{3})-([a-z]{3})"
    TOKENIZER_SUBDIR = "tokenizer"
    TOKENIZER_FILE = "sp_m.model"

    def __init__(self, models_path, model_name, translator = None):

        self._init_read_env_vars()

        model_path = os.path.join(models_path, model_name)
        tokenizer_path = os.path.join(model_path, self.TOKENIZER_SUBDIR, self.TOKENIZER_FILE)

        self.tokenizer = pyonmttok.Tokenizer(mode="none", sp_model_path = tokenizer_path)
        self.tokenizer_language = self._get_sentence_tokenizer_language(model_name)

        print(f"device: {self.device}, inter_threads: {self.inter_threads}, intra_threads: {self.intra_threads}, beam_size {self.beam_size}, use_vmap {self.use_vmap}")

        if translator is None:
            self.model_path = model_path
            ctranslate_model_path = os.path.join(model_path, "ctranslate2")
            self.translator = ctranslate2.Translator(ctranslate_model_path, device = self.device, inter_threads = self.inter_threads, intra_threads = self.intra_threads)
        else:
            self.translator = translator

        self.model_name = model_name


    def _init_read_env_vars(self):
        if self.INTER_THREADS in os.environ:
            self.inter_threads = int(os.environ[self.INTER_THREADS])
        else:
            self.inter_threads = 1

        if self.INTRA_THREADS in os.environ:
            self.intra_threads = int(os.environ[self.INTRA_THREADS])
        else:
            self.intra_threads = 4

        if self.BEAM_SIZE in os.environ:
            self.beam_size = int(os.environ[self.BEAM_SIZE])
        else:
            self.beam_size = 2

        if self.USE_VMAP in os.environ:
            self.use_vmap = True
        else:
            self.use_vmap = False

        self.device = os.environ.get(self.DEVICE, "cpu")

    def get_model_name(self):
        return self.model_name

    def get_model_description(self):
        filename = os.path.join(self.model_path, "metadata/model_description.txt")
        with open(filename, "r") as th_description:
            return th_description.read().splitlines()

    def _get_sentence_tokenizer_language(self, model_name):
        lang = re.match(self.LANGUAGE_MATCH, model_name).groups()[0]
        lang = lang[:2]

        choices = {'ca': 'Catalan', 'en': 'English', 'de' : 'German', 'fr' : 'French', 'sp' : 'Spanish', 'it' : 'Italian',
                  'nl' : 'Dutch', 'po' : 'Portuguese', 'jp': 'Japanese', 'gl': "Galician",
                  "oc": "Catalan", ## No Occitan support, Catalan rules probably the best for now
                  "sw": "Danish" ## Our best option today
                  }

        if lang in choices:
            return choices[lang]
        else:
            return "Generic"

    def _normalize_input_string(self, result):
        result = unicodedata.normalize('NFC', result)

        if (self.model_name[:3] == "cat"):
            mapping = {
                        '’' : '\'',
            }

            for char in mapping.keys():
                result = result.replace(char, mapping[char])

        return result

    def translate_parallel(self, text):

        text = self._normalize_input_string(text)

        # Split sentences
        tokenizer = TextTokenizer()
        sentences, translate = tokenizer.tokenize(text, self.tokenizer_language)
        input_batch = sentences

        num_sentences = len(sentences)
        logging.debug(f"_request_translation {num_sentences}")
        sentences_batch = []
        indexes = []
        results = ["" for x in range(num_sentences)]
        for i in range(num_sentences):
            if translate[i] is False:
                continue

            sentences_batch.append(sentences[i])
            indexes.append(i)

        translated_batch = self._translate_batch(sentences_batch)
        for pos in range(0, len(translated_batch)):
            i = indexes[pos]
            results[i] = translated_batch[pos] 

        logging.debug(f"_request_translation completed. Results: {len(results)}")
        #Rebuild split sentences
        translated = tokenizer.sentence_from_tokens(sentences, translate, results)
        return translated


    '''
        Translates asking CTranslate to batch / parallelize
    '''
    def _translate_batch(self, input_batch):

        batch_input_tokenized = []
        batch_input_markers = []

        preserve_markup = PreserveMarkup()

        num_sentences = len(input_batch)
        for pos in range(0, num_sentences):
            markers, text = preserve_markup.create_markers_in_string(input_batch[pos])
            tokenized = self.tokenizer.tokenize(text)[0]
            batch_input_tokenized.append(tokenized)
            batch_input_markers.append(markers)

        result = self.translator.translate_batch(batch_input_tokenized, return_scores=False, replace_unknowns=True,
                                                 beam_size=self.beam_size, use_vmap=self.use_vmap)

        batch_output = []
        for pos in range(0, num_sentences):
            tokenized = result[pos][0]['tokens']
            translated = self.tokenizer.detokenize(tokenized)
            translated = preserve_markup.get_back_markup(translated, batch_input_markers[pos])
            batch_output.append(translated)

        return batch_output
