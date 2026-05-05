import os
import google.generativeai as genai
from dotenv import load_dotenv
import sys

# Configure UTF-8 for Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key found: {api_key[:10]}...")

if api_key:
    genai.configure(api_key=api_key)
    print("\nChecking available models...")
    try:
        models = genai.list_models()
        found = False
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
                found = True
        
        if found:
            # Try a simple generation with the first found model
            model_to_test = "models/gemini-1.5-flash"
            print(f"\nTesting {model_to_test}...")
            model = genai.GenerativeModel(model_to_test)
            response = model.generate_content("Hola")
            print(f"Response: {response.text}")
        else:
            print("No models supporting generateContent found.")
            
    except Exception as e:
        print(f"Error: {str(e)}")
else:
    print("No API Key found.")
