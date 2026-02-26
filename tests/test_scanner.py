"""Tests for the codebase scanner."""

import json
from pathlib import Path

from dotruler.scanner import (
    scan_commands,
    scan_existing_ai_configs,
    scan_frameworks,
    scan_languages,
    scan_project,
)


def test_scan_languages(tmp_path):
    (tmp_path / "app.py").write_text("print('hello')")
    (tmp_path / "index.ts").write_text("console.log('hello')")
    (tmp_path / "main.go").write_text("package main")

    langs = scan_languages(tmp_path)
    assert "python" in langs
    assert "typescript" in langs
    assert "go" in langs


def test_scan_languages_skips_node_modules(tmp_path):
    nm = tmp_path / "node_modules" / "pkg"
    nm.mkdir(parents=True)
    (nm / "index.js").write_text("module.exports = {}")
    (tmp_path / "app.py").write_text("print('hello')")

    langs = scan_languages(tmp_path)
    assert "python" in langs
    assert "javascript" not in langs


def test_scan_frameworks_from_config_files(tmp_path):
    (tmp_path / "next.config.js").write_text("module.exports = {}")
    (tmp_path / "tailwind.config.js").write_text("module.exports = {}")

    frameworks = scan_frameworks(tmp_path)
    assert "nextjs" in frameworks
    assert "tailwind" in frameworks


def test_scan_frameworks_from_package_json(tmp_path):
    pkg = {"dependencies": {"react": "^18.0.0", "express": "^4.0.0"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))

    frameworks = scan_frameworks(tmp_path)
    assert "react" in frameworks
    assert "express" in frameworks


def test_scan_commands_from_package_json(tmp_path):
    pkg = {"scripts": {"build": "next build", "test": "jest", "dev": "next dev"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))

    commands = scan_commands(tmp_path)
    assert commands["build"] == "npm run build"
    assert commands["test"] == "npm test"
    assert commands["dev"] == "npm run dev"


def test_scan_commands_python_fallback(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'\n")

    commands = scan_commands(tmp_path)
    assert commands["test"] == "pytest"
    assert commands["lint"] == "ruff check ."


def test_scan_existing_ai_configs(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("# Rules")
    (tmp_path / ".cursorrules").write_text("rules")
    github_dir = tmp_path / ".github"
    github_dir.mkdir()
    (github_dir / "copilot-instructions.md").write_text("instructions")

    configs = scan_existing_ai_configs(tmp_path)
    assert "claude-md" in configs
    assert "cursorrules" in configs
    assert "copilot" in configs


def test_scan_project_full(tmp_path):
    (tmp_path / "app.py").write_text("print('hello')")
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'\n")
    (tmp_path / "CLAUDE.md").write_text("# Rules")

    result = scan_project(tmp_path)
    assert "python" in result["languages"]
    assert "test" in result["commands"]
    assert "claude-md" in result["existing_ai_configs"]
