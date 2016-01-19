# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Set up paths for Fast R-CNN."""

import os.path as osp
import sys

def add_path(path):
  if path not in sys.path:
    sys.path.insert(0, path)


# Add caffe to PYTHONPATH
#caffe_path = osp.join(this_dir, '..', 'caffe-fast-rcnn', 'python')
caffe_path = osp.join('/works/caffe_build_sys_py/python')
add_path(caffe_path)
print('caffe_path: %s' % caffe_path)

# Add lib to PYTHONPATH
lib_path = osp.join('/works/py_faster_rcnn/lib')
add_path(lib_path)
print('faster_rcnn_path: %s' % lib_path)

