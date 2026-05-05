#!/usr/bin/env python3
"""
Script to add @csrf.exempt decorators to all AI endpoints in icfes_api.py
"""

import re

# Read the file
with open('icfes_api.py', 'r', encoding='utf-8') as f:
    content = f.read()

# First, add the CSRF import after app.secret_key line
csrf_import = """
# Import CSRF to exempt AI endpoints
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
"""

# Find the line with app.secret_key and add the import after it
content = content.replace(
    "app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')\n\n",
    f"app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')\n{csrf_import}\n"
)

# List of endpoints to add @csrf.exempt to
endpoints = [
    "/generate-question",
    "/evaluate-order",
    "/get-feedback",
    "/analyze-document",
    "/add-custom-knowledge",
    "/save-model",
    "/generate-visual",
    "/generate-visual-by-competencia",
    "/generate-geometry-visual",
    "/submit-all-answers",
    "/api/chat"
]

# Add @csrf.exempt to each endpoint
for endpoint in endpoints:
    # Pattern to find @app.route(endpoint, methods=['POST'])
    pattern = f"(@app\\.route\\('{re.escape(endpoint)}'.*?\\n)(def )"
    replacement = r"\1@csrf.exempt\n\2"
    content = re.sub(pattern, replacement, content)

# Write the modified content back
with open('icfes_api.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Successfully added @csrf.exempt to all AI endpoints!")
print(f"✅ Modified {len(endpoints)} endpoints")
print("\nEndpoints modified:")
for endpoint in endpoints:
    print(f"  - {endpoint}")
