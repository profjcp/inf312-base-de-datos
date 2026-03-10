# practica/01_normalizacion.py
# Unidad V: Normalización paso a paso — 0FN → 1FN → 2FN → 3FN
# ==============================================================
# Muestra una tabla "mal diseñada" y la lleva a 3FN,
# comparando los problemas antes y después de cada paso.

import sqlite3
import os


DB = "/tmp/normalizacion_bd1.db"


def conectar():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def separador(titulo: str, nivel: int = 1):
    ch = "═" if nivel == 1 else "─"
    print(f"\n{ch*60}")
    print(f"  {titulo}")
    print(f"{ch*60}")


def mostrar_tabla(conn, tabla: str, titulo: str = ""):
    cursor = conn.execute(f"SELECT * FROM {tabla}")
    filas = cursor.fetchall()
    if not filas:
        print(f"  (tabla {tabla} vacía)")
        return
    cols = [d[0] for d in cursor.description]
    anchos = {c: max(len(c), max(len(str(f[i] or '')) for f in filas))
              for i, c in enumerate(cols)}
    sep = "  +" + "+".join("-"*(anchos[c]+2) for c in cols) + "+"
    if titulo:
        print(f"\n  📋 {titulo}")
    print(sep)
    print("  |" + "|".join(f" {c.upper():<{anchos[c]}} " for c in cols) + "|")
    print(sep)
    for f in filas:
        print("  |" + "|".join(f" {str(f[i] or ''):<{anchos[c]}} "
                                for i, c in enumerate(cols)) + "|")
    print(sep)
    print(f"  {len(filas)} fila(s)\n")


# ================================================================
# TABLA ORIGINAL: 0FN (sin normalizar)
# ================================================================

def crear_tabla_0fn(conn):
    """
    Caso real: tabla de pedidos de una ferretería,
    tal como la guardarían en una planilla de Excel.
    Tiene todos los problemas de diseño.
    """
    conn.execute("DROP TABLE IF EXISTS PEDIDO_MAL")
    conn.execute("""
        CREATE TABLE PEDIDO_MAL (
            num_pedido    INTEGER,
            fecha         DATE,
            ci_cliente    VARCHAR(10),
            nombre_cliente VARCHAR(100),
            ciudad_cliente VARCHAR(50),
            productos     TEXT,          -- MULTIVALUADO: "Martillo,Tornillo,Pintura"
            cantidades    TEXT,          -- MULTIVALUADO: "2,10,1"
            precios       TEXT,          -- MULTIVALUADO: "35.00,0.50,45.00"
            id_vendedor   INTEGER,
            nombre_vendedor VARCHAR(100),
            sucursal_vendedor VARCHAR(50)
        )
    """)
    conn.executemany("INSERT INTO PEDIDO_MAL VALUES (?,?,?,?,?,?,?,?,?,?,?)", [
        (1001,'2024-01-10','7654321','Ana García',   'Santa Cruz',
         'Martillo,Tornillo,Pintura', '2,10,1',    '35.00,0.50,45.00', 1,'Carlos Lima','Centro'),
        (1002,'2024-01-11','8123456','Luis Mamani',  'Santa Cruz',
         'Pincel,Lija',               '3,5',       '8.00,3.50',        2,'María Vaca', 'Norte'),
        (1003,'2024-01-12','7654321','Ana García',   'Santa Cruz',
         'Tornillo,Clavo',            '20,15',     '0.50,0.30',        1,'Carlos Lima','Centro'),
    ])
    conn.commit()


def demo_0fn(conn):
    separador("0FN — TABLA SIN NORMALIZAR (problema original)")
    mostrar_tabla(conn, "PEDIDO_MAL", "Tabla PEDIDO_MAL (planilla de Excel)")
    
    print("  ❌ PROBLEMAS identificados:")
    print("     • Atributos MULTIVALUADOS: productos, cantidades, precios")
    print("       → ¿Cómo busco todos los pedidos que incluyen 'Martillo'?")
    print("     • Redundancia: nombre_cliente se repite en cada pedido de Ana")
    print("     • Redundancia: nombre_vendedor se repite en cada pedido de Carlos")
    print("     • Anomalía: si Ana cambia de ciudad, hay que buscar TODAS sus filas")
    print("     • No hay clave primaria clara")


# ================================================================
# PRIMERA FORMA NORMAL (1FN)
# ================================================================

def crear_1fn(conn):
    """
    Solución: una fila por producto pedido.
    Clave primaria compuesta: (num_pedido, id_producto)
    """
    conn.execute("DROP TABLE IF EXISTS PEDIDO_1FN")
    conn.execute("""
        CREATE TABLE PEDIDO_1FN (
            num_pedido      INTEGER,
            fecha           DATE,
            ci_cliente      VARCHAR(10),
            nombre_cliente  VARCHAR(100),
            ciudad_cliente  VARCHAR(50),
            id_producto     INTEGER,
            nombre_producto VARCHAR(100),
            cantidad        INTEGER,
            precio_unit     DECIMAL(10,2),
            id_vendedor     INTEGER,
            nombre_vendedor VARCHAR(100),
            sucursal_vend   VARCHAR(50),
            PRIMARY KEY (num_pedido, id_producto)
        )
    """)
    conn.executemany("INSERT INTO PEDIDO_1FN VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", [
        (1001,'2024-01-10','7654321','Ana García',  'Santa Cruz', 101,'Martillo',  2,35.00,1,'Carlos Lima','Centro'),
        (1001,'2024-01-10','7654321','Ana García',  'Santa Cruz', 102,'Tornillo', 10, 0.50,1,'Carlos Lima','Centro'),
        (1001,'2024-01-10','7654321','Ana García',  'Santa Cruz', 103,'Pintura',   1,45.00,1,'Carlos Lima','Centro'),
        (1002,'2024-01-11','8123456','Luis Mamani', 'Santa Cruz', 104,'Pincel',    3, 8.00,2,'María Vaca', 'Norte'),
        (1002,'2024-01-11','8123456','Luis Mamani', 'Santa Cruz', 105,'Lija',      5, 3.50,2,'María Vaca', 'Norte'),
        (1003,'2024-01-12','7654321','Ana García',  'Santa Cruz', 102,'Tornillo', 20, 0.50,1,'Carlos Lima','Centro'),
        (1003,'2024-01-12','7654321','Ana García',  'Santa Cruz', 106,'Clavo',    15, 0.30,1,'Carlos Lima','Centro'),
    ])
    conn.commit()


def demo_1fn(conn):
    separador("1FN — PRIMERA FORMA NORMAL")
    mostrar_tabla(conn, "PEDIDO_1FN", "Tabla en 1FN — una fila por producto")
    
    print("  ✅ Lo que se corrigió:")
    print("     • Atributos atómicos: cada celda tiene un solo valor")
    print("     • Clave primaria definida: (num_pedido, id_producto)")
    print()
    print("  ❌ Problemas que QUEDAN (dependencias parciales):")
    print("     • nombre_cliente depende solo de ci_cliente (no de toda la PK)")
    print("       ci_cliente → nombre_cliente, ciudad_cliente")
    print("     • nombre_producto, precio_unit dependen solo de id_producto")
    print("       id_producto → nombre_producto, precio_unit")
    print("     • nombre_vendedor depende solo de id_vendedor")
    print("       id_vendedor → nombre_vendedor, sucursal_vend")
    print("     → Estos son dependencias PARCIALES → hay que llegar a 2FN")


# ================================================================
# SEGUNDA FORMA NORMAL (2FN)
# ================================================================

def crear_2fn(conn):
    """
    Eliminar dependencias parciales: separar CLIENTE, PRODUCTO, VENDEDOR.
    En PEDIDO_DETALLE solo quedan atributos que dependen de la PK completa.
    """
    for t in ["CLIENTE_2FN","PRODUCTO_2FN","VENDEDOR_2FN","PEDIDO_2FN","DETALLE_2FN"]:
        conn.execute(f"DROP TABLE IF EXISTS {t}")
    
    conn.execute("""CREATE TABLE CLIENTE_2FN (
        ci          VARCHAR(10) PRIMARY KEY,
        nombre      VARCHAR(100),
        ciudad      VARCHAR(50))""")
    
    conn.execute("""CREATE TABLE PRODUCTO_2FN (
        id_producto  INTEGER     PRIMARY KEY,
        nombre       VARCHAR(100),
        precio_unit  DECIMAL(10,2))""")
    
    conn.execute("""CREATE TABLE VENDEDOR_2FN (
        id_vendedor  INTEGER     PRIMARY KEY,
        nombre       VARCHAR(100),
        sucursal     VARCHAR(50))""")
    
    conn.execute("""CREATE TABLE PEDIDO_2FN (
        num_pedido   INTEGER     PRIMARY KEY,
        fecha        DATE,
        ci_cliente   VARCHAR(10),
        id_vendedor  INTEGER,
        FOREIGN KEY (ci_cliente)  REFERENCES CLIENTE_2FN(ci),
        FOREIGN KEY (id_vendedor) REFERENCES VENDEDOR_2FN(id_vendedor))""")
    
    conn.execute("""CREATE TABLE DETALLE_2FN (
        num_pedido   INTEGER,
        id_producto  INTEGER,
        cantidad     INTEGER,
        PRIMARY KEY (num_pedido, id_producto),
        FOREIGN KEY (num_pedido)  REFERENCES PEDIDO_2FN(num_pedido),
        FOREIGN KEY (id_producto) REFERENCES PRODUCTO_2FN(id_producto))""")
    
    # Poblar tablas normalizadas
    conn.executemany("INSERT OR IGNORE INTO CLIENTE_2FN VALUES (?,?,?)", [
        ('7654321','Ana García','Santa Cruz'),
        ('8123456','Luis Mamani','Santa Cruz'),
    ])
    conn.executemany("INSERT OR IGNORE INTO PRODUCTO_2FN VALUES (?,?,?)", [
        (101,'Martillo',35.00),(102,'Tornillo',0.50),(103,'Pintura',45.00),
        (104,'Pincel',8.00),(105,'Lija',3.50),(106,'Clavo',0.30),
    ])
    conn.executemany("INSERT OR IGNORE INTO VENDEDOR_2FN VALUES (?,?,?)", [
        (1,'Carlos Lima','Centro'),(2,'María Vaca','Norte'),
    ])
    conn.executemany("INSERT OR IGNORE INTO PEDIDO_2FN VALUES (?,?,?,?)", [
        (1001,'2024-01-10','7654321',1),
        (1002,'2024-01-11','8123456',2),
        (1003,'2024-01-12','7654321',1),
    ])
    conn.executemany("INSERT OR IGNORE INTO DETALLE_2FN VALUES (?,?,?)", [
        (1001,101,2),(1001,102,10),(1001,103,1),
        (1002,104,3),(1002,105,5),
        (1003,102,20),(1003,106,15),
    ])
    conn.commit()


def demo_2fn(conn):
    separador("2FN — SEGUNDA FORMA NORMAL")
    for tabla, titulo in [
        ("CLIENTE_2FN",  "CLIENTE"),
        ("PRODUCTO_2FN", "PRODUCTO"),
        ("VENDEDOR_2FN", "VENDEDOR"),
        ("PEDIDO_2FN",   "PEDIDO (cabecera)"),
        ("DETALLE_2FN",  "DETALLE_PEDIDO (filas)"),
    ]:
        mostrar_tabla(conn, tabla, tabla)
    
    print("  ✅ Lo que se corrigió:")
    print("     • Dependencias parciales eliminadas")
    print("     • Cada tabla tiene un propósito claro y único")
    print()
    print("  ❌ Problema que QUEDA (dependencia transitiva):")
    print("     En VENDEDOR_2FN:")
    print("       id_vendedor → sucursal  (ok, directa)")
    print("     Si sucursal tiene más datos (dirección, ciudad):")
    print("       id_vendedor → id_sucursal → ciudad_sucursal  (TRANSITIVA)")
    print("     → Hay que llegar a 3FN")


# ================================================================
# TERCERA FORMA NORMAL (3FN)
# ================================================================

def crear_3fn(conn):
    """
    Eliminar dependencias transitivas restantes.
    Ahora se extrae SUCURSAL a su propia tabla.
    """
    for t in ["SUCURSAL_3FN","VENDEDOR_3FN"]:
        conn.execute(f"DROP TABLE IF EXISTS {t}")
    
    conn.execute("""CREATE TABLE SUCURSAL_3FN (
        id_sucursal  INTEGER     PRIMARY KEY,
        nombre       VARCHAR(100),
        ciudad       VARCHAR(50),
        direccion    VARCHAR(200))""")
    
    conn.execute("""CREATE TABLE VENDEDOR_3FN (
        id_vendedor  INTEGER     PRIMARY KEY,
        nombre       VARCHAR(100),
        id_sucursal  INTEGER,
        FOREIGN KEY (id_sucursal) REFERENCES SUCURSAL_3FN(id_sucursal))""")
    
    conn.executemany("INSERT OR IGNORE INTO SUCURSAL_3FN VALUES (?,?,?,?)", [
        (1,'Sucursal Centro','Santa Cruz','Av. Cañoto 123'),
        (2,'Sucursal Norte', 'Santa Cruz','Av. Banzer Km 4'),
    ])
    conn.executemany("INSERT OR IGNORE INTO VENDEDOR_3FN VALUES (?,?,?)", [
        (1,'Carlos Lima',1),(2,'María Vaca',2),
    ])
    conn.commit()


def demo_3fn(conn):
    separador("3FN — TERCERA FORMA NORMAL (diseño final)")
    for tabla in ["SUCURSAL_3FN","VENDEDOR_3FN"]:
        mostrar_tabla(conn, tabla, tabla)
    
    print("  ✅ Esquema final en 3FN:")
    print()
    print("  CLIENTE(ci, nombre, ciudad)")
    print("  SUCURSAL(id_sucursal, nombre, ciudad, direccion)")
    print("  VENDEDOR(id_vendedor, nombre, id_sucursal→SUCURSAL)")
    print("  PEDIDO(num_pedido, fecha, ci→CLIENTE, id_vendedor→VENDEDOR)")
    print("  PRODUCTO(id_producto, nombre, precio_unit)")
    print("  DETALLE(num_pedido→PEDIDO, id_producto→PRODUCTO, cantidad)")
    print()
    print("  ✅ Ventajas del diseño en 3FN:")
    print("     • Sin redundancia de datos")
    print("     • Sin anomalías de inserción, borrado ni modificación")
    print("     • Cada dato se guarda UNA SOLA VEZ")
    print("     • Fácil mantenimiento e integridad referencial")


# ================================================================
# COMPARATIVA FINAL
# ================================================================

def demo_comparativa(conn):
    separador("COMPARATIVA: consulta antes vs después")
    
    print("  Pedido 1001 en la tabla SIN normalizar (0FN):")
    filas = conn.execute("SELECT * FROM PEDIDO_MAL WHERE num_pedido=1001").fetchall()
    for f in filas:
        print(f"    {dict(f)}")
    
    print("\n  Pedido 1001 en el diseño NORMALIZADO (3FN):")
    filas = conn.execute("""
        SELECT p.num_pedido, p.fecha,
               c.nombre AS cliente,
               pr.nombre AS producto,
               d.cantidad,
               pr.precio_unit,
               (d.cantidad * pr.precio_unit) AS subtotal
        FROM PEDIDO_2FN p
        JOIN CLIENTE_2FN  c  ON p.ci_cliente   = c.ci
        JOIN DETALLE_2FN  d  ON p.num_pedido   = d.num_pedido
        JOIN PRODUCTO_2FN pr ON d.id_producto  = pr.id_producto
        WHERE p.num_pedido = 1001
    """).fetchall()
    for f in filas:
        print(f"    {dict(f)}")
    
    total = sum(f['subtotal'] for f in filas)
    print(f"\n  Total del pedido 1001: Bs. {total:.2f}")


# ================================================================
# MAIN
# ================================================================

def main():
    print("\n" + "🗄️ " * 20)
    print("  INF-312 BASE DE DATOS I")
    print("  Práctica 5 — Normalización: 0FN → 1FN → 2FN → 3FN")
    print("  UAGRM — Facultad de Ingeniería")
    print("🗄️ " * 20)
    
    if os.path.exists(DB):
        os.remove(DB)
    
    conn = conectar()
    
    # 0FN
    crear_tabla_0fn(conn)
    demo_0fn(conn)
    
    # 1FN
    crear_1fn(conn)
    demo_1fn(conn)
    
    # 2FN
    crear_2fn(conn)
    demo_2fn(conn)
    
    # 3FN
    crear_3fn(conn)
    demo_3fn(conn)
    
    # Comparativa
    demo_comparativa(conn)
    
    conn.close()
    print(f"\n{'═'*60}")
    print("  ✅ Demostración de normalización completada")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    main()
