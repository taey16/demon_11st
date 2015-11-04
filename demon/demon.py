
# coding: utf8

import os, sys, time
import logging
import flask
import werkzeug
import optparse
import tornado.wsgi
import tornado.httpserver
import cStringIO as StringIO
import urllib
import json

PJT_PATH = '/home/taey16/'
PJT_NAME = 'demon_11st'
UTIL_ROOT = '{}/{}/utils'.format(PJT_PATH, PJT_NAME)
FEAT_ROOT = '{}/{}/agent'.format(PJT_PATH, PJT_NAME)
INDEXER_ROOT = '{}/{}/indexer'.format(PJT_PATH, PJT_NAME)
sys.path.insert(0, UTIL_ROOT)
sys.path.insert(0, FEAT_ROOT)
sys.path.insert(0, INDEXER_ROOT)
from agent import agent
from parser_11st import parser_11st
from indexer import indexer

gpu_mode = True
model_def_file = '{}/storage/models/inception5/inception5.prototxt'.format(PJT_PATH)
pretrained_model_file = '{}/storage/models/inception5/inception5.caffemodel'.format(PJT_PATH)
image_dim, raw_scale = 384, 255.

#DATABASE_FILENAME = '/storage/product/det/unique-labeller_eng_20150625144012.csv.cate_bbox.csv.shuffle_00.csv.readable_only.csv.bit.pickle.webpath.pickle.inception5.pickle'
#DATABASE_FILENAME = '/storage/product/11st_6M/11st_380K.shuffle.webpath.bit.pickle.inception5.pickle'
#DATABASE_FILENAME = '/storage/product/11st_6M/11st_380K.shuffle.webpath.bit.pickle.inception5.4096bit.pickle'
#DATABASE_FILENAME = '/home/taey16/storage/product/11st_6M/11st_380K.shuffle.webclasspath.bit.pickle.inception5.4096bit.pickle'
#DATABASE_FILENAME = '/home/taey16/storage/product/11st_6M/11st_380K.shuffle.webclasspath.bit.pickle.inception5.pickle'
CATEGORY_NAME = []
#CATEGORY_NAME.append('127681')
CATEGORY_NAME.append('127687')
DATABASE_FILENAME = '/home/taey16/storage/product/11st_julia/demo_%s.txt.pickle'

NUM_NEIGHBORS = 10

port = '15002'


# Obtain the flask app object
app = flask.Flask(__name__)


@app.route('/url_request_handler', methods=['GET'])
def url_request_handler():
  #import pdb; pdb.set_trace()
  imageurl = flask.request.args.get('url', '')
  category = flask.request.args.get('category', '')
  try:
    string_buffer = StringIO.StringIO(urllib.urlopen(imageurl).read())
    image = app.agent.load_image(string_buffer)
    logging.info('Image({}): {}'.format(category, imageurl))

    feature = app.agent.extract_feature(image, 'pool5/7x7_s1')
    logging.info('extract_feature done')
    feature = app.indexer.hashing(feature)
    feature = app.indexer.pack_bit_16(feature)
    logging.info('hashing done')
    neighbor_list = app.indexer.get_nearest_neighbor( feature, category, NUM_NEIGHBORS )
    logging.info('get nearest neighbor done')

    neighbor_list = json.dumps(neighbor_list)
    #res = flask.jsonify(url=imageurl, category=category)
  except Exception as err:
    logging.info('URL Image open error: %s', err)
    return None

  return neighbor_list


def start_tornado(app, port=5000):
  http_server = tornado.httpserver.HTTPServer(
    tornado.wsgi.WSGIContainer(app))
  http_server.listen(port)
  tornado.ioloop.IOLoop.instance().start()


def start_from_terminal(app):
  parser = optparse.OptionParser()
  parser.add_option(
    '-p', '--port',
    help="which port to serve content on",
    type='int', default=port)

  opts, args = parser.parse_args()
  net_args = {
    'model_def_file': model_def_file,
    'pretrained_model_file': pretrained_model_file,
    'gpu_mode': gpu_mode, 'device_id': 1,
    'image_dim': image_dim, 'raw_scale': raw_scale,
  }
  # Initialize classifier
  app.agent = agent(**net_args)
  logging.info('Initialize vision model done')
  # warm start by forward for allocation
  app.agent.net.forward()
  logging.info('Net forward done')

  app.indexer = indexer()
  for category_id in CATEGORY_NAME: 
    app.indexer.load(category_id, DATABASE_FILENAME % category_id)
    logging.info('Loading indexer for {}'.format(category_id))
  logging.info('Initialize indexer done')
  #app.indexer.load(DATABASE_FILE)

  start_tornado(app, opts.port)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  start_from_terminal(app)

