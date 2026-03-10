# Unidad V · Normalización y Dependencias Funcionales

**Tiempo:** 10 horas  
**Objetivo:** Identificar y eliminar las anomalías en las relaciones utilizando las reglas de normalización.

---

## 5.1 Pautas Informales de Diseño

Antes de las formas normales, hay 4 pautas informales que guían un buen diseño:

**Pauta 1:** Cada tabla debe representar UNA sola entidad o relación.
```
❌ MAL: INSCRIPCION_COMPLETA(ci, nombre_est, codigo_mat, nombre_mat, nota)
✓ BIEN: ESTUDIANTE(ci, nombre)  MATERIA(codigo, nombre)  INSCRIPCION(ci, codigo, nota)
```

**Pauta 2:** Evitar colocar atributos cuyo valor se repite en múltiples tuplas.
```
❌ MAL: VENTA(id_venta, nombre_cliente, ciudad_cliente, ...)
       → nombre_cliente y ciudad_cliente se repiten por cada venta
✓ BIEN: extraer CLIENTE a tabla separada
```

**Pauta 3:** Evitar valores nulos en la medida de lo posible.

**Pauta 4:** Cuidar las anomalías de actualización (inserción, borrado, modificación).

### Tipos de anomalías

```
Tabla problemática:
EMPLEADO_DEPTO(ci, nombre, id_depto, nombre_depto, ubicacion_depto)

Anomalía de INSERCIÓN:
  → No puedo insertar un departamento nuevo sin tener un empleado
  → Si inserto un empleado, debo repetir nombre_depto y ubicacion_depto

Anomalía de BORRADO:
  → Si borro el único empleado de un departamento, pierdo
    los datos del departamento (nombre_depto, ubicacion_depto)

Anomalía de MODIFICACIÓN:
  → Si cambia la ubicación de un departamento, debo actualizar
    TODAS las filas de empleados de ese departamento
  → Si olvido alguna → INCONSISTENCIA
```

---

## 5.2 Dependencias Funcionales

Una **dependencia funcional** X → Y significa que conocer X determina unívocamente el valor de Y.

```
Notación: X → Y    "X determina Y" o "Y depende funcionalmente de X"

Ejemplos:
  ci → nombre, apellido, fecha_nac
  (ci, codigo, gestion) → nota          ← clave compuesta determina nota
  codigo_postal → ciudad                 ← el código postal determina la ciudad
  isbn → titulo, anio_pub               ← el ISBN determina el título del libro
```

### Tipos de dependencias funcionales

```
DEPENDENCIA COMPLETA:
  {ci, codigo} → nota
  → nota depende de la clave COMPLETA (ci, codigo)
  → si se elimina ci, ya no podemos determinar nota
  → si se elimina codigo, ya no podemos determinar nota

DEPENDENCIA PARCIAL:
  {ci, codigo} → nombre_estudiante
  → nombre_estudiante solo depende de ci (parte de la clave)
  → PROBLEMA: redundancia en 2FN

DEPENDENCIA TRANSITIVA:
  ci → id_carrera → nombre_carrera
  → nombre_carrera depende de ci TRANSITIVAMENTE a través de id_carrera
  → PROBLEMA: hay que eliminarla en 3FN
```

---

## 5.3 Formas Normales

### 5.3.1 Primera Forma Normal (1FN)

> **Regla:** Todos los atributos deben ser **atómicos** (indivisibles) y debe existir una clave primaria.

```
TABLA EN 0FN (no normalizada):
┌──────────┬──────────┬────────────────────────────────┐
│ ci       │ nombre   │ telefonos                      │
├──────────┼──────────┼────────────────────────────────┤
│ 7654321  │ Ana      │ 72345678, 71111111             │ ← multivaluado
│ 8123456  │ Luis     │ 71234567                       │
└──────────┴──────────┴────────────────────────────────┘
Problema: "telefonos" tiene varios valores en una celda → NO ATÓMICO

SOLUCIÓN para llevar a 1FN:
Opción A: Una fila por teléfono
┌──────────┬──────────┬───────────┐
│ ci       │ nombre   │ telefono  │
├──────────┼──────────┼───────────┤
│ 7654321  │ Ana      │ 72345678  │
│ 7654321  │ Ana      │ 71111111  │ ← nueva fila
│ 8123456  │ Luis     │ 71234567  │
└──────────┴──────────┴───────────┘
PK: (ci, telefono)

Opción B: Tabla separada TELEFONO(ci_fk, telefono) ← RECOMENDADA
```

---

### 5.3.2 Segunda Forma Normal (2FN)

> **Regla:** Estar en 1FN + todos los atributos no-clave deben depender de la **clave primaria completa** (no parcialmente).

```
TABLA EN 1FN con dependencia parcial:
INSCRIPCION(ci, codigo, gestion, nota, nombre_est, nombre_mat)
PK: (ci, codigo, gestion)

Dependencias:
  (ci, codigo, gestion) → nota         ← completa ✓
  ci → nombre_est                       ← PARCIAL ✗ (solo depende de ci)
  codigo → nombre_mat                   ← PARCIAL ✗ (solo depende de codigo)

SOLUCIÓN — separar en tablas:
ESTUDIANTE(ci, nombre_est)              ← ci → nombre_est
MATERIA(codigo, nombre_mat)             ← codigo → nombre_mat
INSCRIPCION(ci, codigo, gestion, nota)  ← PK completa, solo nota depende de toda la PK
```

---

### 5.3.3 Tercera Forma Normal (3FN)

> **Regla:** Estar en 2FN + ningún atributo no-clave debe depender **transitivamente** de la clave primaria.

```
TABLA EN 2FN con dependencia transitiva:
EMPLEADO(id_emp, nombre, id_depto, nombre_depto, ubicacion_depto)
PK: id_emp

Dependencias:
  id_emp → id_depto          ← directa ✓
  id_emp → nombre_depto      ← TRANSITIVA (a través de id_depto) ✗
  id_depto → nombre_depto    ← dependencia transitiva
  id_depto → ubicacion_depto ← dependencia transitiva

SOLUCIÓN — separar en 2 tablas:
DEPARTAMENTO(id_depto, nombre_depto, ubicacion_depto)
EMPLEADO(id_emp, nombre, id_depto)  ← id_depto es FK
```

---

### 5.3.4 Forma Normal de Boyce-Codd (FNBC)

> **Regla:** Estar en 3FN + para toda dependencia funcional X → Y, X debe ser una superclave.

```
FNBC es más estricta que 3FN. Afecta tablas con MÚLTIPLES claves candidatas superpuestas.

Ejemplo problemático:
TURNO(est, materia, tutor)
  Restricciones del dominio:
  - Un estudiante tiene un tutor por materia
  - Un tutor solo enseña una materia

  Claves candidatas: {est, materia} y {est, tutor}
  Dependencia: tutor → materia (tutor NO es superclave) → VIOLA FNBC

SOLUCIÓN:
TUTOR_MATERIA(tutor, materia)
ASIGNACION(est, tutor)
```

---

### 5.3.5 Cuarta Forma Normal (4FN)

> **Regla:** Estar en FNBC + no tener dependencias multivaluadas no triviales.

```
Una dependencia multivaluada X →→ Y significa que para cada valor de X
hay un conjunto de valores de Y independiente de otros atributos.

EMPLEADO_PROYECTO_HABILIDAD(emp, proyecto, habilidad)
  emp →→ proyecto    (un empleado tiene varios proyectos)
  emp →→ habilidad   (un empleado tiene varias habilidades)
  Estas son INDEPENDIENTES entre sí → 4FN se viola

SOLUCIÓN: descomponer
EMPLEADO_PROYECTO(emp, proyecto)
EMPLEADO_HABILIDAD(emp, habilidad)
```

---

### 5.3.6 Quinta Forma Normal (5FN)

> **Regla:** Estar en 4FN + no tener dependencias de reunión no triviales.

```
5FN (también llamada Forma Normal de Proyección-Reunión) aplica cuando
una tabla puede descomponerse en 3 o más tablas sin pérdida de información.

Es la forma normal más alta prácticamente usada.
En la práctica, llegar a 3FN o FNBC es suficiente para la mayoría de aplicaciones.
```

---

## Resumen: Proceso de Normalización

```
Tabla sin normalizar
        │
        ▼  Eliminar atributos multivaluados, garantizar clave primaria
       1FN
        │
        ▼  Eliminar dependencias parciales (para PKs compuestas)
       2FN
        │
        ▼  Eliminar dependencias transitivas
       3FN  ← Objetivo habitual del diseñador de BD
        │
        ▼  Resolver superposición de claves candidatas
      FNBC  ← Recomendado en casos críticos
        │
        ▼  Eliminar dependencias multivaluadas
       4FN
        │
        ▼  Eliminar dependencias de reunión
       5FN
```

---

## 📁 Archivos de esta unidad

| Archivo | Descripción |
|---------|-------------|
| [`practica/01_normalizacion.py`](./practica/01_normalizacion.py) | Demostración paso a paso: 0FN → 3FN |
| [`practica/01_normalizacion.sql`](./practica/01_normalizacion.sql) | SQL antes y después de normalizar |
| [`practica/enunciados.md`](./practica/enunciados.md) | 8 ejercicios de normalización |
