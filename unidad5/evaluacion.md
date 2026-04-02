# Unidad V · Banco de Evaluacion y Rubrica

## Objetivo

Evaluar identificacion de dependencias funcionales, deteccion de anomalias y normalizacion hasta 3FN/FNBC.

## Formato sugerido (100 puntos)

| Componente | Puntos |
|------------|--------|
| Dependencias funcionales | 30 |
| Proceso de normalizacion | 50 |
| Analisis critico y desnormalizacion | 20 |

## Banco de preguntas

### Parte A · Dependencias funcionales

1. Define X -> Y y da 3 ejemplos validos.
2. Identifica dependencias completas, parciales y transitivas en una tabla dada.
3. Determina claves candidatas para un esquema con PK compuesta.

### Parte B · Normalizacion aplicada

1. Lleva una tabla 0FN a 1FN corrigiendo atributos multivaluados.
2. Lleva una tabla 1FN a 2FN eliminando dependencias parciales.
3. Lleva una tabla 2FN a 3FN eliminando transitivas.
4. Evalua si una tabla en 3FN viola FNBC y descomponla si corresponde.

### Parte C · Analisis de trade-offs

1. Describe 3 anomalias de actualizacion y donde aparecen.
2. Propone un caso real donde conviene desnormalizar.
3. Explica el costo de mantenimiento de datos desnormalizados.

## Criterios de correccion rapida

- Correctitud de dependencias: 35%
- Calidad de descomposiciones: 45%
- Justificacion de decisiones: 20%

## Errores frecuentes

- Confundir dependencia parcial con transitiva.
- Separar tablas sin conservar sentido del negocio.
- Buscar FNBC sin verificar primero 3FN.
