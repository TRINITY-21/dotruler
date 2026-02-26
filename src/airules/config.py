"""TOML config loading and validation."""

from __future__ import annotations

import tomllib
from pathlib import Path

from airules.models import (
    AiRulesConfig,
    ArchitectureConfig,
    CommandsConfig,
    ProjectConfig,
    StyleConfig,
    TargetOverride,
    TargetsConfig,
)

CONFIG_FILENAME = ".airules.toml"


def find_config(start: Path | None = None) -> Path | None:
    """Find .airules.toml starting from the given directory, walking up."""
    current = start or Path.cwd()
    for directory in [current, *current.parents]:
        config_path = directory / CONFIG_FILENAME
        if config_path.exists():
            return config_path
    return None


def load_config(path: Path) -> AiRulesConfig:
    """Load and parse .airules.toml into typed config."""
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    return _parse_config(raw)


def _parse_config(raw: dict) -> AiRulesConfig:
    """Convert raw TOML dict into typed AiRulesConfig."""
    project = _parse_project(raw.get("project", {}))
    style = _parse_style(raw.get("style", {}))
    commands = _parse_commands(raw.get("commands", {}))
    architecture = _parse_architecture(raw.get("architecture", {}))
    targets = _parse_targets(raw.get("targets", {}))

    return AiRulesConfig(
        project=project,
        style=style,
        commands=commands,
        architecture=architecture,
        targets=targets,
    )


def _parse_project(data: dict) -> ProjectConfig:
    return ProjectConfig(
        name=data.get("name", ""),
        description=data.get("description", ""),
        languages=data.get("languages", []),
        frameworks=data.get("frameworks", []),
    )


def _parse_style(data: dict) -> StyleConfig:
    return StyleConfig(rules=data.get("rules", []))


def _parse_commands(data: dict) -> CommandsConfig:
    return CommandsConfig(
        build=data.get("build", ""),
        test=data.get("test", ""),
        lint=data.get("lint", ""),
        dev=data.get("dev", ""),
    )


def _parse_architecture(data: dict) -> ArchitectureConfig:
    return ArchitectureConfig(notes=data.get("notes", []))


def _parse_targets(data: dict) -> TargetsConfig:
    enabled = data.get("enabled", ["claude-md", "cursorrules", "copilot"])
    overrides: dict[str, TargetOverride] = {}

    for key, value in data.items():
        if key == "enabled":
            continue
        if isinstance(value, dict):
            overrides[key] = TargetOverride(
                extra_rules=value.get("extra_rules", []),
                output_path=value.get("output_path", ""),
            )

    return TargetsConfig(enabled=enabled, overrides=overrides)


def validate_config(config: AiRulesConfig) -> list[str]:
    """Validate config and return list of warnings/errors."""
    issues: list[str] = []

    if not config.project.name:
        issues.append("[error] project.name is required")

    if not config.style.rules:
        issues.append("[warn] style.rules is empty — your AI tools won't have any coding rules")

    if not config.targets.enabled:
        issues.append("[error] targets.enabled is empty — no output files will be generated")

    from airules.registry import list_targets

    available = list_targets()
    for target_id in config.targets.enabled:
        if target_id not in available:
            issues.append(f"[error] unknown target '{target_id}' in targets.enabled")

    for target_id in config.targets.overrides:
        if target_id not in available:
            issues.append(f"[warn] override for unknown target '{target_id}'")

    return issues
