# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
Refresh star/language/last-commit fields in _data/projects.yml from
the GitHub REST API. Manual fields (repo, name, description, pinned)
are left untouched.

Invoked by .github/workflows/sync-stars.yml as:
    uv run .github/scripts/sync_stars.py
"""
from __future__ import annotations

import json
import os
import sys
from urllib.request import Request, urlopen

import yaml

API_BASE = "https://api.github.com"


def fetch_repo(repo: str, token: str) -> dict:
    """Call GET /repos/{repo}. Returns the parsed JSON body."""
    req = Request(
        f"{API_BASE}/repos/{repo}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "dimarkov.github.io-sync-stars",
        },
    )
    with urlopen(req) as response:
        return json.loads(response.read())


def update_projects(path: str, token: str) -> None:
    """Read projects YAML, refresh star fields, write back."""
    with open(path, encoding="utf-8") as f:
        projects = yaml.safe_load(f) or []

    for p in projects:
        repo = p.get("repo")
        if not repo:
            print(f"[skip] no repo field on entry: {p!r}", file=sys.stderr)
            continue
        try:
            data = fetch_repo(repo, token)
        except Exception as exc:
            print(f"[error] {repo}: {exc}", file=sys.stderr)
            continue
        p["stars"] = int(data.get("stargazers_count", 0))
        p["language"] = data.get("language") or ""
        # pushed_at = "2026-05-20T12:00:00Z" -> "2026-05-20"
        pushed = data.get("pushed_at", "")
        p["last_commit"] = pushed[:10] if pushed else ""
        print(f"[ok] {repo}: stars={p['stars']} language={p['language']} last={p['last_commit']}")

    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(projects, f, sort_keys=False, allow_unicode=True, default_flow_style=False)


if __name__ == "__main__":
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("GH_TOKEN env var is required", file=sys.stderr)
        sys.exit(1)
    update_projects("_data/projects.yml", token)
