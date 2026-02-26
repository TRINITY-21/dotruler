"""Shared fixtures for airules tests."""

import pytest

from airules.models import (
    AiRulesConfig,
    ArchitectureConfig,
    CommandsConfig,
    ProjectConfig,
    StyleConfig,
    TargetOverride,
    TargetsConfig,
)


@pytest.fixture
def sample_config() -> AiRulesConfig:
    return AiRulesConfig(
        project=ProjectConfig(
            name="myapp",
            description="A test application",
            languages=["typescript", "python"],
            frameworks=["nextjs", "fastapi"],
        ),
        style=StyleConfig(
            rules=["Use functional components", "Prefer const over let"],
        ),
        commands=CommandsConfig(
            build="npm run build",
            test="pytest && npm test",
            lint="ruff check .",
            dev="npm run dev",
        ),
        architecture=ArchitectureConfig(
            notes=["API routes in src/app/api/", "Models in src/models/"],
        ),
        targets=TargetsConfig(
            enabled=["claude-md", "cursorrules", "copilot"],
            overrides={
                "claude-md": TargetOverride(extra_rules=["Use Read tool first"]),
            },
        ),
    )


@pytest.fixture
def minimal_config() -> AiRulesConfig:
    return AiRulesConfig(
        project=ProjectConfig(name="minimal"),
        style=StyleConfig(rules=["One rule"]),
        targets=TargetsConfig(enabled=["claude-md"]),
    )


@pytest.fixture
def sample_toml() -> str:
    return """\
[project]
name = "myapp"
description = "A test application"
languages = ["typescript", "python"]
frameworks = ["nextjs", "fastapi"]

[style]
rules = [
  "Use functional components",
  "Prefer const over let",
]

[commands]
build = "npm run build"
test = "pytest && npm test"
lint = "ruff check ."
dev = "npm run dev"

[architecture]
notes = [
  "API routes in src/app/api/",
  "Models in src/models/",
]

[targets]
enabled = ["claude-md", "cursorrules", "copilot"]

[targets.claude-md]
extra_rules = ["Use Read tool first"]
"""
