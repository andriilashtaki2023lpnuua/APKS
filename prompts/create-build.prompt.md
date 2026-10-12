---
mode: agent
description: Generate CMake configuration and local build/test scripts.
---

Follow `.github/skills/build-and-test/SKILL.md`. Create `CMakeLists.txt`, `ci.sh`, and `ci.bat` that configure, build, and execute the project's GoogleTest suite. Ensure script failures propagate, use the `build/` directory, and do not commit generated build output. Run the platform-appropriate script if the required tools are available and report the result accurately.