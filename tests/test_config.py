"""Tests for config loading and validation."""

from pathlib import Path

import dotruler.outputs  # noqa: F401
from dotruler.config import _parse_config, load_config, validate_config


def test_parse_config_full(sample_toml, tmp_path):
    config_path = tmp_path / ".dotruler.toml"
    config_path.write_text(sample_toml)

    config = load_config(config_path)

    assert config.project.name == "myapp"
    assert config.project.description == "A test application"
    assert config.project.languages == ["typescript", "python"]
    assert config.project.frameworks == ["nextjs", "fastapi"]
    assert len(config.style.rules) == 2
    assert config.commands.build == "npm run build"
    assert config.commands.test == "pytest && npm test"
    assert len(config.architecture.notes) == 2
    assert config.targets.enabled == ["claude-md", "cursorrules", "copilot"]
    assert "claude-md" in config.targets.overrides
    assert config.targets.overrides["claude-md"].extra_rules == ["Use Read tool first"]


def test_parse_empty_config():
    config = _parse_config({})
    assert config.project.name == ""
    assert config.style.rules == []
    assert config.targets.enabled == ["claude-md", "cursorrules", "copilot"]


def test_validate_valid_config(sample_config):
    issues = validate_config(sample_config)
    assert not issues


def test_validate_missing_name(sample_config):
    sample_config.project.name = ""
    issues = validate_config(sample_config)
    assert any("[error] project.name is required" in i for i in issues)


def test_validate_empty_rules(sample_config):
    sample_config.style.rules = []
    issues = validate_config(sample_config)
    assert any("style.rules is empty" in i for i in issues)


def test_validate_empty_targets(sample_config):
    sample_config.targets.enabled = []
    issues = validate_config(sample_config)
    assert any("targets.enabled is empty" in i for i in issues)


def test_validate_unknown_target(sample_config):
    sample_config.targets.enabled.append("nonexistent")
    issues = validate_config(sample_config)
    assert any("unknown target 'nonexistent'" in i for i in issues)
