# Usage

## Local build and tests

Install CMake 3.20 or newer and a C++17 compiler. The first CMake configure downloads GoogleTest from GitHub, so network access is needed unless the dependency is already cached.

From the repository root:

```powershell
ci.bat
```

On Linux or macOS:

```sh
bash ci.sh
```

To run the steps separately on any platform:

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

The executable is `build/greeting_app` on single-configuration generators. With Visual Studio, it is under `build/Release/`. The tests cover a named greeting and the empty-name fallback.

## Run the VS Code agent

1. Check out `develop` to inspect or update the agent, skills, and prompts.
2. Open GitHub Copilot Chat and select the `build-engineer` custom agent.
3. Run the `init` prompt from the prompt picker. It creates a `feature/...` branch from `develop`, generates project files, and runs available checks.
4. Review the feature branch and run `ci.bat` or `bash ci.sh` locally.

The agent and prompts are stored in `agents/build-engineer.agent.md` and `prompts/`. GitHub Actions validates all three operating systems after the branch is pushed to GitHub. Creating a pull request titled `lab1/finish` requires a configured GitHub remote and GitHub access.