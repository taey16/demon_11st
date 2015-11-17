#include "TimeStamp.h"

TimeStamp::TimeStamp() {}

TimeStamp::~TimeStamp() {}

void TimeStamp::initStamp()
{
	_startMoment = getClock();
}

double TimeStamp::getStampMilliSecond()
{
	return getStampSecond()*1000;
}

double TimeStamp::getStampSecond()
{
	time_stamp thisMoment =getClock();
	return ((double) (thisMoment -_startMoment)) / CLOCK_SECONDS_SCALE ;
}

time_stamp TimeStamp::getClock()
{
	#if defined(__GNUC__)
		timespec ts;
		#if defined(_POSIX_TIMERS) && _POSIX_TIMERS>0
			clock_gettime(CLOCK_REALTIME, &ts);
		#else
			struct timeval tv;
			gettimeofday(&tv, NULL);
			ts.tv_sec = tv.tv_sec;
			ts.tv_nsec = tv.tv_usec * 1000;
		#endif
		return (time_stamp)ts.tv_sec * 1000000LL + (time_stamp)ts.tv_nsec / 1000LL;
	#else
		return clock();
	#endif
}

