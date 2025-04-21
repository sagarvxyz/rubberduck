import os
from dotenv import load_dotenv
from google import genai


def get_api_key():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("""
            Error: GEMINI_API_KEY not set. 
            Create or update a `.env` file with a valid API key in the project root.
        """)
        return
    else:
        return api_key


def app():
    try:
        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(model="gemini-2.5-flash-preview-04-17")

        response = chat.send_message_stream("Hello world! Tell me about yourself.")
        for chunk in response:
            print(chunk.text, end="")

        # for message in chat.get_history():
        #     print(f'role - {message.role}', end=": ")
        #     print(message.parts[0].text)

    except Exception as e:
        print(f"\nAn error occurred during the Gemini API call: {e}")
        print("Please check your API key, internet connection, and API usage limits.")
