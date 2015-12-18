
# -*- coding: UTF-8 -*-

import flask
from web_server import web_server
import urllib
import json
import logging
import time
from flask_decorator import crossdomain
from korean_url_handler import korean_url_handler

agent_root  = '/home/taey16/demon_11st/agent'
indexer_root= '/home/taey16/demon_11st/indexer'
utils_root = '/home/taey16/demon_11st/utils'
import sys
sys.path.insert(0, agent_root)
sys.path.insert(0, indexer_root)
sys.path.insert(0, utils_root)
from agent import agent
from indexer import indexer
from parser_utils import parser_utils

num_neighbors = 60

# global the flask app object
app = flask.Flask(__name__)


@app.route('/mosaic_request_handler', methods=['GET'])
@crossdomain(origin='*')
def mosaic_request_handler():
  global_starttime = time.time()
  imageurl = flask.request.args.get('url', '')
  #import pdb; pdb.set_trace()
  try:
    download_starttime = time.time()
    filename = app.korean_url_handler.download_image(imageurl)
    image = app.agent.load_image(filename)
    #logging.info('Image download done, %.4f', 
    #  time.time() - download_starttime)

    fe_starttime = time.time()
    feature = app.agent.extract_feature(image, 'pool5/7x7_s1', app.oversample)
    logging.info('extract_feature done, %.4f', time.time() - fe_starttime)
    feature_binary = app.indexer.hashing(feature)
    #signature = app.indexer.pack_bit_16(feature_binary)
    signature = app.indexer.pack_bit_64(feature_binary)
    result_dic = {}
    result_dic['__org_img_url__'] = imageurl
    result_dic['feature'] = feature[0,:].tolist()
    result_dic['signature'] = signature[0,:].tolist()
    result_json = json.dumps(result_dic)
  except Exception as err:
    logging.info('moasic_request_handler error: %s', err)
    return None

  return result_json


@app.route('/url_request_handler', methods=['GET'])
@crossdomain(origin='*')
def url_request_handler():
  #import pdb; pdb.set_trace()
  global_starttime = time.time()
  imageurl = flask.request.args.get('url', '')
  category = flask.request.args.get('category', '')
  try:
    #string_buffer = StringIO.StringIO(urllib.urlopen(imageurl).read())
    #image = app.agent.load_image(string_buffer)
    #logging.info('Image({}): {}'.format(category, imageurl))
    download_starttime = time.time()
    filename = app.korean_url_handler.download_image(imageurl)
    image = app.agent.load_image(filename)
    logging.info('Image download done, %.4f', 
      time.time() - download_starttime)

    fe_starttime = time.time()
    feature = app.agent.extract_feature(image, 'pool5/7x7_s1', app.oversample)
    logging.info('extract_feature done, %.4f', time.time() - fe_starttime)
    feature = app.indexer.hashing(feature)
    feature = app.indexer.pack_bit_16(feature)
    logging.info('hashing done')
    nn_starttime = time.time()
    neighbor_list, neighbor_distance = \
      app.indexer.get_nearest_neighbor(feature, category, num_neighbors)
    assert(len(neighbor_list) == len(neighbor_distance))
    logging.info('get nearest neighbor done, %.4f', time.time() - nn_starttime)

    result_dic = {}
    result_dic['request_category'] = category
    result_dic['query'] = imageurl
    result_dic['retrieval_list'] = []
    for meta, distance in zip(neighbor_list, neighbor_distance):
      meta['__distance__'] = str(distance)
      result_dic['retrieval_list'].append(meta)
      
    result_dic['result'] = True
    #neighbor_list.insert(0, query_meta)
    neighbor_list = json.dumps(result_dic)
  except Exception as err:
    logging.info('URL Image open error: %s', err)
    return None

  return neighbor_list


@app.route('/browser_request_handler', methods=['GET'])
@crossdomain(origin='*')
def browser_request_handler():
  #import pdb; pdb.set_trace()
  imageurl = flask.request.args.get('url', '')
  category = flask.request.args.get('category', '')
  try:
    query_meta = app.parser_utils.generate_meta_dic() 
    query_meta = app.parser_utils.update_meta(query_meta, '__mctgr_no__', category)
    query_meta = app.parser_utils.update_meta(query_meta, '__org_img_url__', imageurl)
    #string_buffer = StringIO.StringIO(urllib.urlopen(imageurl).read())
    #image = app.agent.load_image(string_buffer)
    #logging.info('Image({}): {}'.format(category, imageurl))
    filename = app.korean_url_handler.download_image(imageurl)
    image = app.agent.load_image(filename)

    feature = app.agent.extract_feature(image, 'pool5/7x7_s1', app.oversample)
    logging.info('extract_feature done')
    feature_probe = feature
    feature = app.indexer.hashing(feature)
    feature = app.indexer.pack_bit_16(feature)
    logging.info('hashing done')
    neighbor_list, neighbor_distance = \
      app.indexer.get_nearest_neighbor(feature, category, num_neighbors)
    assert(len(neighbor_list) == len(neighbor_distance))
    logging.info('get nearest neighbor done')
    neighbor_list.insert(0, query_meta)
    #neighbor_list = json.dumps(neighbor_list)

    result = []
    query_check_flag = 0
    for item in neighbor_list:
      meta_url_distance = {}
      if query_check_flag == 0: 
        meta_url_distance['meta'] = item['__org_img_url__']
        meta_url_distance['distance'] = 0
      else: 
        meta_url_distance['meta'] = 'http://i.011st.com%s' % item['__org_img_url__']
        meta_url_distance['distance'] = neighbor_distance[query_check_flag-1]
      result.append(meta_url_distance)
      query_check_flag += 1
      
  except Exception as err:
    logging.info('URL Image open error: %s', err)
    return flask.render_template(
      'index.html', has_result=False, result=result, flag='fail')

  return flask.render_template(
    'index.html', has_result=True, result=result, flag=feature_probe[0,:])
    #'index.html', has_result=True, result=result, flag='success')


@app.route('/')
def index():
  #import pdb; pdb.set_trace()
  return flask.render_template(
    'index.html', has_result=False, result=[], flag='fail')


class application(web_server):
  def __init__(self, port, net_args, oversample, category_no, max_num_items, database_filename):
    self.net_args = net_args
    self.database_filename = database_filename
    # Initialize classifier
    app.oversample = oversample
    app.agent = agent(**self.net_args)
    logging.info('Initialize vision model done')
    app.agent.net.forward()
    logging.info('Net forward done')
    # Initialize indexer
    app.indexer = indexer(category_no, max_num_items)
    app.indexer.load_category(database_filename)
    logging.info('Initialize indexer done')
    # get parser_utils
    app.parser_utils = parser_utils()
    app.korean_url_handler = korean_url_handler() 

    # start web server
    web_server.__init__(self, app, port)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  # set net args
  net_args = {
    'model_def_file': 
      '/home/taey16/storage/models/inception5/inception5.prototxt',
    'pretrained_model_file': 
      '/home/taey16/storage/models/inception5/inception5.caffemodel',
    'gpu_mode': True, 'device_id': 0,
    'image_dim': 384, 'raw_scale': 255,
  }
 
  #port = 8080
  port = 15003
  oversample = True

  # set indexer args
  category_no = []
  max_num_items = []
  """
  category_no.append('127681')
  max_num_items.append(140000)
  category_no.append('127687')
  max_num_items.append(41000)
  category_no.append('1530')
  max_num_items.append(43000)
  category_no.append('1645')
  max_num_items.append(26300)
  """
  category_no.append('1612')
  max_num_items.append(42900)

  database_filename = \
    '/home/taey16/storage/product/11st_julia/demo_%s.txt.wrap_size0.pickle'
    #'/home/taey16/storage/product/11st_julia/demo_%s.txt.wrap_size0.oversampleFalse.pickle'

  app = application(port, net_args, oversample, category_no, max_num_items, database_filename)

