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
from optparse import OptionParser
from opennmt import OpenNMT
import pyonmttok
from batchfiles.batchfiles import *


def init_logging(del_logs):
    logfile = 'process-batch.log'

    if del_logs and os.path.isfile(logfile):
        os.remove(logfile)

    import logging
    logger = logging.getLogger()

    hdlr = logging.FileHandler(logfile)
    logger.addHandler(hdlr)
    logger.setLevel(logging.WARNING)

def main():

    init_logging(True)    
    print("Process batch files to translaate")
    database.open()
    batchfiles = BatchFile.select()

    for batchfile in batchfiles:
        print(batchfile.filename)
        cmd("")
        os.system(cmd)




if __name__ == "__main__":
    main()
