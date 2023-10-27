# -*- coding: utf-8 -*-
# vim:ts=3:sw=3:expandtab
"""
---------------------------
Copyright (C) 2022
@Authors: dnnvu.menlo
@Date: 22-Mar-22
@Version: 1.0
---------------------------
 Usage example:
   - crawl_image.py <options>

"""

import urllib.request
import logging
import queue
import sys
import threading
import json

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

class ImageCrawler(object):
   """docstring for ImageCrawler"""

   def __init__(self, *args, **kwargs):
      super(ImageCrawler, self).__init__()
      self.arg = kwargs.get('arg', None)
      self.tasks = kwargs.get('tasks', None)
      self.workers = range(int(kwargs.get('workers', 10)))
      self.url = kwargs.get('url',
                            '/images/emp_images/big_new')

   @staticmethod
   def download_image(url, emp_id):
      url = "%s/%s.jpg" % (url, emp_id)
      local_file = "./img/intra/%s.jpg" % str(emp_id)
      try:
         urllib.request.urlretrieve(url, local_file)
         logger.info("Downloaded : %s" % local_file)
      except Exception as err:
         logger.error("Failed to download : %s - %s" % (local_file, url))
         # raise err

   def start_workers(self, thread_func, q, workers=None, **kwargs):
      workers = workers if workers else self.workers
      for worker in workers:
         wk = threading.Thread(target=thread_func,
                               args=(q, worker,),
                               daemon=True)
         wk.start()

   @staticmethod
   def start_tasks(q, tasks):
      for i in tasks:
         i = i.strip()
         if i.startswith(('T', 'B')):
            i = i[1:]
         q.put(int(i))
      q.join()

   def thread_func(self, q_item, thread_no):
      while True:
         task_item = q_item.get()
         ImageCrawler.download_image(self.url, task_item)
         q_item.task_done()
         logger.debug('Thread [%s] is doing [%s]...' % (str(thread_no),
                                                        str(task_item)))

   def run(self):
      q = queue.Queue()
      self.start_workers(self.thread_func, q)
      self.start_tasks(q, self.tasks)
      return

def setup_logging(debug=False):
   """
   Using to setup the logging configuration
   :param debug: Debug flag
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

def main(args):
   setup_logging(False)
   with open('id_list.txt', 'r') as id_list:
      tasks = id_list.readlines()
   imgc = ImageCrawler(arg=args, tasks=tasks, workers=30)
   imgc.run()
   return

if __name__ == '__main__':
   args = None
   main(args)
