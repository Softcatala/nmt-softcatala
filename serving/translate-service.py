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

from __future__ import print_function
from flask import Flask, request, Response
import json
import datetime
from opennmt import OpenNMT
import pyonmttok


app = Flask(__name__)
openNMT = OpenNMT()
openNMT.tokenizer_source = pyonmttok.Tokenizer(mode="none", sp_model_path="en_m.model")
openNMT.tokenizer_target = pyonmttok.Tokenizer(mode="none", sp_model_path="ca_m.model")


@app.route('/translate/', methods=['GET'])
def translate_api():
    start_time = datetime.datetime.now()
    text = request.args.get('text')

    model_name = 'eng-cat'
    translated = openNMT.translate(model_name, text)

    result = {}
    result['text'] = text
    result['translated'] = translated
    result['time'] = str(datetime.datetime.now() - start_time)
    return json_answer(json.dumps(result, indent=4, separators=(',', ': ')))

@app.route('/version/', methods=['GET'])
def version_api():

    with open("model_description.txt", "r") as th_description:
        lines = th_description.read().splitlines()

    result = {}
    result['version'] = lines
    return json_answer(json.dumps(result, indent=4, separators=(',', ': ')))


def json_answer(data):
    resp = Response(data, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.debug = True
    app.run()
