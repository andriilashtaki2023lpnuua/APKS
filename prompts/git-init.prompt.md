---
mode: agent
description: Initialize or inspect Git, idempotently update ignore rules, and report repository status.
---

Prerequisites: a writable workspace and Git installed.

1. Check `git rev-parse --is-inside-work-tree`. If this is a new directory, initialize Git without deleting or replacing files; otherwise leave the current branch unchanged.
2. Inspect `.gitignore`; create it if missing, otherwise add only missing rules for `/build/`, caches, and local secrets. Preserve all existing content.
3. Run `git status --short --branch` and report the active branch and existing changes. Do not stage or commit user files.

Expected files: `.gitignore` only if absent or missing required rules. Verification: `git status --short --branch` and `git check-ignore build/`. Repeated runs must not duplicate ignore entries.

On failure, report the failed Git command and exit code; do not switch branches, discard changes, force-push, or claim a remote operation succeeded. Example error: `Git is not installed or this directory cannot be initialized; no project files were changed.`