
# -*- coding: UTF-8 -*-

from parser_11st import parser_11st

class parser_utils(parser_11st):

  def __init__(self):
    parser_11st.__init__(self)


  def generate_meta_dic(self):
    token_dict = dict()
    for idx in range(len(self.stringtoken_pattern_list)):
      v = self.stringtoken_list[idx]
      token_dict[v] = ''
    return token_dict


  def update_meta(self, meta, key, val):
    assert(key in meta.keys())
    meta[key] = val
    return meta


  def get_roi_meta_dic(self, object_roi):
    roi = {}
    roi['x'], roi['y'], \
    roi['width'], roi['height'], \
    roi['confidence'], roi['category'] = \
    int(object_roi[0]), int(object_roi[1]), \
    int(object_roi[2]), int(object_roi[3]), \
    str(object_roi[4]), str(object_roi[5])

    return roi


