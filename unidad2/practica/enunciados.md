# Unidad II — Ejercicios Prácticos

> **Archivos de referencia:** [`01_herencia_mapeo.sql`](./01_herencia_mapeo.sql)

---

## Ejercicio 1 — Identificación de clases y atributos

Para cada uno de los siguientes dominios, identifica las clases principales, sus atributos (con tipo y restricciones) y señala la clave primaria de cada una:

**a)** Sistema de reservas de un hotel  
**b)** Plataforma de streaming de música  
**c)** Sistema de gestión de una aerolínea (vuelos, pasajeros, asientos)

Para cada clase usa la notación UML de tres compartimentos:
```
┌──────────────────┐
│   NOMBRE_CLASE   │
├──────────────────┤
│ + atributo: Tipo │
└──────────────────┘
```

---

## Ejercicio 2 — Tipos de atributos

Clasifica los siguientes atributos como: **simple**, **compuesto**, **derivado** o **multivaluado**.

| Atributo | Contexto |
|----------|----------|
| `nombre_completo` | Clase PERSONA |
| `edad` | Clase PERSONA (dada la fecha de nacimiento) |
| `dirección` (tiene: calle, ciudad, CP) | Clase CLIENTE |
| `teléfonos` (puede tener varios) | Clase EMPLEADO |
| `precio_con_iva` | Clase PRODUCTO (dado el precio base) |
| `calificacion_promedio` | Clase ESTUDIANTE |
| `nombre` | Clase PRODUCTO |
| `coordenadas_gps` (latitud + longitud) | Clase SUCURSAL |

---

## Ejercicio 3 — Cardinalidades

Para cada par de clases, determina la multiplicidad (1:1, 1:N, N:M) y justifica tu respuesta:

**a)** PAÍS — CAPITAL  
**b)** MÉDICO — PACIENTE (en un hospital)  
**c)** AUTOR — LIBRO  
**d)** EMPLEADO — PROYECTO (un empleado puede estar en varios proyectos, y un proyecto tiene varios empleados)  
**e)** ESTUDIANTE — CARRERA (en la UAGRM)  
**f)** VUELO — ASIENTO  
**g)** FACTURA — PRODUCTO  
**h)** PERSONA — DNI/CI  

---

## Ejercicio 4 — Herencia

Diseña la jerarquía de herencia para los siguientes escenarios:

**a)** Un sistema universitario gestiona PERSONAS, que pueden ser ESTUDIANTES, DOCENTES o PERSONAL_ADMINISTRATIVO. Los estudiantes tienen carrera y año de ingreso; los docentes tienen categoría y departamento; el personal tiene cargo y salario.

- Dibuja el diagrama UML con herencia  
- Aplica las 3 opciones de mapeo relacional (tabla única, tabla por hoja, tabla por clase)  
- ¿Cuál opción elegirias? Justifica

**b)** Un banco maneja CUENTAS que pueden ser CUENTA_AHORRO (con tasa de interés y saldo mínimo) o CUENTA_CORRIENTE (con sobregiro permitido y cargos mensuales).

---

## Ejercicio 5 — Composición vs Agregación

Determina si la relación entre las siguientes clases es **composición** (◆) o **agregación** (◇) y justifica:

**a)** PEDIDO — ÍTEM_PEDIDO  
**b)** EMPRESA — EMPLEADO  
**c)** FACTURA — LÍNEA_FACTURA  
**d)** DEPARTAMENTO — DOCENTE  
**e)** EDIFICIO — PISO  
**f)** CURSO — ESTUDIANTE  
**g)** EXPEDIENTE_MÉDICO — DIAGNÓSTICO  

---

## Ejercicio 6 — Diagrama completo: Sistema de Veterinaria

Diseña el Diagrama de Clases UML completo para el siguiente caso:

> Una clínica veterinaria atiende **mascotas** de diferentes especies (perro, gato, ave, reptil). Cada mascota pertenece a uno o más **dueños**. Los **veterinarios** realizan **consultas** a las mascotas; en cada consulta se puede emitir una **receta** con medicamentos. La clínica también lleva un registro de **vacunas** aplicadas.

Incluye:
- Al menos 6 clases con atributos completos
- Herencia para los tipos de mascota
- Relaciones con multiplicidades
- Al menos una composición y una agregación

---

## Ejercicio 7 — Mapeo ORM

Para el siguiente Diagrama de Clases, aplica las reglas de mapeo y escribe el esquema relacional completo:

```
FACULTAD (1) ──── (N) CARRERA (1) ──── (N) MATERIA
                         │
                         └── (N) ESTUDIANTE (N) ──── (M) MATERIA
                                    │
                              INSCRIPCION (atributos: gestion, nota)
```

Para cada tabla resultante, indica:
- Nombre de la tabla en mayúsculas
- Atributos con tipo de dato
- PK y FK indicados
- Al menos 2 restricciones CHECK relevantes

---

## Ejercicio 8 — ER → Diagrama de Clases

Convierte el siguiente esquema ER (Chen) a un Diagrama de Clases UML:

```
[EMPLEADO] ─── (trabaja_en) ─── [DEPARTAMENTO]
    │                                  │
(supervisa)                     (ubicado_en)
    │                                  │
[EMPLEADO]                       [CIUDAD]
```
- Un empleado trabaja en un departamento (N:1)
- Un empleado puede supervisar a otros empleados (autorreferencia 1:N)
- Un departamento está ubicado en una ciudad (N:1)

¿Qué diferencias observas entre la notación ER y UML para representar este caso?
