.SUFFIXES: .o .c .cpp .a .so

CXX = g++
CC = gcc
AR = ar
CP = cp
RM = rm -f
DEBUG = -g -O2

# set release dir
RELEASE_DIR	= ../

# for including hamming dist. lib. with SSE4
HAMMING_ROOT = ../HammingDistanceLibrary-1.0
INCS_HAMMING = $(HAMMING_ROOT)/include

SRCS_DIR = .
TARGET_DIR = ../lib/

CXX_SRCS=$(foreach dir, $(SRCS_DIR), $(wildcard $(dir)/*.cpp) )
CXX_OBJS=$(CXX_SRCS:.cpp=.o)

INCS=	-I$(SRCS_DIR) \
      -I$(INCS_HAMMING)

OBJS 	= $(CXX_OBJS)

CXXFLAGS=$(DEBUG) -Wall $(INCS)
ARFLAGS = rcusv

OS_ARCH = $(shell getconf LONG_BIT)
ifeq ($(OS_ARCH),64)
COMPILE_ARCH = -m64
TARGET 	= $(TARGET_DIR)/libhammingdistancecalc64.a
else
COMPILE_ARCH = -m32
TARGET 	= $(TARGET_DIR)/libhammingdistancecalc32.a
endif

build : $(TARGET)

$(TARGET) : $(OBJS)
	$(AR) $(ARFLAGS) $@ $^

.cpp .o: $(OBJS)
	$(CXX) $(CXXFLAGS) -c $<

clean:
	$(RM) $(OBJS) $(TARGET)

install: build 
	mkdir -p $(RELEASE_DIR)/include
	mkdir -p $(RELEASE_DIR)/lib
	$(CP) $(SRCS_DIR)/*.hpp $(RELEASE_DIR)/include
