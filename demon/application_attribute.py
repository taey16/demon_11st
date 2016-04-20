
# -*- coding: UTF-8 -*-

import os
import sys
import flask
from web_server import web_server
from flask_decorator import crossdomain
import json
import logging
import time

#from PIL import Image

html_filename = 'index_11st_attribute.html'
host_ip = '10.202.35.109'
port = 8081

# global the flask app object
app = flask.Flask(__name__)
def init_result_dic():
  result_dic = {}
  result_dic['result'] = False
  result_dic['result_roi'] = False
  result_dic['result_sentence'] = False
  result_dic['result_retrieval'] = False
  result_dic['result_feature'] = False
  result_dic['result_signature'] = False
  result_dic['result_category'] = False
  result_dic['url'] = None
  result_dic['roi'] = None
  result_dic['roi_box_image'] = None
  result_dic['sentence'] = None
  result_dic['sentence_scores'] = None
  result_dic['retrieved_item'] = None
  result_dic['feature'] = None
  result_dic['signature'] = None
  result_dic['category_scores'] = None
  result_dic['category_name'] = None
  return result_dic

def encode_json(result_dic):
  import pdb; pdb.set_trace()
  for key in result_dic['roi'].keys():
    result_dic['roi'][key] = result_dic['roi'][key].tolist()
    result_dic['feature'][key] = result_dic['feature'][key].tolist()
  result_json = json.dumps(result_dic)
  return result_json

def encode_flask_template(_html_filename, _has_result, _result_dic, _flag='success'):
  return flask.render_template(\
    _html_filename, has_result=_has_result,result=_result_dic, flag=_flag
  )

def set_result_dic(result_dic, result):
  for k in result.keys():
    result_dic[k] = result[k]

  result_dic['result'] = True
  return result_dic


def call_attribute(agent, imageurl, local_path):
  #import pdb; pdb.set_trace()
  try:
    fe_starttime = time.time()
    response = agent.get_attribute(imageurl, local_path)
    logging.info('caption done, %.4f', time.time() - fe_starttime)
    if response <> None:
      result = json.loads(response)
    else:
      result['result'] = False
      result['result_sentence'] = False
  except Exception as err:
    logging.info('call_attribute error: %s', err)
    return {'result': False, 'result_sentence': False}

  return result


def call_detector(agent, local_filename):
  #import pdb; pdb.set_trace()
  try:
    fe_starttime = time.time()
    result = agent.detect(local_filename)
    result['roi_box_image'] = \
      agent.draw_rois(agent.img, result['roi'])
    logging.info('detection done, %.4f', time.time() - fe_starttime)
  except Exception as err:
    logging.info('call_attribute error: %s', err)
    return {'result': False, 'result_roi': False}

  return result


def call_vsm(vsm, query_string, imageurl, limit=600):
  try:
#    import pdb; pdb.set_trace()
    flag ={}
    start_vsm = time.time()
    result = vsm.do_search(query_string,limit)
    if imageurl <> '': result['url'] = imageurl
    result['result_sentence'] = True
    result['sentence'] = [query_string]
    result['sentence_scores'] = [-1]
    number_of_retrieved_docs = len(result['retrieved_item'])
    elapsed_vsm = time.time() - start_vsm
    flag['total_docs'] = vsm.N
    flag['number_of_retrieved_docs'] = number_of_retrieved_docs
    flag['elapsed'] = elapsed_vsm
  except Exception as err:
		raise err
  return result, flag


@app.route('/julia', methods=['GET'])
@crossdomain(origin='*')
def julia():
  imageurl = flask.request.args.get('url', None)
  local_path = flask.request.args.get('local_path', None)
  app.result_dic = init_result_dic()
  #import pdb; pdb.set_trace()
  try:
    app.result_dic = set_result_dic(app.result_dic, {'url': imageurl})
    filename, local_url = app.demon_utils.download_get_req(imageurl)
    result = call_attribute(app.agent_attribute, local_url, filename)
    app.result_dic = set_result_dic(app.result_dic, result)
    result = call_detector(app.agent_detector, filename)
    roi_box_image = result['roi_box_image']
    result['roi_box_image'] = \
      filename.replace('/storage/', 'http://%s:2596/PBrain/' % host_ip) + '.det.jpg'
    roi_box_image.save('%s' % filename + '.det.jpg')
    app.result_dic = set_result_dic(app.result_dic, result)
  except Exception as err:
    logging.info('julia error: %s', err)
    return encode_json({'result': False, 'url': imageurl})
  
  return encode_json(app.result_dic)

def call_attr_detect_vsm(url,filename):
  try:
    result = call_attribute(app.agent_attribute, url, filename)
    app.result_dic = set_result_dic(app.result_dic, result)
    result = call_detector(app.agent_detector, filename)
    roi_box_image = result['roi_box_image']
    result['roi_box_image'] = \
      filename.replace('/storage/', 'http://%s:2596/PBrain/' % host_ip) + '.det.jpg'
    roi_box_image.save('%s' % filename + '.det.jpg')
    app.result_dic = set_result_dic(app.result_dic, result)
    result,flag = call_vsm(app.vsm,app.result_dic['sentence'][0],url)
    app.result_dic = set_result_dic(app.result_dic,result)
  except Exception as err:
    raise err	
  return flag
	


@app.route('/vsm_request_handler', methods=['GET'])
@crossdomain(origin='*')
def vsm_request_handler():
  #import pdb; pdb.set_trace()
  query_string = flask.request.args.get('query_string', '')
  is_browser = flask.request.args.get('is_browser', '')
  imageurl = flask.request.args.get('url', '')
  app.result_dic = init_result_dic()
  try:
    result,flag = call_vsm(app.vsm, query_string,imageurl)
    app.result_dic = set_result_dic(app.result_dic, result)
  except Exception as err:
    logging.info(err)
    return encode_flask_template(\
      html_filename, True, app.result_dic, 'fail')

  return encode_flask_template(\
    html_filename, True, app.result_dic, flag)


@app.route('/request_handler_upload', methods=['POST'])
@crossdomain(origin='*')
def request_handler_upload():
  #import pdb; pdb.set_trace()
  is_browser = flask.request.args.get('is_browser', '1')
  app.result_dic = init_result_dic()
  try:
    imagefile = flask.request.files['imagefile']
    filename, local_url = app.demon_utils.download_post_req(imagefile)
    logging.info('local_path %s', filename)
    flag = call_attr_detect_vsm(local_url,filename)
  except Exception as err:
    logging.info('request_handler_upload error: %s', err)
    if is_browser <> '1': return encode_json({'result': False, 'url': local_url})
    else:
      return encode_flask_template(\
        html_filename, False, app.result_dic, 'fail')
  
  if is_browser <> '1':
    #for key in app.result_dic['roi'].keys():
    #  app.result_dic['roi'][key] = app.result_dic['roi'][key].tolist()
    return encode_json(app.result_dic)
  else:
    if local_url == None:
      app.result_dic['url'] = filename.replace('/storage/', 'http://%s:2596/PBrain/' % host_ip)
    return encode_flask_template(\
      html_filename, True, app.result_dic,flag)


@app.route('/request_handler', methods=['GET'])
@crossdomain(origin='*')
def request_handler():
  imageurl = flask.request.args.get('url', None)
  local_path = flask.request.args.get('local_path', None)
  is_browser = flask.request.args.get('is_browser', '')
  app.result_dic = init_result_dic()
  #import pdb; pdb.set_trace()
  try:
    if imageurl <> None:
      app.result_dic = set_result_dic(app.result_dic, {'url': imageurl})
      filename, local_url = app.demon_utils.download_get_req(imageurl)
    else: 
      if os.path.exists(local_path):
        local_url = None
        filename = local_path
      else: return encode_json({'url': local_path, 'result': False})
    flag = call_attr_detect_vsm(imageurl,filename)
  except Exception as err:
    logging.info('request_handler error: %s', err)
    if is_browser <> '1': return encode_json({'result': False, 'url': imageurl})
    else:
      return encode_flask_template(\
        html_filename, False, app.result_dic, 'fail')
  
  if is_browser <> '1':
   # for key in app.result_dic['roi'].keys():
   #   app.result_dic['roi'][key] = app.result_dic['roi'][key].tolist()
    return encode_json(app.result_dic)
  else:
    if local_url == None:
      app.result_dic['url'] = filename.replace('/storage/', 'http://%s:2596/PBrain/' % host_ip)
    return encode_flask_template(\
      html_filename, True, app.result_dic, flag)

@app.route('/')
@crossdomain(origin='*')
def index():
  return flask.render_template(
    html_filename, has_result=False, result=[], flag='')


class application(web_server):
  def __init__(self, port):

    util_root = '/works/demon_11st/utils'
    sys.path.insert(0, util_root)
    from demon_utils import demon_utils
    app.demon_utils = demon_utils(host_ip, '/storage/enroll')

    vsm_root = '/works/demon_11st/vsm'
    sys.path.insert(0, vsm_root)
    from vsm import vsm
    #import pdb; pdb.set_trace()
    app.vsm = vsm(\
      '/storage/attribute/PBrain_all.csv.image_sentence.txt'
    )

    agent_detector_root = '/works/demon_11st/agent/detection'
    sys.path.insert(0, agent_detector_root)
    import _init_paths
    from conf import conf
    from agent_detector import agent_detector
    yaml_file = '/storage/product/detection/11st_All/cfg/faster_rcnn_end2end_test.yml'
    conf = conf(yaml_file, 0)
    app.agent_detector = agent_detector()

    #import pdb; pdb.set_trace()
    agent_attribute_root = '/works/demon_11st/agent/attribute' 
    sys.path.insert(0, agent_attribute_root)
    from agent_attribute import agent_attribute 
    attribute_demon_host_ip = host_ip
    attribute_demon_port= 8080
    app.agent_attribute = agent_attribute( \
      attribute_demon_host_ip, attribute_demon_port)

    app.result_dic = init_result_dic()

    web_server.__init__(self, app, port)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  application = application(port)

