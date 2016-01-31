
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

html_filename = 'index_11st_detection.html'
port = 8080

# global the flask app object
app = flask.Flask(__name__)


def call_feature_demon(input_data):
  result_dic = {}
  #import pdb; pdb.set_trace()
  try:
    fe_starttime = time.time()
    roi_boxes_and_scores, feature_vectors = app.agent.detect(input_data)
    roi_box_image = app.agent.draw_rois(app.agent.img, roi_boxes_and_scores)
    logging.info('detection done, %.4f', time.time() - fe_starttime)
    result_dic['result'] = True
    result_dic['roi_boxes_and_scores'] = roi_boxes_and_scores
    result_dic['feature_vectors'] = feature_vectors
  except Exception as err:
    logging.info('call_feature_demon error: %s', err)
    return {'result': False}, None

  return result_dic, roi_box_image


def encode_json(result_dic):
  for cls_name in result_dic['roi_boxes_and_scores'].keys():
    result_dic['roi_boxes_and_scores'][cls_name] = \
      result_dic['roi_boxes_and_scores'][cls_name].tolist()
    result_dic['feature_vectors'][cls_name] = \
      result_dic['feature_vectors'][cls_name].tolist()
  result_json = json.dumps(result_dic)
  return result_json


def encode_flask_template(_html_filename, _has_result, _result_dic, _flag='success'):
  return flask.render_template(\
    _html_filename, has_result=_has_result,result=_result_dic, flag=_flag
  )
  

UPLOAD_FOLDER = '/storage/enroll'
@app.route('/detector_request_handler', methods=['GET'])
@crossdomain(origin='*')
def detector_request_handler():
  imageurl = flask.request.args.get('url', '')
  is_browser = flask.request.args.get('is_browser', '')
  result_dic = {}
  #import pdb; pdb.set_trace()
  try:
    fe_starttime = time.time()
    filename = app.korean_url_handler.download_image(imageurl, UPLOAD_FOLDER)
    result_dic, roi_box_image = call_feature_demon(filename)
    bbox_image_url = filename.replace('/storage/', 'http://10.202.4.219:2596/PBrain/')
    roi_box_image.save('%s' % filename)
    result_dic['bbox_image_url'] = bbox_image_url
  except Exception as err:
    logging.info('detector_request_handler error: %s', err)
    if is_browser <> '1': return {'result': False}
    else:
      return decode_flask_template(\
        html_filename, False, result_dic, 'fail')

  if is_browser <> '1':
    return encode_json(result_dic)
  else:
    return decode_falsk_template(\
      html_filename, True, result_dic, 'success')


@app.route('/detector_request_handler_upload', methods=['POST'])
@crossdomain(origin='*')
def detector_request_handler_upload():
  #import pdb; pdb.set_trace()
  result_dic = {}
  try:
    imagefile = flask.request.files['imagefile']
    filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
      werkzeug.secure_filename(imagefile.filename)
    filename = os.path.join(UPLOAD_FOLDER, filename_)
    imagefile.save(filename)
    logging.info('Saving to %s', filename)
    image = app.exifutils.open_oriented_im(filename)
    imageurl = 'http://%(host_ip)s:2596/PBrain/enroll/%(filename)s' % \
      {'host_ip': host_ip, 'filename':filename_}
    logging.info('imageurl %s', imageurl)
    result_dic, roi_box_image = call_feature_demon(imageurl)
  except Exception as err:
    logging.info('Uploaded image open error: %s', err)
    return flask.render_template(
      html_filename, has_result=False, result=result_dic, flag='fail')

  return flask.render_template(
    html_filename, has_result=True, result=result_dic, flag=[0])


@app.route('/')
@crossdomain(origin='*')
def index():
  #import pdb; pdb.set_trace()
  return flask.render_template(
    html_filename, has_result=False, result=[], flag='fail')


class application(web_server):

  def __init__(self, port):

    util_root = '/works/demon_11st/utils'
    sys.path.insert(0, util_root)
    from exifutil import exifutil
    app.exifutils = exifutil()

    #import pdb; pdb.set_trace()
    agent_root = '/works/demon_11st/agent/detection'
    sys.path.insert(0, agent_root)
    import _init_paths
    from conf import conf
    from agent import agent
    yaml_file = '/storage/product/detection/11st_All/cfg/faster_rcnn_end2end_test.yml'
    conf = conf(yaml_file, 0)
    app.agent = agent()

    from korean_url_handler import korean_url_handler
    app.korean_url_handler = korean_url_handler()

    # start web server
    web_server.__init__(self, app, port)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
 
  application = application(port)

