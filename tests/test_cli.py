"""Tests for the CLI commands."""

from pathlib import Path

from typer.testing import CliRunner

from airules.cli import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "One config" in result.output


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_list():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "claude-md" in result.output
    assert "cursorrules" in result.output
    assert "copilot" in result.output


def test_init(tmp_path):
    result = runner.invoke(app, ["init", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / ".airules.toml").exists()


def test_init_no_overwrite(tmp_path):
    (tmp_path / ".airules.toml").write_text("[project]\nname = 'x'\n")
    result = runner.invoke(app, ["init", str(tmp_path)])
    assert result.exit_code == 1
    assert "already exists" in result.output


def test_init_force_overwrite(tmp_path):
    (tmp_path / ".airules.toml").write_text("[project]\nname = 'x'\n")
    result = runner.invoke(app, ["init", str(tmp_path), "--force"])
    assert result.exit_code == 0


def test_generate(tmp_path):
    config = """\
[project]
name = "test"

[style]
rules = ["Be consistent"]

[targets]
enabled = ["claude-md"]
"""
    (tmp_path / ".airules.toml").write_text(config)
    result = runner.invoke(app, ["generate", str(tmp_path), "--config", str(tmp_path / ".airules.toml")])
    assert result.exit_code == 0
    assert (tmp_path / "CLAUDE.md").exists()


def test_generate_dry_run(tmp_path):
    config = """\
[project]
name = "test"

[style]
rules = ["Be consistent"]

[targets]
enabled = ["claude-md"]
"""
    (tmp_path / ".airules.toml").write_text(config)
    result = runner.invoke(app, ["generate", str(tmp_path), "--config", str(tmp_path / ".airules.toml"), "--dry-run"])
    assert result.exit_code == 0
    assert not (tmp_path / "CLAUDE.md").exists()
    assert "would write" in result.output


def test_validate_valid(tmp_path):
    config = """\
[project]
name = "test"

[style]
rules = ["Be consistent"]

[targets]
enabled = ["claude-md"]
"""
    (tmp_path / ".airules.toml").write_text(config)
    result = runner.invoke(app, ["validate", "--config", str(tmp_path / ".airules.toml")])
    assert result.exit_code == 0
    assert "valid" in result.output


def test_validate_invalid(tmp_path):
    config = """\
[project]
name = ""

[targets]
enabled = []
"""
    (tmp_path / ".airules.toml").write_text(config)
    result = runner.invoke(app, ["validate", "--config", str(tmp_path / ".airules.toml")])
    assert result.exit_code == 1


def test_diff_no_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["diff"])
    assert result.exit_code == 1


def test_diff_no_changes(tmp_path):
    config = """\
[project]
name = "test"

[style]
rules = ["Be consistent"]

[targets]
enabled = ["claude-md"]
"""
    (tmp_path / ".airules.toml").write_text(config)
    # First generate
    runner.invoke(app, ["generate", str(tmp_path), "--config", str(tmp_path / ".airules.toml")])
    # Then diff — should show unchanged
    result = runner.invoke(app, ["diff", str(tmp_path), "--config", str(tmp_path / ".airules.toml")])
    assert result.exit_code == 0
    assert "unchanged" in result.output
