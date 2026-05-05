import sys
sys.stdout.reconfigure(encoding='utf-8')

from supabase_client import get_supabase_client

client = get_supabase_client()
result = client.table('administradores').select('*').execute()

if result.data:
    print(f"\nAdministradores en la BD: {len(result.data)}\n")
    for admin in result.data:
        nombre = admin.get('nombre', 'N/A')
        cedula = admin.get('cedula', 'N/A')
        password = admin.get('password', 'N/A')
        print(f"  Nombre  : {nombre}")
        print(f"  Cedula  : {cedula}")
        print(f"  Password: {password}")
        print("  ---")
else:
    print("No hay administradores registrados.")
    print("Usa: python create_admin.py  para crear uno.")
