# Architecture

## Repository branches

- `develop` contains the build-engineer agent, reusable skills, generation prompts, and this architecture guide.
- A `feature/...` branch starts from `develop` and adds the generated C++ project, tests, build configuration, CI workflow, and usage documentation.
- `master` is the final integration branch. Merge a verified feature branch into it only after review and successful checks. A GitHub pull request titled `lab1/finish` requires a configured GitHub remote and must not be represented as created until GitHub confirms it.

## Generation flow

`prompts/init.prompt.md` orchestrates the task. It prepares the branches, then invokes the project scaffold, build/test, and GitHub Actions prompts in sequence. Those prompts each defer to the corresponding skill under `.github/skills/` for detailed implementation requirements. Finally, the check prompt verifies consistency and runs available local validation.

## Generated project

The feature branch contains a portable C++17 application under `src/`, GoogleTest unit tests under `tests/`, a CMake build, platform-specific CI scripts, and a three-operating-system GitHub Actions workflow. `README.md` and `docs/usage.md` explain the project and reproducible local commands. Build output, caches, and secrets are excluded from version control.

## Verification boundary

Local script results establish only the local platform's build and test status. A successful GitHub Actions matrix requires an actual workflow run. Remote pull requests and merges require a configured remote and successful GitHub operation.