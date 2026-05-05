#!/usr/bin/env python3
"""
Script para probar el login directamente sin navegador
Esto ayudará a diagnosticar si el problema es del backend o del frontend
"""

import requests
import json

print("=" * 60)
print("🧪 TEST DE LOGIN DIRECTO")
print("=" * 60)
print()

# URL del servidor
base_url = "http://localhost:5000"

# Credenciales de prueba (admin)
test_credentials = {
    "cedula": "123456789",
    "password": "administrador123123456789"
}

print(f"📍 Servidor: {base_url}")
print(f"👤 Cédula: {test_credentials['cedula']}")
print(f"🔑 Password: {test_credentials['password'][:10]}...")
print()

try:
    print("🔄 Enviando solicitud POST a /login...")
    response = requests.post(
        f"{base_url}/login",
        json=test_credentials,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"📊 Status Code: {response.status_code}")
    print(f"📋 Headers: {dict(response.headers)}")
    print()
    
    print("📄 Response Content:")
    print("-" * 60)
    
    # Intentar parsear como JSON
    try:
        json_response = response.json()
        print(json.dumps(json_response, indent=2, ensure_ascii=False))
        print()
        
        if json_response.get('success'):
            print("✅ LOGIN EXITOSO!")
            print(f"🔗 Redirect: {json_response.get('redirect')}")
        else:
            print("❌ LOGIN FALLIDO")
            print(f"💬 Mensaje: {json_response.get('message')}")
            
    except json.JSONDecodeError:
        print("⚠️ La respuesta NO es JSON válido")
        print("📄 Contenido recibido:")
        print(response.text[:500])  # Primeros 500 caracteres
        print()
        
        if response.text.startswith('<!'):
            print("❌ ERROR: El servidor está devolviendo HTML en lugar de JSON")
            print("Esto indica un error en el backend antes de llegar a la respuesta JSON")
            
except requests.exceptions.ConnectionError:
    print("❌ ERROR: No se puede conectar al servidor")
    print("Verifica que el servidor esté corriendo en http://localhost:5000")
    
except Exception as e:
    print(f"❌ ERROR INESPERADO: {str(e)}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
