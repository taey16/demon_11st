# Python wrapper for Fast Hamming distance computation with Cython
1. Prerequisits
- Cython, numpy
2. Compile
```
hamming_distance$ ls
c_hamming_distance.c  hamming_distance.pyx  Makefile  popcnt_exam.py  README.md  setup.py
hamming_distance$ make
python setup.py build_ext --inplace
running build_ext
cythoning hamming_distance.pyx to hamming_distance.c
building 'hamming_distance' extension
creating build
creating build/temp.linux-x86_64-2.7
x86_64-linux-gnu-gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -I/usr/local/lib/python2.7/dist-packages/numpy/core/include -I/usr/include/python2.7 -c hamming_distance.c -o build/temp.linux-x86_64-2.7/hamming_distance.o

numpy warning ~bla~bla

x86_64-linux-gnu-gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -I/usr/local/lib/python2.7/dist-packages/numpy/core/include -I/usr/include/python2.7 -c c_hamming_distance.c -o build/temp.linux-x86_64-2.7/c_hamming_distance.o
x86_64-linux-gnu-gcc -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -D_FORTIFY_SOURCE=2 -g -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security build/temp.linux-x86_64-2.7/hamming_distance.o build/temp.linux-x86_64-2.7/c_hamming_distance.o -o /home/taey16/Documents/demon_11st/indexer/hamming_distance/hamming_distance.so
hamming_distance$ ls
build  c_hamming_distance.c  hamming_distance.c  hamming_distance.pyx  hamming_distance.so  Makefile  popcnt_exam.py  README.md  setup.py
```
3. Example
```
hamming_distance$ python popcnt_exam.py
Test for hamming_distance.popcnt
3 in 0.000014
Test for hamming_distance.hamming_distance for 320 dim.
320 in 0.000010
Test for hamming_distance.hamming_distance_ref for 1000000 samples
Memory alloc. for 1000000 samples in 24.103649
distance of last two element: 317, 319 in elapsed: 0.602975
```

