# Hello World C++ Project

A minimal cross-platform C++17 Hello World application with a GoogleTest `BasicAddition` test, CMake, and GitHub Actions for Windows, Linux, and macOS.

## Run locally

Prerequisites: Python 3.8+, a C++17 compiler, CMake 3.20 or newer, and network access on the first configure so CMake can download GoogleTest.

On Windows, run `ci.bat` from a terminal. On Linux or macOS, run `bash ci.sh`. Both scripts configure and build the `hello` executable, then run the `BasicAddition` unit test with CTest. Build output goes to the ignored `build/` directory by default.

The detailed setup and agent invocation steps are in [docs/usage.md](docs/usage.md).

Run the read-only project audit with `python scripts/check_project.py`. It validates project customization, build/test behavior, Git hygiene, workflow structure, and the AI log. See [docs/ai-log.md](docs/ai-log.md) for the recorded requests, responses, errors, and decisions.

## Generate with the agent

Open this repository in VS Code with GitHub Copilot Chat. Use the `build-engineer` custom agent and run the `init` prompt from the prompt picker. The agent instructions, skills, and prompt files live in `agents/`, `.github/skills/`, and `prompts/` on the `develop` branch. See [docs/architecture.md](docs/architecture.md) for the branch and generation flow.