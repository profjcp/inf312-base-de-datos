# Unidad III — Apuntes y Ejercicios Resueltos

## Álgebra relacional — Referencia rápida

| Operación | Símbolo | SQL equivalente |
|-----------|---------|-----------------|
| Selección | σ condición (R) | `WHERE condición` |
| Proyección | π atributos (R) | `SELECT atributos` |
| Reunión (Join) | R ⋈(cond) S | `JOIN ... ON cond` |
| Reunión natural | R ⋈ S | `NATURAL JOIN` |
| Unión | R ∪ S | `UNION` |
| Intersección | R ∩ S | `INTERSECT` |
| Diferencia | R − S | `EXCEPT` / `NOT IN` |
| Producto cartesiano | R × S | `FROM R, S` (sin ON) |
| Renombrar | ρ nombre(R) | `... AS nombre` |

---

## Ejercicio resuelto — Álgebra relacional compleja

**Caso:** Encontrar el nombre de los estudiantes que aprobaron **todas** las materias del nivel 3.

```
Sea:

M3 = π codigo (σ nivel=3 (MATERIA))
  → Conjunto de códigos de materias nivel 3

INS_APR = π ci,codigo (σ nota≥51 (INSCRIPCION))
  → Pares (ci, codigo) de materias aprobadas

TODOS_APR = INS_APR ÷ M3
  → CIs de estudiantes que aprobaron TODAS las materias de M3
  → Esto es DIVISIÓN RELACIONAL

π nombre (TODOS_APR ⋈ ESTUDIANTE)
  → Nombres de esos estudiantes
```

**SQL equivalente (sin operador de división nativo):**
```sql
-- Estudiantes que aprobaron TODAS las materias de nivel 3
SELECT e.nombre, e.apellido
FROM ESTUDIANTE e
WHERE NOT EXISTS (
    -- Existe alguna materia de nivel 3 que NO aprobó?
    SELECT 1 FROM MATERIA m
    WHERE m.nivel = 3
    AND NOT EXISTS (
        -- Está aprobada por este estudiante?
        SELECT 1 FROM INSCRIPCION i
        WHERE i.ci = e.ci
          AND i.codigo = m.codigo
          AND i.nota >= 51
    )
);
```

---

## Ejercicio resuelto — Integridad referencial: casos límite

**Escenario:** Schema CARRERA → ESTUDIANTE → INSCRIPCION (cada tabla tiene FK a la anterior)

```
CARRERA(id_carrera PK)
    ↑
ESTUDIANTE(ci PK, id_carrera FK ON DELETE RESTRICT)
    ↑
INSCRIPCION(id PK, ci FK ON DELETE CASCADE)
```

**Caso 1:** Eliminar una carrera que tiene estudiantes  
→ ERROR: `RESTRICT` en `ESTUDIANTE.id_carrera` lo impide.  
→ Solución: eliminar primero los estudiantes (que a su vez eliminan las inscripciones por CASCADE).

**Caso 2:** Eliminar un estudiante  
→ Se eliminan en cascada todas sus inscripciones.  
→ La carrera NO se ve afectada.

**Caso 3:** Cambiar el `id` de una carrera  
→ Si hay `ON UPDATE CASCADE`, todos los `id_carrera` de ESTUDIANTE se actualizan automáticamente.
→ Recomendado usar IDs surrogados (AUTOINCREMENT) para evitar este problema.

---

## Lo que más confunde en examen

**Diferencia NATURAL JOIN vs INNER JOIN:**
- `NATURAL JOIN`: une por columnas con el **mismo nombre**. Peligroso si los nombres coinciden accidentalmente.
- `INNER JOIN ... ON`: explícito y seguro. Siempre preferir este.

**Diferencia ∪ vs ⋈:**
- `∪` apila filas (necesita misma estructura)
- `⋈` multiplica columnas (necesita condición de join)

**NULL en álgebra relacional:**
- La proyección puede generar "duplicados" si hay NULL; SQL elimina duplicados solo con DISTINCT.
- `σ nota>51 (R)` **no incluye** las filas donde nota es NULL (un NULL comparado con cualquier valor da UNKNOWN, no TRUE).

---

## Preguntas de repaso frecuentes

1. ¿Qué diferencia hay entre clave primaria y clave candidata?  
   *Una relación puede tener varias claves candidatas (todas mínimas e identificadoras). La PK es la que el DBA elige como principal.*

2. ¿Puede una FK ser NULL?  
   *Sí, a menos que se declare NOT NULL. NULL indica que la relación no está establecida (ej: un empleado sin departamento asignado).*

3. ¿Qué es una superclave?  
   *Cualquier conjunto de atributos que identifica unívocamente a una tupla. La clave candidata es una superclave mínima.*

4. Explica el producto cartesiano y por qué es peligroso sin condición:  
   *R × S produce todas las combinaciones posibles. Si R tiene 1000 filas y S tiene 1000, el resultado tiene 1,000,000 filas. Sin filtro de JOIN genera datos sin sentido.*

5. ¿Qué es la división relacional?  
   *R ÷ S retorna los valores de R que están relacionados con **todos** los valores de S. Equivale al "para todos" (∀) lógico. Se implementa en SQL con doble NOT EXISTS.*
