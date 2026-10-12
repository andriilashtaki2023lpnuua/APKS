---
mode: agent
description: Scaffold a named Hello World project in the requested language.
argument-hint: "<project-name> <language>"
---

Prerequisites: `git-init` completed and the workspace/project name and language are known. Invoke `.github/skills/project-scaffold/SKILL.md` with `project_name` and `language` from the user's request; do not infer a different language silently.

Expected files: language-specific source, `README.md`, and a non-destructive `.gitignore` update. For `hello`/`C++17`, create `src/main.cpp` printing `Hello, World!`; document the exact run command. Verify the source exists, the command is present in README, and build output is ignored.

On conflict or unsupported language, preserve existing files and report `Scaffold blocked: <reason>` with the source paths inspected. Do not duplicate README sections or ignore entries on rerun.