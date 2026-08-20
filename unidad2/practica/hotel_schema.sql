-- Esquema: Sistema de Reservas (PostgreSQL)
BEGIN;

-- CLIENTE
CREATE TABLE cliente (
  id_cliente     SERIAL PRIMARY KEY,
  nombre         VARCHAR(100) NOT NULL,
  apellido       VARCHAR(100) NOT NULL,
  email          VARCHAR(150) NOT NULL UNIQUE,
  telefono       VARCHAR(20)
);

-- HABITACION
CREATE TABLE habitacion (
  id_habitacion  SERIAL PRIMARY KEY,
  numero         VARCHAR(10) NOT NULL UNIQUE,
  piso           INTEGER NOT NULL,
  tipo           VARCHAR(20) NOT NULL CHECK (tipo IN ('individual','doble','suite')),
  capacidad      INTEGER NOT NULL CHECK (capacidad > 0)
);

-- RESERVA
CREATE TABLE reserva (
  id_reserva     SERIAL PRIMARY KEY,
  id_cliente     INTEGER NOT NULL REFERENCES cliente(id_cliente),
  fecha_reserva  DATE NOT NULL DEFAULT CURRENT_DATE,
  fecha_ingreso  DATE NOT NULL,
  fecha_salida   DATE NOT NULL,
  estado         VARCHAR(20) NOT NULL CHECK (estado IN ('confirmada','cancelada','check-in','check-out')),
  CHECK (fecha_ingreso < fecha_salida)
);

-- Entidad asociativa RESERVA_HABITACION
CREATE TABLE reserva_habitacion (
  id_reserva     INTEGER NOT NULL REFERENCES reserva(id_reserva) ON DELETE CASCADE,
  id_habitacion  INTEGER NOT NULL REFERENCES habitacion(id_habitacion),
  precio_noche   NUMERIC(10,2) NOT NULL CHECK (precio_noche >= 0),
  num_huespedes  INTEGER DEFAULT 1 CHECK (num_huespedes > 0),
  comentario     VARCHAR(255),
  PRIMARY KEY (id_reserva, id_habitacion)
);

-- PAGO
CREATE TABLE pago (
  id_pago        SERIAL PRIMARY KEY,
  id_reserva     INTEGER NOT NULL REFERENCES reserva(id_reserva) ON DELETE CASCADE,
  metodo         VARCHAR(30) CHECK (metodo IN ('efectivo','tarjeta','transferencia')),
  monto          NUMERIC(12,2) NOT NULL CHECK (monto >= 0),
  fecha_pago     DATE NOT NULL DEFAULT CURRENT_DATE
);

-- SERVICIO y relación RESERVA_SERVICIO
CREATE TABLE servicio (
  id_servicio    SERIAL PRIMARY KEY,
  nombre         VARCHAR(100) NOT NULL,
  descripcion    VARCHAR(255),
  precio         NUMERIC(10,2) NOT NULL CHECK (precio >= 0)
);

CREATE TABLE reserva_servicio (
  id_reserva     INTEGER NOT NULL REFERENCES reserva(id_reserva) ON DELETE CASCADE,
  id_servicio    INTEGER NOT NULL REFERENCES servicio(id_servicio),
  cantidad       INTEGER DEFAULT 1 CHECK (cantidad > 0),
  precio_unitario NUMERIC(10,2) NOT NULL CHECK (precio_unitario >= 0),
  PRIMARY KEY (id_reserva, id_servicio)
);

-- Índices útiles
CREATE INDEX idx_reserva_fecha ON reserva(fecha_ingreso, fecha_salida);
CREATE INDEX idx_rh_habitacion ON reserva_habitacion(id_habitacion);

-- Trigger function para evitar solapamiento (INSERT/UPDATE en reserva_habitacion)
CREATE OR REPLACE FUNCTION trg_check_no_solapamiento() RETURNS TRIGGER AS $$
DECLARE
  v_ing DATE;
  v_sal DATE;
BEGIN
  -- obtener fechas de la reserva que se está vinculando
  SELECT fecha_ingreso, fecha_salida INTO v_ing, v_sal FROM reserva WHERE id_reserva = NEW.id_reserva;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'Reserva % no existe', NEW.id_reserva;
  END IF;

  -- verificar si existe alguna otra reserva para la misma habitación con rango que intersecte
  IF EXISTS (
    SELECT 1
    FROM reserva r
    JOIN reserva_habitacion rh ON r.id_reserva = rh.id_reserva
    WHERE rh.id_habitacion = NEW.id_habitacion
      AND r.id_reserva <> NEW.id_reserva
      AND NOT (r.fecha_salida <= v_ing OR r.fecha_ingreso >= v_sal)
  ) THEN
    RAISE EXCEPTION 'Solapamiento de reserva para la habitación % en las fechas % - %', NEW.id_habitacion, v_ing, v_sal;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_no_solapamiento_ins
BEFORE INSERT ON reserva_habitacion
FOR EACH ROW EXECUTE FUNCTION trg_check_no_solapamiento();

CREATE TRIGGER trg_no_solapamiento_upd
BEFORE UPDATE ON reserva_habitacion
FOR EACH ROW EXECUTE FUNCTION trg_check_no_solapamiento();

-- Datos de ejemplo
INSERT INTO cliente (nombre, apellido, email, telefono) VALUES ('Ana','García','ana@example.com','72345678');
INSERT INTO habitacion (numero, piso, tipo, capacidad) VALUES ('101',1,'doble',2);
INSERT INTO habitacion (numero, piso, tipo, capacidad) VALUES ('102',1,'suite',4);

INSERT INTO reserva (id_cliente, fecha_ingreso, fecha_salida, estado) VALUES (1,'2026-09-01','2026-09-05','confirmada');
INSERT INTO reserva_habitacion (id_reserva, id_habitacion, precio_noche, num_huespedes) VALUES (1,1,120.00,2);
INSERT INTO pago (id_reserva, metodo, monto) VALUES (1,'tarjeta',240.00);

COMMIT;
