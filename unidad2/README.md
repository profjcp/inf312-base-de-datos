# Unidad II · Diseño Conceptual de Bases de Datos bajo Modelo Orientado a Objetos

**Tiempo:** 20 horas  
**Objetivo:** Aplicar el modelo orientado a objetos como herramienta de modelado conceptual de datos en la fase de diseño de una base de datos.

---

## 2.1 Introducción

El **diseño conceptual** es la primera fase del diseño de una base de datos. Su objetivo es capturar todos los requisitos de información del problema, independientemente del SGBD que se usará.

### Fases del diseño de una BD

```
Mundo Real
    │
    ▼
1. DISEÑO CONCEPTUAL (← Esta unidad)
   → Diagrama de Clases UML
   → ¿Qué entidades existen? ¿Cómo se relacionan?
    │
    ▼
2. DISEÑO LÓGICO / RELACIONAL (← Unidad III)
   → Tablas, columnas, claves
   → Modelo relacional
    │
    ▼
3. DISEÑO FÍSICO
   → SQL CREATE TABLE
   → Índices, particiones, optimización
    │
    ▼
4. IMPLEMENTACIÓN
   → Script SQL ejecutado en el SGBD
```

---

## 2.2 Clases y Objetos

En el modelado orientado a objetos:

- Una **clase** describe un tipo de entidad del problema (ej: Estudiante, Materia)
- Un **objeto** es una instancia concreta de esa clase (ej: Ana García, ci=7654321)

### Representación UML de una clase

```
┌─────────────────────────────┐
│         ESTUDIANTE          │  ← Nombre de la clase
├─────────────────────────────┤
│ - ci: String  {PK}          │  ← Atributos
│ - nombre: String            │     (- = privado)
│ - apellido: String          │
│ - fechaNac: Date            │
│ - email: String             │
├─────────────────────────────┤
│ + getNombreCompleto(): Str  │  ← Métodos
│ + calcularEdad(): Integer   │     (+ = público)
└─────────────────────────────┘
```

### Tipos de atributos

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Simple** | Valor único e indivisible | nombre, ci |
| **Compuesto** | Formado por sub-atributos | dirección (calle, ciudad, CP) |
| **Derivado** | Calculado a partir de otro | edad (derivada de fechaNac) |
| **Multivaluado** | Puede tener varios valores | teléfonos {celular, fijo} |
| **Clave (PK)** | Identifica unívocamente al objeto | ci, codigo_materia |

---

## 2.3 Relaciones

### Asociación

Relación simple entre dos clases. Incluye multiplicidad (cardinalidad).

```
Multiplicidades:
  1     exactamente uno
  0..1  cero o uno (opcional)
  1..*  uno o más (al menos uno)
  *     cero o más (cualquier cantidad)
  0..*  igual que *
  n..m  entre n y m

Ejemplo: Un estudiante se inscribe en varias materias
         Una materia tiene varios estudiantes inscritos

ESTUDIANTE ──────────────── MATERIA
           1..* inscrito en *..1
```

#### Diagrama texto de la BD Universitaria

```
CARRERA          ESTUDIANTE          INSCRIPCION          MATERIA
┌──────────┐     ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│id_carrera│     │ci    {PK}    │    │id_inscripcion│    │codigo {PK}   │
│nombre    │1──* │nombre        │1──*│ci  {FK}     │*──1│nombre        │
│duracion  │     │apellido      │    │codigo {FK}  │    │creditos      │
└──────────┘     │fecha_nac     │    │gestion      │    │nivel         │
                 │id_carrera{FK}│    │nota         │    └──────────────┘
                 └──────────────┘    └─────────────┘
```

#### Tipos de cardinalidad

```
1:1 (uno a uno)
  PERSONA ──── PASAPORTE
  Una persona tiene un pasaporte; un pasaporte pertenece a una persona

1:N (uno a muchos) ← el más común
  CARRERA ──── ESTUDIANTE
  Una carrera tiene muchos estudiantes; un estudiante pertenece a una carrera

N:M (muchos a muchos)
  ESTUDIANTE ──── MATERIA
  Un estudiante cursa muchas materias; una materia tiene muchos estudiantes
  → Se implementa con una tabla intermedia: INSCRIPCION
```

---

### Generalización (Herencia)

Permite definir clases más específicas a partir de una clase general.

```
          PERSONA
          /      \
  ESTUDIANTE    DOCENTE
  
PERSONA (ci, nombre, apellido, fecha_nac)
  │
  ├── ESTUDIANTE (ci_fk, carrera, anio_ingreso)
  └── DOCENTE    (ci_fk, categoria, departamento)
```

En UML: flecha con triángulo hueco apuntando a la superclase.

```
         ┌──────────────────┐
         │     PERSONA      │
         ├──────────────────┤
         │ ci: String {PK}  │
         │ nombre: String   │
         │ apellido: String │
         └────────┬─────────┘
                  △  (herencia)
         ┌────────┴────────┐
         │                 │
┌────────┴─────┐   ┌───────┴──────┐
│  ESTUDIANTE  │   │   DOCENTE    │
├──────────────┤   ├──────────────┤
│ carrera      │   │ categoria    │
│ anio_ingreso │   │ departamento │
└──────────────┘   └──────────────┘
```

---

### Composición

Relación de "parte de" donde las partes **no pueden existir** sin el todo. Si el todo se elimina, las partes también.

```
PEDIDO ◆──── ITEM_PEDIDO
(Si se elimina el pedido, se eliminan sus ítems)

EDIFICIO ◆──── AULA
(Las aulas no existen sin el edificio)
```

En UML: rombo lleno (◆) en la clase "todo".

---

### Agregación

Relación de "tiene" donde las partes **pueden existir** independientemente del todo.

```
DEPARTAMENTO ◇──── DOCENTE
(Los docentes existen aunque se disuelva el departamento)

PROYECTO ◇──── EMPLEADO
(Los empleados existen aunque el proyecto termine)
```

En UML: rombo vacío (◇) en la clase "todo".

---

## 2.4 Diagrama de Clases — Caso: Sistema de Biblioteca

```
┌─────────────────────┐        ┌──────────────────────┐
│      SOCIO          │        │       LIBRO           │
├─────────────────────┤        ├──────────────────────┤
│ + id_socio: Int {PK}│        │ + isbn: Str {PK}      │
│ + nombre: Str       │        │ + titulo: Str         │
│ + apellido: Str     │        │ + anio_pub: Int       │
│ + email: Str        │        │ + id_autor: Int {FK}  │
│ + activo: Bool      │        │ + id_editorial: Int   │
└──────────┬──────────┘        └──────────┬───────────┘
           │  1                            │  1
           │  registra                    tiene
           │  *                            │  *
   ┌───────┴──────────┐          ┌─────────┴──────────┐
   │     PRESTAMO     │          │    EJEMPLAR         │
   ├──────────────────┤          ├────────────────────┤
   │ + id: Int {PK}   │    *     │ + id_ejemplar: Int  │
   │ + id_socio {FK}  │──────────│ + isbn_fk: Str      │
   │ + id_ejemplar{FK}│ prestado │ + estado: Str       │
   │ + fecha_prestamo │          └────────────────────┘
   │ + fecha_devol    │
   │ + devuelto: Bool │                ┌──────────────┐
   └──────────────────┘                │    AUTOR     │
                                       ├──────────────┤
   ┌──────────────────┐         *      │ + id: Int    │
   │   MULTA          │◆────────────── │ + nombre     │
   ├──────────────────┤  tiene         │ + pais       │
   │ + id_multa: Int  │ (composición)  └──────────────┘
   │ + id_prestamo{FK}│
   │ + monto: Decimal │
   │ + pagada: Bool   │
   └──────────────────┘
```

---

## 2.5 Mapeo Objeto Relacional (ORM conceptual)

Reglas para convertir el Diagrama de Clases a tablas relacionales:

### Regla 1: Clase → Tabla

```
Clase ESTUDIANTE            Tabla ESTUDIANTE
─────────────────    →      ─────────────────────────
ci: String {PK}             ci          VARCHAR(10) PK
nombre: String              nombre      VARCHAR(100) NOT NULL
apellido: String            apellido    VARCHAR(100) NOT NULL
fechaNac: Date              fecha_nac   DATE
```

### Regla 2: Asociación 1:N → Clave foránea en el lado "N"

```
CARRERA 1──────* ESTUDIANTE

Tabla CARRERA:    id_carrera (PK), nombre
Tabla ESTUDIANTE: ci (PK), nombre, ..., id_carrera (FK) ← clave foránea aquí
```

### Regla 3: Asociación N:M → Tabla intermedia

```
ESTUDIANTE *──────* MATERIA

Se crea tabla intermedia:
Tabla INSCRIPCION: id_inscripcion (PK), ci (FK), codigo (FK), gestion, nota
```

### Regla 4: Herencia → 3 opciones

```
Opción A: Tabla por jerarquía (una sola tabla)
  PERSONA(ci, nombre, tipo, carrera, categoria)
  ✓ Simple  ✗ Muchos nulls

Opción B: Tabla por clase concreta (una tabla por hoja)
  ESTUDIANTE(ci, nombre, apellido, carrera)
  DOCENTE(ci, nombre, apellido, categoria)
  ✓ Sin nulls  ✗ Duplicación de atributos comunes

Opción C: Tabla por clase (una tabla por clase)  ← RECOMENDADA
  PERSONA(ci, nombre, apellido)
  ESTUDIANTE(ci_fk, carrera)        ← ci_fk es PK y FK a PERSONA
  DOCENTE(ci_fk, categoria)
  ✓ Sin redundancia  ✗ Más JOINs
```

---

## 📁 Archivos de esta unidad

| Archivo | Descripción |
|---------|-------------|
| [`practica/01_mapeo_orm.py`](./practica/01_mapeo_orm.py) | Mapeo OO → Relacional en Python |
| [`practica/01_herencia.sql`](./practica/01_herencia.sql) | Implementación de herencia en SQL |
| [`practica/enunciados.md`](./practica/enunciados.md) | Ejercicios de modelado |
