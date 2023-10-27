# -*- coding: utf-8 -*-
# vim:ts=3:sw=3:expandtab
"""
 - Authors: Vic Dang
 - Skype: traxanh_dl
 - Usage example:
   + python execute.py -d -v exec
"""

import argparse
import glob
import json
import logging.config
import os
import re
import time
import pathlib
import sys
import unicodedata
from argparse import ArgumentDefaultsHelpFormatter as Formatter

import cv2
import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFont


logger = logging.getLogger()
CUR_PATH = pathlib.Path().resolve()
config = None

class ImageSizeException(Exception):
   """ImageSizeException"""
   pass

class UserInfoException(Exception):
   """UserInfoException"""
   pass

class Utility(object):
   """docstring for Utility"""

   @staticmethod
   def get_config():
      try:
         from configparser import ConfigParser
      except ImportError:
         from ConfigParser import ConfigParser  # ver. < 3.0
      # instantiate
      config = ConfigParser()
      # parse existing file
      config.read('./config.ini')
      return config

   @staticmethod
   def validate(string, regex):
      """
      Use for validating a string
      :param string: input string
      :param regex: regular expression to verify the string
      :return:
      """
      result = ""
      if re.search(regex, string):
         result = string
      else:
         logger.error("[{}] is not match [{}]".format(string, regex))
      return result

   @staticmethod
   def convert_img(input_img):
      """
      Convert image
      :param input_img: input image
      :return: converted image
      """
      return cv2.imdecode(np.fromfile(input_img, dtype=np.uint8), -1)

   @staticmethod
   def countdown(due_time):
      """
      Used to countdown when processing
      :param due_time: due time
      """
      logger.debug("Couting down for %s" % due_time)
      while due_time:
         mins, secs = divmod(due_time, 60)
         timeformat = '{:02d}:{:02d}'.format(mins, secs)
         print(timeformat, end='\r')
         time.sleep(1)
         due_time -= 1

   @staticmethod
   def check_folder(folders):
      """
      Prepare required folders, including create folders and remove trunks
      :param folders: Target folder(s)
      """
      for folder in folders:
         if not os.path.isdir(folder):
            logger.debug("Making dir: %s" % folder)
            os.mkdir(folder)
         else:
            files = glob.glob(folder)
            for f in files:
               logger.debug("Removing: %s" % f)
               os.remove(f)

   @staticmethod
   def ResizeWithAspectRatio(image, width=None, height=None,
                             inter=cv2.INTER_AREA):
      """
      ResizeWithAspectRatio
      :param image:
      :param width:
      :param height:
      :param inter:
      :return:
      """
      (h, w) = image.shape[:2]
      if width is None and height is None:
         return image
      if width is None:
         r = height / float(h)
         dim = (int(w * r), height)
      else:
         r = width / float(w)
         dim = (width, int(h * r))

      return cv2.resize(image, dim, interpolation=inter)

class ImageMaker(object):
   """docstring for ImageMaker"""
   def __init__(self, name, arg, conf):
      super(ImageMaker, self).__init__()
      self.arg = arg
      self.name = name
      self.src_path = os.path.join(CUR_PATH, arg.src_path)
      self.des_path = os.path.join(CUR_PATH, arg.des_path)
      self.tmp_path = os.path.join(CUR_PATH, conf.get("general", "tmppath"))
      self.template = os.path.join(CUR_PATH, arg.template)
      self.debug = arg.debug or False
      self.img_prefix = conf.get("general", "imgprefix")
      self.tpl_avata_x = conf.getint("template", "avatax")
      self.tpl_avata_y = conf.getint("template", "avatay")
      self.tpl_avata_w = conf.getint("template", "avataw")
      self.tpl_avata_h = conf.getint("template", "avatah")
      self.tpl_w = conf.getint("template", "width")
      self.tpl_h = conf.getint("template", "height")
      self.conf = conf
      self.base_text_size = self.conf.getint("general", "basetextsize")
      with open("positions.json", "r") as pos_file:
         self.positions = json.load(pos_file)
      self.re_name = "^[\w\.\- ]+$"
      self.re_id = "^[\w]?[\d]+$"

      self.img = self.img_resized = self.img_cropt = self.bg_img = None
      self.user_pos = self.positions["E"]
      self.user_name = self.user_id = ""
      self.img_num = 1

   def get_focus_position(self, input_img):
      """
      Used to detect faces in the image then return the focus position
      :param input_img: The input image
      :return: Focus position of the image (x, y)
      """
      face_cascade = cv2.CascadeClassifier(
            "Haar Cascade/haarcascade_frontalface_default.xml")
      image = Utility.convert_img(input_img)
      gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray_image,
                                            # scaleFactor=1.2,
                                            scaleFactor=self.conf.getfloat(
                                                      "avata", "scalefactor"),
                                            minNeighbors=3,
                                            minSize=(30, 30),
                                            maxSize=(200, 200),
                                            flags=cv2.CASCADE_SCALE_IMAGE)

      logger.info("Found {0} faces!".format(len(faces)))
      x = y = 0
      # when face(s) detected
      if len(faces):
         # Track the base position (of the very first face)
         a, b, c, d = faces[0]
         for (i, j, w, h) in faces:
            logger.debug("Detected face : [{},{},{},{}]".format(i, j, w, h))
            c = int((c + w) / 2)
            d = int((d + h) / 2)
            a = int((a + i) / 2)
            b = int((b + j) / 2)
            x = a + int(c / 2)
            y = b + int(d / 2)
            if self.arg.debug:
               cv2.rectangle(image,
                             (i + int(w / 2), j + int(h / 2)),
                             (i + int(w / 2) + 2, j + int(h / 2) + 2),
                             (0, 200, 100), 2)
               cv2.rectangle(image, (i, j), (i + w, j + h), (0, 200, 100), 2)
               cv2.rectangle(image, (x, y), (x + 2, y + 2), (0, 255, 255), 2)
      if self.debug:
         resize = Utility.ResizeWithAspectRatio(image, height=1024)
         cv2.imshow("Faces found", resize)
         cv2.imwrite(self.tmp_path + "faces_" + str(self.name),
                     image)
         if self.arg.test and self.arg.verbose:
            cv2.waitKey(0)
      logger.debug("Focus coordinate : [{},{}]".format(x, y))
      return x, y

   @staticmethod
   def convert_images(src_path, des_path):
      """
      Convert Images
      :param src_path: Source path
      :param des_path: Desination path
      """
      files = []
      format_list = ['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG']
      logger.debug(os.listdir(src_path))
      f = [fi for fi in os.listdir(src_path) if os.path.isfile(src_path + fi)]
      logger.debug("File List : %s" % [item for item in f])
      for file in f:
         if any(s for s in format_list if s in file):
            files.append(u'{}'.format(file))

      for f in files:
         # name = f.split(".")[0].replace(" ", "-")
         name = f.split(".")[0]
         file_name = os.path.join(src_path, f)
         logger.info("Converting : %s to PNG format ..." % file_name)
         im = Image.open(file_name).convert("RGBA")
         im.save(des_path + name + '.png', format="png")

   def correct_img(self):
      """
      Correct the image
      """
      orientation = 274  # get 274 through upper loop
      try:
         exif = self.img._getexif()
         if exif:
            exif = dict(exif.items())
            if exif[orientation] == 3:
              self.img.rotate(180, expand=True)
            elif exif[orientation] == 6:
              self.img.rotate(270, expand=True)
            elif exif[orientation] == 8:
              self.img.rotate(90, expand=True)
      except Exception as err:
         logger.error(err)
         # There is AttributeError: _getexif sometimes.
         pass

   def resize_img(self):
      """
      Resize image
      :return:
      """
      img_w, img_h = self.img.size
      logger.info("Width: %f, Height: %f" % (img_w, img_h))
      basewidth = self.tpl_avata_w + self.conf.getint("template", "padding")
      if img_h >= img_w:
         wpercent = (basewidth / float(img_w))
         hsize = int((float(img_h) * float(wpercent)))
         self.img_resized = self.img.resize((basewidth, hsize),
                                            Image.ANTIALIAS)
      else:
         hpercent = (basewidth / float(img_h))
         wsize = int((float(img_w) * float(hpercent)))
         self.img_resized = self.img.resize((wsize, basewidth),
                                            Image.ANTIALIAS)
      # cropped_example = cropped_example.resize((basewidth,hsize), Image.ANTIALIAS)
      logger.debug("Resized image: %f x %f" % self.img_resized.size)
      self.img_resized.save(self.tmp_path + self.name, format="png")

   def crop_img(self):
      """
      Crop image
      """
      basewidth = self.tpl_avata_w + self.conf.getint("template", "padding")
      x, y = self.get_focus_position(self.tmp_path + self.name)
      img_r_w, img_r_h = self.img_resized.size
      if img_r_w < basewidth or img_r_h < basewidth:
         raise ImageSizeException("Image is too small, Please try another.")
      base_w = basewidth/2
      if x <= 0 and y <= 0:
         x = int(img_r_w / 2)
         y = int(img_r_h / 2)
      else:
         if x - base_w <= 0:
            x = base_w
         elif x + base_w > img_r_w:
            x = img_r_w - base_w
         if y - base_w <= 0:
            y = base_w
         elif y + base_w > img_r_h:
            y = base_w
      correct_x, correct_y = x - base_w, y - base_w
      correct_w, correct_h = basewidth + correct_x, basewidth + correct_y
      logger.debug("\nx:{}, y:{}\nc_x:{}, c_y:{}\nw:{}, h:{}".format(
            x, y, correct_x, correct_y, basewidth, basewidth))
      draw = ImageDraw.Draw(self.img_resized)
      if self.debug:
         draw.rectangle([correct_x, correct_y, correct_w, correct_h], width=3,
                        outline="#0000ff")
      self.img_cropt = self.img_resized.crop((correct_x, correct_y,
                                              correct_w, correct_h))
      logger.debug("Cropt image: %f x %f" % self.img_cropt.size)
      if self.arg.debug or self.arg.test:
         self.img_cropt.save(self.tmp_path + "cr_" + self.name, format="png")

   def parse_user_info(self):
      """
      Parse user information
      Parse user information
      :return: 
      """
      img_info_arr = self.name.split(".")[0].split("_")
      self.user_name = Utility.validate(img_info_arr[0].strip(),
                                        self.re_name)
      if self.user_name == 0:
         raise UserInfoException("User name not found!")
      self.user_pos = img_info_arr[1].capitalize()
      if self.user_pos.strip().upper() in self.positions:
         self.user_pos = self.positions[self.user_pos.strip().upper()]
         logger.info("pos: {}".format(self.user_pos))
      else:
         logger.error(
            "[{}] is not in [{}]".format(self.user_pos, self.positions))
         raise UserInfoException("User position is incorrect!")
      self.user_id = Utility.validate(img_info_arr[2].strip(), self.re_id)
      if self.user_id == 0:
         raise UserInfoException("User ID not found!")
      if len(img_info_arr) == 4:
         self.img_num = img_info_arr[3]

   def parse_qr_code(self):
      """
      Make QR code
      """
      # Make RQ code
      qr = qrcode.QRCode(version=self.conf.getint("qrcode", "version"),
                         error_correction=qrcode.constants.ERROR_CORRECT_L,
                         box_size=self.conf.getint("qrcode", "boxsize"),
                         border=self.conf.getint("qrcode", "border"))
      name = unicodedata.normalize('NFKD', self.user_name).encode('ascii', 'ignore')
      img_info = "Fullname: %s,Position: %s, Badge_Id: %s, Company: %s" % (name, self.user_pos, self.user_id, "www.tmasolutions.com")
      logger.info("info: {}".format(img_info))
      if self.arg.qr_text:
         qr_img = qrcode.make(self.arg.qr_text)
      else:
         qr.add_data(img_info)
         qr.make(fit=self.conf.get("qrcode", "fit"))
         qr_img = qr.make_image(fill_color=self.conf.get("qrcode",
                                                         "fillcolor"),
                                back_color=self.conf.get("qrcode",
                                                         "backcolor"))
      qrx = self.conf.getint("qrcode", "qrx")
      qry = self.conf.getint("qrcode", "qry")
      self.bg_img.paste(qr_img, (qrx, qry), mask=qr_img)

   def execute(self):
      """
      Execute image maker
      :return:
      """
      try:
         logger.info("Processing Image: %s" % self.name)
         template_img = Image.open(self.template, 'r')
         tpl_w, tpl_h = template_img.size

         self.img = Image.open(self.src_path + self.name, 'r').convert(
               "RGBA")
         curr_y = 0.0
         self.correct_img()
         self.resize_img()
         self.crop_img()
         # Make background
         self.bg_img = Image.new('RGBA', (tpl_w, tpl_h), self.conf.get(
               "general", "backgroundcolor"))
         img_cropt_w, img_cropt_h = self.img_cropt.size
         img_cropt_pos = (int(self.tpl_avata_x - (img_cropt_w / 2)),
                          int(self.tpl_avata_y - (img_cropt_h / 2)))
         self.parse_user_info()
         if self.arg.verbose:
            self.img_cropt.save(self.tmp_path + self.user_id + ".png",
                                format="png")
         self.bg_img.paste(self.img_cropt, img_cropt_pos)
         if self.arg.test:
            template_img.putalpha(125)
         self.bg_img.paste(template_img, (0, 0), mask=template_img)
         self.parse_qr_code()
         draw = ImageDraw.Draw(self.bg_img)

         curr_y += self.tpl_avata_y + img_cropt_pos[1]
         th = self.conf.getint("username", "toppad")
         if self.user_name:
            curr_y += th
            if not self.arg.auto_size:
               size = self.conf.getint("username", "size")
            else:
               size = self.base_text_size
            n_size = size
            while True:
               font = ImageFont.truetype(os.path.join(CUR_PATH,
                                                      self.conf.get(
                                                            "username",
                                                            "font")), n_size)
               msg = self.user_name.upper().strip()
               tw, th = draw.textsize(msg, font=font)
               logger.info("info: {} {} {}".format(msg, tw, th))
               if tw < (tpl_w - 50):
                  break
               else:
                  n_size = n_size - 5
            draw.text(((tpl_w - tw) / 2, curr_y), msg, self.conf.get(
                  "username", "color"), font=font)

         if self.user_pos:
            curr_y += th + self.conf.getint("position", "toppad")
            if not self.arg.auto_size:
               size = self.conf.getint("position", "size")
            else:
               size = self.base_text_size - 10
            font = ImageFont.truetype(os.path.join(CUR_PATH, self.conf.get(
                                                            "position",
                                                            "font")), size)
            msg = self.user_pos.strip()
            tw, th = draw.textsize(msg, font=font)
            draw.text(((tpl_w - tw) / 2, curr_y), msg, self.conf.get(
                  "position", "color"), font=font)

         if self.user_id:
            curr_y += th + self.conf.getint("userid", "toppad")
            if not self.arg.auto_size:
               size = self.conf.getint("userid", "size")
            else:
               size = self.base_text_size - 15
            font = ImageFont.truetype(os.path.join(CUR_PATH, self.conf.get(
                                                            "userid",
                                                            "font")), size)
            msg = "ID: " + self.user_id.strip()
            tw, _ = draw.textsize(msg, font=font)
            draw.text(((tpl_w - tw) / 2, curr_y), msg,
                      self.conf.get("userid", "color"), font=font)

         # Saved in the same relative location
         self.bg_img.save(self.des_path + self.img_prefix + "-" +
                          self.user_name + "_" + self.user_pos + "_" +
                          self.user_id + "_" + str(self.img_num) + ".png",
                          format="png")

      except IOError as error:
         logger.error("Error: %s" % error)

def add_args(parser, action='exec'):
   """
   :param parser:
   :param action:
   """
   if action in ['exec']:
      parser.add_argument('-c', '--convert',
                          action='store_true', default=False,
                          help='Convert image to PNG format')
      parser.add_argument('--check-path',
                          action='store_true', default=False,
                          help='Check out put')
      parser.add_argument('-s', '--src-path',
                          default=config.get("general", "srcpath"),
                          help='Path of the source folder')
      parser.add_argument('-f', '--des-path',
                          default=config.get("general", "despath"),
                          help='Path of the destination folder')
      parser.add_argument('-t', '--template',
                          default=config.get("template", "filename"),
                          help='Template file name')
      parser.add_argument('-q', '--qr-text',
                          help='RQ code text')
      parser.add_argument('-a', '--auto-size',
                          action='store_true', default=True,
                          help='Auto size for text')
      parser.add_argument('-l', '--loop',
                          type=bool, default=False,
                          help='Lopping the process')
      parser.add_argument('-i', '--interval',
                          default=config.get('general', 'interval'),
                          help='Interval for looping the process')

def parse_cli():
   """
   :return:
   """
   parser = argparse.ArgumentParser(description=__doc__.strip(),
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('-d', '--debug', action='store_true')
   parser.add_argument('--test', action='store_true')
   parser.add_argument('-v', '--verbose', action='store_true')

   subparsers = parser.add_subparsers(help='Subcommand help', dest='action')
   add_args(subparsers.add_parser('exec', formatter_class=Formatter,
                                  help='Full Execution'), 'exec')
   return parser.parse_args()

def setup_logging(debug=False):
   """
   :param debug:
   """
   if debug:
      log_level = logging.DEBUG
   else:
      log_level = logging.INFO
   # logging.config.fileConfig('pictool.conf', disable_existing_loggers=True,
   #                           defaults={'logfilename': 'pictool.log'})
   # logging.getLogger().setLevel(log_level)
   logging.basicConfig(level=log_level,
                       format='%(asctime)s %(levelname)s %(funcName)s %('
                              'lineno)d : %(message)s',
                       stream=sys.stderr,
                       filemode='w')
   global logger
   logger = logging.getLogger('sLogger')

def main(args, config):
   """
   Main processing
   :return:
   """
   # path = "//10.250.193.251/Softs/tmp/new padge/Dot 2 2019"
   # out = "//10.250.193.251/Softs/tmp/new padge/Badge_by_tool/"
   files = []
   src_path = os.path.join(CUR_PATH, args.src_path)
   des_path = os.path.join(CUR_PATH, args.des_path)
   tmp_path = os.path.join(CUR_PATH, config.get("general", "tmppath"))
   cv_path = os.path.join(CUR_PATH, config.get("general", "convertedpath"))
   format_list = ['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG']

   if args.convert:
      ImageMaker.convert_images(src_path, cv_path)
      args.src_path = config.get("general", "convertedpath")
      src_path = cv_path
   if args.check_path:
      Utility.check_folder([src_path, des_path, tmp_path])

   for r, d, f in os.walk(src_path):
      for file in f:
         if any(s for s in format_list if s in file):
            files.append(file)
   logger.debug("Exec file list: %s" % [item for item in files])

   count = 0
   while True:
      start = time.time()
      for file_name in files:
         count = count + 1
         logger.info("Executing: %s" % file_name)
         img_maker = ImageMaker(file_name, args, config)
         img_maker.execute()
      end = time.time()
      logger.info("Generated [" + str(count) + " "
                  "items] in [" + str(end - start) + "] seconds...")
      if not args.loop:
         return
      Utility.countdown(int(args.interval))

if __name__ == "__main__":
   config = Utility.get_config()
   args = parse_cli()
   setup_logging(args.debug)
   main(args, config)
   # try:
   #    logging.debug('Execute with arguments :')
   #    logging.debug(args)
   #    main(args, config)
   # except Exception as err:
   #    logging.error('Error performing action: %s, %s' % (args.action, err))
