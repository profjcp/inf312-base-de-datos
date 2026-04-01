# Unidad I — Apuntes y Ejercicios Resueltos

## Resumen de conceptos clave

### Definiciones esenciales

| Término | Definición breve |
|---------|-----------------|
| **Base de Datos** | Colección organizada de datos relacionados que representa un minimundo |
| **SGBD** | Software que gestiona el almacenamiento, recuperación y seguridad de los datos |
| **Instancia** | Los datos que contiene una BD en un momento concreto |
| **Esquema** | La descripción estructural de la BD (tablas, tipos, restricciones) |
| **Metadatos** | Datos que describen a otros datos; almacenados en el catálogo del SGBD |
| **Minimundo** | La parte del mundo real que la BD modela |

---

## Ejercicio resuelto 1 — Comparativa SGBD

**Enunciado:** Compara SQLite, PostgreSQL y MySQL para los siguientes escenarios:

| Escenario | SGBD recomendado | Justificación |
|-----------|-----------------|---------------|
| App móvil con almacenamiento local | SQLite | Sin servidor, archivo único, sin instalación |
| Sistema web con miles de usuarios concurrentes | PostgreSQL | ACID completo, soporte de concurrencia avanzado |
| Sistema de e-commerce de mediano porte | MySQL o PostgreSQL | Ambos válidos; MySQL más extendido en LAMP |
| Prototipo rápido o pruebas en clase | SQLite | Cero configuración, Python lo incluye |
| BD geoespacial (mapas, coordenadas) | PostgreSQL + PostGIS | Extensión nativa con funciones espaciales |

---

## Ejercicio resuelto 2 — Los tres niveles de abstracción (Arquitectura ANSI/SPARC)

```
┌─────────────────────────────────────────────────────┐
│  NIVEL EXTERNO (Vistas)                             │
│  Lo que ve cada usuario o aplicación                │
│                                                     │
│  Vista alumno:           Vista secretaria:          │
│  mis_notas (ci, materia, │ inscripciones (ci,       │
│  gestion, nota)          │ nombre, codigo, gestion) │
└───────────────────────────────────────────────────── ┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│  NIVEL CONCEPTUAL (Esquema lógico global)           │
│  Todas las tablas, relaciones y restricciones       │
│                                                     │
│  ESTUDIANTE(ci, nombre, apellido, id_carrera)       │
│  MATERIA(codigo, nombre, creditos)                  │
│  INSCRIPCION(ci, codigo, gestion, nota)             │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│  NIVEL INTERNO (Almacenamiento físico)              │
│  Archivos, páginas, índices, estructuras de disco   │
│                                                     │
│  tabla_estudiante.db → B-Tree indexado por ci       │
│  tabla_inscripcion.db → Hash index por (ci,codigo)  │
└─────────────────────────────────────────────────────┘

Independencia lógica: cambiar el nivel conceptual sin afectar las vistas externas.
Independencia física: cambiar el almacenamiento sin afectar el nivel conceptual.
```

---

## Ejercicio resuelto 3 — Actores en un SGBD universitario

| Actor | Ejemplo | Operaciones típicas |
|-------|---------|---------------------|
| **DBA** (Administrador) | Jefe de TI de la UAGRM | CREATE TABLE, GRANT, backup, optimización |
| **Diseñador de BD** | Analista de sistemas | Diseño del esquema, normalización |
| **Programador de aplicaciones** | Desarrollador del SIU | INSERT, UPDATE, SELECT a través de API |
| **Usuario final casual** | Docente consultando notas | Consultas simples predefinidas |
| **Usuario final sofisticado** | Analista de datos | Consultas SQL complejas directas |

---

## Preguntas de repaso frecuentes en examen parcial

1. ¿Cuál es la diferencia entre una base de datos y un SGBD?  
   *La BD son los datos; el SGBD es el software que los gestiona.*

2. ¿Qué significa que un sistema de BD es "autodescriptivo"?  
   *El SGBD almacena tanto los datos como su estructura (metadatos/catálogo) en la misma plataforma.*

3. ¿Qué es la independencia de datos y por qué es importante?  
   *Permite cambiar el nivel físico o conceptual sin afectar a las aplicaciones. Reduce el costo de mantenimiento.*

4. Enumera 5 ventajas de usar un SGBD vs archivos planos:  
   *Elimina redundancia, garantiza integridad, controla concurrencia, facilita seguridad, permite consultas ad-hoc.*

5. ¿Cuándo NO conviene usar un SGBD?  
   *Cuando los datos son simples y estáticos, el sistema tiene un solo usuario y las consultas son triviales. Ej: configuración en un archivo .ini.*
