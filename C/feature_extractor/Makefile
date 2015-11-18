CXX=	g++

DEBUG= -g 

# dynamic link for cuda
CUDA_ROOT= /usr/local/cuda
INCS_CUDA= /$(CUDA_ROOT)/include
LIBS_CUDA= /$(CUDA_ROOT)/lib64

# for including various lib. due to caffe
INCS_SYS = /usr/include
LIBS_SYS = /usr/local/lib

THIRD_PART_LIB=../3rd_party
# dynamic link for caffe
CAFFE_ROOT= $(THIRD_PART_LIB)/caffe
INCS_CAFFE= $(CAFFE_ROOT)/include
LIBS_CAFFE= $(CAFFE_ROOT)/lib

# static link for deep feature extractor
# self-contained hamming distance lib.
FE_ROOT= ../agent
INCS_FE= $(FE_ROOT)/include
LIBS_FE= $(FE_ROOT)/lib

INDEXER_ROOT=../indexer
INCS_INDEXER=$(INDEXER_ROOT)/include
LIBS_INDEXER=$(INDEXER_ROOT)/lib

SRCS_DIR=	.

LIBS=	-lm -ldeepfeatureextractor64 -lhammingdistancecalc64 \
      -lcaffe -lprotobuf -lglog -lboost_system \
      -lopencv_imgproc -lopencv_core -lopencv_highgui -lopencv_features2d

INCLUDES_ALL=	-I$(INCS_FE) \
              -I$(INCS_INDEXER) \
              -I$(INCS_CUDA) \
              -I$(INCS_CAFFE) \
              -I$(INCS_SYS)

LIBS_ALL=	-L$(LIBS_FE) \
          -L$(LIBS_INDEXER) \
          -L$(LIBS_CAFFE) \
          -L$(LIBS_CUDA) \
          -L$(INCS_SYS)

CXXFLAGS=	$(DEBUG) $(INCLUDES_ALL)
LINKFLAGS=$(DEBUG) $(LIBS_ALL)

SRCS_FE= $(SRCS_DIR)/feature_extractor.cpp
OBJS_FE= $(SRCS_FE:.cpp=.o)
SRCS_CLA= $(SRCS_DIR)/classifier.cpp
OBJS_CLA= $(SRCS_CLA:.cpp=.o)

OBJS= $(OBJS_CLA) $(OBJS_FE)

TARGET_FE= feature_extractor
TARGET_CLA= classifier

all : $(TARGET_FE) $(TARGET_CLA)
#all : $(TARGET_FE)
#all : $(TARGET_CLA)

$(TARGET_FE) : $(OBJS_FE)
	$(CXX) $(LINKFLAGS) -o $@ $< $(LIBS)

$(TARGET_CLA) : $(OBJS_CLA)
	$(CXX) $(LINKFLAGS) -o $@ $< $(LIBS)

.cpp .o: $(OBJS)
	$(CXX) $(CXXFLAGS) -c $<

clean:
	rm -f $(OBJS) $(TARGET_FE) $(TARGET_CLA)
