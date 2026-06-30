"""Public seed system utilities."""

__all__ = [
    "build_payload",
    "render_markdown",
    "get_architecture_contract",
    "get_growth_model",
    "get_tool_knowledge",
    "contract_validate",
    "agent_capabilities",
    "agent_primitives",
    "bootstrap_context_pack",
    "capability_index",
    "growth_model",
    "kb_search",
    "kb_stats",
    "maintenance_contract",
    "public_api",
    "tool_catalog",
    "tool_knowledge",
]


def __getattr__(name):
    if name in {"build_payload", "render_markdown"}:
        from .core import bootstrap_context

        return getattr(bootstrap_context, name)
    if name == "get_architecture_contract":
        from .core.architecture_contract import get_architecture_contract

        return get_architecture_contract
    if name == "get_growth_model":
        from .core.growth_model import get_growth_model

        return get_growth_model
    if name == "get_tool_knowledge":
        from .core.tool_knowledge import get_tool_knowledge

        return get_tool_knowledge
    if name in {
        "agent_capabilities",
        "agent_primitives",
        "bootstrap_context_pack",
        "capability_index",
        "contract_validate",
        "growth_model",
        "kb_search",
        "kb_stats",
        "maintenance_contract",
        "public_api",
        "tool_catalog",
        "tool_knowledge",
    }:
        from .core import project_kb_mcp

        return getattr(project_kb_mcp, name)
    raise AttributeError(name)
