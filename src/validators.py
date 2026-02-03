# -*- coding: utf-8 -*-
"""
Input Validation Pipeline - Comprehensive validation for all inputs

Authors: Vic Dang
Purpose: Validate images, configuration, and employee data before processing
"""

import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import cv2
import numpy as np
from PIL import Image

from src.utilities import Utility, ValidationError

LOGGER = logging.getLogger(__name__)


class ValidationResult:
    """Holds validation results with detailed error information"""

    def __init__(self, is_valid: bool, errors: List[str] = None, warnings: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []

    def add_error(self, error: str):
        """Add error message"""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str):
        """Add warning message"""
        self.warnings.append(warning)

    def merge(self, other: 'ValidationResult'):
        """Merge another validation result into this one"""
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.is_valid = self.is_valid and other.is_valid

    def __str__(self) -> str:
        lines = []
        if self.errors:
            lines.append("❌ Errors:")
            for error in self.errors:
                lines.append(f"  - {error}")
        if self.warnings:
            lines.append("⚠️  Warnings:")
            for warning in self.warnings:
                lines.append(f"  - {warning}")
        if not self.errors and not self.warnings:
            lines.append("✅ Validation passed")
        return "\n".join(lines)


class ImageValidator:
    """Validates image files and quality"""

    MIN_IMAGE_WIDTH = 100
    MIN_IMAGE_HEIGHT = 100
    MAX_IMAGE_WIDTH = 10000
    MAX_IMAGE_HEIGHT = 10000
    MAX_FILE_SIZE_MB = 100

    @classmethod
    def validate_image_file(cls, filepath: Path) -> ValidationResult:
        """
        Validate image file comprehensively
        
        :param filepath: path to image file
        :return: ValidationResult with detailed feedback
        """
        result = ValidationResult(True)

        # Check file existence
        if not filepath.exists():
            result.add_error(f"Image file not found: {filepath}")
            return result

        # Check file extension
        if not Utility.is_valid_image_format(filepath.name):
            result.add_error(f"Invalid image format: {filepath.suffix}. Supported: PNG, JPG, BMP, TIFF")
            return result

        # Check file size
        file_size_mb = filepath.stat().st_size / (1024 * 1024)
        if file_size_mb > cls.MAX_FILE_SIZE_MB:
            result.add_error(f"Image file too large: {file_size_mb:.2f} MB (max: {cls.MAX_FILE_SIZE_MB} MB)")
            return result

        if file_size_mb < 0.01:
            result.add_error("Image file is too small (empty or corrupted)")
            return result

        # Try to open and verify
        try:
            with Image.open(filepath) as img:
                width, height = img.size
                
                # Check dimensions
                if width < cls.MIN_IMAGE_WIDTH or height < cls.MIN_IMAGE_HEIGHT:
                    result.add_error(
                        f"Image too small: {width}x{height} (min: {cls.MIN_IMAGE_WIDTH}x{cls.MIN_IMAGE_HEIGHT})"
                    )
                
                if width > cls.MAX_IMAGE_WIDTH or height > cls.MAX_IMAGE_HEIGHT:
                    result.add_error(
                        f"Image too large: {width}x{height} (max: {cls.MAX_IMAGE_WIDTH}x{cls.MAX_IMAGE_HEIGHT})"
                    )
                
                # Check if image has content
                arr = np.array(img)
                if np.all(arr == arr[0, 0]):
                    result.add_warning("Image appears to be single color (possibly blank)")

        except Exception as e:
            result.add_error(f"Failed to open/read image: {e}")

        return result

    @classmethod
    def validate_batch_images(cls, filepaths: List[Path]) -> Tuple[List[Path], Dict[str, str]]:
        """
        Validate multiple images, separate valid from invalid
        
        :param filepaths: list of image paths
        :return: (valid_files, error_dict) where error_dict maps filename to error message
        """
        valid_files = []
        errors = {}

        for filepath in filepaths:
            result = cls.validate_image_file(filepath)
            if result.is_valid:
                valid_files.append(filepath)
            else:
                errors[filepath.name] = "; ".join(result.errors)

        return valid_files, errors


class EmployeeDataValidator:
    """Validates employee data and filenames"""

    @classmethod
    def validate_filename(cls, filename: str) -> ValidationResult:
        """
        Validate employee filename format
        
        Format: {username}_{userid}_{position}_{number}.{ext}
        
        :param filename: filename to validate
        :return: ValidationResult
        """
        result = ValidationResult(True)

        try:
            name = Path(filename).stem
            ext = Path(filename).suffix.lower()

            # Check extension
            if not Utility.is_valid_image_format(filename):
                result.add_error(f"Invalid file extension: {ext}")
                return result

            # Parse components
            parts = name.split('_')
            if len(parts) < 3:
                result.add_error(
                    f"Invalid filename format. Expected: username_userid_position_number.ext, got: {filename}"
                )
                return result

            username, userid, position = parts[0], parts[1], parts[2]

            # Validate components
            if not username:
                result.add_error("Username cannot be empty")
            
            if not userid:
                result.add_error("User ID cannot be empty")
            else:
                # User ID should be numeric
                if not userid.lstrip('TB').isdigit():
                    result.add_warning(f"User ID '{userid}' contains non-numeric characters")

            if not position:
                result.add_error("Position code cannot be empty")

        except Exception as e:
            result.add_error(f"Failed to validate filename: {e}")

        return result

    @classmethod
    def validate_employee_data(cls, data: Dict) -> ValidationResult:
        """
        Validate employee data dictionary
        
        :param data: employee data dict with keys: username, userid, position, filename
        :return: ValidationResult
        """
        result = ValidationResult(True)

        required_fields = ['username', 'userid', 'position', 'filename']
        for field in required_fields:
            if field not in data or not data[field]:
                result.add_error(f"Missing required field: {field}")

        if 'username' in data and len(data['username']) > 100:
            result.add_error("Username too long (max 100 characters)")

        if 'userid' in data and len(data['userid']) > 50:
            result.add_error("User ID too long (max 50 characters)")

        # Validate filename if present
        if 'filename' in data:
            filename_result = cls.validate_filename(data['filename'])
            result.merge(filename_result)

        return result


class ConfigurationValidator:
    """Validates application configuration"""

    @classmethod
    def validate_paths(cls, paths: Dict[str, Path]) -> ValidationResult:
        """
        Validate that all required paths exist or can be created
        
        :param paths: dictionary of path names to Path objects
        :return: ValidationResult
        """
        result = ValidationResult(True)

        for path_name, path_obj in paths.items():
            if not isinstance(path_obj, Path):
                result.add_error(f"Invalid path type for {path_name}: {type(path_obj)}")
                continue

            if not path_obj.exists():
                result.add_warning(f"Path does not exist and will be created: {path_name} → {path_obj}")
                # Try to create parent directories
                try:
                    path_obj.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    result.add_error(f"Cannot create directory {path_name}: {e}")

        return result

    @classmethod
    def validate_badge_config(cls, badge_config: Dict) -> ValidationResult:
        """
        Validate badge generation configuration
        
        :param badge_config: badge config dictionary
        :return: ValidationResult
        """
        result = ValidationResult(True)

        # Validate dimensions
        if 'width' in badge_config:
            width = badge_config['width']
            if not isinstance(width, int) or width <= 0:
                result.add_error(f"Invalid width: {width} (must be positive integer)")
            elif width > 10000:
                result.add_error(f"Width too large: {width} (max: 10000)")

        if 'height' in badge_config:
            height = badge_config['height']
            if not isinstance(height, int) or height <= 0:
                result.add_error(f"Invalid height: {height} (must be positive integer)")
            elif height > 10000:
                result.add_error(f"Height too large: {height} (max: 10000)")

        # Validate text size
        if 'text_size' in badge_config:
            text_size = badge_config['text_size']
            if not isinstance(text_size, int) or text_size <= 0:
                result.add_error(f"Invalid text size: {text_size} (must be positive integer)")

        return result

    @classmethod
    def validate_crawler_config(cls, crawler_config: Dict) -> ValidationResult:
        """
        Validate image crawler configuration
        
        :param crawler_config: crawler config dictionary
        :return: ValidationResult
        """
        result = ValidationResult(True)

        if not crawler_config.get('base_url'):
            result.add_warning("No base URL configured for image crawler")
        else:
            url = crawler_config['base_url']
            if not url.startswith(('http://', 'https://')):
                result.add_error(f"Invalid URL: {url} (must start with http:// or https://)")

        workers = crawler_config.get('workers', 5)
        if not isinstance(workers, int) or workers <= 0:
            result.add_error(f"Invalid worker count: {workers} (must be positive integer)")
        elif workers > 100:
            result.add_warning(f"Many workers requested: {workers} (recommended max: 20)")

        timeout = crawler_config.get('timeout', 30)
        if not isinstance(timeout, int) or timeout <= 0:
            result.add_error(f"Invalid timeout: {timeout} (must be positive integer)")

        return result


def validate_all(image_paths: List[Path], employee_data: List[Dict], config: Dict) -> ValidationResult:
    """
    Run complete validation pipeline
    
    :param image_paths: list of image file paths
    :param employee_data: list of employee data dictionaries
    :param config: configuration dictionary
    :return: ValidationResult with all checks
    """
    result = ValidationResult(True)

    # Validate images
    LOGGER.info(f"Validating {len(image_paths)} images...")
    valid_images, image_errors = ImageValidator.validate_batch_images(image_paths)
    if image_errors:
        for filename, error in list(image_errors.items())[:5]:  # Show first 5 errors
            result.add_error(f"Image {filename}: {error}")
        if len(image_errors) > 5:
            result.add_error(f"... and {len(image_errors) - 5} more image errors")

    # Validate employee data
    LOGGER.info(f"Validating {len(employee_data)} employee records...")
    for i, emp_data in enumerate(employee_data[:10]):  # Check first 10
        emp_result = EmployeeDataValidator.validate_employee_data(emp_data)
        if not emp_result.is_valid:
            result.add_error(f"Employee #{i+1}: {'; '.join(emp_result.errors[:2])}")

    # Validate configuration
    if 'paths' in config:
        LOGGER.info("Validating paths...")
        path_result = ConfigurationValidator.validate_paths(config['paths'])
        result.merge(path_result)

    if 'badge' in config:
        LOGGER.info("Validating badge configuration...")
        badge_result = ConfigurationValidator.validate_badge_config(config['badge'])
        result.merge(badge_result)

    if 'crawler' in config:
        LOGGER.info("Validating crawler configuration...")
        crawler_result = ConfigurationValidator.validate_crawler_config(config['crawler'])
        result.merge(crawler_result)

    return result
