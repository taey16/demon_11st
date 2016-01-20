
#-*- coding: utf8 -*-

import sys
import os
import cv2
import PIL.Image
import PIL.ImageDraw
import numpy as np
import _init_paths
from conf import conf
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
import caffe


class agent(object):


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


  def detect(self, image_path, proposal=None):
    scores, boxes = self.im_detect(image_path, proposal)
    if len(scores) == 0:
      print('ERROR in agent.detect (scores and boxes are all [])' )
      return [], []

    class_names, roi_boxes_and_scores = self.post_process(scores, boxes)
    return class_names, roi_boxes_and_scores


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
    feature = np.squeeze(self.net.blobs[blob_name].data)
    return feature


  def post_process(self, scores, boxes):
    roi_boxes_and_scores = {}
    class_names = {}
    roi_info = {}
    for cls_ind, cls_name in enumerate(cfg.CLASSES[1:]):
      cls_ind += 1 # skip bg   
      cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
      cls_scores = scores[:, cls_ind]
      roi_boxes_and_scores[cls_ind] = \
        np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
      keep = nms(roi_boxes_and_scores[cls_ind], cfg.TEST.NMS_THRESH)
      roi_boxes_and_scores[cls_ind] = roi_boxes_and_scores[cls_ind][keep, :]
      class_names[cls_ind] = cls_name
      per_class_roi_index = np.where(roi_boxes_and_scores[cls_ind][:, -1] >= cfg.TEST.CONF_THRESH)[0]
      if len(per_class_roi_index) == 0:
        #roi_boxes_and_scores[cls_ind] = []
        roi_boxes_and_scores.pop(cls_ind, None)
      else:
        roi_boxes_and_scores[cls_ind] = roi_boxes_and_scores[cls_ind][per_class_roi_index,:]

    return class_names, roi_boxes_and_scores


  def draw_rois(self, im, class_name, roi_boxes_and_scores):
    # bgr2rgb
    im_rgb = im[:, :, (2, 1, 0)]
    im_pil = PIL.Image.fromarray(np.uint8(im_rgb)) 
    im_draw= PIL.ImageDraw.Draw(im_pil)
    for cls_index in roi_boxes_and_scores:
      roi_info = roi_boxes_and_scores[cls_index]
      #if len(roi_info) == 0: continue
      # for each roi
      for info in roi_info:
        bbox = info[:4]
        score= str(info[-1])
        im_draw.rectangle([bbox[0], bbox[1], bbox[2], bbox[3]], outline=(0,0,0))
        im_draw.rectangle([bbox[0]+2, bbox[1]+2, bbox[2]-2, bbox[3]-2], outline=(255,255,255))
        im_draw.text([bbox[0], bbox[1]], score, fill=(0,0,255))
        im_draw.text([bbox[0], bbox[1]+20], class_name[cls_index], fill=(0,0,255))

    return im_pil


import pdb; pdb.set_trace()
#prototxt = '/storage/ImageNet/ILSVRC2012/model/vgg/faster_rcnn_end2end/prototxt/test.prototxt'
#caffemodel = '/works/py_faster_rcnn/output/EXP_END2END_with_acc/voc_2007_trainval/vgg16_faster_rcnn_iter_70000.caffemodel'
yaml_file = '/storage/ImageNet/ILSVRC2012/model/vgg/faster_rcnn_end2end/cfgs/faster_rcnn_end2end_test.yml'
conf = conf(yaml_file, 1)
agent = agent()
agent.im_detect('/works/caffe_build_sys_py/examples/images/cat.jpg')
class_names, roi_boxes_and_scores = agent.detect('/works/caffe_build_sys_py/examples/images/cat.jpg')
feature = agent.extract_feature(blob_name='fc7')
roi_box_image = agent.draw_rois(agent.img, class_names, roi_boxes_and_scores)
roi_box_image.save('rectangle.png')
