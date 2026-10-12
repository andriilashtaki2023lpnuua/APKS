# AI Interaction Log

This log records material requests, important responses, errors, and accepted decisions. It contains no credentials or private tokens.

## User requests

- Create `develop`, `feature/...`, and `master` branches containing the agent architecture, skills, commands, generated C++ project, tests, build scripts, and cross-platform CI.
- Refine the workflow for a named, language-aware Hello World scaffold, CMake/GoogleTest, a `BasicAddition` test, three-OS CI, idempotent commands, and exact local usage instructions.
- Require `check` and manual review to cover agent/skill/command contracts, orchestration order and reruns, local build/tests, workflow matrix, Git hygiene, and an AI interaction journal.
- Use meaningful commits, prepare a PR titled `lab1/finish`, link logs/architecture/test/Actions results, and document a safe failure demo and video steps.

## Important responses

- Initialized the local repository at `D:\LAB_1`; `develop` stores reusable customization, `feature/lab1-cpp-project` stores the generated project, and `master` remains the final integration target.
- Added a C++17 Hello World executable named `hello` and a GoogleTest `BasicAddition` case.
- Made local scripts accept an external build directory so `check` can build/test without writing output into the repository.
- Added `scripts/check_project.py`, a read-only audit that checks customization contracts, project outputs, workflow structure, Git hygiene, and native tests.
- Documented the command sequence, data handoffs, stop-on-error behavior, and safe rerun policy.

## Errors

- The initial workspace was not a Git repository. Git was initialized on `develop` without deleting workspace contents.
- CMake was unavailable; `ci.bat` could not configure. CMake Tools also failed to configure, and a user-level CMake install attempt failed.
- PyYAML and `actionlint` were unavailable during earlier checks. Workflow structure was inspected, but YAML schema validation and remote Actions remain pending.
- An early PowerShell contract check mishandled CRLF and case-sensitive comparisons. The checker was corrected; the skill/command contract validation then passed.
- The first audit implementation searched for the first occurrence of command names across all prose and falsely flagged `check` ordering. It now parses the explicit `Run commands sequentially` line; rerunning the audit confirmed the correct order.
- The first complete audit found CMake and a YAML parser unavailable. It now reports those as `NOT RUN` and still exits nonzero, rather than claiming success or mislabeling a missing tool as a syntax failure.
- Bash was absent from `PATH`, but was found at `C:\msys64\usr\bin\bash.exe`; `bash -n ci.sh` passed.
- Direct `g++` verification passed for `Hello, World!` and `add(2, 3) == 5`. The GoogleTest suite itself has not run because CMake is unavailable.

## Accepted decisions

- Keep the agent, skills, commands, checker, and architecture on `develop`; merge those reusable instructions into the generated feature branch.
- Keep generated sources, CI, usage docs, AI log, and PR notes on `feature/lab1-cpp-project`.
- Keep agent, skills/commands, program, and CI work in separate meaningful commits; merge develop customization into feature before final integration.
- Do not merge feature into `master` or claim a PR/Actions success until required local and remote checks pass.
- Do not fabricate a remote: `git remote -v` returned no configured remote, so GitHub PR creation and Actions links are blocked.
- The instructor's video destination was not supplied; document the demo flow rather than claiming an upload.

## Verification status

- PASS: direct C++17 compilation and Hello World output.
- PASS: direct addition check for `2 + 3 == 5`.
- PASS: `git check-ignore build/`, `git diff --check`, and `bash -n ci.sh`.
- PASS: the project audit's manifest, skill/command contracts, command order/rerun policy, project-file, journal, workflow-structure, Git-hygiene, and unchanged-worktree checks.
- NOT RUN: CMake configure/build and GoogleTest, because CMake is unavailable.
- NOT RUN: actionlint/PyYAML YAML parsing and GitHub Actions, because validators/remote are unavailable. The full audit correctly exits nonzero while required checks are not run.