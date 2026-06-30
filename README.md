# Seed System

A public, sanitized seed system for reusable Codex/agent bootstrap context packs.

## Layout

```text
.
├── README.md
├── VERSION.md
├── CHANGELOG.md
├── releases/
├── LICENSE
├── seed_system/
│   └── core/
├── docs/
└── examples/
```

## What it does

- Generates read-only bootstrap packs.
- Summarizes rules, checkpoints, and sanitized config.
- Exposes a tiny MCP-style wrapper for `bootstrap_context_pack`.

## Versioning

This repository follows Semantic Versioning. See [VERSION.md](VERSION.md) and [CHANGELOG.md](CHANGELOG.md).

## Release notes

GitHub Releases should be used for published versions. Keep release notes concise and user-facing.

## Release structure

Use `releases/<version>.md` for the human-readable release draft before publishing.

## Quick start

```bash
python -m seed_system.core.bootstrap_context --workspace . --project-id my-project --depth quick --format markdown
python -m seed_system.core.bootstrap_context --workspace . --project-id my-project --depth normal --format json
```
