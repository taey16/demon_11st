
from database_11st import database_11st
import MySQLdb


import pdb; pdb.set_trace()
meta_filename = '/storage/product/11st_julia/october_11st_metadata.txt'
database = database_11st()
meta = database.parse(meta_filename)
database.connect('10.202.211.120', 3307, 'taey16', 'Skp02596', '11st_julia')
database.insert(meta, True)
