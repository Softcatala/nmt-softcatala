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
from genderbiasdetection import (
    GenderBiasDetection,
    GenderBiasDetectionFactory,
    GenderBiasDetectionBasque,
)


class TestGenderBiasDetectionFactory(unittest.TestCase):

    def test_eng_cat(self):
        detector = GenderBiasDetectionFactory.get("eng-cat")
        self.assertEqual(GenderBiasDetection, type(detector))

    def test_eus_cat(self):
        detector = GenderBiasDetectionFactory.get("eus-cat")
        self.assertEqual(GenderBiasDetectionBasque, type(detector))

    def test_none(self):
        detector = GenderBiasDetectionFactory.get("xxx-xxx")
        self.assertEqual(None, detector)


class TestGenderBiasDetectionBasque(unittest.TestCase):

    def setUp(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        self.terms_file = os.path.join(dir, "eus-gender-bias-terms.tsv")
        self.regexs = os.path.join(dir, "eus-regex.tsv")

    def test_bias_false(self):
        detector = GenderBiasDetectionBasque(terms=self.terms_file, regexs=self.regexs)
        self.assertEqual(0, len(detector.get_words("Kaixo")))

    def test_bias_false(self):

        sentence = """
            Eusko Jaurlaritza osatzen duten alderdiek —EAJk eta PSE-EEk— eta EH Bilduk ez dute akordiorik lortu Gasteizko gobernuaren 2025eko aurrekontu proiektuaren inguruan. Negoziazioan murgildurik egon dira gaur arte, baina koalizio abertzaleak ez du onartu Ogasun Sailak eskainitako azken proposamena, Bingen Zupiria Segurtasun sailburuak Euskadi Irratian iragarri duenez, eta, hortaz, gobernuak bukatutzat jo du koalizioarekin egin duen negoziazio prozesua. Gobernuaren iragarpenaren ondorioa da EAJk eta PSEk euren gehiengoa baliatuko dutela Eusko Legebiltzarrean, abenduaren 20ko osoko bilkuran, aurrekontuak euren kabuz onartzeko, oposizioko taldeen babesik gabe.

            Lanbide arteko gutxieneko soldata baten sorreran eta etxebizitzarako bitarteko gehiagoren eskaeran kokatu dute negoziazioa, azken egunetan. Atzo gauean, Ogasun sailburu Noel D'Anjou bere azken eskaintza igorri zion EH Bilduri, eta bertan ez dira onartzen koalizioaren eskaera gehienak. Hau da, EH Bilduren zuzenketa gehienak baztertu egingo ditu Ogasun Sailak. Etxebizitzarako 90 milioi euroko bitartekoak eskatu ditu koalizio subiranistak, eta 16 besterik ez ditu eskaini Jaurlaritzak. Kopuru hori 100 milioira igotzeko aukera ere jasotzen du Ogasun Sailak, baina legealdi osoa kontuan hartuta, eta eskaera baldin badago. Izan ere, diru hori merkatu librera aterako diren etxebizitzak erosi eta babes ofizialeko gisa merkaturatzeko eskatu du EH Bilduk.

            Gaurko aurrekontuen Batzordean, zuzenketa horiek eta gainontzeko taldeenak onartu ala baztertuko dituzte, eta, gaurko informazio horren arabera, EH Bilduren zuzenketa gehienak ez dituzte onartuko EAJk eta PSEk. Lanbide arteko gutxieneko soldataren eskaera ere atzera bota du Ogasun Sailak, argudiatuta ez dela gobernuaren eskumenen arteko edukia.

            Madalen Iriarte Gipuzkoako Batzar Nagusietako EH Bilduren eledunak ohartarazi du «terminoak irauli» egiten ari direla, eta ezezkoa gobernuarena dela, bai eta aurrekontuen inguruko akordioa ez lortzearen «ardura» ere, eta ez EH Bildurena. «Gobernuak esan die ezetz EH Bilduren bi proposamenei». Erantsi du Jaurlaritzak negoziazioa eten egin dela iragartzeko moduak «politika zaharra» islatzen duela. Edonola ere, Iriartek ez du itxitzat jo negoziazioa eta gogoratu du EAJk eta PSEk aukera dutela gaurko batzordean EH Bilduren zuzenketak onartzeko.

            Baserritarrenganako neurriak ez dira herritarrenganakoak bezain argiak.
            """

        detector = GenderBiasDetectionBasque(terms=self.terms_file, regexs=self.regexs)
        self.assertEqual(
            [
                "sailburuak",
                "bitarteko",
                "sailburu",
                "bitartekoak",
                "ofizialeko",
                "nagusietako",
                "baserritarrenganako",
                "herritarrenganakoak",
            ],
            detector.get_words(sentence),
        )


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
        self.assertEqual(
            {"accountant", "administrator"},
            bias.get_words("You are an administrator or an accountant"),
        )


if __name__ == "__main__":
    unittest.main()
