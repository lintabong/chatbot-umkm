

from app import mongo, client, genai_context
from google.genai import types

def create_chat(history=[]):
    return client.chats.create(
        model='gemini-2.5-flash',
        config=types.GenerateContentConfig(
                system_instruction=(genai_context)
            ),
        history=history if len(history) > 0 else None
    )