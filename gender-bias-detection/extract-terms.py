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

def get_plural(word):

    last = word[-1:]
    if last == 's' or last == 'x' or last == 'z' or last == 'ss' or last == 'sh' or last == 'ch':
        return word + "es"

    if 'y' == last:
        return word[0:-1] + "ies"

    if 'child' in word:
        return 'children'

    return word + "s"


def main():

    print("Extract terms from file")

    terms = set()
    with open("en.txt") as fp: 
        while True: 
            line = fp.readline() 
      
            if not line: 
                break

            components = line.split('\t')
            n_components = len(components)
            if n_components != 4:
                continue

            term = components[3]
            if len(term.split()) > 1:
                continue

            term = term.replace("\n", "")
            terms.add(term)

    # Remove polysmeic
    with open("polysemic.txt") as fp: 
        while True: 
            line = fp.readline()
            if not line:
                break

            pos = line.find('#')
            if pos >= 0:
                line = line[:pos - 1]

            term = line.strip()
            if term in terms:
                terms.remove(term)

    counter = 0
    with open("gender-bias-terms.txt", "w+") as fp:
        for term in sorted(terms, key=str.lower):
            plural_term = get_plural(term)
            fp.write(f"{term}\n")   
            counter = counter + 1

            if plural_term:
                fp.write(f"{plural_term}\n")
                counter = counter + 1
            
    print(f"terms: {counter}")

  
if __name__ == "__main__":
    main()
