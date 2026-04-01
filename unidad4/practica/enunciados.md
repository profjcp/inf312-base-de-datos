# Unidad IV — Ejercicios Prácticos

> **Archivos de referencia:** [`01_ddl_dml.sql`](./01_ddl_dml.sql) · [`02_consultas_avanzadas.sql`](./02_consultas_avanzadas.sql) · [`03_sql_python.py`](./03_sql_python.py)

---

## Esquema de referencia

```sql
CARRERA(id_carrera PK, nombre, duracion)
ESTUDIANTE(ci PK, nombre, apellido, fecha_nac, email UNIQUE, id_carrera FK)
MATERIA(codigo PK, nombre, creditos, nivel)
INSCRIPCION(id_insc PK, ci FK, codigo FK, gestion, nota)
DOCENTE(id_docente PK, nombre, apellido, especialidad, email)
DICTADO(id_dict PK, id_docente FK, codigo FK, gestion, seccion)
```

---

## PARTE 1 — DDL

### Ejercicio 1 — CREATE TABLE

Crea las tablas del esquema con las siguientes restricciones:
- `nota` debe estar entre 0 y 100
- `creditos` debe ser positivo
- `nivel` debe estar entre 1 y 10
- `duracion` en años, entre 3 y 6
- `email` debe contener '@'
- `fecha_nac` no puede ser en el futuro

Incluye `ON DELETE` y `ON UPDATE` apropiados para todas las FK.

---

### Ejercicio 2 — ALTER TABLE

Partiendo de las tablas creadas:

**a)** Agrega la columna `activo` (INTEGER DEFAULT 1) a `ESTUDIANTE`  
**b)** Agrega la columna `fecha_alta` (DATE) a `ESTUDIANTE`  
**c)** Renombra la columna `duracion` de `CARRERA` a `duracion_anios`  
**d)** Crea un índice compuesto en `INSCRIPCION(ci, codigo)`  
**e)** Crea un índice en `ESTUDIANTE(apellido)` para búsquedas frecuentes

---

### Ejercicio 3 — Diseño físico básico

Para el siguiente caso de uso identifica qué índices crearías y justifica:

> La aplicación más frecuente es: buscar estudiantes por apellido, listar todas las inscripciones de un semestre dado, y obtener el promedio de notas por materia.

**a)** Escribe los `CREATE INDEX` correspondientes  
**b)** ¿Qué consulta se beneficia más de un índice? ¿Por qué los índices no deben crearse en exceso?  
**c)** Ejecuta `EXPLAIN QUERY PLAN` en SQLite para una consulta con y sin índice, y compara el resultado

---

## PARTE 2 — DML

### Ejercicio 4 — INSERT

**a)** Inserta 3 carreras, 5 estudiantes, 4 materias y 8 inscripciones con datos coherentes  
**b)** Inserta un estudiante sin email (debe permitirse). Intenta insertar uno con CI duplicado. ¿Qué error obtienes?  
**c)** Usando `INSERT INTO ... SELECT`, crea una copia de backup de los estudiantes de la carrera 1 en una tabla `ESTUDIANTE_BACKUP` (créala primero con `CREATE TABLE ... AS SELECT`)

---

### Ejercicio 5 — UPDATE y DELETE

**a)** Sube 5 puntos a todos los estudiantes con nota entre 45 y 50 (para aprobar)  
**b)** Marca como inactivo (`activo = 0`) a todos los estudiantes sin inscripciones  
**c)** Elimina todas las inscripciones de la gestión '2020-I'  
**d)** Escribe un UPDATE peligroso (sin WHERE) en un comentario y explica qué haría

---

## PARTE 3 — Consultas

### Ejercicio 6 — Consultas básicas

Escribe SQL para:

1. Listar todos los estudiantes ordenados por apellido y nombre
2. Mostrar código y nombre de materias del nivel 3 o superior
3. Contar cuántos estudiantes hay por carrera
4. Mostrar notas entre 60 y 80 de la gestión '2024-I'
5. Listar estudiantes cuyo apellido empiece con 'M'
6. Mostrar la nota máxima, mínima y promedio de INF312

---

### Ejercicio 7 — JOINs

Escribe SQL usando **solo JOINs explícitos** (`INNER JOIN`, `LEFT JOIN`):

1. Nombre completo del estudiante + nombre de la materia + nota, para todas las inscripciones
2. Todos los estudiantes y cuántas materias están cursando (incluyendo los que no tienen ninguna)
3. Materias que nunca han sido cursadas (usa LEFT JOIN + IS NULL)
4. Nombre del docente + materia que dicta + sección, para la gestión '2024-I'
5. Estudiante + carrera + total de créditos acumulados (solo materias aprobadas con nota ≥ 51)

---

### Ejercicio 8 — Subconsultas

Resuelve **sin usar JOIN**, solo con subconsultas:

1. Nombres de estudiantes que aprobaron INF312 (nota ≥ 51)
2. Materias cuyo promedio de notas es mayor al promedio general
3. Estudiantes que están inscritos en más materias que el promedio de inscripciones por estudiante
4. El nombre del estudiante con la nota más alta de todo el sistema
5. Docentes que NO dictan ninguna materia en '2024-I' (usa `NOT EXISTS`)

---

### Ejercicio 9 — CTEs y consultas anidadas

Utiliza `WITH` (Common Table Expressions) para:

```sql
-- a) Calcular el promedio por estudiante, luego filtrar los que tienen promedio >= 70
WITH promedios AS (
    SELECT ci, AVG(nota) AS prom
    FROM INSCRIPCION
    WHERE nota IS NOT NULL
    GROUP BY ci
)
SELECT e.nombre, e.apellido, p.prom
FROM promedios p
JOIN ESTUDIANTE e ON p.ci = e.ci
WHERE p.prom >= 70
ORDER BY p.prom DESC;
```

**b)** Usa un CTE para calcular el ranking de materias por promedio de notas  
**c)** Usa CTEs encadenados: primero calcular aprobados por materia, luego el porcentaje de aprobación  
**d)** ¿En qué se diferencia un CTE de una subconsulta en `FROM`? ¿Cuándo preferirías cada uno?

---

### Ejercicio 10 — Funciones de ventana *(avanzado)*

Las **funciones de ventana** calculan valores sobre un conjunto de filas relacionadas sin colapsar el resultado.

```sql
-- ROW_NUMBER: numerar filas dentro de cada materia por nota descendente
SELECT
    ci,
    codigo,
    nota,
    ROW_NUMBER() OVER (PARTITION BY codigo ORDER BY nota DESC) AS ranking
FROM INSCRIPCION
WHERE nota IS NOT NULL;
```

**a)** Usa `RANK()` para obtener el puesto de cada estudiante dentro de su carrera  
**b)** Usa `AVG() OVER (PARTITION BY codigo)` para mostrar la nota de cada estudiante junto al promedio de su materia  
**c)** Usa `LAG()` para calcular la diferencia de nota entre inscripciones consecutivas de un estudiante  
**d)** ¿Qué diferencia hay entre `RANK()` y `DENSE_RANK()` cuando hay empates?

> **Nota SQLite:** Las funciones de ventana están disponibles desde SQLite 3.25 (2018). Verifica tu versión con `SELECT sqlite_version();`

---

### Ejercicio 11 — Vistas

**a)** Crea una vista `V_CALIFICACIONES` que muestre: ci, nombre completo del estudiante, carrera, materia, gestión, nota y estado ('Aprobado'/'Reprobado'/'Cursando')

**b)** Crea una vista `V_RESUMEN_ESTUDIANTE` que muestre por estudiante: total de materias cursadas, aprobadas, reprobadas y promedio general

**c)** Usa la vista `V_CALIFICACIONES` para encontrar los 3 estudiantes con mejor promedio de la carrera 'Sistemas'

**d)** ¿Puede hacerse INSERT sobre una vista? ¿En qué condiciones?

---

## PARTE 4 — Transacciones y control

### Ejercicio 12 — Transacciones ACID

```sql
-- Escenario: transferencia bancaria
-- Tabla: CUENTA(id, titular, saldo)
```

**a)** Escribe una transacción que transfiera $500 de la cuenta 1 a la cuenta 2, asegurando atomicidad  
**b)** ¿Qué pasa si hay un error entre el débito y el crédito **sin** transacción?  
**c)** ¿Qué pasa si hay un error entre el débito y el crédito **con** transacción y `ROLLBACK`?  
**d)** Explica con tus palabras cada propiedad ACID usando el ejemplo de la transferencia bancaria

---

### Ejercicio 13 — SQL desde Python

Estudia el archivo [`03_sql_python.py`](./03_sql_python.py) y:

**a)** ¿Qué es un cursor? ¿Por qué se usa `?` como placeholder en lugar de formatear el string?  
**b)** ¿Por qué es importante usar `conn.commit()` y en qué casos no es necesario?  
**c)** Escribe una función Python `buscar_estudiante(ci)` que reciba un CI y retorne todos los datos del estudiante usando la conexión SQLite  
**d)** ¿Qué vulnerabilidad de seguridad evitas al usar parámetros en lugar de concatenar strings? (Pista: SQL Injection)

---

## Ejercicio 14 — Desafío integrador

Diseña y ejecuta completamente una BD para una **biblioteca**:

1. **DDL:** Crea las tablas (LIBRO, AUTOR, EDITORIAL, SOCIO, PRESTAMO, EJEMPLAR) con todas las restricciones
2. **DML:** Inserta datos suficientes (mínimo 10 libros, 20 socios, 30 préstamos)
3. **Consultas:** Implementa las siguientes 8 consultas:
   - Libros más prestados (TOP 5)
   - Socios con préstamos vencidos (fecha_devolucion_esperada < hoy y no devuelto)
   - Libros disponibles (con ejemplares sin préstamo activo)
   - Promedio de días de préstamo por categoría
   - Socios que nunca han hecho un préstamo
   - Autor con más libros en el catálogo
   - Vista `V_PRESTAMOS_ACTIVOS` con todos los préstamos en curso
   - Transacción: registrar devolución de un libro (actualizar préstamo + stock disponible)
