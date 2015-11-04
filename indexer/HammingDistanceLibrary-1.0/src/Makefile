.SUFFIXES: .o .c .cpp .a .so

OSTYPE = $(shell uname)

CXX = g++
CC = gcc
AR = ar
CP = cp
RM = rm -f
DEBUG = -O2

HAMMING_METHOD=-D__SSE4_INTRINSIC__
#HAMMING_METHOD=-D__LOOKUP_TABLE_8_POPCNT__
#HAMMING_METHOD=-D__LOOKUP_TABLE_16_POPCNT__

#ifeq ($(OSTYPE),Linux)
#	OS_OPTION=-lrt
#endif

RELEASES_DIR=	../releases

SRCS_DIR=	.
LIBS_DIR=	../lib
INCS_DIR=	../include

CXX_SRCS=$(foreach dir, $(SRCS_DIR), $(wildcard $(dir)/*.cpp) )
CXX_OBJS=$(CXX_SRCS:.cpp=.o)

INCS=	-I$(INCS_DIR)
OBJS= 	$(CXX_OBJS)

CXXFLAGS=$(DEBUG) -Wall $(INCS) $(HAMMING_METHOD)
ARFLAGS = rcusv

OS_ARCH = $(shell getconf LONG_BIT)
ifeq ($(OS_ARCH),64)
COMPILE_ARCH = -m64
TARGET = $(LIBS_DIR)/libhammingdistance64.a
else
COMPILE_ARCH = -m32
TARGET = $(LIBS_DIR)/libhammingdistance32.a
endif

build: $(TARGET)

$(TARGET) : $(OBJS)
	$(AR) $(ARFLAGS) $@ $^

.cpp .o: $(OBJS)
	$(CXX) $(CXXFLAGS) -c $<

clean:
	$(RM) $(OBJS) $(TARGET)

install: build
	mkdir -p $(RELEASES_DIR)/include
	mkdir -p $(RELEASES_DIR)/lib
	$(CP) $(INCS_DIR)/* $(RELEASES_DIR)/include
	$(CP) $(LIBS_DIR)/* $(RELEASES_DIR)/lib
