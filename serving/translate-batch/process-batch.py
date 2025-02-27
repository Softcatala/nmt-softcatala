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
from batchfilesdb import BatchFilesDB
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

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
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console.setFormatter(formatter)
    logger.addHandler(console)

def send_email(translated_file, email, attachment):
    try:
        port = 25
        sender_email = "serveis@softcatala.org"

        with smtplib.SMTP("mail.scnet", port) as server:
            message = MIMEMultipart("alternative")
            message["Subject"] = "Traducció de Softcatalà"
            message["From"] = sender_email
            message["To"] = email

            if attachment:

                with open(translated_file, mode='rb') as file:
                    translation = file.read()

                attachment_name = 'ca.po'
                part1 = MIMEText("Aquí teniu la traducció que heu demanat", "plain")
                message.attach(part1)

                part = MIMEApplication(translation, Name="ca.po")
                part['Content-Disposition'] = f'attachment; filename={attachment_name}'
                message.attach(part)

            else:
                with open(translated_file, encoding='utf-8', mode='r') as file:
                    translation = file.read()

                part1 = MIMEText(translation, "plain")
                message.attach(part1)

            server.sendmail(sender_email, email, message.as_string())
    except Exception as e:
        msg = "Error '{0}' sending to {1}".format(e, email)
        logging.error(msg)

MAX_SIZE = 8192 * 1024

def truncate_file(filename):
    f = open(filename, "a")
    f.truncate(MAX_SIZE)
    f.close()

def _is_po_file(filename):

    try:
        msgid = False
        msgstr = False
        with open(filename, "r") as read_file:
            lines = 0
            while True:

                src = read_file.readline().lower()

                if not src or lines > 50:
                    break

                if 'msgid' in src:
                    msgid = True

                if 'msgstr' in src:
                    msgstr = True

                if msgid and msgstr:
                    return True

                lines += 1

    except Exception as e:
        msg = "_is_po_file. Error '{0}'".format(e)
        logging.error(msg)

    return False


def main():

    print("Process batch files to translate")
    init_logging()
    db = BatchFilesDB()

    while True:
        batchfiles = db.select()
        for batchfile in batchfiles:
            source_file = batchfile.filename
            print(source_file)
            translated_file = source_file + "-translated.txt"

            if _is_po_file(source_file):
                command = 'model_to_po'
                attachment = True
            else:
                command = 'model_to_txt'
                truncate_file(source_file)
                attachment = False

            cmd = "{0} -f {1} -t {2} -m {3} -x {4}".format(command, source_file,
                   translated_file, batchfile.model_name, TRANSLATION_MODELS)

            logging.debug("Run {0}".format(cmd))
            os.system(cmd)
            send_email(translated_file, batchfile.email, attachment)
            db.delete(batchfile.filename_dbrecord)
            os.remove(source_file)
            os.remove(translated_file)

        time.sleep(10)


if __name__ == "__main__":
    main()
