#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Jordi Mas i Hernandez <jmas@softcatala.org>
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
import datetime
from shutil import copyfile

'''
    This class keeps a log of the usage of a service
        - For usage write a line on the file with the date
        - At the number of days specified cleans old entries
'''
class Usage(object):

    FILE = "usage.txt"
    DAYS_TO_KEEP = 7

    def __init__(self):
        self.rotate = True

    def _get_time_now(self):
        return datetime.datetime.utcnow()

    def get_date_from_line(self, line):
         return line.split("\t", 1)[0]

    def log(self, model_name, words, time_used):
        try:
            with open(self.FILE, "a+") as file_out:
                current_time = self._get_time_now().strftime('%Y-%m-%d %H:%M:%S')
                file_out.write('{0}\t{1}\t{2}\t{3}\n'.format(current_time, model_name, words, time_used.microseconds))

            if self.rotate and self._is_old_line(self._read_first_line()):
                self._rotate_file()
        except Exception as exception:
            print("Error:" + str(exception))
            pass

    def _get_line_components(self, line):
        components = line.split("\t")
        return components[0], components[1], components[2], components[3]

    def _init_stats_dict(self, dictionary):
        dictionary["calls"] = 0
        dictionary["words"] = 0
        dictionary["time"] = 0
        return dictionary

    def get_stats(self, date_requested):
        results = {}
        try:
            with open(self.FILE, "r") as file_in:
                for line in file_in:
                    date_component, model_component, words_component, time_component = self._get_line_components(line)

                    if model_component in results:
                        stats = results[model_component]
                    else:
                        stats = {}
                        results[model_component] = self._init_stats_dict(stats)
                    
                    datetime_no_newline = date_component
                    line_datetime = datetime.datetime.strptime(datetime_no_newline, '%Y-%m-%d %H:%M:%S')
                    if line_datetime.date() == date_requested.date():
                        stats["calls"] = stats["calls"] + 1
                        stats["words"] = stats["words"] + int(words_component)
                        stats["time"] = stats["time"] + int(time_component)

        except Exception as exception:
            print("Error:" + str(exception))
            pass

        return results

    def _read_first_line(self):
        try:
            with open(self.FILE, "r") as f:
                first = f.readline()
                return first
        except IOError:
            return None

    def _is_old_line(self, line):
        if line is None:
            return False

        line = self.get_date_from_line(line)
        line_datetime = datetime.datetime.strptime(line, '%Y-%m-%d %H:%M:%S')
        return line_datetime < self._get_time_now() - datetime.timedelta(days = self.DAYS_TO_KEEP)

    def _rotate_file(self):
        TEMP = "usage.bak"
        copyfile(self.FILE, TEMP)

        with open(TEMP, "r") as temp:
            with open(self.FILE, "w") as new:
                for line in temp:
                    if self._is_old_line(line) is False:
                        new.write(line)
