---
mode: agent
description: Prepare the repository branches for the generated C++ project.
---

Inspect the current Git state first. If Git is not initialized, initialize it without overwriting files. Ensure the automation instructions are committed on `develop`. Create a descriptive `feature/...` branch from `develop` for generated project files. Preserve existing changes, do not force-push, and do not claim to have created a remote branch or pull request without a configured remote and successful GitHub operation. Report the branch names and any blocker.