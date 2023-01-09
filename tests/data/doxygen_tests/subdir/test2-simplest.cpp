#define BOOST_TEST_MODULE Test2
#include <data/included/unit_test.hpp>

/** \file subdir/test2-simplest.cpp */

/// \verify req-3a
void test3a();
BOOST_AUTO_TEST_CASE(test3a)
{
	int i = 1;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}


//! \verify req-3b
void test3b();
BOOST_AUTO_TEST_CASE(test3b)
{
	int i = 5;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}

/*! 
 * \verify req-4a */
void test4a();
BOOST_AUTO_TEST_CASE(test4a)
{
	int i = 5;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}

/** 
 * \verify req-4b */
void test4b();
BOOST_AUTO_TEST_CASE(test4b)
{
	int i = 5;
	BOOST_CHECK(i > 4);
	BOOST_CHECK(i > i * i);
}
