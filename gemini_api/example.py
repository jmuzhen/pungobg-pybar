"""
Before running the example, ensure you have a valid Gemini API key set in your environment variables.
Get one here: https://aistudio.google.com/app/apikey
...then run `export GEMINI_API_KEY=<API key here>` in your terminal.
"""

from gemini import *

# Create a new chat context
context = Chat()

# Create a new Gemini instance
gemini = Gemini(context)

print(gemini.generate("What is the meaning of life?"))

# ... or continue a conversation!
messages = [
    {"role": "user", "content": "What is NUSH?"},
    {"role": "model", "content": "NUSH stands for National University of Singapore High School."},
]

context2 = Chat(messages)

gemini.set_context(context2)
print(gemini.generate("What is the school motto?"))
