#define BOOST_TEST_MODULE Test1
#include <boost/test/included/unit_test.hpp>

/// @req req-3a
BOOST_AUTO_TEST_CASE(test3a)
{
	int i = 1;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}


//! @req req-3b
BOOST_AUTO_TEST_CASE(test3b)
{
	int i = 5;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}
