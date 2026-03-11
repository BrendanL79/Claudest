#!/usr/bin/env python3
"""Pre-commit hook: auto-bump patch version for plugins with staged changes,
and sync README badges (plugin README + root README section headers) in the
same pass so badges never lag behind plugin.json.

Skips any plugin whose plugin.json is already staged — that signals a manual
version bump is in progress and the hook should not interfere.

Skips any plugin where every staged file is README.md or CHANGELOG.md — docs-only
changes should not trigger a version bump.

Install via pre-commit:
    pip install pre-commit
    pre-commit install
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BADGE_RE = re.compile(
    r'!\[v[\d.]+\]\(https://img\.shields\.io/badge/v[\d.]+-blue\?style=flat-square\)'
)

DOCS_ONLY_FILENAMES = {"README.md", "CHANGELOG.md"}


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT).stdout.strip()


def git_add(path: str) -> None:
    result = subprocess.run(["git", "add", path], capture_output=True, text=True, cwd=ROOT)
    if result.returncode != 0:
        print(f"[auto-version] WARNING: git add {path} failed: {result.stderr.strip()}", file=sys.stderr)


def get_staged_files() -> list[str]:
    out = run(["git", "diff", "--cached", "--name-only"])
    return [f for f in out.split("\n") if f]


def bump_patch(version: str) -> str:
    parts = version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


def make_badge(version: str) -> str:
    return f"![v{version}](https://img.shields.io/badge/v{version}-blue?style=flat-square)"


def update_plugin_readme(plugin_name: str, new_version: str) -> None:
    readme = ROOT / "plugins" / plugin_name / "README.md"
    if not readme.exists():
        return
    content = readme.read_text()
    new_content = BADGE_RE.sub(make_badge(new_version), content, count=1)
    if new_content != content:
        readme.write_text(new_content)


def update_root_readme_badge(plugin_name: str, new_version: str) -> None:
    readme = ROOT / "README.md"
    if not readme.exists():
        return
    content = readme.read_text()
    # Match any ### heading line that contains the plugin name followed by a badge
    header_re = re.compile(
        r'(###[^\n]*\b' + re.escape(plugin_name) + r'\b[^\n]*?)'
        r'!\[v[\d.]+\]\(https://img\.shields\.io/badge/v[\d.]+-blue\?style=flat-square\)'
    )
    new_content = header_re.sub(r'\g<1>' + make_badge(new_version), content)
    if new_content != content:
        readme.write_text(new_content)


def is_docs_only(plugin_name: str, staged: list[str]) -> bool:
    for f in staged:
        if not f.startswith(f"plugins/{plugin_name}/"):
            continue
        if Path(f).name not in DOCS_ONLY_FILENAMES:
            return False
    return True


def main() -> None:
    staged = get_staged_files()
    if not staged:
        sys.exit(0)

    # Collect plugins with staged changes; track if plugin.json is manually staged
    changed_plugins: dict[str, bool] = {}
    for f in staged:
        m = re.match(r"plugins/([^/]+)/", f)
        if not m:
            continue
        name = m.group(1)
        if name not in changed_plugins:
            changed_plugins[name] = False
        if f == f"plugins/{name}/.claude-plugin/plugin.json":
            changed_plugins[name] = True  # manual bump — skip

    if not changed_plugins:
        sys.exit(0)

    bumped: dict[str, tuple[str, str]] = {}
    for plugin_name, has_manual_bump in changed_plugins.items():
        if has_manual_bump:
            continue
        if is_docs_only(plugin_name, staged):
            continue

        plugin_json = ROOT / "plugins" / plugin_name / ".claude-plugin" / "plugin.json"
        if not plugin_json.exists():
            continue

        data = json.loads(plugin_json.read_text())
        old = data["version"]
        new = bump_patch(old)
        data["version"] = new
        plugin_json.write_text(json.dumps(data, indent=2) + "\n")
        git_add(str(plugin_json))
        bumped[plugin_name] = (old, new)
        print(f"[auto-version] {plugin_name}: {old} → {new}")

    if not bumped:
        sys.exit(0)

    # Sync marketplace.json
    marketplace = ROOT / ".claude-plugin" / "marketplace.json"
    market = json.loads(marketplace.read_text())
    for plugin in market["plugins"]:
        if plugin["name"] in bumped:
            plugin["version"] = bumped[plugin["name"]][1]
    marketplace.write_text(json.dumps(market, indent=2) + "\n")
    git_add(str(marketplace))
    print("[auto-version] marketplace.json updated")

    # Sync README badges
    root_readme_dirty = False
    for plugin_name, (_, new_version) in bumped.items():
        update_plugin_readme(plugin_name, new_version)
        plugin_readme = ROOT / "plugins" / plugin_name / "README.md"
        if plugin_readme.exists():
            git_add(str(plugin_readme))

        root_readme = ROOT / "README.md"
        old_content = root_readme.read_text() if root_readme.exists() else ""
        update_root_readme_badge(plugin_name, new_version)
        if root_readme.exists() and root_readme.read_text() != old_content:
            root_readme_dirty = True

    if root_readme_dirty:
        git_add(str(ROOT / "README.md"))
        print("[auto-version] README.md badges updated")


if __name__ == "__main__":
    main()
