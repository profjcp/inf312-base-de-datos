# Unidad III — Ejercicios Prácticos

> **Archivo de referencia:** [`01_algebra_relacional.sql`](./01_algebra_relacional.sql)

---

## Esquema de referencia

Para todos los ejercicios, trabaja con el siguiente esquema:

```
CARRERA(id_carrera, nombre, duracion)
ESTUDIANTE(ci, nombre, apellido, fecha_nac, id_carrera→CARRERA)
MATERIA(codigo, nombre, creditos, nivel)
INSCRIPCION(id_insc, ci→ESTUDIANTE, codigo→MATERIA, gestion, nota)
DOCENTE(id_docente, nombre, apellido, especialidad)
DICTADO(id_dict, id_docente→DOCENTE, codigo→MATERIA, gestion, seccion)
```

---

## Ejercicio 1 — Conceptos del modelo relacional

**a)** Para la relación `ESTUDIANTE`, define:
- El grado (número de atributos)
- El dominio de cada atributo
- Al menos 2 restricciones de dominio representadas en SQL

**b)** ¿Cuál es la diferencia entre una **clave candidata**, una **clave primaria** y una **clave alternativa**? Da ejemplos con la tabla `ESTUDIANTE`.

**c)** ¿Por qué las tuplas no tienen orden en el modelo relacional? ¿Tiene alguna implicación práctica esta característica?

---

## Ejercicio 2 — Restricciones relacionales

**a)** Para cada una de las siguientes operaciones, indica qué restricción podría violarse y cómo manejarla:

| Operación | Restricción posible |
|-----------|---------------------|
| `INSERT INTO ESTUDIANTE VALUES ('7654321', 'Ana', 'García', NULL, 5)` | ? |
| `INSERT INTO INSCRIPCION VALUES (1, '9999999', 'INF312', '2024-I', NULL)` | ? |
| `INSERT INTO ESTUDIANTE VALUES ('7654321', 'Luis', 'López', '1995-03-10', 1)` | ? |
| `DELETE FROM ESTUDIANTE WHERE ci = '7654321'` | ? |
| `UPDATE MATERIA SET codigo = 'NEW001' WHERE codigo = 'INF312'` | ? |

**b)** Explica las 4 acciones posibles ante una violación de FK en DELETE (`RESTRICT`, `CASCADE`, `SET NULL`, `SET DEFAULT`). ¿Cuándo usarías cada una?

---

## Ejercicio 3 — Álgebra relacional: operaciones básicas

Dadas las tablas de referencia con los siguientes datos de ejemplo:

```
ESTUDIANTE:                    INSCRIPCION:
ci      | nombre | id_carrera  ci      | codigo | gestion  | nota
--------|--------|----------   --------|--------|----------|-----
111     | Ana    | 1           111     | INF312 | 2024-I   | 85
222     | Luis   | 2           111     | INF220 | 2023-II  | 70
333     | María  | 1           222     | INF312 | 2024-I   | NULL
444     | Pedro  | 3           333     | MAT101 | 2024-I   | 60
```

Expresa en álgebra relacional Y escribe el SQL equivalente:

**a)** Todos los estudiantes de la carrera 1  
**b)** El ci y nombre de todos los estudiantes  
**c)** Los estudiantes con nota mayor a 75  
**d)** El ci y nota de inscripciones de la gestión '2024-I'  
**e)** Nombre de estudiantes que tienen una inscripción (usa reunión ⋈)

---

## Ejercicio 4 — Álgebra relacional: operaciones de conjuntos

Dadas:
```
A = π ci (σ codigo='INF312' (INSCRIPCION))  -- estudiantes de INF312
B = π ci (σ codigo='INF220' (INSCRIPCION))  -- estudiantes de INF220
```

Expresa en álgebra relacional Y SQL:

**a)** Estudiantes que cursan INF312 **o** INF220  
**b)** Estudiantes que cursan **ambas** materias  
**c)** Estudiantes que cursan INF312 pero **no** INF220  
**d)** Estudiantes que cursan INF220 pero **no** INF312  

---

## Ejercicio 5 — Álgebra relacional: consultas complejas

Expresa en álgebra relacional Y SQL (con estructura comentada):

**a)** Nombre y nota de todos los estudiantes **aprobados** (nota ≥ 51) en INF312  
**b)** Nombre de los estudiantes que **nunca** han sido reprobados (nota < 51)  
**c)** Materias que NO han sido cursadas por ningún estudiante de la carrera 2  
**d)** El nombre del estudiante con la nota más alta en cada materia  
**e)** Docentes que dictan **todas** las materias de nivel 3 (división relacional)

---

## Ejercicio 6 — Integridad referencial en la práctica

**Escenario:** Se quiere eliminar la materia `INF312` de la tabla `MATERIA`.

**a)** ¿Qué pasaría si `INSCRIPCION` tiene `ON DELETE RESTRICT`?  
**b)** ¿Qué pasaría si `INSCRIPCION` tiene `ON DELETE CASCADE`?  
**c)** ¿Qué pasaría si `INSCRIPCION` tiene `ON DELETE SET NULL`?  
**d)** En un sistema universitario real, ¿cuál de las opciones anteriores sería más apropiada? Justifica.

---

## Ejercicio 7 — Diseño de esquema relacional

Para el siguiente enunciado, escribe el esquema relacional completo (notación con PK, FK, restricciones):

> Una empresa de transporte tiene **vehículos** (placa, marca, modelo, año, capacidad) y **conductores** (CI, nombre, licencia, categoría de licencia). Un conductor puede manejar varios vehículos a lo largo del tiempo, y un vehículo puede ser conducido por distintos conductores. Se registran **asignaciones** con fecha de inicio, fecha de fin y kilometraje recorrido. Cada vehículo pertenece a una **flota** (nombre, descripción, ciudad_base).

**a)** Escribe el esquema relacional completo  
**b)** Indica todas las dependencias funcionales de cada tabla  
**c)** Verifica que el esquema esté en 3FN

---

## Ejercicio 8 — Desafío: expresar SQL en álgebra relacional

Traduce las siguientes consultas SQL a expresiones de álgebra relacional:

```sql
-- a)
SELECT DISTINCT e.nombre
FROM ESTUDIANTE e
JOIN INSCRIPCION i ON e.ci = i.ci
WHERE i.nota >= 90 AND i.gestion = '2024-I';

-- b)
SELECT m.nombre, COUNT(i.id_insc) AS total_inscritos
FROM MATERIA m
LEFT JOIN INSCRIPCION i ON m.codigo = i.codigo
GROUP BY m.codigo, m.nombre
HAVING COUNT(i.id_insc) > 5;

-- c)
SELECT e.nombre
FROM ESTUDIANTE e
WHERE NOT EXISTS (
    SELECT 1 FROM INSCRIPCION i
    WHERE i.ci = e.ci AND i.nota < 51
);
```
