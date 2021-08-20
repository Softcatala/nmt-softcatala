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

import unittest
join_single_file = __import__('join-single-file')


class TestJoinSingleFile(unittest.TestCase):

    def test_process_dot_no(self):
        src = "Yes"
        trg = "No"
        cnt = 0
        src, trg, cnt = join_single_file._process_dot(src, trg, cnt)

        self.assertEquals(0, cnt)
        self.assertEquals("Yes", src)
        self.assertEquals("No", trg)

    def test_process_dot_src(self):
        src = "Yes."
        trg = "No"
        cnt = 0
        src, trg, cnt = join_single_file._process_dot(src, trg, cnt)

        self.assertEquals(1, cnt)
        self.assertEquals("Yes.", src)
        self.assertEquals("No.", trg)

    def test_process_dot_tgt(self):
        src = "Yes"
        trg = "No."
        cnt = 0
        src, trg, cnt = join_single_file._process_dot(src, trg, cnt)

        self.assertEquals(1, cnt)
        self.assertEquals("Yes.", src)
        self.assertEquals("No.", trg)

    def test__has_dot_or_equivalent_true(self):
        self.assertTrue(join_single_file._has_dot_or_equivalent("Hola."))
        self.assertTrue(join_single_file._has_dot_or_equivalent("Hola?"))
        self.assertTrue(join_single_file._has_dot_or_equivalent("Hola!"))
        self.assertTrue(join_single_file._has_dot_or_equivalent("Hola…"))

    def test__has_dot_or_equivalent_false(self):
        self.assertFalse(join_single_file._has_dot_or_equivalent("num1"))
        self.assertFalse(join_single_file._has_dot_or_equivalent("Hola"))

if __name__ == '__main__':
    unittest.main()
