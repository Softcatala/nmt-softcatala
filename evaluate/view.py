#!/usr/bin/env python3
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

import json
import polib
import re
import os
import fnmatch

    
def main():

    print("View different translations")

    txt_en_file = 'input/gnome-user-manual-en.txt'
    txt_ca_file = 'input/gnome-user-manual-ca.txt'
    txt_yandex_file = 'translated/gnome-user-manual-yandex-ca.txt'
    txt_apertium_file = 'translated/gnome-user-manual-apertium-ca.txt'
    txt_sc_nmt_file = '/home/jordi/sc/OpenNMT/nmt-softcatala/ApplyToPoFile/output.txt'

    strings = 0
    with open(txt_en_file, 'r') as tf_en, open(txt_ca_file, 'r') as tf_ca,\
         open(txt_apertium_file, 'r') as tf_apertium, open(txt_yandex_file, 'r') as tf_yandex,\
         open(txt_sc_nmt_file, 'r') as tf_sc_nmt:
        
        txt_en = tf_en.read().splitlines()
        txt_ca = tf_ca.read().splitlines()
        txt_apertium = tf_apertium.read().splitlines()
        txt_yandex = tf_yandex.read().splitlines()
        txt_sc_nmt = tf_sc_nmt.read().splitlines()

        for i in range (0, len(txt_en)):
            print("---")
            print(" en: {0}".format(txt_en[i]))
            print(" ca (org): {0}".format(txt_ca[i]))
            print(" ca (apertium): {0}".format(txt_apertium[i]))
            print(" ca (yandex): {0}".format(txt_yandex[i]))
            print(" ca (nmt): {0}".format(txt_sc_nmt[i]))


if __name__ == "__main__":
    main()
