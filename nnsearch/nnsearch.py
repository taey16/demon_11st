
#-*-coding: utf-8 -*-
import numpy as np
import io
import json

try:
	input_file = io.open('result_log_test.log','r')
	output_file = io.open('filtered_result.log','w')
	retrieved_items = []
	i=0
	for line in input_file:
		retrieved_items.append(json.loads(line))
		i+=1
		print i
	import pdb;pdb.set_trace()
	for item in retrieved_items:
		del item['retrieved_item']
	output_file.write(unicode(json.dumps(retrieved_items)))
	#attr_words = retrieved_items['sentence'][0]
	#detect_words = retrieved_items['feature'].keys()
	#print attr_words
	#print detect_words
	output_file.close()
except Exception as err:
	print err
