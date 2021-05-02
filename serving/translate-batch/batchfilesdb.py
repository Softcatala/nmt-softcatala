# -*- encoding: utf-8 -*-
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

import os
import uuid
import fnmatch


class BatchFile():
    def __init__(self, filename_dbrecord, filename, email, model_name):
        self.filename_dbrecord = filename_dbrecord
        self.filename = filename
        self.email = email
        self.model_name = model_name

class BatchFilesDB():

    ENTRIES = '/srv/data/entries'
    SEPARATOR = "\t"
    g_check_directory = True


    def create(self, filename, email, model_name):
        if self.g_check_directory:
            self.g_check_directory = False
            if not os.path.exists(self.ENTRIES):
                os.makedirs(self.ENTRIES)

        filename_dbrecord = str(uuid.uuid4())
        filename_dbrecord = os.path.join(self.ENTRIES, filename_dbrecord)

        with open(filename_dbrecord, "w") as fh:
            line = f"{filename}{self.SEPARATOR}{email}{self.SEPARATOR}{model_name}"
            fh.write(line)

        return filename_dbrecord

    def _find(self, directory, pattern):
        filelist = []

        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    filelist.append(filename)

        return filelist

    def _read_record(self, filename_dbrecord):
        with open(filename_dbrecord, "r") as fh:
            line = fh.readline()
            components = line.split(self.SEPARATOR)
            return BatchFile(filename_dbrecord, components[0], components[1], components[2])

    def select(self):
        filenames = self._find(self.ENTRIES, "*")
        records = []
        for filename in filenames:
            record = self._read_record(filename)
            records.append(record)

        return records

    def delete(self, filename):
        os.remove(filename)

