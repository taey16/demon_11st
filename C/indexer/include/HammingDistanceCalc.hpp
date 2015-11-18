#include <vector>
#include <stdint.h>
#include <algorithm>

#ifndef SRC_LIBSKP_HAMMING_DISTANCE_CALC_HPP_
#define SRC_LIBSKP_HAMMING_DISTANCE_CALC_HPP_

class HammingDistanceCalc {

public:
  HammingDistanceCalc(
    const unsigned int feature_size);

  int HashingAndPackbit64(
    const std::vector<float>& feature,
    std::vector<uint64_t>& binary_feature); 
  unsigned int HammingDistance(
    std::vector<uint64_t>& query,
    std::vector<uint64_t>& reference);
  int HammingDistance(
    std::vector<uint64_t>& query,
    std::vector<std::vector<uint64_t> >& reference,
    std::vector<unsigned int>& distance);

  unsigned int GetSignatureSize() const { return m_binary_feature_size; }
  unsigned int GetFeatureSize() const { return m_feature_size; }

private:
  int hashing(
    const std::vector<float>& input,
    std::vector<uint8_t>& output);
  int Packbit64(
    const std::vector<uint8_t>& input,
    std::vector<uint64_t>& output);

  unsigned int m_binary_feature_size;
  unsigned int m_feature_size;
};


#endif

