
# coding: utf8

import numpy as np
import cPickle as pickle
import urllib2
import json
import sys, os, time
PJT_ROOT = '/work'
PJT_NAME = '{}/demon_11st/'.format(PJT_ROOT)
INDEXER_ROOT = '{}/indexer'.format(PJT_NAME)
UTILS_ROOT = '{}/utils'.format(PJT_NAME)
sys.path.insert(0, INDEXER_ROOT)
sys.path.insert(0, UTILS_ROOT)
from indexer import indexer
from parser_utils import parser_utils

url_prefix = 'http://10.202.35.0:8081/mosaic_request_handler/?query=%s&cate=cate'
DATASET_ROOT = '/storage/product'

INPUT_FILENAME = '{}/demo_{}.txt'.format(
  '11st_julia', category_no[current_category])
OUTPUT_FILENAME = \
  '/storage/product/11st_julia/demo_{}.txt.wrap_size0.det16.pickle'.format(
    category_no[current_category])

#import pdb; pdb.set_trace()
start_total = time.time()
#import pdb; pdb.set_trace()
meta_filename = '{}/{}'.format(DATASET_ROOT, INPUT_FILENAME)
parser = parser_utils()
meta = parser.parse(meta_filename)
for n, item in enumerate(meta):
  try:
    prd_no = item['__prd_no__']
    fname  = \
      '/userdata2/index_11st_20151020/october_11st_imgdata/{}.jpg'.format(prd_no)
    object_roi = item['__object_roi__'].strip().split(',')
    category_id = item['__mctgr_no__']
    roi = parser.get_roi_meta_dic(object_roi)
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

