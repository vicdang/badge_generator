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
+ python owncloud_connector.py -s "https://box.***.com.vn/" -u "dnnvu" -p "***" -f "//IMG Badge ID/"
"""

from owncloud import Client
import name_verifier
import logging

class OwnCloudFileLister:
    """
    A class to interact with ownCloud and list files/folders.

    Methods
    -------
    connect_to_owncloud()
        Connects to the ownCloud server.

    list_all_folders_recursive()
        Lists all folders recursively in ownCloud.

    list_folders_recursive(folder_path)
        Lists folders recursively starting from a given folder path.

    list_files_in_folder()
        Lists files in a specified folder and verifies their names.

    """

    def __init__(self, args):
        """
        Initializes the OwnCloudFileLister class.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed arguments containing server_url, username, password, folder_path, and log_file.
        """
        self.server_url = args.server_url
        self.username = args.username
        self.password = args.password
        self.folder_path = args.folder_path
        self.log_file = args.log_file

        # Initialize logger
        self.logger = self.setup_logger()

        self.client = self.connect_to_owncloud()
        self.verifier = name_verifier.ImageNameVerifier(args)

    def setup_logger(self):
        """
        Sets up logging configuration.

        Returns
        -------
        logging.Logger
            Configured logger instance.
        """
        logger = logging.getLogger('OwnCloudFileLister')
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Stream handler for terminal logging
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger

    def connect_to_owncloud(self):
        """
        Connects to the ownCloud server.

        Returns
        -------
        owncloud.Client
            Connected ownCloud client.
        """
        oc = Client(self.server_url)
        oc.login(self.username, self.password)
        self.logger.info(f"Connected to ownCloud server: {self.server_url}")
        return oc
    
    def list_all_folders_recursive(self):
        """
        Lists all folders recursively in ownCloud.
        """
        self.list_folders_recursive('/')

    def list_folders_recursive(self, folder_path):
        """
        Lists folders recursively starting from a given folder path.

        Parameters
        ----------
        folder_path : str
            Path to the folder in ownCloud.
        """
        folder_contents = self.client.list(folder_path)
        if folder_contents:
            self.logger.info(f"Folders in '{folder_path}':")
            for item in folder_contents:
                if item.is_dir():
                    self.logger.info("Dir: " + item.path)
                    self.list_folders_recursive(item.path)
                else:
                    self.logger.info("File: " + item.path)

    def list_files_in_folder(self):
        """
        Lists files in a specified folder and verifies their names.
        """
        self.logger.info(f"Files in '{self.folder_path}':")
        folder_contents = self.client.list(self.folder_path)
        if folder_contents:
            for item in folder_contents:
                if not item.is_dir():
                    f = item.path.split('/')[-1]
                    self.verifier.verify_name(f)

def parse_arguments():
    """
    Parses command line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed arguments.
    """
    import argparse
    parser = argparse.ArgumentParser(description='Connect to ownCloud and list files in a folder.')
    parser.add_argument('-s', '--server', dest='server_url', type=str, help='URL of the ownCloud server')
    parser.add_argument('-u', '--username', type=str, help='ownCloud username')
    parser.add_argument('-p', '--password', type=str, help='ownCloud password')
    parser.add_argument('-f', '--folder', dest='folder_path', type=str, help='Path to the folder in ownCloud')
    parser.add_argument('-l', '--log-file', dest='log_file', type=str, default="./log.log", nargs='?', help='Path to the log file')
    return parser.parse_args()

def main():
    """
    Main function to execute ownCloud file listing and verification.
    """
    args = parse_arguments()
    file_lister = OwnCloudFileLister(args)
    if args.folder_path:
        file_lister.list_files_in_folder()
    else:
        file_lister.list_all_folders_recursive()

if __name__ == "__main__":
    main()
