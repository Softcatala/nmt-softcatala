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
import os
import datetime
from batchfiles.batchfiles import *
import time
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def init_logging(del_logs):
    logfile = 'process-batch.log'

    if del_logs and os.path.isfile(logfile):
        os.remove(logfile)

    logger = logging.getLogger()

    hdlr = logging.FileHandler(logfile)
    logger.addHandler(hdlr)
    logger.setLevel(logging.WARNING)

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
        print(msg)
        logging.error(msg)

def main():

    init_logging(True)    
    print("Process batch files to translate")
    database.open()

    while True:
        print("Starting to process")
        batchfiles = BatchFile.select().where(BatchFile.done == 0)
        for batchfile in batchfiles:
            print(batchfile.filename)
            translated_file = batchfile.filename + "-ca.txt"
            cmd = "python3 model-to-txt.py -f {0} -t {1} {2}".format(batchfile.filename,
                   translated_file, batchfile.model)
            logging.debug("Run {0}".format(cmd))
            os.system(cmd)
            send_email(translated_file, batchfile.email)
            batchfile.done = True
            batchfile.save()

        time.sleep(10)


if __name__ == "__main__":
    main()
