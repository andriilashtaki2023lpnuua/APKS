---
mode: agent
description: Generate the cross-platform GitHub Actions workflow.
---

Follow `.github/skills/github-actions/SKILL.md`. Create `.github/workflows/ci.yml` with Windows, Linux, and macOS jobs that invoke the repository's platform build scripts. Match the actual script names and shell behavior. Keep permissions minimal and do not introduce secrets.