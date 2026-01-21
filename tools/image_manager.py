# -*- coding: utf-8 -*-
"""
Image Manager - Handles image availability, downloading, and validation

Authors: Vic Dang
Purpose: Manages image workflow with automatic downloading from internal web
"""

import logging
import os
import re
import urllib.request
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from threading import Thread
import queue

LOGGER = logging.getLogger(__name__)


class ImageManager:
    """
    Manages image workflow including:
    - Checking image availability
    - Downloading missing images
    - Validating image formats
    """

    SUPPORTED_FORMATS = ['.png', '.jpg', '.jpeg', '.bmp']
    
    def __init__(
        self,
        src_path: str,
        base_url: str,
        workers: int = 5,
        timeout: int = 30
    ):
        """
        Initialize ImageManager
        
        :param src_path: Path to source images directory
        :param base_url: Base URL for downloading images (e.g., https://intranet.company.com/images/)
        :param workers: Number of download threads
        :param timeout: Download timeout in seconds
        """
        self.src_path = Path(src_path)
        self.base_url = base_url.rstrip('/')
        self.workers = workers
        self.timeout = timeout
        self.download_queue = queue.Queue()
        self.failed_downloads: Dict[str, str] = {}
        self.successful_downloads: List[str] = []

    def get_employee_id_from_filename(self, filename: str) -> Optional[str]:
        """
        Extract employee ID from filename
        
        Format: {username}_{userid}_{position}_{number}.{ext}
        
        :param filename: Filename to parse
        :return: Employee ID or None if invalid
        """
        name = Path(filename).stem
        parts = name.split('_')
        
        if len(parts) < 3:
            return None
        
        emp_id = parts[1]  # userid
        return emp_id.lstrip('TB')  # Remove prefix if exists

    def file_exists(self, filename: str) -> bool:
        """
        Check if image file exists locally
        
        :param filename: Filename to check
        :return: True if file exists, False otherwise
        """
        file_path = self.src_path / filename
        return file_path.exists() and file_path.is_file()

    def get_missing_images(self, filenames: List[str]) -> List[str]:
        """
        Get list of missing images that need to be downloaded
        
        :param filenames: List of expected filenames
        :return: List of missing filenames
        """
        missing = []
        for filename in filenames:
            if not self.file_exists(filename):
                missing.append(filename)
                LOGGER.warning(f"Missing image: {filename}")
            else:
                LOGGER.debug(f"Image found: {filename}")
        
        return missing

    def build_download_url(self, emp_id: str) -> str:
        """
        Build download URL from employee ID
        
        :param emp_id: Employee ID (numeric part without prefix)
        :return: Full download URL
        """
        # Remove leading zeros and convert to int then back to string
        emp_id_clean = str(int(emp_id))
        url = f"{self.base_url}/{emp_id_clean}.jpg"
        return url

    def download_single_image(self, filename: str, emp_id: str) -> Tuple[bool, str]:
        """
        Download single image from web
        
        :param filename: Target filename
        :param emp_id: Employee ID
        :return: (success: bool, message: str)
        """
        try:
            url = self.build_download_url(emp_id)
            file_path = self.src_path / filename
            
            LOGGER.info(f"Downloading: {url} → {file_path}")
            
            urllib.request.urlretrieve(
                url,
                str(file_path),
                timeout=self.timeout
            )
            
            LOGGER.info(f"Successfully downloaded: {filename}")
            self.successful_downloads.append(filename)
            return True, f"Downloaded: {filename}"
            
        except urllib.error.URLError as err:
            msg = f"URL error for {filename}: {err}"
            LOGGER.error(msg)
            self.failed_downloads[filename] = msg
            return False, msg
            
        except urllib.error.HTTPError as err:
            msg = f"HTTP {err.code} for {filename}: {err.reason}"
            LOGGER.error(msg)
            self.failed_downloads[filename] = msg
            return False, msg
            
        except Exception as err:
            msg = f"Failed to download {filename}: {str(err)}"
            LOGGER.error(msg)
            self.failed_downloads[filename] = msg
            return False, msg

    def _worker_thread(self, thread_id: int) -> None:
        """
        Worker thread for downloading images
        
        :param thread_id: Thread identifier
        """
        while True:
            item = self.download_queue.get()
            
            if item is None:  # Sentinel value to stop
                LOGGER.debug(f"Thread {thread_id} stopping")
                self.download_queue.task_done()
                break
            
            filename, emp_id = item
            LOGGER.debug(f"Thread {thread_id} processing: {filename}")
            self.download_single_image(filename, emp_id)
            self.download_queue.task_done()

    def download_missing_images(
        self,
        filenames: List[str],
        use_threading: bool = True
    ) -> Dict[str, object]:
        """
        Download all missing images
        
        :param filenames: List of filenames to download
        :param use_threading: Use multi-threading for downloads
        :return: Dictionary with download statistics
        """
        missing = self.get_missing_images(filenames)
        
        if not missing:
            LOGGER.info("All images are available locally")
            return {
                'total': len(filenames),
                'missing': 0,
                'downloaded': 0,
                'failed': 0,
                'skipped': len(filenames)
            }
        
        LOGGER.info(f"Found {len(missing)} missing images, starting download...")
        self.successful_downloads.clear()
        self.failed_downloads.clear()
        
        if use_threading and len(missing) > 1:
            return self._download_threaded(missing)
        else:
            return self._download_sequential(missing)

    def _download_sequential(self, filenames: List[str]) -> Dict[str, object]:
        """
        Download images sequentially
        
        :param filenames: List of filenames to download
        :return: Download statistics
        """
        for filename in filenames:
            emp_id = self.get_employee_id_from_filename(filename)
            if emp_id:
                self.download_single_image(filename, emp_id)
        
        return self._get_download_stats(filenames)

    def _download_threaded(self, filenames: List[str]) -> Dict[str, object]:
        """
        Download images using multi-threading
        
        :param filenames: List of filenames to download
        :return: Download statistics
        """
        # Start worker threads
        threads = []
        for i in range(min(self.workers, len(filenames))):
            t = Thread(target=self._worker_thread, args=(i,), daemon=False)
            t.start()
            threads.append(t)
        
        # Queue download tasks
        for filename in filenames:
            emp_id = self.get_employee_id_from_filename(filename)
            if emp_id:
                self.download_queue.put((filename, emp_id))
        
        # Wait for queue to be processed
        self.download_queue.join()
        
        # Stop worker threads
        for _ in threads:
            self.download_queue.put(None)
        
        for t in threads:
            t.join()
        
        return self._get_download_stats(filenames)

    def _get_download_stats(self, expected_files: List[str]) -> Dict[str, object]:
        """
        Calculate download statistics
        
        :param expected_files: List of expected files
        :return: Statistics dictionary
        """
        return {
            'total': len(expected_files),
            'missing': len(self.get_missing_images(expected_files)),
            'downloaded': len(self.successful_downloads),
            'failed': len(self.failed_downloads),
            'skipped': len(expected_files) - len(self.get_missing_images(expected_files)) - len(self.successful_downloads),
            'failed_files': self.failed_downloads,
            'successful_files': self.successful_downloads
        }

    def validate_image_format(self, filename: str) -> bool:
        """
        Validate image file format
        
        :param filename: Filename to validate
        :return: True if valid format
        """
        ext = Path(filename).suffix.lower()
        return ext in self.SUPPORTED_FORMATS

    def get_local_images(self) -> List[str]:
        """
        Get list of all local images in source directory
        
        :return: List of image filenames
        """
        if not self.src_path.exists():
            return []
        
        images = []
        for file in self.src_path.iterdir():
            if file.is_file() and self.validate_image_format(file.name):
                images.append(file.name)
        
        return images

    def cleanup_duplicates(self) -> None:
        """Remove duplicate images keeping only the latest"""
        images = self.get_local_images()
        seen = {}
        
        for img in images:
            name = Path(img).stem
            parts = name.split('_')
            
            if len(parts) >= 3:
                key = '_'.join(parts[:3])  # username_userid_position
                
                if key in seen:
                    # Remove older duplicate (lower number)
                    old_img = seen[key]
                    old_file = self.src_path / old_img
                    if old_file.exists():
                        old_file.unlink()
                        LOGGER.info(f"Removed duplicate: {old_img}")
                
                seen[key] = img
