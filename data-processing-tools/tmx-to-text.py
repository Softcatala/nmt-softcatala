#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Jordi Mas i Hernandez <jmas@softcatala.org>
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

import xml.etree.ElementTree as ET

class ConvertTmx():

    def __init__(self, input_file, en_filename, ca_filename):
        self.input_file = input_file
        self.en_filename = en_filename
        self.ca_filename = ca_filename

    def convert(self):
        tree = ET.parse(self.input_file)
        root = tree.getroot()
        sources = set()

        entries = 0

        tf_en = open(self.en_filename, 'w')
        tf_ca = open(self.ca_filename, 'w')

        for tu_entry in root.iter('tu'):

            entry_id = None
            if 'tuid' in tu_entry.attrib:
                if len(tu_entry.attrib['tuid']):
                    entry_id = 'id: {0}'.format(tu_entry.attrib['tuid'])

            source = ''
            translation = ''
            for tuv_entry in tu_entry:
                if tuv_entry.tag != 'tuv':
                    continue

                if '{http://www.w3.org/XML/1998/namespace}lang' in tuv_entry.attrib:
                    llengua = tuv_entry.attrib['{http://www.w3.org/XML/1998/namespace}lang'].lower()
                else:
                    llengua = tuv_entry.attrib['lang'].lower()

                for seg_entry in tuv_entry.iter('seg'):
                    if llengua == 'en' or llengua == 'en-us':
                        source = seg_entry.text
                    elif llengua == 'ca':
                        translation = seg_entry.text

            if source is None or source is '':
                continue

            if translation is None or translation is '':
                continue

            if source in sources:
                msgctxt = str(entries)
            else:
                msgctxt = None
                sources.add(source)

            tf_en.write(source + "\n")
            tf_ca.write(translation + "\n")

            entries = entries + 1

            #if entries >= 2000:
            #    break

        tf_en.close()
        tf_ca.close()
        print("Wrote {0} strings".format(entries))

def main():

    print("Converts  into Text")
    print("and cleans the strings")

    txt_file = 'raw/GlobalVoices-ca-en.tmx'
    txt_en_file = 'input/globalvoices-en.txt'
    txt_ca_file = 'input/globalvoices-ca.txt'

    convert = ConvertTmx(txt_file, txt_en_file, txt_ca_file)
    convert.convert()

if __name__ == "__main__":
    main()
