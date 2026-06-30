# Design Notes

## Goal

The seed system gives a new agent session a compact, read-only bootstrap pack for a workspace. It is useful for handoff, restart, context inheritance, and maintenance workflows.

## Non-goals

- It does not replace project-specific memory.
- It does not repair system state.
- It does not upload generated packs.
- It does not assume a private directory layout.

## Core Contract

1. Default behavior is read-only.
2. Missing files are reported, not treated as fatal.
3. Drift-prone facts must be verified live by the consumer.
4. Config values are sanitized before output.
5. Optional command checks only run in a deliberately expanded diagnostic mode.
6. Public layering is explicit: iteration, resource, maintenance, and tool.
7. Maintenance and repair planning stay separate from payload generation.

## Suggested Workspace Layout

```text
.
├── README.md
├── VERSION.md
├── seed_system/
│   └── core/
├── docs/
└── examples/
```
