cmake_minimum_required(VERSION 3.20)

project(lab1_hello LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(CTest)

add_library(project_math src/math.cpp)
target_include_directories(project_math PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)

add_executable(hello src/main.cpp)
target_link_libraries(hello PRIVATE project_math)

if(BUILD_TESTING)
    include(FetchContent)
    set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
    set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)
    FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
    )
    FetchContent_MakeAvailable(googletest)

    add_executable(hello_tests tests/test_main.cpp)
    target_link_libraries(hello_tests PRIVATE project_math GTest::gtest_main)

    include(GoogleTest)
    gtest_discover_tests(hello_tests)
endif()