# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 Jordi Mas i Hernandez <jmas@softcatala.org>
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

from nmt_sc.sentencepiecetokenizer import SentencePieceTokenizer
import unittest


class TestSentencePieceTokenizer(unittest.TestCase):

    def test_tokenize(self):
        sp = SentencePieceTokenizer("tests/data/eng-cat/tokenizer/sp_m.model")
        tokenized = sp.tokenize("Hola, com esteu avui?")
        self.assertEquals(['▁H', 'ola', ',', '▁com', '▁', 'est', 'eu', '▁a', 'v', 'ui', '?'], tokenized)

    def test_detokenize(self):
        sp = SentencePieceTokenizer("tests/data/eng-cat/tokenizer/sp_m.model")
        tokenized = sp.detokenize(['▁H', 'ola', ',', '▁com', '▁', 'est', 'eu', '▁a', 'v', 'ui', '?'])
        self.assertEquals("Hola, com esteu avui?", tokenized)

if __name__ == '__main__':
    unittest.main()
