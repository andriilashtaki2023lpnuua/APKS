#include "math.hpp"

#include <gtest/gtest.h>

TEST(MathTest, BasicAddition) {
    EXPECT_EQ(add(2, 3), 5);
}