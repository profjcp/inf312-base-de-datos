# Guía: De requisitos narrativos a Diagrama Entidad-Relación (DER)

Esta guía muestra un proceso repetible para transformar una narración de cliente (requisitos en lenguaje natural) en un modelo conceptual (entidades, atributos, relaciones y cardinalidades) listo para dibujar un DER y luego mapear a un esquema relacional.

---

## Pasos (resumen rápido)

1. Recoger la narración del cliente (qué hace, actores, eventos, restricciones).
2. Identificar posibles entidades (sustantivos relevantes) y atributos.
3. Determinar claves primarias y tipos básicos para los atributos.
4. Detectar relaciones entre entidades y fijar cardinalidades (1:1, 1:N, N:M). Justificar cada cardinalidad según la narración.
5. Añadir restricciones importantes (unicidad, no null, checks, ciclos de vida — composición/ agregación).
6. Dibujar el DER (rectángulos para entidades, rombos para relaciones o usar notación crow's foot) y publicar.
7. Mapear a tablas relacionales (esquema), incluyendo tablas intermedias para N:M y llaves foráneas con acciones ON DELETE/ON UPDATE.

---

## Plantilla de captura de requisitos (usa esto para cada práctica)

- Título del caso: 
- Narración del cliente (1–4 párrafos): describir actores, procesos, excepciones, reglas de negocio.
- Suposiciones (si hay ambigüedad): listar lo que decides por ahora.
- Entidades iniciales (lista breve): sustantivos detectados.
- Reglas y restricciones extra: unicidades, límites, valores permitidos.

---

## Ejemplo completo 1 — Sistema de reservas de hotel

Título: Reservas y gestión de habitaciones — Hotel "Sol y Luna"

Narración del cliente:

"Soy el gerente del Hotel Sol y Luna. Necesitamos un sistema para gestionar habitaciones, reservas y pagos. Un cliente puede reservar una o varias habitaciones en una sola reserva (p. ej., familia). Cada habitación pertenece a un piso y tiene un tipo (individual, doble, suite). Las reservas tienen fecha de entrada y salida; debemos controlar ocupación (no permitir doble reserva de la misma habitación en fechas solapadas). Queremos registrar pagos (método, monto, fecha) y opcionalmente servicios contratados (desayuno, lavandería). Además el personal (recepción) crea y modifica reservas." 

Suposiciones:
- Identificamos cliente por documento o email.
- Una reserva puede incluir varias habitaciones y cada habitación puede estar en varias reservas en distintos períodos (relación N:M con entidad intermedia Reserva_Habitación que incluye precio por noche y número de huéspedes por habitación).

Entidades y atributos (modelo conceptual):

- CLIENTE
  - id_cliente (PK) — UUID o INTEGER
  - nombre VARCHAR(100) NOT NULL
  - apellido VARCHAR(100) NOT NULL
  - email VARCHAR(150) UNIQUE NOT NULL
  - telefono VARCHAR(20)

- HABITACION
  - id_habitacion (PK) — INTEGER
  - numero VARCHAR(10) UNIQUE NOT NULL
  - piso INTEGER NOT NULL
  - tipo VARCHAR(20) CHECK (tipo IN ('individual','doble','suite'))
  - capacidad INTEGER CHECK (capacidad > 0)

- RESERVA
  - id_reserva (PK)
  - id_cliente (FK → CLIENTE)
  - fecha_reserva DATE DEFAULT CURRENT_DATE
  - fecha_ingreso DATE NOT NULL
  - fecha_salida DATE NOT NULL
  - estado VARCHAR(20) CHECK (estado IN ('confirmada','cancelada','check-in','check-out'))

- RESERVA_HABITACION (entidad asociativa para N:M)
  - id_reserva (PK parcial, FK → RESERVA)
  - id_habitacion (PK parcial, FK → HABITACION)
  - precio_noche DECIMAL(8,2) NOT NULL
  - num_huespedes INTEGER DEFAULT 1

- PAGO
  - id_pago (PK)
  - id_reserva (FK → RESERVA)
  - metodo VARCHAR(30) CHECK (metodo IN ('efectivo','tarjeta','transferencia'))
  - monto DECIMAL(10,2) NOT NULL CHECK (monto >= 0)
  - fecha_pago DATE

- SERVICIO (catalogo de servicios)
  - id_servicio (PK)
  - nombre VARCHAR(100)
  - precio DECIMAL(8,2)

- RESERVA_SERVICIO (opcional: N:M entre RESERVA y SERVICIO)
  - id_reserva (FK)
  - id_servicio (FK)
  - cantidad INTEGER DEFAULT 1

Relaciones y cardinalidades (justificación):

- CLIENTE 1 — N RESERVA
  - Un cliente puede tener muchas reservas en el tiempo; cada reserva pertenece a un único cliente.

- RESERVA N — M HABITACION (implementada con RESERVA_HABITACION)
  - Una reserva puede incluir varias habitaciones; una habitación puede estar en muchas reservas en tiempos distintos.

- RESERVA 1 — N PAGO
  - Una reserva puede pagarse en varias transacciones (depósitos, saldo final). Cada pago corresponde a una reserva.

- RESERVA N — M SERVICIO (a través de RESERVA_SERVICIO)
  - Una reserva puede contratar varios servicios y un servicio puede aplicarse en muchas reservas.

Restricciones de negocio importantes:
- Validación de solapamiento: al insertar en RESERVA_HABITACION/RESERVA, verificar que no exista otra reserva que tenga la misma HABITACION con fechas que se intersecten (se realiza en la capa de aplicación o con triggers).
- Precio por noche se puede fijar en el momento de la reserva para evitar cambios por variaciones futuras.

Representación para DER:
- Entidades: rectángulos para CLIENTE, HABITACION, RESERVA, PAGO, SERVICIO.
- Entidad asociativa: RESERVA_HABITACION (rombo o rectángulo con doble línea según notación) con atributos propios.
- Cardinalidades: CLIENTE (1) — (N) RESERVA; RESERVA (N) — (M) HABITACION.

Mapeo relacional (breve ejemplo SQL):

```sql
CREATE TABLE CLIENTE (
  id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  telefono VARCHAR(20)
);

CREATE TABLE HABITACION (
  id_habitacion INTEGER PRIMARY KEY AUTOINCREMENT,
  numero VARCHAR(10) UNIQUE NOT NULL,
  piso INTEGER NOT NULL,
  tipo VARCHAR(20) NOT NULL,
  capacidad INTEGER NOT NULL CHECK(capacidad > 0)
);

CREATE TABLE RESERVA (
  id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
  id_cliente INTEGER NOT NULL REFERENCES CLIENTE(id_cliente),
  fecha_reserva DATE DEFAULT CURRENT_DATE,
  fecha_ingreso DATE NOT NULL,
  fecha_salida DATE NOT NULL,
  estado VARCHAR(20) NOT NULL
);

CREATE TABLE RESERVA_HABITACION (
  id_reserva INTEGER NOT NULL REFERENCES RESERVA(id_reserva) ON DELETE CASCADE,
  id_habitacion INTEGER NOT NULL REFERENCES HABITACION(id_habitacion),
  precio_noche DECIMAL(8,2) NOT NULL,
  num_huespedes INTEGER DEFAULT 1,
  PRIMARY KEY (id_reserva, id_habitacion)
);
```

---

## Ejemplo breve 2 — Plataforma de streaming de música (resumen)

Narración del cliente (resumen):
"Quiero una plataforma donde los usuarios creen playlists, escuchen canciones, y los artistas suban álbumes y pistas. Una pista puede pertenecer a un álbum; las pistas tienen duración, género; los usuarios pueden marcar 'me gusta' a pistas y seguir artistas."

Entidades principales: USUARIO, ARTISTA, ALBUM, PISTA, PLAYLIST, MEGUSTA (USUARIO-PISTA), SEGUIMIENTO (USUARIO-ARTISTA).

Relaciones clave:
- ARTISTA 1 — N ALBUM
- ALBUM 1 — N PISTA
- USUARIO N — M PLAYLIST (una playlist pertenece a un único usuario: USUARIO 1 — N PLAYLIST)
- USUARIO N — M PISTA (MEGUSTA)
- USUARIO N — M ARTISTA (SEGUIMIENTO)

Notas: PISTA puede tener atributos derivados como 'reproducciones_total' (derivado, no guardarlo necesariamente) y multivaluado como etiquetas/genres (mejor tabla separada PISTA_GENERO).

---

## Checklist para convertir a DER

- ¿Cada entidad tiene una PK clara?
- ¿Hay relaciones N:M que requieren tabla intermedia? ¿Sus atributos están en la intermedia?
- ¿Existen atributos multivaluados o compuestos? Si sí, normalizarlos a tablas o columnas simples.
- ¿Restricciones de unicidad y checks documentados?
- ¿Reglas de borrado (composición) o independencia (agregación) definidas?

---

## ¿Qué más puedo hacer por ti?
- Generar el DER (diagrama) en formato ASCII o en notación Mermaid para pegar en Markdown.
- Mapear el modelo completo a SQL (CREATE TABLE) con constraints y ejemplos de test data.
- Resolver ambigüedades del enunciado o convertir cualquiera de tus ejercicios en prácticas completas siguiendo esta guía.

---

_Este archivo fue añadido para proporcionar una plantilla y ejemplos prácticos que puedes reutilizar para las prácticas de la asignatura._
