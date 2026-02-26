<p align="center">
  <h1 align="center">📐 dotruler</h1>
  <p align="center">
    <strong>One config. Every AI coding tool. Always in sync.</strong>
  </p>
  <p align="center">
    <a href="https://pypi.org/project/dotruler/"><img src="https://img.shields.io/pypi/v/dotruler?color=blue" alt="PyPI"></a>
    <a href="https://pypi.org/project/dotruler/"><img src="https://img.shields.io/pypi/pyversions/dotruler" alt="Python"></a>
    <a href="https://github.com/TRINITY-21/dotruler/blob/main/LICENSE"><img src="https://img.shields.io/github/license/TRINITY-21/dotruler" alt="License"></a>
  </p>
</p>

---

Stop maintaining 6 separate config files. Define your project rules once in `.dotruler.toml` and generate configs for **Claude Code**, **Cursor**, **GitHub Copilot**, **Windsurf**, **OpenAI Codex**, and **Aider** — instantly.

```bash
pip install dotruler
```

## Overview

Modern development workflows involve multiple AI coding assistants, each requiring its own instruction file:

| AI Tool | Config File |
|---------|------------|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurfrules` |
| OpenAI Codex | `AGENTS.md` |
| Aider | `CONVENTIONS.md` |

These files inevitably drift out of sync — you update one, forget the rest, and your AI tools produce inconsistent results. **dotruler** solves this with a single source of truth.

## How It Works

```bash
dotruler init          # Scan your project, scaffold .dotruler.toml
vim .dotruler.toml     # Edit your single config
dotruler generate      # Generate all target configs at once
```

## Getting Started

### Installation

```bash
pip install dotruler
```

Requires Python 3.11+.

### Initialize

```bash
cd your-project
dotruler init
```

Automatically detects your languages, frameworks, package manager, and existing commands to scaffold a starter `.dotruler.toml`.

### Configure

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

### Generate

```bash
dotruler generate
```

```
Generating from .dotruler.toml...

  ✓ CLAUDE.md
  ✓ .cursorrules
  ✓ .github/copilot-instructions.md

Done. 3 configs generated.
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `dotruler init` | Scan project and create starter `.dotruler.toml` |
| `dotruler generate` | Generate config files for all enabled targets |
| `dotruler generate --dry-run` | Preview output without writing files |
| `dotruler validate` | Check config for errors and warnings |
| `dotruler diff` | Show what would change before writing |
| `dotruler list` | Display all available output targets |

## Supported Targets

| Target | Output File | Char Limit |
|--------|------------|------------|
| `claude-md` | `CLAUDE.md` | — |
| `cursorrules` | `.cursorrules` | — |
| `copilot` | `.github/copilot-instructions.md` | — |
| `windsurf` | `.windsurfrules` | 12,000 |
| `codex` | `AGENTS.md` | 32,768 |
| `aider` | `CONVENTIONS.md` | — |

Character limits for Windsurf and Codex are automatically enforced during generation.

## Per-Target Overrides

Append tool-specific rules or customize output paths per target:

```toml
[targets]
enabled = ["claude-md", "cursorrules", "copilot"]

[targets.claude-md]
extra_rules = ["Use Read tool before editing files"]
output_path = "CLAUDE.md"

[targets.cursorrules]
extra_rules = ["Prefer .cursor/rules/*.mdc format"]
```

## Plugin Architecture

All output targets are implemented as plugins using a registry pattern. The 6 built-in targets cover the major AI coding tools, but the system is designed for extensibility — adding a new target requires a single file with a decorated class.

## Comparison

| Approach | Limitation |
|----------|-----------|
| Manual copy-paste | Drifts within days |
| Symlinks | Formats differ across tools |
| [ruler](https://github.com/intellectronica/ruler) | Limited per-tool customization |
| [rulesync](https://github.com/dyoshikawa/rulesync) | Requires Node.js |
| [ai-rulez](https://github.com/Goldziher/ai-rulez) | Requires Go |

**dotruler** is Python-native, TOML-configured, plugin-extensible, and validates your config before generating.

## License

[MIT](LICENSE)
