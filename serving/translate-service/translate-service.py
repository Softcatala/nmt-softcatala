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
from flask_cors import CORS, cross_origin
import json
import datetime
from ctranslate import CTranslate
import pyonmttok
from texttokenizer import TextTokenizer
from usage import Usage
from batchfiles import *
import os
import uuid
import logging
import logging.handlers
from genderbiasdetection import GenderBiasDetection

app = Flask(__name__)
CORS(app)

MODELS = '/srv/models/'
#MODELS = '../../models/' # local
UPLOAD_FOLDER = '/srv/data/files/'
SAVED_TEXTS = '/srv/data/saved/'

openNMT_engcat = CTranslate(f"{MODELS}", "eng-cat")
openNMT_cateng = CTranslate(f"{MODELS}", "cat-eng")
openNMT_deucat = CTranslate(f"{MODELS}", "deu-cat")
openNMT_catdeu = CTranslate(f"{MODELS}", "cat-deu")

def init_logging():
    logfile = 'translate-service.log'

    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    logger = logging.getLogger()
    hdlr = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024*1024, backupCount=1)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(LOGLEVEL)

    console = logging.StreamHandler()
    console.setLevel(LOGLEVEL)
    logger.addHandler(console)


@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@app.route('/translate', methods=['GET'])
def apertium_translate_get():
    return apertium_translate_process(request.args)

# This should become /translate once front calls the right API endpoint
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@app.route('/translate/', methods=['POST'])
def translate_api():
    return apertium_translate_process(request.form)

def apertium_translate_process(values):
    start_time = datetime.datetime.now()

    text = None
    languages = None

    text = values['q']
    langpair = values['langpair']
    savetext = 'savetext' in values and values['savetext'] == True

    if langpair in ['en|cat', 'en|ca', 'eng|ca', 'eng|cat']:
        languages = 'eng-cat'
    elif langpair in ['de|cat', 'de|ca', 'deu|ca', 'deu|cat']:
        languages = 'deu-cat'
    elif langpair in ['cat|de', 'ca|de', 'ca|deu', 'cat|deu']:
        languages = 'cat-deu'
    else:
        languages = 'cat-eng'

    if savetext:
        saved_filename = os.path.join(SAVED_TEXTS, "source.txt")
        with open(saved_filename, "a") as text_file:
            t = text.replace('\n', '')
            text_file.write(f'{languages}\t{t}\n')

    translated = translate(languages, text)

    check_bias = languages == 'eng-cat'
    result = {}

    time_used = datetime.datetime.now() - start_time
    words = len(text.split(' '))
    usage = Usage()
    usage.log(languages, words, time_used)

    if check_bias:
        bias = GenderBiasDetection(text)
        if bias.has_bias():
            words = ', '.join(bias.get_words())
            msg = f'Atenció: tingueu present que el text original en anglès conté professions sense marca de gènere, '
            msg += f'com ara «{words}». Adapteu-ne la traducció si és necessari.'
            result['message'] = msg

    responseData = {}
    responseData['translatedText'] = translated
    result['responseStatus'] = 200
    result['responseData'] = responseData
    result['time'] = str(time_used)
    return json_answer(result)



def translate(languages, text):

    if languages == 'eng-cat':
        openNMT = openNMT_engcat
    elif languages == 'deu-cat':
        openNMT = openNMT_deucat
    elif languages == 'cat-deu':
        openNMT = openNMT_catdeu
    else:
        openNMT = openNMT_cateng

    return openNMT.translate_parallel(text)
    

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


@app.route('/savedtexts/', methods=['GET'])
def savedtexts():
    saved_filename = os.path.join(SAVED_TEXTS, "source.txt")
    with open(saved_filename, "r") as text_file:
        return Response(text_file.read(), mimetype='text/plain')

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

    models = [openNMT_engcat, openNMT_cateng, openNMT_deucat]

    result = {}

    for model in models:
        result[model.get_model_name()] = model.get_model_description()

    return json_answer(result)

def _allowed_file(filename):
    ALLOWED_EXTENSIONS = ['txt', 'po']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

    result = {}
    result['error'] = "Error desconegut"
    return json_answer(result, 500)


def json_answer(data, status = 200):
    json_data = json.dumps(data, indent=4, separators=(',', ': '))
    resp = Response(json_data, mimetype='application/json', status = status)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/listLanguageNames', methods=['GET'])
def list_language_names():
    languages = request.args.get('languages')
    languages = languages.split()

    result = {}
    for language in languages:
        if language == 'cat':
            result['cat'] = 'Catalan'
        elif language == 'eng':
            result['eng'] = 'English'

    return json_answer(result, 200)

@app.route('/listPairs', methods=['GET'])
def list_pairs():

    result = {}
    responseData = []

    pair = { "sourceLanguage": "eng",
             "targetLanguage": "cat"}
    responseData.append(pair)

    pair = { "sourceLanguage": "cat",
             "targetLanguage": "eng"}
    responseData.append(pair)

    result['responseStatus'] = 200
    result['responseData'] = responseData
    return json_answer(result)


if __name__ == '__main__':
#    app.debug = True
    init_logging()
    app.run()

if __name__ != '__main__':
    init_logging()
