# Proyecto Final · INF-312 Base de Datos I

> **Universidad Autónoma "Gabriel René Moreno"**  
> **Valor:** 20% de la nota final  
> **Modalidad:** Grupal (3-4 integrantes)  
> **Caso asignado:** Sistema de Gestión de un Hospital

---

## 📋 Descripción General

**Rubrica de defensa:** [rubrica_defensa.md](rubrica_defensa.md)

El proyecto consiste en diseñar e implementar una base de datos para un **Hospital Público de Santa Cruz de la Sierra**. El sistema debe gestionar pacientes, médicos, consultas, hospitalizaciones, medicamentos e insumos.

El proyecto se evalúa en **dos fases:**

| Fase | Descripción | % del Proyecto |
|------|-------------|---------------|
| **Fase 1** | Diseño conceptual + lógico | 50% |
| **Fase 2** | Implementación en SQL + consultas | 50% |

---

## 🛤️ Trazabilidad por hitos (durante el semestre)

Para evitar concentrar todo al final, el proyecto se construye por entregas parciales conectadas a cada unidad:

| Momento | Entrega parcial | Relación con unidad |
|---------|------------------|---------------------|
| Semana 2 | Alcance del caso, actores y reglas de negocio | Unidad I |
| Semana 5 | Diagrama UML consolidado | Unidad II |
| Semana 8 | Esquema relacional con PK/FK y restricciones | Unidad III |
| Semana 12 | DDL + DML + consultas base | Unidad IV |
| Semana 14 | Verificación de normalización y ajustes | Unidad V |
| Semana 15 | Entrega y defensa final | Integración |

---

## ✅ Criterios de aceptación técnica mínimos

La entrega final se considera lista cuando cumple:

- El script SQL se ejecuta de inicio a fin sin errores en una BD vacía.
- Todas las FK tienen política explícita de ON DELETE/ON UPDATE.
- Existen datos de prueba suficientes para demostrar cada consulta requerida.
- Las consultas entregadas están comentadas y validadas.
- Las vistas responden a necesidades reales de operación.
- La normalización está justificada hasta 3FN como mínimo.
- El modelo implementado refleja el diagrama conceptual aprobado.

---

## 📐 Fase 1 — Diseño Conceptual e Intermedio

### Entregable: Documento técnico (PDF) + Diagrama de Clases

---

### Descripción del caso: HOSPITAL "SAN JUAN DE DIOS"

El hospital necesita registrar y gestionar la siguiente información:

**PACIENTES**
- Cada paciente tiene: CI, nombre completo, fecha de nacimiento, sexo, grupo sanguíneo, teléfono, dirección y correo electrónico.
- Un paciente puede tener uno o más seguros médicos (nombre de la aseguradora, número de póliza).

**MÉDICOS**
- Cada médico tiene: matrícula médica, CI, nombre completo, especialidad, teléfono y email.
- Un médico puede tener varias especialidades (una principal y otras secundarias).

**PERSONAL ADMINISTRATIVO**
- Secretarías, enfermeros y personal de limpieza.
- Tienen: CI, nombre, cargo, turno y salario.

**CONSULTAS MÉDICAS**
- Un paciente asiste a una consulta con un médico específico.
- Se registra: fecha/hora, motivo de consulta, diagnóstico, tratamiento indicado y costo.
- Una consulta puede generar una o más recetas médicas.

**RECETAS**
- Asociadas a una consulta, contienen una lista de medicamentos con dosis y duración.

**HOSPITALIZACIONES**
- Un paciente puede ser hospitalizado varias veces.
- Se registra: sala, número de cama, fecha de ingreso y fecha de alta.
- Un médico es responsable de la hospitalización.

**SALAS Y CAMAS**
- El hospital tiene varias salas (Pediatría, Cirugía, UCI, etc.).
- Cada sala tiene un número de camas definido.

**MEDICAMENTOS E INSUMOS**
- El hospital tiene un stock de medicamentos con: código, nombre, principio activo, precio, stock actual y stock mínimo.
- Los medicamentos se consumen en consultas y hospitalizaciones.

---

### Requerimiento 1: Diagrama de Clases UML

Diseñar el **Diagrama de Clases** que represente el modelo conceptual del hospital, incluyendo:

- Todas las clases con sus atributos (indicar tipo y si es PK)
- Todas las relaciones: asociación, generalización, composición y/o agregación
- Multiplicidades correctas en cada extremo de las relaciones

**Herramientas recomendadas:** draw.io, Lucidchart, StarUML, o dibujado a mano con escáner.

---

### Requerimiento 2: Mapeo Objeto-Relacional

Aplicar las reglas de mapeo para obtener el **esquema relacional**:

Escribir la notación de cada tabla resultante:
```
TABLA(atributo1 {PK}, atributo2, atributo3 {FK→OTRA_TABLA}, ...)
```

Indicar para cada tabla:
- Clave primaria
- Claves foráneas (con tabla referenciada)
- Restricciones importantes (NOT NULL, UNIQUE, CHECK)

---

### Requerimiento 3: Normalización

Verificar que el esquema resultante esté en **3FN**:

1. Identificar las dependencias funcionales de cada tabla
2. Verificar 1FN: ¿hay atributos multivaluados? Corregir si aplica
3. Verificar 2FN: ¿hay dependencias parciales? Corregir si aplica
4. Verificar 3FN: ¿hay dependencias transitivas? Corregir si aplica

---

## 💻 Fase 2 — Implementación en SQL

### Entregable: Archivo `.sql` ejecutable + Informe de consultas

---

### Requerimiento 4: Script DDL completo

```sql
-- Crear todas las tablas con:
-- ✓ Tipos de datos adecuados
-- ✓ Claves primarias (PK)
-- ✓ Claves foráneas (FK) con ON DELETE/ON UPDATE
-- ✓ Restricciones CHECK
-- ✓ Valores DEFAULT donde corresponda
-- ✓ Índices en columnas de búsqueda frecuente
```

### Requerimiento 5: Datos de prueba (DML - INSERT)

Insertar datos suficientes para demostrar todas las consultas:
- Mínimo 5 médicos con diferentes especialidades
- Mínimo 15 pacientes
- Mínimo 20 consultas
- Mínimo 3 hospitalizaciones activas
- Mínimo 20 medicamentos
- Datos que permitan probar casos límite (stock mínimo, camas disponibles, etc.)

---

### Requerimiento 6: Consultas SQL requeridas

Implementar **las siguientes 15 consultas** con SQL comentado:

```sql
-- 1. Listar todos los médicos con su especialidad principal, ordenados por apellido
-- 2. Mostrar los pacientes hospitalizados actualmente (sin fecha de alta)
-- 3. Contar las consultas realizadas por cada médico en el último mes
-- 4. Listar los medicamentos con stock por debajo del mínimo
-- 5. Mostrar el historial completo de consultas de un paciente (por CI)
-- 6. Calcular el promedio de días de hospitalización por sala
-- 7. Listar los 5 medicamentos más recetados
-- 8. Mostrar médicos que NO han tenido consultas en los últimos 30 días
-- 9. Calcular el total facturado por consultas por médico
-- 10. Listar pacientes con más de 3 hospitalizaciones históricas
-- 11. Mostrar la ocupación actual de cada sala (camas usadas vs disponibles)
-- 12. Listar todas las recetas emitidas hoy con detalle de medicamentos
-- 13. Encontrar pacientes con el mismo grupo sanguíneo que necesitan donaciones
-- 14. Calcular el costo promedio de consultas por especialidad médica
-- 15. Listar el personal por turno con totales por cargo
```

### Requerimiento 7: Vistas

Crear **mínimo 3 vistas** útiles para el sistema:

```sql
-- Sugerencias:
CREATE VIEW V_CAMAS_DISPONIBLES AS ...   -- ocupación en tiempo real
CREATE VIEW V_HISTORIAL_PACIENTE AS ...  -- historial completo de paciente
CREATE VIEW V_STOCK_CRITICO AS ...       -- medicamentos bajo mínimo
```

---

## 📊 Rúbrica de Evaluación

### Fase 1 (50 puntos del proyecto)

| Criterio | Puntos |
|----------|--------|
| Diagrama de Clases completo y correcto | 15 |
| Multiplicidades correctas en todas las relaciones | 10 |
| Mapeo OO→Relacional correcto (PKs, FKs, notación) | 15 |
| Verificación de normalización hasta 3FN | 10 |
| **Total Fase 1** | **50** |

### Fase 2 (50 puntos del proyecto)

| Criterio | Puntos |
|----------|--------|
| Script DDL ejecuta sin errores | 10 |
| Tipos de datos, PK, FK, CHECK correctos | 10 |
| Datos de prueba suficientes y coherentes | 5 |
| Las 15 consultas funcionan y son correctas | 20 |
| Mínimo 3 vistas implementadas | 5 |
| **Total Fase 2** | **50** |

---

## 📁 Estructura de Entrega

```
proyecto_hospital_Apellido1_Apellido2/
├── README.md                    ← Integrantes y descripción
├── fase1/
│   ├── diagrama_clases.png      ← Imagen del diagrama UML
│   ├── esquema_relacional.md    ← Notación de todas las tablas
│   └── normalizacion.md         ← Análisis de dependencias funcionales
└── fase2/
    ├── hospital.sql             ← Script DDL + INSERT + consultas + vistas
    └── informe_consultas.md     ← Capturas de resultados de cada consulta
```

---

## 📁 Starter Code — fase2/hospital.sql

```sql
-- hospital.sql
-- Proyecto Final INF-312 Base de Datos I
-- Hospital "San Juan de Dios"
-- Integrantes: [Apellido1, Apellido2, Apellido3]
-- Fecha: [fecha de entrega]

-- ============================================================
-- DDL: CREAR TABLAS
-- ============================================================
-- (completar aquí)

-- ============================================================
-- DML: INSERTAR DATOS DE PRUEBA
-- ============================================================
-- (completar aquí)

-- ============================================================
-- CONSULTAS REQUERIDAS
-- ============================================================

-- Consulta 1: Médicos con su especialidad principal
-- (completar aquí)

-- Consulta 2: Pacientes hospitalizados actualmente
-- (completar aquí)

-- [... continuar con las 15 consultas ...]

-- ============================================================
-- VISTAS
-- ============================================================
-- (completar aquí)
```
