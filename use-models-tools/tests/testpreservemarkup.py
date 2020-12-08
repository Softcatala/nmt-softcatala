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

from preservemarkup import PreserveMarkup
import unittest


class TestPreserveMarkup(unittest.TestCase):


    def test_create_markers_in_string(self):
        preserve_markup = PreserveMarkup()
        text = '<b>Hello</b>'
        markers, text = preserve_markup.create_markers_in_string(text)
        print(markers)
        print(text)
        keys = list(markers.keys())
        self.assertEquals("{877190 Hello {877191", text)
        self.assertEquals("{877190 ", keys[0])
        self.assertEquals(" {877191", keys[1])

    def test_create_markers_in_string_two_words(self):
        preserve_markup = PreserveMarkup()
        text = '<b>Hello</b><u id=1>World</u>'
        markers, text = preserve_markup.create_markers_in_string(text)
        print(markers)
        print(text)
        keys = list(markers.keys())
        self.assertEquals("{877190 Hello {877191  {877192 World {877193", text)
        self.assertEquals("{877190 ", keys[0])
        self.assertEquals(" {877191 ", keys[1])
        self.assertEquals(" {877192 ", keys[2])
        self.assertEquals(" {877193", keys[3])

    def test_create_markers_in_string_self_close(self):
        preserve_markup = PreserveMarkup()
        text = 'Hello<br/>my friends'
        markers, text = preserve_markup.create_markers_in_string(text)
        print(markers)
        print(text)
        keys = list(markers.keys())
        self.assertEquals("Hello {877190 my friends", text)
        self.assertEquals(" {877190 ", keys[0])
        
    def test_get_back_markup(self):
        preserve_markup = PreserveMarkup()
        src_text = '<b>Hello</b>'
        markers, text = preserve_markup.create_markers_in_string(src_text)
        translated = preserve_markup.get_back_markup(text, markers)
        self.assertEquals(src_text, translated)


if __name__ == '__main__':
    unittest.main()
