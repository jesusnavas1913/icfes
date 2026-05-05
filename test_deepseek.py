import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
print(f"DeepSeek API Key found: {'Yes' if api_key else 'No'}")

if api_key:
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hola, ¿estás funcionando con DeepSeek?"},
            ],
            stream=False
        )
        print(f"Response: {response.choices[0].message.content}")
        print("✅ DeepSeek API is WORKING correctly.")
    except Exception as e:
        print(f"❌ DeepSeek API Error: {str(e)}")
else:
    print("❌ No DEEPSEEK_API_KEY found in .env file.")
