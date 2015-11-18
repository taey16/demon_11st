#ifndef __LOG_H__
#define __LOG_H__

#include <stdarg.h>
#include <string>
using namespace std;


namespace logging {
	void info(const char* format, ...);
	void logFile(string strFilename, string strMsg);
};

#endif
