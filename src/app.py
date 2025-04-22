from google import genai


def app(config):
    try:
        start_agent(config)
    except Exception as e:
        print(f"\nAn error occurred during the Gemini API call: {e}")
        print("Please check your API key, internet connection, and API usage limits.")


def start_agent(config):
    """
    Create a new agent with the given configuration.
    """
    # Implement the logic to create a new agent using the provided config
    client = genai.Client(api_key=config["api_key"])
    agent = client.chats.create(model=config["model"])

    def get_user_input():
        return input("\u001b[93mYou\u001b[0m: ")

    def get_response(context, message):
        print("\u001b[93mDuck\u001b[0m: ", end="", flush=True)
        full_response = ""
        response = agent.send_message_stream(message)

        for chunk in response:
            print(chunk.text, end="\n", flush=True)
            full_response += chunk.text

        return full_response

    def run(context=""):
        """
        Run the agent with the given context.
        """
        conversation = []
        print("\u001b[93mDuck\u001b[0m: ", "Quack? (ctrl-c to exit)")
        is_running = True
        while is_running:
            try:
                user_message = get_user_input()
                conversation.append({"role": "user", "content": user_message})
                agent_response = get_response(context, user_message)
                conversation.append({"role": "chat_agent", "content": agent_response})

            except KeyboardInterrupt:
                print("\nExiting...")
                print(agent.get_history())
                is_running = False
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                is_running = False

    run()
