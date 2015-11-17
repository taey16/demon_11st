#include "HamType.h"


uint128_t operator^(const uint128_t& a, const uint128_t& b)
{
	uint128_t r(a.hi^b.hi,a.low^b.low);
	return r;
}


uint256_t operator^(const uint256_t& a, const uint256_t& b)
{
	uint256_t r(a.hi^b.hi,a.low^b.low);
	return r;
}

uint512_t operator^(const uint512_t& a, const uint512_t& b)
{
	uint512_t r(a.hi^b.hi,a.low^b.low);
	return r;
}


