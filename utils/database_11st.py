
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


  def update(self, entries, set_id):
    for entry in entries:
      try:
        #sql = "UPDATE %s SET dataset=\'11st_julia\' WHERE __org_img_url__ = \'%s\'" % \
        #  (self.table_name, entry['__org_img_url__'])
        sql = "UPDATE %(table)s SET set_id = %(set_id)d WHERE __org_img_url__ = \'%(url)s\'" % \
          {'table': self.table_name, 'url': entry[0], 'set_id': set_id}
        print sql
        sys.stdout.flush()
        self.cur.execute("SET NAMES \'utf8\'")
        self.cur.execute(sql)
        #time.sleep(0.01)
      except Exception as e:
        print('ERROR update %s' % entry['__org_img_url__'], e)


  def select(self, condition):
    try:
      sql = "SELECT __org_img_url__ FROM %(table)s WHERE label = 0 ORDER BY rand(123)" % \
        {'table': self.table_name}
      print sql 

      self.cur.execute(sql)
      entries = self.cur.fetchall()
    except Exception as e:
      print('ERROR select %s' % entry['__org_img_url__'], e)
      entries = None

    return entries

