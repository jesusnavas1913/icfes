import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")

if api_key:
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hola, ¿estás funcionando?")
        print(f"Response: {response.text}")
        print("✅ Gemini API is WORKING correctly.")
    except Exception as e:
        print(f"❌ Gemini API Error: {str(e)}")
        
        print("\nChecking available models...")
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"- {m.name}")
        except Exception as e2:
            print(f"Could not list models: {e2}")
else:
    print("❌ No API Key found in .env file.")
