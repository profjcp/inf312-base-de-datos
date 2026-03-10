-- practica/01_algebra_relacional.sql
-- Unidad III: Álgebra Relacional → SQL
-- =====================================
-- Cada bloque muestra: operación formal + su equivalente SQL

-- Ejecutar con: sqlite3 universidad_bd1.db < 01_algebra_relacional.sql
-- (usar la BD creada en la Unidad I)

-- ============================================================
-- SELECCIÓN (σ) — filtra FILAS
-- ============================================================
-- σ nota >= 51 (INSCRIPCION)

SELECT * FROM INSCRIPCION
WHERE nota >= 51;

-- σ nota >= 51 AND gestion = '2023-I' (INSCRIPCION)
SELECT * FROM INSCRIPCION
WHERE nota >= 51 AND gestion = '2023-I';

-- ============================================================
-- PROYECCIÓN (π) — selecciona COLUMNAS
-- ============================================================
-- π ci, nombre, apellido (ESTUDIANTE)

SELECT DISTINCT ci, nombre, apellido FROM ESTUDIANTE;

-- ============================================================
-- SELECCIÓN + PROYECCIÓN combinadas
-- ============================================================
-- π nombre, apellido (σ id_carrera = 1 (ESTUDIANTE))

SELECT nombre, apellido
FROM ESTUDIANTE
WHERE id_carrera = 1;

-- ============================================================
-- REUNIÓN (JOIN) — combina relaciones
-- ============================================================
-- ESTUDIANTE ⋈(ci) INSCRIPCION ⋈(codigo) MATERIA

SELECT e.nombre || ' ' || e.apellido AS estudiante,
       m.nombre  AS materia,
       i.gestion,
       i.nota
FROM INSCRIPCION i
JOIN ESTUDIANTE e ON i.ci = e.ci
JOIN MATERIA    m ON i.codigo = m.codigo
ORDER BY e.apellido, i.gestion;

-- ============================================================
-- UNIÓN (∪)
-- ============================================================
-- Estudiantes que cursaron INF220 O INF312

SELECT ci FROM INSCRIPCION WHERE codigo = 'INF220'
UNION
SELECT ci FROM INSCRIPCION WHERE codigo = 'INF312';

-- Con nombres completos:
SELECT DISTINCT e.ci, e.nombre || ' ' || e.apellido AS estudiante,
       'Cursó INF220 o INF312' AS descripcion
FROM ESTUDIANTE e
WHERE e.ci IN (
    SELECT ci FROM INSCRIPCION WHERE codigo = 'INF220'
    UNION
    SELECT ci FROM INSCRIPCION WHERE codigo = 'INF312'
);

-- ============================================================
-- INTERSECCIÓN (∩)
-- ============================================================
-- Estudiantes que cursaron TANTO INF220 COMO INF312

SELECT ci FROM INSCRIPCION WHERE codigo = 'INF220'
INTERSECT
SELECT ci FROM INSCRIPCION WHERE codigo = 'INF312';

-- ============================================================
-- DIFERENCIA (-)
-- ============================================================
-- Estudiantes que cursaron INF220 pero NO INF312

SELECT ci FROM INSCRIPCION WHERE codigo = 'INF220'
EXCEPT
SELECT ci FROM INSCRIPCION WHERE codigo = 'INF312';

-- Con nombre completo:
SELECT e.ci, e.nombre || ' ' || e.apellido AS estudiante
FROM ESTUDIANTE e
WHERE e.ci IN (
    SELECT ci FROM INSCRIPCION WHERE codigo = 'INF220'
    EXCEPT
    SELECT ci FROM INSCRIPCION WHERE codigo = 'INF312'
);

-- ============================================================
-- DIVISIÓN (÷)
-- ============================================================
-- Estudiantes que cursaron TODAS las materias de nivel 3 o 4

-- Primero: ¿cuáles son esas materias?
-- SELECT codigo FROM MATERIA WHERE nivel IN (3, 4) → {INF220, INF310}

-- División: estudiantes que cursaron INF220 Y INF310
SELECT DISTINCT ci
FROM INSCRIPCION i1
WHERE NOT EXISTS (
    SELECT codigo
    FROM MATERIA
    WHERE nivel IN (3, 4)
    AND codigo NOT IN (
        SELECT codigo
        FROM INSCRIPCION i2
        WHERE i2.ci = i1.ci
    )
);

-- ============================================================
-- FUNCIONES DE AGREGACIÓN (extensión del álgebra relacional)
-- ============================================================

-- Promedio de notas por materia
SELECT m.nombre        AS materia,
       COUNT(i.ci)     AS total_inscritos,
       ROUND(AVG(i.nota), 2) AS promedio,
       MAX(i.nota)     AS nota_maxima,
       MIN(i.nota)     AS nota_minima,
       SUM(CASE WHEN i.nota >= 51 THEN 1 ELSE 0 END) AS aprobados
FROM MATERIA m
LEFT JOIN INSCRIPCION i ON m.codigo = i.codigo
WHERE i.nota IS NOT NULL
GROUP BY m.nombre
HAVING COUNT(i.ci) > 0
ORDER BY promedio DESC;

-- ============================================================
-- PRODUCTO CARTESIANO (para DEMOSTRAR por qué no usarlo solo)
-- ============================================================
-- R × S sin condición: genera combinaciones sin sentido

-- Con 3 carreras × 3 materias = 9 combinaciones (poco útiles)
SELECT c.nombre AS carrera, m.nombre AS materia
FROM CARRERA c, MATERIA m
ORDER BY c.nombre, m.nombre;
-- → Esto no tiene significado real, ¡siempre usar JOIN con condición!

-- ============================================================
-- INTEGRIDAD REFERENCIAL — demostrar violaciones
-- ============================================================

-- Intentar insertar con FK inexistente (debe fallar si FK activas)
-- INSERT INTO INSCRIPCION(ci, codigo, gestion)
-- VALUES ('9999999', 'INF312', '2024-I');
-- Error: FOREIGN KEY constraint failed

-- Ver las restricciones activas:
PRAGMA foreign_key_list(INSCRIPCION);
