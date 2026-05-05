import bcrypt

# INSTRUCCIONES:
# 1. Cambia la variable 'nueva_contraseña' con tu nueva contraseña
# 2. Ejecuta este script: python generar_hash_password.py
# 3. Copia el hash generado
# 4. Usa el SQL que se muestra al final

# ========================================
# CONFIGURA TU NUEVA CONTRASEÑA AQUÍ
# ========================================
nueva_contraseña = "MiNuevaContraseña123"  # ⬅️ CAMBIA ESTO
tu_cedula = "1234567890"  # ⬅️ CAMBIA ESTO

# ========================================
# GENERAR HASH BCRYPT
# ========================================
print("=" * 60)
print("🔐 GENERADOR DE HASH BCRYPT PARA CONTRASEÑA")
print("=" * 60)
print()

# Generar hash
hashed_password = bcrypt.hashpw(nueva_contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print(f"✅ Hash generado exitosamente!")
print()
print(f"📝 Nueva contraseña: {nueva_contraseña}")
print(f"🔒 Hash bcrypt: {hashed_password}")
print()
print("=" * 60)
print("📋 SQL PARA EJECUTAR EN SUPABASE")
print("=" * 60)
print()
print("-- Para ESTUDIANTE:")
print(f"UPDATE estudiantes SET password = '{hashed_password}' WHERE cedula = '{tu_cedula}';")
print()
print("-- Para PROFESOR:")
print(f"UPDATE profesores SET password = '{hashed_password}' WHERE cedula = '{tu_cedula}';")
print()
print("=" * 60)
print("🚀 PASOS SIGUIENTES:")
print("=" * 60)
print("1. Copia el SQL de arriba")
print("2. Ve a Supabase → SQL Editor")
print("3. Pega y ejecuta el SQL correspondiente")
print("4. Intenta iniciar sesión con tu nueva contraseña")
print("=" * 60)
