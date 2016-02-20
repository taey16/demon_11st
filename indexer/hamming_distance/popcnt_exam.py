#!/usr/bin/env python

import hamming_distance
import time
import numpy as np

# test popcnt
print('Test for hamming_distance.popcnt')
query = np.random.randint(0, 100000)
ref = np.random.randint(0,100000)
start = time.time()
diff = np.bitwise_xor(query,ref)
dist = hamming_distance.popcnt(diff)
elapsed = time.time() - start
print('%d in %.6f' % (dist, elapsed))


dimension = 320
query = np.zeros((1,dimension), dtype=np.uint64)
ref = np.ones((1,dimension), dtype=np.uint64)
print('Test for hamming_distance.hamming_distance')
start = time.time()
distance = hamming_distance.hamming_distance(query, ref)
elapsed = time.time() - start
print('%d in %.6f' % (distance, elapsed))


print('Test for hamming_distance.hamming_distance_ref')
num_ref = 1000000
ref = np.ones((num_ref,dimension), dtype=np.uint64)
dist= np.zeros((num_ref), dtype=np.uint32)
start = time.time()
#import pdb; pdb.set_trace()
ref[num_ref-1,dimension-1] = 0
ref[num_ref-1,dimension-2] = 0
ref[num_ref-1,dimension-3] = 0
ref[num_ref-2,dimension-3] = 0
hamming_distance.hamming_distance_ref(query, ref, dist)
elapsed = time.time() - start
print('distance of last two element: %d, %d in elapsed: %f ' % (dist[num_ref-1], dist[num_ref-2], elapsed))
#for d in dist:
#  print('%d ' % (d))
#print('elapsed: %f ' % (elapsed))



