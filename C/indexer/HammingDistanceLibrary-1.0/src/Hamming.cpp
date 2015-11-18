#include "Hamming.h"
#include <math.h>


/*
Hamming::Hamming()	
	:_pLookup(0)
{
	#if defined(__LOOKUP_TABLE_8_POPCNT__) || defined(__LOOKUP_TABLE_16_POPCNT__)
		_initLookupTable();
	#endif
}


Hamming::~Hamming()
{
	#if defined(__LOOKUP_TABLE_8_POPCNT__) || defined(__LOOKUP_TABLE_16_POPCNT__)
		_releaseLookupTable();
	#endif
}
*/


void Hamming::_initLookupTable()
{	
	int totalBit = 0;
	#if defined(__LOOKUP_TABLE_8_POPCNT__)
		totalBit = sizeof(unsigned char)*8;
	#elif defined(__LOOKUP_TABLE_16_POPCNT__)
		totalBit = sizeof(WORD)*8;
	#endif
	_lookupTableSize = int(pow(2.,double(totalBit) ));
	_pLookup = new char[_lookupTableSize];

	for(uint32_t i=0;i<(uint32_t)_lookupTableSize;++i)
		_pLookup[i] = _popcntBitTwiddling( i );	
}


void Hamming::_releaseLookupTable()
{
	if(_pLookup)
	{
		delete [] _pLookup;
		_pLookup = 0;
	}
}


int Hamming::_popcntBitTwiddling( uint32_t& data )
{
	int c=0;
	uint32_t copiedData = data;
	for(;copiedData;c++) {
		copiedData &= copiedData-1;
	}
	return c;
}
