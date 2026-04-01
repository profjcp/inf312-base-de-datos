-- =============================================================================
-- Unidad IV · Consultas avanzadas: JOINs, Subconsultas, CTEs, Window Functions
-- Base de datos: Universidad (BD Universitaria)
-- SGBD: SQLite 3.25+
-- =============================================================================

-- Ejecutar este script después de 01_ddl_dml.sql (usa la misma estructura)
-- O ejecutar el bloque de setup de abajo para crear los datos en memoria.

-- =============================================================================
-- SETUP: Esquema y datos de prueba
-- =============================================================================

CREATE TABLE IF NOT EXISTS CARRERA (
    id_carrera INTEGER PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS ESTUDIANTE (
    ci          VARCHAR(10)  PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    apellido    VARCHAR(100) NOT NULL,
    fecha_nac   DATE,
    id_carrera  INTEGER REFERENCES CARRERA(id_carrera)
);

CREATE TABLE IF NOT EXISTS MATERIA (
    codigo   VARCHAR(10)  PRIMARY KEY,
    nombre   VARCHAR(150) NOT NULL,
    creditos INTEGER,
    nivel    INTEGER
);

CREATE TABLE IF NOT EXISTS INSCRIPCION (
    id_insc  INTEGER PRIMARY KEY AUTOINCREMENT,
    ci       VARCHAR(10) REFERENCES ESTUDIANTE(ci),
    codigo   VARCHAR(10) REFERENCES MATERIA(codigo),
    gestion  VARCHAR(10),
    nota     DECIMAL(5,2)
);

INSERT OR IGNORE INTO CARRERA VALUES (1,'Sistemas'),(2,'Redes'),(3,'Computación');

INSERT OR IGNORE INTO MATERIA VALUES
    ('INF312','Base de Datos I',5,5),
    ('INF220','Programación II',4,3),
    ('MAT101','Matemáticas I',5,1),
    ('INF401','Redes I',4,6),
    ('INF500','Inteligencia Artificial',5,8);

INSERT OR IGNORE INTO ESTUDIANTE VALUES
    ('111','Ana',   'García',  '2000-03-15',1),
    ('222','Luis',  'Mamani',  '1999-07-22',1),
    ('333','María', 'López',   '2001-01-05',2),
    ('444','Pedro', 'Rojas',   '2000-09-30',3),
    ('555','Sofía', 'Vaca',    '2001-11-20',1);

INSERT OR IGNORE INTO INSCRIPCION(ci, codigo, gestion, nota) VALUES
    ('111','INF312','2024-I', 92),
    ('111','INF220','2023-II',78),
    ('111','MAT101','2023-I', 65),
    ('222','INF312','2024-I', 45),  -- reprobado
    ('222','INF220','2023-II',82),
    ('333','INF312','2024-I', 70),
    ('333','INF401','2024-I', NULL),-- cursando
    ('444','MAT101','2023-I', 88),
    ('444','INF220','2023-II',55),
    ('555','INF312','2024-I', 95),
    ('555','INF220','2023-II',NULL),-- cursando
    ('555','MAT101','2023-I', 72);

-- =============================================================================
-- SECCIÓN 1: JOINs
-- =============================================================================

-- 1.1 INNER JOIN: estudiante + materia + nota
SELECT  e.nombre || ' ' || e.apellido  AS estudiante,
        m.nombre                        AS materia,
        i.gestion,
        COALESCE(CAST(i.nota AS TEXT), 'cursando') AS nota
FROM INSCRIPCION i
INNER JOIN ESTUDIANTE e ON i.ci     = e.ci
INNER JOIN MATERIA    m ON i.codigo = m.codigo
ORDER BY e.apellido, m.nombre;

-- 1.2 LEFT JOIN: todos los estudiantes y cuántas materias tienen
SELECT  e.nombre || ' ' || e.apellido   AS estudiante,
        COUNT(i.id_insc)                AS inscripciones
FROM ESTUDIANTE e
LEFT JOIN INSCRIPCION i ON e.ci = i.ci
GROUP BY e.ci
ORDER BY inscripciones DESC;

-- 1.3 Materias que NADIE ha cursado (LEFT JOIN + IS NULL)
SELECT m.codigo, m.nombre
FROM MATERIA m
LEFT JOIN INSCRIPCION i ON m.codigo = i.codigo
WHERE i.ci IS NULL;

-- =============================================================================
-- SECCIÓN 2: Subconsultas
-- =============================================================================

-- 2.1 Subconsulta en WHERE: estudiantes que aprobaron INF312
SELECT nombre, apellido
FROM ESTUDIANTE
WHERE ci IN (
    SELECT ci FROM INSCRIPCION
    WHERE codigo = 'INF312' AND nota >= 51
);

-- 2.2 Subconsulta correlacionada: materias aprobadas por estudiante
SELECT  e.nombre,
        (SELECT COUNT(*)
         FROM INSCRIPCION i
         WHERE i.ci = e.ci AND i.nota >= 51) AS aprobadas,
        (SELECT COUNT(*)
         FROM INSCRIPCION i
         WHERE i.ci = e.ci AND i.nota < 51)  AS reprobadas
FROM ESTUDIANTE e;

-- 2.3 NOT EXISTS: estudiantes que nunca reprobaron
SELECT nombre, apellido
FROM ESTUDIANTE e
WHERE NOT EXISTS (
    SELECT 1 FROM INSCRIPCION i
    WHERE i.ci = e.ci AND i.nota IS NOT NULL AND i.nota < 51
);

-- 2.4 Materia con promedio más alto (subconsulta escalar)
SELECT codigo, nombre,
       (SELECT AVG(nota) FROM INSCRIPCION i2
        WHERE i2.codigo = m.codigo AND nota IS NOT NULL) AS promedio
FROM MATERIA m
ORDER BY promedio DESC
LIMIT 1;

-- =============================================================================
-- SECCIÓN 3: CTEs (WITH)
-- =============================================================================

-- 3.1 CTE simple: promedio por estudiante
WITH promedios AS (
    SELECT ci, AVG(nota) AS prom_general
    FROM INSCRIPCION
    WHERE nota IS NOT NULL
    GROUP BY ci
)
SELECT  e.nombre || ' ' || e.apellido AS estudiante,
        ROUND(p.prom_general, 1)       AS promedio
FROM promedios p
JOIN ESTUDIANTE e ON p.ci = e.ci
ORDER BY promedio DESC;

-- 3.2 CTEs encadenados: porcentaje de aprobación por materia
WITH totales AS (
    SELECT  codigo,
            COUNT(*)                                    AS total,
            SUM(CASE WHEN nota >= 51 THEN 1 ELSE 0 END) AS aprobados,
            SUM(CASE WHEN nota <  51 THEN 1 ELSE 0 END) AS reprobados
    FROM INSCRIPCION
    WHERE nota IS NOT NULL
    GROUP BY codigo
),
porcentajes AS (
    SELECT  t.codigo,
            m.nombre,
            t.total,
            t.aprobados,
            ROUND(100.0 * t.aprobados / t.total, 1) AS pct_aprobacion
    FROM totales t
    JOIN MATERIA m ON t.codigo = m.codigo
)
SELECT * FROM porcentajes ORDER BY pct_aprobacion ASC;

-- 3.3 CTE con ranking: top 3 estudiantes por promedio por carrera
WITH prom_est AS (
    SELECT  e.ci, e.nombre, e.apellido, e.id_carrera,
            AVG(i.nota) AS promedio
    FROM ESTUDIANTE e
    JOIN INSCRIPCION i ON e.ci = i.ci
    WHERE i.nota IS NOT NULL
    GROUP BY e.ci
)
SELECT  c.nombre AS carrera,
        p.nombre, p.apellido,
        ROUND(p.promedio, 1) AS promedio
FROM prom_est p
JOIN CARRERA c ON p.id_carrera = c.id_carrera
WHERE (
    SELECT COUNT(*) FROM prom_est p2
    WHERE p2.id_carrera = p.id_carrera AND p2.promedio > p.promedio
) < 3
ORDER BY c.nombre, p.promedio DESC;

-- =============================================================================
-- SECCIÓN 4: Funciones de ventana (requiere SQLite >= 3.25)
-- =============================================================================

-- 4.1 ROW_NUMBER: ranking por materia
SELECT  ci, codigo, nota,
        ROW_NUMBER() OVER (PARTITION BY codigo ORDER BY nota DESC) AS posicion
FROM INSCRIPCION
WHERE nota IS NOT NULL;

-- 4.2 RANK vs DENSE_RANK con empates
SELECT  ci, codigo, nota,
        RANK()       OVER (PARTITION BY codigo ORDER BY nota DESC) AS rank,
        DENSE_RANK() OVER (PARTITION BY codigo ORDER BY nota DESC) AS dense_rank
FROM INSCRIPCION
WHERE nota IS NOT NULL;

-- 4.3 AVG() OVER: nota individual vs promedio de la materia
SELECT  e.nombre || ' ' || e.apellido                          AS estudiante,
        m.nombre                                               AS materia,
        i.nota,
        ROUND(AVG(i.nota) OVER (PARTITION BY i.codigo), 1)    AS prom_materia,
        ROUND(i.nota - AVG(i.nota) OVER(PARTITION BY i.codigo), 1) AS diferencia
FROM INSCRIPCION i
JOIN ESTUDIANTE e ON i.ci     = e.ci
JOIN MATERIA    m ON i.codigo = m.codigo
WHERE i.nota IS NOT NULL
ORDER BY materia, diferencia DESC;

-- 4.4 LAG: comparar nota actual con gestión anterior del mismo estudiante
SELECT  ci,
        gestion,
        nota,
        LAG(nota) OVER (PARTITION BY ci ORDER BY gestion) AS nota_anterior,
        CASE
            WHEN LAG(nota) OVER (PARTITION BY ci ORDER BY gestion) IS NULL THEN 'primera vez'
            WHEN nota > LAG(nota) OVER (PARTITION BY ci ORDER BY gestion) THEN 'mejora'
            WHEN nota < LAG(nota) OVER (PARTITION BY ci ORDER BY gestion) THEN 'baja'
            ELSE 'igual'
        END AS tendencia
FROM INSCRIPCION
WHERE nota IS NOT NULL
ORDER BY ci, gestion;

-- =============================================================================
-- SECCIÓN 5: Vistas avanzadas
-- =============================================================================

-- 5.1 Vista completa de calificaciones
CREATE VIEW IF NOT EXISTS V_CALIFICACIONES AS
SELECT  e.ci,
        e.nombre || ' ' || e.apellido   AS estudiante,
        c.nombre                         AS carrera,
        m.nombre                         AS materia,
        i.gestion,
        i.nota,
        CASE
            WHEN i.nota IS NULL  THEN 'Cursando'
            WHEN i.nota >= 51    THEN 'Aprobado'
            ELSE                      'Reprobado'
        END AS estado
FROM INSCRIPCION i
JOIN ESTUDIANTE e  ON i.ci            = e.ci
JOIN MATERIA    m  ON i.codigo        = m.codigo
JOIN CARRERA    c  ON e.id_carrera    = c.id_carrera;

-- Usar la vista
SELECT * FROM V_CALIFICACIONES WHERE estado = 'Reprobado';

-- 5.2 Vista de resumen por estudiante
CREATE VIEW IF NOT EXISTS V_RESUMEN_ESTUDIANTE AS
SELECT  e.ci,
        e.nombre || ' ' || e.apellido  AS estudiante,
        c.nombre                        AS carrera,
        COUNT(i.id_insc)                AS total_materias,
        SUM(CASE WHEN i.nota >= 51 THEN 1 ELSE 0 END) AS aprobadas,
        SUM(CASE WHEN i.nota <  51 THEN 1 ELSE 0 END) AS reprobadas,
        ROUND(AVG(CASE WHEN i.nota IS NOT NULL THEN i.nota END), 1) AS promedio
FROM ESTUDIANTE e
LEFT JOIN INSCRIPCION i ON e.ci         = i.ci
LEFT JOIN CARRERA     c ON e.id_carrera = c.id_carrera
GROUP BY e.ci, e.nombre, e.apellido, c.nombre;

SELECT * FROM V_RESUMEN_ESTUDIANTE ORDER BY promedio DESC;
