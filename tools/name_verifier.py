# -*- coding: utf-8 -*-
"""
Image name verifier - validate image filenames against required pattern.

Copyright (C) 2021
Authors: Vic Dang
Date: 16-Dec-21
Version: 1.0

Usage example:
  export PYTHONIOENCODING=utf-8
  python name_verifier.py ./img/src_img ./log.log
"""

import argparse
import logging
import logging.handlers
import re
from pathlib import Path
from typing import List, Optional

from tools.util import Utilities as uT


class ImageNameVerifier:
    """Verify image filenames against required naming pattern."""

    def __init__(self, folder_path: str, log_file: str) -> None:
        """
        Initialize ImageNameVerifier.

        Args:
            folder_path: Path to folder containing images.
            log_file: Path to log file.
        """
        self.folder_path = Path(folder_path)
        self.log_file = log_file
        
        # Build regex pattern from configuration
        positions = "|".join(uT.get_dict_positions().keys())
        extensions = "|".join(uT.get_list_file_extensions())
        
        # Pattern: name_{T|B}?digits_position_[1-3].ext
        self.pattern = (
            r'^[^\s_]+ [\w\s\u00C0-\u017F]+_(T|B)?\d{6}_'
            r'(' + positions + r')_[1-3]\.'
            r'(' + extensions + r')$'
        )
        self.regex = re.compile(self.pattern, re.UNICODE | re.IGNORECASE)
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """
        Setup logging configuration.

        Returns:
            Configured logger instance.
        """
        logger = logging.getLogger('image_name_verification')
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

    def verify_name(self, name: str, counter: int = 1) -> bool:
        """
        Verify a single filename.

        Args:
            name: Filename to verify.
            counter: Counter for output formatting.

        Returns:
            True if filename is valid, False otherwise.
        """
        is_valid = bool(self.regex.match(name))
        status = "✓" if is_valid else "✗"
        message = f"{counter:4} [{status}] {name}"
        self.logger.info(message)
        return is_valid

    def verify_names(self, names: List[str]) -> int:
        """
        Verify a list of filenames.

        Args:
            names: List of filenames to verify.

        Returns:
            Number of valid filenames.
        """
        valid_count = 0
        for counter, name in enumerate(names, 1):
            if self.verify_name(name, counter):
                valid_count += 1
        return valid_count

    def verify_folder(self) -> tuple:
        """
        Verify all image filenames in folder.

        Returns:
            Tuple of (total_files, valid_files, invalid_files).
        """
        if not self.folder_path.exists():
            self.logger.error(f"Folder not found: {self.folder_path}")
            return 0, 0, []

        files = [f.name for f in self.folder_path.iterdir() if f.is_file()]
        
        self.logger.info(f"Verifying {len(files)} files in {self.folder_path}")
        
        valid_count = 0
        invalid_files: List[str] = []
        
        for counter, filename in enumerate(files, 1):
            if self.verify_name(filename, counter):
                valid_count += 1
            else:
                invalid_files.append(filename)
        
        return len(files), valid_count, invalid_files


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Verify image filenames against required pattern.'
    )
    parser.add_argument(
        '-f', '--folder-path',
        dest='folder_path',
        type=str,
        default="./mock_images",
        help='Path to folder containing images'
    )
    parser.add_argument(
        '-l', '--log-file',
        dest='log_file',
        type=str,
        default="./log.log",
        help='Path to log file'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    return parser.parse_args()


def main() -> None:
    """Main execution function."""
    args = parse_arguments()
    
    verifier = ImageNameVerifier(args.folder_path, args.log_file)
    total, valid, invalid = verifier.verify_folder()
    
    print(f"\n=== Verification Summary ===")
    print(f"Total files: {total}")
    print(f"Valid: {valid}")
    print(f"Invalid: {len(invalid)}")
    
    if invalid and args.verbose:
        print(f"\nInvalid files:")
        for filename in invalid:
            print(f"  - {filename}")


if __name__ == "__main__":
    main()
