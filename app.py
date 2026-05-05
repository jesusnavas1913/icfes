import bcrypt
from flask import render_template, redirect, request, session, jsonify, flash
from icfes_api import app
from supabase_client import get_supabase_client
import re
import json

# ===========================================
# CONFIGURACIÓN DE SEGURIDAD CRÍTICA
# ===========================================
from extensions import csrf
from security_config import configure_security
limiter = configure_security(app, csrf)

# ===========================================
# MANEJO DE ERRORES GLOBAL (JSON)
# ===========================================
@app.errorhandler(400)
def bad_request(e):
    if request.is_json or request.path.startswith('/api/') or request.path in ['/login', '/register/estudiante', '/register/profesor']:
        return jsonify({'success': False, 'message': f'Bad Request: {str(e)}'}), 400
    return render_template('error.html', error=e), 400

@app.errorhandler(404)
def not_found(e):
    if request.is_json or request.path.startswith('/api/'):
        return jsonify({'success': False, 'message': 'Resource not found'}), 404
    return render_template('error.html', error=e), 404

@app.errorhandler(500)
def server_error(e):
    if request.is_json or request.path.startswith('/api/') or request.path in ['/login', '/register/estudiante', '/register/profesor']:
        return jsonify({'success': False, 'message': f'Internal Server Error: {str(e)}'}), 500
    return render_template('error.html', error=e), 500


# Rutas de páginas (Front)
@app.route('/')
def root_page():
    return render_template('index.html')

@app.route('/login')
def login_page():
    # Limpiar sesión al acceder a login
    session.clear()
    return render_template('login.html')

@app.route('/test-connectivity')
def test_connectivity():
    """Página de prueba para verificar conectividad con el backend"""
    return render_template('test_connectivity.html')

@app.route('/login/profesor')
def login_profesor_page():
    # Limpiar sesión al acceder a login
    session.clear()
    return render_template('login.html', user_type='profesor')

@app.route('/login/estudiante')
def login_estudiante_page():
    # Limpiar sesión al acceder a login
    session.clear()
    return render_template('login.html', user_type='estudiante')

@app.route('/inicio')
def inicio_page():
    # Verificar si el usuario está logueado
    if 'user_type' not in session:
        return redirect('/login')
    # Renderizar la plantilla según el tipo de usuario
    if session['user_type'] == 'profesor':
        return render_template('dashboard_profesor.html')
    elif session['user_type'] == 'estudiante':
        return render_template('dashboard_estudiante.html')
    else:
        return redirect('/login')

@app.route('/test-login')
def test_login():
    return render_template('test_login.html')


@app.route('/dashboard/profesor')
def dashboard_profesor():
    if 'user_type' not in session or session['user_type'] != 'profesor':
        return redirect('/')
    return render_template('dashboard_profesor.html')

@app.route('/dashboard/estudiante')
def dashboard_estudiante():
    if 'user_type' not in session or session['user_type'] != 'estudiante':
        return redirect('/')
    return render_template('dashboard_estudiante.html')

@app.route('/dashboard')
def dashboard_page():
    # Verificar si el usuario está logueado
    if 'user_type' not in session:
        return redirect('/')
    # Si es profesor, mostrar dashboard profesor
    if session['user_type'] == 'profesor':
        return render_template('dashboard_profesor.html')
    # Si es estudiante, redirigir a su dashboard
    else:
        return render_template('dashboard_estudiante.html')

@app.route('/dashboard-estudiante')
def dashboard_estudiante_page():
    # Verificar si el usuario está logueado
    if 'user_type' not in session:
        return redirect('/')
    # Si es estudiante, mostrar dashboard estudiante
    if session['user_type'] == 'estudiante':
        return render_template('dashboard_estudiante.html')
    # Si es profesor, redirigir a su dashboard
    else:
        return render_template('dashboard_profesor.html')

@app.route('/simulator')
def simulator_page():
    # Verificar si el usuario está logueado
    if 'user_type' not in session:
        return redirect('/login/estudiante')
    # Solo estudiantes pueden acceder al simulador
    if session['user_type'] != 'estudiante':
        return redirect('/dashboard')  # Redirigir profesores a su dashboard
    return render_template('icfes_exam_simulator.html')

@app.route('/generator')
def generator_page():
    # Ambos tipos de usuario pueden acceder al generador de preguntas
    if 'user_type' not in session:
        return redirect('/login/estudiante')  # Default to estudiante for generator
    return render_template('icfes_generator_mcq.html', user_type=session['user_type'])

@app.route('/pdf-evaluation')
def pdf_evaluation_page():
    # Verificar si el usuario está logueado
    if 'user_type' not in session:
        return redirect('/login/profesor')
    # Solo profesores pueden acceder a la evaluación de PDF
    if session['user_type'] != 'profesor':
        return redirect('/dashboard-estudiante')  # Redirigir estudiantes a su dashboard
    return render_template('icfes_pdf_evaluation.html')

@app.route('/order-exercise')
def order_exercise_page():
    # Verificar si el usuario está logueado
    if 'user_type' not in session:
        return redirect('/login/estudiante')
    # Solo estudiantes pueden acceder al ejercicio de ordenamiento
    if session['user_type'] != 'estudiante':
        return redirect('/dashboard')  # Redirigir profesores a su dashboard
    return render_template('icfes_order_exercise.html')

@app.route('/progress')
def progress_page():
    # Verificar si el usuario está logueado
    if 'user_type' not in session:
        return redirect('/login/estudiante')
    # Solo estudiantes pueden acceder al progreso
    if session['user_type'] != 'estudiante':
        return redirect('/dashboard')  # Redirigir profesores a su dashboard
    return render_template('progress.html')

@app.route('/chat')
def chat_page():
    # Ambos tipos de usuario pueden acceder al chat
    if 'user_type' not in session:
        return redirect('/login/estudiante')  # Default to estudiante for chat
    return render_template('chat.html')

@app.route('/library')
def library_page():
    # Verificar si el usuario está logueado
    if 'user_type' not in session:
        return redirect('/login/profesor')
    # Solo profesores pueden acceder a la biblioteca
    if session['user_type'] != 'profesor':
        return redirect('/dashboard-estudiante')  # Redirigir estudiantes a su dashboard
    return render_template('library.html')

@app.route('/register/profesor', methods=['GET', 'POST'])
@csrf.exempt
@limiter.limit("3 per minute")  # Máximo 3 registros por minuto
def register_profesor():
    if request.method == 'POST':
        data = request.get_json()
        nombre = data.get('nombre')
        cedula = data.get('cedula')
        email = data.get('email')
        password = data.get('password')

        # Validaciones
        if not all([nombre, cedula, email, password]):
            return jsonify({'success': False, 'message': 'Todos los campos son requeridos'}), 400
        if not cedula.isdigit():
            return jsonify({'success': False, 'message': 'Cédula debe contener solo números'}), 400
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return jsonify({'success': False, 'message': 'Email inválido'}), 400
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Contraseña debe tener al menos 6 caracteres'}), 400

        supabase = get_supabase_client()

        # Verificar si cedula ya existe
        existing = supabase.table('profesores').select('cedula').eq('cedula', cedula).execute()
        if existing.data:
            return jsonify({'success': False, 'message': 'Cédula ya registrada'}), 400

        # Encriptar contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insertar en Supabase con aprobado=True (auto-aprobado)
        new_user = {
            'nombre': nombre,
            'cedula': cedula,
            'email': email,
            'password': hashed_password,
            'aprobado': True
        }
        supabase.table('profesores').insert(new_user).execute()

        return jsonify({'success': True, 'message': 'Registro exitoso. Ya puedes iniciar sesión.'})

    return render_template('register_profesor.html')

@app.route('/register/estudiante', methods=['GET', 'POST'])
@csrf.exempt
@limiter.limit("3 per minute")  # Máximo 3 registros por minuto
def register_estudiante():
    if request.method == 'POST':
        data = request.get_json()
        nombre = data.get('nombre')
        cedula = data.get('cedula')
        email = data.get('email')
        password = data.get('password')

        # Validaciones
        if not all([nombre, cedula, email, password]):
            return jsonify({'success': False, 'message': 'Todos los campos son requeridos'}), 400
        if not cedula.isdigit():
            return jsonify({'success': False, 'message': 'Cédula debe contener solo números'}), 400
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return jsonify({'success': False, 'message': 'Email inválido'}), 400
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Contraseña debe tener al menos 6 caracteres'}), 400

        supabase = get_supabase_client()

        # Verificar si cedula ya existe
        existing = supabase.table('estudiantes').select('cedula').eq('cedula', cedula).execute()
        if existing.data:
            return jsonify({'success': False, 'message': 'Cédula ya registrada'}), 400

        # Encriptar contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insertar en Supabase con aprobado=True (auto-aprobado)
        new_user = {
            'nombre': nombre,
            'cedula': cedula,
            'email': email,
            'password': hashed_password,
            'aprobado': True
        }
        supabase.table('estudiantes').insert(new_user).execute()

        return jsonify({'success': True, 'message': 'Registro exitoso'})

    return render_template('register_estudiante.html')

@app.route('/login', methods=['POST'])
@csrf.exempt
@limiter.limit("5 per minute")  # Máximo 5 intentos de login por minuto
def login():
    try:
        # Log request details
        print(f"DEBUG: Login request received")
        print(f"DEBUG: Content-Type: {request.content_type}")
        print(f"DEBUG: Request data: {request.data}")
        
        data = request.get_json()
        print(f"DEBUG: Parsed JSON: {data}")
        
        if data is None:
            print("ERROR: No JSON data received")
            return jsonify({'success': False, 'message': 'No se recibieron datos JSON'}), 400
            
        cedula = data.get('cedula')
        password = data.get('password')
        
        print(f"DEBUG: Cedula: {cedula}, Password length: {len(password) if password else 0}")

        if not cedula or not password:
            print("ERROR: Datos incompletos")
            return jsonify({'success': False, 'message': 'Datos incompletos'}), 400

        supabase = get_supabase_client()
        print("DEBUG: Supabase client obtained")

        # Buscar en tabla profesores
        profesor = supabase.table('profesores').select('*').eq('cedula', cedula).execute()
        print(f"DEBUG: Profesor query result: {len(profesor.data) if profesor.data else 0} records")
        
        if profesor.data:
            user = profesor.data[0]
            # Check de 'aprobado' eliminado - todos pueden entrar
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                session['user_id'] = user['id']
                session['user_type'] = 'profesor'
                print(f"DEBUG: Login exitoso para profesor: {cedula}")
                return jsonify({'success': True, 'redirect': '/dashboard/profesor'})
            else:
                print("DEBUG: Contraseña incorrecta para profesor")
                return jsonify({'success': False, 'message': 'Contraseña incorrecta'}), 401

        # Si no en profesores, buscar en estudiantes
        estudiante = supabase.table('estudiantes').select('*').eq('cedula', cedula).execute()
        print(f"DEBUG: Estudiante query result: {len(estudiante.data) if estudiante.data else 0} records")
        
        if estudiante.data:
            user = estudiante.data[0]
            # Check de 'aprobado' eliminado - todos pueden entrar
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                session['user_id'] = user['id']
                session['user_type'] = 'estudiante'
                print(f"DEBUG: Login exitoso para estudiante: {cedula}")
                return jsonify({'success': True, 'redirect': '/dashboard/estudiante'})
            else:
                print("DEBUG: Contraseña incorrecta para estudiante")
                return jsonify({'success': False, 'message': 'Cédula o contraseña incorrecta'}), 401

        # No encontrado en ninguna tabla
        print(f"DEBUG: Usuario no encontrado: {cedula}")
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
        
    except Exception as e:
        print(f"ERROR en login: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error interno: {str(e)}'}), 500

@app.route('/logout')
def logout():
    rol = session.get('rol')
    session.clear()
    return redirect('/login')

# ===========================================
# RUTAS DE ADMINISTRADOR
# ===========================================

@app.route('/admin/login')
def admin_login_page():
    # Limpiar sesión al acceder a login de admin
    session.clear()
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect('/admin/login')
    return render_template('admin_dashboard.html')

@app.route('/admin/users')
def admin_users():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect('/admin/login')
    return render_template('admin_users.html')

@app.route('/admin/pending-users')
def admin_pending_users():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect('/admin/login')
    return render_template('admin_pending_users.html')

# ===========================================
# API ENDPOINTS PARA ADMINISTRADOR
# ===========================================

@app.route('/api/admin/login', methods=['POST'])
@csrf.exempt
@limiter.limit("5 per minute")  # Máximo 5 intentos de login por minuto
def admin_login():
    data = request.get_json()
    cedula = data.get('cedula')
    password = data.get('password')

    if not cedula or not password:
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400

    supabase = get_supabase_client()

    # Buscar en tabla administradores
    admin = supabase.table('administradores').select('*').eq('cedula', cedula).execute()
    if admin.data:
        user = admin.data[0]
        # Comparar contraseña directamente (sin hash) - limpiar espacios
        db_password = user['password'].strip() if user['password'] else ''
        input_password = password.strip() if password else ''
        if input_password == db_password:
            session['user_id'] = user['id']
            session['user_type'] = 'admin'
            return jsonify({'success': True, 'redirect': '/admin/dashboard'})
        else:
            return jsonify({'success': False, 'message': 'Cédula o contraseña incorrecta'}), 401

    return jsonify({'success': False, 'message': 'Cédula o contraseña incorrecta'}), 401

@app.route('/api/admin/users', methods=['GET'])
@csrf.exempt
def get_all_users():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return jsonify({'error': 'Acceso no autorizado'}), 403

    supabase = get_supabase_client()

    try:
        # Obtener todos los profesores
        profesores = supabase.table('profesores').select('*').execute()
        # Obtener todos los estudiantes
        estudiantes = supabase.table('estudiantes').select('*').execute()

        users = {
            'profesores': profesores.data or [],
            'estudiantes': estudiantes.data or []
        }

        return jsonify({'success': True, 'users': users})
    except Exception as e:
        return jsonify({'error': f'Error obteniendo usuarios: {str(e)}'}), 500

@app.route('/api/admin/pending-users', methods=['GET'])
@csrf.exempt
def get_pending_users():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return jsonify({'error': 'Acceso no autorizado'}), 403

    supabase = get_supabase_client()

    try:
        # Obtener profesores pendientes
        profesores_pendientes = supabase.table('profesores').select('*').eq('aprobado', False).execute()
        # Obtener estudiantes pendientes
        estudiantes_pendientes = supabase.table('estudiantes').select('*').eq('aprobado', False).execute()

        pending_users = {
            'profesores': profesores_pendientes.data or [],
            'estudiantes': estudiantes_pendientes.data or []
        }

        return jsonify({'success': True, 'pending_users': pending_users})
    except Exception as e:
        return jsonify({'error': f'Error obteniendo usuarios pendientes: {str(e)}'}), 500

@app.route('/api/admin/approve-user', methods=['POST'])
@csrf.exempt
def approve_user():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return jsonify({'error': 'Acceso no autorizado'}), 403

    data = request.get_json()
    print(f"DEBUG: Received data for approve-user: {data}")
    app.logger.info(f"Received data for approve-user: {data}")
    user_id = data.get('user_id')
    user_type = data.get('user_type')  # 'profesor' o 'estudiante'
    print(f"DEBUG: user_id: {user_id} (type: {type(user_id)}), user_type: {user_type}")
    app.logger.info(f"user_id: {user_id} (type: {type(user_id)}), user_type: {user_type}")

    # Normalize user_type
    if user_type == 'profesores':
        user_type = 'profesor'
    elif user_type == 'estudiantes':
        user_type = 'estudiante'

    if not user_id or user_type not in ['profesor', 'estudiante']:
        print(f"DEBUG: Datos inválidos: user_id={user_id}, user_type={user_type}")
        app.logger.error(f"Datos inválidos: user_id={user_id}, user_type={user_type}")
        return jsonify({'error': 'Datos inválidos'}), 400

    supabase = get_supabase_client()

    try:
        table_name = 'profesores' if user_type == 'profesor' else 'estudiantes'
        print(f"DEBUG: Updating table {table_name} for user_id {user_id}")
        result = supabase.table(table_name).update({'aprobado': True}).eq('id', user_id).execute()
        print(f"DEBUG: Update result: {result}")
        app.logger.info(f"Update result: {result}")

        return jsonify({'success': True, 'message': f'Usuario {user_type} aprobado exitosamente'})
    except Exception as e:
        print(f"DEBUG: Error aprobando usuario: {str(e)}")
        app.logger.error(f"Error aprobando usuario: {str(e)}")
        return jsonify({'error': f'Error aprobando usuario: {str(e)}'}), 500

@app.route('/api/admin/reject-user', methods=['POST'])
@csrf.exempt
def reject_user():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return jsonify({'error': 'Acceso no autorizado'}), 403

    data = request.get_json()
    user_id = data.get('user_id')
    user_type = data.get('user_type')  # 'profesor' o 'estudiante'

    if not user_id or user_type not in ['profesor', 'estudiante']:
        return jsonify({'error': 'Datos inválidos'}), 400

    supabase = get_supabase_client()

    try:
        table_name = 'profesores' if user_type == 'profesor' else 'estudiantes'
        supabase.table(table_name).delete().eq('id', user_id).execute()

        return jsonify({'success': True, 'message': f'Usuario {user_type} rechazado y eliminado'})
    except Exception as e:
        return jsonify({'error': f'Error rechazando usuario: {str(e)}'}), 500

@app.route('/api/admin/delete-user', methods=['POST'])
@csrf.exempt
def delete_user():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return jsonify({'error': 'Acceso no autorizado'}), 403

    data = request.get_json()
    user_id = data.get('user_id')
    user_type = data.get('user_type')  # 'profesor' o 'estudiante'

    if not user_id or user_type not in ['profesor', 'estudiante']:
        return jsonify({'error': 'Datos inválidos'}), 400

    supabase = get_supabase_client()

    try:
        table_name = 'profesores' if user_type == 'profesor' else 'estudiantes'
        supabase.table(table_name).delete().eq('id', user_id).execute()

        return jsonify({'success': True, 'message': f'Usuario {user_type} eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': f'Error eliminando usuario: {str(e)}'}), 500

if __name__ == '__main__':
    import os
    host = '0.0.0.0' if os.getenv('FLASK_ENV') == 'production' else '127.0.0.1'
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host=host, port=5000)
else:
    # Para producción con gunicorn
    application = app
