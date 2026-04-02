# Unidad IV · Lenguaje Estructurado de Consulta (SQL)

**Tiempo:** 20 horas  
**Objetivo:** Utilizar el lenguaje estructurado de consultas para la definición, construcción y manipulación de bases de datos.

---

## Resultado de aprendizaje de la unidad

Al finalizar la unidad podrás construir una base de datos funcional en SQL (DDL y DML), resolver consultas de complejidad creciente y automatizar operaciones desde Python con buenas prácticas.

## Ruta recomendada de trabajo

1. Implementa primero el esquema completo (DDL) y valida restricciones.
2. Inserta datos de prueba realistas (DML) para cubrir casos límite.
3. Resuelve consultas básicas y luego avanzadas (JOIN, subconsultas, CTE).
4. Crea vistas útiles para reportes recurrentes.
5. Ejecuta scripts SQL desde Python usando parámetros seguros.

## Práctica por niveles

| Nivel | Meta práctica |
|------|---------------|
| Básico | Crear tablas con PK/FK/CHECK y hacer CRUD correcto |
| Medio | Resolver consultas multi-tabla con JOIN y agregación |
| Reto | Diseñar consultas analíticas con CTE y ventanas |

## Hito de proyecto (Unidad IV)

Entregar para el caso Hospital:

- Script DDL completo ejecutable sin errores.
- Carga de datos de prueba coherentes.
- Implementación inicial de las consultas requeridas.
- Al menos 1 vista útil validada con datos reales.

## Autoevaluación rápida

- ¿Tu script puede ejecutarse de inicio a fin en una BD vacía?
- ¿Tus consultas críticas tienen resultados verificados?
- ¿Usas transacciones donde corresponde?
- ¿Tu código Python evita SQL injection con parámetros?

---

## 4.1 Sublenguaje de Definición de Datos (DDL)

El **DDL** define y modifica la estructura de la base de datos.

### CREATE TABLE

```sql
CREATE TABLE PRODUCTO (
    id_producto  INTEGER      PRIMARY KEY AUTOINCREMENT,
    codigo       VARCHAR(20)  NOT NULL UNIQUE,
    nombre       VARCHAR(150) NOT NULL,
    precio       DECIMAL(10,2) NOT NULL CHECK (precio > 0),
    stock        INTEGER      DEFAULT 0 CHECK (stock >= 0),
    id_categoria INTEGER,
    activo       INTEGER      DEFAULT 1,
    fecha_alta   DATE         DEFAULT (DATE('now')),
    FOREIGN KEY (id_categoria) REFERENCES CATEGORIA(id_categoria)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

### ALTER TABLE — modificar estructura existente

```sql
-- Agregar columna
ALTER TABLE PRODUCTO ADD COLUMN descripcion TEXT;

-- Renombrar columna (SQLite 3.25+)
ALTER TABLE PRODUCTO RENAME COLUMN activo TO habilitado;

-- Renombrar tabla
ALTER TABLE PRODUCTO RENAME TO ARTICULO;
```

### DROP TABLE — eliminar tabla

```sql
DROP TABLE IF EXISTS TABLA_TEMPORAL;
-- IF EXISTS evita error si la tabla no existe
```

### CREATE INDEX — mejorar rendimiento de consultas

```sql
-- Índice simple
CREATE INDEX idx_producto_nombre ON PRODUCTO(nombre);

-- Índice único (similar a UNIQUE constraint)
CREATE UNIQUE INDEX idx_producto_codigo ON PRODUCTO(codigo);

-- Índice compuesto
CREATE INDEX idx_inscripcion_ci_codigo ON INSCRIPCION(ci, codigo);
```

---

## 4.2 Sublenguaje de Manipulación de Datos (DML)

El **DML** manipula los datos almacenados.

### INSERT — insertar filas

```sql
-- Insertar una fila especificando columnas
INSERT INTO ESTUDIANTE (ci, nombre, apellido, id_carrera)
VALUES ('1234567', 'Pedro', 'Rojas', 1);

-- Insertar múltiples filas
INSERT INTO MATERIA (codigo, nombre, creditos, nivel) VALUES
    ('INF401', 'Análisis de Algoritmos', 5, 7),
    ('INF402', 'Inteligencia Artificial', 5, 8);

-- Insertar desde otra consulta
INSERT INTO ESTUDIANTE_BACKUP
SELECT * FROM ESTUDIANTE WHERE id_carrera = 1;
```

### SELECT — consultar datos

```sql
-- Sintaxis completa de SELECT:
SELECT  [DISTINCT] lista_columnas
FROM    tabla(s)
[JOIN   tabla ON condicion]
[WHERE  condicion_filtro]
[GROUP BY columna(s)]
[HAVING condicion_grupo]
[ORDER BY columna [ASC|DESC]]
[LIMIT  n OFFSET m];
```

### UPDATE — actualizar filas

```sql
-- Actualizar una fila específica
UPDATE INSCRIPCION
SET nota = 88.5
WHERE ci = '7654321' AND codigo = 'INF312' AND gestion = '2024-I';

-- Actualizar con cálculo
UPDATE PRODUCTO
SET precio = precio * 1.10   -- aumentar 10%
WHERE id_categoria = 2;

-- ¡CUIDADO! Sin WHERE actualiza TODAS las filas:
-- UPDATE ESTUDIANTE SET id_carrera = 1;  ← MUY PELIGROSO
```

### DELETE — eliminar filas

```sql
-- Eliminar fila específica
DELETE FROM INSCRIPCION
WHERE ci = '7654321' AND codigo = 'INF220';

-- Eliminar con subconsulta
DELETE FROM INSCRIPCION
WHERE ci IN (SELECT ci FROM ESTUDIANTE WHERE id_carrera = 3);

-- ¡CUIDADO! Sin WHERE elimina TODAS las filas:
-- DELETE FROM ESTUDIANTE;  ← MUY PELIGROSO
```

---

## 4.3 Sublenguaje de Control de Datos (DCL)

El **DCL** controla permisos y transacciones.

### Transacciones (ACID)

```sql
-- Una transacción agrupa operaciones en una unidad atómica
BEGIN TRANSACTION;
    UPDATE CUENTA SET saldo = saldo - 500 WHERE id = 1;  -- débito
    UPDATE CUENTA SET saldo = saldo + 500 WHERE id = 2;  -- crédito
COMMIT;   -- confirmar todos los cambios

-- Si algo falla:
-- ROLLBACK;   -- deshacer todos los cambios

-- Propiedades ACID:
-- A = Atomicidad  → todo o nada
-- C = Consistencia → la BD queda en estado válido
-- I = Aislamiento  → transacciones no se interfieren
-- D = Durabilidad  → cambios confirmados son permanentes
```

### Usuarios y Privilegios (PostgreSQL/MySQL)

```sql
-- GRANT — otorgar permisos
GRANT SELECT ON ESTUDIANTE TO 'alumno_user';
GRANT SELECT, INSERT ON INSCRIPCION TO 'secretaria_user';
GRANT ALL PRIVILEGES ON DATABASE universidad TO 'admin_user';

-- REVOKE — quitar permisos
REVOKE INSERT ON INSCRIPCION FROM 'alumno_user';

-- Crear usuario (PostgreSQL)
CREATE USER secretaria WITH PASSWORD 'pass_segura_123';

-- Crear rol
CREATE ROLE rol_docente;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO rol_docente;
GRANT rol_docente TO usuario_juan;
```

---

## 4.4 Consultas Básicas

```sql
-- 1. Todos los registros
SELECT * FROM ESTUDIANTE;

-- 2. Columnas específicas
SELECT ci, nombre, apellido FROM ESTUDIANTE;

-- 3. Con alias
SELECT ci AS "Carnet", nombre || ' ' || apellido AS "Nombre Completo"
FROM ESTUDIANTE;

-- 4. Con filtro simple
SELECT * FROM ESTUDIANTE WHERE id_carrera = 1;

-- 5. Con múltiples condiciones
SELECT * FROM INSCRIPCION
WHERE nota >= 51 AND gestion = '2023-I';

-- 6. LIKE — búsqueda por patrón
SELECT * FROM ESTUDIANTE WHERE nombre LIKE 'An%';  -- empieza con An
SELECT * FROM MATERIA   WHERE nombre LIKE '%Datos%'; -- contiene Datos

-- 7. BETWEEN — rango de valores
SELECT * FROM INSCRIPCION WHERE nota BETWEEN 51 AND 70;

-- 8. IN — lista de valores
SELECT * FROM MATERIA WHERE nivel IN (3, 4, 5);

-- 9. IS NULL / IS NOT NULL
SELECT * FROM INSCRIPCION WHERE nota IS NULL;  -- cursando actualmente

-- 10. ORDER BY
SELECT * FROM ESTUDIANTE ORDER BY apellido ASC, nombre ASC;

-- 11. LIMIT
SELECT * FROM INSCRIPCION ORDER BY nota DESC LIMIT 5;
```

---

## 4.5 Consultas Complejas

### JOINs

```sql
-- INNER JOIN: solo filas que tienen coincidencia en ambas tablas
SELECT e.nombre, m.nombre AS materia, i.nota
FROM INSCRIPCION i
INNER JOIN ESTUDIANTE e ON i.ci = e.ci
INNER JOIN MATERIA m    ON i.codigo = m.codigo;

-- LEFT JOIN: todos los de la izquierda, aunque no tengan coincidencia
SELECT e.nombre, COUNT(i.id_inscripcion) AS materias_cursadas
FROM ESTUDIANTE e
LEFT JOIN INSCRIPCION i ON e.ci = i.ci
GROUP BY e.ci, e.nombre;

-- Diferencia LEFT vs INNER:
-- INNER: solo estudiantes CON inscripciones
-- LEFT:  TODOS los estudiantes, incluso los sin inscripciones
```

### Subconsultas

```sql
-- Subconsulta en WHERE
SELECT nombre, apellido FROM ESTUDIANTE
WHERE ci IN (
    SELECT ci FROM INSCRIPCION WHERE nota >= 90
);

-- Subconsulta correlacionada
SELECT e.nombre,
       (SELECT COUNT(*) FROM INSCRIPCION i
        WHERE i.ci = e.ci AND i.nota >= 51) AS aprobadas
FROM ESTUDIANTE e;

-- Subconsulta en FROM (tabla derivada)
SELECT * FROM (
    SELECT ci, AVG(nota) AS promedio
    FROM INSCRIPCION
    WHERE nota IS NOT NULL
    GROUP BY ci
) AS promedios
WHERE promedio >= 75;

-- EXISTS
SELECT nombre FROM ESTUDIANTE e
WHERE EXISTS (
    SELECT 1 FROM INSCRIPCION i
    WHERE i.ci = e.ci AND i.nota >= 90
);
```

### Agregaciones y GROUP BY

```sql
-- GROUP BY + HAVING
SELECT codigo,
       COUNT(*)           AS total,
       AVG(nota)          AS promedio,
       MAX(nota)          AS maxima,
       MIN(nota)          AS minima
FROM INSCRIPCION
WHERE nota IS NOT NULL
GROUP BY codigo
HAVING AVG(nota) > 70
ORDER BY promedio DESC;

-- Funciones de texto
SELECT UPPER(nombre), LOWER(apellido),
       LENGTH(nombre)       AS largo,
       SUBSTR(nombre, 1, 3) AS iniciales
FROM ESTUDIANTE;

-- Funciones de fecha
SELECT nombre,
       fecha_nac,
       (strftime('%Y', 'now') - strftime('%Y', fecha_nac)) AS edad
FROM ESTUDIANTE;

-- CASE WHEN — condicional
SELECT nombre, nota,
       CASE
           WHEN nota >= 90 THEN 'Sobresaliente'
           WHEN nota >= 70 THEN 'Bueno'
           WHEN nota >= 51 THEN 'Aprobado'
           WHEN nota < 51  THEN 'Reprobado'
           ELSE                  'Sin nota'
       END AS calificacion
FROM INSCRIPCION i
JOIN ESTUDIANTE e ON i.ci = e.ci;
```

---

## 4.6 Vistas (VIEWS)

Una **vista** es una consulta almacenada que se comporta como una tabla virtual.

```sql
-- Crear vista
CREATE VIEW V_INSCRIPCIONES_DETALLE AS
SELECT
    e.ci,
    e.nombre || ' ' || e.apellido AS estudiante,
    c.nombre AS carrera,
    m.nombre AS materia,
    i.gestion,
    i.nota,
    CASE
        WHEN i.nota IS NULL THEN 'Cursando'
        WHEN i.nota >= 51   THEN 'Aprobado'
        ELSE                     'Reprobado'
    END AS estado
FROM INSCRIPCION i
JOIN ESTUDIANTE e ON i.ci     = e.ci
JOIN MATERIA    m ON i.codigo = m.codigo
JOIN CARRERA    c ON e.id_carrera = c.id_carrera;

-- Usar la vista igual que una tabla
SELECT * FROM V_INSCRIPCIONES_DETALLE WHERE estado = 'Aprobado';
SELECT estudiante, COUNT(*) AS aprobadas
FROM V_INSCRIPCIONES_DETALLE
WHERE estado = 'Aprobado'
GROUP BY estudiante;

-- Eliminar vista
DROP VIEW IF EXISTS V_INSCRIPCIONES_DETALLE;

-- Ventajas de las vistas:
-- ✓ Simplifica consultas complejas
-- ✓ Seguridad: el usuario ve solo lo que necesita
-- ✓ Independencia lógica: si cambia la estructura, se actualiza la vista
```

---

## 4.7 Usuarios y Privilegios

Ver sección 4.3 (DCL) para los comandos GRANT, REVOKE, CREATE USER.

```
Niveles de privilegio:
  SISTEMA  → CREATE DATABASE, CREATE USER
  BASE DE DATOS → CONNECT, CREATE TABLE
  TABLA    → SELECT, INSERT, UPDATE, DELETE
  COLUMNA  → SELECT(columna), UPDATE(columna)
  FILA     → mediante Row-Level Security (PostgreSQL)
```

---

## 4.8 Expresiones de Tabla Comunes (CTEs)

Una **CTE** (`WITH`) es una consulta nombrada que se define antes del `SELECT` principal. Mejora legibilidad y evita subconsultas repetidas.

```sql
-- CTE simple: promedio por carrera
WITH promedios_carrera AS (
    SELECT e.id_carrera,
           AVG(i.nota) AS promedio
    FROM INSCRIPCION i
    JOIN ESTUDIANTE e ON i.ci = e.ci
    WHERE i.nota IS NOT NULL
    GROUP BY e.id_carrera
)
SELECT c.nombre AS carrera,
       ROUND(p.promedio, 2) AS promedio_notas
FROM promedios_carrera p
JOIN CARRERA c ON p.id_carrera = c.id_carrera
ORDER BY promedio_notas DESC;

-- CTEs encadenados: porcentaje de aprobación por materia
WITH totales AS (
    SELECT codigo,
           COUNT(*)                                      AS total,
           SUM(CASE WHEN nota >= 51 THEN 1 ELSE 0 END)  AS aprobados
    FROM INSCRIPCION
    WHERE nota IS NOT NULL
    GROUP BY codigo
),
porcentajes AS (
    SELECT t.codigo,
           m.nombre,
           t.total,
           t.aprobados,
           ROUND(100.0 * t.aprobados / t.total, 1)      AS pct_aprobacion
    FROM totales t
    JOIN MATERIA m ON t.codigo = m.codigo
)
SELECT *
FROM porcentajes
WHERE pct_aprobacion < 60   -- materias con alto nivel de reprobación
ORDER BY pct_aprobacion;
```

> **CTE vs Subconsulta en FROM:** Un CTE corre una sola vez aunque se refiera múltiples veces. Una subconsulta en `FROM` también funciona pero se vuelve ilegible si es compleja. Preferir CTEs cuando la lógica ayuda a la comprensión.

---

## 4.9 Funciones de Ventana

Las **funciones de ventana** calculan un valor para cada fila tomando en cuenta un conjunto de filas relacionadas (la "ventana"), **sin colapsar el resultado** como haría `GROUP BY`.

```sql
-- Sintaxis general:
función() OVER (
    [PARTITION BY columna(s)]   -- divide en grupos (como GROUP BY sin colapsar)
    [ORDER BY columna(s)]       -- orden dentro de cada partición
    [ROWS/RANGE ...]            -- tamaño de la ventana (avanzado)
)
```

### Funciones de ranking

```sql
-- ROW_NUMBER: número de fila único, sin empates
SELECT ci, codigo, nota,
       ROW_NUMBER() OVER (PARTITION BY codigo ORDER BY nota DESC) AS fila
FROM INSCRIPCION WHERE nota IS NOT NULL;

-- RANK: igual ranking para empates, salta números (1,1,3)
SELECT ci, codigo, nota,
       RANK() OVER (PARTITION BY codigo ORDER BY nota DESC) AS puesto
FROM INSCRIPCION WHERE nota IS NOT NULL;

-- DENSE_RANK: igual ranking para empates, sin saltar (1,1,2)
SELECT ci, codigo, nota,
       DENSE_RANK() OVER (PARTITION BY codigo ORDER BY nota DESC) AS puesto
FROM INSCRIPCION WHERE nota IS NOT NULL;
```

### Funciones de agregación como ventana

```sql
-- Nota de cada estudiante vs promedio de su materia
SELECT
    e.nombre || ' ' || e.apellido                              AS estudiante,
    m.nombre                                                   AS materia,
    i.nota,
    ROUND(AVG(i.nota) OVER (PARTITION BY i.codigo), 1)        AS promedio_materia,
    ROUND(i.nota - AVG(i.nota) OVER (PARTITION BY i.codigo), 1) AS diferencia
FROM INSCRIPCION i
JOIN ESTUDIANTE e ON i.ci     = e.ci
JOIN MATERIA    m ON i.codigo = m.codigo
WHERE i.nota IS NOT NULL;
```

### Funciones LAG / LEAD

```sql
-- Comparar nota actual con la anterior del mismo estudiante (por fecha gestión)
SELECT ci, gestion, nota,
       LAG(nota)  OVER (PARTITION BY ci ORDER BY gestion) AS nota_anterior,
       nota - LAG(nota) OVER (PARTITION BY ci ORDER BY gestion) AS progreso
FROM INSCRIPCION
WHERE nota IS NOT NULL;
```

> **Nota de compatibilidad:** Las funciones de ventana requieren SQLite ≥ 3.25.0 (septiembre 2018). Verificar con `SELECT sqlite_version();`. PostgreSQL las soporta completamente desde la versión 8.4.

---

## 4.10 Diseño Físico — Índices

El **diseño físico** decide cómo se almacenan los datos para optimizar el rendimiento. El principal mecanismo son los **índices**.

### ¿Cómo funciona un índice?

```
Sin índice: buscar ci='7654321' en 1,000,000 de filas
  → Lectura secuencial: revisar fila por fila → O(n)

Con índice B-Tree en ci:
  → Búsqueda binaria en el árbol → O(log n) → miles de veces más rápido
```

### Cuándo crear un índice

```sql
-- ✓ Crear índice cuando:
--   · La columna aparece frecuentemente en WHERE
--   · La columna es FK (para acelerar JOINs)
--   · La columna aparece en ORDER BY de consultas frecuentes
--   · La columna tiene alta cardinalidad (muchos valores distintos)

CREATE INDEX idx_estudiante_apellido  ON ESTUDIANTE(apellido);
CREATE INDEX idx_inscripcion_ci       ON INSCRIPCION(ci);
CREATE INDEX idx_inscripcion_codigo   ON INSCRIPCION(codigo);
CREATE INDEX idx_inscripcion_gestion  ON INSCRIPCION(gestion);

-- Índice compuesto: útil cuando se filtra por ambas columnas juntas
CREATE INDEX idx_insc_ci_codigo ON INSCRIPCION(ci, codigo);

-- ✗ No crear índice cuando:
--   · La tabla tiene pocas filas (< 1,000 filas aprox.)
--   · La columna tiene baja cardinalidad (ej: sexo: solo 2 valores)
--   · La tabla recibe muchos INSERT/UPDATE (el índice se reconstruye)
```

### EXPLAIN QUERY PLAN (SQLite)

```sql
-- Ver el plan de ejecución ANTES de optimizar
EXPLAIN QUERY PLAN
SELECT * FROM INSCRIPCION WHERE ci = '7654321';
-- Sin índice: "SCAN INSCRIPCION"  → recorre toda la tabla

-- Crear el índice y verificar
CREATE INDEX idx_insc_ci ON INSCRIPCION(ci);
EXPLAIN QUERY PLAN
SELECT * FROM INSCRIPCION WHERE ci = '7654321';
-- Con índice: "SEARCH INSCRIPCION USING INDEX idx_insc_ci" → optimizado ✓
```

---

## 📁 Archivos de esta unidad

| Archivo | Descripción |
|---------|-------------|
| [`practica/01_ddl_dml.sql`](./practica/01_ddl_dml.sql) | DDL y DML completo — BD Farmacia |
| [`practica/02_consultas_avanzadas.sql`](./practica/02_consultas_avanzadas.sql) | JOINs, subconsultas, CTEs, funciones de ventana |
| [`practica/03_sql_python.py`](./practica/03_sql_python.py) | SQL desde Python con SQLite |
| [`practica/enunciados.md`](./practica/enunciados.md) | 14 ejercicios graduados de SQL |
| [`teoria/apuntes.md`](./teoria/apuntes.md) | Referencia rápida, ejercicios resueltos y errores comunes |
