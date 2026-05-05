import requests
import json

# Test the generate-question endpoint
url = "http://127.0.0.1:5000/generate-question"
data = {
    "competencia": "Matemáticas",
    "num_questions": 1,
    "dificultad": "medio",
    "use_custom_knowledge": False
}

try:
    response = requests.post(url, json=data, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
