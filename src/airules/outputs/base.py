"""Base renderer for output adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from airules.models import AiRulesConfig, TargetOverride


class BaseRenderer(ABC):
    """Base class for all output adapters."""

    target_id: str = ""
    default_output_path: str = ""
    description: str = ""
    max_chars: int = 0  # 0 = no limit

    def get_output_path(self, override: TargetOverride | None = None) -> str:
        """Get the output path, respecting overrides."""
        if override and override.output_path:
            return override.output_path
        return self.default_output_path

    def get_all_rules(self, config: AiRulesConfig) -> list[str]:
        """Combine base rules with target-specific extra rules."""
        rules = list(config.style.rules)
        override = config.targets.overrides.get(self.target_id)
        if override:
            rules.extend(override.extra_rules)
        return rules

    @abstractmethod
    def render(self, config: AiRulesConfig) -> str:
        """Render config into the target format string."""

    def write(self, config: AiRulesConfig, base_dir: Path) -> Path:
        """Render and write to file. Returns the output path."""
        override = config.targets.overrides.get(self.target_id)
        output_path = base_dir / self.get_output_path(override)
        content = self.render(config)

        if self.max_chars and len(content) > self.max_chars:
            content = content[: self.max_chars]

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        return output_path
