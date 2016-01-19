
import os.path as osp
import sys

def add_path(path):
  if path not in sys.path:
    sys.path.insert(0, path)


# Add caffe to PYTHONPATH
lib_path = osp.join('/works/', 'caffe_build_sys_py', 'python')
add_path(lib_path)
print('add path: %s' % lib_path)

# Add lib to PYTHONPATH
lib_path = osp.join('/works/py_faster_rcnn/lib/fast_rcnn')
add_path(lib_path)
print('add path: %s' % lib_path)

#lib_path = osp.join('/works/py_faster_rcnn/lib/utils')
#add_path(lib_path)
#print('add path: %s' % lib_path)

