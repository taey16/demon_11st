#ifndef __HAMDISTANCE_H__
#define __HAMDISTANCE_H__

#include "HamType.h"
#include <stdint.h>

#if defined(_MSC_VER) && (defined(_WIN32) || defined(_WIN64))
  #include <nmmintrin.h>	// _mm_popcnt_u32(), _mm_popcnt_u64()
#endif

class Hamming
{
	public:
		//Hamming();
		//~Hamming();

	public:
		static int distance(uint32_t& first, uint32_t& second)
		{
			unsigned long xored = first ^ second;
			return _popcnt( xored );
		}

		static int distance(uint64_t& first, uint64_t& second)
		{
			uint64_t xored = first^second;
			#if (defined(_WIN64) || defined(__x86_64__)) && !defined(__LOOKUP_TABLE_8_POPCNT__) && !defined(__LOOKUP_TABLE_16_POPCNT__)
				return _popcnt( xored );
			#else
				return _popcnt( HIUINT32(xored) ) + _popcnt( LOUINT32(xored) );
			#endif
		}

		static int distance(uint128_t& first, uint128_t& second)
		{
			return distance(first.hi, second.hi) + distance(first.low, second.low);
		}

		static int distance(uint256_t& first, uint256_t& second)
		{
			return distance(first.hi, second.hi) + distance(first.low, second.low);
		}

		static int distance(uint512_t& first, uint512_t& second)
		{
			return distance(first.hi, second.hi) + distance(first.low, second.low);
		}

	protected:
		int _lookupTableSize;
		char* _pLookup;		// 8bit or 16bit Table
		void _initLookupTable();
		void _releaseLookupTable();
		
	private:
		// To initialize LookupTable, when SSE4 is not available.
		static int _popcntBitTwiddling( uint32_t& data );		

	public:

	#if defined(__LOOKUP_TABLE_8_POPCNT__)
		static inline uint32_t _popcnt(uint32_t x) 
		{
			WORD hiWord = HIWORD( x );
			WORD loWord = LOWORD( x );
			return _pLookup[ HIBYTE(hiWord) ] + _pLookup[ LOBYTE(hiWord) ]
				+ _pLookup[ HIBYTE(loWord) ] + _pLookup[ LOBYTE(loWord) ];
		}
	#elif defined(__LOOKUP_TABLE_16_POPCNT__)
		static inline uint32_t _popcnt(uint32_t x)
		{
			return _pLookup[ HIWORD(x) ] + _pLookup[ LOWORD(x) ];
		}
	#elif defined(_MSC_VER) && defined(_WIN64)
		static inline uint64_t _popcnt(uint64_t x) 
		{
			return _mm_popcnt_u64(x);
		}
	#elif defined(_MSC_VER) && defined(_WIN32)
		static inline uint32_t _popcnt(uint32_t x) 
		{
			return _mm_popcnt_u32(x);
		}				
	#elif defined(__x86_64__)		
		// SSE4
		// GNU GCC >= 4.2 supports the POPCNT instruction
		static inline uint64_t _popcnt(uint64_t x) 
		{
		#if !defined(__GNUC__) || (__GNUC__ >= 4 && __GNUC_MINOR__ >= 1)
			__asm__ ("popcnt %1, %0" : "=r" (x) : "0" (x));
		#endif
			return x;
		}
	#elif defined(__i386__) || defined(__i386)
		static inline uint32_t _popcnt(uint32_t x) {
		#if !defined(__GNUC__) || (__GNUC__ >= 4 && __GNUC_MINOR__ >= 1)
			__asm__ ("popcnt %1, %0" : "=r" (x) : "0" (x));
		#endif
			return x;
		}
	#endif
};

#endif
