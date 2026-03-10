-- fase2/hospital_referencia.sql
-- Proyecto Final INF-312 — REFERENCIA DEL DOCENTE
-- =================================================
-- Esqueleto completo del Hospital San Juan de Dios.
-- Los estudiantes deben completar los INSERT y las 15 consultas.

PRAGMA foreign_keys = ON;

-- ============================================================
-- DDL
-- ============================================================

DROP TABLE IF EXISTS DETALLE_RECETA;
DROP TABLE IF EXISTS RECETA;
DROP TABLE IF EXISTS DETALLE_HOSPITALIZACION;
DROP TABLE IF EXISTS HOSPITALIZACION;
DROP TABLE IF EXISTS CONSULTA;
DROP TABLE IF EXISTS MEDICO_ESPECIALIDAD;
DROP TABLE IF EXISTS ESPECIALIDAD;
DROP TABLE IF EXISTS CAMA;
DROP TABLE IF EXISTS SALA;
DROP TABLE IF EXISTS SEGURO_PACIENTE;
DROP TABLE IF EXISTS MEDICAMENTO;
DROP TABLE IF EXISTS LABORATORIO;
DROP TABLE IF EXISTS PERSONAL;
DROP TABLE IF EXISTS MEDICO;
DROP TABLE IF EXISTS PACIENTE;

CREATE TABLE PACIENTE (
    ci           VARCHAR(10)  PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    apellido     VARCHAR(100) NOT NULL,
    fecha_nac    DATE         NOT NULL,
    sexo         CHAR(1)      CHECK (sexo IN ('M','F')),
    grupo_sang   VARCHAR(5)   CHECK (grupo_sang IN ('A+','A-','B+','B-','AB+','AB-','O+','O-')),
    telefono     VARCHAR(20),
    email        VARCHAR(150),
    direccion    TEXT
);

CREATE TABLE SEGURO_PACIENTE (
    id_seguro    INTEGER     PRIMARY KEY AUTOINCREMENT,
    ci_paciente  VARCHAR(10) NOT NULL,
    aseguradora  VARCHAR(100) NOT NULL,
    num_poliza   VARCHAR(50)  NOT NULL,
    vigente      INTEGER     DEFAULT 1,
    FOREIGN KEY (ci_paciente) REFERENCES PACIENTE(ci) ON DELETE CASCADE
);

CREATE TABLE ESPECIALIDAD (
    id_esp  INTEGER     PRIMARY KEY AUTOINCREMENT,
    nombre  VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE MEDICO (
    matricula    VARCHAR(20)  PRIMARY KEY,
    ci           VARCHAR(10)  NOT NULL UNIQUE,
    nombre       VARCHAR(100) NOT NULL,
    apellido     VARCHAR(100) NOT NULL,
    telefono     VARCHAR(20),
    email        VARCHAR(150),
    activo       INTEGER     DEFAULT 1
);

CREATE TABLE MEDICO_ESPECIALIDAD (
    matricula    VARCHAR(20) NOT NULL,
    id_esp       INTEGER     NOT NULL,
    es_principal INTEGER     DEFAULT 0,
    PRIMARY KEY (matricula, id_esp),
    FOREIGN KEY (matricula) REFERENCES MEDICO(matricula),
    FOREIGN KEY (id_esp)    REFERENCES ESPECIALIDAD(id_esp)
);

CREATE TABLE PERSONAL (
    ci       VARCHAR(10)  PRIMARY KEY,
    nombre   VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cargo    VARCHAR(50)  NOT NULL
             CHECK (cargo IN ('Enfermero','Secretaria','Camillero','Limpieza','Administrativo')),
    turno    VARCHAR(10)  CHECK (turno IN ('mañana','tarde','noche')),
    salario  DECIMAL(10,2)
);

CREATE TABLE SALA (
    id_sala      INTEGER     PRIMARY KEY AUTOINCREMENT,
    nombre       VARCHAR(80) NOT NULL UNIQUE,
    tipo         VARCHAR(50) CHECK (tipo IN ('General','UCI','Pediatría','Maternidad','Cirugía','Emergencias')),
    total_camas  INTEGER     DEFAULT 10
);

CREATE TABLE CAMA (
    id_cama     INTEGER     PRIMARY KEY AUTOINCREMENT,
    id_sala     INTEGER     NOT NULL,
    numero      INTEGER     NOT NULL,
    disponible  INTEGER     DEFAULT 1,
    UNIQUE (id_sala, numero),
    FOREIGN KEY (id_sala) REFERENCES SALA(id_sala)
);

CREATE TABLE LABORATORIO (
    id_lab  INTEGER     PRIMARY KEY AUTOINCREMENT,
    nombre  VARCHAR(100) NOT NULL,
    pais    VARCHAR(50)
);

CREATE TABLE MEDICAMENTO (
    id_med         INTEGER     PRIMARY KEY AUTOINCREMENT,
    codigo         VARCHAR(20) NOT NULL UNIQUE,
    nombre         VARCHAR(150) NOT NULL,
    principio_act  VARCHAR(150),
    presentacion   VARCHAR(80),
    precio         DECIMAL(10,2) CHECK (precio > 0),
    stock          INTEGER     DEFAULT 0 CHECK (stock >= 0),
    stock_minimo   INTEGER     DEFAULT 10,
    id_lab         INTEGER,
    FOREIGN KEY (id_lab) REFERENCES LABORATORIO(id_lab)
);

CREATE TABLE CONSULTA (
    id_consulta  INTEGER     PRIMARY KEY AUTOINCREMENT,
    ci_paciente  VARCHAR(10) NOT NULL,
    matricula    VARCHAR(20) NOT NULL,
    fecha_hora   DATETIME    DEFAULT (DATETIME('now')),
    motivo       TEXT        NOT NULL,
    diagnostico  TEXT,
    tratamiento  TEXT,
    costo        DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (ci_paciente) REFERENCES PACIENTE(ci),
    FOREIGN KEY (matricula)   REFERENCES MEDICO(matricula)
);

CREATE TABLE RECETA (
    id_receta    INTEGER     PRIMARY KEY AUTOINCREMENT,
    id_consulta  INTEGER     NOT NULL UNIQUE,
    fecha        DATE        DEFAULT (DATE('now')),
    FOREIGN KEY (id_consulta) REFERENCES CONSULTA(id_consulta) ON DELETE CASCADE
);

CREATE TABLE DETALLE_RECETA (
    id_detalle   INTEGER     PRIMARY KEY AUTOINCREMENT,
    id_receta    INTEGER     NOT NULL,
    id_med       INTEGER     NOT NULL,
    dosis        VARCHAR(100),
    frecuencia   VARCHAR(80),
    duracion_dias INTEGER,
    FOREIGN KEY (id_receta) REFERENCES RECETA(id_receta) ON DELETE CASCADE,
    FOREIGN KEY (id_med)    REFERENCES MEDICAMENTO(id_med)
);

CREATE TABLE HOSPITALIZACION (
    id_hosp      INTEGER     PRIMARY KEY AUTOINCREMENT,
    ci_paciente  VARCHAR(10) NOT NULL,
    id_cama      INTEGER     NOT NULL,
    matricula    VARCHAR(20) NOT NULL,  -- médico responsable
    fecha_ingreso DATE       NOT NULL DEFAULT (DATE('now')),
    fecha_alta   DATE,                  -- NULL = hospitalizado actualmente
    motivo       TEXT,
    FOREIGN KEY (ci_paciente) REFERENCES PACIENTE(ci),
    FOREIGN KEY (id_cama)     REFERENCES CAMA(id_cama),
    FOREIGN KEY (matricula)   REFERENCES MEDICO(matricula)
);

-- Índices
CREATE INDEX idx_consulta_paciente ON CONSULTA(ci_paciente);
CREATE INDEX idx_consulta_medico   ON CONSULTA(matricula);
CREATE INDEX idx_consulta_fecha    ON CONSULTA(fecha_hora);
CREATE INDEX idx_hosp_paciente     ON HOSPITALIZACION(ci_paciente);
CREATE INDEX idx_hosp_activa       ON HOSPITALIZACION(fecha_alta);

-- ============================================================
-- DATOS DE EJEMPLO (mínimo para validar el esquema)
-- ============================================================

INSERT INTO ESPECIALIDAD (nombre) VALUES
    ('Medicina General'),('Pediatría'),('Cardiología'),
    ('Traumatología'),('Ginecología'),('Neurología'),
    ('Emergencias');

INSERT INTO SALA (nombre, tipo, total_camas) VALUES
    ('Sala General A', 'General', 20),
    ('UCI',            'UCI',     8),
    ('Pediatría',      'Pediatría',12),
    ('Maternidad',     'Maternidad',10),
    ('Emergencias',    'Emergencias',6);

-- Crear camas para cada sala
INSERT INTO CAMA (id_sala, numero) SELECT 1, value FROM (
    WITH RECURSIVE cnt(value) AS (SELECT 1 UNION ALL SELECT value+1 FROM cnt WHERE value<20)
    SELECT value FROM cnt
);
INSERT INTO CAMA (id_sala, numero) SELECT 2, value FROM (
    WITH RECURSIVE cnt(value) AS (SELECT 1 UNION ALL SELECT value+1 FROM cnt WHERE value<8)
    SELECT value FROM cnt
);

INSERT INTO LABORATORIO (nombre, pais) VALUES
    ('Bagó Bolivia','Bolivia'),('Pfizer','EEUU'),('Bayer','Alemania');

INSERT INTO MEDICAMENTO (codigo, nombre, principio_act, presentacion, precio, stock, stock_minimo, id_lab) VALUES
    ('H001','Paracetamol 500mg x100','Paracetamol',  'Tabletas',  25.00, 200, 30, 1),
    ('H002','Amoxicilina 500mg x100','Amoxicilina',  'Cápsulas',  85.00,  45, 20, 1),
    ('H003','Suero Fisiológico 1L',  'NaCl 0.9%',   'Solución', 18.00,   8, 15, 2),
    ('H004','Ibuprofeno 400mg x100', 'Ibuprofeno',  'Tabletas',  30.00,  60, 20, 1),
    ('H005','Morfina 10mg/1ml',      'Morfina',     'Inyectable',75.00,   5, 10, 3);

INSERT INTO PACIENTE (ci, nombre, apellido, fecha_nac, sexo, grupo_sang, telefono) VALUES
    ('7000001','Carlos',  'Mendoza',  '1985-06-12','M','O+','71234567'),
    ('7000002','Luisa',   'Torrez',   '1990-03-25','F','A+','72345678'),
    ('7000003','Roberto', 'Quispe',   '1975-11-08','M','B-','73456789'),
    ('7000004','Sandra',  'Molina',   '2005-01-15','F','O+','74567890'),
    ('7000005','Andrés',  'Vargas',   '1960-09-30','M','AB+','75678901');

INSERT INTO MEDICO (matricula, ci, nombre, apellido, telefono) VALUES
    ('MED-001','5000001','Jorge',    'Suárez',   '76789012'),
    ('MED-002','5000002','Patricia', 'Vaca',     '77890123'),
    ('MED-003','5000003','Ricardo',  'Flores',   '78901234');

INSERT INTO MEDICO_ESPECIALIDAD (matricula, id_esp, es_principal) VALUES
    ('MED-001',1,1),('MED-001',7,0),
    ('MED-002',2,1),
    ('MED-003',3,1),('MED-003',6,0);

INSERT INTO PERSONAL (ci, nombre, apellido, cargo, turno, salario) VALUES
    ('6000001','María',  'Rojas', 'Enfermero','mañana',3500.00),
    ('6000002','Karina', 'Paz',   'Secretaria','tarde', 3000.00),
    ('6000003','Diego',  'Vidal', 'Enfermero','noche',  3500.00);

INSERT INTO CONSULTA (ci_paciente, matricula, motivo, diagnostico, tratamiento, costo) VALUES
    ('7000001','MED-001','Fiebre y dolor de cabeza','Gripe estacional','Reposo, Paracetamol 500mg', 80.00),
    ('7000002','MED-001','Control prenatal','Embarazo 20 semanas','Vitaminas prenatales', 120.00),
    ('7000003','MED-003','Dolor en el pecho','Arritmia leve','Monitoreo, Enalapril', 200.00);

INSERT INTO RECETA (id_consulta) VALUES (1),(3);
INSERT INTO DETALLE_RECETA (id_receta, id_med, dosis, frecuencia, duracion_dias) VALUES
    (1, 1, '500mg', 'Cada 8 horas', 5),
    (2, 4, '400mg', 'Cada 12 horas', 7);

-- Hospitalización activa
UPDATE CAMA SET disponible = 0 WHERE id_cama = 1;
INSERT INTO HOSPITALIZACION (ci_paciente, id_cama, matricula, motivo) VALUES
    ('7000003', 1, 'MED-003', 'Monitoreo cardíaco');

-- ============================================================
-- VISTAS DE REFERENCIA
-- ============================================================

CREATE VIEW IF NOT EXISTS V_CAMAS_DISPONIBLES AS
SELECT s.nombre AS sala, s.tipo,
       s.total_camas,
       SUM(CASE WHEN c.disponible=1 THEN 1 ELSE 0 END) AS disponibles,
       SUM(CASE WHEN c.disponible=0 THEN 1 ELSE 0 END) AS ocupadas
FROM SALA s
JOIN CAMA c ON s.id_sala = c.id_sala
GROUP BY s.id_sala;

CREATE VIEW IF NOT EXISTS V_STOCK_CRITICO AS
SELECT codigo, nombre, stock, stock_minimo,
       (stock_minimo - stock) AS unidades_faltan
FROM MEDICAMENTO
WHERE stock < stock_minimo;

CREATE VIEW IF NOT EXISTS V_HISTORIAL_CONSULTAS AS
SELECT
    p.ci, p.nombre || ' ' || p.apellido AS paciente,
    c.fecha_hora, c.motivo, c.diagnostico,
    m.nombre || ' ' || m.apellido AS medico,
    e.nombre AS especialidad
FROM CONSULTA c
JOIN PACIENTE    p ON c.ci_paciente = p.ci
JOIN MEDICO      m ON c.matricula   = m.matricula
LEFT JOIN MEDICO_ESPECIALIDAD me ON m.matricula = me.matricula AND me.es_principal = 1
LEFT JOIN ESPECIALIDAD e ON me.id_esp = e.id_esp;

-- ============================================================
-- CONSULTAS DE VERIFICACIÓN
-- ============================================================

SELECT 'Pacientes registrados:', COUNT(*) FROM PACIENTE;
SELECT 'Médicos activos:',        COUNT(*) FROM MEDICO WHERE activo=1;
SELECT 'Consultas realizadas:',   COUNT(*) FROM CONSULTA;
SELECT 'Camas disponibles:' AS info, disponibles AS valor FROM V_CAMAS_DISPONIBLES;
SELECT 'Stock crítico:' AS info, nombre, stock, stock_minimo FROM V_STOCK_CRITICO;
