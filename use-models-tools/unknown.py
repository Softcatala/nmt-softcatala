#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
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

class Unknown():

    def __init__(self):
        self.UNKNOWN = "<unk>"

    def _get_highest_attention_position(self, attention_word):
        highest = 0
        pos = 0
        for i in range(len(attention_word)):
            attention = attention_word[i]
            if attention > highest:
                highest = attention
                pos = i

        return pos

    def _replace_unknown_with_source(self, source, pos, target, unk_pos):
        token_from_source = source[0][pos]
        target[unk_pos] = token_from_source

    def replace_with_source(self, batch_input, results):
        translated = results[0][0]['tokens']
        for unk_pos in range(len(translated)):
            if translated[unk_pos] != self.UNKNOWN:
                continue

#            print(f"Input {batch_input}\noriginal {translated}")
            attention_word = results[0][0]['attention'][unk_pos]
            pos = self._get_highest_attention_position(attention_word)
            self._replace_unknown_with_source(batch_input, pos, translated, unk_pos)
#            print(f"changed:{translated}\n\n")

        return translated
