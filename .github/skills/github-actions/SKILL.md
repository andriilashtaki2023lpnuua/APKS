---
name: github-actions
description: Create and validate a three-OS GitHub Actions matrix that delegates build and tests to checked-in scripts.
---

# GitHub Actions

## Purpose

Create a cross-platform workflow that delegates all configure/build/test behavior to checked-in platform scripts.

## Inputs

- Existing `ci.bat` and `ci.sh` paths and their invocation conventions.
- Required runner matrix and push/pull_request branch filters.
- Build/test handoff and current GitHub Actions constraints.

## Outputs

- `.github/workflows/ci.yml` with one job and the three-OS matrix.
- Workflow validation result and a handoff describing triggers, runners, scripts, and diagnostics.

Create `.github/workflows/ci.yml` only after the platform build scripts exist. The workflow checks out the repository and invokes those scripts; all configure, compile, executable, and test logic stays in `ci.bat` or `ci.sh`.

## Requirements

- Trigger on push and pull request targeting `develop` or `master` only.
- Use one job with a matrix containing `ubuntu-latest`, `windows-latest`, and `macos-latest`.
- Check out the repository with `actions/checkout`.
- Invoke `ci.bat` on Windows and `bash ci.sh` on Linux/macOS. Do not duplicate CMake or test commands in YAML.
- Let script failures fail the job; do not mark jobs as allowed to fail.
- Use a reasonable job timeout and least-privilege workflow permissions (`contents: read`).
- Avoid secrets and unnecessary third-party actions.

Keep a clear per-OS job name, useful timeout, and least-privilege `contents: read` permission. Do not store credentials or secrets in the workflow or repository.

## Example input and result

Input: existing `ci.bat` and `ci.sh` scripts.

Expected result: one matrix job in `.github/workflows/ci.yml`, filtered to push/pull_request on `develop` and `master`, with checkout and exactly one OS-appropriate script invocation per matrix leg.

## Checks

- Validate YAML with `actionlint .github/workflows/ci.yml` when installed.
- Confirm the matrix has exactly the three required runner labels and the trigger branch filters include both target branches.
- Confirm every run step invokes a checked-in script and no configure/build/test commands or secrets are embedded in YAML.
- Verify action/job failures are not ignored.

## Typical failure

If `actionlint` is unavailable or reports a syntax/schema error, report that check as not run or failed and the exact diagnostic. Do not claim GitHub validation; only a real Actions run can establish remote success.