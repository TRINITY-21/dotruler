# airules

**One config. Every AI coding tool. Always in sync.**

Stop maintaining 5 separate config files for Claude Code, Cursor, Copilot, Windsurf, Codex, and Aider. Write your rules once in `.airules.toml`, generate all configs instantly.

```
pip install airules
```

## The Problem

You use multiple AI coding tools. Each one wants its own config file:

| Tool | Config File |
|------|------------|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurfrules` |
| OpenAI Codex | `AGENTS.md` |
| Aider | `CONVENTIONS.md` |

They drift out of sync within a week. You update one, forget the others. Your AI tools give inconsistent results.

## The Fix

```bash
# Scan your project, generate a starter config
airules init

# Edit your single source of truth
vim .airules.toml

# Generate all configs at once
airules generate
```

That's it. One file, all tools, always in sync.

## Quick Start

### 1. Install

```bash
pip install airules
```

### 2. Initialize

```bash
cd your-project
airules init
```

This scans your project — detects languages, frameworks, and existing commands — and creates `.airules.toml`.

### 3. Edit your config

```toml
[project]
name = "myapp"
description = "Next.js web app with PostgreSQL"
languages = ["typescript", "python"]
frameworks = ["nextjs", "fastapi"]

[style]
rules = [
  "Use functional components with hooks",
  "Prefer const over let",
  "Use TypeScript strict mode",
]

[commands]
build = "npm run build"
test = "pytest && npm test"
lint = "ruff check . && npm run lint"
dev = "npm run dev"

[architecture]
notes = [
  "API routes in src/app/api/",
  "Database models in src/models/",
]

[targets]
enabled = ["claude-md", "cursorrules", "copilot"]
```

### 4. Generate

```bash
airules generate
```

```
Generating from .airules.toml...

  ✓ CLAUDE.md
  ✓ .cursorrules
  ✓ .github/copilot-instructions.md

Done. 3 configs generated.
```

## Commands

| Command | What it does |
|---------|-------------|
| `airules init` | Scan project, create starter `.airules.toml` |
| `airules generate` | Generate all enabled config files |
| `airules validate` | Check config for errors and warnings |
| `airules diff` | Preview changes before writing |
| `airules list` | Show all available output targets |
| `airules generate --dry-run` | See what would be generated without writing |

## Supported Targets

| Target | Output File | Char Limit |
|--------|------------|------------|
| `claude-md` | `CLAUDE.md` | none |
| `cursorrules` | `.cursorrules` | none |
| `copilot` | `.github/copilot-instructions.md` | none |
| `windsurf` | `.windsurfrules` | 12,000 |
| `codex` | `AGENTS.md` | 32,768 |
| `aider` | `CONVENTIONS.md` | none |

Windsurf and Codex have character limits — airules automatically enforces them.

## Per-Target Overrides

Need extra rules for a specific tool? Add target overrides:

```toml
[targets]
enabled = ["claude-md", "cursorrules", "copilot"]

[targets.claude-md]
extra_rules = ["Use Read tool before editing files"]
output_path = "CLAUDE.md"  # custom location

[targets.cursorrules]
extra_rules = ["Prefer .cursor/rules/*.mdc format"]
```

## Plugin System

All output targets are plugins. Built-in ones cover the 6 major tools, but the registry pattern means anyone can add more.

## Why Not X?

| Tool | Issue |
|------|-------|
| Manual copy-paste | Drifts within a week |
| Symlinks | Formats differ — Claude wants markdown headers, Cursor wants plain text |
| ruler (2.5K stars) | Limited customization per tool |
| rulesync (829 stars) | Node.js dependency |
| ai-rulez (91 stars) | Go, 18 targets but low adoption |

airules is Python-native, TOML-based, plugin-extensible, and validates your config.

## License

MIT
