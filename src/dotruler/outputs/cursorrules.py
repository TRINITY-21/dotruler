"""Cursor .cursorrules renderer."""

from __future__ import annotations

from dotruler.models import AiRulesConfig
from dotruler.outputs.base import BaseRenderer
from dotruler.registry import register


@register("cursorrules")
class CursorRulesRenderer(BaseRenderer):
    target_id = "cursorrules"
    default_output_path = ".cursorrules"
    description = "Cursor AI project rules"

    def render(self, config: AiRulesConfig) -> str:
        sections: list[str] = []

        # Project context
        if config.project.name or config.project.description:
            ctx = f"You are working on {config.project.name}."
            if config.project.description:
                ctx += f" {config.project.description}."
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
