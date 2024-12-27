# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Jordi Mas i Hernandez <jmas@softcatala.org>
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

from nmt_sc.ctranslate import CTranslate
import unittest

class CTranslate2Mock():

    def translate_batch(self, source, target_prefix=None, max_batch_size=0, batch_type="examples", beam_size=2, num_hypotheses=1,
         length_penalty=0, coverage_penalty=0, max_decoding_length=250, min_decoding_length=1, use_vmap=False,
         return_scores=True, return_attention=False, return_alternatives=False, sampling_topk=1, sampling_temperature=1,
         replace_unknowns=False):

        eng_to_cat = {
                        "▁Hello." : ["▁Hola", "."],
                        "▁How▁are▁you?" : ["▁Com", "▁estàs", "?"],
                        "▁It▁is▁getting▁late" : ["▁És", "▁tard", "."],
                        '▁Hello▁everybody.' : ['▁Hola', '▁a', '▁tothom', '.'],
                        '▁It▁is▁a▁sunny▁day.' : ['▁És', '▁un', '▁dia', '▁as', 'sol', 'ella', 't', '.'],
                        "▁Let's▁go▁to▁the▁beach." : ['▁Anem', '▁a', '▁la', '▁platja', '.']
                     }

        translations = []

        for sentence in source:
            translated_sentence = []
            single_text = ''
            for word in sentence:
                single_text += word

            if single_text in eng_to_cat:
                translated= eng_to_cat[single_text]
            else:
                translated = sentence

            token_dict = {}
            token_dict["tokens"] = translated
            translations.append([token_dict])

        return translations


class TestCTranslate(unittest.TestCase):

    def test_translate_parallel(self):
        ctranslate = CTranslate("tests/data/", "eng-cat", translator = CTranslate2Mock())

        text = 'Hello.\rHow are you?\rIt is getting late'
        translated = ctranslate.translate_parallel(text)

        sentences = translated.split("\r")
        self.assertEquals(3, len(sentences))
        self.assertEquals("Hola.", sentences[0])
        self.assertEquals("Com estàs?", sentences[1])
        self.assertEquals("És tard.", sentences[2])

    def test_translate_parallel_three_sentences_one_line(self):
        ctranslate = CTranslate("tests/data/", "eng-cat", translator = CTranslate2Mock())

        text = "Hello everybody. It is a sunny day. Let's go to the beach."
        translated = ctranslate.translate_parallel(text)

        self.assertEquals("Hola a tothom. És un dia assolellat. Anem a la platja.", translated)

    def test_normalize_input_string_cat(self):
        ctranslate = CTranslate("tests/data/", "cat-eng", translator = CTranslate2Mock())

        text = 'L’oferta demà és molt bona'

        result = ctranslate._normalize_input_string(text)
        self.assertEquals("L'oferta demà és molt bona", result)

    def test_languages(self):
        ctranslate = CTranslate("tests/data/", "cat-eng", translator = CTranslate2Mock())

        self.assertEquals('English', ctranslate._get_sentence_tokenizer_language("eng-cat"))
        self.assertEquals('Catalan', ctranslate._get_sentence_tokenizer_language("cat-eng"))
        self.assertEquals('Catalan', ctranslate._get_sentence_tokenizer_language("oci-eng"))
        self.assertEquals('Danish', ctranslate._get_sentence_tokenizer_language("swe-eng"))
        self.assertEquals('Generic', ctranslate._get_sentence_tokenizer_language("xxx-xxx"))

if __name__ == '__main__':
    unittest.main()
