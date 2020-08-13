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
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from __future__ import print_function
import logging
import logging.handlers
import os
import datetime
from batchfiles import *
import time
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

TOKENIZER_MODELS = '/srv/models/tokenizer/'
TRANSLATION_MODELS = '/srv/models/'

def init_logging():

    logfile = 'process-batch.log'

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

def send_email(translated_file, email):
    try:
        port = 25
        sender_email = "info@softcatala.org"

        with open(translated_file, encoding='utf-8', mode='r') as file:
            translation = file.read()

        with smtplib.SMTP("mail.scnet", port) as server:
            message = MIMEMultipart("alternative")
            message["Subject"] = "Traducció de Softcatalà"
            message["From"] = sender_email
            message["To"] = email
            part1 = MIMEText(translation, "plain")
            message.attach(part1)
            server.sendmail(sender_email, email, message.as_string())
    except Exception as e:
        msg = "Error '{0}' sending to {1}".format(e, email)
        logging.error(msg)

MAX_SIZE = 256 * 1024

def truncate_file(filename):
    f = open(filename, "a")
    f.truncate(MAX_SIZE)
    f.close()

def main():

    print("Process batch files to translate")
    init_logging()
    database.open()

    while True:
        batchfiles = BatchFile.select().where(BatchFile.done == 0)
        for batchfile in batchfiles:
            source_file = batchfile.filename
            print(source_file)
            translated_file = source_file + "-translated.txt"
            truncate_file(source_file)
            cmd = "python3 model-to-txt.py -f {0} -t {1} -m {2} -p {3} -x {4}".format(source_file,
                   translated_file, batchfile.model, TOKENIZER_MODELS, TRANSLATION_MODELS)
            logging.debug("Run {0}".format(cmd))
            os.system(cmd)
            send_email(translated_file, batchfile.email)
            batchfile.done = True
            batchfile.save()

            os.remove(source_file)
            os.remove(translated_file)

        time.sleep(10)


if __name__ == "__main__":
    main()
