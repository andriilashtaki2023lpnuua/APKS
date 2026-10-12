#include "greeting.hpp"

#include <gtest/gtest.h>

TEST(GreetingTest, IncludesTheProvidedName) {
    EXPECT_EQ(make_greeting("Ada"), "Hello, Ada!");
}

TEST(GreetingTest, UsesWorldWhenNameIsEmpty) {
    EXPECT_EQ(make_greeting(""), "Hello, world!");
}