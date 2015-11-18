
//#include <string>
//#include <vector>
#include "DeepFeatureExtractor.hpp"
#include "Utils.hpp"

int main(int argc, char** argv) 
{
  ::google::InitGoogleLogging(argv[0]);

  const std::string model_file = 
    "/storage/models/inception5/inception5.prototxt";
  const std::string trained_file = 
    "/storage/models/inception5/inception5.caffemodel";
  const std::string label_file = 
    "data/synset_words.txt";
  const int use_gpu = 1;
  const int gpu_id = 1;
  //const std::string img_file = "data/cat.jpg";
  //cv::Mat img = cv::imread(img_file, -1);
  //CHECK(!img.empty()) << "Unable to decode image " << img_file;
  DeepFeatureExtractor agent(
    model_file, trained_file, 
    cv::Scalar(104.0, 116.0, 122.0), 
    use_gpu, gpu_id);

  agent.SetLabel(label_file);

  const std::string val_file = "/storage/ImageNet/ILSVRC2012/val_synset.txt";
  const std::string pathPrefix = "/storage/ImageNet/ILSVRC2012/val/"; 
  std::vector<std::string> filepath;
  std::vector<int> lab;
  Utils::loadGT(val_file, pathPrefix, filepath, lab); 

  int top1_count = 0;
  int top5_count = 0;
  for(unsigned int n=0; n<lab.size(); n++) {
    std::vector<int> top_N(5, 0);
    cv::Mat img = cv::imread(filepath[n], -1);
    cv::Point2i origin;
    cv::Point2i sz;
    origin.x = 0;
    origin.y = 0;
    sz.x = img.cols;
    sz.y = img.rows;
    cv::Rect roi = cv::Rect(origin, sz);
    unsigned long tic = Utils::getTickCount();

    agent.SetImage(img, roi, 224, 224);
    std::vector<Prediction> predictions = agent.Classify(5, top_N, false);

    unsigned long toc = Utils::getTickCount();
    int hit_in_5 = 0;
    for (size_t i = 0; i < predictions.size(); ++i) {
      if (top_N[i] == lab[n]) hit_in_5 = 1;
      //Prediction p = predictions[i];
      //std::cout << std::fixed << std::setprecision(4) << 
      //p.second << " - \"" << p.first << "\"" << " " << 
      //top_N[i] << std::endl;
    }
    if (lab[n] == top_N[0]) top1_count++;
    if (hit_in_5 == 1) top5_count++;

    std::cout<< n << " " << 
      "top1: " << top1_count / (n+1.) * 100. << " " << 
      "top5: " << top5_count / (n+1.) * 100. << " " <<
      "elap: " << toc - tic <<  " ms" << std::endl;
  }
  return 0;
}

