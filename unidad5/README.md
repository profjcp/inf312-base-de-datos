# Unidad V · Normalización y Dependencias Funcionales

**Tiempo:** 10 horas  
**Objetivo:** Identificar y eliminar las anomalías en las relaciones utilizando las reglas de normalización.

---

## Resultado de aprendizaje de la unidad

Al finalizar la unidad podrás identificar dependencias funcionales, detectar anomalías de diseño y normalizar esquemas hasta 3FN (y cuando sea necesario FNBC), justificando cada descomposición.

## Ruta recomendada de trabajo

1. Identifica claves candidatas y dependencias funcionales.
2. Verifica 1FN, 2FN y 3FN en secuencia.
3. Descompón tablas con anomalías y valida pérdida/cobertura.
4. Evalúa casos especiales de FNBC.
5. Decide cuándo conviene desnormalizar por rendimiento.

## Práctica por niveles

| Nivel | Meta práctica |
|------|---------------|
| Básico | Detectar violaciones de 1FN y 2FN |
| Medio | Llevar esquemas reales a 3FN documentando pasos |
| Reto | Analizar trade-offs entre FNBC y conservación de dependencias |

## Hito de proyecto (Unidad V)

Entregar para el caso Hospital:

- Matriz de dependencias funcionales por tabla.
- Verificación formal de 1FN, 2FN y 3FN.
- Ajustes finales del esquema con justificación técnica.
- Riesgos de desnormalización identificados.

## Autoevaluación rápida

- ¿Puedes identificar dependencias parciales y transitivas sin ambigüedad?
- ¿Cada descomposición preserva integridad y sentido de negocio?
- ¿Tu esquema final evita anomalías de inserción, borrado y actualización?
- ¿Sabes justificar cuándo NO desnormalizar?

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

## 5.5 SQL Relacional vs NoSQL — Perspectiva comparativa

El modelo relacional con normalización es la base de los SGBD SQL. Sin embargo, en proyectos modernos aparecen frecuentemente bases de datos **NoSQL** (Not only SQL). Esta sección ofrece una introducción comparativa.

### ¿Por qué existen las BD NoSQL?

El modelo relacional normalizado es excelente para **integridad y consistencia**, pero puede ser un cuello de botella cuando:

- Los datos no tienen estructura fija (esquema dinámico)
- El sistema necesita escalar horizontalmente a miles de servidores
- Se procesan millones de operaciones por segundo (redes sociales, IoT)
- Los datos son inherentemente jerárquicos o en grafo

### Tipos principales de NoSQL

| Tipo | Estructura | Casos de uso | Ejemplos |
|------|-----------|-------------|---------|
| **Documento** | JSON/BSON anidado | CMS, catálogos, perfiles de usuario | MongoDB, CouchDB |
| **Clave-Valor** | Diccionario simple | Caché, sesiones, configuración | Redis, DynamoDB |
| **Columnar** | Columnas agrupadas | Analítica de grandes volúmenes (OLAP) | Cassandra, HBase |
| **Grafo** | Nodos y aristas | Redes sociales, rutas, recomendaciones | Neo4j, Amazon Neptune |

### Ejemplo comparativo: Consulta de un perfil

**SQL normalizado (3FN):**
```sql
-- 3 tablas, 2 JOINs para obtener el perfil completo
SELECT u.nombre, u.email,
       d.calles, d.ciudad,
       t.numero, t.tipo
FROM USUARIO u
JOIN DIRECCION d ON u.id = d.id_usuario
JOIN TELEFONO  t ON u.id = t.id_usuario
WHERE u.id = 42;
```

**MongoDB (documento):**
```json
// Todo en un documento, una sola lectura
{
  "_id": 42,
  "nombre": "Ana García",
  "email": "ana@example.com",
  "direccion": { "calle": "Av. Cañoto 123", "ciudad": "Santa Cruz" },
  "telefonos": ["71234567", "33456789"]
}
```

### ¿SQL o NoSQL?

```
                    ┌─────────────┐
                    │  Estructura │
                    │  de datos   │
                    └──────┬──────┘
                           │
                ┌──────────┴──────────┐
           Estructura fija        Estructura flexible
           relaciones complejas   / documentos anidados
                │                          │
                ▼                          ▼
           SQL (relacional)          NoSQL (documento)
           PostgreSQL, MySQL         MongoDB, CouchDB
           SQLite                         │
                                          ▼
                               Alta escala / baja latencia?
                                    │            │
                                   SÍ            NO
                                    │
                              Redis (cache)
                              Cassandra (big data)
```

### Propiedades BASE vs ACID

| ACID (SQL) | BASE (NoSQL) |
|-----------|-------------|
| **A**tomicity | **B**asically **A**vailable |
| **C**onsistency | **S**oft state |
| **I**solation | **E**ventually consistent |
| **D**urability | — |

> Los sistemas NoSQL prioriza disponibilidad y rendimiento sobre consistencia inmediata. En una red social, está bien que un "me gusta" tarde 1 segundo en propagarse. En un sistema bancario, NO está bien.

> **Para este curso:** el foco es el modelo relacional. NoSQL es un tema de materias posteriores (Bases de Datos II, Sistemas Distribuidos). Esta sección sólo da contexto de cuándo SQL es la herramienta correcta —que es la mayoría de los casos de negocios.

---

## 📁 Archivos de esta unidad

| Archivo | Descripción |
|---------|-------------|
| [`practica/01_normalizacion.py`](./practica/01_normalizacion.py) | Demostración paso a paso: 0FN → 3FN |
| [`practica/enunciados.md`](./practica/enunciados.md) | 8 ejercicios graduados de normalización |
| [`teoria/apuntes.md`](./teoria/apuntes.md) | Reglas de Armstrong, cierre de atributos, ejercicios resueltos |
