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
file_extensions: List[str] = ['png', 'jpg', 'bmp', 'jpeg', 'webp']

# GUI Configuration
gui_config: Dict[str, any] = {
    # Window settings
    'window_title': 'Image Producer',
    'window_height': 790,
    'window_width': 1700,
    'grid_cols': 5,
    
    # Window and layout
    'padding': 2,
    'frame_padx': 2,
    'frame_pady': 2,
    'frame_ipadx': 2,
    'frame_ipady': 2,
    
    # Font
    'font_name': 'Lucida Grande',
    'font_size': 12,
    
    # Section frames (Legend/LabelFrame)
    'section_padx': 5,
    'section_pady': 5,
    'section_ipadx': 5,
    'section_ipady': 5,  # Reduce this to decrease section height
    'section_expand': False,  # Set to False to prevent sections from expanding vertically
    
    # Labels
    'label_justify': 'left',
    'label_text_align': 'left',    # 'left', 'right', or 'center'
    'label_padx': 5,
    'label_width': 30,             # Width in characters
    'label_color': '#000000',      # Text color in HEX format
    'label_ipadx': 10,
    
    # Input fields (textbox for configuration parameters)
    'input_width': 10,
    'input_width_file': 10,
    'input_width_button': 15,
    'input_ipadx': 5,
    'input_pady': 5,
    'input_grid_padx': 0,
    'input_grid_pady': 0,
    'input_grid_ipadx': 0,
    'input_sticky': 'EW',
    
    # Buttons
    'button_height': 2,
    'button_width': 5,
    'button_padx': 5,
    'button_pady': 5,
    'button_ipadx': 5,
    'button_ipady': 5,
    'execute_bg': 'Light grey',
    'execute_fg': 'Black',
    'save_bg': 'Light grey',
    'save_fg': 'Black',
    'generate_bg': 'Green',
    'generate_fg': 'Black',
    
    # Text box
    'textbox_height': 38,
    'textbox_width': 60,
    'textbox_fg': 'Light green',
    'textbox_bg': 'Black',
    'textbox_padx': 10,
    'textbox_pady': 10,
    'textbox_ipadx': 5,
    'textbox_ipady': 5,
    
    # Progress bar
    'progressbar_length': 10,
    'progressbar_height': 1,
    'progressbar_padx': 5,
    'progressbar_pady': 5,
    'progressbar_ipadx': 5,
    'progressbar_ipady': 5,    
    'progressbar_pulse_interval': 10,  # Lower value = faster animation (in milliseconds)
}


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


def get_gui_config() -> Dict[str, any]:
    """
    Get GUI configuration.

    Returns:
        Dictionary with GUI configuration values.
    """
    return gui_config.copy()

def get_label_config() -> Dict[str, any]:
    """
    Get label configuration.

    Returns:
        Dictionary with label configuration values.
    """
    return label_config.copy()