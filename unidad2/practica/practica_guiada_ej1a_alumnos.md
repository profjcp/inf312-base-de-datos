# Práctica guiada — Sistema de Reservas de Hotel (pistas para alumnos)

Objetivo de aprendizaje:
- Identificar entidades/atributos a partir de una narración de cliente.
- Modelar relaciones y cardinalidades y justificar decisiones.
- Normalizar atributos multivaluados y mapear a tablas relacionales.
- Implementar restricciones de integridad y una comprobación de negocio (solapamiento de reservas).

Actividad paso a paso (con pistas):
1. Leer la narración y subrayar sustantivos. Pista: ¿Quiénes son actores? (cliente, recepción, hotel, habitación, servicio).
2. Proponer una lista inicial de entidades. Pista: ¿Qué objetos tienen identidad propia y vida independiente? (cliente, habitación, reserva, pago, servicio).
3. Para cada entidad listar atributos mínimos y la clave primaria. Pista: ¿Qué permite identificar unívocamente un cliente? (email o id).
4. Detectar relaciones N:M. Pista: Si una reserva puede incluir varias habitaciones y viceversa ¿qué haces? (crear entidad asociativa).
5. Definir cardinalidades con justificación en una frase por relación.
6. Escribir un esquema SQL con PK, FK y constraints básicos (NOT NULL, UNIQUE, CHECK).
7. Implementar en la base de datos la comprobación de solapamiento. Pista: puedes comprobar con SELECT antes de INSERT o usar triggers.
8. Probar con casos que deberían fallar (dos reservas superpuestas) y casos que deberían pasar.

Preguntas de entrega (para el alumno):
- Adjunta el DER (Mermaid o imagen).
- Adjunta el script SQL para crear la BD y un script con datos de prueba.
- Incluye 3 consultas: (a) habitaciones ocupadas en fecha X, (b) total facturado por reserva Y, (c) historial de reservas de cliente Z.
- Describe 2 decisiones de modelado que tomaste (p. ej., fijar precio_noche en la asociación).

Checklist de evaluación (para autocontrol):
- [ ] Cada entidad tiene PK
- [ ] No hay atributos multivaluados en la misma tabla
- [ ] Relaciones N:M modeladas con tabla intermedia
- [ ] Restricciones de integridad definidas (CHECK/UNIQUE)
- [ ] Mecanismo para evitar solapamientos probado
- [ ] Consultas solicitadas funcionan con datos de prueba
