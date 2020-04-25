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

def init_logging(del_logs):
    logfile = 'process-batch.log'

    if del_logs and os.path.isfile(logfile):
        os.remove(logfile)

    logger = logging.getLogger()

    hdlr = logging.FileHandler(logfile)
    logger.addHandler(hdlr)
    logger.setLevel(logging.WARNING)

def send_email():
    print("Send email start")
    port = 465  # For SSL
    context = ssl.create_default_context()
    
    sender_email = "jmas@softcatala.org"
    receiver_email = "jordimash2@gmail.com"

    with smtplib.SMTP_SSL("mail.scnet", port, context=context) as server:
        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = sender_email
        message["To"] = receiver_email
        text = "Prova al fitxer"
        part1 = MIMEText(text, "plain")
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Send email end")

def main():

    init_logging(True)    
    print("Process batch files to translate")
    database.open()

    while True:
        print("Starting to process")
        batchfiles = BatchFile.select().where(BatchFile.done == 1)
        for batchfile in batchfiles:
            print(batchfile.filename)
            cmd = "python3 model-to-txt.py -f {0} -t {1} {2}".format(batchfile.filename, 
                  str(batchfile.filename) + "-ca.txt", batchfile.model)
            logging.debug("Run {0}".format(cmd))
            os.system(cmd)
            send_email()
#            batchfile.done = True
            batchfile.update()

        time.sleep(10*1000)





if __name__ == "__main__":
    main()
