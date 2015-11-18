# Hamming Distance Library Sample application.
OSTYPE = $(shell uname)
CC=g++

HAMMING_METHOD=-D__SSE4_INTRINSIC__
#HAMMING_METHOD=-D__LOOKUP_TABLE_8_POPCNT__
#HAMMING_METHOD=-D__LOOKUP_TABLE_16_POPCNT__

INC_DIR=../include
SRC_DIR=../src
OUTPUT_DIR=.

TARGETS=hammingDistance

CFlags=-O2
INC_OPTION=-I$(SRC_DIR) \
		-I$(INC_DIR)

LINUX_OPTION=-lrt

ifeq ($(OSTYPE),Linux)
	OS_OPTION=-lrt
endif

OBJS=main.o testHamming.o Hamming.o TimeStamp.o log.o

$(TARGETS): $(OBJS) 
	$(CC) -o $(OUTPUT_DIR)/$(TARGETS) \
		$(OUTPUT_DIR)/main.o \
		$(OUTPUT_DIR)/testHamming.o \
		$(OUTPUT_DIR)/TimeStamp.o \
		$(OUTPUT_DIR)/log.o \
		$(OUTPUT_DIR)/Hamming.o \
		$(CFlags) $(OS_OPTION) $(HAMMING_METHOD)

main.o:
	$(CC) -c main.cpp -o $(OUTPUT_DIR)/main.o $(INC_OPTION) $(CFlags)

testHamming.o:
	g++ -c $(SRC_DIR)/testHamming.cpp -o $(OUTPUT_DIR)/testHamming.o $(INC_OPTION) $(CFlags) $(HAMMING_METHOD)

Hamming.o:
	g++ -c $(SRC_DIR)/Hamming.cpp -o $(OUTPUT_DIR)/Hamming.o $(INC_OPTION) $(CFlags) $(HAMMING_METHOD)
	
log.o:
	g++ -c $(SRC_DIR)/log.cpp -o $(OUTPUT_DIR)/log.o $(INC_OPTION) $(CFlags)

TimeStamp.o:
	g++ -c $(SRC_DIR)/TimeStamp.cpp -o $(OUTPUT_DIR)/TimeStamp.o $(INC_OPTION) $(CFlags)

clean:
	rm -f $(OUTPUT_DIR)/$(TARGETS)
	rm -f $(OUTPUT_DIR)/main.o	
	rm -f $(OUTPUT_DIR)/testHamming.o	
	rm -f $(OUTPUT_DIR)/Hamming.o
	rm -f $(OUTPUT_DIR)/TimeStamp.o
