
#-*- coding: utf8 -*-
import sys
import numpy as np
import PIL.Image
import PIL.ImageDraw
PJT_PATH = '/home/taey16/'
CAFFE_ROOT = '{}/caffe/python'.format(PJT_PATH)
sys.path.insert(0, CAFFE_ROOT)
import caffe


class agent(object):
  default_args = {
    'model_def_file': ( 
      '{}/storage/models/inception5/inception5.prototxt'.format(PJT_PATH)),
    'pretrained_model_file': (
      '{}/storage/models/inception5/inception5.caffemodel'.format(PJT_PATH)),
    'gpu_mode': True, 'device_id': 0,
    'image_dim': 384, 'raw_scale': 255.,
  }


  def __init__(self, model_def_file, pretrained_model_file,
         raw_scale, image_dim, gpu_mode, device_id):
    if gpu_mode: 
      caffe.set_device(device_id)
      caffe.set_mode_gpu()
    else: caffe.set_mode_cpu()


    self.net = caffe.Classifier(
      model_def_file, pretrained_model_file,
      image_dims=(image_dim, image_dim), raw_scale=raw_scale,
      mean=np.array([104.0, 116.0, 122.0]), channel_swap=(2, 1, 0))


  def load_image(self, filename):
    try:
      image = caffe.io.load_image(filename)
      return image
    except Exception as err:
      print 'ERROR in agent.load_image ', err
      return None


  def load_image_roi(self, filename, roi, wrap_size=0):
    try:
      image = self.load_image(filename)
      roi_image = self.wrap_roi(image, roi, wrap_size)
      return roi_image
    except Exception as err:
      print 'ERROR in agent.load_image_roi ', err
      return None


  def wrap_roi(self, image, roi, wrap_size=0):
    # wrap roi region, following region-cnn
    if roi['x'] - wrap_size < 0: roi['x'] = 0 
    else: roi['x'] -= wrap_size
    if roi['y'] - wrap_size < 0: roi['y'] = 0 
    else: roi['y'] -= wrap_size
    if roi['x']+roi['width'] + wrap_size > image.shape[1]: 
      roi['width'] = image.shape[1]
    else: roi['width'] += wrap_size
    if roi['y']+roi['height'] + wrap_size > image.shape[0]: 
      roi['height'] = image.shape[0]
    else: roi['height'] += wrap_size
        
    roi_image = image[roi['y']:roi['y']+roi['height'], roi['x']:roi['x']+roi['width'],:]

    return roi_image

  
  def draw_roi(self, filename, roi, expend_border=0):
    try:
      image = self.load_image(filename)
      roi_image = self.wrap_roi(image, roi, expend_border)
      roi_image = caffe.io.resize_image(roi_image, (384, 384))

      roi_pil  = roi_image * 255.
      image_pil= image * 255.
      image_pil= PIL.Image.fromarray(np.uint8(image_pil))
      roi_pil  = PIL.Image.fromarray(np.uint8(roi_pil))
      dr_image = PIL.ImageDraw.Draw(image_pil)
      dr_image.rectangle(
        [roi['x'], 
         roi['y'], 
         roi['x']+roi['width'], 
         roi['y']+roi['height']], 
        outline=(0,0,255)
      )
      dr_image.text([roi['x'], roi['y']], 
        roi['confidence'], fill=(0,0,255))
      dr_image.text([roi['x'], roi['y']+40], 
        roi['category'], fill=(0,0,255))
      return roi_pil, image_pil
    except Exception as err:
      print 'ERROR in agent.draw_roi ', err
      return None


  def extract_feature(self, image, blob_name, oversample=True):
    try:
      scores = self.net.predict([image], oversample)
      if oversample:
        feature = np.reshape(np.squeeze(
          self.net.blobs[blob_name].data), (1,10*1024))
      else:
        feature = np.reshape(np.squeeze(
          self.net.blobs[blob_name].data), (1,1024))
      return feature
    except Exception as err:
      print('ERROR extract_feature: %s', err)
      return None

