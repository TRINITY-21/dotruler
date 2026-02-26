"""Codebase scanner for auto-detecting project info."""

from __future__ import annotations

import json
from pathlib import Path

# File extension → language mapping
LANGUAGE_MAP: dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".jsx": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".java": "java",
    ".kt": "kotlin",
    ".swift": "swift",
    ".c": "c",
    ".cpp": "cpp",
    ".cs": "csharp",
    ".php": "php",
    ".dart": "dart",
    ".lua": "lua",
    ".zig": "zig",
    ".ex": "elixir",
    ".exs": "elixir",
}

# Config file → framework detection
FRAMEWORK_SIGNALS: dict[str, str] = {
    "next.config.js": "nextjs",
    "next.config.mjs": "nextjs",
    "next.config.ts": "nextjs",
    "nuxt.config.ts": "nuxt",
    "nuxt.config.js": "nuxt",
    "svelte.config.js": "svelte",
    "astro.config.mjs": "astro",
    "angular.json": "angular",
    "vue.config.js": "vue",
    "vite.config.ts": "vite",
    "vite.config.js": "vite",
    "remix.config.js": "remix",
    "gatsby-config.js": "gatsby",
    "manage.py": "django",
    "Cargo.toml": "rust",
    "go.mod": "go",
    "Gemfile": "rails",
    "pubspec.yaml": "flutter",
    "Package.swift": "swift",
    "build.gradle": "gradle",
    "pom.xml": "maven",
    "composer.json": "laravel",
    "tailwind.config.js": "tailwind",
    "tailwind.config.ts": "tailwind",
}

# Existing AI config files to detect
AI_CONFIG_FILES: dict[str, str] = {
    "CLAUDE.md": "claude-md",
    ".cursorrules": "cursorrules",
    ".github/copilot-instructions.md": "copilot",
    ".windsurfrules": "windsurf",
    "AGENTS.md": "codex",
    "CONVENTIONS.md": "aider",
}

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__",
    "build", "dist", ".next", ".nuxt", "target", ".tox",
    ".mypy_cache", ".pytest_cache", ".ruff_cache",
}


def scan_languages(project_dir: Path, max_depth: int = 3) -> list[str]:
    """Detect languages from file extensions."""
    found: set[str] = set()

    for path in _walk(project_dir, max_depth):
        lang = LANGUAGE_MAP.get(path.suffix.lower())
        if lang:
            found.add(lang)

    return sorted(found)


def scan_frameworks(project_dir: Path) -> list[str]:
    """Detect frameworks from config files."""
    found: set[str] = set()

    for filename, framework in FRAMEWORK_SIGNALS.items():
        if (project_dir / filename).exists():
            found.add(framework)

    # Check package.json for additional signals
    pkg_json = project_dir / "package.json"
    if pkg_json.exists():
        try:
            pkg = json.loads(pkg_json.read_text(encoding="utf-8"))
            all_deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "react" in all_deps:
                found.add("react")
            if "vue" in all_deps:
                found.add("vue")
            if "express" in all_deps:
                found.add("express")
            if "fastify" in all_deps:
                found.add("fastify")
        except (json.JSONDecodeError, OSError):
            pass

    # Check pyproject.toml for Python frameworks
    pyproject = project_dir / "pyproject.toml"
    if pyproject.exists():
        try:
            import tomllib

            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            deps = data.get("project", {}).get("dependencies", [])
            dep_str = " ".join(deps).lower()
            if "fastapi" in dep_str:
                found.add("fastapi")
            if "flask" in dep_str:
                found.add("flask")
            if "django" in dep_str:
                found.add("django")
        except (ValueError, OSError):
            pass

    return sorted(found)


def scan_commands(project_dir: Path) -> dict[str, str]:
    """Detect common commands from project config files."""
    commands: dict[str, str] = {}

    # Check package.json scripts
    pkg_json = project_dir / "package.json"
    if pkg_json.exists():
        try:
            pkg = json.loads(pkg_json.read_text(encoding="utf-8"))
            scripts = pkg.get("scripts", {})
            if "build" in scripts:
                commands["build"] = f"npm run build"
            if "test" in scripts:
                commands["test"] = f"npm test"
            if "lint" in scripts:
                commands["lint"] = f"npm run lint"
            if "dev" in scripts:
                commands["dev"] = f"npm run dev"
            elif "start" in scripts:
                commands["dev"] = f"npm start"
        except (json.JSONDecodeError, OSError):
            pass

    # Check for Makefile
    if (project_dir / "Makefile").exists():
        if "build" not in commands:
            commands["build"] = "make build"
        if "test" not in commands:
            commands["test"] = "make test"

    # Check for Python test tools
    if (project_dir / "pyproject.toml").exists() or (project_dir / "setup.py").exists():
        if "test" not in commands:
            commands["test"] = "pytest"
        if "lint" not in commands:
            commands["lint"] = "ruff check ."

    return commands


def scan_existing_ai_configs(project_dir: Path) -> dict[str, Path]:
    """Find existing AI config files."""
    found: dict[str, Path] = {}
    for rel_path, target_id in AI_CONFIG_FILES.items():
        full_path = project_dir / rel_path
        if full_path.exists():
            found[target_id] = full_path
    return found


def scan_project(project_dir: Path) -> dict:
    """Full project scan. Returns dict ready for TOML generation."""
    return {
        "languages": scan_languages(project_dir),
        "frameworks": scan_frameworks(project_dir),
        "commands": scan_commands(project_dir),
        "existing_ai_configs": scan_existing_ai_configs(project_dir),
    }


def _walk(directory: Path, max_depth: int, _depth: int = 0):
    """Walk directory tree with depth limit, skipping common build dirs."""
    if _depth > max_depth:
        return
    try:
        for item in directory.iterdir():
            if item.is_file():
                yield item
            elif item.is_dir() and item.name not in SKIP_DIRS:
                yield from _walk(item, max_depth, _depth + 1)
    except PermissionError:
        pass
