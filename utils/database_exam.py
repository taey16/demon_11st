
# -*- coding: UTF-8 -*-

from database_11st import database_11st
import MySQLdb


import pdb; pdb.set_trace()
meta_filename = '/storage/product/11st_julia/example_metadata.txt'
#meta_filename = '/storage/product/11st_julia/october_11st_metadata.txt'
database = database_11st()
meta = database.parse(meta_filename)
database.connect('10.202.211.120', 3307, 'taey16', 'Skp02596', '11st_julia')
database.insert(meta, 
  ['__prd_no__', 
   '__prd_nm__', 
   '__org_img_url__',
   '__tag__',
   '__lctgr_no__',
   '__lctgr_nm__', 
   '__mctgr_no__',
   '__mctgr_nm__',
   '__sctgr_no__',
   '__sctgr_nm__',
   '__gender_ctgr__'],
   True)
