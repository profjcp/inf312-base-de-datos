# Unidad IV — Apuntes y Ejercicios Resueltos

## SQL: Referencia rápida de sintaxis

```sql
-- Estructura completa de un SELECT
SELECT  [DISTINCT] col1, col2, expresión AS alias
FROM    tabla1 t1
  [INNER | LEFT | RIGHT] JOIN tabla2 t2 ON t1.col = t2.col
WHERE   condicion_fila
GROUP BY col1, col2
HAVING  condicion_grupo
ORDER BY col1 [ASC|DESC], col2
LIMIT   n OFFSET m;
```

**Orden de ejecución lógica** (no el orden de escritura):
1. `FROM` + `JOIN`  → construye la tabla combinada
2. `WHERE`          → filtra filas individuales
3. `GROUP BY`       → agrupa
4. `HAVING`         → filtra grupos
5. `SELECT`         → proyecta columnas
6. `DISTINCT`       → elimina duplicados
7. `ORDER BY`       → ordena
8. `LIMIT/OFFSET`   → recorta

> **Truco de examen:** `WHERE` no puede usar alias definidos en `SELECT` porque WHERE se ejecuta antes. `HAVING` sí puede (se ejecuta después de `SELECT`).

---

## Ejercicio resuelto — JOINs encadenados

**Consulta:** Listar nombre del estudiante, carrera, materia y nota de todos los aprobados en la gestión '2024-I'.

```sql
SELECT
    e.nombre || ' ' || e.apellido  AS estudiante,
    c.nombre                        AS carrera,
    m.nombre                        AS materia,
    i.nota
FROM INSCRIPCION i
INNER JOIN ESTUDIANTE e ON i.ci        = e.ci
INNER JOIN MATERIA    m ON i.codigo    = m.codigo
INNER JOIN CARRERA    c ON e.id_carrera = c.id_carrera
WHERE i.gestion = '2024-I'
  AND i.nota    >= 51
ORDER BY c.nombre, e.apellido, e.nombre;
```

---

## Ejercicio resuelto — CTE con múltiples pasos

**Consulta:** Encontrar las 3 materias con mayor tasa de reprobación (nota < 51).

```sql
WITH stats AS (
    SELECT
        codigo,
        COUNT(*)                                          AS total,
        SUM(CASE WHEN nota < 51  THEN 1 ELSE 0 END)     AS reprobados,
        SUM(CASE WHEN nota >= 51 THEN 1 ELSE 0 END)     AS aprobados
    FROM INSCRIPCION
    WHERE nota IS NOT NULL
    GROUP BY codigo
),
porcentajes AS (
    SELECT
        s.codigo,
        m.nombre,
        s.total,
        s.reprobados,
        ROUND(100.0 * s.reprobados / s.total, 1) AS pct_reprobacion
    FROM stats s
    JOIN MATERIA m ON s.codigo = m.codigo
    WHERE s.total >= 5   -- solo materias con suficientes datos
)
SELECT *
FROM porcentajes
ORDER BY pct_reprobacion DESC
LIMIT 3;
```

---

## Ejercicio resuelto — Función de ventana

**Consulta:** Para cada inscripción, mostrar la nota del estudiante, el promedio de su materia, y qué tanto se aleja del promedio.

```sql
SELECT
    e.nombre || ' ' || e.apellido                    AS estudiante,
    m.nombre                                          AS materia,
    i.nota,
    ROUND(AVG(i.nota) OVER (PARTITION BY i.codigo), 1) AS promedio_materia,
    ROUND(i.nota - AVG(i.nota) OVER (PARTITION BY i.codigo), 1) AS diferencia,
    RANK() OVER (PARTITION BY i.codigo ORDER BY i.nota DESC)    AS puesto
FROM INSCRIPCION i
JOIN ESTUDIANTE e ON i.ci     = e.ci
JOIN MATERIA    m ON i.codigo = m.codigo
WHERE i.nota IS NOT NULL
ORDER BY m.nombre, puesto;
```

---

## Ejercicio resuelto — Transacción con manejo de error en Python

```python
import sqlite3

def transferir(conn, cuenta_origen, cuenta_destino, monto):
    try:
        conn.execute("BEGIN")
        # Verificar saldo suficiente
        saldo = conn.execute(
            "SELECT saldo FROM CUENTA WHERE id = ?", (cuenta_origen,)
        ).fetchone()[0]

        if saldo < monto:
            raise ValueError(f"Saldo insuficiente: {saldo} < {monto}")

        conn.execute(
            "UPDATE CUENTA SET saldo = saldo - ? WHERE id = ?",
            (monto, cuenta_origen)
        )
        conn.execute(
            "UPDATE CUENTA SET saldo = saldo + ? WHERE id = ?",
            (monto, cuenta_destino)
        )
        conn.execute("COMMIT")
        print(f"Transferencia de ${monto} exitosa.")

    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"Error: {e}. Transacción revertida.")
        raise
```

> **Nota de seguridad:** Siempre usar parámetros (`?`) en lugar de f-strings para evitar SQL Injection.

---

## Errores comunes en examen

| Error | Consecuencia | Corrección |
|-------|-------------|------------|
| `WHERE` con función de agregación | Error de sintaxis | Usar `HAVING` |
| `GROUP BY` sin incluir todas las columnas no agregadas de `SELECT` | Error o resultado incorrecto | Incluir todas las columnas no agregadas |
| `JOIN` sin condición `ON` | Producto cartesiano inesperado | Siempre especificar la condición |
| `UPDATE` sin `WHERE` | Actualiza todas las filas | Verificar con `SELECT` antes |
| Comparar con `= NULL` en vez de `IS NULL` | Siempre devuelve FALSE | Usar `IS NULL` / `IS NOT NULL` |
| `BETWEEN` con orden invertido (`BETWEEN 100 AND 50`) | Retorna 0 filas | El menor siempre primero |
