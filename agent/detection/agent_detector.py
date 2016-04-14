
#-*- coding: utf8 -*-
import sys
import os
import cv2
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import numpy as np
import _init_paths
from conf import conf
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
import caffe


class agent_detector(object):


  def __init__(self):
    if cfg['USE_GPU']: 
      caffe.set_device(cfg['GPU_ID'])
      caffe.set_mode_gpu()
    else: caffe.set_mode_cpu()

    self.phase = cfg['PHASE']
    self.prototxt = cfg[cfg.PHASE]['PROTOTXT']
    self.caffemodel=cfg[cfg.PHASE]['CAFFE_MODEL']
    if cfg['PHASE'] == 'TRAIN':
      self.caffe_phase = caffe.TRAIN
    else:
      self.caffe_phase = caffe.TEST

    self.net = caffe.Net(self.prototxt, self.caffemodel, self.caffe_phase)
    print(
      'Loading model done, \nprototxt: {}\ncaffemodel: {}'.format( \
        self.prototxt, self.caffemodel
    ))
    sys.stdout.flush()


  def load_image(self, image_path):
    assert(os.path.exists(image_path))
    self.img = cv2.imread(image_path)


  def flip_image(self):
    self.img_flipped = self.img[:,::-1,:]


  def detect(self, image_path, proposal=None):
    scores, boxes = self.im_detect(image_path, proposal)
    roi_boxes_and_scores, feature_vectors = self.post_process(scores, boxes)
    result = {}
    if len(roi_boxes_and_scores) == 0:
      print('ERROR in agent.detect (scores and boxes are all [])' )
      result['result_roi'] = False
      result['roi'] = dict()
      result['result_feature'] = False
      result['feature'] = dict()
      return result
    else:
      result['result_roi'] = True
      result['roi'] = roi_boxes_and_scores
      result['result_feature'] = True
      result['feature'] = feature_vectors

    return result


  def im_detect(self, image_path, proposal=None):
    try:
      self.load_image(image_path)
      #box_proposals = None
      scores, boxes = im_detect(self.net, self.img, proposal)
    except Exception as err:
      print('ERROR in agent.im_detect ', err)
      return [], [] 

    return scores, boxes


  def extract_feature(self, blob_name):
    #feature = np.reshape(np.squeeze(self.net.blobs[blob_name].data))
    #import pdb; pdb.set_trace()
		feature = np.squeeze(self.net.blobs[blob_name].data)
		return feature


  def post_process(self, scores, boxes, blob_name='fc7'):
    roi_boxes_and_scores = {}
    feature_vector = {}
    for cls_ind, cls_name in enumerate(cfg.CLASSES[1:]):
      cls_ind += 1 # skip bg   
      cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
      cls_scores = scores[:, cls_ind]
      roi_boxes_and_scores[cls_name] = \
        np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
      keep = nms(roi_boxes_and_scores[cls_name], cfg.TEST.NMS_THRESH)
      roi_boxes_and_scores[cls_name] = roi_boxes_and_scores[cls_name][keep, :]
      feature_vector[cls_name] = self.net.blobs[blob_name].data[keep]
      per_class_roi_index = np.where(roi_boxes_and_scores[cls_name][:, -1] >= cfg.TEST.CONF_THRESH)[0]
      if len(per_class_roi_index) == 0:
        roi_boxes_and_scores.pop(cls_name, None)
        feature_vector.pop(cls_name, None)
      else:
        roi_boxes_and_scores[cls_name] = roi_boxes_and_scores[cls_name][per_class_roi_index,:]
        feature_vector[cls_name] = feature_vector[cls_name][per_class_roi_index,:]

    """ 
    roi_boxes_and_scores = {}
    class_names = {}
    feature_vector = {}
    for cls_ind, cls_name in enumerate(cfg.CLASSES[1:]):
      cls_ind += 1 # skip bg   
      cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
      cls_scores = scores[:, cls_ind]
      roi_boxes_and_scores[cls_ind] = \
        np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
      keep = nms(roi_boxes_and_scores[cls_ind], cfg.TEST.NMS_THRESH)
      roi_boxes_and_scores[cls_ind] = roi_boxes_and_scores[cls_ind][keep, :]
      feature_vector[cls_ind] = self.net.blobs[blob_name].data[keep]
      class_names[cls_ind] = cls_name
      per_class_roi_index = np.where(roi_boxes_and_scores[cls_ind][:, -1] >= cfg.TEST.CONF_THRESH)[0]
      if len(per_class_roi_index) == 0:
        roi_boxes_and_scores.pop(cls_ind, None)
        feature_vector.pop(cls_ind, None)
      else:
        roi_boxes_and_scores[cls_ind] = roi_boxes_and_scores[cls_ind][per_class_roi_index,:]
        feature_vector[cls_ind] = feature_vector[cls_ind][per_class_roi_index,:]
    return class_names, roi_boxes_and_scores, feature_vector
    """

    return roi_boxes_and_scores, feature_vector


  # 10.202.4.219 black
  #fnt = PIL.ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 15)
  # 10.202.34.211 jang-ph
  fnt = PIL.ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 15)
  def draw_rois(self, im, roi_boxes_and_scores):
    # bgr2rgb
    im_rgb = im[:, :, (2, 1, 0)]
    im_pil = PIL.Image.fromarray(np.uint8(im_rgb)) 
    im_draw= PIL.ImageDraw.Draw(im_pil)
    for cls_name in roi_boxes_and_scores:
      roi_info = roi_boxes_and_scores[cls_name]
      for info in roi_info:
        bbox = info[:4]
        score= str(info[-1])
        im_draw.rectangle([bbox[0],  bbox[1],  bbox[2],  bbox[3]],  outline=(0,0,0))
        im_draw.rectangle([bbox[0]+2,bbox[1]+2,bbox[2]-2,bbox[3]-2],outline=(255,255,255))
        im_draw.text([bbox[0], bbox[1]], score, font=self.fnt, fill=(0,0,255))
        im_draw.text([bbox[0], bbox[1]+20], cls_name, font=self.fnt, fill=(0,0,255))

    return im_pil


"""
#prototxt = '/storage/ImageNet/ILSVRC2012/model/vgg/faster_rcnn_end2end/prototxt/test.prototxt'
#caffemodel = '/works/py_faster_rcnn/output/EXP_END2END_with_acc/voc_2007_trainval/vgg16_faster_rcnn_iter_70000.caffemodel'
#yaml_file = '/storage/ImageNet/ILSVRC2012/model/vgg/faster_rcnn_end2end/cfgs/faster_rcnn_end2end_test.yml'
yaml_file = '/storage/product/detection/11st_All/cfg/faster_rcnn_end2end_test.yml'
conf = conf(yaml_file, 1)
agent = agent()
import pdb; pdb.set_trace()
agent.im_detect('/works/caffe_build_sys_py/examples/images/cat.jpg')
class_names, roi_boxes_and_scores, feature_vectors = agent.detect('/works/caffe_build_sys_py/examples/images/cat.jpg')
feature = agent.extract_feature(blob_name='fc7')
roi_box_image = agent.draw_rois(agent.img, class_names, roi_boxes_and_scores)
roi_box_image.save('rectangle.png')
"""
