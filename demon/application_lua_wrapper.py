
# -*- coding: UTF-8 -*-

import flask
from web_server import web_server
import urllib, urllib2
import json
import logging
import time
from flask_decorator import crossdomain
from korean_url_handler import korean_url_handler

import numpy as np

index_filename = 'index_11st.html'
url_prefix = 'http://10.202.35.0:8080/lua_wrapper_request_handler/?query=%s'

# global the flask app object
app = flask.Flask(__name__)


@app.route('/lua_wrapper_request_handler', methods=['GET'])
@crossdomain(origin='*')
def mosaic_request_handler():
  global_starttime = time.time()
  imageurl = flask.request.args.get('url', '')
  is_browser = flask.request.args.get('is_browser', '')
  import pdb; pdb.set_trace()
  try:
    download_starttime = time.time()
    filename = app.korean_url_handler.download_image(imageurl)
    image = app.agent.load_image(filename)
    logging.info('Image download done, %.4f', 
      time.time() - download_starttime)

    fe_starttime = time.time()
    url = url_prefix % imageurl
    response = urllib2.urlopen(url)
    logging.info('extract_feature done, %.4f', time.time() - fe_starttime)
    if response <> None:
      retrieved_items = json.loads(response.read())
      if retrieved_items['result']:
        result_dic = {}
        result_dic['url'] = retrieved_items['url']
        result_dic['predicted_category'] = retrieved_items['category']
        result_dic['scores'] = retrieved_items['score']
        result_dic['feature'] = np.asarray(retrieved_items['feature'])
  except Exception as err:
    logging.info('lua_wrapper_request_handler error: %s', err)
    if is_browser <> '1': return {'result': False}
    else:
      return flask.render_template(
        index_filename, has_result=False, result=result_dic, flag='fail')

  if is_browser <> '1':
    result_json = json.dumps(result_dic)
    return result_json
  else
    return flask.render_template(
      index_filename, has_result=True, result=result, flag=np.squeeze(feature))


@app.route('/')
def index():
  #import pdb; pdb.set_trace()
  return flask.render_template(
    index_filename, has_result=False, result=[], flag='fail')


class application(web_server):
  def __init__(self, port):
    app.korean_url_handler = korean_url_handler() 
    # start web server
    web_server.__init__(self, app, port)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
 
  port = 8081
  app = application(port)

