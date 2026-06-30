# Bootstrap Skill

## Purpose

Provide a reusable bootstrap context pack for new agent sessions.

## Trigger

Use when a fresh session needs workspace rules, checkpoint baselines, and sanitized config.

## Output

- Bootstrap pack in markdown or JSON
- Optional MCP-style wrapper

## Safety

- Read-only by default.
- Sanitize config and secrets.
- Report missing files instead of failing hard.
