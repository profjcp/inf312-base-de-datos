# Unidad III · Banco de Evaluacion y Rubrica

## Objetivo

Evaluar dominio del modelo relacional, restricciones e interpretacion de algebra relacional.

## Formato sugerido (100 puntos)

| Componente | Puntos |
|------------|--------|
| Modelo relacional y restricciones | 35 |
| Algebra relacional | 35 |
| Traduccion a SQL y validacion | 30 |

## Banco de preguntas

### Parte A · Fundamentos relacionales

1. Define dominio, atributo, tupla, relacion y cardinalidad.
2. Diferencia clave candidata, primaria y alternativa.
3. Explica integridad de entidad con ejemplo invalido.
4. Explica integridad referencial con un caso de FK inexistente.
5. Describe que puede romper INSERT, UPDATE y DELETE.

### Parte B · Algebra relacional

Dado un esquema ESTUDIANTE, MATERIA, INSCRIPCION:

1. Expresa en algebra y SQL: estudiantes aprobados en INF312.
2. Expresa en algebra y SQL: estudiantes que cursan INF312 o INF220.
3. Expresa en algebra y SQL: materias sin inscritos.
4. Expresa en algebra y SQL: docentes que dictan todas las materias de nivel 3.

### Parte C · Analisis de decisiones

1. En que casos elegir ON DELETE CASCADE vs RESTRICT.
2. Disena 3 restricciones CHECK utiles para INSCRIPCION.
3. Propone un diccionario de datos minimo para 2 tablas.

## Criterios de correccion rapida

- Correctitud formal: 40%
- Equivalencia algebra-SQL: 35%
- Capacidad de justificar restricciones: 25%

## Errores frecuentes

- Confundir proyeccion con seleccion.
- Perder condiciones de join al pasar a SQL.
- Ignorar valores NULL en reglas de integridad.
