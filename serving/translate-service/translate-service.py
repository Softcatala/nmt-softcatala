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
from flask import Flask, request, Response, flash, redirect, url_for
from flask_cors import CORS, cross_origin
import json
import datetime
from opennmt import OpenNMT
import pyonmttok
from threading import Thread
from texttokenizer import TextTokenizer
from usage import Usage
from werkzeug.utils import secure_filename
from batchfiles.batchfiles import *
import os
import uuid

app = Flask(__name__)
CORS(app)

openNMT_engcat = OpenNMT()
openNMT_engcat.tokenizer_source = pyonmttok.Tokenizer(mode="none", sp_model_path="en_m.model")
openNMT_engcat.tokenizer_target = pyonmttok.Tokenizer(mode="none", sp_model_path="ca_m.model")

openNMT_cateng = OpenNMT()
openNMT_cateng.tokenizer_source = pyonmttok.Tokenizer(mode="none", sp_model_path="ca_m.model")
openNMT_cateng.tokenizer_target = pyonmttok.Tokenizer(mode="none", sp_model_path="en_m.model")


def translate_thread(sentence, openNMT, i, model_name, results):
    if sentence.strip() == '':
        results[i] = ''
    else:
        results[i] = openNMT.translate(model_name, sentence)
#    print("{0} - {1} -> {2}".format(i, sentence, results[i]))

def _launch_translate_threads(openNMT, model_name, text, sentences, translate):
    num_sentences = len(sentences)
    num_threads = 0
    for i in range(0, len(sentences)):
#        print("Sentence: '{0}': {1}".format(sentences[i], translate[i]))
        if translate[i] is False:
            continue
       
        num_threads = num_threads + 1

    threads = []
    results = ["" for x in range(num_sentences)]
    for i in range(num_sentences):
        if translate[i] is False:
            continue
        
        process = Thread(target=translate_thread, args=[sentences[i], openNMT, i, model_name, results])
        process.start()
        threads.append(process)

    for process in threads:
        process.join()

    return num_sentences, results

#    print("All threads processed")


@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@app.route('/translate/', methods=['POST'])
def translate_api():
    start_time = datetime.datetime.now()
    text = request.json['text']
    languages = request.json['languages']

    if languages == 'eng-cat':
        model_name = 'eng-cat'
        openNMT = openNMT_engcat
    else:
        model_name = 'cat-eng'
        openNMT = openNMT_cateng

#    print("Input:" + text)
    tokenizer = TextTokenizer()
    sentences, translate = tokenizer.tokenize(text)

    num_sentences, results = _launch_translate_threads(openNMT, model_name, text, sentences, translate)

    translated = ''
    for i in range(0, num_sentences):
        if translate[i] is True:
            translated += results[i] + " "
        else:
            translated += sentences[i]

#    print("Translated:" + str(translated))
    time_used = datetime.datetime.now() - start_time
    words = len(text.split(' '))
    usage = Usage()
    usage.log(model_name, words, time_used)
    result = {}
    result['text'] = text
    result['translated'] = translated
    result['time'] = str(time_used)
    return json_answer(result)

def _get_processed_files(date):
    try:
        database.open()
        cnt = batchfiles = BatchFile.select().where(BatchFile.done ==1 and\
                (BatchFile.date.year == date.year and\
                 BatchFile.date.month == date.month and\
                 BatchFile.date.day == date.day)).count()
        database.close()
    except:
        cnt = 0

    return cnt

@app.route('/stats/', methods=['GET'])
def stats():
    requested = request.args.get('date')
    date_requested = datetime.datetime.strptime(requested, '%Y-%m-%d')
    usage = Usage()
    result = usage.get_stats(date_requested)

    cnt = _get_processed_files(date_requested)
    result["files"] = cnt
    return json_answer(result)


@app.route('/version/', methods=['GET'])
def version_api():

    with open("model-description-engcat.txt", "r") as th_description:
        lines = th_description.read().splitlines()

    with open("model-description-cateng.txt", "r") as th_description:
        lines_cat_eng = th_description.read().splitlines()

    lines += lines_cat_eng

    result = {}
    result['version'] = lines
    return json_answer(result)

def _allowed_file(filename):
    ALLOWED_EXTENSIONS = 'txt'
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


UPLOAD_FOLDER = 'files/'

def save_file_to_process(filename, email, model_name):
    database.open()    
    db_entry = BatchFile()
    db_entry.filename = filename
    db_entry.email = email
    db_entry.model = model_name
    db_entry.save()
    
    database.close()


@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@app.route('/translate_file/', methods=['POST'])
def upload_file():
    print("**Start")
    file = request.files['file']
    email = request.values['email']
    model_name = request.values['model_name']
    
    if file.filename == '':
        result = {}
        result['error'] = "No s'ha especificat el fitxer"
        return json_answer(result, 404)

    if email == '':
        result = {}
        result['error'] = "No s'ha especificat el correu"
        return json_answer(result, 404)

    if file and _allowed_file(file.filename):
        filename = uuid.uuid4().hex;
        fullname = os.path.join(UPLOAD_FOLDER, filename)
        file.save(fullname)

        save_file_to_process(fullname, email, model_name)
        print("Saved file {0}".format(fullname))
        result = []
        return json_answer(result)

    result['error'] = "Error desconegut"
    return json_answer(result, 500)


def json_answer(data, status = 200):
    json_data = json.dumps(data, indent=4, separators=(',', ': '))
    resp = Response(json_data, mimetype='application/json', status = status)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.debug = True
    app.run()
