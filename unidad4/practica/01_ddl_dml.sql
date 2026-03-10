-- practica/01_ddl_dml.sql
-- Unidad IV: SQL Completo — Base de Datos FARMACIA UAGRM
-- ========================================================
-- Caso práctico real: sistema de gestión de una farmacia.
-- Cubre DDL (CREATE, ALTER, DROP) + DML (SELECT, INSERT, UPDATE, DELETE)
-- + Vistas + Transacciones

-- Ejecutar: sqlite3 farmacia.db < 01_ddl_dml.sql

-- ============================================================
-- DDL: CREAR ESTRUCTURA
-- ============================================================

DROP TABLE IF EXISTS DETALLE_VENTA;
DROP TABLE IF EXISTS VENTA;
DROP TABLE IF EXISTS MEDICAMENTO;
DROP TABLE IF EXISTS LABORATORIO;
DROP TABLE IF EXISTS CATEGORIA_MED;
DROP TABLE IF EXISTS CLIENTE;
DROP TABLE IF EXISTS EMPLEADO;
DROP TABLE IF EXISTS SUCURSAL;

CREATE TABLE SUCURSAL (
    id_sucursal  INTEGER     PRIMARY KEY AUTOINCREMENT,
    nombre       VARCHAR(100) NOT NULL,
    direccion    VARCHAR(200),
    telefono     VARCHAR(20),
    ciudad       VARCHAR(50)  DEFAULT 'Santa Cruz'
);

CREATE TABLE EMPLEADO (
    id_empleado  INTEGER     PRIMARY KEY AUTOINCREMENT,
    ci           VARCHAR(10) NOT NULL UNIQUE,
    nombre       VARCHAR(100) NOT NULL,
    apellido     VARCHAR(100) NOT NULL,
    cargo        VARCHAR(50)  DEFAULT 'Farmacéutico'
                 CHECK (cargo IN ('Farmacéutico','Cajero','Gerente','Delivery')),
    salario      DECIMAL(10,2) CHECK (salario > 0),
    id_sucursal  INTEGER,
    activo       INTEGER     DEFAULT 1,
    FOREIGN KEY (id_sucursal) REFERENCES SUCURSAL(id_sucursal)
);

CREATE TABLE CATEGORIA_MED (
    id_categoria INTEGER     PRIMARY KEY AUTOINCREMENT,
    nombre       VARCHAR(80) NOT NULL UNIQUE,
    descripcion  TEXT
);

CREATE TABLE LABORATORIO (
    id_laboratorio INTEGER    PRIMARY KEY AUTOINCREMENT,
    nombre         VARCHAR(100) NOT NULL,
    pais           VARCHAR(50),
    contacto       VARCHAR(150)
);

CREATE TABLE MEDICAMENTO (
    id_med         INTEGER     PRIMARY KEY AUTOINCREMENT,
    codigo         VARCHAR(20) NOT NULL UNIQUE,
    nombre         VARCHAR(150) NOT NULL,
    principio_act  VARCHAR(150),
    precio_compra  DECIMAL(10,2) NOT NULL CHECK (precio_compra > 0),
    precio_venta   DECIMAL(10,2) NOT NULL CHECK (precio_venta > precio_compra),
    stock          INTEGER     DEFAULT 0 CHECK (stock >= 0),
    stock_minimo   INTEGER     DEFAULT 5,
    fecha_vencim   DATE,
    requiere_receta INTEGER    DEFAULT 0,
    id_categoria   INTEGER,
    id_laboratorio INTEGER,
    FOREIGN KEY (id_categoria)   REFERENCES CATEGORIA_MED(id_categoria),
    FOREIGN KEY (id_laboratorio) REFERENCES LABORATORIO(id_laboratorio)
);

CREATE TABLE CLIENTE (
    id_cliente   INTEGER     PRIMARY KEY AUTOINCREMENT,
    ci           VARCHAR(10) UNIQUE,
    nombre       VARCHAR(100) NOT NULL,
    apellido     VARCHAR(100),
    telefono     VARCHAR(20),
    email        VARCHAR(150),
    fecha_nac    DATE,
    puntos       INTEGER     DEFAULT 0
);

CREATE TABLE VENTA (
    id_venta     INTEGER     PRIMARY KEY AUTOINCREMENT,
    id_cliente   INTEGER,
    id_empleado  INTEGER     NOT NULL,
    id_sucursal  INTEGER     NOT NULL,
    fecha_venta  DATETIME    DEFAULT (DATETIME('now')),
    total        DECIMAL(12,2) DEFAULT 0,
    descuento    DECIMAL(5,2)  DEFAULT 0,
    metodo_pago  VARCHAR(20)   DEFAULT 'efectivo'
                 CHECK (metodo_pago IN ('efectivo','tarjeta','transferencia','QR')),
    FOREIGN KEY (id_cliente)  REFERENCES CLIENTE(id_cliente),
    FOREIGN KEY (id_empleado) REFERENCES EMPLEADO(id_empleado),
    FOREIGN KEY (id_sucursal) REFERENCES SUCURSAL(id_sucursal)
);

CREATE TABLE DETALLE_VENTA (
    id_detalle   INTEGER     PRIMARY KEY AUTOINCREMENT,
    id_venta     INTEGER     NOT NULL,
    id_med       INTEGER     NOT NULL,
    cantidad     INTEGER     NOT NULL CHECK (cantidad > 0),
    precio_unit  DECIMAL(10,2) NOT NULL,
    subtotal     DECIMAL(12,2) GENERATED ALWAYS AS (cantidad * precio_unit) VIRTUAL,
    FOREIGN KEY (id_venta) REFERENCES VENTA(id_venta) ON DELETE CASCADE,
    FOREIGN KEY (id_med)   REFERENCES MEDICAMENTO(id_med)
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_med_nombre   ON MEDICAMENTO(nombre);
CREATE INDEX idx_venta_fecha  ON VENTA(fecha_venta);
CREATE INDEX idx_venta_cliente ON VENTA(id_cliente);

-- ============================================================
-- DML: INSERTAR DATOS
-- ============================================================

INSERT INTO SUCURSAL (nombre, direccion, telefono) VALUES
    ('Farmacia Central', 'Av. Cañoto 123, Centro', '3-3456789'),
    ('Sucursal Norte',   'Av. Banzer Km 4.5',      '3-3456790'),
    ('Sucursal Este',    'Av. Roca y Coronado 55',  '3-3456791');

INSERT INTO EMPLEADO (ci, nombre, apellido, cargo, salario, id_sucursal) VALUES
    ('5000001', 'Carmen',   'Rojas',    'Gerente',       8000.00, 1),
    ('5000002', 'Roberto',  'Flores',   'Farmacéutico',  4500.00, 1),
    ('5000003', 'Patricia', 'Vaca',     'Cajero',        3500.00, 1),
    ('5000004', 'Miguel',   'Gutiérrez','Farmacéutico',  4500.00, 2),
    ('5000005', 'Andrea',   'Paz',      'Farmacéutico',  4500.00, 3);

INSERT INTO CATEGORIA_MED (nombre) VALUES
    ('Analgésicos'),('Antibióticos'),('Antiinflamatorios'),
    ('Vitaminas y Suplementos'),('Antihistamínicos'),
    ('Antihipertensivos'),('Antiácidos');

INSERT INTO LABORATORIO (nombre, pais) VALUES
    ('Bayer',          'Alemania'),
    ('Pfizer',         'EEUU'),
    ('Bagó Bolivia',   'Bolivia'),
    ('Roemmers',       'Argentina'),
    ('Genfar',         'Colombia');

INSERT INTO MEDICAMENTO (codigo, nombre, principio_act, precio_compra, precio_venta, stock, stock_minimo, requiere_receta, id_categoria, id_laboratorio) VALUES
    ('MED001', 'Paracetamol 500mg x20',   'Paracetamol',    8.50,  15.00, 120, 20, 0, 1, 3),
    ('MED002', 'Ibuprofeno 400mg x20',    'Ibuprofeno',     9.00,  18.00,  85, 15, 0, 3, 3),
    ('MED003', 'Amoxicilina 500mg x12',   'Amoxicilina',   22.00,  45.00,  40, 10, 1, 2, 3),
    ('MED004', 'Aspirina 100mg x30',      'Ácido acetilsalicílico', 12.00, 22.00, 60, 10, 0, 1, 1),
    ('MED005', 'Vitamina C 500mg x30',    'Ácido ascórbico', 15.00, 28.00, 95, 20, 0, 4, 4),
    ('MED006', 'Loratadina 10mg x10',     'Loratadina',    10.00,  20.00,  55, 10, 0, 5, 3),
    ('MED007', 'Omeprazol 20mg x14',      'Omeprazol',     14.00,  30.00,  70, 15, 0, 7, 4),
    ('MED008', 'Enalapril 10mg x30',      'Enalapril',     18.00,  35.00,  45, 10, 1, 6, 5),
    ('MED009', 'Azitromicina 500mg x3',   'Azitromicina',  25.00,  55.00,   8,  5, 1, 2, 2),
    ('MED010', 'Metformina 850mg x30',    'Metformina',    20.00,  38.00,   3,  5, 1, 1, 5);

INSERT INTO CLIENTE (ci, nombre, apellido, telefono, email) VALUES
    ('7654321', 'Ana',    'García',  '72345678', 'ana@gmail.com'),
    ('8123456', 'Luis',   'Mamani',  '71234567', 'luis@gmail.com'),
    ('9234567', 'María',  'López',   '73456789', 'maria@gmail.com'),
    (NULL,      'Cliente','General',  NULL,       NULL);   -- cliente sin registro

-- Ventas
INSERT INTO VENTA (id_cliente, id_empleado, id_sucursal, total, metodo_pago) VALUES
    (1, 2, 1, 0, 'efectivo'),
    (2, 2, 1, 0, 'tarjeta'),
    (3, 3, 1, 0, 'QR'),
    (NULL, 2, 1, 0, 'efectivo');   -- cliente sin registro

INSERT INTO DETALLE_VENTA (id_venta, id_med, cantidad, precio_unit) VALUES
    (1, 1, 2, 15.00),   -- Paracetamol x2
    (1, 5, 1, 28.00),   -- Vitamina C x1
    (2, 3, 1, 45.00),   -- Amoxicilina x1
    (2, 7, 2, 30.00),   -- Omeprazol x2
    (3, 2, 1, 18.00),   -- Ibuprofeno x1
    (3, 6, 1, 20.00),   -- Loratadina x1
    (4, 4, 3, 22.00),   -- Aspirina x3
    (4, 1, 1, 15.00);   -- Paracetamol x1

-- Actualizar totales de ventas
UPDATE VENTA SET total = (
    SELECT SUM(cantidad * precio_unit)
    FROM DETALLE_VENTA
    WHERE id_venta = VENTA.id_venta
);

-- ============================================================
-- CONSULTAS BÁSICAS
-- ============================================================

-- Medicamentos con stock bajo el mínimo (alerta de reposición)
SELECT codigo, nombre, stock, stock_minimo,
       (stock_minimo - stock) AS unidades_faltan
FROM MEDICAMENTO
WHERE stock < stock_minimo
ORDER BY unidades_faltan DESC;

-- Medicamentos más vendidos
SELECT m.nombre,
       SUM(dv.cantidad) AS unidades_vendidas,
       SUM(dv.cantidad * dv.precio_unit) AS total_recaudado
FROM DETALLE_VENTA dv
JOIN MEDICAMENTO m ON dv.id_med = m.id_med
GROUP BY m.nombre
ORDER BY unidades_vendidas DESC;

-- ============================================================
-- VISTAS ÚTILES
-- ============================================================

CREATE VIEW IF NOT EXISTS V_VENTA_DETALLE AS
SELECT
    v.id_venta,
    COALESCE(c.nombre || ' ' || c.apellido, 'Cliente General') AS cliente,
    e.nombre || ' ' || e.apellido AS empleado,
    s.nombre AS sucursal,
    v.fecha_venta,
    m.nombre AS medicamento,
    dv.cantidad,
    dv.precio_unit,
    (dv.cantidad * dv.precio_unit) AS subtotal,
    v.metodo_pago
FROM VENTA v
JOIN DETALLE_VENTA dv ON v.id_venta   = dv.id_venta
JOIN MEDICAMENTO   m  ON dv.id_med    = m.id_med
JOIN EMPLEADO      e  ON v.id_empleado = e.id_empleado
JOIN SUCURSAL      s  ON v.id_sucursal = s.id_sucursal
LEFT JOIN CLIENTE  c  ON v.id_cliente  = c.id_cliente;

-- Consultar la vista
SELECT * FROM V_VENTA_DETALLE;

-- Resumen de ventas por sucursal
SELECT sucursal,
       COUNT(DISTINCT id_venta) AS num_ventas,
       SUM(subtotal)             AS total_ventas,
       ROUND(AVG(subtotal), 2)  AS ticket_promedio
FROM V_VENTA_DETALLE
GROUP BY sucursal;

-- ============================================================
-- TRANSACCIÓN: registrar una nueva venta completa
-- ============================================================

BEGIN TRANSACTION;

-- 1. Registrar la venta
INSERT INTO VENTA (id_cliente, id_empleado, id_sucursal, metodo_pago)
VALUES (1, 2, 1, 'efectivo');

-- 2. Agregar detalle
INSERT INTO DETALLE_VENTA (id_venta, id_med, cantidad, precio_unit)
VALUES (last_insert_rowid(), 1, 3, 15.00);  -- Paracetamol x3

-- 3. Descontar del stock
UPDATE MEDICAMENTO SET stock = stock - 3 WHERE id_med = 1;

-- 4. Actualizar total de la venta
UPDATE VENTA SET total = 45.00 WHERE id_venta = last_insert_rowid();

COMMIT;
-- Si hay error en cualquier paso: ROLLBACK;

-- Ver resultado
SELECT 'Stock de Paracetamol después de la venta:',
       stock FROM MEDICAMENTO WHERE id_med = 1;
