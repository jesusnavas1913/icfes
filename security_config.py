# ===========================================
# CONFIGURACIÓN DE SEGURIDAD CRÍTICA
# ===========================================
# Este archivo contiene las mejoras de seguridad implementadas
# para proteger la aplicación contra ataques comunes

from datetime import timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

def configure_security(app, csrf):
    """
    Configura las medidas de seguridad críticas para la aplicación Flask
    
    Incluye:
    1. Session Timeout (2 horas)
    2. CSRF Protection
    3. Rate Limiting
    """
    
    # 1. Configurar timeout de sesiones (2 horas)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
    
    # 2. Configurar CSRF Protection
    csrf.init_app(app)
    
    # 3. Configurar Rate Limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"  # Cambiar a Redis en producción: "redis://localhost:6379"
    )
    
    # Configurar before_request para sesiones permanentes
    @app.before_request
    def make_session_permanent():
        """Hacer las sesiones permanentes para que expiren según PERMANENT_SESSION_LIFETIME"""
        from flask import session
        session.permanent = True
    
    return limiter


# ===========================================
# DECORADORES DE RATE LIMITING
# ===========================================
# Aplicar estos decoradores a las rutas críticas:

"""
EJEMPLO DE USO EN app.py:

from security_config import configure_security

# Configurar seguridad
limiter, csrf = configure_security(app)

# Aplicar rate limiting a rutas críticas:

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Máximo 5 intentos por minuto
def login():
    # ... código existente ...
    pass

@app.route('/api/estudiante/register', methods=['POST'])
@limiter.limit("3 per minute")  # Máximo 3 registros por minuto
def register_estudiante():
    # ... código existente ...
    pass

@app.route('/api/profesor/register', methods=['POST'])
@limiter.limit("3 per minute")
def register_profesor():
    # ... código existente ...
    pass

@app.route('/api/admin/login', methods=['POST'])
@limiter.limit("5 per minute")
def admin_login():
    # ... código existente ...
    pass

@app.route('/api/estudiante/change-password', methods=['POST'])
@limiter.limit("3 per minute")
def change_password_estudiante():
    # ... código existente ...
    pass

@app.route('/api/profesor/change-password', methods=['POST'])
@limiter.limit("3 per minute")
def change_password_profesor():
    # ... código existente ...
    pass

@app.route('/api/admin/change-password', methods=['POST'])
@limiter.limit("3 per minute")
def admin_change_password():
    # ... código existente ...
    pass
"""
