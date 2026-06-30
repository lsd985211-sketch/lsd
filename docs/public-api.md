# Public API

The public API is the stable surface a generic agent may rely on.

## Stable Surfaces

- `seed_system.core.bootstrap_context`
- `seed_system.core.architecture_contract`
- `seed_system.core.growth_model`
- `seed_system.core.tool_knowledge`
- `seed_system.core.project_kb_mcp`
- `docs/architecture.schema.json`
- `docs/contracts/*.schema.json`
- `examples/bootstrap-pack.example.json`

## MCP Tools

- `kb_stats`
- `kb_search`
- `architecture_contract`
- `maintenance_contract`
- `capability_index`
- `agent_capabilities`
- `growth_model`
- `agent_primitives`
- `tool_knowledge`
- `tool_catalog`
- `guardrails_contract`
- `public_api`
- `contract_validate`
- `bootstrap_context_pack`

## Compatibility

- Backward-compatible additions bump `MINOR`.
- Breaking schema or tool signature changes bump `MAJOR`.
- Documentation-only fixes bump `PATCH`.

## Safety Boundary

- Public artifacts must not include private paths, credentials, tokens, runtime logs, local account data, or user-specific configuration.
- Tool surfaces default to read-only unless explicitly documented otherwise.

