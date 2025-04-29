__all__ = ["get_mcp"]
import os
import yaml
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack


def get_mcp(agent_id="chat"):
    """
    Get the MCP client instance.
    """
    server_params = get_mcp_servers(agent_id)

    return MCP(server_params)


def get_mcp_servers(agent_id: str):
    """
    Get the configuration for a given agent_id (key) from the agent_config.yml file at the project root.
    """

    try:
        config_path = "./config.yml"
        server_params = []
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"config.yml not found at {config_path}.")

        tool_names = []
        with open(config_path, "r") as config_file:
            config = yaml.safe_load(config_file)
            mcp_servers = config["mcp_servers"]
            tool_names = config["agents"][agent_id]["tools"]

        for tool_name in tool_names:
            if tool_name in mcp_servers:
                server_params.append(StdioServerParameters(**mcp_servers[tool_name]))
            else:
                raise ValueError(f"Tool {tool_name} not found in MCP tools configuration.")
        return server_params

    except Exception as e:
        raise ValueError(f"Error loading agent configuration: {e}")


class MCP:
    """
    Model Context Protocol (MCP) client implementation.
    """

    def __init__(self, server_params):
        self.exit_stack = AsyncExitStack()
        self.server_params = server_params
        self.sessions = []
        self._tool_session_map = {}

    async def run(self):
        """
        Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """

        try:
            for server in self.server_params:
                stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server))
                (self.stdio, self.write) = stdio_transport
                session = await self.exit_stack.enter_async_context(
                    ClientSession(
                        read_stream=self.stdio,
                        write_stream=self.write,
                    )
                )
                self.sessions.append(session)
            # initialize all sessions at once async
            await asyncio.gather(*[session.initialize() for session in self.sessions])
            print("Connected to MCP servers.")
        except Exception as e:
            print(f"Failed to connect to MCP server: {e}")

    async def get_tool_list(self):
        """
        Get the list of tools available in MCP server sessions.
        """
        tools = []

        for session in self.sessions:
            if not session:
                raise RuntimeError("MCP sessions are not initialized. Please run the server first.")

            session_list = await session.list_tools()

            for tool in session_list.tools:
                tools.append(tool)
                self._tool_session_map[tool.name] = session

        return tools

    async def get_tool_session(self, tool_name):
        """
        Get the session for a specific tool.
        """
        if tool_name in self._tool_session_map:
            return self._tool_session_map[tool_name]
        else:
            raise ValueError(f"Tool {tool_name} not found in MCP sessions.")
