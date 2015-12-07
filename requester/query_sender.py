
# coding: utf8

import urllib2
import json

#url = 'http://175.126.56.112:15002/url_request_handler?category=127681&url=http://i01.i.aliimg.com/wsphoto/v0/765356643/Hot-sale-Free-shipping-2014-Fashion-Good-font-b-Quality-b-font-Cotton-T-font-b.jpg'
#url = 'http://175.126.56.112:15002/url_request_handler?category=127687&url=https://s-media-cache-ak0.pinimg.com/736x/e3/40/28/e34028c15d0b10064d64a4defe63f7ec.jpg'
url = 'http://175.126.56.112:15002/url_request_handler?category=1530&url=http%3A%2F%2Fimage.gsshop.com%2Fimage%2F15%2F53%2F15537256_L1.jpg'
#url = 'http://175.126.56.112:8080/mosaic_request_handler?url=http://i.011st.com/aj/0/6/9/0/5/0/1213069050_L300.jpg'

try:
  import pdb; pdb.set_trace()
  # get json object
  response = urllib2.urlopen(url)
  # read json object into managable json object in python
  retrieved_items = json.loads(response.read())

  # print retrieved_items
  for meta in retrieved_items['retrieval_list']:
    print meta

  print 'keys, {}'.format(retrieved_items.keys())
  print 'request_category,', retrieved_items['request_category']
  print 'query,', retrieved_items['query']
  print '# of retrieved items,', len(retrieved_items['retrieval_list'])
  print 'result,', retrieved_items['result']

except urllib2.HTTPError, err:
  if err.code == 404:
    print "Page not found!"
  elif err.code == 403:
    print "Access denied!"
  else:
    print "Something happened! Error code", err.code
except urllib2.URLError, err:
  print "Some other error happened:", err.reason

