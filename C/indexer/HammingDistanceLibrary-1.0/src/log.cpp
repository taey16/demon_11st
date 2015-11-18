#include "log.h"
#include <fstream>
using namespace std;

#include <stdio.h>

#ifdef WIN32
	#include "stdafx.h"
#endif

namespace logging {


	#ifdef WIN32
		#define _write(prefix, x) TRACE("%s %s\n",prefix, x);
	#else
		#define _write(prefix, x) printf("%s %s\n",prefix, x);
	#endif

	
	void info(const char* format, ...)
	{
		char buffer[1024];

		va_list args;
		va_start (args, format);
		vsprintf (buffer,format, args);
		_write("[info]", buffer );
		va_end (args);
	}
	/*
	void logFile(string strFilename, string strMsg)
	{
		ofstream fout( strFilename, ios::app );
		fout<< strMsg <<endl;
		fout.close();
	}*/

};
