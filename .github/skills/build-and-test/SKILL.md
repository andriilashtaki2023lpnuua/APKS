---
name: build-and-test
description: Configure a portable CMake build, GoogleTest unit tests, and local CI scripts.
---

# Build and Test

Use this skill to create and verify the C++ build configuration.

## CMake requirements

- Require CMake 3.20 or newer and declare a C++ project.
- Require C++17 without compiler extensions.
- Build the application from `src/main.cpp`.
- Use CTest and GoogleTest for `tests/test_main.cpp`. Prefer `FetchContent` for GoogleTest so CI does not depend on a preinstalled package.
- Register tests with `gtest_discover_tests` or `add_test` and enable testing.
- Keep warnings and build settings portable across MSVC, GCC, and Clang.

## Local scripts

- `ci.sh` and `ci.bat` must configure into `build/`, build the project, and run CTest with failure output enabled.
- Propagate each failing command's nonzero exit status. Do not hide build or test failures.
- Use a multi-configuration-safe CMake invocation so the scripts also work with Visual Studio generators.

## Verification

Run the native script for the current platform when its required tools are installed. Report missing CMake, compiler, or network access instead of claiming success. Do not add generated build directories to version control.