
#-*- coding: utf8 -*-

import numpy as np
import PIL.Image
import scipy.io as sio
import cPickle as pickle
import sys, os
import datetime
PJT_ROOT = '/work/'
PJT_NAME = '{}/demon_11st/'.format(PJT_ROOT)
INDEXER_ROOT = '{}/indexer'.format(PJT_NAME)
UTILS_ROOT = '{}/utils'.format(PJT_NAME)
AGENT_ROOT = '{}/agent'.format(PJT_NAME)
sys.path.insert(0, AGENT_ROOT)
sys.path.insert(0, INDEXER_ROOT)
sys.path.insert(0, UTILS_ROOT)
from agent import agent
from parser_utils import parser_utils
from indexer import indexer

net_args = {
  'model_def_file': '{}/storage/models/inception5/inception5.prototxt'.format(PJT_ROOT),
  'pretrained_model_file': '{}/storage/models/inception5/inception5.caffemodel'.format(PJT_ROOT),
  'gpu_mode': True, 'device_id': 0,
  'image_dim': 384, 'raw_scale': 255.,
}

DATASET_ROOT = '/storage/product'
#demo_127681.txt woman,tshirts
#demo_127687.txt woman,skirts
#demo_1530.txt jacats, coats
#demo_1612.txt  long-arm T shirts, man-to-man
#demo_1645.txt casual-pants,pants

category_no = []
max_num_items = []
category_no.append('127681')
max_num_items.append(140000)
category_no.append('127687')
max_num_items.append(41000)
category_no.append('1530')
max_num_items.append(43000)
category_no.append('1645')
max_num_items.append(26300)
category_no.append('1612')
max_num_items.append(42900)
current_category = 4 

INPUT_FILENAME = '{}/demo_{}.txt'.format(
  '11st_julia', category_no[current_category])
OUTPUT_FILENAME = \
  '/home/taey16/storage/product/11st_julia/demo_{}.txt.wrap_size0.pickle'.format(
    category_no[current_category])


if __name__ == '__main__':
  print 'Start to indexing for {}'.format(INPUT_FILENAME)
  print 'output will be saved in {}'.format(OUTPUT_FILENAME)

  meta_filename = '{}/{}'.format(DATASET_ROOT, INPUT_FILENAME)
  parser = parser_utils()
  input = parser.parse(meta_filename)

  agent = agent(**net_args)
  agent.net.forward()
  import pdb; pdb.set_trace()
  indexer = indexer(category_no, max_num_items)

  item_counter = 0
  for item in input:
    try:
      prd_no = item['__prd_no__']
      fname  = '{}/october_11st_imgdata/{}.jpg'.format(DATASET_ROOT, prd_no)
      object_roi = item['__object_roi__'].strip().split(',')
      category_id = item['__mctgr_no__']
      roi = parser.get_roi_meta_dic(object_roi)
      image  = agent.load_image_roi(fname, roi, 0)
      #roi_pil, image_pil  = agent.draw_roi(fname, roi, 0)
      #roi_pil.save('roi.png')
      #image_pil.save('rectangle.png')
      feature= agent.extract_feature(image, 'pool5/7x7_s1')
      binary_feature = indexer.hashing(feature)
      packed_binary_feature = indexer.pack_bit_16(binary_feature)
      indexer.insert(item_counter, packed_binary_feature, category_id, item)
      item_counter += 1
    except:
      print 'ERROR: filename: ', fname

    if item_counter == max_num_items[current_category]: break

    if item_counter % 10 == 0: 
      print 'End of ', item_counter; sys.stdout.flush()

    #if num_indexed_samples == 10000:
    #  break

  #import pdb; pdb.set_trace()
  indexer.dump( category_no[current_category], OUTPUT_FILENAME )
  print 'Save to indexer.database[{}], {}'.format(category_no[current_category], OUTPUT_FILENAME)

