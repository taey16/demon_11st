
#include "DeepFeatureExtractor.hpp"
#include "Utils.hpp"

int main(int argc, char** argv) 
{
  ::google::InitGoogleLogging(argv[0]);

  std::string model_file = 
    "/storage/models/inception5/inception5_pool5_7x7_s1.prototxt";
  std::string trained_file = 
    "/storage/models/inception5/inception5.caffemodel";
  //std::string mean_file = 
  //  "/works/demon_11st/feature_extractor/C/release/lib/caffe/imagenet_mean.binaryproto";
  const int use_gpu = 1;
  const int gpu_id = 0;
  std::string img_file = "data/cat.jpg";
  DeepFeatureExtractor agent(
    model_file, trained_file, 
    cv::Scalar(104.0, 116.0, 122.0), 
    use_gpu, gpu_id);

  cv::Mat img = cv::imread(img_file, -1);
  CHECK(!img.empty()) << "Unable to decode image " << img_file;

  cv::Point2i origin;
  cv::Point2i sz;
  origin.x = 0;
  origin.y = 0;
  sz.x = img.cols;
  sz.y = img.rows;
  cv::Rect roi = cv::Rect(origin, sz);

  agent.SetImage(img, roi, 384, 384);
  unsigned int tic_fe = Utils::getTickCount();
  std::vector<float> feature = agent.Process(true);
  unsigned int toc_fe = Utils::getTickCount();
  std::vector<uint64_t> signature(agent.GetSignatureSize(), 0); 
  agent.HashingAndPackbit64(feature, signature); 
  for (unsigned int i = 0; i < 100; ++i) { 
    std::cout << feature[i] << " "; 
  } 
  std::cout << std::endl; 
  for (unsigned int i = 0; i < 10; ++i) { 
    std::cout << signature[i] << " ";
  }
  std::cout << std::endl;

  std::vector<std::vector<uint64_t> > ref(1000000);
  for(unsigned int n=0; n<1000000; n++) {
    ref[n] = std::vector<uint64_t>(agent.GetSignatureSize(), 0);
  }
  unsigned int distance = agent.HammingDistance(signature, signature);
  std::vector<unsigned int> distance_vector; 
  std::vector<unsigned int> index_vector; 
  unsigned int tic_he = Utils::getTickCount();
  agent.HammingDistance(signature, ref, distance_vector);
  unsigned int toc_he = Utils::getTickCount();
  unsigned int tic_sort = Utils::getTickCount();
  Utils::Argsort(distance_vector, index_vector);
  unsigned int toc_sort = Utils::getTickCount();

  std::cout<< "fe: " << toc_fe - tic_fe << " "
           << "he: " << toc_he - tic_he << " "
           << "sort: " << toc_sort - tic_sort << std::endl;

  return 0;
}

