# -*- coding: utf-8 -*-
"""
Utility functions for badge generator.

Copyright (C) 2022
Authors: Vic Dang
Date: 22-Mar-22
Version: 1.0
"""

from pathlib import Path
from typing import Dict, List

from config import app_conf as conf


class Utilities:
    """Utility functions for file handling and configuration."""

    @staticmethod
    def check_file_type(file_path: str) -> str:
        """
        Check the file type based on extension.

        Args:
            file_path: Path to the file.

        Returns:
            File type as string: 'excel', 'txt', or 'Unknown'.
        """
        ext = Path(file_path).suffix.lower()
        
        if ext in {'.xlsx', '.xls'}:
            return "excel"
        elif ext in {'.txt', '.ini'}:
            return "txt"
        
        return "Unknown"

    @staticmethod
    def get_dict_positions() -> Dict[str, str]:
        """
        Get position mapping dictionary.

        Returns:
            Dictionary mapping position codes to position names.
        """
        return conf.positions

    @staticmethod
    def get_list_file_extensions() -> List[str]:
        """
        Get list of supported file extensions.

        Returns:
            List of file extensions (without dots).
        """
        return conf.file_extensions
