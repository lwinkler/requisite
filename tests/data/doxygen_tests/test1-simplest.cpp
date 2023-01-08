#define BOOST_TEST_MODULE Test1
#include <boost/tests/data/included/unit_test.hpp>

/** @file test1-simplest.cpp */

/// @verify req-1a
void test1a();
BOOST_AUTO_TEST_CASE(test1a)
{
	int i = 1;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}


//! @verify req-1b
void test1b();
BOOST_AUTO_TEST_CASE(test1b)
{
	int i = 5;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}

/** 
 * @verify req-2a */
void test2a();
BOOST_AUTO_TEST_CASE(test2a)
{
	int i = 5;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}

/*! 
 * @verify req-2b */
void test2b();
BOOST_AUTO_TEST_CASE(test2b)
{
	int i = 5;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}
