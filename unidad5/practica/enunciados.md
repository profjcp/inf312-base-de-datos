# Unidad V — Ejercicios Prácticos

> **Archivo de referencia:** [`01_normalizacion.py`](./01_normalizacion.py)

---

## Ejercicio 1 — Dependencias funcionales

Para cada caso, identifica **todas** las dependencias funcionales y determina las claves candidatas:

**a)** `VUELO(num_vuelo, fecha, origen, destino, avion, piloto, capacidad)`

Suposiciones: un piloto vuela en un avión a la vez; un avión tiene una capacidad fija; en una fecha + origen puede haber varios vuelos.

**b)** `PRODUCTO(cod_prod, nombre, id_proveedor, nombre_proveedor, precio, stock)`

**c)** `EMPLEADO(ci, nombre, id_depto, nombre_depto, id_proyecto, horas_proyecto)`

---

## Ejercicio 2 — Primera Forma Normal (1FN)

Normaliza a 1FN las siguientes tablas. Para cada una, explica qué violación existía y cómo la resolviste:

**a)**
```
CLIENTE(id, nombre, telefonos)
Ejemplo: (1, 'Ana García', '71234567, 72345678')
```

**b)**
```
PEDIDO(id_pedido, fecha, cliente, productos)
Ejemplo: (101, '2024-01-15', 'Luis Mamani', 'Laptop x1, Mouse x2, Teclado x1')
```

**c)**
```
EMPLEADO(ci, nombre, habilidades, cargo_actual_y_anterior)
Ejemplo: ('123', 'Pedro', 'Python,SQL,Java', 'Analista (2020-2022), Desarrollador (2022-hoy)')
```

---

## Ejercicio 3 — Segunda Forma Normal (2FN)

Las siguientes tablas están en 1FN pero **no** están en 2FN. Identifica las dependencias parciales y descompón adecuadamente:

**a)**
```
INSCRIPCION_COMPLETA(ci, codigo_mat, gestion, nota, nombre_estudiante, creditos_materia, nivel_materia)
PK: (ci, codigo_mat, gestion)
```

**b)**
```
VENTA_DETALLE(id_venta, cod_producto, cantidad, precio_unitario, nombre_producto, categoria_producto, nombre_cliente, fecha_venta)
PK: (id_venta, cod_producto)
```

**c)**
```
ASISTENCIA(ci_emp, fecha, id_proyecto, nombre_proyecto, horas, nombre_empleado, departamento_empleado)
PK: (ci_emp, fecha, id_proyecto)
```

---

## Ejercicio 4 — Tercera Forma Normal (3FN)

Las siguientes tablas están en 2FN pero **no** en 3FN. Identifica las dependencias transitivas y corrige:

**a)**
```
EMPLEADO(ci, nombre, id_depto, nombre_depto, ciudad_depto, jefe_depto)
PK: ci
```

**b)**
```
ESTUDIANTE(ci, nombre, cod_postal, ciudad, departamento)
PK: ci
(Se sabe que: cod_postal → ciudad, cod_postal → departamento)
```

**c)**
```
PRODUCTO(id_prod, nombre, id_categoria, nombre_categoria, id_proveedor, nombre_proveedor, pais_proveedor)
PK: id_prod
```

---

## Ejercicio 5 — Forma Normal de Boyce-Codd (FNBC)

**a)** La siguiente tabla está en 3FN pero **NO** en FNBC. Identifica por qué y corrige:

```
HORARIO(estudiante, materia, tutor)

Restricciones del dominio:
- Un estudiante tiene un único tutor por materia
- Un tutor solo enseña una materia

Claves candidatas: {estudiante, materia} y {estudiante, tutor}
Dependencia problemática: tutor → materia
```

**b)** ¿Cuándo una tabla está en 3FN pero NO en FNBC? Describe la condición en tus propias palabras.

**c)** ¿Siempre es posible descomponer una tabla en FNBC sin perder información y sin perder dependencias? Investiga y explica el "dilema de la FNBC".

---

## Ejercicio 6 — Proceso completo de normalización

Normaliza completamente la siguiente tabla desde 0FN hasta 3FN. Muestra cada paso con la tabla resultante:

```
FACTURA_VENTA (tabla sin normalizar):
┌──────────┬────────────┬───────────────┬─────────────────┬────────────────────────────────────────────────┐
│ id_fact  │ fecha      │ cliente_ci    │ nombre_cliente  │ productos                                      │
├──────────┼────────────┼───────────────┼─────────────────┼────────────────────────────────────────────────┤
│ F001     │ 2024-01-10 │ 7654321       │ Ana García      │ Laptop($800,1), Mouse($15,2), Teclado($25,1)  │
│ F002     │ 2024-01-11 │ 8123456       │ Luis Mamani     │ Monitor($350,2)                                │
└──────────┴────────────┴───────────────┴─────────────────┴────────────────────────────────────────────────┘

Datos adicionales conocidos:
- cliente_ci determina nombre_cliente (y también dirección, teléfono)
- cod_producto determina nombre, precio_unitario, categoria
- (id_fact, cod_producto) determina cantidad
```

Para cada paso muestra: la tabla antes, el problema identificado, y las tablas resultantes.

---

## Ejercicio 7 — Desnormalización justificada

La normalización maximiza la integridad, pero a veces se **desnormaliza** intencionalmente para mejorar el rendimiento.

**a)** La siguiente vista se consulta millones de veces al día:
```sql
SELECT e.nombre, e.apellido, c.nombre AS carrera,
       COUNT(i.id_insc) AS materias, AVG(i.nota) AS promedio
FROM ESTUDIANTE e
JOIN CARRERA c ON e.id_carrera = c.id_carrera
LEFT JOIN INSCRIPCION i ON e.ci = i.ci
GROUP BY e.ci, e.nombre, e.apellido, c.nombre;
```
¿Cómo desnormalizarías el esquema para acelerar esta consulta? ¿Qué columna agregarías y a qué tabla?

**b)** Una tabla `ORDEN` con millones de registros tiene FK a `CLIENTE(id, nombre, ciudad)`. La aplicación siempre muestra el nombre y ciudad del cliente junto con la orden.
- ¿Tiene sentido desnormalizar guardando `nombre_cliente` y `ciudad_cliente` directamente en `ORDEN`?
- ¿Qué riesgos introduce esta decisión?

**c)** Investiga qué es una **tabla de resumen** (summary table) y da un ejemplo práctico de cuándo conviene crearla.

---

## Ejercicio 8 — Desafío integrador

Dado el siguiente requerimiento:

> Una plataforma de e-learning registra: **cursos** (título, descripción, nivel, precio), **instructores** (nombre, email, país, especialidades), **alumnos** (nombre, email, país, fecha_registro), **inscripciones** de alumnos a cursos (con fecha y precio pagado que puede diferir del precio actual), **lecciones** de cada curso (título, duración en minutos, orden), y **progreso** de cada alumno en cada lección (completado: sí/no, fecha_completado).

**a)** Modela la BD (esquema relacional completo)  
**b)** Identifica las dependencias funcionales de cada tabla  
**c)** Verifica que el esquema esté en 3FN. Si no, corrígelo  
**d)** Escribe 5 consultas SQL no triviales sobre este esquema  
**e)** Identifica dónde podría convenir desnormalizar y por qué
