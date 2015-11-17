#include <string>
#include <vector>
#include "HammingDistanceCalc.hpp"
#include "Hamming.h"


HammingDistanceCalc:HammingDistanceCalc(
  const unsigned int feature_size) {
  m_feature_size = feature_size;
  m_binary_feature_size = m_feature_size / 64;
}

int HammingDistanceCalc::hashing(
  const std::vector<float>& input,
  std::vector<uint8_t>& output)
{
  for(unsigned int d=0; d<m_feature_size; d++) {
    if (input[d] > 0) {
      output[d] = 1;
    }
  }
  return 0;
}


int HammingDistanceCalc::Packbit64(
  const std::vector<uint8_t>& input,
  std::vector<uint64_t>& output)
{
  output.resize(m_binary_feature_size);
  unsigned int multiply = 0;
  unsigned int residual = 0;
  for(unsigned int d=0; d<m_feature_size; d++) {
    if (input[d]) {
      multiply = d >> 6;
      residual = d % 64; 
      output[multiply] += (uint64_t)1 << (63 - residual);
    }
  }
  return 0;
}


int HammingDistanceCalc::HashingAndPackbit64(
  const std::vector<float>& feature, 
  std::vector<uint64_t>& signature)
{
  std::vector<uint8_t> binary_feature(m_feature_size, 0);
  this->hashing(feature, binary_feature);
  this->Packbit64(binary_feature, signature);
  return 0;
}


unsigned int HammingDistanceCalc::HammingDistance(
  std::vector<uint64_t>& query,
  std::vector<uint64_t>& reference)
{
  unsigned int distance = 0;
  const unsigned int dimension= query.size();
  for(unsigned int d=0; d<dimension; d++) {
    distance += 
      (unsigned int)Hamming::distance(query[d], reference[d]);
  }
  return distance;
}


int HammingDistanceCalc::HammingDistance(
  std::vector<uint64_t>& query,
  std::vector<std::vector<uint64_t> >& reference, 
  std::vector<unsigned int>& distance)
{
  const unsigned int num_ref = reference.size();
  distance = std::vector<unsigned int>(num_ref, 0);
  for(unsigned int n=0; n<num_ref; n++) {
    distance[n] += this->HammingDistance(query, reference[n]);
  }
  return 0;
}

