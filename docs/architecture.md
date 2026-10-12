# Architecture

## Problems solved

The build engineer turns a project name and language into a repeatable Hello World scaffold, a tested build, and cross-platform CI. It reduces inconsistent hand-created files, missing test/build steps, accidental tracking of build output, and CI that duplicates local build logic. The required example uses C++17, emits `hello`, and verifies `BasicAddition` with GoogleTest.

## Skills

- `project-scaffold` accepts the project name and language, creates the source, README, directory layout, and idempotent `.gitignore` entries, then verifies the source and documented run command.
- `build-and-test` creates the CMake configuration, reusable addition function, `BasicAddition` unit test, and `ci.bat`/`ci.sh`. The scripts configure, build, run tests, and produce `hello`.
- `github-actions` creates a single matrix job for Windows, Linux, and macOS. The workflow checks out source and delegates configure/build/test to the checked-in scripts.

## User commands

Commands are prompt files registered from `prompts/` in `.vscode/settings.json`.

| Command | Responsibility | Main outputs |
| --- | --- | --- |
| `git-init` | Inspect or initialize Git, add missing ignore rules, report status | `.gitignore` |
| `create-project` | Run `project-scaffold` with project name and language | source, README, directories |
| `create-build` | Run `build-and-test` | `CMakeLists.txt`, function/test, `ci.bat`, `ci.sh` |
| `create-actions` | Run `github-actions` | `.github/workflows/ci.yml` |
| `check` | Read-only structure, build, tests, ignore, and YAML validation | report only; no project files |
| `init` | Run all commands in dependency order | complete project and verification report |

Every command states preconditions, actions, outputs, checks, and an actionable failure message. Repeated runs preserve existing content and add only missing compatible configuration.

## Data passed between stages

`init` receives `project_name` and `language` from the user. `git-init` returns repository state, active branch, and ignore-check result. `create-project` receives those values and returns source/README paths, run command, and files changed. `create-build` receives the source paths and language, then returns CMake target, build/test commands, script paths, and tool/exit status. `create-actions` receives script paths and returns workflow path, matrix/trigger settings, and YAML validation result. `check` receives all paths and commands and returns PASS/FAIL/NOT RUN results with diagnostics. Each handoff includes unresolved errors; no stage infers success from file existence alone.

## Error handling and reruns

The orchestrator checks stage preconditions, runs one command at a time, and stops at the first failure. It preserves partial files and user changes, reports the stage, exact failing command, exit code, diagnostic, completed stages, and safe resume point. It does not roll back or conceal failures; the user reruns the failed command after correcting the cause. Commands inspect existing files, avoid duplicate sections/rules/jobs, and never overwrite unrelated content. `check` is strictly read-only and directs build output to a temporary directory outside the worktree.

## Repository branches

- `develop` contains the build-engineer agent, reusable skills, generation prompts, and this architecture guide.
- A `feature/...` branch starts from `develop` and adds the generated C++ project, tests, build configuration, CI workflow, and usage documentation.
- `master` is the final integration branch. Merge a verified feature branch into it only after review and successful checks. A GitHub pull request titled `lab1/finish` requires a configured GitHub remote and must not be represented as created until GitHub confirms it.

## Generation flow

`prompts/init.prompt.md` orchestrates `git-init`, `create-project`, `create-build`, `create-actions`, and `check` in sequence. The first three generation commands defer to their corresponding skills under `.github/skills/`; `check` validates without repairing or modifying files.

## Generated project

The feature branch contains a portable C++17 Hello World application under `src/`, a reusable addition function and GoogleTest `BasicAddition` under `tests/`, a CMake build that emits `hello`, platform-specific CI scripts, and a three-operating-system GitHub Actions workflow. `README.md` and `docs/usage.md` explain the project and exact local commands. Build output, caches, and secrets are excluded from version control.

## Verification boundary

Local script results establish only the local platform's build and test status. A successful GitHub Actions matrix requires an actual workflow run. Remote pull requests and merges require a configured remote and successful GitHub operation.