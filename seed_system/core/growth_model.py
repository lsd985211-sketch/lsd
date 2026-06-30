"""Canonical public growth model for agent capability accumulation."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

GROWTH_MODEL_VERSION = "1.0.0"

GROWTH_MODEL: dict[str, Any] = {
    "version": GROWTH_MODEL_VERSION,
    "goal": "Help a generic agent absorb reusable capability, knowledge, and tool discipline quickly.",
    "phases": [
        {
            "name": "observe",
            "purpose": "Start from live evidence and local instructions before acting.",
            "inputs": ["workspace rules", "architecture contract", "capability index", "maintenance contract"],
            "outputs": ["current-state summary", "risk map", "available capabilities"],
        },
        {
            "name": "orient",
            "purpose": "Map the task onto reusable patterns before generating output.",
            "inputs": ["problem statement", "tool inventory", "knowledge summaries"],
            "outputs": ["task shape", "layer selection", "planned path"],
        },
        {
            "name": "act",
            "purpose": "Use the smallest useful tool or knowledge surface and keep outputs structured.",
            "inputs": ["selected capability", "constraints", "verification target"],
            "outputs": ["draft", "patch", "query", "report", "plan"],
        },
        {
            "name": "verify",
            "purpose": "Check machine-readable evidence before treating work as complete.",
            "inputs": ["tests", "schema checks", "tool responses", "live evidence"],
            "outputs": ["pass/fail", "mismatches", "next repair step"],
        },
        {
            "name": "retain",
            "purpose": "Capture reusable lessons without polluting the contract with private runtime noise.",
            "inputs": ["outcome", "new pattern", "failure mode", "verified insight"],
            "outputs": ["updated notes", "skill delta", "release note candidate"],
        },
    ],
    "tool_principles": [
        "Prefer read-only discovery before mutation.",
        "Use the minimal tool surface needed for the task.",
        "Keep tool outputs structured and machine-readable when possible.",
        "Treat fallback paths as recovery, not primary design.",
    ],
    "knowledge_principles": [
        "Distinguish stable contract knowledge from live environment facts.",
        "Use live verification for drift-prone claims.",
        "Record reusable findings in the public contract, not hidden chat state.",
        "Keep examples aligned with the canonical payload shape.",
    ],
    "growth_targets": [
        "Faster task decomposition",
        "Safer tool use",
        "Stronger verification habits",
        "Cleaner capability reuse",
        "Better release discipline",
    ],
}


def get_growth_model() -> dict[str, Any]:
    return deepcopy(GROWTH_MODEL)

