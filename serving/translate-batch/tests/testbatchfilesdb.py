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

from batchfilesdb import BatchFilesDB
import unittest
import os
import tempfile
import sys

class TestBatchFilesDB(unittest.TestCase):

    FILENAME = "fitxer.txt"
    EMAIL = "jmas@softcatala.org"
    MODEL_NAME = "eng-cat"

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.ENTRIES = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def _create_db_object(self):
        db = BatchFilesDB()
        db.ENTRIES = self.ENTRIES
        return db    

    def test_create(self):
        db = self._create_db_object()
        filename_dbrecord = db.create(self.FILENAME, self.EMAIL, self.MODEL_NAME)

        record = db._read_record(filename_dbrecord)
        self.assertEquals(self.FILENAME, record.filename)
        self.assertEquals(self.EMAIL, record.email)
        self.assertEquals(self.MODEL_NAME, record.model_name)

    def test_select(self):
        db = self._create_db_object()
        db.create(self.FILENAME, self.EMAIL, self.MODEL_NAME)

        records = db.select()
        self.assertEquals(1, len(records))

        record = records[0]
        self.assertEquals(self.FILENAME, record.filename)
        self.assertEquals(self.EMAIL, record.email)
        self.assertEquals(self.MODEL_NAME, record.model_name)

    def test_delete(self):
        db = self._create_db_object()
        filename_dbrecord = db.create(self.FILENAME, self.EMAIL, self.MODEL_NAME)

        records_org = db.select()
        db.delete(filename_dbrecord)

        records = len(records_org) - len(db.select())
        self.assertEquals(1, records)

if __name__ == '__main__':
    unittest.main()
