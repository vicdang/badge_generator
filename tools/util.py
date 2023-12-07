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
# Import
import os
import sys

# Add the parent directory of the current script to the Python path
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config import app_conf as conf


class Utilities:

   @staticmethod
   def check_file_type(file_path):
      if file_path.lower().endswith(('.xlsx', '.xls')):
         return "excel"
      elif file_path.lower().endswith(('.txt', '.ini')):
         return "txt"
      else:
         return "Unknown"

   @staticmethod
   def get_dict_positions():
      return conf.positions

   @staticmethod
   def get_list_file_extensions():
      return conf.file_extensions
