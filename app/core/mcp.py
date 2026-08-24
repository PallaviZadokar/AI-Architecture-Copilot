from agent_framework import MCPStreamableHTTPTool

from app.core.config import settings


def get_mcp_tool() -> MCPStreamableHTTPTool:
    return MCPStreamableHTTPTool(
        name="architecture_catalog",
        url=settings.MCP_SERVER_URL,
        description=(
            "Architecture technology catalog and architecture "
            "pattern knowledge service."
        ),
        approval_mode="never_require",
    )
