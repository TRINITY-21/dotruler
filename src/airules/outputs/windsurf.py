"""Windsurf .windsurfrules renderer."""

from __future__ import annotations

from airules.models import AiRulesConfig
from airules.outputs.base import BaseRenderer
from airules.registry import register

WINDSURF_CHAR_LIMIT = 12_000


@register("windsurf")
class WindsurfRenderer(BaseRenderer):
    target_id = "windsurf"
    default_output_path = ".windsurfrules"
    description = "Windsurf Cascade project rules"
    max_chars = WINDSURF_CHAR_LIMIT

    def render(self, config: AiRulesConfig) -> str:
        sections: list[str] = []

        # Project context
        if config.project.name or config.project.description:
            ctx = f"Project: {config.project.name}"
            if config.project.description:
                ctx += f" — {config.project.description}"
            sections.append(ctx)

        # Tech stack
        stack_parts: list[str] = []
        if config.project.languages:
            stack_parts.append(f"Languages: {', '.join(config.project.languages)}")
        if config.project.frameworks:
            stack_parts.append(f"Frameworks: {', '.join(config.project.frameworks)}")
        if stack_parts:
            sections.append("Tech Stack:\n" + "\n".join(f"- {p}" for p in stack_parts))

        # Rules
        rules = self.get_all_rules(config)
        if rules:
            rule_lines = "\n".join(f"- {r}" for r in rules)
            sections.append(f"Code Style:\n{rule_lines}")

        # Commands
        commands = config.commands.as_dict()
        if commands:
            cmd_lines = "\n".join(f"- {name}: `{cmd}`" for name, cmd in commands.items())
            sections.append(f"Commands:\n{cmd_lines}")

        # Architecture
        if config.architecture.notes:
            note_lines = "\n".join(f"- {n}" for n in config.architecture.notes)
            sections.append(f"Architecture:\n{note_lines}")

        return "\n\n".join(sections) + "\n"
