# GUIA DE CLASES
## INF-312 BASE DE DATOS I

Universidad Autonoma Gabriel Rene Moreno  
Semestre: Quinto  
Carga horaria: 6 horas por semana (4HT + 2HP)  
Duracion sugerida: 15 semanas

---

## 1. PROPOSITO DE ESTA GUIA

Esta guia organiza el curso en una ruta de aprendizaje clara para estudiantes. Integra teoria, practica, evaluacion continua y proyecto final para que cada semana tenga objetivos concretos y evidencia de avance.

## 2. OBJETIVO GENERAL DEL CURSO

Modelar e implementar bases de datos para resolver problemas reales, aplicando modelado conceptual, modelo relacional, SQL y normalizacion.

## 3. RESULTADOS DE APRENDIZAJE ESPERADOS

Al finalizar el curso, el estudiante sera capaz de:

- Explicar fundamentos de los sistemas de bases de datos y su arquitectura.
- Construir modelos conceptuales con UML para casos reales.
- Transformar modelos conceptuales a esquema relacional con restricciones.
- Implementar y consultar bases de datos con SQL (DDL, DML, consultas avanzadas).
- Normalizar esquemas hasta 3FN y justificar decisiones de diseno.
- Integrar todo lo anterior en un proyecto funcional.

## 4. METODOLOGIA DE TRABAJO POR CLASE

Cada semana se sugiere esta secuencia:

1. Activacion de conocimientos previos (10-15 min).
2. Exposicion teorica breve y focalizada (40-60 min).
3. Demostracion guiada por el docente (30-40 min).
4. Taller practico en equipos o individual (60-90 min).
5. Cierre con retroalimentacion y mini evaluacion (15-20 min).

## 5. PLAN DE CLASES (15 SEMANAS)

### Semana 1 - Introduccion a BD y SGBD

- Tema central: conceptos base, minimundo, diferencia entre archivos y BD.
- Objetivo de clase: identificar problemas de datos en sistemas basados en archivos.
- Actividad practica: analisis de un caso real con redundancia e inconsistencia.
- Evidencia: resumen conceptual + glosario de terminos.

### Semana 2 - Arquitectura y actores del SGBD

- Tema central: niveles ANSI/SPARC, actores y responsabilidades.
- Objetivo de clase: interpretar como fluye una consulta desde usuario a almacenamiento.
- Actividad practica: mapa de actores y vistas externas para un caso universitario.
- Evidencia: mini cuestionario de 10 preguntas.

### Semana 3 - Modelado conceptual OO: clases y atributos

- Tema central: clases, objetos, atributos y tipos de atributos.
- Objetivo de clase: definir entidades y atributos de un caso de negocio.
- Actividad practica: primer borrador de diagrama de clases.
- Evidencia: diagrama UML inicial.

### Semana 4 - Relaciones y multiplicidades en UML

- Tema central: asociacion, agregacion, composicion, generalizacion.
- Objetivo de clase: definir relaciones correctas y cardinalidades.
- Actividad practica: correccion colectiva de diagramas.
- Evidencia: diagrama UML corregido con multiplicidades.

### Semana 5 - Mapeo objeto-relacional

- Tema central: reglas de transformacion de clases a tablas.
- Objetivo de clase: obtener esquema relacional preliminar.
- Actividad practica: mapeo de herencia y relaciones N:M.
- Evidencia: esquema relacional inicial del proyecto.

### Semana 6 - Modelo relacional y restricciones

- Tema central: dominios, claves, integridad de entidad y referencial.
- Objetivo de clase: disenar tablas consistentes con restricciones.
- Actividad practica: deteccion de violaciones de integridad en ejemplos SQL.
- Evidencia: lista de restricciones por tabla.

### Semana 7 - Algebra relacional basica

- Tema central: seleccion, proyeccion, renombrar, joins.
- Objetivo de clase: expresar consultas formales y pasarlas a SQL.
- Actividad practica: resolver 8 consultas algebra + SQL.
- Evidencia: hoja de ejercicios resueltos.

### Semana 8 - Algebra avanzada y evaluacion parcial

- Tema central: operaciones de conjuntos, division relacional y casos complejos.
- Objetivo de clase: resolver consultas con mayor nivel de abstraccion.
- Actividad practica: simulacro de parcial.
- Evidencia: evaluacion parcial 1.

### Semana 9 - SQL DDL

- Tema central: CREATE, ALTER, DROP, constraints e indices.
- Objetivo de clase: construir un script DDL completo y robusto.
- Actividad practica: creacion de esquema del proyecto en SQLite.
- Evidencia: script DDL ejecutable sin errores.

### Semana 10 - SQL DML y transacciones

- Tema central: INSERT, UPDATE, DELETE, ACID.
- Objetivo de clase: manipular datos sin comprometer consistencia.
- Actividad practica: carga de datos de prueba y casos de rollback.
- Evidencia: script DML validado.

### Semana 11 - SQL consultas intermedias y avanzadas

- Tema central: JOIN, subconsultas, GROUP BY, HAVING.
- Objetivo de clase: construir consultas de analisis para reportes.
- Actividad practica: set de consultas del caso hospital.
- Evidencia: banco de consultas comentadas.

### Semana 12 - CTE, vistas y SQL con Python

- Tema central: WITH, funciones de ventana, vistas y uso de sqlite3.
- Objetivo de clase: automatizar consultas desde codigo.
- Actividad practica: script Python para consultas parametrizadas.
- Evidencia: script funcional y evidencia de resultados.

### Semana 13 - Dependencias funcionales y 1FN-2FN

- Tema central: deteccion de dependencias y anomalias.
- Objetivo de clase: iniciar normalizacion formal del proyecto.
- Actividad practica: normalizar tablas problematicas a 2FN.
- Evidencia: documento de dependencias funcionales.

### Semana 14 - 3FN y FNBC

- Tema central: eliminacion de dependencias transitivas y casos limite.
- Objetivo de clase: cerrar normalizacion y justificar decisiones.
- Actividad practica: auditoria tecnica del esquema final.
- Evidencia: version final normalizada.

### Semana 15 - Integracion, defensa y cierre

- Tema central: presentacion del proyecto final.
- Objetivo de clase: demostrar dominio integral del proceso de diseno e implementacion.
- Actividad practica: defensa tecnica por equipo.
- Evidencia: entrega final + defensa.

## 6. SISTEMA DE EVALUACION SUGERIDO

- Primer parcial (Unidades I-II): 20%
- Segundo parcial (Unidades III-IV): 20%
- Proyecto final: 20%
- Examen final integrador: 40%

## 7. ESTRATEGIA DE SEGUIMIENTO DEL ESTUDIANTE

Checklist semanal:

- Comprende los conceptos teoricos clave de la semana.
- Resuelve al menos un ejercicio por nivel (basico, medio, reto).
- Sube evidencia practica ejecutable.
- Corrige errores detectados en retroalimentacion.
- Actualiza avance del proyecto.

## 8. RECOMENDACIONES DIDACTICAS PARA ESTUDIANTES

- Llegar a clase con lectura previa de teoria.
- Trabajar con datos pequenos antes de escalar consultas.
- Documentar errores frecuentes y su solucion.
- Verificar siempre resultados SQL con casos de prueba.
- Integrar cada unidad al proyecto, no dejar todo al final.

## 9. PRODUCTO FINAL DEL CURSO

Cada equipo debe entregar:

- Diagrama conceptual UML validado.
- Esquema relacional con PK/FK y restricciones.
- Script SQL completo (DDL, DML, consultas y vistas).
- Evidencia de normalizacion hasta 3FN.
- Presentacion y defensa tecnica.

## 10. BIBLIOGRAFIA BASE

- Elmasri y Navathe, Fundamentos de Sistemas de Bases de Datos.
- Silberschatz, Korth y Sudarshan, Fundamentos de Bases de Datos.
- Date, Introduccion a los Sistemas de Bases de Datos.

---

Fin de la guia de clases.
