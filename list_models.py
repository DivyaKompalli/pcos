import google.generativeai as genai
import sys
import os

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    try:
        with open(".env", "r") as f:
            for line in f:
                if "API_KEY" in line:
                    API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    except FileNotFoundError:
        pass

if not API_KEY:
    print("API_KEY not found in .env or environment variables.")
    sys.exit(1)

try:
    genai.configure(api_key=API_KEY)
    print("Listing available models for this API key:")
    models = genai.list_models()
    for m in models:
        print(f"- {m.name} (Supports: {m.supported_generation_methods})")
except Exception as e:
    print(f"Error listing models: {e}")
