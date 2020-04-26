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


from peewee import SqliteDatabase, Model, TextField, IntegerField, FloatField, BooleanField, DateTimeField
import os
import datetime

# http://peewee.readthedocs.org/en/unstable-2.0/peewee/cookbook.html

class BatchFilesDatabase(SqliteDatabase):

    def _create(self, database_name):
        if os.path.exists(database_name) == False:
            self.create_schema()

    def open(self, database_name = 'data/bachfiles.db3'):
        self.init(database_name)
        self._create(database_name)

    def create_schema(self):
        self.connect()
        self.create_tables([BatchFile])

    def close(self):
        self.commit()

database = BatchFilesDatabase(None, autocommit=False)


class BaseModel(Model):

    @property
    def dict(self):
        '''Returns model fields' as an array of properties'''
        properties = {}
        for k in self._data.keys():
            r = str(getattr(self, k))
            properties[k] = r
       
        return properties

    class Meta:
        database = database


class BatchFile(BaseModel):
    '''Simple denormalized model to represent a batch file to process'''

    filename = TextField(unique=False)
    email = TextField(unique=False)
    model = TextField(unique=False)
    done = BooleanField(unique=False, default=False)
    date = DateTimeField(unique=False, default=datetime.datetime.now)

    class Meta:
        db_table = 'batchfiles'
