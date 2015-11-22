
# -*- coding: UTF-8 -*-

from parser_11st import parser_11st
import MySQLdb

class database_11st(parser_11st):


  def __init__(self):
    parser_11st.__init__(self)
    self.field_list = \
      [field for field in self.stringtoken_list[0:-3]]
    self.field_names= ','.join(self.field_list)


  def connect(self, host, port, user, p, 
              table_name, db='PBrain'):
    self.db = MySQLdb.connect(host, user, p, db, port)
    self.cur= db.cursor()
    self.table_name = table_name


  def insert(self, entries):
    for entry in entries:
      k_v_pair = ""
      for attr, val in entry.iteritems():
        k_v_pair += "%s = %s," % (attr, val) 
      sql = "INSERT %s set %s" % (self.table_name, k_v_pair[:-1])
      print sql
      k_v_pair = ''

