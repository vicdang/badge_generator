# -*- coding: utf-8 -*-
"""
OwnCloud connector - list files and folders from OwnCloud server.

Copyright (C) 2021
Authors: Vic Dang
Date: 16-Dec-21
Version: 1.0

Usage example:
  python owncloud_connector.py \
    -s "https://box.company.com/" \
    -u "username" \
    -p "password" \
    -f "//IMG Badge ID/"
"""

import argparse
import logging
import logging.handlers
from typing import Optional, List

try:
    from owncloud import Client
except ImportError:
    Client = None

from .name_verifier import ImageNameVerifier


class OwnCloudConnector:
    """Connect to OwnCloud server and manage files."""

    def __init__(
        self,
        server_url: str,
        username: str,
        password: str,
        folder_path: str = "/",
        log_file: str = "./log.log"
    ) -> None:
        """
        Initialize OwnCloud connector.

        Args:
            server_url: OwnCloud server URL.
            username: OwnCloud username.
            password: OwnCloud password.
            folder_path: Folder path to list.
            log_file: Path to log file.

        Raises:
            ImportError: If owncloud package is not installed.
        """
        if Client is None:
            raise ImportError("owncloud package is required. Install with: pip install owncloud")

        self.server_url = server_url
        self.username = username
        self.password = password
        self.folder_path = folder_path
        self.log_file = log_file

        self.logger = self._setup_logger()
        self.client = self._connect()
        self.verifier = ImageNameVerifier(
            folder_path=folder_path,
            log_file=log_file
        )

    def _setup_logger(self) -> logging.Logger:
        """
        Setup logging configuration.

        Returns:
            Configured logger instance.
        """
        logger = logging.getLogger('OwnCloudConnector')
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )

        # File handler
        file_handler = logging.FileHandler(
            self.log_file,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def _connect(self) -> Client:
        """
        Connect to OwnCloud server.

        Returns:
            Connected OwnCloud client.

        Raises:
            Exception: If connection fails.
        """
        try:
            client = Client(self.server_url)
            client.login(self.username, self.password)
            self.logger.info(f"Connected to OwnCloud: {self.server_url}")
            return client
        except Exception as err:
            self.logger.error(f"Failed to connect to OwnCloud: {err}")
            raise

    def list_folders_recursive(
        self,
        folder_path: str = "/"
    ) -> None:
        """
        Recursively list folders from OwnCloud.

        Args:
            folder_path: Starting folder path.
        """
        try:
            items = self.client.list(folder_path)
            
            if not items:
                self.logger.debug(f"No items in {folder_path}")
                return
            
            for item in items:
                if item.is_dir():
                    self.logger.info(f"Dir: {item.path}")
                    self.list_folders_recursive(item.path)
                else:
                    self.logger.info(f"File: {item.path}")
                    
        except Exception as err:
            self.logger.error(f"Error listing {folder_path}: {err}")

    def list_all_folders(self) -> None:
        """List all folders recursively from root."""
        self.logger.info("Listing all folders recursively:")
        self.list_folders_recursive("/")

    def list_files_in_folder(self) -> None:
        """List and verify files in specified folder."""
        try:
            self.logger.info(f"Listing files in: {self.folder_path}")
            items = self.client.list(self.folder_path)
            
            if not items:
                self.logger.warning(f"No files found in {self.folder_path}")
                return
            
            file_count = 0
            valid_count = 0
            
            for item in items:
                if not item.is_dir():
                    filename = item.path.split('/')[-1]
                    file_count += 1
                    
                    # Verify filename
                    if self.verifier.verify_name(filename, file_count):
                        valid_count += 1
            
            self.logger.info(f"\nSummary: {valid_count}/{file_count} files are valid")
            
        except Exception as err:
            self.logger.error(f"Error listing files: {err}")

    def get_file_count(self, folder_path: Optional[str] = None) -> int:
        """
        Get count of files in folder.

        Args:
            folder_path: Folder path (default: self.folder_path).

        Returns:
            Number of files.
        """
        folder_path = folder_path or self.folder_path
        
        try:
            items = self.client.list(folder_path)
            return sum(1 for item in items if not item.is_dir())
        except Exception as err:
            self.logger.error(f"Error counting files: {err}")
            return 0


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Connect to OwnCloud server and list files.'
    )
    parser.add_argument(
        '-s', '--server',
        dest='server_url',
        type=str,
        required=True,
        help='OwnCloud server URL (e.g., https://box.company.com/)'
    )
    parser.add_argument(
        '-u', '--username',
        type=str,
        required=True,
        help='OwnCloud username'
    )
    parser.add_argument(
        '-p', '--password',
        type=str,
        required=True,
        help='OwnCloud password'
    )
    parser.add_argument(
        '-f', '--folder',
        dest='folder_path',
        type=str,
        default="/",
        help='Folder path to list (default: root)'
    )
    parser.add_argument(
        '-l', '--log-file',
        dest='log_file',
        type=str,
        default="./log.log",
        help='Path to log file'
    )
    parser.add_argument(
        '--recursive',
        action='store_true',
        help='List folders recursively'
    )

    return parser.parse_args()


def main() -> None:
    """Main execution function."""
    args = parse_arguments()
    
    try:
        connector = OwnCloudConnector(
            server_url=args.server_url,
            username=args.username,
            password=args.password,
            folder_path=args.folder_path,
            log_file=args.log_file
        )
        
        if args.recursive:
            connector.list_all_folders()
        else:
            connector.list_files_in_folder()
        
        print("✓ OwnCloud operation completed")
        
    except ImportError as err:
        print(f"✗ Error: {err}")
    except Exception as err:
        print(f"✗ Failed: {err}")


if __name__ == "__main__":
    main()
