"""
====================================================
CAPA DE BASE DE DATOS
====================================================
Archivo: database/db.py
Rol en MVC: Infraestructura de datos.
Contiene:
  - Creación de tablas (DDL)
  - Datos de prueba (Seeders)
  - Función de conexión reutilizable
====================================================
"""

import sqlite3
import os

# Ruta absoluta de la base de datos SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), 'envios.db')


def get_connection():
    """
    Abre y retorna una conexión a la base de datos SQLite.
    Usa row_factory para acceder a columnas por nombre.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # Permite acceso por nombre de columna
    return conn


def init_db():
    """
    Inicializa la base de datos:
      1. Crea las tablas si no existen.
      2. Inserta datos de prueba si las tablas están vacías.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # ------------------------------------------------
    # DDL - Creación de tablas
    # ------------------------------------------------

    # TABLA: repartidores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS repartidores (
            id_repartidor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre        TEXT NOT NULL,
            email         TEXT NOT NULL
        )
    """)

    # TABLA: zonas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS zonas (
            id_zona       INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_zona   TEXT NOT NULL,
            tarifa_por_kg REAL NOT NULL
        )
    """)

    # TABLA: envios
    # Claves foráneas hacia repartidores y zonas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS envios (
            id_envio       INTEGER PRIMARY KEY AUTOINCREMENT,
            id_repartidor  INTEGER NOT NULL,
            id_zona        INTEGER NOT NULL,
            peso_kg        REAL NOT NULL,
            fecha_envio    TEXT NOT NULL,
            FOREIGN KEY (id_repartidor) REFERENCES repartidores(id_repartidor),
            FOREIGN KEY (id_zona)       REFERENCES zonas(id_zona)
        )
    """)

    conn.commit()

    # ------------------------------------------------
    # SEEDERS - Insertar datos de prueba
    # ------------------------------------------------
    # Solo inserta si las tablas están vacías
    if cursor.execute("SELECT COUNT(*) FROM repartidores").fetchone()[0] == 0:
        _seed_repartidores(cursor)
        _seed_zonas(cursor)
        conn.commit()
        _seed_envios(cursor)
        conn.commit()
        print("✅ Base de datos inicializada con datos de prueba.")
    else:
        print("ℹ️  Base de datos ya contiene datos.")

    conn.close()


def _seed_repartidores(cursor):
    """Inserta 5 repartidores de ejemplo."""
    repartidores = [
        ("Andrés Morales",  "andres@logistica.com"),
        ("Camila Torres",   "camila@logistica.com"),
        ("Luis Herrera",    "luis@logistica.com"),
        ("Valentina Ríos",  "valentina@logistica.com"),
        ("Diego Paredes",   "diego@logistica.com"),
    ]
    cursor.executemany(
        "INSERT INTO repartidores (nombre, email) VALUES (?, ?)",
        repartidores
    )


def _seed_zonas(cursor):
    """Inserta 3 zonas con sus tarifas."""
    zonas = [
        ("Norte",  1.50),
        ("Sur",    2.00),
        ("Centro", 1.75),
    ]
    cursor.executemany(
        "INSERT INTO zonas (nombre_zona, tarifa_por_kg) VALUES (?, ?)",
        zonas
    )


def _seed_envios(cursor):
    """
    Inserta 18 envíos distribuidos entre diferentes
    repartidores, zonas, pesos y fechas.
    Formato fecha: YYYY-MM-DD
    """
    envios = [
        # (id_repartidor, id_zona, peso_kg, fecha_envio)
        (1, 1,  5.0, "2024-01-05"),   # Andrés - Norte
        (1, 2,  8.5, "2024-01-12"),   # Andrés - Sur
        (1, 1,  3.2, "2024-02-03"),   # Andrés - Norte
        (1, 3,  6.0, "2024-02-18"),   # Andrés - Centro
        (1, 2,  9.3, "2024-03-07"),   # Andrés - Sur

        (2, 2,  7.0, "2024-01-08"),   # Camila - Sur
        (2, 3,  4.5, "2024-01-25"),   # Camila - Centro
        (2, 1, 11.0, "2024-02-14"),   # Camila - Norte

        (3, 3,  6.5, "2024-01-10"),   # Luis - Centro
        (3, 1,  2.8, "2024-02-20"),   # Luis - Norte
        (3, 2, 13.0, "2024-03-01"),   # Luis - Sur
        (3, 3,  5.5, "2024-03-15"),   # Luis - Centro

        (4, 1,  4.0, "2024-01-15"),   # Valentina - Norte
        (4, 2,  8.0, "2024-02-10"),   # Valentina - Sur
        (4, 1,  7.5, "2024-03-20"),   # Valentina - Norte

        (5, 3,  3.0, "2024-01-22"),   # Diego - Centro
        (5, 2,  6.0, "2024-02-28"),   # Diego - Sur
        (5, 1, 10.0, "2024-03-10"),   # Diego - Norte
    ]
    cursor.executemany(
        """INSERT INTO envios (id_repartidor, id_zona, peso_kg, fecha_envio)
           VALUES (?, ?, ?, ?)""",
        envios
    )
