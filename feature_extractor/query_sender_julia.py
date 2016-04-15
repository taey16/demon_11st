
# coding: utf8

import numpy as np
import cPickle as pickle
#import h5py
import urllib2
import json
import sys, os, time
sys.path.append('/works/demon_11st/indexer')
from indexer import indexer

def encode_json(result_dic):
  for key in result_dic['roi'].keys():
    result_dic['roi'][key] = result_dic['roi'][key].tolist()
    result_dic['feature'][key] = result_dic['feature'][key].tolist()
  result_json = json.dumps(result_dic)
  return result_json

def decode_json(result_dic):
  for key in result_dic['roi'].keys():
    result_dic['roi'][key] = \
      np.asarray(result_dic['roi'][key]).astype(np.float32)
    result_dic['feature'][key] = \
      np.asarray(result_dic['feature'][key]).astype(np.float32)
  return result_dic

bins = np.array([0],dtype=np.uint64)


url_prefix_req = 'http://10.202.35.109:8081/julia?url=%s'

filename = \
  '/storage/attribute/PBrain_tshirts_shirts_blous_knit_jacket_onepiece_skirts_coat_cardigan_vest_from0.csv'
  #'/storage/attribute/PBrain_tshirts_shirts_blous_knit_jacket_onepiece_skirts_coat_cardigan_vest_from500000.csv'
pkl_filename = '%s.pickle' % filename
url_prefix_img = 'http://i.011st.com%s'
entries = [entry.strip() for entry in open(filename, 'r')]


#import pdb; pdb.set_trace()
td_count = 0
item_info = []
for n, entry in enumerate(entries):
  imageurl = url_prefix_img % entry
  url = url_prefix_req % imageurl
  try:
    start_det = time.time()
    response = urllib2.urlopen(url)
    end_det = time.time()
    if response <> None:
      retrieved_items = decode_json(json.loads(response.read()))
      for key in retrieved_items['feature'].keys():
        feature = retrieved_items['feature'][key]
        #retrieved_items['signature'][key] = np.digitize(feature ,bins ,right=True)
        if retrieved_items['signature'] == None: retrieved_items['signature'] = dict()
        retrieved_items['signature'][key] = indexer.hashing(feature)
        retrieved_items['signature'][key] = indexer.pack_bit_64(retrieved_items['signature'][key])
        retrieved_items['feature'] = dict()
        item_info.append(retrieved_items)
        break
    else:
      print 'No response to url:', url

    if n % 100 == 0:
      with open(pkl_filename, 'wb') as f:
        pickle.dump(item_info, f)
      print('%d dump: %s' % (n, pkl_filename))
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

