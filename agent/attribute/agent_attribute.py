
#-*- coding: utf8 -*-
import os
import urllib2

class agent_attribute:


  def __init__(self, host_ip, port):
    self.demon_host_ip = host_ip
    self.demon_port= port
    self.url_request_prefix = \
    'http://%(host_ip)s:%(port)d/attribute_request_handler?url=%%s' % \
    {'host_ip': self.demon_host_ip, 'port': self.demon_port}
    self.local_path_request_prefix = \
    'http://%(host_ip)s:%(port)d/attribute_request_handler?local_path=%%s' % \
    {'host_ip': self.demon_host_ip, 'port': self.demon_port}


  def get_attribute(self, imageurl, local_path):
    if imageurl <> None:
      url = self.url_request_prefix % imageurl
      response = urllib2.urlopen(url)
    elif local_path <> None:
      url = self.local_path_request_prefix % local_path
      response = urllib2.urlopen(url)
    return response.read()

  def extract_feature(self, image, blob_name, oversample=True):
    try:
      pass
    except Exception as err:
      print('ERROR extract_feature: %s', err)
      return None

