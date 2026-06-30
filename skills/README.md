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

## Public policy

This repository only publishes framework-level guidance and templates. It does not publish private skill payloads, local workspace secrets, or runtime-only instructions.
