
# coding: utf8

import urllib2
import json

# input url list file
input_url_list = 'demo_all.txt.url.txt'
# get url list
urls = [entry.strip() for entry in open(input_url_list, 'r')]
# set API prefix
url_prefix = 'http://175.126.56.112:8080/mosaic_request_handler?url=%s'

try:
  #import pdb; pdb.set_trace()
  for url in urls:
    # get json object
    response = urllib2.urlopen(url_prefix % url)
    # read json object into managable json object in python
    retrieved_items = json.loads(response.read())
    print '__org_img_url__, {}'.format(retrieved_items['__org_img_url__'])
    print 'signature', retrieved_items['signature']
    print 'feature', retrieved_items['feature']

except urllib2.HTTPError, err:
  if err.code == 404:
    print "Page not found!"
  elif err.code == 403:
    print "Access denied!"
  else:
    print "Something happened! Error code", err.code
except urllib2.URLError, err:
  print "Some other error happened:", err.reason

