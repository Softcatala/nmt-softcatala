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

from nmt_sc.model_to_po import _clean_string
import unittest


class TestModelToPo(unittest.TestCase):

    def test_clean_string_removes_accelerators(self):
        for text, expected in [("_File", "File"), ("&Open", "Open"), ("~Save", "Save"),
                               ("Save _As...", "Save As..."), ("Sa&ve", "Save"), ("E~xit", "Exit")]:
            self.assertEqual(expected, _clean_string(text), text)

    def test_clean_string_keeps_other_uses(self):
        for text in ["my_variable_name", "24.6.x_-_PR_morph-browser_125", "Tom & Jerry",
                     "Fish &amp; chips", "Rock&Roll&Blues", "Use ``_a_b`` here",
                     "__init__", "_private_member", "AT&amp;T", "Area &sup2;", "&#x27;quoted&#39;"]:
            self.assertEqual(text, _clean_string(text), text)

    def test_clean_string_skips_code_spans(self):
        self.assertEqual("Use ``~/.config`` now", _clean_string("Use ``~/.config`` _now"))


if __name__ == '__main__':
    unittest.main()
