
# coding: utf8

import flask
from web_server import web_server
import cStringIO as StringIO
import urllib
import json
import logging
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
@app.route('/url_request_handler', methods=['GET'])
def url_request_handler():
  #import pdb; pdb.set_trace()
  imageurl = flask.request.args.get('url', '')
  category = flask.request.args.get('category', '')
  try:
    #query_meta = app.parser_utils.generate_meta_dic() 
    #query_meta = app.parser_utils.update_meta(query_meta, '__mctgr_no__', category)
    #query_meta = app.parser_utils.update_meta(query_meta, '__org_img_url__', imageurl)
    string_buffer = StringIO.StringIO(urllib.urlopen(imageurl).read())
    image = app.agent.load_image(string_buffer)
    logging.info('Image({}): {}'.format(category, imageurl))

    feature = app.agent.extract_feature(image, 'pool5/7x7_s1')
    logging.info('extract_feature done')
    feature = app.indexer.hashing(feature)
    feature = app.indexer.pack_bit_16(feature)
    logging.info('hashing done')
    neighbor_list = \
      app.indexer.get_nearest_neighbor(feature, category, num_neighbors)
    logging.info('get nearest neighbor done')

    result_dic = {}
    result_dic['request_category'] = category
    result_dic['query'] = imageurl
    result_dic['retrieval_list'] = neighbor_list
    result_dic['result'] = True
    #neighbor_list.insert(0, query_meta)
    neighbor_list = json.dumps(result_dic)
  except Exception as err:
    logging.info('URL Image open error: %s', err)
    return None

  return neighbor_list


@app.route('/browser_request_handler', methods=['GET'])
def browser_request_handler():
  #import pdb; pdb.set_trace()
  imageurl = flask.request.args.get('url', '')
  category = flask.request.args.get('category', '')
  try:
    query_meta = app.parser_utils.generate_meta_dic() 
    query_meta = app.parser_utils.update_meta(query_meta, '__mctgr_no__', category)
    query_meta = app.parser_utils.update_meta(query_meta, '__org_img_url__', imageurl)
    string_buffer = StringIO.StringIO(urllib.urlopen(imageurl).read())
    image = app.agent.load_image(string_buffer)
    logging.info('Image({}): {}'.format(category, imageurl))

    feature = app.agent.extract_feature(image, 'pool5/7x7_s1')
    logging.info('extract_feature done')
    feature = app.indexer.hashing(feature)
    feature = app.indexer.pack_bit_16(feature)
    logging.info('hashing done')
    neighbor_list = \
      app.indexer.get_nearest_neighbor(feature, category, num_neighbors)
    logging.info('get nearest neighbor done')
    neighbor_list.insert(0, query_meta)
    #neighbor_list = json.dumps(neighbor_list)

    result = []
    query_check_flag = 0
    for item in neighbor_list:
      if query_check_flag == 0: result.append(item['__org_img_url__'])
      else: result.append('http://i.011st.com%s' % item['__org_img_url__'])
      query_check_flag += 1
      
  except Exception as err:
    logging.info('URL Image open error: %s', err)
    return flask.render_template(
      'index.html', has_result=False, result=result, flag='fail')

  return flask.render_template(
    'index.html', has_result=True, result=result, flag='success')


@app.route('/')
def index():
  #import pdb; pdb.set_trace()
  return flask.render_template(
    'index.html', has_result=False, result=[], flag='fail')



class application(web_server):
  def __init__(self, net_args, category_no, max_num_items, database_filename):
    self.net_args = net_args
    self.database_filename = database_filename
    # Initialize classifier
    app.agent = agent(**self.net_args)
    logging.info('Initialize vision model done')
    app.agent.net.forward()
    logging.info('Net forward done')
    # Initialize indexer
    app.indexer = indexer(category_no, max_num_items)
    app.indexer.load_category(database_filename)
    logging.info('Initialize indexer done')

    app.parser_utils = parser_utils()

    # start web server
    web_server.__init__(self, app, self.net_args)


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

  # set indexer args
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

  database_filename = \
  '/home/taey16/storage/product/11st_julia/demo_%s.txt.wrap_size0.pickle'

  app = application(net_args, category_no, max_num_items, database_filename)

