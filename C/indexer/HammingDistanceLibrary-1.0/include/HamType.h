#ifndef __HAMTYPE_H__
#define __HAMTYPE_H__

#include<stdint.h>

#if !defined(__WIN32) && !defined(_WIN32_)
	typedef unsigned char BYTE;		// 8bit
	typedef unsigned short WORD;		// 16bit
	typedef unsigned long DWORD;		// 32bit
#endif

typedef struct _uint128_t
{
	_uint128_t() {}
	_uint128_t(const uint64_t& copy ):hi(0LL), low(copy){}
	_uint128_t(const _uint128_t& copy ):hi(copy.hi), low(copy.low){}
	_uint128_t(uint64_t iHi, uint64_t iLo) : hi(iHi), low(iLo){	}
	
	
	uint64_t hi;
	uint64_t low;
} uint128_t;


typedef struct _uint256_t {
	_uint256_t() {}
	_uint256_t(const _uint256_t& copy ):hi(copy.hi), low(copy.low){}
	_uint256_t(uint128_t iHi, uint128_t iLo) : hi(iHi), low(iLo) { }
	uint128_t hi;
	uint128_t low;
	
} uint256_t;

typedef struct _uint512_t {
	_uint512_t() {}
	_uint512_t(const _uint512_t& copy ):hi(copy.hi), low(copy.low){}
	_uint512_t(uint256_t iHi, uint256_t iLo) : hi(iHi), low(iLo) { }
	uint256_t hi;
	uint256_t low;
} uint512_t;


#if !defined(__WIN32) && !defined(_WIN32_)
	#define HIBYTE(l) ((BYTE)(((WORD)(l)>>8) & 0xFF))
	#define LOBYTE(l) ((BYTE)(l))
	#define HIWORD(l) ((WORD)(((DWORD)(l)>>16) & 0xFFFF))
	#define LOWORD(l) ((WORD)(l))
#endif

#define HIUINT32(l) ((uint32_t)(((uint64_t)(l)>>32) & 0xFFFFFFFF))
#define LOUINT32(l) ((uint32_t)(l))

#define HIUINT64(l) (uint64_t)uint128_t(l).hi
#define LOUINT64(l) (uint64_t)uint128_t(l).low

#define HIUINT128(l) (uint128_t)uint256_t(l).hi
#define LOUINT128(l) (uint128_t)uint256_t(l).low

#define HIUINT256(l) (uint256_t)uint512_t(l).hi
#define LOUINT256(l) (uint256_t)uint512_t(l).low

uint128_t operator^(const uint128_t& a, const uint128_t& b);
uint256_t operator^(const uint256_t& a, const uint256_t& b);
uint512_t operator^(const uint512_t& a, const uint512_t& b);

#endif
