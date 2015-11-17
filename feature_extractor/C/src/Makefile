.SUFFIXES: .o .c .cpp .a .so

CXX = g++
CC = gcc
AR = ar
CP = cp
RM = rm -f
DEBUG = -g -O2

# for including cuda
CUDA_ROOT = /usr/local/cuda
INCS_CUDA = $(CUDA_ROOT)/include

# set release dir
RELEASE_DIR	= ../release

# for including caffe
CAFFE_ROOT = $(RELEASE_DIR)/lib/caffe
INCS_CAFFE = $(CAFFE_ROOT)/include
# for including hamming dist. lib. with SSE4
HAMMING_ROOT = $(RELEASE_DIR)/lib/HammingDistanceLibrary-1.0
INCS_HAMMING = $(HAMMING_ROOT)/include

# for including various lib. due to caffe
INCS_SYS = /usr/include

SRCS_DIR = .
INCS_DIR = ../include
TARGET_DIR = ../lib/

CXX_SRCS=$(foreach dir, $(SRCS_DIR), $(wildcard $(dir)/*.cpp) )
CXX_OBJS=$(CXX_SRCS:.cpp=.o)

INCS=	-I$(INCS_DIR) \
      -I$(INCS_CUDA) \
      -I$(INCS_CAFFE) \
      -I$(INCS_SYS) \
      -I$(INCS_HAMMING)

OBJS 	= $(CXX_OBJS)

CXXFLAGS=$(DEBUG) -Wall $(INCS)
ARFLAGS = rcusv

OS_ARCH = $(shell getconf LONG_BIT)
ifeq ($(OS_ARCH),64)
COMPILE_ARCH = -m64
TARGET 	= $(TARGET_DIR)/libdeepfeatureextractor64.a
else
COMPILE_ARCH = -m32
TARGET 	= $(TARGET_DIR)/libdeepfeatureextractor32.a
endif

build : $(TARGET)

$(TARGET) : $(OBJS)
	$(AR) $(ARFLAGS) $@ $^

.cpp .o: $(OBJS)
	$(CXX) $(CXXFLAGS) -c $<

clean:
	$(RM) $(OBJS) $(TARGET)

install: build 
	mkdir -p $(RELEASE_DIR)/lib/extractor/include
	mkdir -p $(RELEASE_DIR)/lib/extractor/lib
	$(CP) $(INCS_DIR)/* $(RELEASE_DIR)/lib/extractor/include
	$(CP) $(TARGET_DIR)/* $(RELEASE_DIR)/lib/extractor/lib
