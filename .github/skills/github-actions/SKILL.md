---
name: github-actions
description: Add cross-platform GitHub Actions CI for the CMake and GoogleTest project.
---

# GitHub Actions

Create `.github/workflows/ci.yml` to run the repository's build script on `windows-latest`, `ubuntu-latest`, and `macos-latest`.

## Requirements

- Trigger on pushes and pull requests.
- Use a matrix with all three operating systems and a clear job name.
- Check out the repository with `actions/checkout` and use the hosted runner's CMake or install a pinned, supported CMake version.
- Invoke `ci.bat` on Windows and `bash ci.sh` on Linux/macOS.
- Let script failures fail the job; do not mark jobs as allowed to fail.
- Use a reasonable job timeout and least-privilege workflow permissions (`contents: read`).
- Avoid secrets and unnecessary third-party actions.

Validate YAML structure and ensure workflow commands match the checked-in scripts.