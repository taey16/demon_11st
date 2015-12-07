
# coding: utf8

import urllib2
import json
import time
import sys

# input url list file
#input_url_list = 'demo_all.txt.url.txt'
input_url_list = 'demo_example.txt'
# get url list
urls = [entry.strip() for entry in open(input_url_list, 'r')]
# set API prefix
url_prefix = 'http://175.126.56.112:8080/mosaic_request_handler?url=%s'

#import pdb; pdb.set_trace()
start_total = time.time()
for n, url in enumerate(urls):
  try:
    start_request = time.time()
    # get json object
    response = urllib2.urlopen(url_prefix % url)
    # read json object into managable json object in python
    retrieved_items = json.loads(response.read())
    elapsed_start = time.time() - start_request
    print '__org_img_url__, {}'.format(retrieved_items['__org_img_url__'])
    print 'signature', retrieved_items['signature'][0:20]
    print 'feature', retrieved_items['feature'][0:10]
    print '%06d th sample, elapsed: %.4f msec.' % (n, elapsed_start)
    sys.stdout.flush()
  except urllib2.HTTPError, err:
    if err.code == 404:
      print "Page not found!"
    elif err.code == 403:
      print "Access denied!"
    else:
      print "Something happened! Error code", err.code
  except urllib2.URLError, err:
    print "Some other error happened:", err.reason

print 'total elapsed for 2000 samples %.4f' % time.time() - start_total

