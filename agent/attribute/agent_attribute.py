
#-*- coding: utf8 -*-
import os
import urllib, urllib2

class agent_attribute:
  feature_demon_host_ip = '10.202.4.219'
  feature_demon_port= 8080 
  feature_demon_request_prefix = \
    'http://%(host_ip)s:%(port)d/attribute_request_handler?url=%%s' % \
    {'host_ip': feature_demon_host_ip, 'port': feature_demon_port}


  #def __init__(self, exe_command):
  def __init__(self):
    #CUDA_VISIBLE_DEVICES=0 luajit lua/demon/feature_demon_attribute.lua
    #os.system(exe_command)
    pass


  def get_attribute(self, imageurl):
    url = self.feature_demon_request_prefix % imageurl
    response = urllib2.urlopen(url)
    return response.read()

  def extract_feature(self, image, blob_name, oversample=True):
    try:
      pass
    except Exception as err:
      print('ERROR extract_feature: %s', err)
      return None

