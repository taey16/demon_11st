
#-*- coding: utf8 -*-

import sys
import os
import numpy as np
import cv2
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
        roi_boxes_and_scores[cls_ind] = []
      else:
        roi_boxes_and_scores[cls_ind] = roi_boxes_and_scores[cls_ind][per_class_roi_index,:]

    return class_names, roi_boxes_and_scores


  def vis_detections(self, im, class_name, roi_boxes_and_scores, fig_filename='example.png'):
    import matplotlib.pyplot as plt
    im = im[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    for cls_index, cls_name in class_name[1:]:
      cls_index += 1 
      dets = roi_boxes_and_scores[cls_index]
      #inds = np.where(dets[:, -1] >= cfg.TEST.CONF_THRESH)[0]
      if len(inds) == 0: continue

      #ax.imshow(im, aspect='equal')
      for i in inds:
        bbox = dets[i, :4]
        score= dets[i, -1]
        ax.add_patch(
          plt.Rectangle((bbox[0], bbox[1]),
                         bbox[2] - bbox[0],
                         bbox[3] - bbox[1], fill=False,
                         edgecolor='red', linewidth=3.5)
          )
        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(class_name, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')

    ax.set_title(('{} detections with ' 'p({} | box) >= {:.1f}').format( \
      class_name, class_name, thresh), fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(fig_filename)
    #plt.draw()


import pdb; pdb.set_trace()
#prototxt = '/storage/ImageNet/ILSVRC2012/model/vgg/faster_rcnn_end2end/prototxt/test.prototxt'
#caffemodel = '/works/py_faster_rcnn/output/EXP_END2END_with_acc/voc_2007_trainval/vgg16_faster_rcnn_iter_70000.caffemodel'
yaml_file = '/storage/ImageNet/ILSVRC2012/model/vgg/faster_rcnn_end2end/cfgs/faster_rcnn_end2end_test.yml'
conf = conf(yaml_file, 1)
agent = agent()
agent.im_detect('/works/caffe_build_sys_py/examples/images/cat.jpg')
class_names, roi_boxes_and_scores = agent.detect('/works/caffe_build_sys_py/examples/images/cat.jpg')
agent.vis_detections(agent.img, class_names, roi_boxes_and_scores)
