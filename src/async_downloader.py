# -*- coding: utf-8 -*-
"""
Async Image Downloader - Multi-threaded/async downloads with progress tracking

Authors: Vic Dang
Purpose: Efficient image downloading with progress callbacks and retry logic
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import List, Dict, Callable, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import urllib.request
import urllib.error

LOGGER = logging.getLogger(__name__)


@dataclass
class DownloadTask:
    """Represents a single download task"""
    task_id: str
    url: str
    destination: Path
    emp_id: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    timeout: int = 30

    def __str__(self) -> str:
        return f"Download({self.task_id}, {self.destination.name})"


@dataclass
class DownloadResult:
    """Result of a download operation"""
    task_id: str
    success: bool
    destination: Path
    file_size_bytes: int = 0
    download_time_ms: int = 0
    error_message: str = None
    retry_count: int = 0

    def __str__(self) -> str:
        status = "✅" if self.success else "❌"
        return f"{status} {self.destination.name} ({self.file_size_bytes} bytes, {self.download_time_ms}ms)"


class AsyncDownloadManager:
    """Manages asynchronous image downloads with progress tracking"""

    def __init__(self, max_workers: int = 5, timeout: int = 30):
        """
        Initialize download manager

        :param max_workers: number of parallel download threads
        :param timeout: download timeout in seconds
        """
        self.max_workers = max_workers
        self.timeout = timeout
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.progress_callback: Optional[Callable] = None
        self.results: List[DownloadResult] = []
        self.active_downloads: Dict[str, float] = {}

    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """
        Set callback for progress updates

        :param callback: function(current, total, message) called for progress
        """
        self.progress_callback = callback

    def _report_progress(self, current: int, total: int, message: str = ""):
        """Report progress via callback"""
        if self.progress_callback:
            try:
                self.progress_callback(current, total, message)
            except Exception as e:
                LOGGER.warning(f"Progress callback error: {e}")

    def _download_file(self, task: DownloadTask) -> DownloadResult:
        """
        Download single file with retry logic

        :param task: download task
        :return: download result
        """
        start_time = time.time()

        try:
            # Ensure destination directory exists
            task.destination.parent.mkdir(parents=True, exist_ok=True)

            # Attempt download with retries
            for attempt in range(task.max_retries + 1):
                try:
                    LOGGER.debug(f"Downloading {task.url} → {task.destination} (attempt {attempt + 1})")

                    # Add timeout to download
                    with urllib.request.urlopen(task.url, timeout=task.timeout) as response:
                        with open(task.destination, 'wb') as out_file:
                            out_file.write(response.read())

                    # Get file size
                    file_size = task.destination.stat().st_size
                    elapsed_ms = int((time.time() - start_time) * 1000)

                    LOGGER.info(f"Downloaded {task}: {file_size} bytes in {elapsed_ms}ms")

                    return DownloadResult(
                        task_id=task.task_id,
                        success=True,
                        destination=task.destination,
                        file_size_bytes=file_size,
                        download_time_ms=elapsed_ms,
                        retry_count=attempt
                    )

                except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
                    if attempt < task.max_retries:
                        wait_time = 2 ** attempt  # Exponential backoff
                        LOGGER.warning(f"Download failed (attempt {attempt + 1}): {e}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise

        except Exception as e:
            elapsed_ms = int((time.time() - start_time) * 1000)
            error_msg = f"Failed to download {task.url}: {str(e)}"
            LOGGER.error(error_msg)

            # Clean up partial file
            if task.destination.exists():
                try:
                    task.destination.unlink()
                except Exception as cleanup_error:
                    LOGGER.warning(f"Failed to clean up partial file: {cleanup_error}")

            return DownloadResult(
                task_id=task.task_id,
                success=False,
                destination=task.destination,
                download_time_ms=int((time.time() - start_time) * 1000),
                error_message=error_msg,
                retry_count=task.max_retries
            )

    async def _async_download_wrapper(self, task: DownloadTask, loop) -> DownloadResult:
        """Wrapper to run download in thread pool"""
        return await loop.run_in_executor(self.executor, self._download_file, task)

    async def download_batch_async(self, tasks: List[DownloadTask]) -> List[DownloadResult]:
        """
        Download multiple files asynchronously

        :param tasks: list of download tasks
        :return: list of download results
        """
        loop = asyncio.get_event_loop()
        self.results = []
        total = len(tasks)

        # Create coroutines for all downloads
        coroutines = [self._async_download_wrapper(task, loop) for task in tasks]

        # Execute downloads with progress tracking
        completed = 0
        for coro in asyncio.as_completed(coroutines):
            result = await coro
            completed += 1
            self.results.append(result)

            status_msg = f"Downloaded {completed}/{total}: {result.destination.name}"
            self._report_progress(completed, total, status_msg)
            LOGGER.info(status_msg)

        return self.results

    def download_batch_sync(self, tasks: List[DownloadTask]) -> List[DownloadResult]:
        """
        Download multiple files synchronously (easier API)

        :param tasks: list of download tasks
        :return: list of download results
        """
        self.results = []
        total = len(tasks)

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self.download_batch_async(tasks))

    def get_statistics(self) -> Dict:
        """Get download statistics"""
        successful = sum(1 for r in self.results if r.success)
        failed = len(self.results) - successful
        total_size = sum(r.file_size_bytes for r in self.results if r.success)
        total_time = sum(r.download_time_ms for r in self.results)
        avg_time = total_time / len(self.results) if self.results else 0

        return {
            'total_downloads': len(self.results),
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / len(self.results) * 100) if self.results else 0,
            'total_size_bytes': total_size,
            'total_time_ms': total_time,
            'avg_time_ms': avg_time,
            'results': self.results
        }

    def close(self):
        """Shutdown executor"""
        self.executor.shutdown(wait=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class DownloadScheduler:
    """Manages download scheduling and prioritization"""

    def __init__(self, manager: AsyncDownloadManager):
        """
        Initialize scheduler

        :param manager: AsyncDownloadManager instance
        """
        self.manager = manager
        self.queue: List[DownloadTask] = []
        self.priority_queue: List[DownloadTask] = []

    def add_task(self, task: DownloadTask, priority: int = 0):
        """
        Add download task

        :param task: download task
        :param priority: task priority (higher = execute first)
        """
        if priority > 0:
            self.priority_queue.append(task)
        else:
            self.queue.append(task)
        LOGGER.debug(f"Added download task: {task}")

    def add_tasks(self, tasks: List[DownloadTask], priority: int = 0):
        """Add multiple tasks"""
        for task in tasks:
            self.add_task(task, priority)

    def get_scheduled_tasks(self) -> List[DownloadTask]:
        """Get all scheduled tasks in priority order"""
        # Sort by priority (higher first), then by task_id
        combined = self.priority_queue + self.queue
        return sorted(combined, key=lambda t: t.task_id)

    def execute(self) -> Dict:
        """Execute all scheduled downloads"""
        tasks = self.get_scheduled_tasks()
        LOGGER.info(f"Starting download of {len(tasks)} tasks")

        # Execute downloads
        results = self.manager.download_batch_sync(tasks)

        # Clear queues
        self.queue.clear()
        self.priority_queue.clear()

        return self.manager.get_statistics()

    def __len__(self) -> int:
        return len(self.queue) + len(self.priority_queue)


# Example usage and testing
def create_sample_tasks(base_url: str, dest_dir: Path, count: int = 5) -> List[DownloadTask]:
    """Create sample download tasks for testing"""
    tasks = []
    for i in range(count):
        task = DownloadTask(
            task_id=f"task_{i:03d}",
            url=f"{base_url}/image_{i}.png",
            destination=dest_dir / f"image_{i}.png",
            emp_id=f"EMP{i:03d}"
        )
        tasks.append(task)
    return tasks
