# dotruler

> One config. Every AI coding tool. Always in sync.

Generate `CLAUDE.md`, `.cursorrules`, `copilot-instructions.md`, and other AI tool configs from a **single source of truth** — so your project's AI guidance stays consistent no matter which tool your team is using today.

## The problem

If you've used more than one AI coding tool, you've hit this:

- Claude Code reads `CLAUDE.md`
- Cursor reads `.cursorrules`
- GitHub Copilot reads `copilot-instructions.md`
- Cline, Aider, Continue — each with their own format

Same project guidance, four-plus copies, all slowly drifting out of sync.

## The fix

Write your project's AI guidance once in `dotruler.yaml`. Run `dotruler sync`. Every supported AI tool now sees the same instructions.

## Install

```sh
pip install dotruler
```

## Quick start

```sh
# In your project root
dotruler init

# Edit dotruler.yaml with your project's guidance

# Generate all configs
dotruler sync
```

## Supported tools

- Claude Code (`CLAUDE.md`)
- Cursor (`.cursorrules`)
- GitHub Copilot (`copilot-instructions.md`)
- Cline
- ...more on the way — open an issue for the tool you use.

## Why

I switched between Claude Code and Cursor on the same project enough times to get tired of paste-into-three-files-after-every-update. `dotruler` is the tool I wished existed.

## Tech

Python · Textual · Rich · packaged on PyPI

## License

MIT

---

Built by [Joseph Yaw Agyeman](https://jagyeman.dev) · [@TRINITY-21](https://github.com/TRINITY-21)
