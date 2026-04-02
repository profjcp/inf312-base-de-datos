# Unidad IV · Banco de Evaluacion y Rubrica

## Objetivo

Evaluar implementacion SQL completa: DDL, DML, consultas avanzadas, vistas y transacciones.

## Formato sugerido (100 puntos)

| Componente | Puntos |
|------------|--------|
| DDL y restricciones | 30 |
| DML y manejo de datos | 20 |
| Consultas avanzadas | 35 |
| Transacciones y buenas practicas | 15 |

## Banco de preguntas

### Parte A · DDL

1. Crea tablas ESTUDIANTE, MATERIA e INSCRIPCION con PK/FK/CHECK.
2. Agrega indices para busquedas por apellido y por (ci, codigo).
3. Explica por que una FK debe tener accion ON DELETE definida.

### Parte B · DML

1. Inserta datos de prueba coherentes para 5 estudiantes y 8 inscripciones.
2. Escribe un UPDATE para subir 5 puntos a notas entre 45 y 50.
3. Escribe un DELETE seguro y explica por que no afecta de mas.

### Parte C · Consultas

1. JOIN de estudiante, materia y nota con alias claros.
2. LEFT JOIN para encontrar materias sin inscritos.
3. Subconsulta para estudiantes con promedio mayor al promedio general.
4. CTE para ranking de materias por promedio.
5. Consulta con ventana ROW_NUMBER por materia.

### Parte D · Transacciones y seguridad

1. Simula transferencia entre cuentas con BEGIN, COMMIT y ROLLBACK.
2. Explica SQL injection y como evitarla con placeholders en Python.

## Criterios de correccion rapida

- SQL ejecutable sin errores: 35%
- Exactitud de resultados: 35%
- Calidad y legibilidad de consultas: 20%
- Seguridad y buenas practicas: 10%

## Errores frecuentes

- JOIN sin condicion.
- UPDATE/DELETE sin WHERE.
- Uso incorrecto de GROUP BY y HAVING.
