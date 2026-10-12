---
name: project-scaffold
description: Create an idempotent Hello World scaffold from a project name and language, including README and ignore rules.
---

# Project Scaffold

Use this skill when the user requests a project scaffold. Inputs are `project_name` and `language`; preserve their spelling in the project title and choose language-appropriate source and run instructions. For this repository's required example, use project name `hello` and language `C++17`.

## Procedure

1. Inspect Git status, repository files, and existing README/ignore rules. Never replace unrelated content.
2. Create only missing directories and files. If a target exists, retain it and make only the smallest compatible addition; do not append duplicate sections or duplicate ignore entries.
3. Generate a minimal Hello World program in the chosen language and a README with the project name, prerequisites, and an exact runnable command. For C++17, the source is `src/main.cpp` and the executable is named `hello` after the build skill runs.
4. Create or update `.gitignore`, preserving current entries and idempotently adding build directories, caches, and local secrets.
5. Return a scaffold handoff containing the project name, language, source path, documented run command, files created/updated, and checks performed.

## Example input and result

Input: `project_name=hello`, `language=C++17`.

Expected result: `src/main.cpp` prints `Hello, World!`; `README.md` documents `ci.bat` on Windows and `bash ci.sh` on Linux/macOS; `.gitignore` excludes `build/`; the source path and run command are included in the handoff.

## Checks

- Confirm the language-specific source exists and contains the Hello World entry point.
- Confirm README contains a project title and a non-empty, copyable run command.
- Confirm `.gitignore` contains the build directory rule without adding duplicate rules on a second run.
- Do not claim the executable runs until the build stage has produced and invoked it.

## Typical failure

If the requested language has no configured scaffold or compiler, do not silently substitute another language. Preserve existing files, report `Unsupported language: <language>` or the missing tool, and ask the orchestrator to stop before build generation.

## Expected layout

```text
src/main.cpp
tests/test_main.cpp
CMakeLists.txt
ci.bat
ci.sh
README.md
docs/usage.md
```

Do not generate build output or add secrets to the repository.