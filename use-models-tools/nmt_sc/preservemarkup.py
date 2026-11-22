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
    """Replaces text the model must not translate with markers, and puts it back afterwards.

    Protected: HTML tags (each on its own, so the text between them is still translated),
    inline code (``code`` and `code`) and, when an is_unknown(char) function is given, text the
    model cannot represent: words such as my_variable or user@example.com as a whole, and any
    other run of unknown characters (e.g. €, |, >=). Unknown characters would otherwise become
    <unk>, which the model fills with an unrelated source word.
    """

    TAG = "{87719"
    SPANS_REGEX = re.compile(r"<[^>]*>|``.+?``|`[^`\n]+`")
    WORD_REGEX = re.compile(r"\S+")
    # Punctuation around a word that stays outside its marker, so the model still sees it.
    LEADING = "([\"'«“‘"
    TRAILING = ".,;:!?)]\"'»”’"

    def __init__(self, is_unknown=None, tag=None):
        self.is_unknown = is_unknown or (lambda char: False)
        self.tag = tag or self.TAG

    def _get_marker(self, pos):
        return self.tag + str(pos)

    def _protected_spans(self, text):
        spans = [m.span() for m in self.SPANS_REGEX.finditer(text)]

        # Words outside tags and code: blank those out first, keeping positions.
        blanked = list(text)
        for start, end in spans:
            blanked[start:end] = " " * (end - start)
        blanked = "".join(blanked)

        for word in self.WORD_REGEX.finditer(blanked):
            start, end = word.span()
            if not any(self.is_unknown(c) for c in text[start:end]):
                continue
            while start < end and text[start] in self.LEADING and not self.is_unknown(text[start]):
                start += 1
            while end > start and text[end - 1] in self.TRAILING and not self.is_unknown(text[end - 1]):
                end -= 1
            core = text[start:end]
            if any(c.isalnum() for c in core):
                spans.append((start, end))
                continue
            # No letters or digits (e.g. "€", ">="): protect only the unknown characters.
            pos = start
            while pos < end:
                if self.is_unknown(text[pos]):
                    run = pos
                    while run < end and self.is_unknown(text[run]):
                        run += 1
                    spans.append((pos, run))
                    pos = run
                else:
                    pos += 1

        return sorted(spans)

    def create_markers_in_string(self, text):
        markers = {}
        new_text = ""
        last = 0
        for pos, (start, end) in enumerate(self._protected_spans(text)):
            marker = self._get_marker(pos)
            if end < len(text) and text[end] != ' ':
                marker = marker + ' '
            if start > 0 and text[start - 1] != ' ':
                marker = ' ' + marker

            new_text += text[last:start] + marker
            markers[marker] = text[start:end]
            last = end

        return markers, new_text + text[last:]

    def get_back_markup(self, translated, markers):
        # Highest numbers first, so that marker 1 does not match the start of marker 10.
        for marker in reversed(list(markers.keys())):
            markup = markers[marker]

            translated = translated.replace(marker, markup, 1)
            # In case translate ate the spaces
            translated = translated.replace(marker.rstrip(), markup, 1)
            translated = translated.replace(marker.lstrip(), markup, 1)
            translated = translated.replace(marker.strip(), markup, 1)

        return translated
