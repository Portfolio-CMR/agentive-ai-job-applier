import os
import asyncio
from google.generativeai import GenerativeModel, configure

# Custom Message class
class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

api_key = os.environ.get('GEMINI_API_KEY')
model_name = os.environ.get('GEMINI_MODEL')

if not api_key:
    raise ValueError("Gemini API key was not provided.")

configure(api_key=api_key)
model = GenerativeModel(model_name=model_name)

async def gemini(messages):
    # Convert messages to the format expected by Gemini
    gemini_messages = []
    for message in messages:
        role = "model" if message.role == 'assistant' else message.role
        gemini_messages.append({"role": role, "parts": [message.content]})

    try:
        # Start a chat session
        chat = model.start_chat(history=gemini_messages[:-1])
        
        # Send the last message and get the response
        response = await chat.send_message_async(gemini_messages[-1]['parts'][0])
        
        return response.text
    except Exception as error:
        error_context = {
            'error': str(error),
            'stack': getattr(error, '__traceback__', None),
            'messages': [(msg.role, msg.content) for msg in messages],  # Convert messages to a list of tuples for logging
        }

        raise RuntimeError(f"Failed to generate content with Gemini API. Context: {error_context}")

# Example usage
async def main():
    messages = [
        Message(role="user", content="Hello, how are you?"),
        Message(role="assistant", content="I'm doing well, thank you! How can I assist you today?"),
        Message(role="user", content="Tell me a joke about programming.")
    ]
    
    response = await gemini(messages)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())