# -*- coding: utf-8 -*-
"""
Unit Tests - Test suite for utilities, validators, and services

Authors: Vic Dang
Purpose: Comprehensive testing of core components
"""

import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Import modules to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utilities import Utility, ValidationError
from src.validators import ValidationResult, EmployeeDataValidator, ConfigurationValidator
from src.config_manager import ConfigManager
from src.logging_config import setup_logging, PerformanceLogger
from src.services import BadgeGenerationService, DependencyInjectionContainer


class TestUtility(unittest.TestCase):
    """Test Utility class methods"""

    def test_validate_with_valid_input(self):
        """Test validation with valid input"""
        result = Utility.validate("user123", r"^\w+\d+$")
        self.assertEqual(result, "user123")

    def test_validate_with_invalid_input(self):
        """Test validation with invalid input"""
        result = Utility.validate("invalid@#$", r"^\w+$")
        self.assertEqual(result, "")

    def test_sanitize_filename(self):
        """Test filename sanitization"""
        dirty = 'file<name>with|invalid:chars.png'
        clean = Utility.sanitize_filename(dirty)
        self.assertNotIn('<', clean)
        self.assertNotIn('>', clean)
        self.assertNotIn('|', clean)
        self.assertNotIn(':', clean)

    def test_extract_employee_id(self):
        """Test employee ID extraction from filename"""
        emp_id = Utility.extract_employee_id("john_TB123_SE_1.png")
        self.assertEqual(emp_id, "123")

    def test_extract_employee_id_invalid(self):
        """Test employee ID extraction with invalid filename"""
        emp_id = Utility.extract_employee_id("invalid_file.png")
        self.assertIsNone(emp_id)

    def test_is_valid_image_format(self):
        """Test image format validation"""
        self.assertTrue(Utility.is_valid_image_format("photo.png"))
        self.assertTrue(Utility.is_valid_image_format("photo.jpg"))
        self.assertFalse(Utility.is_valid_image_format("photo.txt"))

    def test_parse_dimensions(self):
        """Test dimension parsing"""
        width, height = Utility.parse_dimensions("1920x1080")
        self.assertEqual(width, 1920)
        self.assertEqual(height, 1080)

    def test_parse_dimensions_invalid(self):
        """Test invalid dimension parsing"""
        with self.assertRaises(ValidationError):
            Utility.parse_dimensions("invalid")

    def test_clamp_value(self):
        """Test value clamping"""
        self.assertEqual(Utility.clamp(5, 0, 10), 5)
        self.assertEqual(Utility.clamp(-5, 0, 10), 0)
        self.assertEqual(Utility.clamp(15, 0, 10), 10)

    def test_format_file_size(self):
        """Test file size formatting"""
        self.assertEqual(Utility.format_file_size(512), "512.00 B")
        self.assertIn("KB", Utility.format_file_size(1024))
        self.assertIn("MB", Utility.format_file_size(1024 * 1024))

    def test_normalize_unicode(self):
        """Test unicode normalization"""
        text = "café"
        normalized = Utility.normalize_unicode(text)
        self.assertEqual(len(normalized), len(text))


class TestValidationResult(unittest.TestCase):
    """Test ValidationResult class"""

    def test_validation_result_valid(self):
        """Test valid validation result"""
        result = ValidationResult(True)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    def test_add_error(self):
        """Test adding errors"""
        result = ValidationResult(True)
        result.add_error("Test error")
        self.assertFalse(result.is_valid)
        self.assertIn("Test error", result.errors)

    def test_merge_results(self):
        """Test merging validation results"""
        result1 = ValidationResult(True)
        result1.add_error("Error 1")

        result2 = ValidationResult(True)
        result2.add_error("Error 2")
        result2.add_warning("Warning 2")

        result1.merge(result2)
        self.assertEqual(len(result1.errors), 2)
        self.assertEqual(len(result1.warnings), 1)


class TestEmployeeDataValidator(unittest.TestCase):
    """Test employee data validation"""

    def test_validate_valid_filename(self):
        """Test validation of valid filename"""
        result = EmployeeDataValidator.validate_filename("john_001_SE_1.png")
        self.assertTrue(result.is_valid)

    def test_validate_invalid_filename(self):
        """Test validation of invalid filename"""
        result = EmployeeDataValidator.validate_filename("invalid.png")
        self.assertFalse(result.is_valid)

    def test_validate_valid_employee_data(self):
        """Test validation of valid employee data"""
        data = {
            'username': 'john',
            'userid': '001',
            'position': 'SE',
            'filename': 'john_001_SE_1.png'
        }
        result = EmployeeDataValidator.validate_employee_data(data)
        self.assertTrue(result.is_valid)

    def test_validate_incomplete_employee_data(self):
        """Test validation of incomplete employee data"""
        data = {'username': 'john'}
        result = EmployeeDataValidator.validate_employee_data(data)
        self.assertFalse(result.is_valid)
        self.assertTrue(any('Missing' in err for err in result.errors))


class TestConfigurationValidator(unittest.TestCase):
    """Test configuration validation"""

    def test_validate_dimensions(self):
        """Test dimension validation"""
        config = {'width': 1920, 'height': 1080}
        result = ConfigurationValidator.validate_badge_config(config)
        self.assertTrue(result.is_valid)

    def test_validate_invalid_dimensions(self):
        """Test invalid dimension validation"""
        config = {'width': -100, 'height': 0}
        result = ConfigurationValidator.validate_badge_config(config)
        self.assertFalse(result.is_valid)

    def test_validate_crawler_url(self):
        """Test crawler URL validation"""
        config = {'base_url': 'https://example.com', 'workers': 5, 'timeout': 30}
        result = ConfigurationValidator.validate_crawler_config(config)
        self.assertTrue(result.is_valid)

    def test_validate_invalid_crawler_url(self):
        """Test invalid crawler URL"""
        config = {'base_url': 'not-a-url', 'workers': 5, 'timeout': 30}
        result = ConfigurationValidator.validate_crawler_config(config)
        self.assertFalse(result.is_valid)


class TestConfigManager(unittest.TestCase):
    """Test ConfigManager"""

    def setUp(self):
        """Set up test fixtures"""
        ConfigManager.reset()

    def test_config_manager_singleton(self):
        """Test ConfigManager is singleton"""
        manager1 = ConfigManager()
        manager2 = ConfigManager()
        self.assertIs(manager1, manager2)

    def test_get_with_default(self):
        """Test getting config with default value"""
        manager = ConfigManager()
        value = manager.get('nonexistent', 'key', default='default_value')
        self.assertEqual(value, 'default_value')

    def test_get_int(self):
        """Test getting integer config"""
        manager = ConfigManager()
        value = manager.get_int('nonexistent', 'key', default=42)
        self.assertEqual(value, 42)


class TestPerformanceLogger(unittest.TestCase):
    """Test performance logging"""

    def test_performance_logging(self):
        """Test performance logger"""
        import logging
        logger = logging.getLogger('test')
        perf = PerformanceLogger(logger, 'test_operation')

        perf.start()
        # Simulate work
        import time
        time.sleep(0.01)
        elapsed = perf.end()

        self.assertGreater(elapsed, 0)

    def test_add_metrics(self):
        """Test adding metrics"""
        import logging
        logger = logging.getLogger('test')
        perf = PerformanceLogger(logger, 'test_operation')

        perf.add_metric('processed_items', 100)
        perf.add_metric('errors', 5, unit='count')

        self.assertEqual(len(perf.metrics), 2)


class TestBadgeGenerationService(unittest.TestCase):
    """Test badge generation service"""

    def setUp(self):
        """Set up test fixtures"""
        ConfigManager.reset()

    def test_service_initialization(self):
        """Test service initialization"""
        service = BadgeGenerationService()
        self.assertIsNotNone(service.config)
        self.assertIsNotNone(service.db)

    def test_progress_callback(self):
        """Test progress callback"""
        service = BadgeGenerationService()

        callback = Mock()
        service.set_progress_callback(callback)

        service._report_progress(5, 10, "Testing")
        callback.assert_called_once_with(5, 10, "Testing")


class TestDependencyInjection(unittest.TestCase):
    """Test dependency injection container"""

    def test_register_singleton(self):
        """Test singleton registration"""
        container = DependencyInjectionContainer()
        instance = {'test': 'data'}
        container.register_singleton('test_service', instance)

        retrieved = container.get('test_service')
        self.assertIs(retrieved, instance)

    def test_register_factory(self):
        """Test factory registration"""
        container = DependencyInjectionContainer()
        factory = Mock(return_value={'created': True})
        container.register_factory('test_service', factory)

        instance1 = container.get('test_service')
        instance2 = container.get('test_service')

        # Factory should be called once
        factory.assert_called_once()
        # Same instance returned
        self.assertIs(instance1, instance2)

    def test_get_nonexistent_service(self):
        """Test getting nonexistent service raises error"""
        container = DependencyInjectionContainer()

        with self.assertRaises(KeyError):
            container.get('nonexistent')


class TestSetupLogging(unittest.TestCase):
    """Test logging setup"""

    def test_setup_logging(self):
        """Test logging setup"""
        logger = setup_logging('test_logger', console=False, file=False)
        self.assertEqual(logger.name, 'test_logger')
        self.assertGreaterEqual(len(logger.handlers), 0)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()
