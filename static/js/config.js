/**
 * Frontend Configuration
 * IMPORTANTE: En producción, configura estas variables en tu servidor
 * Las credenciales de Supabase son públicas, pero es mejor práctica usar variables de entorno
 */

(function() {
    'use strict';
    
    // Obtener variables de entorno o usar valores por defecto
    // En producción, window.ENV debe ser configurado por el servidor
    const SUPABASE_URL = (window.ENV && window.ENV.SUPABASE_URL) || 'https://xapvvirzbxydmrymobja.supabase.co';
    const SUPABASE_ANON_KEY = (window.ENV && window.ENV.SUPABASE_ANON_KEY) || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhhcHZ2aXJ6Ynh5ZG1yeW1vYmphIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg4MTAwMjEsImV4cCI6MjA3NDM4NjAyMX0.1MPy5GIxJOHolm0Xl69bw8TN6h2F1PLaNt-d1CRsIV8';

    // API URL - Detección automática de entorno
    // En desarrollo: usa localhost, en producción: usa la URL de Render
    // Puede ser sobrescrita con window.ENV?.API_URL
    const hostname = window.location.hostname;
    const API_URL = (window.ENV && window.ENV.API_URL) || 
        (hostname === 'localhost' || hostname === '127.0.0.1' 
            ? 'http://127.0.0.1:5000' 
            : window.location.origin);

    // Exportar como variables globales para compatibilidad
    window.API_URL = API_URL;
    window.CONFIG = {
        SUPABASE_URL: SUPABASE_URL,
        SUPABASE_ANON_KEY: SUPABASE_ANON_KEY,
        API_URL: API_URL
    };
    
    // Log para debugging (solo en desarrollo)
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        console.log('🔧 Config cargada:', { API_URL: API_URL });
    }
})();
