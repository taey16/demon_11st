#ifndef __TIMESTAMP_H__
#define __TIMESTAMP_H__

#include <time.h>
#include <stdint.h>

#if defined(__GNUC__)
	#include<sys/time.h>
	typedef uint64_t time_stamp;
	#define CLOCK_SECONDS_SCALE 1000000LL
#else
	typedef clock_t time_stamp;
	#define CLOCK_SECONDS_SCALE CLOCKS_PER_SEC
#endif

class TimeStamp
{
	public:
		TimeStamp();
		~TimeStamp();
	public:
		void initStamp();
		double getStampMilliSecond();
		double getStampSecond();

	protected:
		time_stamp _startMoment;

	private:
		time_stamp getClock();
};

#endif


