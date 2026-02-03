# -*- coding: utf-8 -*-
"""
Service Layer - High-level business logic abstraction

Authors: Vic Dang
Purpose: Separate business logic from implementation details
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass

from src.config_manager import ConfigManager
from src.database import Database
from src.validators import validate_all, EmployeeDataValidator, ImageValidator
from src.logging_config import get_logger, PerformanceLogger
from src.utilities import Utility

LOGGER = get_logger(__name__)


@dataclass
class BadgeProcessingResult:
    """Result of badge processing"""
    success: bool
    badge_id: int
    filename: str
    output_path: Optional[str] = None
    processing_time_ms: int = 0
    error_message: Optional[str] = None

    def __str__(self) -> str:
        status = "✅ Success" if self.success else "❌ Failed"
        return f"{status}: {self.filename} ({self.processing_time_ms}ms)"


@dataclass
class JobStatistics:
    """Statistics for a badge generation job"""
    total_badges: int = 0
    processed_badges: int = 0
    successful_badges: int = 0
    failed_badges: int = 0
    skipped_badges: int = 0
    avg_processing_time_ms: float = 0
    total_processing_time_ms: int = 0

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total_badges == 0:
            return 0
        return (self.successful_badges / self.total_badges) * 100

    def __str__(self) -> str:
        return (
            f"Job Statistics:\n"
            f"  Total: {self.total_badges}\n"
            f"  Processed: {self.processed_badges}\n"
            f"  Success: {self.successful_badges} ({self.success_rate:.1f}%)\n"
            f"  Failed: {self.failed_badges}\n"
            f"  Skipped: {self.skipped_badges}\n"
            f"  Avg Time: {self.avg_processing_time_ms:.2f}ms\n"
            f"  Total Time: {self.total_processing_time_ms}ms"
        )


class BadgeGenerationService:
    """Service for badge generation with progress tracking"""

    def __init__(self, config: ConfigManager = None, db: Database = None):
        """
        Initialize badge generation service

        :param config: ConfigManager instance (creates default if None)
        :param db: Database instance (creates default if None)
        """
        self.config = config or ConfigManager()
        self.db = db or Database()
        self.progress_callback: Optional[Callable] = None
        self.current_job_id: Optional[int] = None

    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """
        Set callback for progress updates

        :param callback: function(current, total, message) called for progress updates
        """
        self.progress_callback = callback

    def _report_progress(self, current: int, total: int, message: str = ""):
        """Report progress via callback"""
        if self.progress_callback:
            try:
                self.progress_callback(current, total, message)
            except Exception as e:
                LOGGER.warning(f"Progress callback error: {e}")

    def create_job(self, job_name: str, images: List[Path], profile: str = None) -> int:
        """
        Create new badge generation job

        :param job_name: name for this job
        :param images: list of image paths to process
        :param profile: config profile name to use
        :return: job ID
        """
        job_id = self.db.create_job(
            job_name=job_name,
            total_badges=len(images),
            config_profile=profile
        )
        self.current_job_id = job_id
        LOGGER.info(f"Created job {job_id}: {job_name} with {len(images)} images")
        return job_id

    def validate_batch(self, images: List[Path], employee_data: List[Dict]) -> Dict:
        """
        Validate a batch of images and employee data

        :param images: list of image paths
        :param employee_data: list of employee data dicts
        :return: validation report dictionary
        """
        perf = PerformanceLogger(LOGGER, "batch_validation")
        perf.start()

        report = {
            'total_images': len(images),
            'valid_images': 0,
            'invalid_images': [],
            'total_employees': len(employee_data),
            'valid_employees': 0,
            'invalid_employees': [],
            'warnings': [],
        }

        # Validate images
        self._report_progress(0, len(images) + len(employee_data), "Validating images...")
        valid_images, image_errors = ImageValidator.validate_batch_images(images)
        report['valid_images'] = len(valid_images)
        report['invalid_images'] = image_errors

        # Validate employees
        self._report_progress(len(images), len(images) + len(employee_data), "Validating employees...")
        for emp_data in employee_data:
            result = EmployeeDataValidator.validate_employee_data(emp_data)
            if result.is_valid:
                report['valid_employees'] += 1
            else:
                report['invalid_employees'].append({
                    'data': emp_data,
                    'errors': result.errors
                })
            report['warnings'].extend(result.warnings)

        perf.add_metric('valid_images', report['valid_images'])
        perf.add_metric('valid_employees', report['valid_employees'])
        perf.log_metrics()
        elapsed = perf.end()

        return report

    def process_badge(self, badge_data: Dict) -> BadgeProcessingResult:
        """
        Process single badge (to be overridden by subclass with actual logic)

        :param badge_data: badge data dictionary
        :return: processing result
        """
        # This is a placeholder - actual badge generation logic would go here
        # In a real implementation, this would call the BadgeMaker class

        try:
            filename = badge_data.get('filename', 'unknown')
            perf = PerformanceLogger(LOGGER, f"badge_processing_{filename}")
            perf.start()

            # Placeholder logic
            badge_id = self.db.add_badge(
                job_id=self.current_job_id or 0,
                filename=filename
            )

            elapsed = perf.end()

            return BadgeProcessingResult(
                success=True,
                badge_id=badge_id,
                filename=filename,
                processing_time_ms=int(elapsed)
            )

        except Exception as e:
            LOGGER.error(f"Badge processing failed: {e}")
            return BadgeProcessingResult(
                success=False,
                badge_id=0,
                filename=badge_data.get('filename', 'unknown'),
                error_message=str(e)
            )

    def process_batch(self, badges: List[Dict]) -> JobStatistics:
        """
        Process batch of badges with progress tracking

        :param badges: list of badge data dictionaries
        :return: job statistics
        """
        stats = JobStatistics(total_badges=len(badges))
        perf = PerformanceLogger(LOGGER, "batch_processing")
        perf.start()

        for i, badge_data in enumerate(badges):
            self._report_progress(i, len(badges), f"Processing {i+1}/{len(badges)}")

            result = self.process_badge(badge_data)

            if result.success:
                stats.successful_badges += 1
                self.db.update_badge(
                    result.badge_id,
                    status='success',
                    processing_time_ms=result.processing_time_ms
                )
            else:
                stats.failed_badges += 1
                self.db.update_badge(
                    result.badge_id,
                    status='failed',
                    error_message=result.error_message
                )

            stats.processed_badges += 1
            stats.total_processing_time_ms += result.processing_time_ms

        self._report_progress(len(badges), len(badges), "Batch processing complete")

        # Update job status
        if self.current_job_id:
            status = 'completed' if stats.failed_badges == 0 else 'failed'
            self.db.update_job_status(self.current_job_id, status)

        # Calculate averages
        if stats.processed_badges > 0:
            stats.avg_processing_time_ms = stats.total_processing_time_ms / stats.processed_badges

        perf.add_metric('total_badges', stats.total_badges)
        perf.add_metric('successful', stats.successful_badges)
        perf.add_metric('failed', stats.failed_badges)
        perf.add_metric('avg_time_ms', round(stats.avg_processing_time_ms, 2))
        perf.log_metrics()
        elapsed = perf.end()

        LOGGER.info(f"Batch processing complete: {stats}")

        return stats

    def get_job_statistics(self, job_id: int) -> Dict:
        """Get detailed statistics for a job"""
        try:
            job = self.db.get_job(job_id)
            badges = self.db.get_job_badges(job_id)
            metrics = self.db.get_job_metrics(job_id)

            stats = {
                'job_id': job_id,
                'job_name': job['job_name'] if job else 'Unknown',
                'status': job['status'] if job else 'Unknown',
                'total_badges': len(badges),
                'badges_by_status': {},
                'metrics': metrics,
            }

            for badge in badges:
                status = badge['status']
                stats['badges_by_status'][status] = stats['badges_by_status'].get(status, 0) + 1

            return stats

        except Exception as e:
            LOGGER.error(f"Failed to get job statistics: {e}")
            return {}

    def save_configuration_profile(self, profile_name: str, config_data: Dict, is_default: bool = False):
        """Save configuration profile to database"""
        try:
            import json
            config_json = json.dumps(config_data, indent=2)
            self.db.save_profile(profile_name, config_json, is_default)
            LOGGER.info(f"Saved configuration profile: {profile_name}")
        except Exception as e:
            LOGGER.error(f"Failed to save profile: {e}")
            raise

    def load_configuration_profile(self, profile_name: str) -> Optional[Dict]:
        """Load configuration profile from database"""
        try:
            import json
            config_json = self.db.get_profile(profile_name)
            if config_json:
                return json.loads(config_json)
            return None
        except Exception as e:
            LOGGER.error(f"Failed to load profile: {e}")
            return None


class DependencyInjectionContainer:
    """Simple DI container for managing service dependencies"""

    def __init__(self):
        self._services: Dict[str, any] = {}
        self._factories: Dict[str, Callable] = {}

    def register_singleton(self, name: str, instance: any):
        """Register singleton instance"""
        self._services[name] = instance

    def register_factory(self, name: str, factory: Callable):
        """Register factory function"""
        self._factories[name] = factory

    def get(self, name: str) -> any:
        """Get service instance"""
        if name in self._services:
            return self._services[name]
        if name in self._factories:
            instance = self._factories[name]()
            self._services[name] = instance
            return instance
        raise KeyError(f"Service not registered: {name}")

    def create_default_container(self) -> 'DependencyInjectionContainer':
        """Create container with default services"""
        container = DependencyInjectionContainer()

        # Register singletons
        config = ConfigManager()
        database = Database()

        container.register_singleton('config', config)
        container.register_singleton('database', database)
        container.register_singleton('badge_service', BadgeGenerationService(config, database))

        return container


# Global DI container
_container = None


def get_container() -> DependencyInjectionContainer:
    """Get or create global DI container"""
    global _container
    if _container is None:
        _container = DependencyInjectionContainer().create_default_container()
    return _container


def reset_container():
    """Reset global DI container (useful for testing)"""
    global _container
    _container = None
