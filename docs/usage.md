# Usage

## Local build and tests

Install CMake 3.20 or newer and a C++17 compiler. The first CMake configure downloads GoogleTest from GitHub, so network access is needed unless the dependency is already cached. The project executable is named `hello` (`hello.exe` on Windows), and the unit test is `BasicAddition`.

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

The executable is `build/hello` on single-configuration generators and `build/Release/hello.exe` with Visual Studio. The test exercises `add(2, 3) == 5`.

For a read-only check that does not create build output in the repository, pass an external build directory:

```powershell
ci.bat "$env:TEMP\lab1-check-build"
```

```sh
bash ci.sh "${TMPDIR:-/tmp}/lab1-check-build"
```

After the default build, verify that Git ignores generated output with `git check-ignore build/`.

## Run the VS Code agent

1. Check out `develop` to inspect or update the agent, skills, and prompts.
2. Open GitHub Copilot Chat and select the `build-engineer` custom agent.
3. Run `/init` with project name `hello` and language `C++17` from the prompt picker. It runs `git-init`, `create-project`, `create-build`, `create-actions`, and the read-only `check` command in sequence without switching branches.
4. Review the feature branch and run `ci.bat` or `bash ci.sh` locally.

The agent and prompts are stored in `agents/build-engineer.agent.md` and `prompts/`; VS Code discovers them through `.vscode/settings.json`. Individual commands are `/git-init`, `/create-project`, `/create-build`, `/create-actions`, and `/check`. GitHub Actions runs the checked-in scripts for all three operating systems on pushes and pull requests targeting `develop` or `master`. Creating a pull request requires a configured GitHub remote and GitHub access.