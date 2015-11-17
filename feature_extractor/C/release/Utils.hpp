
#ifndef __UTILS_HPP__
#define __UTILS_HPP__

#include <sys/time.h>
#include <string>
#include <cstdlib> // atoi
#include <vector>
#include <iostream>
#include <fstream>

class Utils {

public:
  Utils() { }
  ~Utils() { }


  template<class T>
  struct index_cmp {
    index_cmp(const T arr) : arr(arr) {}
    bool operator()(const size_t a, const size_t b) const { 
      return arr[a] < arr[b]; 
    }
    const T arr;
  };


  static int Argsort(
    std::vector<unsigned int>& distance,
    std::vector<unsigned int>& index)
  {
    unsigned int num_sample = distance.size();
    index = std::vector<unsigned int>(num_sample);
    std::sort(index.begin(), 
              index.end(), 
              index_cmp<std::vector<unsigned int>& >(distance));
    std::sort(distance.begin(), distance.end());
    return 0;
  }
    

  static int SplitString (
    const std::string& original, 
    const std::string& token, 
    std::vector<std::string>* results)
  {
    int cutAt;
    std::string localOriginal = original;
    // loop for finding a token
    while((cutAt = (int)localOriginal.find_first_of(token)) != 
          (int)localOriginal.npos) {
      if( cutAt > 0 ) {
        results->push_back(localOriginal.substr(0, cutAt));
      }
      localOriginal = localOriginal.substr(cutAt+1);
    }
    if(localOriginal.length() > 0) {
      results->push_back(localOriginal.substr(0, cutAt));
    }
    return results->size();
  }


  static int loadString(
    const std::string& filename, 
    std::vector<std::string>& results)
  {
    std::ifstream infile(filename.c_str(), std::ios::in);
    if (infile.is_open()) {
      while(infile.good()) {
        std::string line;
        std::getline(infile, line);
        //if(line.size() > 1)
        if(line.size() > 0) {
          results.push_back(line);
        }
      }
    } else {
      std::cerr<<
        "ERROR Daum::Utils::loadString (check filename)"<<std::endl;
      return -1;
    }
    //return (int)results->size();
    return 0;
  }


  static int loadGT(
    const std::string& gtFilename,
    const std::string& pathPrefix,
    std::vector<std::string>& gtFilenameList,
    std::vector<int>& labelList)
  {
    std::ifstream infile(gtFilename.c_str(), std::ios::in);
    while(infile.good()) {
      std::string line;
      std::getline(infile, line);
      if(line.size() > 1) {
        std::vector<std::string>gt;
        std::vector<std::string> item;
        SplitString(line, std::string(" "),&item);
        gtFilenameList.push_back(pathPrefix + item[0]);
        labelList.push_back(atoi(item[1].c_str()));
      }
    }
    return 0;
  }


  static unsigned long getTickCount()
  {
    struct timeval gettick;
    unsigned long tick;
    gettimeofday(&gettick, NULL);
    tick = gettick.tv_sec*1000 + gettick.tv_usec/1000;
    return tick; //return in (millisecond)
  }


};

#endif 

