all:build

#build:prepare
#	make -C src build

#prepare:
#	mkdir -p release/lib
#	mkdir -p release/include

build:
	make -C src build

rebuild:
	make -C src clean
	make -C src build
	make -C src install

install:
	make -C src install

clean:
	make -C src clean
