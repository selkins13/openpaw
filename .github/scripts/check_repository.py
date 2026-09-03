#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = (
    ".editorconfig",
    ".gitignore",
    ".github/CODEOWNERS",
    ".github/copilot-instructions.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "TRADEMARKS.md",
    "docs/architecture.md",
    "docs/communication-protocol.md",
    "docs/continuous-integration.md",
    "docs/getting-started.md",
    "docs/hardware-spec.md",
    "docs/product-requirements.md",
    "docs/roadmap.md",
    "docs/tile-connector-standard.md",
    "hardware/bom/prototype-bom.md",
)

REQUIRED_DIRECTORIES = (
    "dashboard",
    "docs",
    "examples",
    "firmware/tile",
    "hardware/bom",
    "hardware/cad",
    "hardware/pcb",
    "hardware/printables",
    "hub/api",
    "hub/audio",
    "hub/services",
    "labels",
    "tests",
)

LICENSE_MARKERS = (
    "SPDX-License-Identifier: MIT",
    "SPDX-License-Identifier: CERN-OHL-P-2.0",
    "SPDX-License-Identifier: CC-BY-4.0",
)

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
TRAILING_WHITESPACE = re.compile(r"[ \t]+$")


def report(path: Path | None, message: str, line: int | None = None) -> None:
    location = ""
    if path is not None:
        location = f" file={path.relative_to(ROOT)}"
        if line is not None:
            location += f",line={line}"
    print(f"::error{location}::{message}")


def check_required_paths() -> int:
    failures = 0

    for relative_path in REQUIRED_FILES:
        path = ROOT / relative_path
        if not path.is_file():
            report(path, "Required repository file is missing")
            failures += 1

    for relative_path in REQUIRED_DIRECTORIES:
        path = ROOT / relative_path
        if not path.is_dir():
            report(path, "Required repository directory is missing")
            failures += 1

    return failures


def link_target(source: Path, raw_destination: str) -> Path | None:
    destination = raw_destination.strip()
    if destination.startswith("<") and destination.endswith(">"):
        destination = destination[1:-1]
    else:
        destination = destination.split(maxsplit=1)[0]

    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None

    return (source.parent / unquote(parsed.path)).resolve()


def check_markdown() -> int:
    failures = 0

    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            report(path, "Markdown file is not valid UTF-8")
            failures += 1
            continue

        if content and not content.endswith("\n"):
            report(path, "Markdown file must end with a newline")
            failures += 1

        for line_number, line in enumerate(content.splitlines(), start=1):
            if TRAILING_WHITESPACE.search(line):
                report(path, "Trailing whitespace is not allowed", line_number)
                failures += 1

        for match in MARKDOWN_LINK.finditer(content):
            target = link_target(path, match.group(1))
            if target is None:
                continue
            if ROOT not in target.parents and target != ROOT:
                report(path, f"Local link escapes the repository: {match.group(1)}")
                failures += 1
            elif not target.exists():
                report(path, f"Local link target does not exist: {match.group(1)}")
                failures += 1

    return failures


def check_licensing_and_ownership() -> int:
    failures = 0
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")

    for marker in LICENSE_MARKERS:
        if marker not in license_text:
            report(ROOT / "LICENSE", f"Missing license declaration: {marker}")
            failures += 1

    codeowners = (ROOT / ".github/CODEOWNERS").read_text(encoding="utf-8")
    if "* @selkins13" not in codeowners.splitlines():
        report(
            ROOT / ".github/CODEOWNERS",
            "Repository-wide ownership by @selkins13 is required",
        )
        failures += 1

    return failures


def main() -> int:
    failures = (
        check_required_paths()
        + check_markdown()
        + check_licensing_and_ownership()
    )
    if failures:
        print(f"{failures} repository check(s) failed.")
        return 1

    print("Repository checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
