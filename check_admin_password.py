from supabase_client import get_supabase_client

client = get_supabase_client()
result = client.table('administradores').select('*').eq('cedula', '123456789').execute()

if result.data:
    admin = result.data[0]
    password = admin.get('password', '')
    print(f'\n✅ Admin encontrado:')
    print(f'   Nombre: {admin.get("nombre")}')
    print(f'   Cédula: {admin.get("cedula")}')
    print(f'   Password completo: {password}')
    print(f'   Longitud del password: {len(password)} caracteres')
else:
    print('⚠️  No se encontró admin con cedula 123456789')
