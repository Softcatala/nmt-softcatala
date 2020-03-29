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
# but WITHOUT ANY WAR   RANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os
import urllib
from urllib.parse import urlparse
import urllib.request
import json
import time


def _translate_apertium_en_ca(text):

    # Request translation
    url = "https://www.softcatala.org/apertium/json/translate?langpair=en|ca&markUnknown=no"
    url += "&q=" + urllib.parse.quote_plus(text.encode('utf-8'))
    #print("url->" + url)

    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        translated =  data['responseData']['translatedText']
        return translated

    except Exception as e:
        print("ERROR: calling _get_translation: " + str(e))
        time.sleep(5)
        return ""

def _translate_apertium_en_ca2(english):
    with open("input.txt", "w") as text_file:
        text_file.write(english)
        text_file.close()

    cmd = "apertium eng-cat -u input.txt output.txt"
    os.system(cmd)

    with open ("output.txt", "r") as myfile:
        line_list = myfile.readlines()
        translation = ' '.join([str(elem) for elem in line_list]) 
        translation = translation.replace('\n', '')
#        print("text->" + text)
#        print("cmd->" + cmd)
#        print("translation->" + translation)
#        print("translation raw->" + str(line_list))
        return translation

def translate_text_yandex(text):

    _key = 'XXX'
    SERVER = "https://translate.yandex.net/api/v1.5/tr.json"
    language_pair = 'en-ca'
    url = "{0}/translate?lang={1}&format=plain&key={2}".format(SERVER, language_pair, _key)
    url += "&text=" + urllib.parse.quote_plus(text.encode('utf-8'))
    response = urllib.request.urlopen(url)
    r = response.read().decode("utf-8")
    data = json.loads(r)
    all_text = ''

    texts = data['text']
    for text in texts:
        all_text += text
    return all_text.rstrip()

def translate_text_google(text):

    _key = 'XXX'
    SERVER = "https://www.googleapis.com/language/translate/v2"
    language_pair = 'en-ca'
    url = "{0}/?key={1}&source=en&target=ca".format(SERVER, _key)
    url += "&q=" + urllib.parse.quote_plus(text.encode('utf-8'))
    response = urllib.request.urlopen(url)
    r = response.read().decode("utf-8")
    data = json.loads(r)
    translated = data['data']['translations'][0]
    translated = translated['translatedText']
    return translated.rstrip()


def apertium():
    print("Translating Apertium")
    txt_en_file = 'input/globalvoices-en.txt'
    txt_ca_file = 'translated/globalvoices-apertium-ca.txt'

    strings = 0
    with open(txt_en_file, 'r') as tf_en, open(txt_ca_file, 'w') as tf_ca:
        en_strings = tf_en.readlines()
    
        for string in en_strings:
            translated = _translate_apertium_en_ca(string)
            tf_ca.write("{0}\n".format(translated))
            strings = strings + 1

        if strings % 100:
            print(strings)
            time.sleep(60*5*1000)

    print("Translated {0} strings".format(strings))

def yandex():

    print("Translating Yandex")
    txt_en_file = 'input/globalvoices-en.txt'
    txt_ca_file = 'translated/globalvoices-yandex-ca.txt'

    strings = 0
    with open(txt_en_file, 'r') as tf_en, open(txt_ca_file, 'w') as tf_ca:
        en_strings = tf_en.readlines()
    
        cnt = 0
        for string in en_strings:
            cnt = cnt + 1
    
#            if cnt > 10:
#                break

            translated = translate_text_yandex(string)
            tf_ca.write("{0}\n".format(translated))
            strings = strings + 1

    print("Translated {0} strings".format(strings))

def google():

    print("Translating Google")
    txt_en_file = 'input/globalvoices-en.txt'
    txt_ca_file = 'translated/globalvoices-google-ca.txt'

    strings = 0
    with open(txt_en_file, 'r') as tf_en, open(txt_ca_file, 'w') as tf_ca:
        en_strings = tf_en.readlines()
    
        cnt = 0
        for string in en_strings:
            cnt = cnt + 1
    
#            if cnt > 30:
#                break

            try:
                translated = translate_text_google(string)
                tf_ca.write("{0}\n".format(translated))
                strings = strings + 1

            except Exception as e:
                print(e)
                print(string)

                translated = 'Error'
                tf_ca.write("{0}\n".format(translated))
                strings = strings + 1

    print("Translated {0} strings".format(strings))


def main():
#    yandex()
#    apertium()
    google()
    return

if __name__ == "__main__":
    main()
