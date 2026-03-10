# practica/01_intro_sqlite.py
# Unidad I: Primera Base de Datos con Python y SQLite
# ====================================================
# SQLite no necesita instalación adicional — viene incluido en Python.
# Es ideal para aprender SQL antes de migrar a PostgreSQL o MySQL.

import sqlite3
import os
from typing import List, Tuple, Any


# ================================================================
# CONEXIÓN Y CONFIGURACIÓN
# ================================================================

DB_PATH = "/tmp/universidad_bd1.db"


def conectar() -> sqlite3.Connection:
    """
    Crea o abre la base de datos SQLite.
    
    Con SQLite: si el archivo no existe, se crea automáticamente.
    Equivalente en PostgreSQL: psycopg2.connect(host=..., dbname=..., user=...)
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # permite acceder columnas por nombre
    conn.execute("PRAGMA foreign_keys = ON")  # activar integridad referencial
    return conn


def ejecutar_sql(conn: sqlite3.Connection, sql: str,
                 params: tuple = (), verbose: bool = True) -> List[sqlite3.Row]:
    """
    Ejecuta una sentencia SQL y retorna los resultados.
    
    Args:
        conn: Conexión activa a la BD.
        sql: Sentencia SQL a ejecutar.
        params: Parámetros parametrizados (evitan SQL injection).
        verbose: Si True, imprime el SQL ejecutado.
    """
    if verbose:
        sql_limpio = " ".join(sql.split())
        print(f"\n  SQL> {sql_limpio[:100]}{'...' if len(sql_limpio)>100 else ''}")
    
    cursor = conn.cursor()
    cursor.execute(sql, params)
    
    if sql.strip().upper().startswith("SELECT"):
        return cursor.fetchall()
    else:
        conn.commit()
        print(f"       → {cursor.rowcount} fila(s) afectada(s)")
        return []


def imprimir_tabla(filas: List[sqlite3.Row], titulo: str = "") -> None:
    """Imprime resultados en formato tabla legible."""
    if not filas:
        print("  (sin resultados)")
        return
    
    if titulo:
        print(f"\n  📋 {titulo}")
    
    # Obtener nombres de columnas
    columnas = filas[0].keys()
    anchos = {col: max(len(col), max(len(str(f[col] or '')) for f in filas))
              for col in columnas}
    
    # Encabezado
    sep = "  +" + "+".join("-" * (anchos[c] + 2) for c in columnas) + "+"
    header = "  |" + "|".join(f" {c.upper():<{anchos[c]}} " for c in columnas) + "|"
    
    print(sep)
    print(header)
    print(sep)
    
    for fila in filas:
        linea = "  |" + "|".join(f" {str(fila[c] or ''):<{anchos[c]}} " for c in columnas) + "|"
        print(linea)
    
    print(sep)
    print(f"  {len(filas)} fila(s)")


# ================================================================
# CREACIÓN DE LA BASE DE DATOS (DDL)
# ================================================================

def crear_esquema(conn: sqlite3.Connection) -> None:
    """
    Crea todas las tablas de la base de datos universitaria.
    
    DDL = Data Definition Language
    Comandos: CREATE TABLE, ALTER TABLE, DROP TABLE
    """
    print("\n" + "="*55)
    print("  DDL: CREANDO ESTRUCTURA DE LA BASE DE DATOS")
    print("="*55)
    
    sentencias_ddl = [
        """
        CREATE TABLE IF NOT EXISTS CARRERA (
            id_carrera    INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre        VARCHAR(100) NOT NULL UNIQUE,
            duracion_anios INTEGER DEFAULT 5
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS DOCENTE (
            id_docente  INTEGER     PRIMARY KEY AUTOINCREMENT,
            ci          VARCHAR(10) NOT NULL UNIQUE,
            nombre      VARCHAR(100) NOT NULL,
            apellido    VARCHAR(100) NOT NULL,
            categoria   VARCHAR(20) DEFAULT 'Auxiliar'
                        CHECK (categoria IN ('Auxiliar','Instructor','Titular'))
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ESTUDIANTE (
            ci          VARCHAR(10)  PRIMARY KEY,
            nombre      VARCHAR(100) NOT NULL,
            apellido    VARCHAR(100) NOT NULL,
            fecha_nac   DATE,
            email       VARCHAR(150) UNIQUE,
            id_carrera  INTEGER,
            FOREIGN KEY (id_carrera) REFERENCES CARRERA(id_carrera)
                ON DELETE SET NULL ON UPDATE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS MATERIA (
            codigo      VARCHAR(10)  PRIMARY KEY,
            nombre      VARCHAR(100) NOT NULL,
            creditos    INTEGER      NOT NULL CHECK (creditos BETWEEN 1 AND 10),
            nivel       INTEGER      CHECK (nivel BETWEEN 1 AND 10),
            id_docente  INTEGER,
            FOREIGN KEY (id_docente) REFERENCES DOCENTE(id_docente)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS INSCRIPCION (
            id_inscripcion INTEGER     PRIMARY KEY AUTOINCREMENT,
            ci             VARCHAR(10) NOT NULL,
            codigo         VARCHAR(10) NOT NULL,
            gestion        VARCHAR(7)  NOT NULL,
            nota           REAL        CHECK (nota IS NULL OR nota BETWEEN 0 AND 100),
            FOREIGN KEY (ci)     REFERENCES ESTUDIANTE(ci) ON DELETE CASCADE,
            FOREIGN KEY (codigo) REFERENCES MATERIA(codigo) ON DELETE RESTRICT,
            UNIQUE (ci, codigo, gestion)
        )
        """
    ]
    
    for ddl in sentencias_ddl:
        nombre_tabla = [w for w in ddl.split() if w.isupper() and len(w) > 2][3]
        print(f"\n  Creando tabla {nombre_tabla}...")
        conn.execute(ddl)
    
    conn.commit()
    print("\n  ✅ Esquema creado exitosamente")


# ================================================================
# INSERCIÓN DE DATOS (DML - INSERT)
# ================================================================

def insertar_datos(conn: sqlite3.Connection) -> None:
    """
    Inserta datos de ejemplo en todas las tablas.
    DML = Data Manipulation Language
    """
    print("\n" + "="*55)
    print("  DML: INSERTANDO DATOS")
    print("="*55)
    
    # Carreras
    conn.executemany(
        "INSERT OR IGNORE INTO CARRERA (nombre, duracion_anios) VALUES (?, ?)",
        [
            ("Ingeniería en Sistemas", 5),
            ("Ingeniería en Telecomunicaciones", 5),
            ("Licenciatura en Informática", 4),
        ]
    )
    
    # Docentes
    conn.executemany(
        "INSERT OR IGNORE INTO DOCENTE (ci, nombre, apellido, categoria) VALUES (?,?,?,?)",
        [
            ("1234567", "Juan Carlos", "Peinado Pereira", "Titular"),
            ("2345678", "María Elena", "Gutiérrez", "Instructor"),
            ("3456789", "Roberto", "Flores", "Auxiliar"),
        ]
    )
    
    # Estudiantes
    conn.executemany(
        "INSERT OR IGNORE INTO ESTUDIANTE (ci, nombre, apellido, fecha_nac, email, id_carrera) VALUES (?,?,?,?,?,?)",
        [
            ("7654321", "Ana",    "García",   "2000-03-15", "ana.garcia@uagrm.edu.bo",    1),
            ("8123456", "Luis",   "Mamani",   "1999-07-22", "luis.mamani@uagrm.edu.bo",   1),
            ("9234567", "María",  "López",    "2001-01-10", "maria.lopez@uagrm.edu.bo",   2),
            ("5432198", "Carlos", "Quispe",   "2000-11-05", "carlos.quispe@uagrm.edu.bo", 1),
            ("6789012", "Sofía",  "Pereira",  "2001-06-30", "sofia.pereira@uagrm.edu.bo", 3),
            ("7890123", "Diego",  "Vargas",   "2000-04-18", "diego.vargas@uagrm.edu.bo",  1),
            ("8901234", "Laura",  "Morales",  "2001-09-25", "laura.morales@uagrm.edu.bo", 2),
        ]
    )
    
    # Materias
    conn.executemany(
        "INSERT OR IGNORE INTO MATERIA (codigo, nombre, creditos, nivel, id_docente) VALUES (?,?,?,?,?)",
        [
            ("INF220", "Estructuras de Datos I",        5, 3, 3),
            ("INF310", "Estructuras de Datos II",       5, 4, 3),
            ("INF312", "Base de Datos I",               5, 5, 1),
            ("INF315", "Base de Datos II",              5, 6, 1),
            ("INF320", "Sistemas Operativos",           5, 5, 2),
            ("INF330", "Redes de Computadoras",         5, 6, 2),
        ]
    )
    
    # Inscripciones
    conn.executemany(
        "INSERT OR IGNORE INTO INSCRIPCION (ci, codigo, gestion, nota) VALUES (?,?,?,?)",
        [
            ("7654321", "INF220", "2023-I",  85.5),
            ("7654321", "INF310", "2023-II", 78.0),
            ("7654321", "INF312", "2024-I",  None),   # cursando
            ("8123456", "INF220", "2023-I",  90.0),
            ("8123456", "INF310", "2023-II", 65.0),
            ("8123456", "INF312", "2024-I",  None),
            ("9234567", "INF220", "2023-I",  55.0),   # reprobó
            ("9234567", "INF320", "2023-II", 72.5),
            ("5432198", "INF220", "2023-I",  72.0),
            ("5432198", "INF312", "2024-I",  None),
            ("6789012", "INF220", "2023-I",  88.0),
            ("7890123", "INF220", "2023-I",  45.0),   # reprobó
            ("7890123", "INF220", "2024-I",  68.0),   # segunda vez
            ("8901234", "INF220", "2023-I",  91.0),
            ("8901234", "INF320", "2024-I",  None),
        ]
    )
    
    conn.commit()
    print("  ✅ Datos insertados correctamente")


# ================================================================
# CONSULTAS DE EJEMPLO (DML - SELECT)
# ================================================================

def demo_consultas(conn: sqlite3.Connection) -> None:
    """Demuestra distintos tipos de consultas SQL."""
    
    print("\n" + "="*55)
    print("  SELECT: CONSULTAS A LA BASE DE DATOS")
    print("="*55)
    
    # 1. Consulta simple
    filas = ejecutar_sql(conn, "SELECT ci, nombre || ' ' || apellido AS nombre_completo FROM ESTUDIANTE")
    imprimir_tabla(filas, "Todos los estudiantes")
    
    # 2. Con filtro WHERE
    filas = ejecutar_sql(conn, """
        SELECT ci, nombre, apellido, fecha_nac
        FROM ESTUDIANTE
        WHERE id_carrera = 1
        ORDER BY apellido
    """)
    imprimir_tabla(filas, "Estudiantes de Sistemas (id_carrera=1)")
    
    # 3. JOIN entre tablas
    filas = ejecutar_sql(conn, """
        SELECT e.nombre || ' ' || e.apellido AS estudiante,
               m.nombre AS materia,
               i.gestion,
               CASE WHEN i.nota IS NULL     THEN 'Cursando'
                    WHEN i.nota >= 51       THEN 'Aprobado'
                    ELSE                        'Reprobado'
               END AS estado,
               COALESCE(CAST(i.nota AS TEXT), '---') AS nota
        FROM INSCRIPCION i
        JOIN ESTUDIANTE e ON i.ci     = e.ci
        JOIN MATERIA    m ON i.codigo = m.codigo
        ORDER BY e.apellido, i.gestion
    """)
    imprimir_tabla(filas, "Historial completo de inscripciones")
    
    # 4. Agregación con GROUP BY
    filas = ejecutar_sql(conn, """
        SELECT m.nombre AS materia,
               COUNT(i.id_inscripcion) AS total_inscritos,
               ROUND(AVG(CASE WHEN i.nota IS NOT NULL THEN i.nota END), 1) AS promedio_nota,
               SUM(CASE WHEN i.nota >= 51 THEN 1 ELSE 0 END) AS aprobados,
               SUM(CASE WHEN i.nota < 51  THEN 1 ELSE 0 END) AS reprobados
        FROM MATERIA m
        LEFT JOIN INSCRIPCION i ON m.codigo = i.codigo
        GROUP BY m.nombre
        ORDER BY total_inscritos DESC
    """)
    imprimir_tabla(filas, "Estadísticas por materia")
    
    # 5. Subconsulta
    filas = ejecutar_sql(conn, """
        SELECT nombre || ' ' || apellido AS estudiante,
               (SELECT COUNT(*) FROM INSCRIPCION i
                WHERE i.ci = e.ci AND nota >= 51) AS materias_aprobadas
        FROM ESTUDIANTE e
        ORDER BY materias_aprobadas DESC
    """)
    imprimir_tabla(filas, "Materias aprobadas por estudiante")


# ================================================================
# ACTUALIZACIÓN Y ELIMINACIÓN (DML - UPDATE / DELETE)
# ================================================================

def demo_update_delete(conn: sqlite3.Connection) -> None:
    """Demuestra UPDATE y DELETE con manejo de integridad."""
    
    print("\n" + "="*55)
    print("  UPDATE y DELETE: MODIFICAR DATOS")
    print("="*55)
    
    # UPDATE: registrar una nota
    ejecutar_sql(conn, """
        UPDATE INSCRIPCION
        SET nota = 88.5
        WHERE ci = '7654321' AND codigo = 'INF312' AND gestion = '2024-I'
    """)
    
    # Verificar el cambio
    filas = ejecutar_sql(conn, """
        SELECT e.nombre, m.nombre as materia, i.nota
        FROM INSCRIPCION i
        JOIN ESTUDIANTE e ON i.ci = e.ci
        JOIN MATERIA m ON i.codigo = m.codigo
        WHERE i.ci = '7654321' AND i.codigo = 'INF312'
    """)
    imprimir_tabla(filas, "Nota actualizada de Ana en BD I")
    
    # DELETE con integridad referencial
    print("\n  Intentando eliminar una materia con inscripciones...")
    try:
        ejecutar_sql(conn, "DELETE FROM MATERIA WHERE codigo = 'INF220'")
    except sqlite3.IntegrityError as e:
        print(f"  ✗ Error de integridad (esperado): {e}")
        print("    → No se puede eliminar INF220 porque tiene inscripciones asociadas")


# ================================================================
# MAIN
# ================================================================

def main():
    print("\n" + "🗄️ " * 20)
    print("  INF-312 BASE DE DATOS I")
    print("  Práctica 1 — Introducción a SQLite con Python")
    print("  UAGRM — Facultad de Ingeniería")
    print("🗄️ " * 20)
    
    # Limpiar BD anterior si existe
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = conectar()
    print(f"\n  Conectado a: {DB_PATH}")
    print(f"  SQLite versión: {sqlite3.sqlite_version}")
    
    crear_esquema(conn)
    insertar_datos(conn)
    demo_consultas(conn)
    demo_update_delete(conn)
    
    conn.close()
    print(f"\n{'='*55}")
    print(f"  ✅ Práctica completada. BD guardada en: {DB_PATH}")
    print(f"     Podés abrirla con: DB Browser for SQLite")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
