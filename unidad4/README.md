# Unidad IV · Lenguaje Estructurado de Consulta (SQL)

**Tiempo:** 20 horas  
**Objetivo:** Utilizar el lenguaje estructurado de consultas para la definición, construcción y manipulación de bases de datos.

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

## 📁 Archivos de esta unidad

| Archivo | Descripción |
|---------|-------------|
| [`practica/01_ddl_dml.sql`](./practica/01_ddl_dml.sql) | DDL y DML completo — BD Farmacia |
| [`practica/02_consultas_avanzadas.sql`](./practica/02_consultas_avanzadas.sql) | JOINs, subconsultas, vistas |
| [`practica/03_sql_python.py`](./practica/03_sql_python.py) | SQL desde Python con SQLite |
| [`practica/enunciados.md`](./practica/enunciados.md) | 20 ejercicios de SQL |
