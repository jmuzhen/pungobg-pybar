import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


def get_model():
    return "gemini-1.5-flash-latest"


def get_api_key():
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    return os.getenv('GEMINI_API_KEY')


def get_safety_settings():
    return {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }


def get_generation_config():
    return genai.types.GenerationConfig(
        max_output_tokens=512,  # [1, 8192]
        temperature=0.8,  # [0, 2]
    )
