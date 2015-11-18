#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <string>
#include <vector>
#include <caffe/caffe.hpp>
#include "DeepFeatureExtractor.hpp"

using namespace caffe;


DeepFeatureExtractor::DeepFeatureExtractor(
    const std::string& model_file,
    const std::string& trained_file,
    const cv::Scalar& channel_mean,
    const int use_gpu,
    const int gpu_id)
{
  if (use_gpu == 1) {
    Caffe::SetDevice(gpu_id);
    Caffe::set_mode(Caffe::GPU);
    LOG(INFO) << "set_mode(Caffe::GPU), GPU_ID: " << gpu_id << std::endl;
  } else { 
    Caffe::set_mode(Caffe::CPU);
    LOG(INFO) << "set_mode(Caffe::CPU)" << std::endl;
  }

  // Load the network.
  m_net.reset(new Net<float>(model_file, TEST));
  m_net->CopyTrainedLayersFrom(trained_file);

  CHECK_EQ(m_net->num_inputs(), 1) << "Network should have exactly one input.";
  CHECK_EQ(m_net->num_outputs(),1) << "Network should have exactly one output.";

  Blob<float>* input_layer = m_net->input_blobs()[0];
  m_num_channels = input_layer->channels();
  CHECK(m_num_channels == 3 || m_num_channels == 1)
    << "Input layer should have 1 or 3 channels.";
  m_input_geometry = cv::Size(input_layer->width(), input_layer->height());

  // Load the binaryproto mean file.
  //SetMean(m_meanfile);
  // Load the mean value
  SetMean(channel_mean);

  Blob<float>* output_layer = m_net->output_blobs()[0];
  m_feature_size = 1;
  for (unsigned int i=0; i<output_layer->shape().size(); i++) {
    m_feature_size *= (unsigned int)output_layer->shape(i);
  }
  //CHECK_EQ(m_feature_size, 10240)
  CHECK(m_feature_size == 10240 || m_feature_size == 10000)
    << "Number of labels is different from the output layer dimension.";
}


std::vector<float> DeepFeatureExtractor::Process(bool oversample)
{
  CHECK_EQ(m_NormalImageROIMask.empty(), false);
  if (oversample) {
    Oversample(); 
    std::vector<std::vector<float> > feature = 
      this->Predict(m_NormalImageROIMaskOversample);
    std::vector<float> flatten_feature;
    flatten_feature.reserve(GetFeatureSize());
    for(unsigned int i=0; i<10; i++) {
      flatten_feature.insert(flatten_feature.end(), 
        feature[i].begin(), feature[i].end());
    }
    return flatten_feature;
  } else {
    return this->Predict(m_NormalImageROIMask);
  }
}


// set mean value in cvScalar format
int DeepFeatureExtractor::SetMean(
  const cv::Scalar& channel_mean)
{
  m_mean = cv::Mat(m_input_geometry, CV_32FC3, channel_mean);
  return 0;
}


// Load the mean file in binaryproto format.
int DeepFeatureExtractor::SetMean(
  const std::string& meanfile) 
{
  BlobProto blob_proto;
  ReadProtoFromBinaryFileOrDie(meanfile.c_str(), &blob_proto);
  // Convert from BlobProto to Blob<float> 
  Blob<float> meanblob;
  meanblob.FromProto(blob_proto);
  CHECK_EQ(meanblob.channels(), m_num_channels)
    << "Number of channels of mean file doesn't match input layer.";
  // The format of the mean file is planar 32-bit float BGR or grayscale.
  std::vector<cv::Mat> channels;
  float* data = meanblob.mutable_cpu_data();
  for (unsigned int i = 0; i < m_num_channels; ++i) {
    // Extract an individual channel.
    cv::Mat channel(meanblob.height(), meanblob.width(), CV_32FC1, data);
    channels.push_back(channel);
    data += meanblob.height() * meanblob.width();
  }
  // Merge the separate channels into a single image.
  cv::Mat mean;
  cv::merge(channels, mean);
  // Compute the global mean pixel value and create a mean image
  // filled with this value. 
  cv::Scalar channel_mean = cv::mean(mean);
  m_mean = cv::Mat(m_input_geometry, mean.type(), channel_mean);
  return 0;
}


int DeepFeatureExtractor::SetLabel(
  const std::string& label_file)
{
  std::ifstream labels(label_file.c_str());
  CHECK(labels) << "Unable to open labels file " << label_file;
  string line;
  while (std::getline(labels, line))
    m_labels.push_back(string(line));
  return 0;
}


int DeepFeatureExtractor::SetImage(
  const cv::Mat& image,
  const cv::Rect& roi,
  const unsigned int width,
  const unsigned int height )
{
  this->ROI(image, roi);
  cv::resize(this->m_NormalImageROIMask,
             this->m_NormalImageROIMask, 
             cv::Size(width, height));
  return 0;
}


int DeepFeatureExtractor::Oversample()
{
  CHECK_EQ(this->m_NormalImageROIMask.empty(), false);
  std::vector<cv::Rect> samplePoint(10);
  unsigned int iW = this->m_NormalImageROIMask.cols;
  unsigned int iH = this->m_NormalImageROIMask.rows;
  unsigned int oW = m_input_geometry.width;
  unsigned int oH = m_input_geometry.height;
  unsigned int w1 = (iW - oW) / 2;
  unsigned int h1 = (iH - oH) / 2;
  samplePoint[0] = cv::Rect(cv::Point2i(0, 0), cv::Point2i(oW, oH));
  samplePoint[1] = cv::Rect(cv::Point2i(iW-oW, 0),cv::Point2i(iW, oH));
  samplePoint[2] = cv::Rect(cv::Point2i(0, iH-oH),cv::Point2i(oW, iH));
  samplePoint[3] = cv::Rect(cv::Point2i(iW-oW, iH-oH), cv::Point2i(iW, iH));
  samplePoint[4] = cv::Rect(cv::Point2i(w1, h1), cv::Point2i(w1+oW, h1+oH));
  this->m_NormalImageROIMaskOversample = std::vector<cv::Mat>(10);
  for(unsigned int i=0; i<5; i++) {
    this->m_NormalImageROIMaskOversample[i] = 
    this->m_NormalImageROIMask(samplePoint[i]).clone();
    cv::flip(this->m_NormalImageROIMaskOversample[i], 
             this->m_NormalImageROIMaskOversample[i+5], 1);
  }
  return 0;
}


int DeepFeatureExtractor::ROI(const cv::Mat& image, const cv::Rect& roi)
{
  this->m_NormalImage = image.clone();
  this->m_NormalImageROIMask = image(roi).clone();
  return 0;
}


// Return the top N predictions.
std::vector<Prediction> DeepFeatureExtractor::Classify(
  int N, std::vector<int>& top_N, bool oversample)
{
  std::vector<float> output;
  if(oversample) {
    Oversample();
    CHECK_EQ(m_NormalImageROIMaskOversample[9].empty(), false);
    std::vector<std::vector<float> > augmented_output = 
      Predict(this->m_NormalImageROIMaskOversample);
    output = std::vector<float>(augmented_output[0].size(), 0.0);
    for(unsigned int c=0; c<augmented_output[0].size(); c++) {
      for(unsigned int i=0; i<augmented_output.size(); i++) {
        output[c] += augmented_output[i][c];
      }
      output[c] /= augmented_output.size();
    }
  } else {
    CHECK_EQ(m_NormalImageROIMask.empty(), false);
    output = Predict(this->m_NormalImageROIMask);
  }
  N = std::min<int>(m_labels.size(), N);
  std::vector<int> maxN = Argmax(output, N);
  std::copy(maxN.begin(), maxN.end(), top_N.begin());
  std::vector<Prediction> predictions;
  for (int i = 0; i < N; ++i) {
    int idx = maxN[i];
    predictions.push_back(std::make_pair(m_labels[idx], output[idx]));
  }
  return predictions;
}


std::vector<std::vector<float> > DeepFeatureExtractor::Predict(
  const std::vector<cv::Mat>& img) 
{
  Blob<float>* input_layer = m_net->input_blobs()[0];
  input_layer->Reshape(img.size(), m_num_channels,
                       m_input_geometry.height, m_input_geometry.width);
  m_net->Reshape();
  std::vector<cv::Mat> input_channels;
  WrapInputLayer(&input_channels, img.size());
  Preprocess(img, &input_channels);
  m_net->ForwardPrefilled();
  Blob<float>* output_layer = m_net->output_blobs()[0];

  std::vector<std::vector<float> > output;
  for(unsigned int i=0; i<img.size(); i++) {
    const float* begin = output_layer->cpu_data() + i*output_layer->channels();
    const float* end = begin + output_layer->channels();
    output.push_back(std::vector<float>(begin, end));
  }
  return output;
}


std::vector<float> DeepFeatureExtractor::Predict(
  const cv::Mat& img) 
{
  Blob<float>* input_layer = m_net->input_blobs()[0];
  input_layer->Reshape(1, m_num_channels,
                       m_input_geometry.height, m_input_geometry.width);
  // Forward dimension change to all layers. 
  m_net->Reshape();
  std::vector<cv::Mat> input_channels;
  WrapInputLayer(&input_channels);
  Preprocess(img, &input_channels);
  m_net->ForwardPrefilled();
  // Copy the output layer to a std::vector 
  Blob<float>* output_layer = m_net->output_blobs()[0];
  const float* begin = output_layer->cpu_data();
  const float* end = begin + output_layer->channels();
  return std::vector<float>(begin, end);
}


/* Wrap the input layer of the network in separate cv::Mat objects
 * (one per channel). This way we save one memcpy operation and we
 * don't need to rely on cudaMemcpy2D. The last preprocessing
 * operation will write the separate channels directly to the input
 * layer. */
int DeepFeatureExtractor::WrapInputLayer(
  std::vector<cv::Mat>* input_channels, 
  const unsigned int num_inputs) 
{
  Blob<float>* input_layer = m_net->input_blobs()[0];

  int width = input_layer->width();
  int height = input_layer->height();
  float* input_data = input_layer->mutable_cpu_data();
  for (unsigned int i = 0; i < input_layer->channels()*num_inputs; ++i) {
    cv::Mat channel(height, width, CV_32FC1, input_data);
    input_channels->push_back(channel);
    input_data += width * height;
  }
  return 0;
}


int DeepFeatureExtractor::Transform(
  const cv::Mat& img,
  cv::Mat& sample_normalized)
{
  cv::Mat sample;
  if (img.channels() == 3 && m_num_channels == 1)
    cv::cvtColor(img, sample, CV_BGR2GRAY);
  else if (img.channels() == 4 && m_num_channels == 1)
    cv::cvtColor(img, sample, CV_BGRA2GRAY);
  else if (img.channels() == 4 && m_num_channels == 3)
    cv::cvtColor(img, sample, CV_BGRA2BGR);
  else if (img.channels() == 1 && m_num_channels == 3)
    cv::cvtColor(img, sample, CV_GRAY2BGR);
  else
    sample = img;

  cv::Mat sample_resized;
  if (sample.size() != m_input_geometry)
    cv::resize(sample, sample_resized, m_input_geometry);
  else
    sample_resized = sample;

  cv::Mat sample_float;
  if (m_num_channels == 3)
    sample_resized.convertTo(sample_float, CV_32FC3);
  else
    sample_resized.convertTo(sample_float, CV_32FC1);

  //cv::Mat sample_normalized;
  cv::subtract(sample_float, m_mean, sample_normalized);
  return 0;
}


int DeepFeatureExtractor::Preprocess(
  const std::vector<cv::Mat>& img,
  std::vector<cv::Mat>* input_channels)
{
  for(unsigned int i=0; i<img.size(); i++) {
    cv::Mat sample_normalized;
    Transform(img[i], sample_normalized);

    vector<cv::Mat> channels;
    cv::split(sample_normalized, channels);
    for(unsigned int c=0; c<channels.size(); c++) {
      channels[c].copyTo((*input_channels)[i*m_num_channels+c]);  
    }
  }
  return 0;
}


int DeepFeatureExtractor::Preprocess(
  const cv::Mat& img,
  std::vector<cv::Mat>* input_channels) 
{
  cv::Mat sample_normalized;
  Transform(img, sample_normalized);
  // This operation will write the separate BGR planes directly to the
  // input layer of the network because it is wrapped by the cv::Mat
  // objects in input_channels.
  cv::split(sample_normalized, *input_channels);

  CHECK(reinterpret_cast<float*>(input_channels->at(0).data)
        == m_net->input_blobs()[0]->cpu_data())
    << "Input channels are not wrapping the input layer of the network.";

  return 0;
}

