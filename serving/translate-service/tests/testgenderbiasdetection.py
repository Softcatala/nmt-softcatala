# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Jordi Mas i Hernandez <jmas@softcatala.org>
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
import os
import datetime
from genderbiasdetection import GenderBiasDetection, GenderBiasDetectionFactory, GenderBiasDetectionBasque

class TestGenderBiasDetectionFactory(unittest.TestCase):

    def test_eng_cat(self):
        detector = GenderBiasDetectionFactory.get("eng-cat")
        self.assertEquals(GenderBiasDetection, type(detector))

    def test_eus_cat(self):
        detector = GenderBiasDetectionFactory.get("eus-cat")
        self.assertEquals(GenderBiasDetectionBasque, type(detector))

    def test_none(self):
        detector = GenderBiasDetectionFactory.get("xxx-xxx")
        self.assertEquals(None, detector)

class TestGenderBiasDetection(unittest.TestCase):

    def setUp(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        self.terms_file = os.path.join(dir, "eng-terms.txt")

    def test_bias_false(self):
        detector = GenderBiasDetection(self.terms_file)
        self.assertEqual(0, len(detector.get_words("How are you today?")))

    def test_bias_true(self):
        detector = GenderBiasDetection(self.terms_file)
        self.assertEqual(1, len(detector.get_words("You are an accountant")))

    def test_bias_words(self):
        bias = GenderBiasDetection(self.terms_file)
        self.assertEqual({'accountant', 'administrator'}, bias.get_words("You are an administrator or an accountant"))

if __name__ == "__main__":
    unittest.main()
