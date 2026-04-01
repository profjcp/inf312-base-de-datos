"""
Unidad II — Mapeo OO → Relacional en Python/SQLite

Demuestra cómo implementar en SQL las reglas de mapeo aprendidas:
  - Clase simple → tabla
  - Atributo multivaluado → tabla separada
  - Asociación 1:N → clave foránea
  - Asociación N:M → tabla intermedia
  - Herencia (Opción C: tabla por clase)
"""

import sqlite3

# ─── Conexión en memoria ────────────────────────────────────────────────────

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")   # activar integridad referencial
cur = conn.cursor()

# ─── 1. Clase simple → tabla ─────────────────────────────────────────────────

cur.executescript("""
    -- Regla 1: cada clase se convierte en una tabla
    CREATE TABLE CARRERA (
        id_carrera  INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre      VARCHAR(100) NOT NULL UNIQUE,
        duracion    INTEGER CHECK(duracion BETWEEN 3 AND 6)
    );

    -- Regla 2: asociación 1:N — FK en el lado N
    CREATE TABLE ESTUDIANTE (
        ci          VARCHAR(10)  PRIMARY KEY,
        nombre      VARCHAR(100) NOT NULL,
        apellido    VARCHAR(100) NOT NULL,
        fecha_nac   DATE,
        email       VARCHAR(150) UNIQUE,
        id_carrera  INTEGER REFERENCES CARRERA(id_carrera) ON DELETE RESTRICT
    );

    -- Atributo multivaluado: un estudiante puede tener varios teléfonos
    CREATE TABLE ESTUDIANTE_TELEFONO (
        ci          VARCHAR(10)  REFERENCES ESTUDIANTE(ci) ON DELETE CASCADE,
        telefono    VARCHAR(15)  NOT NULL,
        tipo        VARCHAR(10)  DEFAULT 'celular',
        PRIMARY KEY (ci, telefono)
    );
""")

print("✓ Tablas con asociación 1:N creadas")

# ─── 2. Asociación N:M → tabla intermedia ────────────────────────────────────

cur.executescript("""
    CREATE TABLE MATERIA (
        codigo   VARCHAR(10)  PRIMARY KEY,
        nombre   VARCHAR(150) NOT NULL,
        creditos INTEGER      CHECK(creditos > 0),
        nivel    INTEGER      CHECK(nivel BETWEEN 1 AND 10)
    );

    -- Tabla intermedia con atributo propio (nota, gestion)
    CREATE TABLE INSCRIPCION (
        id_inscripcion INTEGER PRIMARY KEY AUTOINCREMENT,
        ci             VARCHAR(10) REFERENCES ESTUDIANTE(ci) ON DELETE CASCADE,
        codigo         VARCHAR(10) REFERENCES MATERIA(codigo) ON DELETE RESTRICT,
        gestion        VARCHAR(10) NOT NULL,
        nota           DECIMAL(5,2) CHECK(nota IS NULL OR (nota >= 0 AND nota <= 100)),
        UNIQUE(ci, codigo, gestion)   -- un estudiante no puede inscribirse dos veces en la misma materia/gestión
    );
""")

print("✓ Tabla intermedia N:M (INSCRIPCION) creada")

# ─── 3. Herencia — Opción C: tabla por clase ─────────────────────────────────

cur.executescript("""
    -- Superclase
    CREATE TABLE PERSONA (
        ci      VARCHAR(10) PRIMARY KEY,
        nombre  VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        tipo    VARCHAR(20)  CHECK(tipo IN ('estudiante', 'docente', 'administrativo'))
    );

    -- Subclase DOCENTE: ci es PK y FK a PERSONA (mismo identificador)
    CREATE TABLE DOCENTE (
        ci           VARCHAR(10) PRIMARY KEY,
        especialidad VARCHAR(100),
        categoria    VARCHAR(50),
        email        VARCHAR(150) UNIQUE,
        FOREIGN KEY (ci) REFERENCES PERSONA(ci) ON DELETE CASCADE
    );

    -- Subclase ADMINISTRATIVO
    CREATE TABLE ADMINISTRATIVO (
        ci      VARCHAR(10) PRIMARY KEY,
        cargo   VARCHAR(100),
        salario DECIMAL(10,2),
        FOREIGN KEY (ci) REFERENCES PERSONA(ci) ON DELETE CASCADE
    );
""")

print("✓ Herencia (tabla por clase) implementada")

# ─── Insertar datos de prueba ─────────────────────────────────────────────────

cur.executescript("""
    INSERT INTO CARRERA VALUES
        (1, 'Ingeniería en Sistemas', 5),
        (2, 'Ingeniería en Redes y Telecomunicaciones', 5),
        (3, 'Ingeniería en Ciencias de la Computación', 5);

    INSERT INTO MATERIA VALUES
        ('INF312', 'Base de Datos I', 5, 5),
        ('INF220', 'Programación II',  4, 3),
        ('MAT101', 'Matemáticas I',    5, 1);

    INSERT INTO ESTUDIANTE(ci, nombre, apellido, fecha_nac, id_carrera) VALUES
        ('7654321', 'Ana',   'García',  '2000-03-15', 1),
        ('8123456', 'Luis',  'Mamani',  '1999-07-22', 1),
        ('9234567', 'María', 'López',   '2001-01-05', 2);

    INSERT INTO ESTUDIANTE_TELEFONO VALUES
        ('7654321', '71234567', 'celular'),
        ('7654321', '33445566', 'fijo'),
        ('8123456', '72345678', 'celular');

    INSERT INTO INSCRIPCION(ci, codigo, gestion, nota) VALUES
        ('7654321', 'INF312', '2024-I', 85.0),
        ('7654321', 'INF220', '2023-II', 70.5),
        ('8123456', 'INF312', '2024-I', NULL),  -- cursando
        ('9234567', 'MAT101', '2024-I', 60.0);
""")

conn.commit()
print("✓ Datos de prueba insertados")

# ─── Consultas de verificación ────────────────────────────────────────────────

print("\n--- Relación 1:N: Estudiantes por carrera ---")
for row in cur.execute("""
    SELECT c.nombre AS carrera, COUNT(e.ci) AS total
    FROM CARRERA c
    LEFT JOIN ESTUDIANTE e ON c.id_carrera = e.id_carrera
    GROUP BY c.id_carrera, c.nombre
"""):
    print(f"  {row[0]}: {row[1]} estudiante(s)")

print("\n--- Relación N:M con atributo: Inscripciones ---")
for row in cur.execute("""
    SELECT e.nombre || ' ' || e.apellido AS estudiante,
           m.nombre AS materia, i.gestion,
           COALESCE(CAST(i.nota AS TEXT), 'cursando') AS nota
    FROM INSCRIPCION i
    JOIN ESTUDIANTE e ON i.ci     = e.ci
    JOIN MATERIA    m ON i.codigo = m.codigo
    ORDER BY estudiante, m.nombre
"""):
    print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]}")

print("\n--- Atributo multivaluado: Teléfonos ---")
for row in cur.execute("""
    SELECT e.nombre, t.telefono, t.tipo
    FROM ESTUDIANTE_TELEFONO t
    JOIN ESTUDIANTE e ON t.ci = e.ci
    ORDER BY e.nombre
"""):
    print(f"  {row[0]}: {row[1]} ({row[2]})")

# ─── Demostrar integridad referencial ─────────────────────────────────────────

print("\n--- Prueba de integridad referencial ---")
try:
    cur.execute("INSERT INTO INSCRIPCION(ci, codigo, gestion) VALUES('9999999', 'INF312', '2024-I')")
    print("  ✗ ERROR: Se insertó un CI que no existe en ESTUDIANTE")
except sqlite3.IntegrityError as e:
    print(f"  ✓ FK correctamente rechazada: {e}")

conn.close()
print("\n✓ Ejecución completada. BD en memoria cerrada.")
