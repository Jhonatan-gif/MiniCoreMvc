-- ====================================================
-- SCRIPT SQL - Sistema de Costos de Envíos
-- Base de datos: SQLite (compatible con MySQL/PostgreSQL
--                cambiando AUTOINCREMENT por AUTO_INCREMENT)
-- ====================================================

-- Eliminar tablas si existen (para reiniciar)
DROP TABLE IF EXISTS envios;
DROP TABLE IF EXISTS repartidores;
DROP TABLE IF EXISTS zonas;

-- =====================
-- TABLA: repartidores
-- =====================
CREATE TABLE repartidores (
    id_repartidor INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre        TEXT    NOT NULL,
    email         TEXT    NOT NULL
);

-- =====================
-- TABLA: zonas
-- =====================
CREATE TABLE zonas (
    id_zona       INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_zona   TEXT    NOT NULL,
    tarifa_por_kg REAL    NOT NULL
);

-- =====================
-- TABLA: envios
-- Claves foráneas: id_repartidor → repartidores
--                  id_zona       → zonas
-- =====================
CREATE TABLE envios (
    id_envio      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_repartidor INTEGER NOT NULL,
    id_zona       INTEGER NOT NULL,
    peso_kg       REAL    NOT NULL,
    fecha_envio   TEXT    NOT NULL,
    FOREIGN KEY (id_repartidor) REFERENCES repartidores(id_repartidor),
    FOREIGN KEY (id_zona)       REFERENCES zonas(id_zona)
);

-- =====================
-- SEEDERS - Datos de prueba
-- =====================

-- Repartidores
INSERT INTO repartidores (nombre, email) VALUES
    ('Andrés Morales',  'andres@logistica.com'),
    ('Camila Torres',   'camila@logistica.com'),
    ('Luis Herrera',    'luis@logistica.com'),
    ('Valentina Ríos',  'valentina@logistica.com'),
    ('Diego Paredes',   'diego@logistica.com');

-- Zonas
INSERT INTO zonas (nombre_zona, tarifa_por_kg) VALUES
    ('Norte',  1.50),
    ('Sur',    2.00),
    ('Centro', 1.75);

-- Envíos (18 registros)
-- Fórmula: costo = peso_kg × tarifa_por_kg
INSERT INTO envios (id_repartidor, id_zona, peso_kg, fecha_envio) VALUES
    (1, 1,  5.0, '2024-01-05'),   -- Andrés, Norte,  $7.50
    (1, 2,  8.5, '2024-01-12'),   -- Andrés, Sur,    $17.00
    (1, 1,  3.2, '2024-02-03'),   -- Andrés, Norte,  $4.80
    (1, 3,  6.0, '2024-02-18'),   -- Andrés, Centro, $10.50
    (1, 2,  9.3, '2024-03-07'),   -- Andrés, Sur,    $18.60
    (2, 2,  7.0, '2024-01-08'),   -- Camila, Sur,    $14.00
    (2, 3,  4.5, '2024-01-25'),   -- Camila, Centro, $7.875
    (2, 1, 11.0, '2024-02-14'),   -- Camila, Norte,  $16.50
    (3, 3,  6.5, '2024-01-10'),   -- Luis,   Centro, $11.375
    (3, 1,  2.8, '2024-02-20'),   -- Luis,   Norte,  $4.20
    (3, 2, 13.0, '2024-03-01'),   -- Luis,   Sur,    $26.00
    (3, 3,  5.5, '2024-03-15'),   -- Luis,   Centro, $9.625
    (4, 1,  4.0, '2024-01-15'),   -- Valentina, Norte,  $6.00
    (4, 2,  8.0, '2024-02-10'),   -- Valentina, Sur,    $16.00
    (4, 1,  7.5, '2024-03-20'),   -- Valentina, Norte,  $11.25
    (5, 3,  3.0, '2024-01-22'),   -- Diego, Centro, $5.25
    (5, 2,  6.0, '2024-02-28'),   -- Diego, Sur,    $12.00
    (5, 1, 10.0, '2024-03-10');   -- Diego, Norte,  $15.00

-- =====================
-- CONSULTA PRINCIPAL
-- (equivalente a la del Modelo en Python)
-- =====================
/*
SELECT
    r.nombre                             AS nombre_repartidor,
    COUNT(e.id_envio)                    AS cantidad_envios,
    ROUND(SUM(e.peso_kg), 2)             AS total_kg,
    GROUP_CONCAT(DISTINCT z.nombre_zona) AS zonas,
    ROUND(SUM(e.peso_kg * z.tarifa_por_kg), 2) AS costo_total
FROM envios e
INNER JOIN repartidores r ON e.id_repartidor = r.id_repartidor
INNER JOIN zonas z        ON e.id_zona        = z.id_zona
WHERE e.fecha_envio BETWEEN '2024-01-01' AND '2024-03-31'
GROUP BY r.id_repartidor, r.nombre
ORDER BY costo_total DESC;
*/
