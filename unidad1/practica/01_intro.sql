-- practica/01_intro.sql
-- Unidad I: Primeros pasos con SQL y SQLite
-- ==========================================
-- Ejecutar con: sqlite3 universidad.db < 01_intro.sql
-- O copiar y pegar en DB Browser for SQLite

-- ============================================
-- CREAR LA BASE DE DATOS DE LA UNIVERSIDAD
-- ============================================

-- DDL: Crear tablas (estructura)
CREATE TABLE IF NOT EXISTS CARRERA (
    id_carrera   INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre       VARCHAR(100) NOT NULL,
    duracion_años INTEGER DEFAULT 5
);

CREATE TABLE IF NOT EXISTS ESTUDIANTE (
    ci           VARCHAR(10)  PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    apellido     VARCHAR(100) NOT NULL,
    fecha_nac    DATE,
    id_carrera   INTEGER,
    FOREIGN KEY (id_carrera) REFERENCES CARRERA(id_carrera)
);

CREATE TABLE IF NOT EXISTS MATERIA (
    codigo       VARCHAR(10)  PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    creditos     INTEGER      NOT NULL CHECK (creditos > 0),
    nivel        INTEGER      CHECK (nivel BETWEEN 1 AND 10)
);

CREATE TABLE IF NOT EXISTS INSCRIPCION (
    id_inscripcion INTEGER     PRIMARY KEY AUTOINCREMENT,
    ci             VARCHAR(10) NOT NULL,
    codigo         VARCHAR(10) NOT NULL,
    gestion        VARCHAR(6)  NOT NULL,  -- ej: 2024-I
    nota           DECIMAL(5,2),
    FOREIGN KEY (ci)     REFERENCES ESTUDIANTE(ci),
    FOREIGN KEY (codigo) REFERENCES MATERIA(codigo),
    UNIQUE (ci, codigo, gestion)
);

-- ============================================
-- DML: Insertar datos (poblar la BD)
-- ============================================

INSERT INTO CARRERA (nombre, duracion_años) VALUES
    ('Ingeniería en Sistemas', 5),
    ('Ingeniería en Telecomunicaciones', 5),
    ('Licenciatura en Informática', 4);

INSERT INTO ESTUDIANTE (ci, nombre, apellido, fecha_nac, id_carrera) VALUES
    ('7654321', 'Ana',    'García',  '2000-03-15', 1),
    ('8123456', 'Luis',   'Mamani',  '1999-07-22', 1),
    ('9234567', 'María',  'López',   '2001-01-10', 2),
    ('5432198', 'Carlos', 'Quispe',  '2000-11-05', 1),
    ('6789012', 'Sofía',  'Pereira', '2001-06-30', 3);

INSERT INTO MATERIA (codigo, nombre, creditos, nivel) VALUES
    ('INF220', 'Estructuras de Datos I',   5, 3),
    ('INF310', 'Estructuras de Datos II',  5, 4),
    ('INF312', 'Base de Datos I',          5, 5),
    ('INF315', 'Base de Datos II',         5, 6),
    ('INF320', 'Sistemas Operativos',      5, 5);

INSERT INTO INSCRIPCION (ci, codigo, gestion, nota) VALUES
    ('7654321', 'INF220', '2023-I',  85.5),
    ('7654321', 'INF310', '2023-II', 78.0),
    ('7654321', 'INF312', '2024-I',  NULL),  -- cursando actualmente
    ('8123456', 'INF220', '2023-I',  90.0),
    ('8123456', 'INF310', '2023-II', 65.0),
    ('9234567', 'INF220', '2023-I',  55.0),  -- reprobó
    ('5432198', 'INF220', '2023-I',  72.0),
    ('5432198', 'INF312', '2024-I',  NULL);

-- ============================================
-- Consultas de verificación
-- ============================================

-- ¿Cuántos estudiantes hay por carrera?
SELECT c.nombre AS carrera, COUNT(e.ci) AS num_estudiantes
FROM CARRERA c
LEFT JOIN ESTUDIANTE e ON c.id_carrera = e.id_carrera
GROUP BY c.nombre;

-- ¿Qué materias está cursando Ana García?
SELECT e.nombre || ' ' || e.apellido AS estudiante,
       m.nombre AS materia,
       i.gestion,
       CASE WHEN i.nota IS NULL THEN 'Cursando'
            WHEN i.nota >= 51  THEN 'Aprobado'
            ELSE 'Reprobado'
       END AS estado
FROM INSCRIPCION i
JOIN ESTUDIANTE e ON i.ci = e.ci
JOIN MATERIA m    ON i.codigo = m.codigo
WHERE e.nombre = 'Ana'
ORDER BY i.gestion;
