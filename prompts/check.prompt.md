---
mode: agent
description: Read-only validation of scaffold, CMake build, tests, ignore rules, and CI YAML.
---

Prerequisites: generation stages are complete. This command is read-only: do not edit, stage, or commit files. Review the source, tests, CMake, scripts, workflow, `.gitignore`, README, and `docs/usage.md`.

Run the native build script with an absolute temporary build directory outside the repository so build/test validation does not change project files. Confirm the `hello` executable prints the expected greeting, `BasicAddition` passes, and `git check-ignore build/` succeeds. Validate `.github/workflows/ci.yml` with `actionlint` when installed; otherwise record YAML validation as not run. Report each check as PASS, FAIL, or NOT RUN, including the exact command and reason. Never fix files from this command and never claim remote Actions passed without a real run.

On any failure, include the first failing command, exit code, and concise diagnostic; leave the worktree untouched and tell the orchestrator which generation stage should be rerun. Example: `FAIL: cmake -S . -B <temp> (exit 1): CMake is unavailable.`