#!/usr/bin/env python3
"""Read-only audit for the Hello World agent project."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SKILLS = {
    "project-scaffold": ["## Purpose", "## Inputs", "## Outputs", "## Checks"],
    "build-and-test": ["## Purpose", "## Inputs", "## Outputs", "## Checks"],
    "github-actions": ["## Purpose", "## Inputs", "## Outputs", "## Checks"],
}
COMMANDS = {
    "git-init": [".gitignore", "git status --short --branch"],
    "create-project": ["project-scaffold/SKILL.md", "project_name", "README.md"],
    "create-build": ["build-and-test/SKILL.md", "BasicAddition", "CMakeLists.txt"],
    "create-actions": ["github-actions/SKILL.md", ".github/workflows/ci.yml"],
    "check": ["read-only", "scripts/check_project.py", "PASS, FAIL, or NOT RUN"],
    "init": ["git-init", "create-project", "create-build", "create-actions", "check"],
}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
]
SECRET_NAMES = {".env", "id_rsa", "id_ed25519", "credentials.json", "secrets.json"}


class Audit:
    def __init__(self) -> None:
        self.failures = 0
        self.blocked = 0

    def check(self, label: str, passed: bool, detail: str = "") -> None:
        state = "PASS" if passed else "FAIL"
        print(f"{state}: {label}" + (f" - {detail}" if detail else ""))
        if not passed:
            self.failures += 1

    def not_run(self, label: str, detail: str = "") -> None:
        print(f"NOT RUN: {label}" + (f" - {detail}" if detail else ""))
        self.blocked += 1


def read_text(root: Path, relative_path: str) -> str:
    try:
        return (root / relative_path).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


def has_populated_section(document: str, heading: str) -> bool:
    match = re.search(rf"(?m)^{re.escape(heading)}\s*$", document)
    if not match:
        return False
    next_heading = re.search(r"(?m)^## ", document[match.end():])
    content = document[match.end():match.end() + next_heading.start()] if next_heading else document[match.end():]
    return any(line.strip() and not line.lstrip().startswith("<!--") for line in content.splitlines())


def run_process(command: list[str], root: Path, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


def check_manifest(root: Path, audit: Audit) -> None:
    path = root / "agents/build-engineer.agent.md"
    text = read_text(root, "agents/build-engineer.agent.md")
    required = [
        "# Build Engineer",
        "## Responsibilities",
        "## Rules",
        "## Forbidden actions",
        "## Completion criteria",
    ]
    audit.check("agent manifest exists", path.is_file(), str(path))
    audit.check("manifest defines role, limits, and completion criteria", all(item in text for item in required))


def check_customization(root: Path, audit: Audit) -> None:
    for skill_name, headings in SKILLS.items():
        relative = f".github/skills/{skill_name}/SKILL.md"
        content = read_text(root, relative)
        audit.check(
            f"skill contract: {skill_name}",
            bool(content) and all(heading in content for heading in headings),
            "purpose, inputs, outputs, checks",
        )

    for command_name, tokens in COMMANDS.items():
        relative = f"prompts/{command_name}.prompt.md"
        content = read_text(root, relative)
        has_description = re.search(r"(?m)^description:\s*.+$", content) is not None
        audit.check(
            f"command action: /{command_name}",
            bool(content) and has_description and all(token in content for token in tokens),
            "prompt exists, is discoverable, and names its action",
        )

    init = read_text(root, "prompts/init.prompt.md")
    ordered_commands = ["git-init", "create-project", "create-build", "create-actions", "check"]
    sequence = re.search(r"(?m)^Run commands sequentially:\s*(.+)$", init)
    listed_commands = re.findall(r"`([a-z-]+)`", sequence.group(1)) if sequence else []
    ordered = listed_commands == ordered_commands
    init_skill = read_text(root, ".github/skills/project-scaffold/SKILL.md")
    forbidden_mutations = ["git reset --hard", "git clean -fd", "git checkout --", "git push --force", "rm -rf"]
    repeat_safe = (
        "Repeated runs inspect existing files and add only missing compatible content" in init
        and "preserve all files and user changes" in init
        and "does not silently create, switch, commit, or push branches" in init
        and "Create only missing directories and files" in init_skill
        and not any(command in init.lower() for command in forbidden_mutations)
    )
    audit.check("init invokes commands in dependency order", ordered)
    audit.check("init reruns preserve files and avoid destructive Git operations", repeat_safe)


def check_project_files(root: Path, audit: Audit) -> None:
    required_files = [
        ".gitignore",
        "README.md",
        "docs/architecture.md",
        "docs/usage.md",
        "docs/ai-log.md",
        "CMakeLists.txt",
        "ci.bat",
        "ci.sh",
        "src/main.cpp",
        "src/math.cpp",
        "src/math.hpp",
        "tests/test_main.cpp",
        "scripts/check_project.py",
        ".github/workflows/ci.yml",
    ]
    missing = [name for name in required_files if not (root / name).is_file()]
    audit.check("required project files exist", not missing, ", ".join(missing))

    main = read_text(root, "src/main.cpp")
    test = read_text(root, "tests/test_main.cpp")
    cmake = read_text(root, "CMakeLists.txt")
    ignore = read_text(root, ".gitignore")
    audit.check("Hello World source and executable target are declared", "Hello, World!" in main and "add_executable(hello" in cmake)
    audit.check("BasicAddition unit test is declared", "BasicAddition" in test and "gtest_discover_tests" in cmake)
    audit.check("build output is ignored", re.search(r"(?m)^/build/$", ignore) is not None)

    journal = read_text(root, "docs/ai-log.md")
    journal_sections = ["## User requests", "## Important responses", "## Errors", "## Accepted decisions"]
    audit.check(
        "AI journal records requests, responses, errors, and decisions",
        all(has_populated_section(journal, section) for section in journal_sections),
    )

    readme = read_text(root, "README.md")
    usage = read_text(root, "docs/usage.md")
    pr = read_text(root, "docs/pull-request.md")
    audit.check(
        "README and usage provide runnable commands",
        all(token in readme + usage for token in ("ci.bat", "bash ci.sh", "scripts/check_project.py")),
    )
    audit.check(
        "PR notes link the requested review material",
        all(token in pr for token in ("lab1/finish", "ai-log.md", "architecture.md", "usage.md", "ci.yml", "python scripts/check_project.py")),
    )


def check_workflow(root: Path, audit: Audit) -> None:
    workflow = read_text(root, ".github/workflows/ci.yml").replace("\r\n", "\n")
    expected_runners = ["ubuntu-latest", "windows-latest", "macos-latest"]
    runners_present = all(workflow.count(f"- {runner}") == 1 for runner in expected_runners)
    events_valid = True
    for event in ("push", "pull_request"):
        match = re.search(
            rf"(?ms)^  {event}:\n(?P<body>.*?)(?=^  [A-Za-z_][A-Za-z0-9_-]*:\s*$|\Z)",
            workflow,
        )
        body = match.group("body") if match else ""
        branches = re.findall(r"(?m)^      - ([^\s]+)\s*$", body)
        events_valid = events_valid and "develop" in branches and "master" in branches
    audit.check("workflow uses exactly the three required operating systems", runners_present)
    audit.check("workflow triggers on push and pull_request to develop/master", events_valid)

    jobs_match = re.search(r"(?ms)^jobs:\n(?P<body>.*)\Z", workflow)
    jobs_body = jobs_match.group("body") if jobs_match else ""
    job_names = re.findall(r"(?m)^  ([A-Za-z0-9_-]+):\s*$", jobs_body)
    runs = re.findall(r"(?m)^\s+run:\s*(.+?)\s*$", jobs_body)
    script_only = len(runs) == 2 and set(runs) == {"ci.bat", "bash ./ci.sh"}
    audit.check("workflow has one job and delegates execution to build scripts", len(job_names) == 1 and script_only)

    workflow_path = root / ".github/workflows/ci.yml"
    actionlint = shutil.which("actionlint")
    if actionlint:
        result = run_process([actionlint, str(workflow_path)], root)
        audit.check("workflow YAML/schema via actionlint", result.returncode == 0, result.stdout.strip())
        return
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        audit.not_run("workflow YAML syntax parser", "install actionlint or PyYAML; structural checks ran")
        return
    try:
        yaml.safe_load(workflow)
        audit.check("workflow YAML syntax via PyYAML", True)
    except Exception as error:  # PyYAML exposes parser-specific exception classes.
        audit.check("workflow YAML syntax via PyYAML", False, str(error))


def git_paths(root: Path) -> tuple[list[str], str]:
    result = run_process(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], root)
    if result.returncode != 0:
        return [], result.stdout.strip()
    return [entry for entry in result.stdout.split("\0") if entry], ""


def check_git_hygiene(root: Path, audit: Audit, static_only: bool) -> bytes | None:
    if static_only:
        print("NOT RUN: Git/build hygiene skipped by --static-only")
        return None
    try:
        before = subprocess.check_output(["git", "status", "--porcelain=v1", "-z"], cwd=root)
        paths, error = git_paths(root)
    except (OSError, subprocess.CalledProcessError) as error:
        audit.check("Git repository status is available", False, str(error))
        return None

    audit.check("Git file inventory is available", not error, error)
    build_paths = [
        path for path in paths
        if any(part.lower() == "build" or part.lower().startswith("cmake-build") for part in Path(path).parts)
    ]
    audit.check("no build directories are tracked or pending in Git", not build_paths, ", ".join(build_paths))

    secret_paths = []
    secret_hits = []
    for relative in paths:
        path = Path(relative)
        lowered = path.name.lower()
        if lowered in SECRET_NAMES or lowered.endswith((".pem", ".key")) or (lowered.startswith(".env") and lowered != ".env.example"):
            secret_paths.append(relative)
            continue
        full_path = root / path
        try:
            if not full_path.is_file() or full_path.stat().st_size > 4 * 1024 * 1024:
                continue
            raw = full_path.read_bytes()
            if b"\0" in raw:
                continue
            content = raw.decode("utf-8", errors="ignore")
            if any(pattern.search(content) for pattern in SECRET_PATTERNS):
                secret_hits.append(relative)
        except OSError:
            continue
    audit.check("no obvious credentials or secret files are in Git", not secret_paths and not secret_hits, ", ".join(secret_paths + secret_hits))

    ignored = run_process(["git", "check-ignore", "--quiet", "build/"], root)
    audit.check("build/ is ignored by Git", ignored.returncode == 0)
    return before


def check_local_build(root: Path, audit: Audit, static_only: bool) -> None:
    if static_only:
        print("NOT RUN: local configure/build/tests skipped by --static-only")
        return
    script = root / ("ci.bat" if os.name == "nt" else "ci.sh")
    if not script.is_file():
        audit.check("native build script exists", False, str(script))
        return
    if shutil.which("cmake") is None:
        audit.not_run("local configure/build and BasicAddition", "CMake is not available in PATH")
        return

    before = None
    try:
        before = subprocess.check_output(["git", "status", "--porcelain=v1", "-z"], cwd=root)
    except (OSError, subprocess.CalledProcessError):
        pass

    try:
        with tempfile.TemporaryDirectory(prefix="lab1-check-") as temporary:
            build_dir = str(Path(temporary) / "build")
            command = (["cmd.exe", "/d", "/c", str(script), build_dir]
                       if os.name == "nt" else ["bash", str(script), build_dir])
            result = run_process(command, root, timeout=900)
            output = result.stdout.strip()
            build_ok = result.returncode == 0 and "100% tests passed" in output and "BasicAddition" in output
            audit.check("local configure/build and BasicAddition", build_ok, output[-1800:])
            if build_ok:
                candidates = [Path(build_dir) / "hello", Path(build_dir) / "hello.exe"]
                candidates.extend([Path(build_dir) / "Release" / "hello.exe", Path(build_dir) / "Debug" / "hello.exe"])
                executable = next((candidate for candidate in candidates if candidate.is_file()), None)
                if executable is None:
                    audit.check("built hello executable exists", False, "searched single- and multi-config output paths")
                else:
                    run = run_process([str(executable)], root, timeout=30)
                    audit.check("hello prints Hello, World!", run.returncode == 0 and run.stdout.strip() == "Hello, World!", run.stdout.strip())
    except (OSError, subprocess.TimeoutExpired) as error:
        audit.check("local configure/build and BasicAddition", False, str(error))

    if before is not None:
        try:
            after = subprocess.check_output(["git", "status", "--porcelain=v1", "-z"], cwd=root)
            audit.check("check leaves Git worktree unchanged", before == after)
        except (OSError, subprocess.CalledProcessError) as error:
            audit.check("check leaves Git worktree unchanged", False, str(error))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="project root to audit (defaults to this repository)")
    parser.add_argument("--static-only", action="store_true", help="skip Git and build checks; useful for isolated fault demonstrations")
    arguments = parser.parse_args()
    root = (arguments.root or Path(__file__).resolve().parents[1]).resolve()
    audit = Audit()

    audit.check("project root exists", root.is_dir(), str(root))
    check_manifest(root, audit)
    check_customization(root, audit)
    check_project_files(root, audit)
    check_workflow(root, audit)
    before = check_git_hygiene(root, audit, arguments.static_only)
    check_local_build(root, audit, arguments.static_only)

    if before is not None:
        try:
            after = subprocess.check_output(["git", "status", "--porcelain=v1", "-z"], cwd=root)
            audit.check("audit leaves Git worktree unchanged", before == after)
        except (OSError, subprocess.CalledProcessError) as error:
            audit.check("audit leaves Git worktree unchanged", False, str(error))

    if audit.failures or audit.blocked:
        print(f"CHECK INCOMPLETE: {audit.failures} failed check(s), {audit.blocked} required check(s) not run.")
        return 1
    print("CHECK PASSED: all required checks succeeded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())