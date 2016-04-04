
# -*- coding: UTF-8 -*-
import os
import sys
import datetime
import PIL
from exifutil import exifutil
from korean_url_handler import korean_url_handler
import werkzeug
import numpy as np


class demon_utils:

  UPLOAD_FOLDER = '/storage/enroll'
  host = 'http://10.202.34.211:2596/PBrain/'


  def __init__(self, upload_folder=None):
    if upload_folder <> None:
      self.UPLOAD_FOLDER = upload_folder

      self.exifutils = exifutil()
      self.korean_url_handler = korean_url_handler()


  def download_get_req(self, url):
    filename = self.korean_url_handler.download_image(url, self.UPLOAD_FOLDER)
    assert(os.path.exists(filename))
    local_url = filename.replace('/storage/', self.host)
    return filename, local_url


  def download_post_req(self, imagefile):
    filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
      werkzeug.secure_filename(imagefile.filename)
    filename = os.path.join(self.UPLOAD_FOLDER, filename_)
    imagefile.save(filename)
    image = self.exifutils.open_oriented_im(filename)
    image = PIL.Image.fromarray(np.uint8(image*255))
    image.save(filename)
    local_url = filename.replace('/storage/', self.host)
    return filename, local_url

