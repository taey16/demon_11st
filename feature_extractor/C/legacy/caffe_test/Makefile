CAFFE_ROOT ?= /home/taey16/caffe

LDFLAGS +=  -L$(CAFFE_ROOT)/build/lib \
  -L/usr/local/lib \
  $(CAFFE_ROOT)/build/lib/libcaffe.so

INCLUDES := -I$(CAFFE_ROOT)/include \
  -I$(CAFFE_ROOT)/distribute/include \
  -I/usr/local/src/opencv-2.4.9/include

LIBRARIES := -lcaffe \
  -lprotobuf \
  -lopencv_imgproc \
  -lopencv_core \
  -lopencv_highgui \
  -lopencv_features2d \
  -lglog

all:
	#g++ -DCPU_ONLY=0 $(INCLUDES) -Ofast -g3 -Wall -fPIC -c -fmessage-length=0 -MMD -MP -MF"TestCaffe.d" -MT"TestCaffe.d" -o "TestCaffe.o" "./src/TestCaffe.cpp"
	g++ -DCPU_ONLY=0 $(INCLUDES) -g -Wall -fPIC -c -fmessage-length=0 -MMD -MP -MF"TestCaffe.d" -MT"TestCaffe.d" -o "TestCaffe.o" "./src/TestCaffe.cpp"
	#g++ $(INCLUDES) -g3 -Wall -fPIC -c -fmessage-length=0 -MMD -MP -MF"TestCaffe.d" -MT"TestCaffe.d" -o "TestCaffe.o" "./src/TestCaffe.cpp"
	g++ -o "TestCaffe" TestCaffe.o $(LDFLAGS) $(LIBRARIES)

clean:
	rm TestCaffe*
