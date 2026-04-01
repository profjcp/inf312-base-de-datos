# Unidad V — Apuntes y Ejercicios Resueltos

## Proceso de normalización — Referencia rápida

```
¿Tiene atributos multivaluados o no atómicos?
        │ SÍ → Separar en tabla propia con FK
        ▼
       1FN ✓
        │
¿Hay atributos que dependen solo de PARTE de la PK compuesta?
        │ SÍ → Mover esos atributos a tabla separada
        ▼
       2FN ✓
        │
¿Hay atributos no-clave que dependen de OTRO atributo no-clave?
        │ SÍ (dependencia transitiva) → Separar en tabla propia
        ▼
       3FN ✓  ← Objetivo estándar
        │
¿Hay dependencias funcionales X→Y donde X NO es superclave?
        │ SÍ → Descomponer (posible pérdida de dependencias)
        ▼
      FNBC ✓  ← Recomendado en tablas con claves candidatas superpuestas
```

---

## Reglas de Armstrong (inferencia de DFs)

Las reglas de Armstrong permiten derivar todas las DFs a partir de un conjunto dado:

| Regla | Descripción | Ejemplo |
|-------|-------------|---------|
| **Reflexividad** | Si Y ⊆ X, entonces X → Y | {ci, nombre} → nombre |
| **Aumentatividad** | Si X → Y, entonces XZ → YZ | ci→nombre ⟹ ci,gestion → nombre,gestion |
| **Transitividad** | Si X→Y y Y→Z, entonces X→Z | ci→id_carrera y id_carrera→nombre_carrera ⟹ ci→nombre_carrera |
| **Unión** | Si X→Y y X→Z, entonces X→YZ | ci→nombre y ci→apellido ⟹ ci→nombre,apellido |
| **Descomposición** | Si X→YZ, entonces X→Y y X→Z | ci→nombre,apellido ⟹ ci→nombre |
| **Pseudotransitividad** | Si X→Y y WY→Z, entonces WX→Z | — |

---

## Ejercicio resuelto — Cierre de atributos

**Dado:** F = {A→B, B→C, A→D, D→E}

Calcular A⁺ (el cierre de A bajo F):

```
Inicio: A⁺ = {A}

A→B:  A ∈ A⁺, por tanto añadir B   → A⁺ = {A, B}
B→C:  B ∈ A⁺, por tanto añadir C   → A⁺ = {A, B, C}
A→D:  A ∈ A⁺, por tanto añadir D   → A⁺ = {A, B, C, D}
D→E:  D ∈ A⁺, por tanto añadir E   → A⁺ = {A, B, C, D, E}

Conclusión: A determina todos los atributos → A es clave candidata.
```

---

## Ejercicio resuelto — Normalización paso a paso

**Tabla original (0FN):**
```
BIBLIOTECA(isbn, titulo, anio, autores, editorial, ciudad_editorial, telefonos_editorial)
```

**Identificar DFs:**
```
isbn → titulo, anio, editorial, ciudad_editorial
isbn →→ autores              (multivaluado)
isbn →→ telefonos_editorial  (multivaluado)
editorial → ciudad_editorial  (transitiva)
```

**→ 1FN:** Eliminar multivaluados
```
LIBRO(isbn PK, titulo, anio, editorial, ciudad_editorial)
LIBRO_AUTOR(isbn FK, autor)                    PK: (isbn, autor)
EDITORIAL_TELEFONO(editorial, telefono)         PK: (editorial, telefono)
```

**→ 2FN:** (PK simples → ya cumple 2FN automáticamente)  
Sin cambios necesarios.

**→ 3FN:** Eliminar dependencia transitiva `editorial → ciudad_editorial`
```
LIBRO(isbn PK, titulo, anio, editorial FK)
EDITORIAL(editorial PK, ciudad)
LIBRO_AUTOR(isbn FK, autor)
EDITORIAL_TELEFONO(editorial FK, telefono)
```

**Verificación final:** Cada no-clave depende directa y únicamente de su PK. ✓

---

## Preguntas de repaso frecuentes

1. ¿Puede una tabla estar en 1FN y tener dependencias parciales?  
   *Sí. 2FN solo aplica cuando la PK es compuesta; una tabla con PK simple en 1FN ya está en 2FN automáticamente.*

2. ¿La normalización siempre mejora el rendimiento?  
   *No. Más tablas = más JOINs. En sistemas con lectura masiva puede convenir desnormalizar estratégicamente.*

3. ¿Cuál es la diferencia práctica entre 3FN y FNBC?  
   *FNBC es más estricta: en 3FN se permite X→Y si Y es atributo primo (parte de alguna clave candidata). FNBC no lo permite.*

4. ¿Qué es una dependencia funcional trivial?  
   *X→Y donde Y ⊆ X. Siempre se cumple y no aporta información. Ej: {ci, nombre} → ci.*

5. ¿Puede perderse información al normalizar?  
   *No si la descomposición tiene la propiedad de reunión sin pérdida (lossless join). Siempre verificar que la intersección de los esquemas determine al menos uno de los dos.*
