"""Canonical public architecture contract for the seed system."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

ARCHITECTURE_CONTRACT_SCHEMA = "docs/architecture.schema.json"
ARCHITECTURE_CONTRACT_VERSION = "1.0.0"

ARCHITECTURE_CONTRACT: dict[str, Any] = {
    "schema": ARCHITECTURE_CONTRACT_SCHEMA,
    "version": ARCHITECTURE_CONTRACT_VERSION,
    "layers": [
        {
            "name": "iteration",
            "purpose": "Versioned evolution, release boundaries, and compatibility policy.",
            "responsibilities": [
                "Version changes",
                "Release notes",
                "Compatibility boundaries",
                "Rollback guidance",
            ],
        },
        {
            "name": "resource",
            "purpose": "Workspace discovery and sanitized context extraction.",
            "responsibilities": [
                "Workspace discovery",
                "Checkpoint manifests",
                "Project knowledge summaries",
                "Sanitized config snapshots",
            ],
        },
        {
            "name": "maintenance",
            "purpose": "Diagnostics, validation, and repair planning.",
            "responsibilities": [
                "Read-only diagnostics",
                "Validation profiles",
                "Drift reporting",
                "Repair planning without mutation by default",
            ],
        },
        {
            "name": "tool",
            "purpose": "Explicit command surfaces and read-only wrappers.",
            "responsibilities": [
                "Minimal command surfaces",
                "MCP-style wrappers",
                "Explicit input/output schemas",
                "Read-only defaults",
            ],
        },
    ],
    "shared_rules": [
        "Prefer public, reusable abstractions over private local paths.",
        "Treat live environment facts as runtime evidence, not static memory.",
        "Sanitize secrets and sensitive values before export.",
        "Missing artifacts should be reported, not hidden.",
        "Keep diagnostics and repair separate from business payloads.",
    ],
    "maintenance_contract": {
        "snapshot": {
            "mode": "read-only",
            "purpose": "Capture current state without mutating workspace or services.",
            "outputs": ["state summary", "drift summary", "risk summary"],
        },
        "doctor": {
            "mode": "read-only",
            "purpose": "Classify blockers, risks, advisories, and unknowns.",
            "outputs": ["blockers", "risks", "advisories", "unknowns"],
        },
        "repair_plan": {
            "mode": "dry-run by default",
            "purpose": "Describe a repair without applying it.",
            "outputs": ["steps", "blast radius", "verification plan", "rollback notes"],
        },
        "validate": {
            "mode": "tiered",
            "purpose": "Run quick or full validation against a known contract.",
            "outputs": ["pass/fail", "mismatches", "evidence"],
        },
        "metrics": {
            "mode": "read-only",
            "purpose": "Expose machine-readable health and usage counters.",
            "outputs": ["status counts", "latency", "failure rates", "throughput hints"],
        },
    },
    "capability_index": {
        "purpose": "A machine-readable index of the public seed system capabilities.",
        "sections": [
            {
                "name": "bootstrap",
                "layer": "resource + tool",
                "entrypoints": [
                    "seed_system.core.bootstrap_context:build_payload",
                    "seed_system.core.bootstrap_context:render_markdown",
                    "seed_system.core.project_kb_mcp:bootstrap_context_pack",
                ],
            },
            {
                "name": "architecture",
                "layer": "iteration",
                "entrypoints": [
                    "seed_system.core.architecture_contract:get_architecture_contract",
                ],
            },
            {
                "name": "maintenance",
                "layer": "maintenance",
                "entrypoints": [
                    "seed_system.core.project_kb_mcp:maintenance_contract",
                ],
            },
            {
                "name": "knowledge",
                "layer": "resource",
                "entrypoints": [
                    "seed_system.core.project_kb_mcp:kb_stats",
                    "seed_system.core.project_kb_mcp:kb_search",
                ],
            },
            {
                "name": "agent_capabilities",
                "layer": "iteration + resource + maintenance + tool",
                "entrypoints": [
                    "versioned evolution",
                    "sanitized workspace ingestion",
                    "read-only maintenance contracts",
                    "machine-readable capability discovery",
                    "MCP-style tool discovery",
                    "release drafting",
                ],
            },
        ],
    },
    "growth_model": {
        "purpose": "A reusable learning loop for helping a generic agent grow from this seed.",
        "entrypoints": ["observe", "orient", "act", "verify", "retain"],
        "capabilities": [
            "task decomposition",
            "tool discipline",
            "verification",
            "knowledge retention",
            "release hygiene",
        ],
    },
    "agent_primitives": {
        "purpose": "The most reusable generic primitives the seed teaches to a new agent.",
        "groups": [
            {
                "name": "discovery",
                "items": [
                    "read local instructions first",
                    "inspect the contract before acting",
                    "find the narrowest useful tool",
                    "distinguish stable docs from live evidence",
                ],
            },
            {
                "name": "execution",
                "items": [
                    "make the smallest effective change",
                    "keep outputs structured",
                    "default to read-only",
                    "prefer reversible operations and backups",
                ],
            },
            {
                "name": "verification",
                "items": [
                    "run a compile or schema check when available",
                    "compare example payloads with real outputs",
                    "treat drift-prone facts as live-only",
                    "separate verification from repair planning",
                ],
            },
            {
                "name": "retention",
                "items": [
                    "promote reusable insights into the contract",
                    "keep examples aligned with canonical shapes",
                    "record versioned changes in release notes",
                    "avoid burying knowledge in ephemeral chat state",
                ],
            },
        ],
    },
    "tool_knowledge": {
        "purpose": "Reusable public tool habits and knowledge patterns.",
        "entrypoints": [
            "code_navigation",
            "safe_editing",
            "verification",
            "source_verification",
            "tool_discovery",
            "browser_and_gui",
            "git_and_release",
            "memory_and_skills",
        ],
        "knowledge_types": [
            "stable_contract",
            "live_state",
            "private_runtime",
            "reusable_lesson",
        ],
    },
    "canonical_public_artifacts": [
        "VERSION.md",
        "CHANGELOG.md",
        "releases/<version>.md",
        "docs/design.md",
        "docs/origin.md",
        "docs/architecture.md",
        "docs/architecture.schema.json",
        "seed_system/core/architecture_contract.py",
        "seed_system/core/growth_model.py",
        "seed_system/core/tool_knowledge.py",
        "seed_system/core/bootstrap_context.py",
        "seed_system/core/project_kb_mcp.py",
        "skills/README.md",
        "skills/template/SKILL.md",
        "skills/bootstrap/SKILL.md",
        "skills/release-notes/SKILL.md",
    ],
}


def get_architecture_contract() -> dict[str, Any]:
    return deepcopy(ARCHITECTURE_CONTRACT)
