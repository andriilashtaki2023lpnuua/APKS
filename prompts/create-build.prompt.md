---
mode: agent
description: Generate CMake, a testable addition function, BasicAddition test, and local build scripts.
---

Prerequisites: `create-project` completed and source paths/language are known. Invoke `.github/skills/build-and-test/SKILL.md` with the scaffold handoff.

For C++17, create or update `CMakeLists.txt`, `src/math.hpp`, `src/math.cpp`, `tests/test_main.cpp`, `ci.bat`, and `ci.sh`. Build the Hello World executable as `hello` and register a GoogleTest named `BasicAddition`. Scripts must configure, build, run CTest, propagate failures, default to `build/`, and accept an optional build directory.

Verify with the native script, run the produced `hello`, require `BasicAddition` to pass, and check `git check-ignore build/`. Preserve compatible existing targets/tests and never add build products to Git. On missing tools/dependency, report `Build blocked: <command and reason>` and stop; do not report unrun tests as passing.