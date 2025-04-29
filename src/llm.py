__all__ = ["get_llm_client"]

import os
import mimetypes
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from google import genai
from google.genai import types

default_model_name = "gemini-2.0-flash"
default_config = types.GenerateContentConfigDict()


def get_llm_client(agent_id):
    """
    Get the LLM client based on the agent ID.
    """
    if agent_id:

        return GoogleLLMClient()
    else:
        raise ValueError(f"Unsupported model provider: {agent_id}")


class LLMClient(ABC):
    """
    Abstract base class for LLM clients.
    """

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def create_content(self, content, type="text", role="user"):
        pass

    @abstractmethod
    def create_tools(self, content, type="text", role="user"):
        pass

    @abstractmethod
    async def post(self, contents, config={}, tools=None):
        pass


class GoogleLLMClient(LLMClient):
    """
    Google LLM client implementation.
    """

    def __init__(self):
        self.client = None

    def run(self):
        """
        Get the Google GenAI client.
        """
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "API key not found. Please set the GOOGLE_API_KEY environment variable."
            )

        self.client = genai.Client(api_key=api_key)

    def create_content(self, content, type="text", role="user"):
        """Convert content into the proper format."""
        if type == "text":
            return types.Content(parts=[types.Part.from_text(text=content)], role=role)
        elif type == "file":
            (mime_type, _encoding) = mimetypes.guess_type(content)
            if mime_type is None:
                raise ValueError(f"Could not determine MIME type for file: {content}")
            return types.Content(
                role, parts=[types.Part.from_uri(file_uri=content, mime_type=mime_type)]
            )
        else:
            raise ValueError(f"Unsupported message type: {type}")

    def create_tools(self, tools):
        """Convert tools from MCP to Gemini format."""
        llm_tools = []
        for tool in tools:
            parameters = {}
            for key, value in tool.inputSchema.items():
                if key not in ["additionalProperties", "$schema"]:
                    parameters[key] = value
            try:
                llm_tool = types.Tool(
                    function_declarations=[
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": parameters,
                        }
                    ]
                )
                llm_tools.append(llm_tool)
            except Exception:
                continue

        return llm_tools

    async def post(self, contents, agent_config={}, tools=None):
        """Post contents to the Google GenAI client. Use create_content to format content before posting."""
        merged_config = default_config | agent_config.get("config", {})

        if not contents:
            raise ValueError("No contents provided to post.")

        # Pass tools_to_pass as a separate argument to generate_content
        response = await self.client.aio.models.generate_content(
            model=agent_config.get("model_name", default_model_name),
            contents=contents,
            config=types.GenerateContentConfig(**merged_config, tools=tools),
        )

        return response
