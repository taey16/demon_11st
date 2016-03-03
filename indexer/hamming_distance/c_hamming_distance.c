
#include <stdint.h>

uint32_t _popcnt(uint64_t x)
{
  __asm__ ("popcnt %1, %0" : "=r" (x) : "0" (x)); 
  return x;
}

uint32_t _distance(uint64_t query, uint64_t ref)
{
  uint32_t xored = query^ref;
  return _popcnt(xored);
}

uint32_t c_hamming_distance(
  uint64_t* query,
  uint64_t* ref,
  uint32_t dimension)
{
  uint32_t dist = 0;
  uint32_t d = 0;
  for(d = 0; d < dimension; d++) {
    dist += _distance(query[d], ref[d]);
  }
  return dist;
}

void c_hamming_distance_ref(
  uint64_t* query,
  uint64_t* ref,
  uint32_t* dist,
  uint32_t dimension,
  uint32_t num_ref)
{
  //uint32_t* dist = (uint32_t*)calloc(dimension, sizeof(uint32_t));
  uint32_t d = 0;
  uint32_t n = 0;
  for(n = 0; n < num_ref; n++) {
    for(d = 0; d < dimension; d++) {
      dist[n] += _distance(query[d], ref[n*dimension+d]);
    }
  }
  //return dist;
  return;
}

void c_hamming_distance_full(
  uint64_t* query,
  uint64_t* ref,
  uint64_t* dist,
  uint32_t dimension,
  uint32_t num_query,
  uint32_t num_ref)
{
  uint32_t d = 0;
  uint32_t n_ref = 0;
  uint32_t n_query = 0;
  for(n_query = 0; n_query < num_query; n_query++) {
    for(n_ref = 0; n_ref < num_ref; n_ref++) {
      for(d = 0; d < dimension; d++) {
        dist[n_query*num_ref+n_ref] += 
          _distance(query[n_query*dimension+d], ref[n_ref*dimension+d]);
      }
    }
  }
  return;
}
