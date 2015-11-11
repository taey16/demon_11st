#-*- coding: utf-8 -*-
'''
Created on 2014. 8. 28.

@author: fantajeon
'''

import urllib3
import cStringIO
import json
import Image
import math
import os.path
import os
import thread
import threading
import time
import certifi
import sys
import cgi
import posixpath
import urlparse



num_workers = 16
http = urllib3.PoolManager(num_pools=num_workers,
                           cert_reqs='CERT_REQUIRED',
                           ca_certs=certifi.where())

''' 주어진 url로 부터, 해상도 정규화를 진행하고 파일로 저장한다.
  Step 1: url을 tmp_filename으로 저장한다
        step 1: url의 .jpg, .png .jpeg가 있는 지 확인한다.
        step 2: tmp_filename에 확장자를 덧붙여서 저장한다.
  Step 2: Image로 영상파일을 메모리로 읽어 들인다.
  Step 3: 영상을 해상도 축소를 한다(만약 640보다 크다면)
  Step 4: jpg로 저장한다. '''
def save_imageurl(image_url, tmp_filename, local_filename):
    ''' (image url, local_filename)->True or False '''

    print("[BEGIN] save images[%s]->[%s]"%(image_url, local_filename))
    if( image_url[-1] == '/') :
        return False
    try:
        image_url = image_url.encode('utf-8').strip()
        print('connecting - Request: %s'%(image_url))

        response = http.request('GET', image_url)
        print('recv url data')
        data = response.data
        if data is None:
            response.release_conn()
            return False

        _, content_disposition = cgi.parse_header(response.headers.get('Content-Disposition', ''))
        content_type = cgi.parse_header(response.headers.get('content-type', ''))
        content_type = content_type[0].lower()

        response.release_conn()
        print("http headers: %s"%(response.headers))
        print("content-disposition; %s"%(content_disposition))
        print("content-type: %s"%(content_type))

        if len(content_disposition) == 0 or content_disposition["filename"] is None:
            path = urlparse.urlsplit(image_url).path
            cgi_filename = posixpath.basename(path)
        else:
            cgi_filename =  content_disposition["filename"].lower()

        # check file extention
        if content_type == "image/jpeg" or content_type == "image/jpg":
            req_ext = ".jpg"
        elif content_type == "image/png":
            req_ext = ".png"
        else:
            print('Reject file format request content-type[%s] : [%s->%s]'%(content_type, image_url,cgi_filename))
            return False

        print("save [%s] from [%s(%s)]"%(tmp_filename, cgi_filename, image_url))
        img_tmpname = "%s%s"%(tmp_filename, req_ext,)   # temporary file name
        img_fname = local_filename   # to save file name
        img_fp = open(img_tmpname, "wb")
        img_fp.write(data)
        img_fp.close()


        print("resize with open")
        im1 = Image.open(img_tmpname)
        (width,height) = im1.size   # get the size of the image
        if( width > height ):
            longest_axis=width
        else:
            longest_axis=height

        if( longest_axis > 640 ) :
            r = 640.0/longest_axis
            print("resize1=%f"%(r))
            sz = ( int(math.floor( width*r )), int(math.floor(height*r)) )
            #print("resize2")
            print("resize[%dx%d]"%(sz[0],sz[1]))
            im2 = im1.resize( sz, Image.BILINEAR )
            print("resize2")
            im2.save(img_fname,format='JPEG')
        else:
            im1.save(img_fname,format='JPEG')
            #im2.close()
        #Image.close()

        return True
    except (IOError) as e:
        print("image url error [%s]"%(image_url))
        return False
    except:
        raise

if __name__ == '__main__':
    os.environ['http_proxy'] = ''
    for x in range(len(sys.argv)):
        print("argv[%d]=%s",x, sys.argv[x])

    """ command 사용 예시: /usr/anaconda/bin/python "saveurlimage.py" "http://cfile224.uf.daum.net/image/264FEF4C52C1891935723E" ./tmp to2.jpg """
    if save_imageurl(sys.argv[1], sys.argv[2], sys.argv[3]):
        print("[OK]")
    else:
        print("[Failed]")
