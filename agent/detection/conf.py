
#-*- coding: utf8 -*-
import numpy as np
from easydict import EasyDict as edict
from fast_rcnn.config import cfg, cfg_from_file, cfg_from_list


class conf:

  def __init__(self, _yaml_file=None, _gpu_id=None):
  #def __init__(self, _prototxt=None, _caffemodel=None, _yaml_file=None, _gpu_id=None):
  #  assert(_prototxt)
  #  assert(_caffemodel)
    assert(_yaml_file)
    #self.prototxt = _prototxt
    #self.caffemodel = _caffemodel
    self.yaml_file = _yaml_file
    self.mean_value = np.zeros((1, 1, 3)).astype(np.float32)
    self.mean_value[0,0,0] = 102.9801
    self.mean_value[0,0,1] = 115.9465
    self.mean_value[0,0,2] = 122.7717
    if _gpu_id == None:
      self.use_gpu = False
      self.gpu_id = -1
    else:
      self.use_gpu = True
      self.gpu_id = _gpu_id

    cfg_from_file(self.yaml_file)

    cfg.USE_GPU= self.use_gpu
    cfg.GPU_ID = self.gpu_id
    #cfg[cfg.PHASE].PROTOTXT = self.prototxt
    #cfg[cfg.PHASE].CAFFE_MODEL = self.caffemodel
    cfg.CLASSES = ('__background__',
                   'aeroplane', 'bicycle', 'bird', 'boat',
                   'bottle', 'bus', 'car', 'cat', 'chair',
                   'cow', 'diningtable', 'dog', 'horse',
                   'motorbike', 'person', 'pottedplant',
                   'sheep', 'sofa', 'train', 'tvmonitor')


    """
    self.cfg = edict({
      'USE_GPU_NMS': True, 
      'ROOT_DIR': '/home/taey16/Documents/py_faster_rcnn', 
      'USE_GPU': USE_GPU,
      'GPU_ID': GPU_ID, 
      'EPS': 1e-14, 
      'RNG_SEED': 3, 
      'TEST': {
        'PROPOSAL_METHOD': 'selective_search', 
        'SVM': False, 
        'NMS': 0.3, 
        'RPN_NMS_THRESH': 0.7, 
        'SCALES': [600], 
        'RPN_POST_NMS_TOP_N': 300, 
        'HAS_RPN': True, 
        'RPN_PRE_NMS_TOP_N': 6000, 
        'BBOX_REG': True, 
        'RPN_MIN_SIZE': 16, 
        'MAX_SIZE': 1000,
        'PROTOTXT': _prototxt,
        'CAFFE_MODEL': _caffemodel
      }, 
      'TRAIN': {
        'RPN_BBOX_INSIDE_WEIGHTS': [1.0, 1.0, 1.0, 1.0], 
        'PROPOSAL_METHOD': 'gt', 
        'SNAPSHOT_ITERS': 10000, 
        'RPN_POST_NMS_TOP_N': 2000, 
        'RPN_PRE_NMS_TOP_N': 12000, 
        'BBOX_REG': True, 
        'IMS_PER_BATCH': 1, 
        'RPN_FG_FRACTION': 0.5, 
        'BBOX_NORMALIZE_STDS': [0.1, 0.1, 0.2, 0.2], 
        'BATCH_SIZE': 128, 
        'ASPECT_GROUPING': True, 
        'USE_PREFETCH': False, 
        'BG_THRESH_LO': 0.1, 
        'FG_THRESH': 0.5, 
        'MAX_SIZE': 1000, 
        'BBOX_THRESH': 0.5, 
        'BG_THRESH_HI': 0.5, 
        'SCALES': [600], 
        'BBOX_NORMALIZE_TARGETS': True, 
        'BBOX_NORMALIZE_TARGETS_PRECOMPUTED': True, 
        'FG_FRACTION': 0.25, 
        'BBOX_NORMALIZE_MEANS': [0.0, 0.0, 0.0, 0.0], 
        'RPN_BATCHSIZE': 256, 
        'SNAPSHOT_INFIX': '', 
        'RPN_POSITIVE_WEIGHT': -1.0, 
        'RPN_NMS_THRESH': 0.7, 
        'USE_FLIPPED': True, 
        'BBOX_INSIDE_WEIGHTS': [1.0, 1.0, 1.0, 1.0], 
        'RPN_CLOBBER_POSITIVES': False, 
        'RPN_NEGATIVE_OVERLAP': 0.3, 
        'HAS_RPN': True, 
        'RPN_MIN_SIZE': 16, 
        'RPN_POSITIVE_OVERLAP': 0.7,
        'PROTOTXT': _prototxt,
        'CAFFE_MODEL': _caffemodel
      }, 
      'PHASE': 'TEST', 
      'EXP_DIR': 'faster_rcnn_end2end', 
      'PIXEL_MEANS': self.mean_value, 
      'DEDUP_BOXES': 0.0625,
    })
    """


