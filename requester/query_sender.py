
# coding: utf8

import urllib2
import json
import io
input_path = '/storage/attribute/PBrain_all.csv'
output_path = input_path + '.result'
machine_prefix = 'http://10.202.34.211:8081/request_handler'
url_prefix = 'url=http://i.011st.com'
i=0
urls = io.open(input_path,'r')
output=io.open(output_path+'.'+i,'w')
for url in urls:
  try:
    # get json object
    response = urllib2.urlopen(machine_prefix+url_prefix+url)
    # read json object into managable json object in python
    retrieved_items = json.loads(response.read())
    output.write(unicode(json.dumps(retrieved_items)))
    # print retrieved_items
    i += 1
    print i
    output.write(unicode('\n'))
    if i%250==0:
      output.close()
      output = io.open(output_path,'a')
    if i % 10000=0:
      output.close()
      output = io.open(output_path+'.'+i,'w')
  except urllib2.HTTPError, err:
    if err.code == 404:
      print "Page not found!"
      continue
    elif err.code == 403:
      print "Access denied!"
      continue
    else:
      print "Something happened! Error code", err.code
      continue
  except urllib2.URLError, err:
    print "Some other error happened:", err.reason
    continue
#output.write(']')
output.close()
