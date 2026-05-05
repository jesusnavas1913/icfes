from supabase_client import get_supabase_client

client = get_supabase_client()
result = client.table('administradores').select('*').execute()

print(f'\n✅ Total administradores en la base de datos: {len(result.data)}\n')

if result.data:
    for admin in result.data:
        print(f"  - Nombre: {admin.get('nombre')}")
        print(f"    Cédula: {admin.get('cedula')}")
        print(f"    Password (primeros 20 chars): {admin.get('password', '')[:20]}...")
        print()
else:
    print("⚠️  No hay administradores en la base de datos.")
    print("   Ejecuta 'python create_admin.py' para crear uno.\n")
