# Unidad I — Ejercicios Prácticos

> **Archivo de referencia:** [`01_intro.sql`](./01_intro.sql) · [`01_intro_sqlite.py`](./01_intro_sqlite.py)

---

## Ejercicio 1 — Identificación de componentes SGBD

Dado el siguiente contexto:

> Una empresa de logística maneja: envíos, clientes, rutas y conductores. Los envíos se registran con fecha, origen, destino, peso y estado (pendiente, en ruta, entregado).

**a)** Define el "minimundo" del sistema. ¿Qué entidades existen?  
**b)** ¿Qué programa usarías como SGBD? Justifica tu elección entre SQLite, PostgreSQL y MySQL.  
**c)** Identifica al menos 3 actores del sistema (roles de usuarios) y qué operaciones realiza cada uno.  
**d)** Dibuja el esquema de tres niveles (externo, conceptual, interno) para este sistema.

---

## Ejercicio 2 — Archivos vs Base de Datos

Una biblioteca universitaria lleva el registro de préstamos en archivos de texto planos, uno por día (ej. `prestamos_20240315.txt`).

**a)** Identifica al menos 4 problemas concretos que este enfoque genera con el tiempo.  
**b)** Propón cómo resolvería cada problema un SGBD relacional.  
**c)** ¿En qué escenario podría ser válido seguir usando archivos planos en lugar de una BD?

---

## Ejercicio 3 — Metadatos y catálogo del sistema

Ejecuta el siguiente comando en SQLite y analiza el resultado:
```sql
SELECT name, type, sql FROM sqlite_master;
```

**a)** ¿Qué información devuelve esta consulta?  
**b)** ¿Por qué el catálogo del sistema es en sí mismo una base de datos?  
**c)** ¿Qué diferencia hay entre datos y metadatos? Da 3 ejemplos de cada uno para una BD de estudiantes.

---

## Ejercicio 4 — Independencia de datos

**Escenario:** La BD de la universidad tiene la tabla `ESTUDIANTE(ci, nombre, apellido, fecha_nac)`. Se decide agregar una columna `email` y cambiar `fecha_nac` por `edad`.

**a)** ¿Qué aplicaciones podrían romperse con este cambio? ¿Por qué?  
**b)** Explica la diferencia entre independencia lógica e independencia física.  
**c)** ¿Cómo ayudan las **vistas** a mantener la independencia lógica de datos?

---

## Ejercicio 5 — Arquitectura de SGBD

```
Aplicación Web   App Móvil   Reporte Python
      │               │             │
      └───────────────┴─────────────┘
                      │
               ¿Componente X?
                      │
                 Base de Datos
```

**a)** ¿Qué es el "Componente X"? ¿Qué funciones tiene?  
**b)** Enumera 5 funciones que cumple un SGBD además de almacenar datos.  
**c)** Diferencia entre un SGBD y un sistema de archivos (filesystem). ¿En qué se parecen?

---

## Ejercicio 6 — Práctica SQLite

Ejecuta el script [`01_intro_sqlite.py`](./01_intro_sqlite.py) y responde:

**a)** ¿En qué directorio se crea el archivo `.db`? ¿Qué pasa si lo eliminas y vuelves a ejecutar el script?  
**b)** Modifica el script para agregar una tabla `CARRERA(id_carrera, nombre, duracion)` e insertar 3 carreras.  
**c)** Escribe una consulta SQL que liste los estudiantes inscritos en una carrera específica, usando `JOIN`.

---

## Ejercicio 7 — Desafío integrador

Diseña (a nivel conceptual, sin SQL) una base de datos para uno de los siguientes sistemas:

- Sistema de votación universitaria  
- Control de inventario de una farmacia  
- Gestión de turnos de un consultorio médico

Para el sistema elegido, define:
1. Al menos 5 entidades con sus atributos principales
2. El minimundo (descripción en 5-8 líneas)
3. Los actores del sistema y sus roles
4. Una lista de 5 consultas que el sistema debería poder responder
