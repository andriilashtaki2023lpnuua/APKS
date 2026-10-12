---
mode: agent
description: Read-only validation of scaffold, CMake build, tests, ignore rules, and CI YAML.
---

Prerequisites: generation stages are complete and Python 3.8+ is available. This command is read-only: do not edit, stage, or commit files.

Run `python scripts/check_project.py`. The checker audits the agent manifest, all skill input/output/check contracts, all six commands and their ordering, init rerun safety, source/test/build outputs, three-OS workflow/branch filters, Git-tracked build directories and likely secrets, and the AI journal. It runs the native CI script with an external temporary build directory, checks the `hello` output and `BasicAddition`, validates YAML with `actionlint` or PyYAML, and confirms Git status is unchanged.

The checker reports each result as PASS, FAIL, or NOT RUN and exits nonzero for failed or unavailable required checks. Do not reinterpret NOT RUN as PASS. On any failure, report the exact command, exit code, diagnostic, completed checks, and the responsible generation stage. Never repair files here or claim remote Actions passed without a real run. For a safe intentional-failure demonstration, use a temporary clone and `--static-only --root <clone>` as documented in `docs/usage.md`.