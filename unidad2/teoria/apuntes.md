# Unidad II — Apuntes y Ejercicios Resueltos

## Reglas de mapeo ORM — Referencia rápida

| Caso | Regla de mapeo |
|------|---------------|
| Clase simple | → 1 tabla |
| Atributo simple | → 1 columna |
| Atributo multivaluado | → tabla separada con FK |
| Atributo compuesto | → expandir en columnas simples |
| Asociación 1:1 | → FK en cualquiera de los dos lados (preferir el lado opcional) |
| Asociación 1:N | → FK en el lado N |
| Asociación N:M | → tabla intermedia con las dos FK como PK compuesta |
| Herencia (opción recomendada) | → tabla por clase con FK+PK en las subclases |
| Composición | → tabla hija con CASCADE en FK |
| Agregación | → tabla hija con SET NULL o RESTRICT en FK |

---

## Ejercicio resuelto — Sistema de Reservas de Vuelos

**Diagrama de Clases:**

```
AEROLINEA (1) ──── (N) VUELO (N) ──── (M) PASAJERO
                        │                     │
                   AEROPUERTO           RESERVA (clase, precio_pagado)
                   (origen/destino)
```

**Mapeo resultante:**

```
AEROLINEA(id_aerolinea PK, nombre, codigo_iata, pais)

AEROPUERTO(id_aeropuerto PK, codigo_iata UNIQUE, nombre, ciudad, pais)

VUELO(id_vuelo PK,
      numero_vuelo UNIQUE,
      id_aerolinea FK→AEROLINEA,
      id_origen FK→AEROPUERTO,
      id_destino FK→AEROPUERTO,
      fecha_hora_salida DATETIME,
      fecha_hora_llegada DATETIME,
      capacidad INT CHECK(capacidad > 0))

PASAJERO(id_pasajero PK,
         pasaporte UNIQUE NOT NULL,
         nombre VARCHAR(100) NOT NULL,
         apellido VARCHAR(100) NOT NULL,
         nacionalidad VARCHAR(50),
         email VARCHAR(150) UNIQUE)

RESERVA(id_reserva PK,
        id_vuelo FK→VUELO ON DELETE RESTRICT,
        id_pasajero FK→PASAJERO ON DELETE RESTRICT,
        clase CHECK(clase IN ('economica','business','primera')),
        precio_pagado DECIMAL(10,2) CHECK(precio_pagado > 0),
        fecha_reserva DATE DEFAULT CURRENT_DATE,
        asiento VARCHAR(5))
```

---

## Ejercicio resuelto — Herencia: mapeo completo

**Caso:** Sistema de empleados con tipos Desarrollador y Gerente.

```
PERSONA
  ├── EMPLEADO
  │     ├── DESARROLLADOR  (lenguajes, senior: bool)
  │     └── GERENTE        (presupuesto, departamento)
  └── CLIENTE              (empresa, plan_contrato)
```

**Opción C — Tabla por clase (RECOMENDADA):**

```sql
CREATE TABLE PERSONA (
    ci          VARCHAR(10) PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    apellido    VARCHAR(100) NOT NULL,
    fecha_nac   DATE,
    tipo        VARCHAR(20) CHECK(tipo IN ('desarrollador','gerente','cliente'))
);

CREATE TABLE EMPLEADO (
    ci          VARCHAR(10) PRIMARY KEY,
    fecha_ingreso DATE NOT NULL,
    salario     DECIMAL(10,2),
    FOREIGN KEY (ci) REFERENCES PERSONA(ci) ON DELETE CASCADE
);

CREATE TABLE DESARROLLADOR (
    ci          VARCHAR(10) PRIMARY KEY,
    lenguajes   TEXT,       -- nota: en producción usar tabla separada
    senior      INTEGER DEFAULT 0,
    FOREIGN KEY (ci) REFERENCES EMPLEADO(ci) ON DELETE CASCADE
);

CREATE TABLE GERENTE (
    ci          VARCHAR(10) PRIMARY KEY,
    presupuesto DECIMAL(12,2),
    departamento VARCHAR(50),
    FOREIGN KEY (ci) REFERENCES EMPLEADO(ci) ON DELETE CASCADE
);

CREATE TABLE CLIENTE (
    ci          VARCHAR(10) PRIMARY KEY,
    empresa     VARCHAR(100),
    plan_contrato VARCHAR(20),
    FOREIGN KEY (ci) REFERENCES PERSONA(ci) ON DELETE CASCADE
);
```

**Para obtener un desarrollador completo (todos sus datos):**
```sql
SELECT p.ci, p.nombre, p.apellido, e.salario, d.lenguajes, d.senior
FROM PERSONA p
JOIN EMPLEADO e ON p.ci = e.ci
JOIN DESARROLLADOR d ON p.ci = d.ci;
```

---

## Preguntas de repaso frecuentes en examen parcial

1. ¿Cuál es la diferencia entre composición y agregación?  
   *En composición las partes no existen sin el todo (ON DELETE CASCADE). En agregación sí (ON DELETE SET NULL/RESTRICT).*

2. ¿Cuándo se crea una tabla intermedia en el mapeo?  
   *En relaciones N:M. La tabla intermedia tiene como PK compuesta las FK de ambas clases.*

3. ¿Cuáles son las 3 opciones para mapear herencia?  
   *Una tabla por jerarquía (simple pero con nulls), una tabla por clase concreta (sin nulls pero duplica atributos), una tabla por clase (recomendada: sin redundancia pero requiere JOINs).*

4. ¿Qué diferencia hay entre asociación y composición en UML?  
   *Asociación es una relación genérica. Composición (◆) implica que las partes pertenecen exclusivamente al todo y tienen el mismo ciclo de vida.*

5. ¿Un atributo multivaluado puede quedar en la misma tabla?  
   *No. Violaría 1FN. Debe crearse una tabla separada con FK a la clase original.*
