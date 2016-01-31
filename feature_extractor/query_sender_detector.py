
# coding: utf8

import numpy as np
import cPickle as pickle
import urllib2
import json
import sys, os, time

def decode_json(result_dic):
  for cls_name in result_dic['roi_boxes_and_scores'].keys():
    result_dic['roi_boxes_and_scores'][cls_name] = \
      np.asarray(result_dic['roi_boxes_and_scores'][cls_name]).astype(np.float32)
    result_dic['feature_vectors'][cls_name] = \
      np.asarray(result_dic['feature_vectors'][cls_name]).astype(np.float32)
  return result_dic


url_prefix_req = 'http://10.202.4.219:8080/detector_request_handler?url=%s&is_browser=0'

filename = '/storage/product/11st_julia/query_result_skirt.csv'
url_prefix_img = 'http://i.011st.com%s'
entries = [entry.strip().split(';') for entry in open(filename, 'r')]
entries = entries[1:]

#import pdb; pdb.set_trace()
for entry in entries:
  imageurl = url_prefix_img % entry[3]
  url = url_prefix_req % imageurl
  try:
    start_det = time.time()
    response = urllib2.urlopen(url)
    end_det = time.time()
    if response <> None:
      retrieved_items = json.loads(response.read())
      if retrieved_items['result']:
        retrieved_items = decode_json(retrieved_items)
      else: raise Exception
    else:
      print 'No response to url:', url
    print('%s in %f' % (url, end_det - start_det))
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

