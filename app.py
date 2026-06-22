"""
====================================================
SISTEMA DE COSTOS DE ENVÍOS POR REPARTIDOR
Framework: Flask (Python) - Patrón MVC
====================================================
Archivo principal: app.py
Rol en MVC: Punto de entrada de la aplicación.
Inicializa Flask, registra rutas y arranca el servidor.
"""

import os
from flask import Flask
from app.controllers.envio_controller import envio_bp  # Importa el controlador (Blueprint)
from database.db import init_db                         # Función para inicializar la BD

# Ruta absoluta al directorio del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------
# Crear instancia de la aplicación Flask
# --------------------------------------------------
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'app', 'views', 'templates')
)
app.secret_key = 'mvc_envios_secretkey'

# --------------------------------------------------
# Registrar rutas del controlador principal
# --------------------------------------------------
app.register_blueprint(envio_bp)

# --------------------------------------------------
# Inicializar base de datos y datos de prueba
# --------------------------------------------------
with app.app_context():
    init_db()

# --------------------------------------------------
# Punto de arranque
# --------------------------------------------------
if __name__ == '__main__':
    print("🚀 Sistema de Costos de Envíos iniciado en http://127.0.0.1:5000")
    app.run(debug=True)
