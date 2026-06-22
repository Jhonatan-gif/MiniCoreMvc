

from database.db import get_connection


class RepartidorModel:
 
    @staticmethod
    def obtener_costos_por_repartidor(fecha_inicio: str, fecha_fin: str) -> list:
    
        conn = get_connection()
        cursor = conn.cursor()

       
        query = """
            SELECT
                r.nombre                            AS nombre_repartidor,
                COUNT(e.id_envio)                   AS cantidad_envios,
                ROUND(SUM(e.peso_kg), 2)            AS total_kg,
                GROUP_CONCAT(DISTINCT z.nombre_zona) AS zonas,
                GROUP_CONCAT(DISTINCT
                    z.nombre_zona || ': $' ||
                    CAST(z.tarifa_por_kg AS TEXT)
                )                                   AS tarifas,
                ROUND(
                    SUM(e.peso_kg * z.tarifa_por_kg), 2
                )                                   AS costo_total
            FROM envios e
            INNER JOIN repartidores r ON e.id_repartidor = r.id_repartidor
            INNER JOIN zonas z        ON e.id_zona        = z.id_zona
            WHERE e.fecha_envio BETWEEN ? AND ?
            GROUP BY r.id_repartidor, r.nombre
            ORDER BY costo_total DESC
        """

        # Ejecutar con parámetros (evita SQL Injection)
        cursor.execute(query, (fecha_inicio, fecha_fin))
        rows = cursor.fetchall()
        conn.close()

        # Convertir resultados a lista de diccionarios
        return [dict(row) for row in rows]
