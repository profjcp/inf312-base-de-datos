# Universidad · Ingeniería en Ciencias de la Computacion · Quinto Semestre

# INF-312
# BASES DE DATOS I

Guia Completa de la Materia · Teoria y Practica con SQL y Python

## UNIDADES DEL CURSO

- Introduccion a Sistemas de Bases de Datos
- Diseno Conceptual Orientado a Objetos (UML)
- Modelo Relacional y Algebra Relacional
- SQL: DDL, DML, Consultas Avanzadas y Vistas
- Normalizacion y Dependencias Funcionales
- Proyecto Integrador: Sistema de Gestion Hospitalaria

Docente: Juan Carlos Peinado Pereira  
Repositorio oficial: https://github.com/profjcp/inf312-base-de-datos  
Gestion academica: 2026

---

## TABLA DE CONTENIDOS

1. Presentacion de la guia
2. Prerrequisitos y alcance del curso
3. Mapa formativo del curso
4. Unidad I · Introduccion a los Sistemas de BD
5. Unidad II · Diseno Conceptual con UML
6. Unidad III · Modelo Relacional
7. Unidad IV · SQL aplicado
8. Unidad V · Normalizacion
9. Proyecto final integrador
10. Sistema de evaluacion
11. Bibliografia y recursos

---

## 1. Presentacion de la guia

Esta guia organiza la materia INF-312 en una progresion pedagogica clara, con enfoque en aprendizaje por evidencia. Cada unidad integra teoria esencial, practica guiada y aplicacion al proyecto final.

## 2. Prerrequisitos y alcance del curso

### Prerrequisitos

- Manejo basico de computacion.
- Logica de programacion introductoria.
- Se recomienda nociones basicas de Python.

### Alcance

El estudiante aprendera a modelar y construir bases de datos relacionales para resolver problemas reales, desde el analisis conceptual hasta la implementacion SQL y validacion por normalizacion.

---

## 3. Mapa formativo del curso

Unidad I                  Unidad II
Fundamentos BD       ->   Modelado conceptual UML
(actores, arquitectura)    (clases, relaciones, cardinalidades)

Unidad III                Unidad IV
Modelo relacional    ->   SQL aplicado
(claves, integridad,        (DDL, DML, JOIN, vistas,
algebra relacional)          transacciones, CTE)

Unidad V                  Proyecto final
Normalizacion        ->   Integracion completa
(1FN, 2FN, 3FN, FNBC)      (diseno + implementacion + defensa)

---

## 4. Unidad I · Introduccion a los Sistemas de BD

### Competencia

Describe componentes, arquitectura y ventajas del enfoque de bases de datos frente a sistemas basados en archivos.

### Contenidos nucleares

- Concepto de base de datos y minimundo.
- Rol del SGBD.
- Caracteristicas del enfoque BD.
- Arquitectura ANSI/SPARC.
- Actores del sistema de BD.

### Practica sugerida

- Analizar un caso real con redundancia de datos.
- Identificar anomalias de inconsistencia.
- Diseñar vistas por perfil de usuario.

### Evidencia esperada

- Glosario tecnico.
- Cuestionario conceptual.
- Mapa de arquitectura del caso.

---

## 5. Unidad II · Diseno Conceptual con UML

### Competencia

Construye diagramas de clases coherentes con reglas de negocio y relaciones correctamente multiplicadas.

### Contenidos nucleares

- Clases, objetos y atributos.
- Asociacion y cardinalidades.
- Herencia (generalizacion).
- Agregacion y composicion.
- Mapeo objeto-relacional inicial.

### Practica sugerida

- Modelado de biblioteca u hospital en UML.
- Revision de multiplicidades ambiguas.
- Identificacion de clase asociativa en relaciones N:M.

### Evidencia esperada

- Diagrama UML completo.
- Justificacion de decisiones de modelado.
- Esquema preliminar para mapeo relacional.

---

## 6. Unidad III · Modelo Relacional

### Competencia

Transforma el modelo conceptual en esquema relacional validado por claves y restricciones de integridad.

### Contenidos nucleares

- Dominios, atributos y tuplas.
- Claves candidatas, primaria y foranea.
- Integridad de entidad y referencial.
- Operaciones de actualizacion y politicas ON DELETE/ON UPDATE.
- Algebra relacional y equivalencia en SQL.

### Practica sugerida

- Resolver consultas con sigma, pi, join, union, interseccion y diferencia.
- Detectar violaciones de integridad en escenarios de insercion y borrado.
- Definir diccionario de datos por tabla.

### Evidencia esperada

- Esquema relacional consolidado.
- Restricciones justificadas.
- Coleccion algebra + SQL validada.

---

## 7. Unidad IV · SQL aplicado

### Competencia

Implementa bases de datos y resuelve consultas de complejidad creciente en SQL, integrando scripts desde Python.

### Contenidos nucleares

- DDL: CREATE, ALTER, DROP, INDEX.
- DML: INSERT, UPDATE, DELETE.
- Consultas basicas y avanzadas.
- JOINs, subconsultas, CTE, funciones de ventana.
- Vistas y transacciones ACID.
- SQL seguro desde Python con parametros.

### Practica sugerida

- Script completo de creacion y carga de datos.
- Banco de consultas del caso hospital.
- Vistas de operacion y reportes.
- Simulacion de rollback en transacciones.

### Evidencia esperada

- Script SQL ejecutable de inicio a fin.
- Resultados de consultas validados.
- Script Python con consultas parametrizadas.

---

## 8. Unidad V · Normalizacion

### Competencia

Identifica dependencias funcionales y elimina anomalias mediante normalizacion hasta 3FN y analisis de FNBC.

### Contenidos nucleares

- Dependencias funcionales.
- 1FN, 2FN, 3FN.
- Dependencias parciales y transitivas.
- FNBC y casos limite.
- Desnormalizacion justificada.

### Practica sugerida

- Normalizar casos en varias etapas.
- Auditar tablas del proyecto para detectar anomalias.
- Justificar trade-offs entre consistencia y rendimiento.

### Evidencia esperada

- Matriz de dependencias funcionales.
- Documento de normalizacion del esquema final.

---

## 9. Proyecto final integrador

Caso base: Sistema de gestion de hospital.

### Entregables

- Diseno conceptual UML.
- Esquema relacional normalizado.
- Script SQL (DDL + DML + consultas + vistas).
- Informe de resultados y defensa tecnica.

### Hitos recomendados

- Semana 2: alcance y reglas de negocio.
- Semana 5: UML consolidado.
- Semana 8: esquema relacional.
- Semana 12: implementacion SQL funcional.
- Semana 14: normalizacion final.
- Semana 15: entrega y defensa.

---

## 10. Sistema de evaluacion sugerido

- Primer parcial: 20% (Unidades I y II)
- Segundo parcial: 20% (Unidades III y IV)
- Proyecto final: 20%
- Examen final: 40%

Criterio transversal de aprobacion: evidencia practica ejecutable y capacidad de justificar decisiones tecnicas.

---

## 11. Bibliografia y recursos

### Bibliografia base

- Elmasri y Navathe. Fundamentos de Sistemas de Bases de Datos.
- Silberschatz, Korth y Sudarshan. Fundamentos de Bases de Datos.
- Date, C.J. Introduccion a los Sistemas de Bases de Datos.

### Recursos del repositorio

- README general de la materia.
- READMEs por unidad.
- Enunciados practicos por unidad.
- Banco de evaluacion por unidad.
- Rubrica de defensa del proyecto.

---

Fin del documento.
