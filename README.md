# Seed System

A public, sanitized seed system for reusable Codex/agent bootstrap context packs.

This repository is based on a local `new_agent_bootstrap` system. The original private system generates a read-only startup pack for fresh agent sessions so they can inherit project rules, checkpoint baselines, tool status, and live audit warnings without loading full history.

## Components

- `seed_system/bootstrap_context.py` - read-only context-pack generator.
- `seed_system/project_kb_mcp.py` - minimal MCP-style wrapper exposing `bootstrap_context_pack` plus knowledge-base helpers.
- `docs/origin.md` - what the private source system was and what was sanitized.
- `docs/design.md` - design contract and safety rules.
- `examples/bootstrap-pack.example.json` - public example payload.

## Safety Model

- Read-only by default.
- Missing files are reported, not treated as fatal.
- Drift-prone facts are marked for live verification.
- Config output is summarized and sanitized.
- Generated packs should be reviewed before publication.

## Quick Start

```bash
python -m seed_system.bootstrap_context --workspace . --project-id my-project --depth quick --format markdown
python -m seed_system.bootstrap_context --workspace . --project-id my-project --depth normal --format json
```

## MCP Wrapper Smoke Test

```bash
printf '{"jsonrpc":"2.0","id":1,"method":"tools/list"}\n' | python seed_system/project_kb_mcp.py
```
