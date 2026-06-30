# Public Architecture Contract

This repository exposes a public, sanitized contract for reusable agent bootstrap systems.

## Schema

- machine-readable schema: `docs/architecture.schema.json`
- schema version: `1.0.0`

## Maintenance Contract

The maintenance layer is machine-readable and stays read-only by default.

- `snapshot`: read-only state capture
- `doctor`: read-only diagnosis classification
- `repair_plan`: dry-run repair planning
- `validate`: tiered validation
- `metrics`: read-only health counters

### Operating Rule

- `snapshot` and `doctor` must remain read-only.
- `repair_plan` defaults to dry-run.
- `validate` should support quick and full profiles.
- `metrics` should remain low overhead and machine-readable.

## Capability Index

The tool layer exposes a public capability index so a generic agent can discover what this seed system can do.

- `bootstrap`: payload generation and MCP bootstrap wrapper
- `architecture`: canonical contract access
- `maintenance`: diagnostics and validation contract access
- `knowledge`: markdown search and stats
- `agent_capabilities`: top-level capability inventory for general agent use

## Seed Goal

This repository is meant to help a generic agent absorb reusable capabilities and keep evolving from the public contract, not just read static framework docs.

## Growth Model

The seed should teach a generic agent how to grow:

- observe: start from live evidence
- orient: map the task to reusable patterns
- act: use the smallest useful tool or knowledge surface
- verify: check machine-readable evidence
- retain: capture reusable lessons without private noise

## Agent Primitives

The seed should also teach a small set of reusable primitives:

- discovery: read instructions, inspect contracts, find the narrowest useful tool
- execution: make the smallest effective change, keep outputs structured, prefer reversibility
- verification: compile or schema check, compare examples with real outputs, separate verification from repair
- retention: promote reusable insights into the contract, keep examples aligned, version lessons

## Tool Knowledge

Reusable tool knowledge is public and generic:

- code navigation
- safe editing
- verification
- source verification
- tool discovery
- browser and GUI checks
- Git and release discipline
- memory and skill retention

## Public API And Guardrails

The seed exposes public API, guardrails, tool catalog, and contract validation surfaces so downstream agents can rely on stable behavior instead of chat-only context.

## Layers

### 1. Iteration Layer

Responsible for:

- versioned evolution
- release notes
- compatibility boundaries
- safe rollout and rollback guidance

### 2. Resource Layer

Responsible for:

- workspace discovery
- checkpoint manifests
- project knowledge summaries
- sanitized config snapshots

### 3. Maintenance Layer

Responsible for:

- read-only diagnostics
- validation profiles
- drift reporting
- repair planning without mutation by default

### 4. Tool Layer

Responsible for:

- minimal command surfaces
- MCP-style wrappers
- explicit input/output schemas
- read-only defaults

## Shared Rules

- Prefer public, reusable abstractions over private local paths.
- Treat live environment facts as runtime evidence, not as static memory.
- Sanitize secrets and sensitive values before export.
- Missing artifacts should be reported, not hidden.
- Keep diagnostics and repair separate from business payloads.

## Canonical Public Artifacts

- `VERSION.md`
- `CHANGELOG.md`
- `releases/<version>.md`
- `docs/architecture.schema.json`
- `docs/design.md`
- `docs/origin.md`
- `seed_system/core/architecture_contract.py`
- `seed_system/core/bootstrap_context.py`
- `seed_system/core/project_kb_mcp.py`
- `skills/README.md`
- `skills/template/SKILL.md`
- `skills/bootstrap/SKILL.md`
- `skills/release-notes/SKILL.md`
