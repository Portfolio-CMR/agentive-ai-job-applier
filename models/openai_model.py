import os
from dotenv import load_dotenv
from openai import OpenAI
import openai

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the .env file in the root directory
env_path = os.path.join(script_dir, '..', '.env')

# Load environment variables from the .env file
load_dotenv(env_path)

class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

# Configuration
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key must be provided")

openai.api_key = api_key

client = OpenAI()

async def gpt(messages: [Message]) -> str:
    chat_messages = [{"role": message.role, "content": message.content} for message in messages]

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            messages=chat_messages
        )

        if response.choices and response.choices[0] and response.choices[0].message:
            return response.choices[0].message.content
        else:
            raise ValueError("Invalid response from OpenAI API")
    except Exception as error:
        print('Error making OpenAI API request:', error)
        raise error
