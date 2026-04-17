import google.generativeai as genai
import sys

API_KEY = "AIzaSyCqB_ChatoUtT34IIN3VnXCEo84efNF9g8"

try:
    genai.configure(api_key=API_KEY)
    print("Listing available models for this API key:")
    models = genai.list_models()
    for m in models:
        print(f"- {m.name} (Supports: {m.supported_generation_methods})")
except Exception as e:
    print(f"Error listing models: {e}")
