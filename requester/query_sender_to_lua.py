
# coding: utf8

import urllib2
import json
import time
import sys

input_url_list = 'demo_example.txt'
urls = [entry.strip() for entry in open(input_url_list, 'r')]
url_prefix = 'http://10.202.35.0:8080/mosaic_request_handler/?query=%s&cate=cate'

#import pdb; pdb.set_trace()
start_total = time.time()
for n, url in enumerate(urls):
  try:
    start_request = time.time()
    # get json object
    response = urllib2.urlopen(url_prefix % url)
    if response <> None:
      # read json object into managable json object in python
      retrieved_items = json.loads(response.read())
      if retrieved_items['result']:
        elapsed_start = time.time() - start_request
        print 'url,', retrieved_items['url']
        #print 'category', retrieved_items['category']
        print 'name', retrieved_items['name']
        print 'score', retrieved_items['score']
        print 'feature', retrieved_items['feature'][0:10]
        print '%06d th sample, elapsed: %.4f msec.' % (n, elapsed_start)
      else: raise Exception
    else:
      print 'No response to url:', url
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
  except ValueError as err:
    print "JSON value error,", err
  except Exception as err:
    print "Unknown error:", err

print 'total elapsed for 2000 samples %.4f' % (time.time() - start_total)

