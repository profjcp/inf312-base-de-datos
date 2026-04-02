# Unidad II · Banco de Evaluacion y Rubrica

## Objetivo

Evaluar modelado conceptual orientado a objetos y su traduccion correcta a diseno de BD.

## Formato sugerido (100 puntos)

| Componente | Puntos |
|------------|--------|
| Conceptos UML | 25 |
| Diagrama de clases de caso | 45 |
| Justificacion de decisiones | 30 |

## Banco de preguntas

### Parte A · Teoria UML

1. Diferencia clase y objeto con ejemplo del dominio universitario.
2. Explica atributo simple, compuesto, derivado y multivaluado.
3. Diferencia asociacion, agregacion y composicion.
4. Que significa multiplicidad 0..1, 1..*, *.
5. Que es generalizacion y cuando usar herencia.

### Parte B · Caso de modelado

Caso: sistema de biblioteca con socios, prestamos, libros, ejemplares y autores.

1. Modela al menos 6 clases con atributos y PK.
2. Define relaciones y multiplicidades correctas.
3. Identifica una composicion y una agregacion justificadas.
4. Modela una jerarquia PERSONA -> SOCIO, EMPLEADO (si aplica).

### Parte C · Calidad del modelo

1. Detecta 3 posibles ambiguedades del diagrama y corrige.
2. Explica por que una relacion N:M requiere clase asociativa.
3. Propone 4 reglas de negocio para convertir despues a restricciones SQL.

## Criterios de correccion rapida

- Correccion de entidades y atributos: 35%
- Consistencia de relaciones y multiplicidades: 40%
- Justificacion tecnica: 25%

## Errores frecuentes

- Multiplicidades invertidas.
- Uso incorrecto de composicion donde era asociacion.
- Mezclar detalles fisicos SQL en fase conceptual.
