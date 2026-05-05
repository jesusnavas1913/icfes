#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la configuración de Supabase
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("=" * 60)
print("🔍 DIAGNÓSTICO DE CONFIGURACIÓN DE SUPABASE")
print("=" * 60)
print()

# Verificar variables de entorno
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
secret_key = os.getenv('SECRET_KEY')

print("📋 Variables de Entorno:")
print(f"  SUPABASE_URL: {'✅ Configurada' if supabase_url else '❌ NO CONFIGURADA'}")
if supabase_url:
    print(f"    Valor: {supabase_url[:30]}...")
    
print(f"  SUPABASE_KEY: {'✅ Configurada' if supabase_key else '❌ NO CONFIGURADA'}")
if supabase_key:
    print(f"    Valor: {supabase_key[:20]}...")
    
print(f"  GOOGLE_API_KEY: {'✅ Configurada' if google_api_key else '❌ NO CONFIGURADA'}")
if google_api_key:
    print(f"    Valor: {google_api_key[:20]}...")
    
print(f"  SECRET_KEY: {'✅ Configurada' if secret_key else '❌ NO CONFIGURADA'}")
if secret_key:
    print(f"    Valor: {secret_key[:20]}...")

print()
print("=" * 60)

# Intentar conectar a Supabase
if supabase_url and supabase_key:
    print("🔌 Intentando conectar a Supabase...")
    try:
        from supabase import create_client
        client = create_client(supabase_url, supabase_key)
        print("✅ Conexión a Supabase exitosa!")
        
        # Intentar hacer una consulta simple
        try:
            result = client.table('administradores').select('cedula').limit(1).execute()
            print(f"✅ Consulta de prueba exitosa! Encontrados {len(result.data)} registros")
        except Exception as e:
            print(f"❌ Error en consulta de prueba: {str(e)}")
            
    except Exception as e:
        print(f"❌ Error conectando a Supabase: {str(e)}")
else:
    print("❌ No se puede conectar - Variables de entorno faltantes")

print("=" * 60)
print()

# Verificar archivo .env
print("📁 Verificando archivo .env:")
if os.path.exists('.env'):
    print("  ✅ Archivo .env existe")
    with open('.env', 'r') as f:
        lines = f.readlines()
    print(f"  📝 Contiene {len(lines)} líneas")
    
    # Verificar qué variables están definidas (sin mostrar valores)
    env_vars = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            var_name = line.split('=')[0].strip()
            env_vars.append(var_name)
    
    print(f"  📋 Variables definidas: {', '.join(env_vars)}")
else:
    print("  ❌ Archivo .env NO EXISTE")
    print()
    print("  💡 Necesitas crear un archivo .env con:")
    print("     SUPABASE_URL=tu_url_de_supabase")
    print("     SUPABASE_KEY=tu_key_de_supabase")
    print("     GOOGLE_API_KEY=tu_api_key_de_google")
    print("     SECRET_KEY=tu_secret_key")

print("=" * 60)
