# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Jordi Mas i Hernandez <jmas@softcatala.org>
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

from nmt_sc.texttokenizer import TextTokenizer
import unittest


class TestTextTokenizer(unittest.TestCase):

    ENGLISH = "English"

    def test_tokenize_single_word(self):
        tokenizer = TextTokenizer()
        text = 'Hello'
        strings, translate = tokenizer.tokenize(text, self.ENGLISH)

        self.assertEquals(1, len(translate))
        self.assertEquals("Hello", strings[0])
        self.assertEquals(True, translate[0])

    def test_tokenize_single_word_with_dot(self):
        tokenizer = TextTokenizer()
        text = 'Hello.'
        strings, translate = tokenizer.tokenize(text, self.ENGLISH)

        self.assertEquals(1, len(translate))
        self.assertEquals("Hello.", strings[0])
        self.assertEquals(True, translate[0])

    def test_tokenize_two_sentences_with_newline(self):
        tokenizer = TextTokenizer()
        text = 'Hello.\nHow are you?'
        strings, translate = tokenizer.tokenize(text, self.ENGLISH)

        self.assertEquals(3, len(translate))
        self.assertEquals("Hello.", strings[0])
        self.assertEquals(True, translate[0])
        self.assertEquals("\n", strings[1])
        self.assertEquals(False, translate[1])
        self.assertEquals("How are you?", strings[2])
        self.assertEquals(True, translate[2])

    def test_tokenize_with_abbreviation(self):
        tokenizer = TextTokenizer()
        text = '"Why not, Mr. Wizard?" asked Jellia.\rNot now.'
        strings, translate = tokenizer.tokenize(text, self.ENGLISH)

        self.assertEquals(3, len(translate))
        self.assertEquals('"Why not, Mr. Wizard?" asked Jellia.', strings[0])
        self.assertEquals(True, translate[0])
        self.assertEquals("\r", strings[1])
        self.assertEquals(False, translate[1])
        self.assertEquals("Not now.", strings[2])
        self.assertEquals(True, translate[2])

if __name__ == '__main__':
    unittest.main()
