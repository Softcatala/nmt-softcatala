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
from flask_cors import CORS
import json
import datetime
from nmt_sc.ctranslate import CTranslate
from usage import Usage
from batchfilesdb import BatchFilesDB
import os
import uuid
import logging
import logging.handlers
import psutil
from genderbiasdetection import GenderBiasDetectionFactory

app = Flask(__name__)
CORS(app)

MODELS = '/srv/models/'
UPLOAD_FOLDER = '/srv/data/files/'
SAVED_TEXTS = '/srv/data/saved/'
openNMTs = {}

LANGUAGE_ALIASES = {
    "eng-cat": ["en|cat", "en|ca", "eng|ca", "eng|cat"],
    "cat-eng": ["cat|en", "ca|en", "ca|eng", "cat|eng"],
    "deu-cat": ["de|cat", "de|ca", "deu|ca", "deu|cat"],
    "cat-deu": ["cat|de", "ca|de", "ca|deu", "cat|deu"],
    "fra-cat": ["fr|cat", "fr|ca", "fra|ca", "fra|cat"],
    "cat-fra": ["cat|fr", "ca|fr", "ca|fra", "cat|fra"],
    "por-cat": ["pt|cat", "pt|ca", "por|ca", "por|cat"],
    "cat-por": ["cat|pt", "ca|pt", "ca|por", "cat|por"],
}

translate_calls = 0
total_seconds = 0
translate_chars = 0
total_words = 0

def load_models():
    model_directories = next(os.walk(MODELS))[1]
    for model_dir in model_directories:
        print(f"Model dir: {model_dir}")
        openNMT = CTranslate(f"{MODELS}", model_dir)
        openNMTs[model_dir] = openNMT

    print(f"{len(openNMTs)} models loaded")


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
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console.setFormatter(formatter)
    logger.addHandler(console)


@app.route('/translate', methods=['GET'])
def apertium_translate_get():
    return apertium_translate_process(request.args)

@app.route('/health', methods=['GET'])
def health_get():
    health = {}
    rss = psutil.Process(os.getpid()).memory_info().rss // 1024 ** 2
    health['id'] = os.getpid()
    health['rss'] = f"{rss} MB"
    health['average_time_per_request'] = total_seconds / translate_calls if translate_calls else 0
    health['translate_calls'] = translate_calls
    health['words_per_second'] = total_words / total_seconds if total_seconds else 0
    health['average_chars'] = translate_chars // translate_calls if translate_calls else 0
    return health

# This should become /translate once front calls the right API endpoint
@app.route('/translate/', methods=['POST'])
def translate_api():
    return apertium_translate_process(request.form)

def _convert_apertium_languages_aliases_to_iso639_3(langpair):
    languages = langpair.replace("|", "-")
    for key, value in LANGUAGE_ALIASES.items():
        if langpair in value:
            return key

    return languages

def get_language_name(language):
    translations = {
        "eng": "anglès",
        "eus": "basc",
    }
    return translations.get(language, f"'{language}'")

def _get_bias_message_if_needed(languages, text, result):
    try:
        bias_detector = GenderBiasDetectionFactory.get(languages=languages)
        if bias_detector:
            bias_words = bias_detector.get_words(text)
            if len(bias_words) > 0:
                source_language = languages[0:3]
                language_name = get_language_name(source_language)
                words = ', '.join(bias_words)
                msg = f'Atenció: tingueu present que el text original en {language_name} conté substantius que poden designar '
                msg += f'persones sense marca de gènere, com ara «{words}». Adapteu-ne la traducció si és necessari.'
                result['message'] = msg
    except Exception as e:
        logging.error(f"_get_bias_message_if_needed. Error: {e}")

    return result

def apertium_translate_process(values):
    global translate_calls, translate_chars, total_seconds, total_words

    translate_calls += 1
    start_time = datetime.datetime.now()

    text = None
    text = values['q']
    langpair = values['langpair']
    savetext = 'savetext' in values and values['savetext'] == True

    languages = _convert_apertium_languages_aliases_to_iso639_3(langpair)

    if savetext:
        saved_filename = os.path.join(SAVED_TEXTS, "source.txt")
        with open(saved_filename, "a") as text_file:
            t = text.replace('\n', '')
            text_file.write(f'{languages}\t{t}\n')

    if languages not in openNMTs:
        result = {}
        result['status'] = "error"
        result['code'] = 400
        result['message'] = "Bad Request"
        result['explanation'] = "No podem traduir en aquest parell de llengües"
        return json_answer(result, 400)
    
    openNMT = openNMTs[languages]
    translated = openNMT.translate_parallel(text)

    result = {}
    result = _get_bias_message_if_needed(languages, text, result)

    time_used = datetime.datetime.now() - start_time
    words = len(text.split(' '))
    usage = Usage()
    usage.log(languages, words, time_used, 'form')

    total_seconds += (time_used).total_seconds()
    total_words += words
    translate_chars += len(text)

    logging.debug(f"/translate - time {time_used} - langpair: {langpair} - words: {words}")
    responseData = {}
    responseData['translatedText'] = translated
    result['responseStatus'] = 200
    result['responseData'] = responseData
    result['time'] = str(time_used)
    return json_answer(result)

@app.route('/savedtexts/', methods=['GET'])
def savedtexts():
    saved_filename = os.path.join(SAVED_TEXTS, "source.txt")
    with open(saved_filename, "r") as text_file:
        return Response(text_file.read(), mimetype='text/plain')

@app.route('/stats/', methods=['GET'])
def stats():
    try:
        requested = request.args.get('date')
        date_requested = datetime.datetime.strptime(requested, '%Y-%m-%d')
    except Exception as e:
        return json_answer({}, 400)

    usage = Usage()
    result = usage.get_stats(date_requested)

    return json_answer(result)


@app.route('/version/', methods=['GET'])
def version_api():

    result = {}

    for model in openNMTs.values():
        result[model.get_model_name()] = model.get_model_description()

    return json_answer(result)

def _allowed_file(filename):
    ALLOWED_EXTENSIONS = ['txt', 'po']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file_to_process(filename, email, model_name):
    db = BatchFilesDB()
    db.create(filename, email, model_name)

@app.route('/translate_file/', methods=['POST'])
def upload_file():
    file = request.files['file'] if 'file' in request.files else ""
    email = request.values['email'] if 'email' in request.values else ""
    model_name = request.values['model_name']
    
    if model_name not in openNMTs:
        result = {}
        result['status'] = "error"
        result['code'] = 400
        result['message'] = "Bad Request"
        result['explanation'] = "No podem traduir en aquest parell de llengües"
        return json_answer(result, 400)

    if file == "" or file.filename == "":
        result = {}
        result['status'] = "error"
        result['code'] = 400
        result['message'] = "Bad Request"
        result['explanation'] = "No s'ha especificat el fitxer"
        return json_answer(result, 400)

    if email == "":
        result = {}
        result['status'] = "error"
        result['code'] = 400
        result['message'] = "Bad Request"
        result['explanation'] = "No s'ha especificat el correu"
        return json_answer(result, 400)

    if file and _allowed_file(file.filename):
        filename = uuid.uuid4().hex
        fullname = os.path.join(UPLOAD_FOLDER, filename)
        file.save(fullname)

        save_file_to_process(fullname, email, model_name)
        logging.debug("Saved file {0}".format(fullname))
        result = []
        usage = Usage()
        usage.log(model_name, 0, datetime.timedelta(), 'file')
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

    for pair in openNMTs.keys():
        src, trg = pair.split("-")

        pair = { "sourceLanguage": src,
                 "targetLanguage": trg}
        responseData.append(pair)

    result['responseStatus'] = 200
    result['responseData'] = responseData
    return json_answer(result)


if __name__ == '__main__':
#    app.debug = True
    init_logging()
    load_models()
    app.run()

if __name__ != '__main__':
    load_models()
    init_logging()
