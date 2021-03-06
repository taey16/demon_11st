
import numpy as np
import cPickle as pickle
import logging
import sys
c_hamming_distance_module = '/works/demon_11st/index/hamming_distance'
sys.path.append(c_hamming_distance_module)
import hamming_distance

class indexer:
  # generate N bit lookup table
  lookup = np.asarray([bin(i).count('1') for i in range(1<<16)])
  #index_key = ['1612', '1645', '127681', '127687', '1530']


  def __init__(self, index_key, num_max_item):
    self.index_key = []
    self.database = {}

    for k, n in zip(index_key, num_max_item):
      self.index_key.append(k)
      self.database[k] = {}
      self.database[k]['meta'] = [None] * n
      self.database[k]['ref'] = \
        np.zeros((n, 64)).astype(np.uint16)


  def remove_database(self, index_key):
    self.index_key.remove(index_key)
    np.delete(self.database[index_key])


  def hashing(self, feature):
    #binary_feature = np.uint8(feature > 0)
    bins = np.array([0],dtype=np.uint8)
    binary_feature = np.digitize(feature,bins,right=True)
    return binary_feature

  
  def pack_bit_16(self, binary_feature):
    binary_feature = (np.packbits(binary_feature, axis=1)).astype(np.uint16)
    shifted_binary = binary_feature << 8
    packed_feature = shifted_binary[:,0::2] + binary_feature[:,1::2]
    return packed_feature


  def pack_bit_64(self, binary_feature):
    """ 
    binary_feature = (np.packbits(binary_feature, axis=1)).astype(np.uint64)
    shifted_binary = binary_feature << 8
    packed_feature = shifted_binary[:,0::2] + binary_feature[:,1::2]
    binary_feature = packed_feature
    shifted_binary = binary_feature << 16
    packed_feature = shifted_binary[:,0::2] + binary_feature[:,1::2]
    binary_feature = packed_feature
    shifted_binary = binary_feature << 32
    packed_feature = shifted_binary[:,0::2] + binary_feature[:,1::2]
    """
    packed_feature = np.uint64(np.packbits(np.uint8(binary_feature),axis=1))
    for i in range (1,5):
      feature_shift = packed_feature << 8*i
      packed_feature = feature_shift[:,0::2] + packed_feature[:,1::2]
    return packed_feature


  def load_category(self, database_filename):
    assert(len(self.index_key) > 0)
    for category_id in self.index_key: 
      self.load(category_id, database_filename % category_id)
      logging.info('Loading indexer for {}'.format(category_id))


  def load(self, index_key, file_name):
    try:
      with open(file_name, 'rb') as fp:
        self.database[index_key] = pickle.load(fp) 
    except Exception as err:
      print 'ERROR in indexer.load ', err
  

  def dump(self, index_key, file_name):
    try:
      with open(file_name, 'wb') as fp:
        pickle.dump(self.database[index_key], fp)
    except Exception as err:
      print 'ERROR in indexer.dump ', err


  def insert(self, idx, feature, index_key, meta):
    try:
      self.database[index_key]['meta'][idx] = meta
      self.database[index_key]['ref'][idx,:] = feature
    except Exception as err:
      print 'ERROR in indexer.insert ', err


  """
  def get_total_samples(self, index_key):
    assert(self.database[index_key]['ref'].shape[0] == \
           len(self.database[index_key]['meta']))
    return len(self.database[index_key]['ref'])
  """


  def get_nearest_neighbor(self, 
    query_feature, index_key, num_neighbors=10):
    diff = np.bitwise_xor(self.database[index_key]['ref'], query_feature)
    diff = self.lookup[diff]
    dist = np.sum(diff, axis=1)
    neighbor_list = np.argsort(dist)
    result_neighbor_meta = []
    result_neighbor_distance = []
    for neighbor_id in neighbor_list[0:num_neighbors]:
      result_neighbor_meta.append(self.database[index_key]['meta'][neighbor_id]) 
      result_neighbor_distance.append(dist[neighbor_id])

    return result_neighbor_meta, result_neighbor_distance
    
