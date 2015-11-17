//#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <string>
#include <vector>
#include <caffe/caffe.hpp>

#ifndef SRC_LIBSKP_DEEPFEATURE_EXTRACTOR_HPP_
#define SRC_LIBSKP_DEEPFEATURE_EXTRACTOR_HPP_

using namespace caffe;

// Pair (label, confidence) representing a prediction.
typedef std::pair<std::string, float> Prediction;

class DeepFeatureExtractor {

public:
  DeepFeatureExtractor(
    const std::string& model_file,
    const std::string& trained_file,
    const cv::Scalar& channel_mean,
    const int use_gpu,
    const int gpu_id);

  int SetImage(const cv::Mat& img, 
               const cv::Rect& roi, 
               const unsigned int width = 224,
               const unsigned int height= 224);
  std::vector<float> Process(const bool oversample=true);
  unsigned int GetFeatureSize() const { return m_feature_size; }


  int SetLabel(const std::string& label_file);
  std::vector<Prediction> Classify(
    int N, 
    std::vector<int>& top_N,
    const bool oversample = true); 

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

  unsigned int GetSignatureSize() const { return binary_feature_size; }

private:
  int ROI(const cv::Mat& image, const cv::Rect& roi);
  int Oversample();
  int SetMean(const cv::Scalar& channel_mean);
  int SetMean(const std::string& meanfile);
  int WrapInputLayer(std::vector<cv::Mat>* input_channels, 
                     const unsigned int num_inputs = 1);
  int Transform(const cv::Mat& img, 
                cv::Mat& sample_normalized);
  int Preprocess(
    const cv::Mat& img,
    std::vector<cv::Mat>* input_channels);
  int Preprocess(
    const std::vector<cv::Mat>& img,
    std::vector<cv::Mat>* input_channels);
  std::vector<float> Predict(const cv::Mat& img);
  std::vector<std::vector<float> > Predict(const std::vector<cv::Mat>& img);

  int hashing(
    const std::vector<float>& input,
    std::vector<uint8_t>& output);
  int Packbit64(
    const std::vector<uint8_t>& input,
    std::vector<uint64_t>& output);

  shared_ptr<Net<float> > m_net;
  cv::Size m_input_geometry;
  unsigned int m_num_channels;
  cv::Mat m_mean;
  std::vector<string> m_labels;
  unsigned int m_feature_size;
  unsigned int binary_feature_size;
  cv::Mat m_NormalImage;
  cv::Mat m_NormalImageROIMask;
  std::vector<cv::Mat> m_NormalImageROIMaskOversample;
};


static uint8_t PairCompare(
  const std::pair<float, int>& lhs,
  const std::pair<float, int>& rhs) 
{ return lhs.first > rhs.first; }


// Return the indices of the top N values of vector v. 
static std::vector<int> Argmax(
  const std::vector<float>& v, int N) 
{
  std::vector<std::pair<float, int> > pairs;
  for (size_t i = 0; i < v.size(); ++i)
    pairs.push_back(std::make_pair(v[i], i));
  std::partial_sort(pairs.begin(), 
                    pairs.begin() + N, 
                    pairs.end(), 
                    PairCompare);

  std::vector<int> result;
  for (int i = 0; i < N; ++i)
    result.push_back(pairs[i].second);

  return result;
}

#endif
