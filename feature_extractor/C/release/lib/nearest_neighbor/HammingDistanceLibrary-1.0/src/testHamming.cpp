#include "testHamming.h"


void testCase1()
{
	uint64_t first64 = 0x0001000200010002LL;
	uint64_t second64 = 0x1000200010002000LL;
	
	uint128_t first128(first64, first64);
	uint128_t second128(second64, second64);

	uint256_t first256(first128, first128);
	uint256_t second256(second128, second128);

	uint512_t first512(first256, first256);
	uint512_t second512(second256, second256);

	Hamming hamming;
	logging::info("  Hamming distance data1: 0x00010002 00010002 00010002 00010002\n");
	logging::info("                   data2: 0x10002000 10002000 10002000 10002000\n");
	logging::info("  - Test 64 SSE4PopCnt() %d\n",hamming.distance(first64, second64) );
	logging::info("  - Test 128 SSE4PopCnt() %d\n",hamming.distance(first128, second128) );	
	logging::info("  - Test 256 SSE4PopCnt() %d\n",hamming.distance(first256, second256) );
	logging::info("  - Test 512 SSE4PopCnt() %d\n",hamming.distance(first512, second512) );

	logging::info("finished..");

}



void testPerformance()
{
	const int loopCount = 1000000000;	// sib uk bun => 10^9
	uint32_t first = 0xF1;
	uint32_t second = 0x02;

	Hamming hamming;
	double elapsedTime;

	logging::info("\n\n\n");
	TimeStamp timeStamp;
	timeStamp.initStamp();
	for(int i=0;i<loopCount;++i) {
		first = (unsigned long)i;
		hamming.distance( first, second );
	}
	elapsedTime = timeStamp.getStampSecond();
	logging::info("32bit Elapsed time %f mSec", int(elapsedTime*1000));


	uint64_t first64 = 0x0001000200010002LL;
	uint64_t second64 = 0x1000200010002000LL;
	
	timeStamp.initStamp();
	for(int i=0;i<loopCount;++i) {
		hamming.distance( first64, second64 );
	}
	elapsedTime = timeStamp.getStampSecond();
	logging::info("64bit Elapsed time %f mSec", int(elapsedTime*1000));


	uint128_t first128(first64, first64);
	uint128_t second128(second64, second64);
	timeStamp.initStamp();
	for(int i=0;i<loopCount;++i) {
		hamming.distance( first128, second128 );
	}
	elapsedTime = timeStamp.getStampSecond();
	logging::info("128bit Elapsed time %f mSec", int(elapsedTime*1000));

	uint256_t first256(first128, first128);
	uint256_t second256(second128, second128);
	timeStamp.initStamp();
	for(int i=0;i<loopCount;++i) {
		hamming.distance( first256, second256 );
	}
	elapsedTime = timeStamp.getStampSecond();
	logging::info("256bit Elapsed time %f mSec", int(elapsedTime*1000));

	uint512_t first512(first256, first256);
	uint512_t second512(second256, second256);

	timeStamp.initStamp();
	for(int i=0;i<loopCount;++i) {
		hamming.distance( first512, second512 );
	}
	elapsedTime = timeStamp.getStampSecond();
	logging::info("512bit Elapsed time %f mSec", int(elapsedTime*1000));
};
