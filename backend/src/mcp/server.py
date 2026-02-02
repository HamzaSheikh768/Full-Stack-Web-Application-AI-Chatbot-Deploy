from mcp.server import MCPServer
from .tools import all_tools

# Create MCP Server instance with all task management tools
mcp_server = MCPServer(
    tools=all_tools,
    # Additional configuration can be added here
)

# Get the ASGI app for the MCP server
app = mcp_server.app