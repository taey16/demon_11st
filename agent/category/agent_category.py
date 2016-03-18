
#-*- coding: utf8 -*-
import os
import urllib2

class agent_category:


  def __init__(self, host_ip, port):
    self.demon_host_ip = host_ip
    self.demon_port= port
    self.request_prefix = \
      'http://%(host_ip)s:%(port)d/category_request_handler?url=%%s' % \
      {'host_ip': self.demon_host_ip, 'port': self.demon_port}


  def get_category(self, imageurl):
    url = self.demon_request_prefix % imageurl
    response = urllib2.urlopen(url)
    return response.read()


  def extract_feature(self, image, blob_name, oversample=True):
    try:
      pass
    except Exception as err:
      print('ERROR extract_feature: %s', err)
      return None

