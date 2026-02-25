import google.generativeai as genai
from decouple import config

# Configure API key
genai.configure(api_key=config('GEMINI_API_KEY'))

# List available models
print("Available Gemini models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")