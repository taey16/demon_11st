
# -*- coding: UTF-8 -*-

import flask
import werkzeug
from web_server import web_server
from flask_decorator import crossdomain
import urllib, urllib2
import json
import logging
import time, datetime
import os,sys
import numpy as np
from PIL import Image

html_filename = 'index_11st_attribute.html'
html_filename_vsm = 'index_vsm.html'
port = 8081
feature_demon_host_ip = '10.202.4.219'
feature_demon_port= 8080 
feature_demon_request_prefix = \
  'http://%(host_ip)s:%(port)d/attribute_request_handler?url=%%s' % \
  {'host_ip': feature_demon_host_ip, 'port': feature_demon_port}

# global the flask app object
app = flask.Flask(__name__)


def call_attribute_demon(imageurl):
  result_dic = {}
  import pdb; pdb.set_trace()
  try:
    fe_starttime = time.time()
    url = feature_demon_request_prefix % imageurl
    response = urllib2.urlopen(url)
    logging.info('caption done, %.4f', time.time() - fe_starttime)
    if response <> None:
      result_dic = json.loads(response.read())
    else:
      result_dic['result'] = False
  except Exception as err:
    logging.info('call_attribute_demon error: %s', err)
    return {'result': False}

  return result_dic


def call_detector_demon(local_filename):
  result_dic = {}
  #import pdb; pdb.set_trace()
  try:
    fe_starttime = time.time()
    roi_boxes_and_scores, feature_vectors = app.agent.detect(local_filename)
    roi_box_image = app.agent.draw_rois(app.agent.img, roi_boxes_and_scores)
    logging.info('detection done, %.4f', time.time() - fe_starttime)
    result_dic['result'] = True
    result_dic['roi_boxes_and_scores'] = roi_boxes_and_scores
    result_dic['feature_vectors'] = feature_vectors
  except Exception as err:
    logging.info('call_attribute_demon error: %s', err)
    return {'result': False}, None

  return result_dic, roi_box_image


def encode_json(result_dic):
  result_json = json.dumps(result_dic)
  return result_json


def encode_flask_template(_html_filename, _has_result, _result_dic, _flag='success'):
  return flask.render_template(\
    _html_filename, has_result=_has_result,result=_result_dic, flag=_flag
  )


UPLOAD_FOLDER = '/storage/enroll'
#wget_cmd = 'wget %s -O %s'
def download_get_req(url):
  #filename = app.korean_url_handler.get_downloaded_filename(UPLOAD_FOLDER, 'jpg')
  filename = app.korean_url_handler.download_image(url, UPLOAD_FOLDER)
  assert(os.path.exists(filename))
  local_url = filename.replace('/storage/', 'http://10.202.4.219:2596/PBrain/')
  #os.system(wget_cmd % (url, '%s' % filename))
  return filename, local_url


def download_post_req(imagefile):
  filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
    werkzeug.secure_filename(imagefile.filename)
  filename = os.path.join(UPLOAD_FOLDER, filename_)
  imagefile.save(filename)
  image = app.exifutils.open_oriented_im(filename)
  image = Image.fromarray(np.uint8(image*255))
  image.save(filename)
  local_url = filename.replace('/storage/', 'http://10.202.4.219:2596/PBrain/')
  return filename, local_url


@app.route('/vsm_request_handler', methods=['GET'])
@crossdomain(origin='*')
def vsm_request_handler():
  #import pdb; pdb.set_trace()
  query_string = flask.request.args.get('query_string', '')
  print(query_string)
  result_dic = {}
  flag = {}
  try:
    start_vsm = time.time()
    result_dic = app.vsm.do_search(query_string, 400)
    number_of_retrieved_docs = len(result_dic['retrieved_item'])
    elapsed_vsm = time.time() - start_vsm
    flag['total_docs'] = app.vsm.N
    flag['number_of_retrieved_docs'] = number_of_retrieved_docs
    flag['elapsed'] = elapsed_vsm
    if result_dic['result']:
      return flask.render_template(
        html_filename_vsm, has_result=True, result=result_dic, flag=flag)
  except Exception as err:
    logging.info(err)
    return flask.render_template(
      html_filename_vsm, has_result=False, result=result_dic, flag=[0])


@app.route('/attribute_request_handler', methods=['GET'])
@crossdomain(origin='*')
def attribute_request_handler():
  imageurl = flask.request.args.get('url', '')
  is_browser = flask.request.args.get('is_browser', '')
  result_dic = {}
  import pdb; pdb.set_trace()
  try:
    fe_starttime = time.time()
    filename, local_url = download_get_req(imageurl)
    result_dic = call_attribute_demon(local_url)
    #result_dic_det, roi_box_image = call_detector_demon(filename)
  except Exception as err:
    logging.info('attribute_request_handler error: %s', err)
    if is_browser <> '1': return {'result': False}
    else:
      return encode_flask_template(\
        html_filename, False, result_dic, 'fail')

  if is_browser <> '1':
    return encode_json(result_dic)
  else:
    return encode_flask_template(\
      html_filename, True, result_dic, 'success')


@app.route('/attribute_request_handler_upload', methods=['POST'])
@crossdomain(origin='*')
def attribute_request_handler_upload():
  #import pdb; pdb.set_trace()
  result_dic = {}
  try:
    imagefile = flask.request.files['imagefile']
    filename, local_url = download_post_req(imagefile)
    logging.info('imageurl %s', local_url)
    result_dic = call_attribute_demon(local_url)
  except Exception as err:
    logging.info('Uploaded image open error: %s', err)
    return encode_flask_template( \
      html_filename, False, result_dic, 'fail')

  return encode_flask_template( \
    html_filename, True, result_dic, 'success')


@app.route('/')
@crossdomain(origin='*')
def index():
  return flask.render_template(
    #html_filename_vsm, has_result=False, result=[], flag='')
    html_filename, has_result=False, result=[], flag='')


class application(web_server):
  def __init__(self, port):
    util_root = '/works/demon_11st/utils'
    sys.path.insert(0, util_root)
    from exifutil import exifutil
    app.exifutils = exifutil()

    from korean_url_handler import korean_url_handler
    app.korean_url_handler = korean_url_handler()

    vsm_root = '/works/demon_11st/vsm'
    sys.path.insert(0, vsm_root)
    from vsm import vsm
    #import pdb; pdb.set_trace()
    app.vsm = vsm( '/storage/attribute/11st_julia_tshirts_shirtstes_blous_sentences.model_id_inception-v3-2015-12-05_bn_removed_epoch31_bs16_encode256_layer2_lr4.000000e-04.t7.txt')

    """
    agent_root = '/works/demon_11st/agent/detection'
    sys.path.insert(0, agent_root)
    import _init_paths
    from conf import conf
    from agent import agent
    yaml_file = '/storage/product/detection/11st_All/cfg/faster_rcnn_end2end_test.yml'
    conf = conf(yaml_file, 0)
    app.agent = agent()
    """

    # start web server
    web_server.__init__(self, app, port)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  application = application(port)

