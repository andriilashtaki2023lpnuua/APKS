---
mode: agent
description: Orchestrate project generation and validation on a feature branch.
---

Run the repository setup in this order:

1. Read `agents/build-engineer.agent.md`, `docs/architecture.md`, and the relevant skills.
2. Run the instructions in `prompts/git-init.prompt.md`; work on a `feature/...` branch created from `develop`.
3. Run `prompts/create-project.prompt.md` to generate the source and GoogleTest tests.
4. Run `prompts/create-build.prompt.md` to generate CMake and local build scripts.
5. Run `prompts/create-actions.prompt.md` to generate cross-platform CI.
6. Add or update `.gitignore`, `README.md`, and `docs/usage.md` so they cover the generated project and exact commands.
7. Run `prompts/check.prompt.md`, fix task-related failures, and report the verification results.

Do not claim a remote pull request, GitHub Actions success, or merge unless the corresponding operation actually occurred. Preserve existing user changes throughout.