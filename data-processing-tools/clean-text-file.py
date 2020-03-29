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

    
def clean_string(text):
    text = re.sub('[_&~]', '', text)
    text = re.sub('<[^>]*>', '', text) # Remove HTML tags
    return text

def main():

    print("Open text file and discard all the English sentence with non valid chars")

    in_file = 'twitts.raw'
    out_file = 'twitts.en'
    
    with open(in_file, 'r') as fh_input:
        lines = fh_input.read().splitlines()

    strings = 0
    with open(out_file, 'w') as fh_output:
        for line in lines:
            valid = True
            for c in line:
                if c.isalpha():
                    continue

                if c.isspace():
                    continue

                if c == ',' or c == '.' or c == '?' or c == ':':
                    continue

                valid = False

            if valid is False:
                print(line)
                continue
            
            fh_output.write("{0}\n".format(line))
            strings = strings + 1

            #if strings >= 2000:
            #    break

    print("Wrote {0} strings".format(strings))
        

if __name__ == "__main__":
    main()
