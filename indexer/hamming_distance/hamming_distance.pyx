
import cython
import numpy as np
cimport numpy as np 
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

# Cython: https://github.com/cython/cython/wiki/tutorials-NumpyPointerToC

cdef extern unsigned int _popcnt(unsigned long long x)

cdef extern unsigned int c_hamming_distance(
  unsigned long long* query,
  unsigned long long* ref,
  unsigned int dimension)

cdef extern unsigned int c_hamming_distance_ref(
  unsigned long long* query,
  unsigned long long* ref,
  unsigned int* distance,
  unsigned int dimension,
  unsigned int num_ref)

cdef extern unsigned int c_hamming_distance_full(
  unsigned long long* query,
  unsigned long long* ref,
  unsigned int* distance,
  unsigned int dimension,
  unsigned int num_query,
  unsigned int num_ref)


@cython.boundscheck(False)
@cython.wraparound(False)
def popcnt(x not None):
  return _popcnt(x);


@cython.boundscheck(False)
@cython.wraparound(False)
def hamming_distance(
  np.ndarray[unsigned long long, ndim=2, mode="c"] query not None,
  np.ndarray[unsigned long long, ndim=2, mode="c"] ref not None):

  cdef dim = query.shape[1]
  distance = c_hamming_distance( &query[0,0], &ref[0,0], dim )

  return distance


@cython.boundscheck(False)
@cython.wraparound(False)
def hamming_distance_ref(
  np.ndarray[unsigned long long, ndim=2, mode="c"] query not None,
  np.ndarray[unsigned long long, ndim=2, mode="c"] ref not None,
  np.ndarray[unsigned int, ndim=1, mode="c"] distance not None):

  cdef dim = query.shape[1]
  assert(dim == ref.shape[1])
  cdef num_ref = ref.shape[0]

  c_hamming_distance_ref(&query[0,0], &ref[0,0], &distance[0], dim, num_ref)

  return


@cython.boundscheck(False)
@cython.wraparound(False)
def hamming_distance_full(
  np.ndarray[unsigned long long, ndim=2, mode="c"] query not None,
  np.ndarray[unsigned long long, ndim=2, mode="c"] ref not None,
  np.ndarray[unsigned int, ndim=2, mode="c"] distance not None):

  cdef num_query = query.shape[0]
  cdef dim = query.shape[1]
  cdef num_ref = ref.shape[0]
  assert(dim == ref.shape[1])
  assert(num_query == distance.shape[0])
  assert(num_ref == distance.shape[1])

  c_hamming_distance_full(
    &query[0,0], &ref[0,0], &distance[0,0], dim, num_query, num_ref)

  return
