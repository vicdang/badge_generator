# -*- coding: utf-8 -*-
"""
SQLite Database Backend - Track badge generation history and statistics

Authors: Vic Dang
Purpose: Persistent storage for badges, employees, and processing history
"""

import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

LOGGER = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DB_PATH = PROJECT_ROOT / 'data' / 'badgegenerator.db'


class Database:
    """SQLite database manager for badge generation tracking"""

    def __init__(self, db_path: Path = None):
        """
        Initialize database connection
        
        :param db_path: path to database file (default: data/badgegenerator.db)
        """
        self.db_path = db_path or DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        self._initialize_connection()
        self._initialize_schema()

    def _initialize_connection(self):
        """Initialize database connection"""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            # Enable foreign keys
            self.connection.execute("PRAGMA foreign_keys = ON")
            LOGGER.info(f"Database connection established: {self.db_path}")
        except Exception as e:
            LOGGER.error(f"Failed to connect to database: {e}")
            raise

    def _initialize_schema(self):
        """Create tables if they don't exist"""
        try:
            cursor = self.connection.cursor()

            # Employees table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    username TEXT NOT NULL,
                    position TEXT,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Badge generation jobs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS badge_jobs (
                    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_name TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',  -- pending, running, completed, failed
                    total_badges INTEGER DEFAULT 0,
                    processed_badges INTEGER DEFAULT 0,
                    failed_count INTEGER DEFAULT 0,
                    config_profile TEXT,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Individual badge records
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS badges (
                    badge_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id INTEGER NOT NULL,
                    emp_id INTEGER,
                    filename TEXT NOT NULL,
                    output_path TEXT,
                    status TEXT DEFAULT 'pending',  -- pending, processing, success, failed
                    image_hash TEXT,
                    file_size_bytes INTEGER,
                    processing_time_ms INTEGER,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES badge_jobs(job_id),
                    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
                )
            """)

            # Image downloads history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS image_downloads (
                    download_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    emp_id INTEGER,
                    source_url TEXT NOT NULL,
                    destination_path TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',  -- pending, success, failed
                    file_size_bytes INTEGER,
                    download_time_ms INTEGER,
                    error_message TEXT,
                    attempted_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
                )
            """)

            # Configuration profiles
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS config_profiles (
                    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_name TEXT UNIQUE NOT NULL,
                    config_data TEXT NOT NULL,  -- JSON serialized config
                    is_default BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Performance metrics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id INTEGER,
                    metric_name TEXT NOT NULL,
                    metric_value REAL,
                    unit TEXT,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES badge_jobs(job_id)
                )
            """)

            self.connection.commit()
            LOGGER.info("Database schema initialized")

        except Exception as e:
            LOGGER.error(f"Failed to initialize schema: {e}")
            raise

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            LOGGER.info("Database connection closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # Employee operations

    def add_employee(self, user_id: str, username: str, position: str = None, email: str = None) -> int:
        """Add or update employee"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO employees (user_id, username, position, email, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(user_id) DO UPDATE SET
                    username = excluded.username,
                    position = excluded.position,
                    email = excluded.email,
                    updated_at = CURRENT_TIMESTAMP
            """, (user_id, username, position, email))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            LOGGER.error(f"Failed to add employee: {e}")
            raise

    def get_employee(self, user_id: str) -> Optional[Dict]:
        """Get employee by user ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM employees WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            LOGGER.error(f"Failed to get employee: {e}")
            return None

    # Badge job operations

    def create_job(self, job_name: str, total_badges: int, config_profile: str = None) -> int:
        """Create new badge generation job"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO badge_jobs (job_name, total_badges, config_profile, status, started_at)
                VALUES (?, ?, ?, 'running', CURRENT_TIMESTAMP)
            """, (job_name, total_badges, config_profile))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            LOGGER.error(f"Failed to create job: {e}")
            raise

    def update_job_status(self, job_id: int, status: str, error_message: str = None):
        """Update job status"""
        try:
            cursor = self.connection.cursor()
            if status == 'completed':
                cursor.execute("""
                    UPDATE badge_jobs 
                    SET status = ?, completed_at = CURRENT_TIMESTAMP
                    WHERE job_id = ?
                """, (status, job_id))
            else:
                cursor.execute("""
                    UPDATE badge_jobs 
                    SET status = ?, error_message = ?
                    WHERE job_id = ?
                """, (status, error_message, job_id))
            self.connection.commit()
        except Exception as e:
            LOGGER.error(f"Failed to update job status: {e}")
            raise

    def get_job(self, job_id: int) -> Optional[Dict]:
        """Get job details"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM badge_jobs WHERE job_id = ?", (job_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            LOGGER.error(f"Failed to get job: {e}")
            return None

    # Badge operations

    def add_badge(self, job_id: int, filename: str, emp_id: int = None) -> int:
        """Add badge record for a job"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO badges (job_id, emp_id, filename, status)
                VALUES (?, ?, ?, 'pending')
            """, (job_id, emp_id, filename))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            LOGGER.error(f"Failed to add badge: {e}")
            raise

    def update_badge(self, badge_id: int, status: str, output_path: str = None,
                     processing_time_ms: int = None, error_message: str = None):
        """Update badge record after processing"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE badges
                SET status = ?, output_path = ?, processing_time_ms = ?, error_message = ?
                WHERE badge_id = ?
            """, (status, output_path, processing_time_ms, error_message, badge_id))
            self.connection.commit()
        except Exception as e:
            LOGGER.error(f"Failed to update badge: {e}")
            raise

    def get_job_badges(self, job_id: int) -> List[Dict]:
        """Get all badges for a job"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM badges WHERE job_id = ? ORDER BY badge_id", (job_id,))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            LOGGER.error(f"Failed to get job badges: {e}")
            return []

    # Download operations

    def add_download_record(self, source_url: str, destination_path: str, emp_id: int = None) -> int:
        """Add image download record"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO image_downloads (emp_id, source_url, destination_path, status, attempted_at)
                VALUES (?, ?, ?, 'pending', CURRENT_TIMESTAMP)
            """, (emp_id, source_url, destination_path))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            LOGGER.error(f"Failed to add download record: {e}")
            raise

    def update_download(self, download_id: int, status: str, file_size_bytes: int = None,
                       download_time_ms: int = None, error_message: str = None):
        """Update download record"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE image_downloads
                SET status = ?, file_size_bytes = ?, download_time_ms = ?,
                    error_message = ?, completed_at = CURRENT_TIMESTAMP
                WHERE download_id = ?
            """, (status, file_size_bytes, download_time_ms, error_message, download_id))
            self.connection.commit()
        except Exception as e:
            LOGGER.error(f"Failed to update download: {e}")
            raise

    # Configuration profiles

    def save_profile(self, profile_name: str, config_data: str, is_default: bool = False):
        """Save configuration profile"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO config_profiles (profile_name, config_data, is_default, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (profile_name, config_data, is_default))
            self.connection.commit()
            LOGGER.info(f"Saved config profile: {profile_name}")
        except Exception as e:
            LOGGER.error(f"Failed to save profile: {e}")
            raise

    def get_profile(self, profile_name: str) -> Optional[str]:
        """Get configuration profile data"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT config_data FROM config_profiles WHERE profile_name = ?",
                          (profile_name,))
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            LOGGER.error(f"Failed to get profile: {e}")
            return None

    def list_profiles(self) -> List[str]:
        """List all available profiles"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT profile_name FROM config_profiles ORDER BY profile_name")
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            LOGGER.error(f"Failed to list profiles: {e}")
            return []

    # Performance metrics

    def record_metric(self, job_id: int, metric_name: str, metric_value: float, unit: str = None):
        """Record performance metric"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO performance_metrics (job_id, metric_name, metric_value, unit)
                VALUES (?, ?, ?, ?)
            """, (job_id, metric_name, metric_value, unit))
            self.connection.commit()
        except Exception as e:
            LOGGER.error(f"Failed to record metric: {e}")
            raise

    def get_job_metrics(self, job_id: int) -> List[Dict]:
        """Get all metrics for a job"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM performance_metrics WHERE job_id = ?
                ORDER BY recorded_at
            """, (job_id,))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            LOGGER.error(f"Failed to get job metrics: {e}")
            return []

    # Statistics

    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        try:
            cursor = self.connection.cursor()

            stats = {}

            # Total employees
            cursor.execute("SELECT COUNT(*) FROM employees")
            stats['total_employees'] = cursor.fetchone()[0]

            # Total jobs
            cursor.execute("SELECT COUNT(*) FROM badge_jobs")
            stats['total_jobs'] = cursor.fetchone()[0]

            # Badges by status
            cursor.execute("""
                SELECT status, COUNT(*) as count FROM badges
                GROUP BY status
            """)
            stats['badges_by_status'] = {row[0]: row[1] for row in cursor.fetchall()}

            # Total badges
            cursor.execute("SELECT COUNT(*) FROM badges")
            stats['total_badges'] = cursor.fetchone()[0]

            # Average processing time
            cursor.execute("""
                SELECT AVG(processing_time_ms) FROM badges
                WHERE processing_time_ms IS NOT NULL
            """)
            avg_time = cursor.fetchone()[0]
            stats['avg_processing_time_ms'] = round(avg_time, 2) if avg_time else 0

            return stats

        except Exception as e:
            LOGGER.error(f"Failed to get statistics: {e}")
            return {}

    def get_recent_jobs(self, limit: int = 10) -> List[Dict]:
        """Get recent jobs"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM badge_jobs
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            LOGGER.error(f"Failed to get recent jobs: {e}")
            return []
