# -*- coding: utf-8 -*-
"""
Structured Logging System - JSON-formatted logs with rotation

Authors: Vic Dang
Purpose: Comprehensive logging with structured format and performance tracking
"""

import json
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
LOGS_DIR = PROJECT_ROOT / 'logs'


class JSONFormatter(logging.Formatter):
    """Custom formatter for JSON-structured logs"""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # Add custom fields if present
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data

        return json.dumps(log_data, default=str)


class PerformanceLogger:
    """Helper class for logging performance metrics"""

    def __init__(self, logger: logging.Logger, operation_name: str):
        """
        Initialize performance logger
        
        :param logger: logger instance
        :param operation_name: name of operation being timed
        """
        self.logger = logger
        self.operation_name = operation_name
        self.start_time = None
        self.metrics: Dict[str, Any] = {}

    def start(self):
        """Start timing"""
        import time
        self.start_time = time.time()
        self.logger.debug(f"Started: {self.operation_name}")

    def end(self) -> float:
        """End timing and return elapsed time in milliseconds"""
        import time
        if self.start_time is None:
            self.logger.warning(f"Timer not started for {self.operation_name}")
            return 0

        elapsed_ms = (time.time() - self.start_time) * 1000
        self.logger.info(
            f"Completed: {self.operation_name}",
            extra={'extra_data': {
                'operation': self.operation_name,
                'elapsed_ms': round(elapsed_ms, 2)
            }}
        )
        return elapsed_ms

    def add_metric(self, name: str, value: Any, unit: str = None):
        """Add metric to log"""
        self.metrics[name] = {'value': value, 'unit': unit}

    def log_metrics(self):
        """Log all collected metrics"""
        if self.metrics:
            self.logger.info(
                f"Metrics for {self.operation_name}",
                extra={'extra_data': {
                    'operation': self.operation_name,
                    'metrics': self.metrics
                }}
            )


def setup_logging(
    name: str = None,
    level: int = logging.INFO,
    console: bool = True,
    file: bool = True,
    json_format: bool = True
) -> logging.Logger:
    """
    Setup structured logging with file rotation and console output

    :param name: logger name (defaults to root)
    :param level: logging level
    :param console: enable console output
    :param file: enable file output
    :param json_format: use JSON format for logs
    :return: configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create logs directory
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Remove existing handlers
    logger.handlers.clear()

    # Choose formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    # Console handler
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler with rotation
    if file:
        log_file = LOGS_DIR / f"{name or 'app'}.log" if name else LOGS_DIR / "app.log"

        # Rotating file handler - max 10MB per file, keep 5 backups
        file_handler = logging.handlers.RotatingFileHandler(
            str(log_file),
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get or create logger with given name"""
    return logging.getLogger(name)


class LoggerContext:
    """Context manager for temporary log level changes"""

    def __init__(self, logger: logging.Logger, level: int):
        """
        Initialize context
        
        :param logger: logger instance
        :param level: temporary log level
        """
        self.logger = logger
        self.level = level
        self.original_level = logger.level

    def __enter__(self):
        self.logger.setLevel(self.level)
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.setLevel(self.original_level)


# Initialize root logger
setup_logging(level=logging.INFO)
