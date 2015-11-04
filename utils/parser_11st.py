
# coding: utf8

import re

class parser_11st:

  stringtoken_list = \
    ['<__tag__>',
     '<__prd_no__>',
     '<__gender_ctgr__>', 
     '<__lctgr_no__>', 
     '<__mctgr_no__>', 
     '<__sctgr_no__>', 
     '<__dctgr_no__>', 
     '<__lctgr_nm__>', 
     '<__mctgr_nm__>', 
     '<__sctgr_nm__>', 
     '<__dctgr_nm__>', 
     '<__org_img_url__>', 
     '<__seller_no__>', 
     '<__seller_nm__>', 
     '<__seller_score__>', 
     '<__prd_nm__>', 
     '<__object_roi__>',
     '<__local_name__>' ]
  stringtoken_pattern_list = []

  
  def __init__(self):
    for strtoken_index in range(len(self.stringtoken_list)):
      v = self.stringtoken_list[strtoken_index]
      v = v[1:(len(v)-1)]
      self.stringtoken_list[strtoken_index] = v
      pattern_string = r"<{}>(?P<keyword>.*?)(<|$)".format(v,v)
      p=re.compile(pattern_string)
      self.stringtoken_pattern_list.append(p)

 
  def TokennizeIntoDict(self, line):
    token_dict = dict()
    for idx in range(len(self.stringtoken_pattern_list)):
      v = self.stringtoken_list[idx]
      p = self.stringtoken_pattern_list[idx]
      m = p.search(line)
      if m is not None:
        token_dict[v] = m.group('keyword').strip()
    return token_dict
 

  def parse(self, meta_data_path): 
    data = []
    with open(meta_data_path, 'rt') as src_fp:
      src_fp.readline()
      for line in src_fp:
        data.append(self.TokennizeIntoDict(line))
        #product_no = item['__prd_no__']
        #image_url = item['__org_img_url__']

    return data

