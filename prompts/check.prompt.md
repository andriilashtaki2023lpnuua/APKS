---
mode: agent
description: Check generated project files and run available validations.
---

Review the generated source, tests, CMake configuration, scripts, workflow, `.gitignore`, README, and `docs/usage.md` for consistency with the skills in `.github/skills/`. Run the native build/test script when possible, inspect Git status, and report each check as passed, failed, or not run with the reason. Fix only issues within this project-generation task. Do not claim GitHub Actions passed unless an actual workflow run is available.