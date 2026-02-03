# -*- coding: utf-8 -*-
"""
Shared utilities module - Consolidated utility functions

Authors: Vic Dang
Purpose: Centralized location for all utility functions
"""

import logging
import re
import unicodedata
from pathlib import Path
from typing import Optional

LOGGER = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


class Utility:
    """Centralized utility functions for badge generation"""

    @staticmethod
    def validate(string: str, regex: str) -> str:
        """
        Validate a string against a regex pattern
        
        :param string: input string
        :param regex: regular expression to verify the string
        :return: string if valid, empty string otherwise
        :raises ValidationError: if validation fails in strict mode
        """
        if re.search(regex, string):
            return string
        else:
            msg = f"String '{string}' does not match pattern '{regex}'"
            LOGGER.error(msg)
            return ""

    @staticmethod
    def validate_strict(string: str, regex: str) -> str:
        """
        Validate a string strictly - raises exception on failure
        
        :param string: input string
        :param regex: regular expression pattern
        :return: string if valid
        :raises ValidationError: if validation fails
        """
        if not re.search(regex, string):
            raise ValidationError(f"Invalid format: '{string}' (expected pattern: '{regex}')")
        return string

    @staticmethod
    def normalize_unicode(text: str) -> str:
        """
        Normalize unicode text to NFC form
        
        :param text: text to normalize
        :return: normalized text
        """
        return unicodedata.normalize('NFC', text)

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename by removing invalid characters
        
        :param filename: filename to sanitize
        :return: sanitized filename
        """
        # Replace invalid characters
        invalid_chars = r'[<>:"/\\|?*]'
        sanitized = re.sub(invalid_chars, '_', filename)
        # Remove trailing spaces/dots
        sanitized = sanitized.rstrip('. ')
        return sanitized

    @staticmethod
    def extract_employee_id(filename: str) -> Optional[str]:
        """
        Extract employee ID from filename
        
        Format: {username}_{userid}_{position}_{number}.{ext}
        
        :param filename: filename to parse
        :return: employee ID or None if invalid
        """
        try:
            name = Path(filename).stem
            parts = name.split('_')
            
            # Must have at least 4 parts: username_userid_position_number
            if len(parts) < 4:
                return None
            
            emp_id = parts[1]  # userid
            # Ensure it looks like an employee ID (numeric or with TB prefix)
            if not emp_id or not (emp_id.isdigit() or emp_id.startswith(('TB', 'tb'))):
                return None
            
            return emp_id.lstrip('TB').lstrip('tb') if emp_id else None
        except Exception as e:
            LOGGER.warning(f"Failed to extract employee ID from {filename}: {e}")
            return None

    @staticmethod
    def is_valid_image_format(filename: str, allowed_formats: list = None) -> bool:
        """
        Check if file is a valid image format
        
        :param filename: filename to check
        :param allowed_formats: list of allowed extensions (e.g., ['.png', '.jpg'])
        :return: True if valid, False otherwise
        """
        if allowed_formats is None:
            allowed_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        
        ext = Path(filename).suffix.lower()
        return ext in allowed_formats

    @staticmethod
    def parse_dimensions(dimension_str: str) -> tuple:
        """
        Parse dimension string (e.g., "1920x1080") to tuple
        
        :param dimension_str: string in format WxH
        :return: (width, height) tuple
        :raises ValidationError: if format is invalid
        """
        try:
            parts = dimension_str.split('x')
            if len(parts) != 2:
                raise ValueError("Invalid format")
            width, height = int(parts[0]), int(parts[1])
            if width <= 0 or height <= 0:
                raise ValueError("Dimensions must be positive")
            return (width, height)
        except (ValueError, AttributeError) as e:
            raise ValidationError(f"Invalid dimension format '{dimension_str}': {e}")

    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """
        Clamp value between min and max
        
        :param value: value to clamp
        :param min_val: minimum value
        :param max_val: maximum value
        :return: clamped value
        """
        return max(min_val, min(value, max_val))

    @staticmethod
    def bytes_to_mb(bytes_size: int) -> float:
        """Convert bytes to megabytes"""
        return bytes_size / (1024 * 1024)

    @staticmethod
    def format_file_size(bytes_size: int) -> str:
        """
        Format file size to human readable format
        
        :param bytes_size: size in bytes
        :return: formatted string (e.g., "1.5 MB")
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"
