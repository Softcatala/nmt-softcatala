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
        self.assertEqual(f"{self.TAG_0} Hello {self.TAG_1}", text)
        self.assertEqual(f"{self.TAG_0} ", keys[0])
        self.assertEqual(f" {self.TAG_1}", keys[1])

    def test_create_markers_in_string_two_words(self):
        preserve_markup = PreserveMarkup()
        text = '<b>Hello</b><u id=1>World</u>'
        markers, text = preserve_markup.create_markers_in_string(text)
        keys = list(markers.keys())
        self.assertEqual(f"{self.TAG_0} Hello {self.TAG_1}  {self.TAG_2} World {self.TAG_3}", text)
        self.assertEqual(f"{self.TAG_0} ", keys[0])
        self.assertEqual(f" {self.TAG_1} ", keys[1])
        self.assertEqual(f" {self.TAG_2} ", keys[2])
        self.assertEqual(f" {self.TAG_3}", keys[3])

    def test_create_markers_in_string_self_close(self):
        preserve_markup = PreserveMarkup()
        text = 'Hello<br/>my friends'
        markers, text = preserve_markup.create_markers_in_string(text)
        keys = list(markers.keys())
        self.assertEqual(f"Hello {self.TAG_0} my friends", text)
        self.assertEqual(f" {self.TAG_0} ", keys[0])
        
    def test_get_back_markup(self):
        preserve_markup = PreserveMarkup()
        src_text = '<b>Hello</b>'
        markers, text = preserve_markup.create_markers_in_string(src_text)
        translated = preserve_markup.get_back_markup(text, markers)
        self.assertEqual(src_text, translated)

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
        self.assertEqual(src_text, translated)

    UNKNOWN = "_`@|>=€°"

    def _protect(self, text):
        preserve_markup = PreserveMarkup(lambda char: char in self.UNKNOWN)
        markers, marked = preserve_markup.create_markers_in_string(text)
        self.assertEqual(text, preserve_markup.get_back_markup(marked, markers))
        return list(markers.values()), marked

    def test_code_spans(self):
        text = ("An MR numbered 125 made against the ``ubports/24.6.x`` branch of Git repository "
                "``morph-browser`` will have an APT archive named ``24.6.x_-_PR_morph-browser_125``.")
        protected, marked = self._protect(text)
        self.assertEqual(["``ubports/24.6.x``", "``morph-browser``", "``24.6.x_-_PR_morph-browser_125``"], protected)
        self.assertNotIn("`", marked)

    def test_single_backtick_code_span(self):
        protected, _ = self._protect("Run `make install` now.")
        self.assertEqual(["`make install`"], protected)

    def test_words_with_unknown_chars(self):
        protected, marked = self._protect("Set my_variable_name and mail user@example.com.")
        self.assertEqual(["my_variable_name", "user@example.com"], protected)
        self.assertTrue(marked.endswith("."))

    def test_surrounding_punctuation_left_to_the_model(self):
        protected, marked = self._protect("(see my_var), then stop.")
        self.assertEqual(["my_var"], protected)
        self.assertTrue(marked.startswith("("))

    def test_standalone_unknown_chars(self):
        protected, _ = self._protect("If x >= 3, it costs 20 € at 30 °C, a | b.")
        self.assertEqual([">=", "€", "°C", "|"], protected)

    def test_tags_keep_text_between_them(self):
        protected, marked = self._protect("Click <b>Save</b> to keep my_file.")
        self.assertEqual(["<b>", "</b>", "my_file"], protected)
        self.assertIn(" Save ", marked)

    def test_text_without_unknown_chars_is_unchanged(self):
        protected, marked = self._protect("Please restart your computer.")
        self.assertEqual([], protected)
        self.assertEqual("Please restart your computer.", marked)

    def test_get_back_markup_brace_removed_by_ctranslator(self):
        preserve = PreserveMarkup(lambda c: c == "_")
        markers, text = preserve.create_markers_in_string("See ([link](https://example.org/a_b)) now")
        # The model returns "See ([877190 )) now": it drops both the space and the {.
        restored = preserve.get_back_markup(text.replace(" {", ""), markers)
        self.assertEqual("See ([link](https://example.org/a_b)) now", restored)

    def test_more_than_ten_markers(self):
        text = " ".join(f"<i>w{i}</i>" for i in range(8))
        protected, _ = self._protect(text)
        self.assertEqual(16, len(protected))

    def test_custom_tag(self):
        preserve_markup = PreserveMarkup(tag="87719")
        markers, text = preserve_markup.create_markers_in_string("<b>Hello</b>")
        self.assertEqual("877190 Hello 877191", text)

if __name__ == '__main__':
    unittest.main()
