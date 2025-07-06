
import os
from app import client
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def create_chat(history=[]):
    return client.chats.create(
        model=os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'),
        config=types.GenerateContentConfig(
                system_instruction=(os.getenv('GEMINI_CONTEXT', ''))
            ),
        history=history if len(history) > 0 else None
    )
