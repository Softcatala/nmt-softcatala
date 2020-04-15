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
from threading import Thread

app = Flask(__name__)
openNMT_engcat = OpenNMT()
openNMT_engcat.tokenizer_source = pyonmttok.Tokenizer(mode="none", sp_model_path="en_m.model")
openNMT_engcat.tokenizer_target = pyonmttok.Tokenizer(mode="none", sp_model_path="ca_m.model")

openNMT_engcat1 = OpenNMT()
openNMT_engcat1.tokenizer_source = pyonmttok.Tokenizer(mode="none", sp_model_path="en_m.model")
openNMT_engcat1.tokenizer_target = pyonmttok.Tokenizer(mode="none", sp_model_path="ca_m.model")

openNMT_engcat2 = OpenNMT()
openNMT_engcat2.tokenizer_source = pyonmttok.Tokenizer(mode="none", sp_model_path="en_m.model")
openNMT_engcat2.tokenizer_target = pyonmttok.Tokenizer(mode="none", sp_model_path="ca_m.model")

openNMT_engcat3 = OpenNMT()
openNMT_engcat3.tokenizer_source = pyonmttok.Tokenizer(mode="none", sp_model_path="en_m.model")
openNMT_engcat3.tokenizer_target = pyonmttok.Tokenizer(mode="none", sp_model_path="ca_m.model")

openNMT_engcat4 = OpenNMT()
openNMT_engcat4.tokenizer_source = pyonmttok.Tokenizer(mode="none", sp_model_path="en_m.model")
openNMT_engcat4.tokenizer_target = pyonmttok.Tokenizer(mode="none", sp_model_path="ca_m.model")


openNMT_cateng = OpenNMT()
openNMT_cateng.tokenizer_source = pyonmttok.Tokenizer(mode="none", sp_model_path="ca_m.model")
openNMT_cateng.tokenizer_target = pyonmttok.Tokenizer(mode="none", sp_model_path="en_m.model")

@app.route('/translate2/', methods=['GET'])
def translate2_api():
    start_time = datetime.datetime.now()
    text = request.args.get('text')
    languages = request.args.get('languages')

    if languages == 'eng-cat':
        model_name = 'eng-cat'
        openNMT = openNMT_engcat
    else:
        model_name = 'cat-eng'
        openNMT = openNMT_cateng

    translated = openNMT.translate(model_name, text)
    result = {}
    result['text'] = text
    result['translated'] = translated
    result['time'] = str(datetime.datetime.now() - start_time)
    return json_answer(json.dumps(result, indent=4, separators=(',', ': ')))

def translate_thread(sentence, openNMT, i, model_name, results):
    if sentence.strip() == '':
        results[i] = ''
    else:
        results[i] = openNMT.translate(model_name, sentence)
    print("{0} - {1} -> {2}".format(i, sentence, results[i]))

@app.route('/translate/', methods=['GET'])
def translate_api():
    print("Hellou")
    start_time = datetime.datetime.now()
    text = request.args.get('text')
    languages = request.args.get('languages')

    if languages == 'eng-cat':
        model_name = 'eng-cat'
        openNMT = openNMT_engcat
    else:
        model_name = 'cat-eng'
        openNMT = openNMT_cateng

    sentences = text.split(".")
    num_threads = len(sentences)
    threads = []
    results = ["" for x in range(num_threads)]
    for i in range(num_threads):
        print('Starting thread {0}'.format(i))
        process = Thread(target=translate_thread, args=[sentences[i], openNMT, i, model_name, results])
        process.start()
        threads.append(process)

    for process in threads:
        process.join()

    print("Done")

    translated = ''
    for r in results:
        translated += r + " "

    result = {}
    result['text'] = text
    result['translated'] = translated
    result['time'] = str(datetime.datetime.now() - start_time)
    return json_answer(json.dumps(result, indent=4, separators=(',', ': ')))

@app.route('/version/', methods=['GET'])
def version_api():

    with open("model-description-engcat.txt", "r") as th_description:
        lines = th_description.read().splitlines()

    with open("model-description-cateng.txt", "r") as th_description:
        lines_cat_eng = th_description.read().splitlines()

    lines += lines_cat_eng

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
