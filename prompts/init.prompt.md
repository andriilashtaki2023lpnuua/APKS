---
mode: agent
description: Orchestrate Git setup, named project scaffolding, build/tests, CI generation, and read-only checks.
---

Inputs: `project_name` and `language` from the user's request. If either is missing, ask before creating files. Preserve the current branch; this command does not silently create, switch, commit, or push branches.

Run commands sequentially: `git-init` -> `create-project` -> `create-build` -> `create-actions` -> `check`.

Expected outputs: `.gitignore`, `README.md`, `src/main.cpp`, `src/math.hpp`, `src/math.cpp`, `CMakeLists.txt`, `tests/test_main.cpp`, `ci.bat`, `ci.sh`, `.github/workflows/ci.yml`, and `docs/usage.md`. Reuse compatible existing files rather than recreating or duplicating them.

At each handoff, pass the project name/language, active branch, created or updated paths, run/build/test commands, tool versions, exit codes, and unresolved diagnostics to the next stage. Confirm each stage's preconditions before invoking it. Repeated runs inspect existing files and add only missing compatible content.

Error policy: on the first failed prerequisite, command, or validation, stop dependent stages; preserve all files and user changes; do not roll back, overwrite, or pretend success. Report the failed stage, exact command, exit code, diagnostic, completed stages, and safe resume point. Do not run `check` as a repair step. Final success requires source and documented run command, `hello` executable, passing `BasicAddition`, ignored `build/`, valid workflow, and accurate README/usage docs. Clearly mark unavailable local or remote checks as NOT RUN.

Verification commands: `git status --short --branch`, `git check-ignore build/`, the native `ci.bat` or `bash ci.sh` (using an external temporary build directory for `check`), and `actionlint .github/workflows/ci.yml` when installed. On failure, report `init stopped at <command>: exit <code> - <diagnostic>; resume with /<stage>.` Never continue past a failed prerequisite.

Do not claim a remote pull request, GitHub Actions success, or merge unless the corresponding operation actually occurred. Preserve existing user changes throughout.