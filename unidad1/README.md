# Unidad I · Introducción a los Sistemas de Bases de Datos

**Tiempo:** 12 horas  
**Objetivo:** Describir los componentes de un sistema de base de datos.

---

## 1.1 Introducción: Conceptos Generales

### ¿Qué es una Base de Datos?

Una **base de datos (BD)** es una colección de datos relacionados que representa algún aspecto del mundo real (un "minimundo"), diseñada para ser compartida por múltiples usuarios y aplicaciones.

```
Mundo real (minimundo)          Base de Datos
─────────────────────           ─────────────────────────────────
Universidad UAGRM     ──▶      ESTUDIANTE(ci, nombre, carrera)
 - Estudiantes                  MATERIA(codigo, nombre, creditos)
 - Materias                     INSCRIPCION(ci, codigo, gestion)
 - Inscripciones                ...
```

### ¿Qué es un Sistema de Gestión de Bases de Datos (SGBD)?

Un **SGBD** (o DBMS en inglés) es el software que permite crear, mantener y usar bases de datos. Es el intermediario entre los usuarios/aplicaciones y los datos almacenados.

```
┌────────────────────────────────────────────────────┐
│                   USUARIOS                         │
│   👤 Admin    👩‍💻 Programador    👨‍🎓 Usuario final  │
└───────────────────────┬────────────────────────────┘
                        │ consultas, actualizaciones
                        ▼
┌────────────────────────────────────────────────────┐
│              SGBD (Software)                       │
│  MySQL · PostgreSQL · Oracle · SQL Server · SQLite │
└───────────────────────┬────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│           Base de Datos (Datos)                    │
│   Tablas · Índices · Procedimientos · Vistas       │
└────────────────────────────────────────────────────┘
```

### Diferencia: Archivos vs Base de Datos

| Característica | Archivos planos | Base de Datos |
|---------------|----------------|---------------|
| Redundancia | Alta | Controlada |
| Inconsistencia | Frecuente | Evitada |
| Acceso concurrente | Difícil | Gestionado |
| Seguridad | Básica | Detallada |
| Integridad | Manual | Automática |
| Consultas complejas | Difícil | SQL estándar |

---

## 1.2 Características del Enfoque de Bases de Datos

### Las 4 características fundamentales

**1. Naturaleza autodescriptiva del sistema de BD**

El SGBD contiene tanto los datos como su descripción (metadatos). El catálogo del sistema describe la estructura de la BD.

```
Catálogo (metadatos) del SGBD:
  Tabla ESTUDIANTE:
    - ci        : VARCHAR(10)  NOT NULL  PK
    - nombre    : VARCHAR(100) NOT NULL
    - carrera   : VARCHAR(50)
    - fecha_nac : DATE

Datos reales:
  | ci        | nombre        | carrera   |
  |-----------|---------------|-----------|
  | 7654321   | Ana García    | Sistemas  |
  | 8123456   | Luis Mamani   | Redes     |
```

**2. Aislamiento entre programas y datos (abstracción)**

Los programas no dependen del almacenamiento físico. Si se cambia la estructura interna, los programas no se ven afectados.

**3. Soporte para múltiples vistas de los datos**

Cada usuario puede ver solo la parte de la BD que le corresponde:
```
Vista del Docente:   ESTUDIANTE(ci, nombre, nota)
Vista del Admin:     ESTUDIANTE(ci, nombre, carrera, fecha_nac, contacto)
Vista de Tesorería:  ESTUDIANTE(ci, nombre, estado_pago)
```

**4. Compartición de datos y procesamiento de transacciones multiusuario**

Múltiples usuarios pueden acceder y modificar datos simultáneamente sin conflictos, gracias al control de concurrencia.

---

## 1.3 Los Actores de los Sistemas de Bases de Datos

```
Actores que interactúan con la BD:

👷 Diseñador de BD
   └─ Define la estructura: tablas, relaciones, restricciones

🔧 Administrador de BD (DBA)
   └─ Gestiona el SGBD: rendimiento, seguridad, respaldos

👩‍💻 Programador de aplicaciones
   └─ Escribe programas que usan la BD (Java, Python, PHP...)

👨‍🎓 Usuario final (naïf)
   └─ Usa la BD a través de interfaces, sin saber SQL

🧑‍🔬 Analista de sistemas
   └─ Analiza requisitos y especifica la BD a diseñar
```

---

## 1.4 Implicaciones del Enfoque de Bases de Datos

### Ventajas del enfoque de BD sobre archivos tradicionales

| Ventaja | Descripción |
|---------|-------------|
| **Control de redundancia** | Un dato se almacena una sola vez |
| **Restricción de acceso** | Permisos granulares por usuario |
| **Almacenamiento persistente** | Los datos sobreviven a las aplicaciones |
| **Soporte para múltiples interfaces** | SQL, GUI, API, reportes |
| **Representación de relaciones** | Vínculos entre datos de distintas tablas |
| **Cumplimiento de restricciones** | Integridad garantizada por el SGBD |
| **Respaldo y recuperación** | El SGBD gestiona backups automáticos |

---

## 1.5 Arquitectura de un SGBD (3 niveles ANSI/SPARC)

La arquitectura de 3 niveles separa la forma en que los usuarios ven los datos, de cómo están organizados lógicamente y cómo se almacenan físicamente.

```
┌─────────────────────────────────────────────────────────────┐
│  NIVEL EXTERNO (Vistas)                                     │
│  Lo que ve cada grupo de usuarios                           │
│  Vista Alumno │ Vista Docente │ Vista Admin                 │
├─────────────────────────────────────────────────────────────┤
│  NIVEL CONCEPTUAL (Esquema lógico)                          │
│  Estructura completa de la BD: todas las tablas y           │
│  relaciones, sin depender del almacenamiento físico         │
│  ESTUDIANTE, MATERIA, INSCRIPCION, DOCENTE...               │
├─────────────────────────────────────────────────────────────┤
│  NIVEL INTERNO (Esquema físico)                             │
│  Cómo se almacenan los datos en disco:                      │
│  archivos, índices, bloques, páginas, clustering            │
└─────────────────────────────────────────────────────────────┘

Independencia lógica: cambios en el esquema conceptual
  no afectan las vistas externas.
Independencia física: cambios en el almacenamiento
  no afectan el esquema conceptual.
```

---

## 1.6 Lenguajes e Interfaces de un SGBD

### Lenguajes

| Lenguaje | Sigla | Función | Ejemplos SQL |
|---------|-------|---------|-------------|
| Definición de datos | DDL | Crear/modificar estructura | `CREATE TABLE`, `ALTER`, `DROP` |
| Manipulación de datos | DML | Insertar/consultar/actualizar/borrar | `SELECT`, `INSERT`, `UPDATE`, `DELETE` |
| Control de datos | DCL | Permisos y transacciones | `GRANT`, `REVOKE`, `COMMIT`, `ROLLBACK` |

### Interfaces de usuario

```
Interfaces de un SGBD típico:
  📋 Interfaz de línea de comandos (psql, mysql, sqlite3)
  🖥️  Interfaz gráfica (pgAdmin, MySQL Workbench, DBeaver)
  📊 Generadores de informes (Crystal Reports, Power BI)
  🌐 Interfaz web (phpMyAdmin)
  💻 API de programación (JDBC, ODBC, SQLAlchemy)
  📝 Formularios de entrada de datos (aplicaciones de usuario)
```

---

## 1.7 Clasificación de los SGBD

### Por modelo de datos

```
Relacional (más común):
  MySQL · PostgreSQL · Oracle · SQL Server · SQLite
  → Datos en tablas relacionadas por claves

NoSQL (no relacional):
  MongoDB (documentos JSON)
  Redis (clave-valor)
  Cassandra (columnar)
  Neo4j (grafos)

Objeto-Relacional:
  PostgreSQL · Oracle (extensiones de objetos)

Orientado a Objetos puro:
  db4o · ObjectDB
```

### Por número de usuarios

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| Monousuario | Un solo usuario a la vez | SQLite, MS Access |
| Multiusuario | Varios usuarios simultáneos | MySQL, PostgreSQL, Oracle |

### Por distribución

```
Centralizado   → datos en un solo servidor
Distribuido    → datos repartidos en varios nodos de red
En la nube     → Amazon RDS, Google Cloud SQL, Azure SQL
```

---

## 1.8 Ventajas de Utilizar un SGBD

```
✅ Control centralizado de datos
✅ Reducción de redundancia e inconsistencia
✅ Acceso eficiente mediante SQL
✅ Seguridad y control de acceso
✅ Integridad de datos garantizada
✅ Copias de seguridad y recuperación ante fallos
✅ Soporte para transacciones concurrentes (ACID)
✅ Independencia entre datos y aplicaciones
```

---

## 1.9 Cuando NO Utilizar un SGBD

A pesar de sus ventajas, hay casos donde un SGBD puede ser innecesario o contraproducente:

```
❌ Datos simples y estáticos (no cambian frecuentemente)
   → Un archivo CSV puede ser suficiente

❌ Aplicaciones en tiempo real estricto
   → La sobrecarga del SGBD puede ser inaceptable

❌ Datos no estructurados (imágenes, videos, audio)
   → Mejor un sistema de archivos especializado

❌ Sistemas embebidos con recursos muy limitados
   → SQLite es la alternativa (sin servidor)

❌ Costo y complejidad no justificados
   → Para proyectos muy pequeños o prototipos rápidos
```

---

## 📁 Archivos de esta unidad

| Archivo | Descripción |
|---------|-------------|
| [`practica/01_intro_sqlite.py`](./practica/01_intro_sqlite.py) | Primera BD con Python y SQLite |
| [`practica/01_intro.sql`](./practica/01_intro.sql) | Primeros comandos SQL |
| [`practica/enunciados.md`](./practica/enunciados.md) | Ejercicios de la unidad |
| [`teoria/apuntes.md`](./teoria/apuntes.md) | Resumen, ejercicios resueltos y preguntas de examen |
