-- Tablas principales (resumen)
CREATE TABLE duenio (
  id_duenio SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  email VARCHAR(150),
  telefono VARCHAR(20)
);

CREATE TABLE mascota (
  id_mascota SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  especie VARCHAR(50) NOT NULL,
  fecha_nac DATE,
  sexo VARCHAR(10),
  atributos_especificos JSONB
);

CREATE TABLE duenios_mascota (
  id_mascota INTEGER REFERENCES mascota(id_mascota) ON DELETE CASCADE,
  id_duenio INTEGER REFERENCES duenio(id_duenio),
  rol VARCHAR(20) DEFAULT 'propietario',
  PRIMARY KEY (id_mascota, id_duenio)
);

CREATE TABLE veterinario (
  id_vet SERIAL PRIMARY KEY,
  nombre VARCHAR(100),
  apellido VARCHAR(100),
  especialidad VARCHAR(100),
  matricula VARCHAR(50) UNIQUE
);

CREATE TABLE consulta (
  id_consulta SERIAL PRIMARY KEY,
  id_mascota INTEGER NOT NULL REFERENCES mascota(id_mascota),
  id_vet INTEGER REFERENCES veterinario(id_vet),
  fecha TIMESTAMP NOT NULL DEFAULT NOW(),
  motivo VARCHAR(255),
  diagnostico TEXT
);

CREATE TABLE medicamento (
  id_med SERIAL PRIMARY KEY,
  nombre VARCHAR(150),
  presentacion VARCHAR(100)
);

CREATE TABLE receta (
  id_consulta INTEGER REFERENCES consulta(id_consulta) ON DELETE CASCADE,
  id_med INTEGER REFERENCES medicamento(id_med),
  dosis VARCHAR(50),
  frecuencia VARCHAR(50),
  instrucciones TEXT,
  PRIMARY KEY (id_consulta, id_med)
);

CREATE TABLE vacuna (
  id_vac SERIAL PRIMARY KEY,
  nombre VARCHAR(150),
  fabricante VARCHAR(150)
);

CREATE TABLE aplicacion_vacuna (
  id_aplicacion SERIAL PRIMARY KEY,
  id_mascota INTEGER REFERENCES mascota(id_mascota),
  id_vac INTEGER REFERENCES vacuna(id_vac),
  fecha DATE,
  lote VARCHAR(50)
);
