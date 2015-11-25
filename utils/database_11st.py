
# -*- coding: UTF-8 -*-

from parser_11st import parser_11st
import MySQLdb
import sys
import time

class database_11st(parser_11st):


  def __init__(self):
    parser_11st.__init__(self)
    self.field_list = \
      [field for field in self.stringtoken_list[0:-3]]
    self.field_names= ','.join(self.field_list)


  def connect(self, host, port, user, p, 
              table_name, db='PBrain'):
    try:
      self.db = MySQLdb.connect(host, user, p, db, port)
      self.cur= self.db.cursor()
      self.cur.execute("SET NAMES \'utf8\'")
      self.table_name = table_name
      print('MySQLdb.connect established') 
    except Exception as e:
      print('ERROR MySQLdb.connect ', e) 
      sys.exit(-1)


  def insert(self, entries, attr, commit=False):
    for entry in entries:
      try:
        k_v_pair = ''
        for field_name in attr:
          value = entry[field_name].strip().replace('"', '')
          k_v_pair += '%s = \"%s\",' % (field_name, value) 
        sql = 'INSERT %s SET %s' % (self.table_name, k_v_pair[:-1])
        print sql
        sys.stdout.flush()
        self.cur.execute("SET NAMES \'utf8\'")
        self.cur.execute(sql)
        #time.sleep(0.01)
      except Exception as e:
        print('ERROR insert %s' % entry['__prd_no__'], e)

    if commit: self.db.commit()


