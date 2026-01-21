# -*- coding: utf-8 -*-
"""
Application configuration - position and file extension definitions.

Copyright (C) 2023
Authors: dnnvu
Date: 07-Dec-23
Version: 1.0
"""

from typing import Dict, List

# Position mapping: code -> full name
positions: Dict[str, str] = {
    "A": "Assistant",
    "SA": "Senior Assistant",
    "SME": "Subject Matter Expert",
    "SE": "Senior Engineer",
    "TL": "Team Lead",
    "PM": "Project Manager",
    "SM": "Senior Manager",
    "D": "Director",
    "E": "Engineer",
    "SD": "Senior Director",
    "VP": "Vice President",
    "CEO": "CEO",
}

# Supported image file extensions
file_extensions: List[str] = ['png', 'jpg', 'bmp', 'jpeg']


def get_position_dict() -> Dict[str, str]:
    """
    Get position mapping dictionary.

    Returns:
        Dictionary mapping position codes to full names.
    """
    return positions.copy()


def get_file_extensions() -> List[str]:
    """
    Get list of supported file extensions.

    Returns:
        List of supported file extensions.
    """
    return file_extensions.copy()
