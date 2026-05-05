import os
import google.generativeai as genai
from dotenv import load_dotenv
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model_name = "gemini-2.5-flash-lite"
    print(f"Testing {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hola, ¿estás funcionando con Gemini 2.5 Flash Lite?")
        print(f"Response: {response.text}")
        print(f"✅ Gemini {model_name} is WORKING correctly.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
else:
    print("No API Key found.")
