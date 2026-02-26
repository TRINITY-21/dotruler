"""Auto-import all output adapters to trigger registration."""

from airules.outputs import aider, claude_md, codex, copilot, cursorrules, windsurf

__all__ = ["aider", "claude_md", "codex", "copilot", "cursorrules", "windsurf"]
