

from flask import Blueprint, render_template, request
from datetime import datetime
from app.models.repartidor_model import RepartidorModel  # Importa el Modelo

# Blueprint: agrupa las rutas del módulo de envíos
envio_bp = Blueprint('envios', __name__)


@envio_bp.route('/', methods=['GET'])
def index():
    """
    RUTA: GET /
    Muestra la pantalla principal con el formulario vacío.
    No realiza ninguna consulta.
    Envía a la Vista: mensaje de bienvenida.
    """
    return render_template('index.html')  # Llama a la Vista


@envio_bp.route('/consultar', methods=['POST'])
def consultar():
    """
    RUTA: POST /consultar
    Flujo del Controlador:
      1. Recibe las fechas enviadas por el formulario (Vista).
      2. Valida que ambas fechas existan y sean correctas.
      3. Valida que fecha_inicio <= fecha_fin.
      4. Llama al Modelo para obtener los datos calculados.
      5. Envía los resultados a la Vista para renderizar.
    """

    fecha_inicio_str = request.form.get('fecha_inicio', '').strip()
    fecha_fin_str    = request.form.get('fecha_fin', '').strip()


    if not fecha_inicio_str or not fecha_fin_str:
        error = "⚠️ Ambas fechas son obligatorias."
        return render_template('index.html', error=error)

  
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        fecha_fin    = datetime.strptime(fecha_fin_str,    '%Y-%m-%d')
    except ValueError:
        error = "⚠️ Formato de fecha inválido. Use YYYY-MM-DD."
        return render_template('index.html', error=error)

    if fecha_inicio > fecha_fin:
        error = "⚠️ La fecha de inicio no puede ser mayor que la fecha fin."
        return render_template(
            'index.html', error=error,
            fecha_inicio=fecha_inicio_str,
            fecha_fin=fecha_fin_str
        )


    resultados = RepartidorModel.obtener_costos_por_repartidor(
        fecha_inicio_str, fecha_fin_str
    )


    total_envios    = sum(r['cantidad_envios'] for r in resultados)
    total_kg        = round(sum(r['total_kg'] for r in resultados), 2)
    total_costo     = round(sum(r['costo_total'] for r in resultados), 2)

 
    return render_template(
        'index.html',
        resultados=resultados,
        fecha_inicio=fecha_inicio_str,
        fecha_fin=fecha_fin_str,
        total_envios=total_envios,
        total_kg=total_kg,
        total_costo=total_costo
    )
