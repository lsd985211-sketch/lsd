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
- Organizes the public contract into iteration, resource, maintenance, and tool layers.

## Architecture

See [docs/architecture.md](docs/architecture.md) for the canonical public contract.
The machine-readable source lives in [docs/architecture.schema.json](docs/architecture.schema.json).
The contract code lives in [seed_system/core/architecture_contract.py](seed_system/core/architecture_contract.py).
Maintenance details are surfaced through the same contract and the `maintenance_contract` MCP tool.
Capability discovery is surfaced through the `capability_index` contract and MCP tool.
The seed is intended to help a generic agent absorb reusable capabilities and keep evolving from this contract.
Growth guidance is surfaced through the `growth_model` contract and MCP tool.
Reusable agent primitives are surfaced through the `agent_primitives` contract and MCP tool.
Reusable tool and knowledge patterns are surfaced through the `tool_knowledge` contract and MCP tool.
Public API, guardrails, tool catalog, and validation helpers are documented in [docs/public-api.md](docs/public-api.md).

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
