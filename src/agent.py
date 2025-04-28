__all__ = ["get_agent"]
from src.llm import get_llm_client
from src.mcp import get_mcp


def get_agent(agent_id: str):
    """
    Get the agent instance based on the agent_id.
    """

    agent_config = get_agent_config(agent_id)
    if agent_config["model_provider"] == "google":

        mcp_client = get_mcp(agent_id)

        return Agent(
            agent_id=agent_id,
            agent_config=agent_config,
            llm_client=get_llm_client(agent_id),
            mcp_client=mcp_client,
        )

    else:
        raise ValueError(f"Unsupported model provider: {agent_config['model_provider']}")


def get_agent_config(agent_id: str):
    """
    Get the configuration for a given agent_id (key) from the agent_config.yml file at the project root.
    """
    import os
    import yaml

    try:
        config_path = "./config.yml"
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"config.yml not found at {config_path}.")

        with open(config_path, "r") as config_file:

            config = yaml.safe_load(config_file)

            return config["agents"][agent_id]

    except Exception as e:
        raise ValueError(f"Error loading agent configuration: {e}")


class Agent:
    """
    An LLM connected agent that can process messages and interact with a user or other agents.
    Each agent maintains a full history of messages and responses.
    """

    def __init__(self, agent_id, agent_config, llm_client, mcp_client):

        self.name = agent_config["name"]
        self.agent_id = agent_id
        self.config = agent_config

        self._llm_client = llm_client
        self._mcp_client = mcp_client
        self._history = []

    async def run(self):

        self._llm_client.run()
        await self._mcp_client.run()

    async def post(self, message):
        """
        Post a message to the agent and return the response.
        """

        new_content = self._llm_client.create_content(
            content=message,
            type="text",
            role="user",
        )
        self._history.append(new_content)

        mcp_tools = await self._mcp_client.get_tool_list()

        llm_tools = self._llm_client.create_tools(mcp_tools)
        # print(llm_tools)
        response = await self._llm_client.post(
            contents=self._history, agent_config=self.config, tools=llm_tools
        )
        if not response:
            raise ValueError("No response received from the LLM client.")

        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call

            session = await self._mcp_client.get_tool_session(function_call.name)
            if not session:
                raise ValueError(f"Session for tool {function_call.name} not found.")
            # Call the MCP server with the predicted tool
            result = await session.call_tool(function_call.name, arguments=function_call.args)
            response = result.content[0]

        content = self._llm_client.create_content(
            content=response.text,
            type="text",
            role="model",
        )
        self._history.append(content)
        return content
