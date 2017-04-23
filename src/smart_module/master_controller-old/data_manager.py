#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
HAPI Master Controller v1.0
Author: Tyler Reed
Release: June 2016 Alpha

Copyright 2016 Maya Culpa, LLC

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import print_function

import sqlite3
import sys
import operator
import time
import datetime
import urllib2
import json

def get_weather():
    response = ""
    f = urllib2.urlopen('http://api.wunderground.com/api/ffb22aac10a07be6/geolookup/conditions/q/TN/Nashville.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    #location = parsed_json['location']['city']
    #temp_f = parsed_json['current_observation']['temp_f']
    #temp_c = parsed_json['current_observation']['temp_c']
    #rel_hmd = parsed_json['current_observation']['relative_humidity']
    #pressure = parsed_json['current_observation']['pressure_mb']
    #print('Current weather in', location)
    #print('    Temperature is: %sF, %sC' % (temp_f, temp_c))
    #print('    Relative Humidity is:', rel_hmd)
    #print('    Atmospheric Pressure is: %smb' % pressure)
    response = parsed_json['current_observation']
    f.close()
    return response

def get_raw_log():
    rtus = []
    field_names = '''
        rtuid
        protocol
        address
        version
        online
    '''.split()
    try:
        conn = sqlite3.connect('hapi.db')
        c = conn.cursor()
        query = c.execute("SELECT  FROM rtus WHERE online = 1;")
        for row in query:
            rtu = RemoteTerminalUnit()
            for field_name, field_value in zip(field_names, row):
                setattr(rtu, field_name, field_value)
            rtus.append(rtu)
            get_pin_modes(rtu)
        conn.close()
    except Exception, excpt:
        print('Error loading rtu table.', excpt)

    return rtus