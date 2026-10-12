---
name: project-scaffold
description: Create a small, portable C++ application and its source and test layout.
---

# Project Scaffold

Use this skill when creating the generated project on a feature branch.

## Procedure

1. Inspect the repository and preserve the agent files and any existing user work.
2. Create `src/main.cpp` and `tests/test_main.cpp`; keep application behavior small and deterministic.
3. Use standard C++ and avoid platform-specific APIs unless the task explicitly requires them.
4. Use GoogleTest for unit tests and keep tests independent of the console entry point.
5. Coordinate target names and source lists with `CMakeLists.txt` and the scripts described by `build-and-test`.
6. Document the project purpose and exact build/test commands in `README.md` and `docs/usage.md`.

## Expected layout

```text
src/main.cpp
tests/test_main.cpp
CMakeLists.txt
ci.bat
ci.sh
README.md
docs/usage.md
```

Do not generate build output or add secrets to the repository.