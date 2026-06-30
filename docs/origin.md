# Origin

This public repository is derived from a private local seed system built around these concepts:

- `new_agent_bootstrap.py`: a read-only generator for new-agent context packs.
- `bootstrap_context_pack`: an MCP tool wrapper registered inside a project knowledge-base MCP server.
- `shared/bootstrap/latest.md` and `latest.json`: generated handoff packs.
- memory-system checkpoints that recorded the evolution from v1 to v1.1 and MCP registration.

The private system was designed so fresh Codex/agent sessions could inherit project rules, checkpoint baselines, MCP status, and live audit warnings without loading full history.

The public repository keeps the same general shape, but abstracts the private implementation into a reusable public contract across iteration, resource, maintenance, and tool layers.

## Sanitization

The public version removes or generalizes absolute private paths, private MCP server names, tokens, local checkpoint contents, logs, runtime files, personal configuration, and project-specific repair logic.
