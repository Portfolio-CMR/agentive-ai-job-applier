import os
from google.generativeai import GenerativeModel, configure

api_key = os.environ.get('GEMINI_API_KEY')
model_name = os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash')

if not api_key:
    raise ValueError("Gemini API key was not provided.")

configure(api_key=api_key)
model = GenerativeModel(model_name=model_name)

async def gemini(messages):
    prompt = '\n'.join([f"{message['role']}: {message['content']}" for message in messages])

    try:
        result = await model.generate_content(prompt)
        return result.text
    except Exception as error:
        error_context = {
            'error': str(error),
            'stack': getattr(error, '__traceback__', None),
            'prompt': prompt,
        }

        raise RuntimeError(f"Failed to generate content with Gemini API. Context: {error_context}")