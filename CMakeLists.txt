cmake_minimum_required(VERSION 3.20)

project(lab1_greeting LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(CTest)

add_library(greeting src/greeting.cpp)
target_include_directories(greeting PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

add_executable(greeting_app src/main.cpp)
target_link_libraries(greeting_app PRIVATE greeting)

if(BUILD_TESTING)
    include(FetchContent)
    set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
    set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)
    FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
    )
    FetchContent_MakeAvailable(googletest)

    add_executable(greeting_tests tests/test_main.cpp)
    target_link_libraries(greeting_tests PRIVATE greeting GTest::gtest_main)

    include(GoogleTest)
    gtest_discover_tests(greeting_tests)
endif()