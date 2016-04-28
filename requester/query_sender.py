
# coding: utf8

import sys
import urllib2
import json
import io

input_path = \
  '/storage/attribute/PBrain_all_2800001_3000000.csv'
  #'/storage/attribute/PBrain_all_2600001_2800000.csv'
  #'/storage/attribute/PBrain_all_2400001_2600000.csv'
  #'/storage/attribute/PBrain_all_2200001_2400000.csv'
  #'/storage/attribute/PBrain_all_2000001_2200000.csv'
  #'/storage/attribute/PBrain_all_1800001_2000000.csv'
  #'/storage/attribute/PBrain_all_1600001_1800000.csv'
  #'/storage/attribute/PBrain_all_1400001_1600000.csv'
  #'/storage/attribute/PBrain_all_1200001_1400000.csv'
  #'/storage/attribute/PBrain_all_1000001_1200000.csv'
  #'/storage/attribute/PBrain_all_0800001_1000000.csv'
  #'/storage/attribute/PBrain_all_0600001_0800000.csv'
  #'/storage/attribute/PBrain_all_0400001_0600000.csv'
  #'/storage/attribute/PBrain_all_0200001_0400000.csv'
  #'/storage/attribute/PBrain_all_0000001_0200000.csv'
host_ip = \
  '10.202.34.211'
  #'10.202.34.172'
port = \
  7081
  #8081
  #6081


machine_prefix = \
  'http://%s:%d/request_handler?url=http://i.011st.com/%%s' % (host_ip, port)


#import pdb; pdb.set_trace()
urls = io.open(input_path, 'r')
success_counter = 0
output_json_filename = '%s.%04d.json' % (input_path, success_counter)
output_fp = io.open(output_json_filename, 'w')
for url in urls:
  try:
    url = str(url.strip())
    # get json object
    response = urllib2.urlopen(machine_prefix % url)
    # read json object into managable json object in python
    retrieved_items = json.loads(response.read())
    output_fp.write(unicode(json.dumps(retrieved_items)))
    output_fp.write(unicode('\n'))
    success_counter += 1

    if success_counter % 100 == 0:
      print('%d th image complete' % success_counter)
      sys.stdout.flush()

    if success_counter % 10000 == 0:
      output_fp.close()
      print('SUCCESS processing %s' % output_json_filename)
      sys.stdout.flush()
      output_json_filename = '%s.%04d.json' % (input_path, success_counter)
      output_fp = io.open(output_json_filename, 'w')
       

  except urllib2.HTTPError, err:
    if err.code == 404:
      print "ERROR page not found!"
      continue
    elif err.code == 403:
      print "ERROR Access denied!"
      continue
    else:
      print "ERROR Something happened! processing %s, Error code" % url, err.code
      continue
  except urllib2.URLError, err:
    print "ERROR Some other error processing %s, happened:" % url, err.reason
    continue

output.close()
print('SUCCESS processing %s' % output_json_filename)
