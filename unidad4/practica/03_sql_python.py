"""
Unidad IV — SQL desde Python con sqlite3

Demuestra la conexión entre una aplicación Python y SQLite:
  - Crear y conectar a una BD
  - CRUD completo con parámetros (previene SQL Injection)
  - Transacciones: commit y rollback
  - Manejo de errores
  - Consultas parametrizadas seguras
"""

import sqlite3
import os

DB_PATH = "universidad_practica.db"

# ─── Conexión y setup ─────────────────────────────────────────────────────────

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.isolation_level = None   # modo autocommit: transacciones manuales
    conn.row_factory = sqlite3.Row   # las filas se comportan como diccionarios
    return conn

def crear_esquema(conn):
    conn.execute("BEGIN")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS CARRERA (
            id_carrera INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre     VARCHAR(100) NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS ESTUDIANTE (
            ci          VARCHAR(10)  PRIMARY KEY,
            nombre      VARCHAR(100) NOT NULL,
            apellido    VARCHAR(100) NOT NULL,
            email       VARCHAR(150) UNIQUE,
            id_carrera  INTEGER REFERENCES CARRERA(id_carrera)
        );
        CREATE TABLE IF NOT EXISTS MATERIA (
            codigo   VARCHAR(10)  PRIMARY KEY,
            nombre   VARCHAR(150) NOT NULL,
            creditos INTEGER CHECK(creditos > 0)
        );
        CREATE TABLE IF NOT EXISTS INSCRIPCION (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            ci       VARCHAR(10) REFERENCES ESTUDIANTE(ci) ON DELETE CASCADE,
            codigo   VARCHAR(10) REFERENCES MATERIA(codigo),
            gestion  VARCHAR(10) NOT NULL,
            nota     DECIMAL(5,2) CHECK(nota IS NULL OR (nota BETWEEN 0 AND 100))
        );
    """)
    # executescript hace COMMIT automáticamente

# ─── CRUD: Estudiantes ────────────────────────────────────────────────────────

def insertar_estudiante(conn, ci, nombre, apellido, email, id_carrera):
    """
    Usa parámetros posicionales (?) para evitar SQL Injection.
    NUNCA usar f-strings o concatenación de strings para construir SQL.
    """
    try:
        conn.execute(
            "INSERT INTO ESTUDIANTE(ci, nombre, apellido, email, id_carrera) VALUES(?,?,?,?,?)",
            (ci, nombre, apellido, email, id_carrera)
        )
        print(f"  ✓ Estudiante {nombre} {apellido} registrado.")
    except sqlite3.IntegrityError as e:
        print(f"  ✗ Error al insertar estudiante: {e}")

def buscar_estudiante(conn, ci):
    """Retorna un estudiante por CI, o None si no existe."""
    row = conn.execute(
        "SELECT e.*, c.nombre AS carrera FROM ESTUDIANTE e "
        "LEFT JOIN CARRERA c ON e.id_carrera = c.id_carrera "
        "WHERE e.ci = ?",
        (ci,)
    ).fetchone()
    return dict(row) if row else None

def listar_estudiantes(conn, id_carrera=None):
    """Lista estudiantes, opcionalmente filtrados por carrera."""
    if id_carrera:
        rows = conn.execute(
            "SELECT ci, nombre, apellido FROM ESTUDIANTE WHERE id_carrera = ? ORDER BY apellido",
            (id_carrera,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT ci, nombre, apellido FROM ESTUDIANTE ORDER BY apellido"
        ).fetchall()
    return [dict(r) for r in rows]

def actualizar_email(conn, ci, nuevo_email):
    affected = conn.execute(
        "UPDATE ESTUDIANTE SET email = ? WHERE ci = ?",
        (nuevo_email, ci)
    ).rowcount
    if affected:
        print(f"  ✓ Email actualizado para CI {ci}")
    else:
        print(f"  ✗ No se encontró estudiante con CI {ci}")

def eliminar_estudiante(conn, ci):
    affected = conn.execute("DELETE FROM ESTUDIANTE WHERE ci = ?", (ci,)).rowcount
    if affected:
        print(f"  ✓ Estudiante {ci} eliminado (inscripciones eliminadas por CASCADE).")
    else:
        print(f"  ✗ No se encontró estudiante {ci}.")

# ─── Transacciones ────────────────────────────────────────────────────────────

def registrar_nota(conn, ci, codigo, gestion, nota):
    """
    Registra o actualiza una nota dentro de una transacción.
    Si falla cualquier paso, se hace ROLLBACK.
    """
    try:
        conn.execute("BEGIN")

        # Verificar que existe el estudiante
        est = conn.execute("SELECT ci FROM ESTUDIANTE WHERE ci=?", (ci,)).fetchone()
        if not est:
            raise ValueError(f"Estudiante con CI {ci} no existe.")

        # Verificar que existe la materia
        mat = conn.execute("SELECT codigo FROM MATERIA WHERE codigo=?", (codigo,)).fetchone()
        if not mat:
            raise ValueError(f"Materia {codigo} no existe.")

        # Insertar o actualizar inscripción
        existe = conn.execute(
            "SELECT id FROM INSCRIPCION WHERE ci=? AND codigo=? AND gestion=?",
            (ci, codigo, gestion)
        ).fetchone()

        if existe:
            conn.execute(
                "UPDATE INSCRIPCION SET nota=? WHERE ci=? AND codigo=? AND gestion=?",
                (nota, ci, codigo, gestion)
            )
            accion = "actualizada"
        else:
            conn.execute(
                "INSERT INTO INSCRIPCION(ci, codigo, gestion, nota) VALUES(?,?,?,?)",
                (ci, codigo, gestion, nota)
            )
            accion = "registrada"

        conn.execute("COMMIT")
        print(f"  ✓ Nota {nota} {accion} para {ci} en {codigo} ({gestion}).")

    except (sqlite3.Error, ValueError) as e:
        conn.execute("ROLLBACK")
        print(f"  ✗ Transacción revertida: {e}")

# ─── Consultas con resultados ─────────────────────────────────────────────────

def promedio_por_materia(conn):
    return conn.execute("""
        SELECT m.nombre AS materia,
               ROUND(AVG(i.nota), 1) AS promedio,
               COUNT(*) AS total_inscritos
        FROM MATERIA m
        LEFT JOIN INSCRIPCION i ON m.codigo = i.codigo AND i.nota IS NOT NULL
        GROUP BY m.codigo, m.nombre
        ORDER BY promedio DESC
    """).fetchall()

# ─── Programa principal ───────────────────────────────────────────────────────

if __name__ == "__main__":
    # Limpiar BD anterior si existe
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = conectar()
    crear_esquema(conn)

    print("=== Insertar datos ===")
    conn.execute("INSERT INTO CARRERA(nombre) VALUES('Sistemas'),('Redes')")
    conn.execute("INSERT INTO MATERIA VALUES('INF312','Base de Datos I',5),('INF220','Programación II',4)")

    insertar_estudiante(conn, '7654321', 'Ana',  'García', 'ana@mail.com',  1)
    insertar_estudiante(conn, '8123456', 'Luis', 'Mamani', 'luis@mail.com', 1)
    insertar_estudiante(conn, '7654321', 'Otra', 'Persona', None, 2)  # CI duplicado → error

    print("\n=== Buscar estudiante ===")
    est = buscar_estudiante(conn, '7654321')
    if est:
        print(f"  Encontrado: {est['nombre']} {est['apellido']} — Carrera: {est['carrera']}")

    print("\n=== Transacciones: registrar notas ===")
    registrar_nota(conn, '7654321', 'INF312', '2024-I', 85.0)
    registrar_nota(conn, '8123456', 'INF312', '2024-I', 70.0)
    registrar_nota(conn, '9999999', 'INF312', '2024-I', 90.0)  # CI no existe → rollback

    print("\n=== Actualizar email ===")
    actualizar_email(conn, '7654321', 'ana.nueva@mail.com')

    print("\n=== Promedio por materia ===")
    for row in promedio_por_materia(conn):
        print(f"  {row['materia']}: promedio={row['promedio']} ({row['total_inscritos']} inscripto/s)")

    print("\n=== SQL Injection: por qué usar parámetros ===")
    # INCORRECTO — vulnerabilidad de SQL Injection
    ci_malicioso = "' OR '1'='1"
    # sql_malo = f"SELECT * FROM ESTUDIANTE WHERE ci = '{ci_malicioso}'"  # PELIGROSO

    # CORRECTO — parámetros parametrizados
    result = conn.execute("SELECT * FROM ESTUDIANTE WHERE ci = ?", (ci_malicioso,)).fetchall()
    print(f"  Búsqueda con CI malicioso usando ?: {len(result)} resultado(s) (correcto: 0)")

    print("\n=== Eliminar estudiante ===")
    registrar_nota(conn, '7654321', 'INF220', '2024-I', 60.0)
    inscripciones_antes = conn.execute("SELECT COUNT(*) FROM INSCRIPCION WHERE ci='7654321'").fetchone()[0]
    print(f"  Inscripciones antes de eliminar: {inscripciones_antes}")
    eliminar_estudiante(conn, '7654321')
    inscripciones_despues = conn.execute("SELECT COUNT(*) FROM INSCRIPCION WHERE ci='7654321'").fetchone()[0]
    print(f"  Inscripciones después de eliminar: {inscripciones_despues} (CASCADE ✓)")

    conn.close()
    print(f"\n✓ BD guardada en: {DB_PATH}")
