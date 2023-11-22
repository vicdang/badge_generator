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
   + python name_verifier.py path/to/your/image/folder path/to/log/file.log
"""

import os
import re
import argparse
import logging

class ImageNameVerifier:
    def __init__(self, folder_path, log_file):
        self.folder_path = folder_path
        self.log_file = log_file
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('image_name_verification')
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    def verify_image_names(self):
        pattern = r'^[\w\s\u00C0-\u017F]+_(T|B)?\d{6}_(E|SE|TL|PM|SM|ASM|SME|A|SA|D|SD|VP)_[1-3]\.(png|jpg|bmp|jpeg)$'
        regex = re.compile(pattern, re.UNICODE)

        files = os.listdir(self.folder_path)

        for file in files:
            if regex.match(file):
                message = f"[PASSED] - {file}"
                print(message)
                self.logger.info(message)
            else:
                message = f"[FAILED] - {file}"
                print(message)
                self.logger.warning(message)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Verify image filenames in a folder.')
    parser.add_argument('folder_path', type=str, default="./mock_images", nargs='?', help='Path to the folder containing images')
    parser.add_argument('log_file', type=str, default="./log.log", nargs='?', help='Path to the log file')
    return parser.parse_args()

def main():
    args = parse_arguments()
    verifier = ImageNameVerifier(args.folder_path, args.log_file)
    verifier.verify_image_names()

if __name__ == "__main__":
    main()
