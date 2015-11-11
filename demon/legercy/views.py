#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import time
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from simple_prj.settings import BASE_DIR
import urllib3

import os
# import cv
# import opencv
# from opencv import cv
# from opencv import highgui
import json
import certifi

import PIL
from PIL import Image
import requests
from io import BytesIO
from urlparse import urlparse
from binascii import a2b_base64
import base64
import binascii
import ctypes
import cStringIO as StringIO
import cgi
import sys


# from simple_prj.settings import imageserach_proxy
from imagesearch_client import *
from simple_prj.settings import socket_file as fastfashion_socket_file
from simple_prj.settings import normaldataset_socket_file as normaldataset_socket_file
from simple_prj.settings import shoesdataset_socket_file as shoesdataset_socket_file
from simple_prj.settings import shoesdataset2_socket_file as shoesdataset2_socket_file

# from simple_prj.settings import imageserach_normal_proxy

# SKPLIBRARY_DIR = os.path.abspath(os.path.dirname('../'))
# logging.info('SKPLIBRARY_DIR:{}'.format(SKPLIBRARY_DIR))
# sys.path.append(SKPLIBRARY_DIR)






num_workers = 7
http = urllib3.PoolManager(num_pools=num_workers,
                           cert_reqs='CERT_REQUIRED',
                           ca_certs=certifi.where())




def parsing_imagedataurl(req_url):
    up = urlparse(req_url)
    try:
        head, data = up.path.split(',')
        bits = head.split(';')
        
        data = data.replace('\n', '')
        data = data.replace(' ', '+')
        mime_type = bits[0] if bits[0] else 'text/plain'
        print("mime_type: {}".format(mime_type))
        #     for v in data:
        #         if v == '+':
        #             print("found!!")
        #     print("contents: {}".format(data))
        
        charset, b64 = 'ASCII', False
        for bit in bits:
            if bit.startswith('charset='):
                charset = bit[8:]
            elif bit == 'base64':
                b64 = True
    except ValueError as err:
        return None, None, None, None
    
    return mime_type, charset, b64, data
   
                              
def getstringbuffer(image_url):
    mime_type, _, b64, urldata = parsing_imagedataurl(image_url)
    if mime_type is None:
        logging.info("http.request: {} SSS".format(image_url))
        response = http.request('GET', image_url, preload_content=True)
        logging.info("http.request: {} EEE".format(image_url))
        remote_response_code = response.status
        if response.status != 200:
            raise Exception("urllib3", 'connection failed, status: {}'.format(response.status))

        logging.info("response.read(): status:{}, headers:{}".format(remote_response_code, response.headers))
        response.read()
        data = response.data
        logging.info("Data Length: {}".format(len(data)))
        
        _, content_disposition = cgi.parse_header(response.headers.get('Content-Disposition', ''))
        content_type = cgi.parse_header(response.headers.get('content-type', ''))
        content_type = content_type[0].lower()
    else:
        if b64:
            data = base64.b64decode(urldata)
        else:
            data = urldata
        content_type = mime_type
       
    logging.info("content-type of {}: {}".format(image_url, content_type))
    if content_type == "image/jpeg" or content_type == "image/jpg":
        req_ext = ".jpg"
    elif content_type == "image/png":
        req_ext = ".png"
    else:
        req_ext = ""
       
    logging.info("req_ext of {}: {}".format(image_url, req_ext))

    string_buffer = StringIO.StringIO(data);
    return string_buffer, data, req_ext
                           
def convert_encoding(data, encoding='ascii'):
    if isinstance(data, dict):
        return dict((convert_encoding(key), convert_encoding(value)) \
             for key, value in data.iteritems())
    elif isinstance(data, list):
        return [convert_encoding(element, encoding) for element in data]
    elif isinstance(data, unicode):
#         return data.encode(encoding, errors='ignore')
#         print("data:%s"%(data))
#         return data.encode(encoding)
#         print("str(%s)=%d"%(str,isinstance(str,unicode)))
        return "%s" % (data,)
#         return data.encoding(encoding)
    else:
        return data
                            
def readJson(filename):
    fp = open(filename, 'rt')
    data = fp.read()
    fp.close()
    return data
    
    
# Create your views here.
def index(request):
    logging.info("request:{}".format(request))
    return HttpResponse("Hello, world. You're at the polls index.")
    
# Create your views here.
def retrieval_normal_db(request):
    logging.info("request:{}".format(request))
    logging.info("parsing")
    jsondata = '{result: False}'
    try:
        imagesearch_proxy = ImageSearchProxy(normaldataset_socket_file)

        request_category = request.GET.get('category', '').encode('utf-8')
        request_imageurl = request.GET.get('queryurl', '').encode('utf-8')
        logging.info("==============request_category:{}\nrequest_imageurl:{}".format(request_category, request_imageurl))
        
        string_buffer, img_rawdata, img_ext = getstringbuffer(request_imageurl)
        img = Image.open(string_buffer)
        
        filename_ = str(datetime.datetime.now()).replace(' ', '_')
        filename = os.path.join('/tmp/11st_upload', '{}{}'.format(filename_, img_ext))
        img_fp = open(filename, "wb")
        img_fp.write(img_rawdata)
        img_fp.close()
        
        logging.info( "Request: 163")
        retrieval_data = imagesearch_proxy.Retrieval(filename, request_category)
        logging.info( "[Before] retrieval_data of normal database:{}\n".format(retrieval_data) )
        if retrieval_data['result']:
            logging.info( "Request: True")
            retrieval_data['query'] = request_imageurl            
            
        retrieval_data['request_category'] = request_category.decode('utf-8')
        logging.info( "retrieval_data:{}\n".format(retrieval_data) )
        data = convert_encoding(retrieval_data, 'utf-8')
        jsondata = json.dumps(data, encoding='utf-8', ensure_ascii=False, indent=None)
    except Exception as e:
        logging.info("exception: {}".format(e))
        raise e    
#     jsondata = readJson(os.path.join(BASE_DIR, 'retrieval.json'))
    response = HttpResponse(jsondata, content_type='application/json');
    response['Access-Control-Allow-Origin'] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"  
    response["Access-Control-Allow-Headers"] = "origin, x-requested-with, content-type, accept"
    # response["Access-Control-Allow-Credentials"] = "true"
    return response
    
    
# Create your views here.
def retrieval(request):
    logging.info("request:{}".format(request))
    logging.info("parsing")
    jsondata = '{result: False}'
    try:
        imageserach_proxy = ImageSearchProxy(fastfashion_socket_file)
        
        request_category = request.GET.get('category', '').encode('utf-8')
        request_imageurl = request.GET.get('queryurl', '').encode('utf-8')
        logging.info("==============request_category:{}\nrequest_imageurl:{}".format(request_category, request_imageurl))
        
        string_buffer, img_rawdata, img_ext = getstringbuffer(request_imageurl)
        img = Image.open(string_buffer)
        
        filename_ = str(datetime.datetime.now()).replace(' ', '_')
        filename = os.path.join('/tmp/11st_upload', '{}{}'.format(filename_, img_ext))
        img_fp = open(filename, "wb")
        img_fp.write(img_rawdata)
        img_fp.close()
        
        logging.info( "Request: 163")
        retrieval_data = imageserach_proxy.Retrieval(filename, request_category)
        logging.info( "[Before] retrieval_data:{}\n".format(retrieval_data) )
        if retrieval_data['result']:
            logging.info( "Request: True")
            retrieval_data['query'] = request_imageurl
            
        retrieval_data['request_category'] = request_category.decode('utf-8')
        logging.info( "retrieval_data:{}\n".format(retrieval_data) )
        data = convert_encoding(retrieval_data, 'utf-8')
        jsondata = json.dumps(data, encoding='utf-8', ensure_ascii=False, indent=None)
    except Exception as e:
        logging.info("exception: {}".format(e))
        raise e    
#     jsondata = readJson(os.path.join(BASE_DIR, 'retrieval.json'))
    response = HttpResponse(jsondata, content_type='application/json');
    response['Access-Control-Allow-Origin'] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"  
    response["Access-Control-Allow-Headers"] = "origin, x-requested-with, content-type, accept"
    # response["Access-Control-Allow-Credentials"] = "true"
    return response

def retrieval_shoes_db(request):
    logging.info("request:{}".format(request))
    logging.info("parsing")
    jsondata = '{result: False}'
    try:
        imagesearch_proxy = ImageSearchProxy(shoesdataset_socket_file)

        request_category = request.GET.get('category', '').encode('utf-8')
        request_imageurl = request.GET.get('queryurl', '').encode('utf-8')
        logging.info("==============request_category:{}\nrequest_imageurl:{}".format(request_category, request_imageurl))
        
        string_buffer, img_rawdata, img_ext = getstringbuffer(request_imageurl)
        img = Image.open(string_buffer)
        
        filename_ = str(datetime.datetime.now()).replace(' ', '_')
        filename = os.path.join('/tmp/11st_upload', '{}{}'.format(filename_, img_ext))
        img_fp = open(filename, "wb")
        img_fp.write(img_rawdata)
        img_fp.close()
        
        logging.info( "Request: 163")
        retrieval_data = imagesearch_proxy.Retrieval(filename, request_category)
        logging.info( "[Before] retrieval_data of normal database:{}\n".format(retrieval_data) )
        if retrieval_data['result']:
            logging.info( "Request: True")
            retrieval_data['query'] = request_imageurl            
            
        retrieval_data['request_category'] = request_category.decode('utf-8')
        logging.info( "retrieval_data:{}\n".format(retrieval_data) )
        data = convert_encoding(retrieval_data, 'utf-8')
        jsondata = json.dumps(data, encoding='utf-8', ensure_ascii=False, indent=None)
    except Exception as e:
        logging.info("exception: {}".format(e))
        raise e    
#     jsondata = readJson(os.path.join(BASE_DIR, 'retrieval.json'))
    response = HttpResponse(jsondata, content_type='application/json');
    response['Access-Control-Allow-Origin'] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"  
    response["Access-Control-Allow-Headers"] = "origin, x-requested-with, content-type, accept"
    # response["Access-Control-Allow-Credentials"] = "true"
    return response

def retrieval_shoes2_db(request):
    logging.info("request:{}".format(request))
    logging.info("parsing")
    jsondata = '{result: False}'
    try:
        imagesearch_proxy = ImageSearchProxy(shoesdataset2_socket_file)

        request_category = request.GET.get('category', '').encode('utf-8')
        request_imageurl = request.GET.get('queryurl', '').encode('utf-8')
        logging.info("==============request_category:{}\nrequest_imageurl:{}".format(request_category, request_imageurl))
        
        string_buffer, img_rawdata, img_ext = getstringbuffer(request_imageurl)
        img = Image.open(string_buffer)
        
        filename_ = str(datetime.datetime.now()).replace(' ', '_')
        filename = os.path.join('/tmp/11st_upload', '{}{}'.format(filename_, img_ext))
        img_fp = open(filename, "wb")
        img_fp.write(img_rawdata)
        img_fp.close()
        
        logging.info( "Request: 163")
        retrieval_data = imagesearch_proxy.Retrieval(filename, request_category)
        logging.info( "[Before] retrieval_data of normal database:{}\n".format(retrieval_data) )
        if retrieval_data['result']:
            logging.info( "Request: True")
            retrieval_data['query'] = request_imageurl            
            
        retrieval_data['request_category'] = request_category.decode('utf-8')
        logging.info( "retrieval_data:{}\n".format(retrieval_data) )
        data = convert_encoding(retrieval_data, 'utf-8')
        jsondata = json.dumps(data, encoding='utf-8', ensure_ascii=False, indent=None)
    except Exception as e:
        logging.info("exception: {}".format(e))
        raise e    
#     jsondata = readJson(os.path.join(BASE_DIR, 'retrieval.json'))
    response = HttpResponse(jsondata, content_type='application/json');
    response['Access-Control-Allow-Origin'] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"  
    response["Access-Control-Allow-Headers"] = "origin, x-requested-with, content-type, accept"
    # response["Access-Control-Allow-Credentials"] = "true"
    return response

