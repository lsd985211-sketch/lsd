"""Public guardrails for generic agent use of the seed system."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

GUARDRAILS_VERSION = "1.0.0"

GUARDRAILS: dict[str, Any] = {
    "version": GUARDRAILS_VERSION,
    "rules": [
        {"name": "read_only_first", "purpose": "Inspect before mutation.", "action": "Use read-only tools before edits or execution."},
        {"name": "sanitize_public_outputs", "purpose": "Keep public artifacts safe.", "action": "Remove private paths, tokens, logs, and account data."},
        {"name": "verify_drift_prone_facts", "purpose": "Avoid stale facts.", "action": "Re-check tool availability, ports, services, versions, and permissions."},
        {"name": "separate_repair_from_diagnosis", "purpose": "Reduce unsafe automation.", "action": "Keep doctor/snapshot read-only and repair-plan dry-run by default."},
        {"name": "version_public_contracts", "purpose": "Protect downstream users.", "action": "Bump SemVer when schemas or tool surfaces change."},
    ],
}


def get_guardrails() -> dict[str, Any]:
    return deepcopy(GUARDRAILS)

