-- practica/01_herencia_mapeo.sql
-- Unidad II: Mapeo Objeto-Relacional en SQL
-- ==========================================
-- Implementa los 3 tipos de mapeo de herencia + N:M + composición

-- ============================================================
-- CASO: SISTEMA DE BIBLIOTECA UAGRM
-- ============================================================
-- Diagrama de clases:
--   PERSONA ──▷ SOCIO
--   PERSONA ──▷ BIBLIOTECARIO
--   LIBRO ──────────── AUTOR  (N:M)
--   LIBRO ──────── EJEMPLAR   (composición)
--   SOCIO ────────── PRESTAMO (1:N)
--   PRESTAMO ◆──── MULTA      (composición)

-- ============================================================
-- OPCIÓN C: TABLA POR CLASE (mapeo de herencia recomendado)
-- ============================================================

CREATE TABLE IF NOT EXISTS PERSONA (
    ci         VARCHAR(10)  PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    apellido   VARCHAR(100) NOT NULL,
    fecha_nac  DATE,
    telefono   VARCHAR(20),
    tipo       VARCHAR(15)  NOT NULL
               CHECK (tipo IN ('socio', 'bibliotecario'))
);

-- Socio: extiende PERSONA
CREATE TABLE IF NOT EXISTS SOCIO (
    ci         VARCHAR(10) PRIMARY KEY,
    num_socio  INTEGER     UNIQUE NOT NULL,
    fecha_alta DATE        DEFAULT (DATE('now')),
    activo     INTEGER     DEFAULT 1,   -- 1=sí, 0=no
    FOREIGN KEY (ci) REFERENCES PERSONA(ci) ON DELETE CASCADE
);

-- Bibliotecario: extiende PERSONA
CREATE TABLE IF NOT EXISTS BIBLIOTECARIO (
    ci         VARCHAR(10) PRIMARY KEY,
    legajo     VARCHAR(20) UNIQUE NOT NULL,
    turno      VARCHAR(10) CHECK (turno IN ('mañana','tarde','noche')),
    FOREIGN KEY (ci) REFERENCES PERSONA(ci) ON DELETE CASCADE
);

-- ============================================================
-- LIBRO y su composición con EJEMPLAR
-- ============================================================

CREATE TABLE IF NOT EXISTS EDITORIAL (
    id_editorial INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre       VARCHAR(100) NOT NULL,
    pais         VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS AUTOR (
    id_autor  INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre    VARCHAR(100) NOT NULL,
    pais      VARCHAR(50),
    anio_nac  INTEGER
);

CREATE TABLE IF NOT EXISTS LIBRO (
    isbn          VARCHAR(20)  PRIMARY KEY,
    titulo        VARCHAR(200) NOT NULL,
    anio_pub      INTEGER,
    num_paginas   INTEGER,
    id_editorial  INTEGER,
    FOREIGN KEY (id_editorial) REFERENCES EDITORIAL(id_editorial)
);

-- N:M: Un libro puede tener varios autores; un autor escribe varios libros
CREATE TABLE IF NOT EXISTS LIBRO_AUTOR (
    isbn      VARCHAR(20) NOT NULL,
    id_autor  INTEGER     NOT NULL,
    es_principal INTEGER  DEFAULT 0,   -- 1 = autor principal
    PRIMARY KEY (isbn, id_autor),
    FOREIGN KEY (isbn)     REFERENCES LIBRO(isbn) ON DELETE CASCADE,
    FOREIGN KEY (id_autor) REFERENCES AUTOR(id_autor)
);

-- EJEMPLAR: composición con LIBRO (si se borra el libro, se borran ejemplares)
CREATE TABLE IF NOT EXISTS EJEMPLAR (
    id_ejemplar INTEGER     PRIMARY KEY AUTOINCREMENT,
    isbn        VARCHAR(20) NOT NULL,
    codigo_bar  VARCHAR(30) UNIQUE NOT NULL,
    estado      VARCHAR(20) DEFAULT 'disponible'
                CHECK (estado IN ('disponible','prestado','dañado','baja')),
    FOREIGN KEY (isbn) REFERENCES LIBRO(isbn) ON DELETE CASCADE
);

-- ============================================================
-- PRÉSTAMO y su composición con MULTA
-- ============================================================

CREATE TABLE IF NOT EXISTS PRESTAMO (
    id_prestamo   INTEGER     PRIMARY KEY AUTOINCREMENT,
    ci_socio      VARCHAR(10) NOT NULL,
    id_ejemplar   INTEGER     NOT NULL,
    ci_biblio     VARCHAR(10),           -- quién atendió
    fecha_inicio  DATE        NOT NULL DEFAULT (DATE('now')),
    fecha_limite  DATE        NOT NULL,
    fecha_devol   DATE,                  -- NULL si aún no devuelto
    devuelto      INTEGER     DEFAULT 0,
    FOREIGN KEY (ci_socio)  REFERENCES SOCIO(ci),
    FOREIGN KEY (id_ejemplar) REFERENCES EJEMPLAR(id_ejemplar),
    FOREIGN KEY (ci_biblio) REFERENCES BIBLIOTECARIO(ci)
);

-- MULTA: composición con PRÉSTAMO (no existe sin el préstamo)
CREATE TABLE IF NOT EXISTS MULTA (
    id_multa    INTEGER     PRIMARY KEY AUTOINCREMENT,
    id_prestamo INTEGER     NOT NULL UNIQUE,  -- 1:1 con préstamo
    monto       DECIMAL(8,2) NOT NULL,
    motivo      VARCHAR(100),
    pagada      INTEGER     DEFAULT 0,
    fecha_pago  DATE,
    FOREIGN KEY (id_prestamo) REFERENCES PRESTAMO(id_prestamo) ON DELETE CASCADE
);

-- ============================================================
-- INSERTAR DATOS DE PRUEBA
-- ============================================================

INSERT OR IGNORE INTO EDITORIAL VALUES (1, 'Addison Wesley', 'EEUU');
INSERT OR IGNORE INTO EDITORIAL VALUES (2, 'McGraw Hill',    'EEUU');
INSERT OR IGNORE INTO EDITORIAL VALUES (3, 'Prentice Hall',  'EEUU');

INSERT OR IGNORE INTO AUTOR VALUES (1, 'Ramez Elmasri',   'EEUU', 1952);
INSERT OR IGNORE INTO AUTOR VALUES (2, 'Shamkant Navathe','EEUU', 1950);
INSERT OR IGNORE INTO AUTOR VALUES (3, 'Abraham Silberschatz', 'EEUU', 1952);
INSERT OR IGNORE INTO AUTOR VALUES (4, 'Henry Korth',     'EEUU', 1953);

INSERT OR IGNORE INTO LIBRO VALUES ('978-0-321-12521-7','Fundamentos de Sistemas de BD',2002,1008,1);
INSERT OR IGNORE INTO LIBRO VALUES ('978-0-073-52332-7','Fundamentos de Bases de Datos', 2010, 954,2);
INSERT OR IGNORE INTO LIBRO VALUES ('978-0-201-54329-7','Introducción a los Sistemas de BD',1999,896,1);

INSERT OR IGNORE INTO LIBRO_AUTOR VALUES ('978-0-321-12521-7', 1, 1);
INSERT OR IGNORE INTO LIBRO_AUTOR VALUES ('978-0-321-12521-7', 2, 0);
INSERT OR IGNORE INTO LIBRO_AUTOR VALUES ('978-0-073-52332-7', 3, 1);
INSERT OR IGNORE INTO LIBRO_AUTOR VALUES ('978-0-073-52332-7', 4, 0);

INSERT OR IGNORE INTO EJEMPLAR VALUES (1,'978-0-321-12521-7','BC-001','disponible');
INSERT OR IGNORE INTO EJEMPLAR VALUES (2,'978-0-321-12521-7','BC-002','prestado');
INSERT OR IGNORE INTO EJEMPLAR VALUES (3,'978-0-073-52332-7','BC-003','disponible');

INSERT OR IGNORE INTO PERSONA VALUES ('7654321','Ana','García','2000-03-15','72345678','socio');
INSERT OR IGNORE INTO PERSONA VALUES ('8123456','Luis','Mamani','1999-07-22','71234567','socio');
INSERT OR IGNORE INTO PERSONA VALUES ('1000001','Carmen','Rojas','1985-05-10','76543210','bibliotecario');

INSERT OR IGNORE INTO SOCIO VALUES ('7654321',1001,'2022-03-01',1);
INSERT OR IGNORE INTO SOCIO VALUES ('8123456',1002,'2022-03-15',1);
INSERT OR IGNORE INTO BIBLIOTECARIO VALUES ('1000001','LIB-001','mañana');

INSERT OR IGNORE INTO PRESTAMO VALUES (
    1,'7654321',2,'1000001','2024-03-01','2024-03-15',NULL,0
);

INSERT OR IGNORE INTO MULTA VALUES (
    1, 1, 5.00, 'Devolución tardía', 0, NULL
);

-- ============================================================
-- CONSULTAS QUE DEMUESTRAN EL MAPEO
-- ============================================================

-- Ver la herencia reconstruida (JOIN entre PERSONA y SOCIO)
SELECT p.ci, p.nombre || ' ' || p.apellido AS nombre_completo,
       p.fecha_nac, s.num_socio, s.activo
FROM PERSONA p
JOIN SOCIO s ON p.ci = s.ci;

-- Ver libros con todos sus autores (N:M)
SELECT l.titulo,
       GROUP_CONCAT(a.nombre, ', ') AS autores,
       e.nombre AS editorial,
       l.anio_pub
FROM LIBRO l
JOIN LIBRO_AUTOR la ON l.isbn = la.isbn
JOIN AUTOR a        ON la.id_autor = a.id_autor
JOIN EDITORIAL e    ON l.id_editorial = e.id_editorial
GROUP BY l.isbn;

-- Ver préstamos con multas (composición)
SELECT p2.nombre || ' ' || p2.apellido AS socio,
       li.titulo,
       pr.fecha_inicio,
       pr.fecha_limite,
       CASE WHEN pr.devuelto=1 THEN 'Devuelto' ELSE 'Pendiente' END AS estado,
       COALESCE(CAST(m.monto AS TEXT), 'Sin multa') AS multa
FROM PRESTAMO pr
JOIN SOCIO s       ON pr.ci_socio = s.ci
JOIN PERSONA p2    ON s.ci = p2.ci
JOIN EJEMPLAR ej   ON pr.id_ejemplar = ej.id_ejemplar
JOIN LIBRO li      ON ej.isbn = li.isbn
LEFT JOIN MULTA m  ON pr.id_prestamo = m.id_prestamo;
