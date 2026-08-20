# Práctica: Sistema de Reservas de Hotel — Enunciado para entrega

Título: Sistema de Reservas de Hotel — Práctica (Entregable)

Enunciado:
El Hotel "Sol y Luna" necesita un sistema de base de datos para gestionar clientes, habitaciones, reservas, pagos y servicios. Entre los requisitos:
- Un cliente puede realizar reservas; una reserva pertenece a un único cliente.
- Una reserva puede incluir varias habitaciones (familia/paquetes) y la asociación guarda precio por noche y número de huéspedes por habitación.
- No se permiten solapamientos de reservas para una misma habitación.
- Se registra un catálogo de servicios (desayuno, lavandería, spa) que pueden ser contratados por reserva.
- Una reserva puede pagarse en múltiples transacciones.
- Se requiere generar consultas para: (a) ocupación de una fecha concreta (habitaciones ocupadas), (b) total facturado por reserva, (c) historial de reservas por cliente.

Entregables (archivos):
- SQL: schema.sql (CREATE TABLE, constraints, triggers, índices)
- SQL: data.sql (datos de prueba)
- MERMAID: der_hotel.mmd (diagrama mermaid)
- README.md: explicación de decisiones/modelado y consultas solicitadas

Rúbrica (100 pts):
- Modelo conceptual claro con entidades, atributos y claves (20 pts)
- Relaciones y cardinalidades justificadas (15 pts)
- Esquema SQL correcto con PK/FK y constraints (25 pts)
- Trigger o mecanismo para evitar solapamientos (15 pts)
- Consultas solicitadas implementadas y funcionando con datos de prueba (15 pts)
- Documentación y comentarios en SQL / README (10 pts)

Solución (resumen):
- Tablas: CLIENTE, HABITACION, RESERVA, RESERVA_HABITACION, PAGO, SERVICIO, RESERVA_SERVICIO.
- Restricciones: CHECK para fechas y tipos; UNIQUE en email y numero de habitacion.
- Trigger en reserva_habitacion que previene solapamientos; ON DELETE CASCADE para dependencias de reserva.
- Consultas ejemplo: ocupación por fecha (JOIN entre RESERVA, RESERVA_HABITACION y HABITACION), total facturado por reserva (SUM de pagos + servicios), historial por cliente (SELECT con JOINs).
