# -*- coding: utf-8 -*-
# vim:ts=3:sw=3:expandtab
"""
---------------------------
Copyright (C) 2022
@Authors: Vic Dang
@Date: 22-Mar-22
@Version: 1.0
---------------------------
Usage example:
  - crawl_image.py <options>
"""

import argparse
import urllib.request
import logging
import queue
import sys
import threading
import json
from util import Utilities as ut

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
CONF = '../config/'
POS_MAP = {}


class ImageCrawler(object):
    """
    A class to crawl and download images from URLs.

    Methods:
    - __init__(*args, **kwargs): Initializes ImageCrawler.
    - download_image(url, emp_id): Downloads an image from a given URL and employee ID.
    - start_workers(thread_func, q, workers=None, **kwargs): Starts worker threads for image downloading tasks.
    - start_tasks(q, tasks): Starts image downloading tasks using a queue.
    - thread_func(q_item, thread_no): Function for worker threads to download images.
    - run(): Runs the image crawler.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize ImageCrawler.

        Args:
        - arg (str): An argument (default: None).
        - tasks (list): A list of tasks (default: None).
        - workers (int): Number of worker threads (default: 10).
        - url (str): URL path for images (default: '/images/emp_images/big_new').
        """
        super(ImageCrawler, self).__init__()
        self.arg = kwargs.get('arg', None)
        self.tasks = kwargs.get('tasks', None)
        self.workers = range(int(kwargs.get('workers', 10)))
        self.url = "https://intranet.t%sa.com.vn%s" % ('m', '/images/emp_images/big_new')

    def download_image(self, url, emp_id):
        """
        Download an image from a given URL and employee ID.

        Args:
        - url (str): URL path for images.
        - emp_id (str): Employee ID.
        """
        if self.arg.file_type == 0:
            name, uid, pos = emp_id.split('_')
            logger.info("emp_id :" + emp_id)
        if uid.startswith(('T', 'B')):
            uid = uid[1:]
        # convert uid to int for remove heading zero, eg: 01234 -> 1234
        url = "%s/%s.jpg" % (url, int(uid))
        logger.debug('Downloading: %s' % url)
        local_file = "./img/%s.jpg" % str(uid)
        if self.arg.file_type == 0:
            local_file = "./img/%s_%s_%s_1.jpg" % (name, str(uid), pos)
        try:
            urllib.request.urlretrieve(url, local_file)
            logger.info("Downloaded : %s" % local_file)
        except Exception as err:
            logger.error("Failed to download : %s - %s" % (local_file, url))
            # raise err

    def start_workers(self, thread_func, q, workers=None, **kwargs):
        """
        Start worker threads for image downloading tasks.

        Args:
        - thread_func (function): Function for worker threads to download images.
        - q (queue.Queue): Queue for tasks.
        - workers (range): Range of worker threads (default: self.workers).
        """
        workers = workers if workers else self.workers
        for worker in workers:
            wk = threading.Thread(target=thread_func,
                                  args=(q, worker,),
                                  daemon=True)
            wk.start()

    def start_tasks(self, q, tasks):
        """
        Start image downloading tasks using a queue.

        Args:
        - q (queue.Queue): Queue for tasks.
        - tasks (list): List of tasks to download images.
        """
        for i in tasks:
            i = i.strip()
            q.put(i)
        q.join()

    def thread_func(self, q_item, thread_no):
        """
        Function for worker threads to download images.

        Args:
        - q_item (queue.Queue): Queue item for tasks.
        - thread_no (int): Thread number.
        """
        while True:
            task_item = q_item.get()
            ImageCrawler.download_image(self, self.url, task_item)
            q_item.task_done()
            logger.debug('Thread [%s] is doing [%s]...' %
                         (str(thread_no), str(task_item)))

    def run(self):
        """
        Run the image crawler.
        """
        q = queue.Queue()
        self.start_workers(self.thread_func, q)
        self.start_tasks(q, self.tasks)
        return


def setup_logging(debug=False):
    """
    Setup the logging configuration.

    Args:
    - debug (bool): Debug flag (default: False).
    """
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level,
                        format='%(asctime)s - %(levelname)s %(threadName)s - %('
                               'name)s %(funcName)s %(lineno)d : %('
                               'message)s',
                        stream=sys.stderr,
                        filemode='w')
    global logger
    logger = logging.getLogger('sLogger')


def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Image Crawler')
    parser.add_argument('-w', '--workers', type=int, default=30,
                        help='Number of workers')
    parser.add_argument('-f', '--file-path', type=str, default="./", nargs='?',
                        help='Path to the list IDs file')
    parser.add_argument('-l', '--link', type=str, 
                        default="https://intranet.t%sa.com.vn" % 'm', nargs='?',
                        help='Path to the folder to create mock data')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debug mode')
    return parser.parse_args()


def get_data(file):
    """
    Get data from a file.

    Args:
    - file (str): File path.

    Returns:
    - int: File type (0: excel, 1: other formats).
    - list: List of tasks/data.
    """
    if ut.check_file_type(file) == 'excel':
        data = []
        from openpyxl import load_workbook
        workbook = load_workbook(filename=file)
        sheet = workbook.active
        skip_first_row = True
        for row in sheet.iter_rows(values_only=True):
            if skip_first_row:
                skip_first_row = False
                continue
            uid, name, pos = row[1:4]
            data.append('_'.join([name, str(uid), pos]))
        workbook.close()
        return 0, data
    else:
        with open(file, 'r') as id_list:
            return 1, id_list.readlines()


def main(args):
    """
    Main function to execute the image crawling process.

    Args:
    - args: Command-line arguments.
    """
    args = parse_arguments()
    setup_logging(args.debug)
    f_type, tasks = get_data(args.file_path)
    args.file_type = f_type
    imgc = ImageCrawler(arg=args, tasks=tasks, workers=args.workers)
    imgc.run()
    return


if __name__ == '__main__':
    main(sys.argv[1:])
