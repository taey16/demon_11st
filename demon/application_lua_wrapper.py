
# -*- coding: UTF-8 -*-

import flask
from web_server import web_server
import urllib, urllib2
import json
import logging
import time
from flask_decorator import crossdomain

import numpy as np

host_ip = '10.202.35.109'
feature_demon_port = 8080
port = 8081
index_filename = 'index_11st.html'
url_prefix = 'http://%(host_ip)s:%(port)d/lua_wrapper_request_handler/?url=%%s' % \
  {'host_ip': host_ip, 'port': feature_demon_port}


# global the flask app object
app = flask.Flask(__name__)


def call_feature_demon(imageurl):
  result_dic = {}
  #import pdb; pdb.set_trace()
  try:
    fe_starttime = time.time()
    url = url_prefix % imageurl
    response = urllib2.urlopen(url)
    logging.info('extract_feature done, %.4f', time.time() - fe_starttime)
    if response <> None:
      retrieved_items = json.loads(response.read())
      if retrieved_items['result']:
        result_dic['url'] = retrieved_items['url']
        result_dic['predicted_category'] = retrieved_items['category']
        result_dic['scores'] = \
          np.trim_zeros((np.asarray(retrieved_items['score']) * 100).astype(np.uint8))
        #print(result_dic['scores'].shape)
        result_dic['predicted_category'] = result_dic['predicted_category'][0:result_dic['scores'].size]
        result_dic['feature'] = np.asarray(retrieved_items['feature'])
  except Exception as err:
    logging.info('call_feature_demon error: %s', err)
    return {'result': False, 'feature': None}

  return result_dic


@app.route('/lua_wrapper_request_handler', methods=['GET'])
@crossdomain(origin='*')
def lua_wrapper_request_handler():
  global_starttime = time.time()
  imageurl = flask.request.args.get('url', '')
  is_browser = flask.request.args.get('is_browser', '')
  result_dic = {}
  import pdb; pdb.set_trace()
  try:
    fe_starttime = time.time()
    result_dic = call_feature_demon(imageurl)
  except Exception as err:
    logging.info('lua_wrapper_request_handler error: %s', err)
    if is_browser <> '1': return {'result': False}
    else:
      return flask.render_template(
        index_filename, has_result=False, result=result_dic, flag='fail')

  if is_browser <> '1':
    result_json = json.dumps(result_dic)
    return result_json
  else:
    return flask.render_template(
      index_filename, has_result=True, result=result_dic, flag=[0])


@app.route('/')
def index():
  #import pdb; pdb.set_trace()
  return flask.render_template(
    index_filename, has_result=False, result=[], flag='fail')


class application(web_server):
  def __init__(self, port):
    # start web server
    web_server.__init__(self, app, port)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
 
  app = application(port)

