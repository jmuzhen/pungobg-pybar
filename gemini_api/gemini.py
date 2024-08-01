from .gemini_prompt import *
from .gemini_utils import *


class Chat:
    def __init__(self, history=None):
        self.history = []
        
        if history:
            try:
                for message in history:
                    self.push(message["content"], message["role"])
            except Exception as e:
                print(f"Error initialising history: {e}")
    
    def push(self, message, role):
        self.history.append(self._get_content(message, role))
    
    def _get_content(self, message, role):
        return genai.types.ContentDict(parts=[message], role=role)


class Gemini:
    def __init__(self, context: Chat = None, api_key: str = None):
        if api_key is None:
            api_key = get_api_key()
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel(get_model(),
                                           safety_settings=get_safety_settings(),
                                           generation_config=get_generation_config(),
                                           system_instruction=get_system_prompt())
        
        self.chat = None
        self.set_context(context)
    
    def generate(self, prompt):
        try:
            response = self.chat.send_message(prompt).text
        except Exception as e:
            response = str(e)
        
        return response
    
    def set_context(self, context: Chat = None):
        if not context:
            context = Chat()
        
        self.chat = genai.ChatSession(
            self.model,
            history=context.history,
        )
