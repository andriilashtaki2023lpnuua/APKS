# Lab 1: C++ Build Engineer

A small cross-platform C++17 greeting application with GoogleTest, CMake, and GitHub Actions for Windows, Linux, and macOS.

## Run locally

Prerequisites: a C++17 compiler, CMake 3.20 or newer, and network access on the first configure so CMake can download GoogleTest.

On Windows, run `ci.bat` from a terminal. On Linux or macOS, run `bash ci.sh`. Both scripts configure and build into the ignored `build/` directory, then run the unit tests with CTest.

The detailed setup and agent invocation steps are in [docs/usage.md](docs/usage.md).

## Generate with the agent

Open this repository in VS Code with GitHub Copilot Chat. Use the `build-engineer` custom agent and run the `init` prompt from the prompt picker. The agent instructions, skills, and prompt files live in `agents/`, `.github/skills/`, and `prompts/` on the `develop` branch. See [docs/architecture.md](docs/architecture.md) for the branch and generation flow.