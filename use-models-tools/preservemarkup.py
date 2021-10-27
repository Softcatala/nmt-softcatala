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

import re

class PreserveMarkup():

    TAG = "{87719"
    HTML_REGEX = re.compile(r"\<(.*?)\>", re.VERBOSE)

    def _get_marker(self, pos):
        return self.TAG + str(pos)


    def create_markers_in_string(self, text):
        markers = {}
        matches = self.HTML_REGEX.findall(text)
        pos = 0
        new_text = text

        for match in matches:
            match = '<' + match + '>'
            where = text.find(match)
            marker = self._get_marker(pos)

            end_pos = where + len(match)
            if end_pos < len(text):
                inspect = end_pos
                #print(f"{inspect} '{text[inspect]}' A - {text} {end_pos} - {len(text)}")
                if text[inspect] != ' ':
                    marker = marker + ' '

            if where > 0:
                inspect = where - 1
                #print(f"{inspect} '{text[inspect]}' '{match}' B - {text}")
                if text[inspect] != ' ':
                    marker = ' ' + marker

            #print(f"Replacing start '{match}' for '{marker}'")  
            new_text = new_text.replace(match, marker, 1)
            markers[marker] = match
            pos = pos + 1

        return markers, new_text

    def get_back_markup(self, translated, markers):
        for marker in markers.keys():
            markup = markers[marker]
      
            translated = translated.replace(marker, markup, 1)
            # In case translate ate the spaces
            translated = translated.replace(marker.strip(), markup, 1)

        return translated

