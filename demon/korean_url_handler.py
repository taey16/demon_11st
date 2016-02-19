
# -*- coding: UTF-8 -*-

# urlhandler
import urllib3
from urlparse import urlparse
from django.http import HttpResponse
import cgi
import certifi
import PIL.Image
import datetime
import logging
import cStringIO as StringIO
import os

class korean_url_handler:

  def __init__(self):
    num_workers = 1
    self.http = urllib3.PoolManager(
      num_pools=num_workers, 
      cert_reqs='CERT_REQUIRED', 
      ca_certs=certifi.where())


  def parsing_imagedataurl(self, req_url):
    up = urlparse(req_url)
    try:
      head, data = up.path.split(',')
      bits = head.split(';')
        
      data = data.replace('\n', '')
      data = data.replace(' ', '+')
      mime_type = bits[0] if bits[0] else 'text/plain'
      logging("korean_url_handler: mime_type: {}".format(mime_type))
        
      charset, b64 = 'ASCII', False
      for bit in bits:
        if bit.startswith('charset='):
          charset = bit[8:]
        elif bit == 'base64':
          b64 = True
    except ValueError as err:
      return None, None, None, None
    
    return mime_type, charset, b64, data
   
                              
  def getstringbuffer(self, image_url):
    mime_type, _, b64, urldata = self.parsing_imagedataurl(image_url)
    if mime_type is None:
      logging.info("http.request: {} SSS".format(image_url))
      response = self.http.request('GET', image_url, preload_content=True)
      logging.info("http.request: {} EEE".format(image_url))
      remote_response_code = response.status
      if response.status != 200:
        raise Exception("urllib3", 'connection failed, status: {}'.format(response.status))

      logging.info("response.read(): status:{}, headers:{}".format(remote_response_code, response.headers))
      response.read()
      data = response.data
      logging.info("Data Length: {}".format(len(data)))
        
      _, content_disposition = cgi.parse_header(response.headers.get('Content-Disposition', ''))
      content_type = cgi.parse_header(response.headers.get('content-type', ''))
      content_type = content_type[0].lower()
    else:
      if b64:
        data = base64.b64decode(urldata)
      else:
        data = urldata
        content_type = mime_type
       
    logging.info("content-type of {}: {}".format(image_url, content_type))
    if content_type == "image/jpeg" or content_type == "image/jpg":
      req_ext = ".jpg"
    elif content_type == "image/png":
      req_ext = ".png"
    else:
      req_ext = ""
       
    logging.info("req_ext of {}: {}".format(image_url, req_ext))

    string_buffer = StringIO.StringIO(data);
    return string_buffer, data, req_ext


  def get_downloaded_filename(self, file_path, img_ext):
    filename = str(datetime.datetime.now()).replace(' ', '_')
    filename = os.path.join(file_path, '{}.{}'.format(filename, img_ext))
    return filename


  def download_image(self, image_url, file_path='tmp'):
    try:
      string_buffer, img_rawdata, img_ext = \
        self.getstringbuffer(image_url.encode('utf-8'))
      filename = self.get_downloaded_filename(file_path, img_ext)
      with open(filename, 'wb') as img_fp:
        img_fp.write(img_rawdata)
    except Exception as err:
      logging.info('URL Image download error: %s', err)
      return None

    return filename

