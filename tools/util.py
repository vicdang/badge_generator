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
        from pathlib import Path
        import os
        # Always resolve file_path relative to project root if not absolute
        if not os.path.isabs(file_path):
            PROJECT_ROOT = Path(__file__).parent.parent.resolve()
            ext = (PROJECT_ROOT / file_path).suffix.lower()
        else:
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
        from src.config import get_position_dict
        return get_position_dict()

    @staticmethod
    def get_list_file_extensions() -> List[str]:
        """
        Get list of supported file extensions.

        Returns:
            List of file extensions (without dots).
        """
        from src.config import get_file_extensions
        return get_file_extensions()
