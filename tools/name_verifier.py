# -*- coding: utf-8 -*-
# vim:ts=3:sw=3:expandtab
"""
---------------------------
Copyright (C) 2021
@Authors: Vic Dang
@Skype: traxanh_dl
@Date: 16-Dec-21
@Version: 1.0
---------------------------
Usage example:
    export PYTHONIOENCODING=utf-8
    + python name_verifier.py path/to/your/image/folder path/to/log/file.log
"""

import argparse
import logging
import os
import re
from util import Utilities as uT


class ImageNameVerifier:
   """
   A class to verify image filenames.

   Methods
   -------
   setup_logger()
       Sets up the logger for logging verification results.

   verify_names(names)
       Verifies a list of image names.

   verify_name(name)
       Verifies an individual image name.

   verify_image_names()
       Verifies image filenames in a folder.
   """

   def __init__(self, args):
      """
      Initializes the ImageNameVerifier class.

      Parameters
      ----------
      args : argparse.Namespace
          Parsed arguments containing folder_path and log_file.
      """
      self.folder_path = args.folder_path
      self.log_file = args.log_file
      self.position_map = "|".join(list(uT.get_dict_positions()))
      self.file_extensions = "|".join(list(uT.get_list_file_extensions()))
      self.pattern = r'^[^\s_]+ [\w\s\u00C0-\u017F]+_(T|B)?\d{6}_'\
                     r'(' + self.position_map + ')_[1-3]\.' \
                     r'(' + self.file_extensions + ')$'
      self.regex = re.compile(self.pattern, re.UNICODE | re.IGNORECASE)
      self.logger = self.setup_logger()

   def setup_logger(self):
      """
      Sets up logging configuration.

      Returns
      -------
      logging.Logger
          Configured logger instance.
      """
      logger = logging.getLogger('image_name_verification')
      logger.setLevel(logging.INFO)

      formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

      # File handler
      file_handler = logging.FileHandler(self.log_file,
                                         encoding='utf-8')  # Specify encoding
      file_handler.setLevel(logging.INFO)
      file_handler.setFormatter(formatter)
      logger.addHandler(file_handler)

      # Stream handler for terminal logging
      stream_handler = logging.StreamHandler()
      stream_handler.setLevel(logging.INFO)
      stream_handler.setFormatter(formatter)
      logger.addHandler(stream_handler)

      return logger

   def verify_names(self, names):
      """
      Verifies a list of image names.

      Parameters
      ----------
      names : list
          List of image filenames.
      """
      for name in names:
         self.verify_name(name)

   def verify_name(self, name, counter=1):
      """
      Verifies an individual image name.

      Parameters
      ----------
      name : str
          Image filename to be verified.
          @param name:
          @param counter:
      """
      if self.regex.match(name):
         message = f"{counter:4} [ _ ] {name}"
         self.logger.info(message)
      else:
         message = f"{counter:4} [ X ] {name}"
         self.logger.info(message)

   def verify_image_names(self):
      """
      Verifies image filenames in a folder.
      """
      files = os.listdir(self.folder_path)

      for file in files:
         if self.regex.match(file):
            message = f"[ _ ] {file}"
            self.logger.info(message)
         else:
            message = f"[ X ] {file}"
            self.logger.info(message)


def parse_arguments():
   """
   Parses command line arguments.

   Returns
   -------
   argparse.Namespace
       Parsed arguments.
   """
   parser = argparse.ArgumentParser(
      description='Verify image filenames in a folder.')
   parser.add_argument('-f', '--folder-path', dest='folder_path', type=str,
                       default="./mock_images", nargs='?',
                       help='Path to the folder containing images')
   parser.add_argument('-l', '--log-file', dest='log_file', type=str,
                       default="./log.log", nargs='?',
                       help='Path to the log file')
   return parser.parse_args()


def main():
   """
   Main function to execute verification of image filenames.
   """
   args = parse_arguments()
   verifier = ImageNameVerifier(args)
   verifier.verify_image_names()


if __name__ == "__main__":
   main()
