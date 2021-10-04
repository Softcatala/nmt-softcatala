#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Jordi Mas i Hernandez <jmas@softcatala.org>
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

from bs4 import BeautifulSoup
import requests
import os
#from urllib.request import Request, urlopen
from urllib.parse import urlparse


URL = 'https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/'
EXT = 'zip'

def get_list_of_models(url, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]

def get_language_pair(url):
    a = urlparse(url)
    filename = os.path.basename(a.path)
    return filename[0:7]

def get_filename(url):
    a = urlparse(url)
    return os.path.basename(a.path)



def main():
    print("Builds a Dockerfile with available models")

    models = get_list_of_models(URL, EXT)
    for url in models:
        
        language_pair = get_language_pair(url)
        filename = get_filename(url)

        print(f"ENV FILE {filename}")
        print(f"RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d {language_pair}/")
        print("")

if __name__ == "__main__":
    main()
