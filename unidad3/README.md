# Unidad III · Modelo Relacional

**Tiempo:** 18 horas  
**Objetivo:** Diseñar una base de datos utilizando los conceptos del modelo relacional (estructura, restricciones y lenguaje).

**Evaluacion sugerida:** [evaluacion.md](evaluacion.md)

---

## Resultado de aprendizaje de la unidad

Al finalizar la unidad podrás transformar un modelo conceptual en un esquema relacional consistente, aplicar restricciones de integridad y expresar consultas con álgebra relacional y SQL equivalente.

## Ruta recomendada de trabajo

1. Estudia dominios, claves y restricciones con ejemplos pequeños.
2. Verifica integridad de entidades y referencial en casos reales.
3. Resuelve operaciones de álgebra en orden: σ, π, ⋈, ∪, ∩, −.
4. Traduce cada expresión de álgebra a SQL y valida resultados.
5. Documenta decisiones para reutilizarlas en el proyecto final.

## Práctica por niveles

| Nivel | Meta práctica |
|------|---------------|
| Básico | Identificar PK, FK y restricciones por tabla |
| Medio | Convertir 10 consultas de álgebra a SQL correcto |
| Reto | Diseñar esquema relacional completo para un caso nuevo |

## Hito de proyecto (Unidad III)

Entregar para el caso Hospital:

- Esquema relacional completo.
- Claves primarias y foráneas justificadas.
- Reglas de integridad (dominio, entidad, referencial).
- Primera versión del diccionario de datos.

## Autoevaluación rápida

- ¿Cada tabla tiene PK explícita?
- ¿Todas las FK referencian claves existentes?
- ¿Tus consultas en álgebra tienen equivalente SQL probado?
- ¿Puedes explicar por qué elegiste cada restricción?

---

## 3.1 Conceptos del Modelo Relacional

El **modelo relacional** fue propuesto por Edgar F. Codd en 1970. Representa los datos como tablas (relaciones) compuestas de filas y columnas.

### 3.1.1 Dominios

Un **dominio** es el conjunto de valores atómicos posibles para un atributo.

```
Dominio de CI_boliviana:  cadena de 7-8 dígitos numéricos
Dominio de nota:          número decimal entre 0 y 100
Dominio de estado:        {'activo', 'inactivo', 'suspendido'}
Dominio de fecha_nac:     fechas entre 1900-01-01 y hoy
```

### 3.1.2 Atributos

Un **atributo** es una propiedad de una relación, definida sobre un dominio.

```
Relación ESTUDIANTE:
  ci        → dom: VARCHAR(10)
  nombre    → dom: VARCHAR(100)
  nota_prom → dom: DECIMAL(5,2), entre 0 y 100
```

### 3.1.3 Tuplas y Relaciones

```
RELACIÓN (tabla):
  Nombre: ESTUDIANTE
  Grado (número de atributos): 4
  Cardinalidad (número de tuplas): 3

  ci       | nombre  | apellido | nota_prom
  ---------|---------|----------|----------
  7654321  | Ana     | García   | 85.50      ← TUPLA 1
  8123456  | Luis    | Mamani   | 77.30      ← TUPLA 2
  9234567  | María   | López    | 60.00      ← TUPLA 3
  ↑                                          ↑
  ATRIBUTO                                  VALOR
```

### 3.1.4 Características de las Relaciones

```
1. No hay tuplas duplicadas
   → Cada fila es única (garantizado por la clave primaria)

2. Las tuplas no están ordenadas
   → No existe "primera fila" o "última fila" conceptualmente

3. Los atributos no están ordenados
   → El orden de columnas no importa en el modelo teórico

4. Todos los valores son atómicos (1FN)
   → Cada celda contiene un solo valor indivisible
   → ❌ No: teléfonos = "71234567, 72345678"
   → ✓ Sí: una fila por teléfono

5. Los atributos tienen nombres únicos dentro de la relación
```

### 3.1.5 Notación del Modelo Relacional

```
Notación esquemática:
  NOMBRE_TABLA(atributo1, atributo2, ..., atributoN)

  PK = subrayado    FK = subrayado doble o (FK)

Ejemplo:
  CARRERA(id_carrera, nombre, duracion)
  ESTUDIANTE(ci, nombre, apellido, fecha_nac, id_carrera→CARRERA)
  MATERIA(codigo, nombre, creditos, nivel)
  INSCRIPCION(id_inscripcion, ci→ESTUDIANTE, codigo→MATERIA, gestion, nota)
```

---

## 3.2 Restricciones Relacionales

### 3.2.1 Restricción de Dominio

Cada valor de un atributo debe pertenecer a su dominio.

```sql
-- Ejemplos de restricciones de dominio en SQL:
nota    DECIMAL(5,2) CHECK (nota BETWEEN 0 AND 100)
estado  VARCHAR(10)  CHECK (estado IN ('activo','inactivo'))
edad    INTEGER      CHECK (edad > 0 AND edad < 150)
email   VARCHAR(150) CHECK (email LIKE '%@%.%')
```

### 3.2.2 Restricción en la Clave y sobre Nulos

```
Clave candidata: conjunto mínimo de atributos que identifica unívocamente
                 cada tupla de la relación.
  Ejemplo ESTUDIANTE: {ci}, {email}  → ambas son claves candidatas

Clave primaria (PK): clave candidata elegida como identificador principal.
  ESTUDIANTE → PK: ci

Clave única (UK): otra clave candidata no elegida como PK.
  ESTUDIANTE → UK: email

Nulos (NULL): valor desconocido o no aplicable.
  La clave primaria NUNCA puede ser NULL.
  Otros atributos pueden ser NULL si se permite.
```

---

## 3.3 Integridad

### 3.3.1 Integridad de Entidades

> **Regla:** Ningún atributo de la clave primaria puede ser NULL.

```
✓ ESTUDIANTE: ci = '7654321'    → válido
✗ ESTUDIANTE: ci = NULL         → VIOLA integridad de entidad
```

### 3.3.2 Integridad Referencial y Claves Externas

> **Regla:** Si una tupla hace referencia a otra tabla mediante FK, el valor referenciado debe existir en la tabla referenciada, o ser NULL.

```
INSCRIPCION.ci = '7654321'  → debe existir en ESTUDIANTE.ci  ✓
INSCRIPCION.ci = '9999999'  → no existe en ESTUDIANTE.ci     ✗ VIOLA

Diagrama:
  ESTUDIANTE          INSCRIPCION
  ┌─────────┐         ┌─────────────┐
  │ ci: PK  │◀──FK────│ ci          │
  │ nombre  │         │ codigo: FK  │──▶ MATERIA
  └─────────┘         │ gestion     │
                      │ nota        │
                      └─────────────┘
```

---

## 3.4 Operaciones de Actualización y Violaciones

| Operación | Restricciones que puede violar |
|-----------|-------------------------------|
| **INSERT** | Dominio, clave primaria (duplicado), integridad referencial (FK no existe) |
| **DELETE** | Integridad referencial (otra tabla apunta a esta fila) |
| **UPDATE** | Cualquiera de las anteriores |

### Acciones ante violación de FK en DELETE

```sql
-- Al borrar el padre, ¿qué pasa con los hijos?

ON DELETE RESTRICT    → Rechaza la eliminación (error)
ON DELETE CASCADE     → Elimina en cascada los hijos
ON DELETE SET NULL    → Pone NULL en la FK del hijo
ON DELETE SET DEFAULT → Pone el valor por defecto

-- Ejemplo:
FOREIGN KEY (ci) REFERENCES ESTUDIANTE(ci)
    ON DELETE CASCADE   -- si se borra el estudiante, se borran sus inscripciones
    ON UPDATE CASCADE   -- si cambia el ci, se actualiza en cascada
```

---

## 3.5 Álgebra Relacional

El **álgebra relacional** es el lenguaje formal del modelo relacional. Define operaciones que toman relaciones como entrada y producen relaciones como salida.

### 3.5.1 Seleccionar (σ), Proyectar (π), Renombrar (ρ)

```
SELECCIONAR σ — filtra filas (equivale a WHERE en SQL)
───────────────────────────────────────────────────
σ nota>=51 (INSCRIPCION)
→ Solo las filas donde nota >= 51

SQL equivalente:
  SELECT * FROM INSCRIPCION WHERE nota >= 51;

──────────────────────────────────────────────────
PROYECTAR π — selecciona columnas (equivale a SELECT columnas)
──────────────────────────────────────────────────
π ci,nombre,apellido (ESTUDIANTE)
→ Solo las columnas ci, nombre y apellido

SQL equivalente:
  SELECT ci, nombre, apellido FROM ESTUDIANTE;

──────────────────────────────────────────────────
Combinados:
π nombre,nota (σ nota>=51 (INSCRIPCION ⋈ ESTUDIANTE))
→ Nombre y nota de estudiantes aprobados

SQL equivalente:
  SELECT e.nombre, i.nota
  FROM INSCRIPCION i JOIN ESTUDIANTE e ON i.ci = e.ci
  WHERE i.nota >= 51;
```

### 3.5.2 Operaciones de Conjuntos: Unión (∪), Intersección (∩), Diferencia (-)

```
Para estas operaciones ambas relaciones deben ser COMPATIBLES
(mismo número de atributos y dominios compatibles)

UNIÓN R ∪ S:
  Todas las tuplas de R MÁS las de S (sin duplicados)
  SQL: SELECT ... UNION SELECT ...

INTERSECCIÓN R ∩ S:
  Solo las tuplas que están en AMBAS relaciones
  SQL: SELECT ... INTERSECT SELECT ...

DIFERENCIA R - S:
  Tuplas de R que NO están en S
  SQL: SELECT ... EXCEPT SELECT ...  (o NOT IN)

Ejemplo:
  A = estudiantes que cursan INF312
  B = estudiantes que cursan INF220

  A ∪ B = estudiantes que cursan INF312 O INF220
  A ∩ B = estudiantes que cursan AMBAS materias
  A - B = estudiantes que cursan INF312 pero NO INF220
```

### 3.5.3 Producto Cartesiano (×), Reunión (⋈), Reunión Natural

```
PRODUCTO CARTESIANO R × S:
  Combina CADA tupla de R con CADA tupla de S
  Si R tiene 3 tuplas y S tiene 4 → resultado: 3×4 = 12 tuplas
  SQL: SELECT * FROM R, S   (sin condición JOIN → muy ineficiente)

REUNIÓN (JOIN) R ⋈(condición) S:
  Producto cartesiano + filtro por condición
  SQL: SELECT * FROM R JOIN S ON condición

REUNIÓN NATURAL R ⋈ S:
  JOIN automático por atributos de mismo nombre y dominio
  Elimina las columnas duplicadas del resultado
  SQL: SELECT * FROM R NATURAL JOIN S  (usar con cuidado)

Ejemplo:
  ESTUDIANTE ⋈(ESTUDIANTE.ci = INSCRIPCION.ci) INSCRIPCION
  → Cada estudiante con sus inscripciones
```

### 3.5.4 Operaciones Adicionales

```
DIVISIÓN R ÷ S:
  Devuelve las tuplas de R que están relacionadas con
  TODAS las tuplas de S.

  Ejemplo:
    R = INSCRIPCION(ci, codigo)
    S = MATERIAS_REQUERIDAS(codigo) = {INF220, INF312}
    R ÷ S = estudiantes que cursaron TODAS las materias requeridas

  SQL equivalente (usando NOT EXISTS):
  SELECT DISTINCT ci FROM INSCRIPCION i1
  WHERE NOT EXISTS (
      SELECT codigo FROM MATERIAS_REQUERIDAS mr
      WHERE NOT EXISTS (
          SELECT * FROM INSCRIPCION i2
          WHERE i2.ci = i1.ci AND i2.codigo = mr.codigo
      )
  );

FUNCIONES DE AGREGACIÓN (extensión del álgebra relacional):
  COUNT, SUM, AVG, MAX, MIN → agrupadas con GROUP BY en SQL
```

---

## 📁 Archivos de esta unidad

| Archivo | Descripción |
|---------|-------------|
| [`practica/01_modelo_relacional.py`](./practica/01_modelo_relacional.py) | Restricciones e integridad en Python/SQLite |
| [`practica/01_algebra_relacional.sql`](./practica/01_algebra_relacional.sql) | Álgebra relacional traducida a SQL |
| [`practica/enunciados.md`](./practica/enunciados.md) | Ejercicios del modelo relacional |
| [`teoria/apuntes.md`](./teoria/apuntes.md) | Álgebra relacional, ejercicios resueltos y preguntas de examen |
