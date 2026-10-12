---
mode: agent
description: Generate a branch-filtered three-OS workflow that only invokes build scripts.
---

Prerequisites: `create-build` completed and the checked-in build scripts exist. Invoke `.github/skills/github-actions/SKILL.md` with their paths.

Create or safely update `.github/workflows/ci.yml` with one job and a matrix for `ubuntu-latest`, `windows-latest`, and `macos-latest`. Trigger on push and pull_request targeting `develop` or `master`. Include checkout and invoke `ci.bat` on Windows or `bash ci.sh` elsewhere; keep build logic in the scripts.

Verify with `actionlint .github/workflows/ci.yml` when available and confirm no secret values are present. If YAML validation fails or actionlint is unavailable, report the exact status and do not claim GitHub Actions passed. Do not append duplicate jobs on rerun.