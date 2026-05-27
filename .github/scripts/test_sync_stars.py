# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml", "pytest"]
# ///
"""
Tests for sync_stars.py.

Run with:  uv run .github/scripts/test_sync_stars.py
       or: uv run --with pyyaml --with pytest python -m pytest .github/scripts/test_sync_stars.py -v
"""
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import yaml
import pytest

# Make sync_stars importable when running this file directly via uv
sys.path.insert(0, str(Path(__file__).resolve().parent))

import sync_stars


SAMPLE_YAML = """\
- repo: owner/repo-a
  name: repo-a
  description: First repo.
  stars: 5
  language: Python
  last_commit: "2020-01-01"
  pinned: true

- repo: owner/repo-b
  name: repo-b
  description: Second repo.
  stars: 0
  language: ""
  last_commit: ""
  pinned: false
"""


def make_api_response(*, stars, language, pushed_at):
    """Build a fake urllib.request.urlopen response."""
    body = json.dumps({
        "stargazers_count": stars,
        "language": language,
        "pushed_at": pushed_at,
    }).encode("utf-8")
    response = MagicMock()
    response.read.return_value = body
    response.__enter__ = lambda self: self
    response.__exit__ = lambda *args: None
    return response


def test_update_projects_overwrites_stars_language_last_commit(tmp_path):
    data_file = tmp_path / "projects.yml"
    data_file.write_text(SAMPLE_YAML)

    fake_responses = [
        make_api_response(stars=42, language="Python",  pushed_at="2026-05-20T12:00:00Z"),
        make_api_response(stars=7,  language="Jupyter", pushed_at="2026-05-21T08:30:00Z"),
    ]

    with patch("sync_stars.urlopen", side_effect=fake_responses):
        sync_stars.update_projects(str(data_file), token="fake-token")

    result = yaml.safe_load(data_file.read_text())
    assert result[0]["stars"] == 42
    assert result[0]["language"] == "Python"
    assert result[0]["last_commit"] == "2026-05-20"
    assert result[1]["stars"] == 7
    assert result[1]["language"] == "Jupyter"
    assert result[1]["last_commit"] == "2026-05-21"


def test_update_projects_preserves_manual_fields(tmp_path):
    """`description`, `name`, `repo`, `pinned` must NOT be touched."""
    data_file = tmp_path / "projects.yml"
    data_file.write_text(SAMPLE_YAML)

    fake_responses = [
        make_api_response(stars=99, language="Rust", pushed_at="2026-05-22T00:00:00Z"),
        make_api_response(stars=1,  language="Go",   pushed_at="2026-05-23T00:00:00Z"),
    ]

    with patch("sync_stars.urlopen", side_effect=fake_responses):
        sync_stars.update_projects(str(data_file), token="t")

    result = yaml.safe_load(data_file.read_text())
    assert result[0]["repo"] == "owner/repo-a"
    assert result[0]["name"] == "repo-a"
    assert result[0]["description"] == "First repo."
    assert result[0]["pinned"] is True
    assert result[1]["pinned"] is False


def test_update_projects_handles_api_error(tmp_path):
    """If the API call for one repo fails, the others still update."""
    data_file = tmp_path / "projects.yml"
    data_file.write_text(SAMPLE_YAML)

    fake_responses = [
        Exception("network"),
        make_api_response(stars=3, language="Python", pushed_at="2026-05-24T00:00:00Z"),
    ]

    with patch("sync_stars.urlopen", side_effect=fake_responses):
        sync_stars.update_projects(str(data_file), token="t")

    result = yaml.safe_load(data_file.read_text())
    # repo-a unchanged (5 was the initial value)
    assert result[0]["stars"] == 5
    # repo-b updated
    assert result[1]["stars"] == 3


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
