# Seed System

A public, sanitized seed system for reusable Codex/agent bootstrap context packs.

## Layout

```text
.
├── README.md
├── VERSION.md
├── LICENSE
├── seed_system/
│   ├── __init__.py
│   └── core/
│       ├── bootstrap_context.py
│       └── project_kb_mcp.py
├── docs/
│   ├── design.md
│   └── origin.md
└── examples/
    └── bootstrap-pack.example.json
```

## What it does

- Generates read-only bootstrap packs.
- Summarizes rules, checkpoints, and sanitized config.
- Exposes a tiny MCP-style wrapper for `bootstrap_context_pack`.

## Versioning

This repository follows Semantic Versioning. See [VERSION.md](VERSION.md).

## Release notes

GitHub Releases should be used for published versions. Keep release notes concise and user-facing.

## Quick start

```bash
python -m seed_system.core.bootstrap_context --workspace . --project-id my-project --depth quick --format markdown
python -m seed_system.core.bootstrap_context --workspace . --project-id my-project --depth normal --format json
```
