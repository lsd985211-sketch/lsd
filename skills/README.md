# Skills Framework

This repository documents the public skill framework that the private seed system was designed to bootstrap into new sessions.

## Goal

- Keep reusable agent capabilities discoverable.
- Separate capability descriptions from session history.
- Make skills easy to audit, version, and hand off.

## Recommended layout

```text
skills/
├── README.md
├── template/
│   └── SKILL.md
├── bootstrap/
│   └── SKILL.md
└── release-notes/
    └── SKILL.md
```

## Skill contract

Each skill should include:

- purpose
- trigger conditions
- inputs and outputs
- safety boundaries
- version or compatibility notes
- examples when useful

## Shared public architecture

All public skills in this repository should align with the same four layers:

- iteration
- resource
- maintenance
- tool

Use the shared architecture contract in `docs/architecture.md` as the source of truth.

## Public policy

This repository only publishes framework-level guidance and templates. It does not publish private skill payloads, local workspace secrets, or runtime-only instructions.
