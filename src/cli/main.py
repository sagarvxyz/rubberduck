from src.agent.main import Agent
from src.agent.types import Message, TextPart


def get_user_message():
    text = input("You: ")
    if text.lower() == "exit":
        print("Exiting...")
        exit(0)
    message = Message(role="user", parts=[TextPart(type="text", text=text)])
    return message


async def run():
    client = Agent("cli_agent")
    # code_agent = Agent("code_agent")

    while True:
        user_message = get_user_message()
        # Process the user message
        response = client.post_message([user_message])
        print("Code Agent: ", end="", flush=True)
        async for chunk in response:
            print(chunk, end="", flush=True)  # Print chunk immediately
        print("")
