#define BOOST_TEST_MODULE Test2
#include <boost/test/included/unit_test.hpp>

/** @file test2-simplest.cpp */

/// @def test3a
/// @req req-3a
BOOST_AUTO_TEST_CASE(test3a)
{
	int i = 1;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}


//! @def test3b
//! @req req-3b
BOOST_AUTO_TEST_CASE(test3b)
{
	int i = 5;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}

/*! 
 * @def test4a
 * @req req-4a */
BOOST_AUTO_TEST_CASE(test4a)
{
	int i = 5;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}

/** 
 * @def test4b
 * @req req-4b */
BOOST_AUTO_TEST_CASE(test4b)
{
	int i = 5;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}
