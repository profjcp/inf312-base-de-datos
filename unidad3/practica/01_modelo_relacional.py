"""
Unidad III — Restricciones e integridad relacional en Python/SQLite

Demuestra:
  - Restricciones de dominio (CHECK, NOT NULL, UNIQUE)
  - Integridad de entidades (PK no nula)
  - Integridad referencial (FK, ON DELETE, ON UPDATE)
  - Prueba de cada tipo de violación
"""

import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

# ─── Crear esquema con restricciones ─────────────────────────────────────────

cur.executescript("""
    CREATE TABLE CARRERA (
        id_carrera INTEGER PRIMARY KEY,
        nombre     VARCHAR(100) NOT NULL UNIQUE
    );

    CREATE TABLE ESTUDIANTE (
        ci          VARCHAR(10)  PRIMARY KEY,
        nombre      VARCHAR(100) NOT NULL,
        apellido    VARCHAR(100) NOT NULL,
        nota_prom   DECIMAL(5,2) CHECK(nota_prom IS NULL OR (nota_prom >= 0 AND nota_prom <= 100)),
        email       VARCHAR(150) UNIQUE,
        id_carrera  INTEGER REFERENCES CARRERA(id_carrera) ON DELETE RESTRICT ON UPDATE CASCADE
    );

    CREATE TABLE MATERIA (
        codigo   VARCHAR(10)  PRIMARY KEY,
        nombre   VARCHAR(150) NOT NULL,
        creditos INTEGER      NOT NULL CHECK(creditos > 0),
        nivel    INTEGER      NOT NULL CHECK(nivel BETWEEN 1 AND 10)
    );

    CREATE TABLE INSCRIPCION (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        ci       VARCHAR(10) NOT NULL REFERENCES ESTUDIANTE(ci) ON DELETE CASCADE,
        codigo   VARCHAR(10) NOT NULL REFERENCES MATERIA(codigo) ON DELETE RESTRICT,
        gestion  VARCHAR(10) NOT NULL,
        nota     DECIMAL(5,2) CHECK(nota IS NULL OR (nota >= 0 AND nota <= 100))
    );
""")

# Datos base
cur.executescript("""
    INSERT INTO CARRERA VALUES (1, 'Sistemas'),(2, 'Redes');
    INSERT INTO MATERIA VALUES ('INF312', 'Base de Datos I', 5, 5);
    INSERT INTO ESTUDIANTE(ci, nombre, apellido, id_carrera)
        VALUES ('7654321', 'Ana', 'García', 1),
               ('8123456', 'Luis', 'Mamani', 1);
    INSERT INTO INSCRIPCION(ci, codigo, gestion, nota) VALUES ('7654321', 'INF312', '2024-I', 85);
""")
conn.commit()

def probar(descripcion, sql, params=()):
    """Ejecuta una operación y muestra si tuvo éxito o fue rechazada."""
    try:
        cur.execute(sql, params)
        conn.commit()
        print(f"  ✓ PERMITIDO: {descripcion}")
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f"  ✗ RECHAZADO [{type(e).__name__}]: {descripcion}")
        print(f"    → {e}")

# ─── 1. Integridad de entidad (PK nunca NULL) ─────────────────────────────────

print("\n=== 1. Integridad de entidad (PK no puede ser NULL) ===")
probar("Insertar estudiante con CI válido",
       "INSERT INTO ESTUDIANTE(ci, nombre, apellido, id_carrera) VALUES('9999999','Pedro','Rojas',1)")
probar("Insertar estudiante con CI duplicado",
       "INSERT INTO ESTUDIANTE(ci, nombre, apellido, id_carrera) VALUES('7654321','Otro','Nombre',1)")
probar("Insertar carrera con nombre duplicado (UNIQUE)",
       "INSERT INTO CARRERA VALUES(3, 'Sistemas')")

# ─── 2. Restricción de dominio (CHECK) ───────────────────────────────────────

print("\n=== 2. Restricciones de dominio (CHECK) ===")
probar("Insertar nota válida (85.0)",
       "INSERT INTO INSCRIPCION(ci, codigo, gestion, nota) VALUES('8123456','INF312','2024-I',85.0)")
probar("Insertar nota inválida (120 > 100)",
       "INSERT INTO INSCRIPCION(ci, codigo, gestion, nota) VALUES('9999999','INF312','2024-II',120)")
probar("Insertar nivel de materia inválido (15 > 10)",
       "INSERT INTO MATERIA VALUES('MAT999','Prueba',3,15)")
probar("Insertar nota NULL (permitida: significa 'cursando')",
       "INSERT INTO INSCRIPCION(ci, codigo, gestion, nota) VALUES('9999999','INF312','2024-II',NULL)")

# ─── 3. Integridad referencial ────────────────────────────────────────────────

print("\n=== 3. Integridad referencial (FK) ===")
probar("Insertar inscripción con CI que no existe",
       "INSERT INTO INSCRIPCION(ci, codigo, gestion) VALUES('0000000','INF312','2024-I')")
probar("Insertar inscripción con código de materia inexistente",
       "INSERT INTO INSCRIPCION(ci, codigo, gestion) VALUES('7654321','XXX999','2024-I')")

# ─── 4. ON DELETE RESTRICT ───────────────────────────────────────────────────

print("\n=== 4. ON DELETE RESTRICT (no puede borrarse si tiene hijos) ===")
probar("Borrar materia INF312 (tiene inscripciones → RESTRICT)",
       "DELETE FROM MATERIA WHERE codigo = 'INF312'")
probar("Borrar carrera 1 (tiene estudiantes → RESTRICT)",
       "DELETE FROM CARRERA WHERE id_carrera = 1")

# ─── 5. ON DELETE CASCADE ────────────────────────────────────────────────────

print("\n=== 5. ON DELETE CASCADE (borrar estudiante elimina sus inscripciones) ===")
antes = cur.execute("SELECT COUNT(*) FROM INSCRIPCION WHERE ci='7654321'").fetchone()[0]
print(f"  Inscripciones de 7654321 antes: {antes}")
cur.execute("DELETE FROM ESTUDIANTE WHERE ci='7654321'")
conn.commit()
despues = cur.execute("SELECT COUNT(*) FROM INSCRIPCION WHERE ci='7654321'").fetchone()[0]
print(f"  Inscripciones de 7654321 después: {despues}  (CASCADE funcionó ✓)")

# ─── 6. ON UPDATE CASCADE ────────────────────────────────────────────────────

print("\n=== 6. ON UPDATE CASCADE (cambiar id_carrera actualiza estudiantes) ===")
carrera_antes = cur.execute("SELECT id_carrera FROM ESTUDIANTE WHERE ci='8123456'").fetchone()[0]
print(f"  id_carrera de 8123456 antes: {carrera_antes}")
cur.execute("UPDATE CARRERA SET id_carrera=10 WHERE id_carrera=1")
conn.commit()
carrera_despues = cur.execute("SELECT id_carrera FROM ESTUDIANTE WHERE ci='8123456'").fetchone()[0]
print(f"  id_carrera de 8123456 después: {carrera_despues}  (CASCADE funcionó ✓)")

conn.close()
print("\n✓ Demostración de integridad relacional completada.")
