# Usage

## Local build and tests

Install CMake 3.20 or newer and a C++17 compiler. The first CMake configure downloads GoogleTest from GitHub, so network access is needed unless the dependency is already cached. The project executable is named `hello` (`hello.exe` on Windows), and the unit test is `BasicAddition`.

Python 3.8+ is required for the repository audit. YAML syntax validation requires `actionlint` or PyYAML; the audit reports a missing validator rather than treating it as a pass.

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

## Read-only check

From the repository root run:

```sh
python scripts/check_project.py
```

The checker audits the agent manifest; skill inputs, outputs, and checks; command actions and order; init rerun-safety instructions; source, executable target, and `BasicAddition`; workflow OS/branch/script contract; ignored build output and likely secrets; and required AI-log sections. It runs the platform CI script with an OS temporary build directory, validates YAML with `actionlint` or PyYAML, and verifies that Git status did not change. A failed or unavailable required check returns a nonzero code.

## Manual verification and demonstration

1. In Copilot Chat, select `build-engineer` and run `/init` with `hello` and `C++17`; demonstrate the five commands in order.
2. Run `python scripts/check_project.py` and review its PASS/FAIL output. Confirm Git status is unchanged.
3. To demonstrate a deliberate failure without touching the working project, copy or clone the repository into a temporary directory, remove `src/main.cpp` only in that copy, then run `python scripts/check_project.py --root <temporary-copy> --static-only`. It should fail on the missing source. Remove the temporary copy afterward.
4. Show the agent manifest, skills, command prompts, architecture, and [AI log](ai-log.md).
5. Record the demonstration and upload it to the instructor-designated folder. That destination was not supplied here, so this repository change does not claim a video upload.

## Run the VS Code agent

1. Check out `develop` to inspect or update the agent, skills, and prompts.
2. Open GitHub Copilot Chat and select the `build-engineer` custom agent.
3. Run `/init` with project name `hello` and language `C++17` from the prompt picker. It runs `git-init`, `create-project`, `create-build`, `create-actions`, and the read-only `check` command in sequence without switching branches.
4. Review the feature branch and run `ci.bat` or `bash ci.sh` locally.

The agent and prompts are stored in `agents/build-engineer.agent.md` and `prompts/`; VS Code discovers them through `.vscode/settings.json`. Individual commands are `/git-init`, `/create-project`, `/create-build`, `/create-actions`, and `/check`. GitHub Actions runs the checked-in scripts for all three operating systems on pushes and pull requests targeting `develop` or `master`. Creating a pull request requires a configured GitHub remote and GitHub access.