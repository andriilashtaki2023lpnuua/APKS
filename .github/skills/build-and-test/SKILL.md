---
name: build-and-test
description: Create an idempotent CMake build, a testable function and BasicAddition unit test, and local CI scripts.
---

# Build and Test

## Purpose

Create a portable build, an independently testable function and unit test, and scripts that perform configure/build/test.

## Inputs

- Project name and language from `project-scaffold`.
- Source paths and the exact run command from the scaffold handoff.
- Existing build configuration, targets, and tests.

## Outputs

- `CMakeLists.txt` and the named CMake executable/test targets.
- Testable function source/header and GoogleTest test.
- `ci.bat` and `ci.sh`, including optional external build-directory support.
- Handoff containing configure/build/test commands, target names, tool versions, and exit results.

Preserve existing targets and tests unless they directly conflict with the requested project.

## CMake requirements

- Require CMake 3.20 or newer and declare a C++ project.
- Require C++17 without compiler extensions.
- Build the Hello World application from `src/main.cpp` with output name `hello` (`hello.exe` on Windows).
- Provide a small `add(int left, int right)` function in a reusable source/header pair and cover it with a GoogleTest named `BasicAddition` in `tests/test_main.cpp`.
- Use CTest and GoogleTest. Prefer pinned GoogleTest `FetchContent` so CI does not depend on a preinstalled package.
- Register tests with `gtest_discover_tests` or `add_test` and enable testing.
- Keep warnings and build settings portable across MSVC, GCC, and Clang.

## Local scripts

- `ci.sh` and `ci.bat` must configure, build, and run CTest with failure output enabled. Their default build directory is `build/`; accept an optional build-directory argument so read-only checks can build outside the repository.
- Propagate each failing command's nonzero exit status. Do not hide build or test failures.
- Use a multi-configuration-safe CMake invocation so the scripts also work with Visual Studio generators.

## Verification

Run the native script for the current platform when its required tools are installed. Verify the `hello` executable exists and prints the greeting, `BasicAddition` passes, and `git check-ignore build/` succeeds. For `check`, pass a temporary directory outside the repository to the script so validation does not modify project files. Report missing CMake, compiler, or network access instead of claiming success. Never commit generated build output.

## Example input and result

Input: `project_name=hello`, `language=C++17`, scaffold source `src/main.cpp`.

Expected result: `CMakeLists.txt`, `src/math.hpp`, `src/math.cpp`, `tests/test_main.cpp`, `ci.bat`, and `ci.sh`; the CMake target emits `hello`, and CTest discovers `BasicAddition`.

## Checks

- Configure and build using the platform script; preserve and report its exit code.
- Run CTest with failure output enabled and require `BasicAddition` to pass.
- Run `hello` and compare its output to `Hello, World!` (allow the platform newline).
- Verify `build/` is ignored and the optional external build path leaves the worktree unchanged.

## Typical failure

If CMake, a C++17 compiler, or the GoogleTest download is unavailable, report the failing command and prerequisite. Do not remove the test, replace it with an unverified echo, or report the build as successful.