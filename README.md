# 🚚 Sistema de Costos de Envíos por Repartidor
### Patrón MVC con Flask (Python) + SQLite

---

## 📐 Arquitectura MVC

```
┌─────────────────────────────────────────────────────┐
│                   USUARIO (Navegador)                │
└────────────────────┬────────────────────────────────┘
                     │ HTTP Request (GET / POST)
                     ▼
┌─────────────────────────────────────────────────────┐
│          CONTROLADOR (envio_controller.py)           │
│  • Recibe fechas del formulario                      │
│  • Valida los datos de entrada                       │
│  • Llama al Modelo                                   │
│  • Pasa resultados a la Vista                        │
└──────────────┬──────────────────────────┬───────────┘
               │ Consulta datos           │ Envía datos
               ▼                          ▼
┌──────────────────────┐    ┌─────────────────────────┐
│  MODELO              │    │  VISTA                  │
│ (repartidor_model.py)│    │ (index.html - Jinja2)   │
│  • Entidades BD      │    │  • Formulario fechas    │
│  • Relaciones SQL    │    │  • Tabla de resultados  │
│  • Cálculo costos    │    │  • KPIs de resumen      │
│  • Retorna lista     │    │  • Diseño responsive    │
└──────────────────────┘    └─────────────────────────┘
```

---

## 📁 Estructura del Proyecto

```
envios_mvc/
│
├── app.py                          ← Punto de entrada Flask
├── requirements.txt                ← Dependencias Python
├── README.md                       ← Este archivo
│
├── database/
│   ├── __init__.py
│   ├── db.py                       ← Conexión + init + seeders
│   ├── schema.sql                  ← Script SQL standalone
│   └── envios.db                   ← Base de datos SQLite (auto-generada)
│
└── app/
    ├── __init__.py
    │
    ├── models/
    │   ├── __init__.py
    │   └── repartidor_model.py     ← MODELO (M)
    │
    ├── controllers/
    │   ├── __init__.py
    │   └── envio_controller.py     ← CONTROLADOR (C)
    │
    └── views/
        ├── __init__.py
        └── templates/
            └── index.html          ← VISTA (V)
```

---

## ⚙️ Instalación y Ejecución

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes)

### Paso 1 – Clonar / descomprimir el proyecto
```bash
cd envios_mvc
```

### Paso 2 – Crear entorno virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Paso 3 – Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4 – Ejecutar la aplicación
```bash
python app.py
```

### Paso 5 – Abrir en el navegador
```
http://127.0.0.1:5000
```

---

## 🧪 Datos de Prueba

Los datos se insertan automáticamente al iniciar la app.

Para probar, usa el rango de fechas:
- **Fecha Inicio:** `2024-01-01`
- **Fecha Fin:** `2024-03-31`

### Repartidores:
| ID | Nombre           | Email                    |
|----|------------------|--------------------------|
| 1  | Andrés Morales   | andres@logistica.com     |
| 2  | Camila Torres    | camila@logistica.com     |
| 3  | Luis Herrera     | luis@logistica.com       |
| 4  | Valentina Ríos   | valentina@logistica.com  |
| 5  | Diego Paredes    | diego@logistica.com      |

### Zonas:
| ID | Zona   | Tarifa/Kg |
|----|--------|-----------|
| 1  | Norte  | $1.50     |
| 2  | Sur    | $2.00     |
| 3  | Centro | $1.75     |

---

## 🔑 Cómo se aplica el patrón MVC

### MODELO (`repartidor_model.py`)
- Define la entidad `Repartidor` con sus relaciones.
- Contiene la consulta SQL con JOIN entre `envios`, `repartidores` y `zonas`.
- Aplica la fórmula: `costo = peso_kg × tarifa_por_kg`.
- Retorna los datos al Controlador, sin saber cómo se mostrarán.

### CONTROLADOR (`envio_controller.py`)
- Recibe las fechas del formulario HTTP.
- Valida campos vacíos, formato de fecha y lógica del rango.
- Invoca al Modelo con las fechas validadas.
- Calcula totales (envíos, kg, costo).
- Llama a `render_template()` para pasar datos a la Vista.

### VISTA (`index.html`)
- Muestra el formulario de fechas al usuario.
- Usa Jinja2 (`{{ }}`, `{% %}`) para renderizar los datos.
- Presenta la tabla de resultados con diseño profesional.
- No contiene lógica de negocio; solo presentación.

---

## 📊 Fórmula de Cálculo

```
Para cada envío:
    costo_envio = peso_kg × tarifa_por_kg

Por repartidor:
    costo_total = Σ costo_envio (todos sus envíos en el rango)
```

---

*Sistema desarrollado con fines académicos — Patrón MVC*
