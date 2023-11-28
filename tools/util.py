# -*- coding: utf-8 -*-
# vim:ts=3:sw=3:expandtab
"""
---------------------------
Copyright (C) 2022
@Authors: Vic Dang
@Date: 22-Mar-22
@Version: 1.0
---------------------------
"""

import json

CONF = '../config'

class Utilities():
   
    @staticmethod
    def check_file_type(file_path):
        if file_path.lower().endswith(('.xlsx', '.xls')):
            return "excel"
        elif file_path.lower().endswith(('.txt', '.ini')):
            return "txt"
        else:
            return "Unknown"
    
    @staticmethod
    def get_position_map():
        with open(CONF + "/positions.json", "r") as pos_file:
            return json.load(pos_file)