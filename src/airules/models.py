"""Typed config dataclasses for .airules.toml."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ProjectConfig:
    name: str = ""
    description: str = ""
    languages: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)


@dataclass
class StyleConfig:
    rules: list[str] = field(default_factory=list)


@dataclass
class CommandsConfig:
    build: str = ""
    test: str = ""
    lint: str = ""
    dev: str = ""

    def as_dict(self) -> dict[str, str]:
        return {k: v for k, v in self.__dict__.items() if v}


@dataclass
class ArchitectureConfig:
    notes: list[str] = field(default_factory=list)


@dataclass
class TargetOverride:
    extra_rules: list[str] = field(default_factory=list)
    output_path: str = ""


@dataclass
class TargetsConfig:
    enabled: list[str] = field(default_factory=lambda: ["claude-md", "cursorrules", "copilot"])
    overrides: dict[str, TargetOverride] = field(default_factory=dict)


@dataclass
class AiRulesConfig:
    project: ProjectConfig = field(default_factory=ProjectConfig)
    style: StyleConfig = field(default_factory=StyleConfig)
    commands: CommandsConfig = field(default_factory=CommandsConfig)
    architecture: ArchitectureConfig = field(default_factory=ArchitectureConfig)
    targets: TargetsConfig = field(default_factory=TargetsConfig)
