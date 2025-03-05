#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2025 Jordi Mas i Hernandez <jmas@softcatala.org>
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

import sentencepiece as spm


class SentencePieceTokenizer:

    def __init__(self, tokenizer_path):
        self.tokenizer = spm.SentencePieceProcessor(model_file=tokenizer_path)

    def tokenize(self, text: str) -> list[str]:
        return self.tokenizer.encode(text, out_type=str)

    def detokenize(self, tokenized: list[str]) -> str:
        text = self.tokenizer.decode(tokenized)
        final_text = text.replace("▁", " ").strip()
        return final_text
