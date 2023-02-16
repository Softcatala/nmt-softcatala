# -*- coding: utf-8 -*-
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

from nmt_sc.preservemarkup import PreserveMarkup
import unittest


class TestPreserveMarkup(unittest.TestCase):

    TAG_0 = PreserveMarkup.TAG + "0"
    TAG_1 = PreserveMarkup.TAG + "1"
    TAG_2 = PreserveMarkup.TAG + "2"
    TAG_3 = PreserveMarkup.TAG + "3"

    def test_create_markers_in_string(self):
        preserve_markup = PreserveMarkup()
        text = '<b>Hello</b>'
        markers, text = preserve_markup.create_markers_in_string(text)
        keys = list(markers.keys())
        self.assertEquals(f"{self.TAG_0} Hello {self.TAG_1}", text)
        self.assertEquals(f"{self.TAG_0} ", keys[0])
        self.assertEquals(f" {self.TAG_1}", keys[1])

    def test_create_markers_in_string_two_words(self):
        preserve_markup = PreserveMarkup()
        text = '<b>Hello</b><u id=1>World</u>'
        markers, text = preserve_markup.create_markers_in_string(text)
        keys = list(markers.keys())
        self.assertEquals(f"{self.TAG_0} Hello {self.TAG_1}  {self.TAG_2} World {self.TAG_3}", text)
        self.assertEquals(f"{self.TAG_0} ", keys[0])
        self.assertEquals(f" {self.TAG_1} ", keys[1])
        self.assertEquals(f" {self.TAG_2} ", keys[2])
        self.assertEquals(f" {self.TAG_3}", keys[3])

    def test_create_markers_in_string_self_close(self):
        preserve_markup = PreserveMarkup()
        text = 'Hello<br/>my friends'
        markers, text = preserve_markup.create_markers_in_string(text)
        keys = list(markers.keys())
        self.assertEquals(f"Hello {self.TAG_0} my friends", text)
        self.assertEquals(f" {self.TAG_0} ", keys[0])
        
    def test_get_back_markup(self):
        preserve_markup = PreserveMarkup()
        src_text = '<b>Hello</b>'
        markers, text = preserve_markup.create_markers_in_string(src_text)
        translated = preserve_markup.get_back_markup(text, markers)
        self.assertEquals(src_text, translated)

    def _simulate_ctranslate_eating_spaces_when_translating(self, text, markers):
        marker0 = list(markers.keys())[0]
        marker3 = list(markers.keys())[3]
        translated_text = text.replace(marker0, marker0[0:-1])
        translated_text = translated_text.replace(marker3, marker3[1:])
        return translated_text

    def test_get_back_markup_spaces_removed_by_ctranslator(self):
        preserve_markup = PreserveMarkup()
        src_text = '<b>Hello</b><i>there</i>'
        markers, text = preserve_markup.create_markers_in_string(src_text)

        translated_text = self._simulate_ctranslate_eating_spaces_when_translating(text, markers)

        translated = preserve_markup.get_back_markup(translated_text, markers)
        self.assertEquals(src_text, translated)

if __name__ == '__main__':
    unittest.main()
