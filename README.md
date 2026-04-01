# 🗄️ INF-312 | Base de Datos I

> **Universidad Autónoma "Gabriel René Moreno"**  
> **Facultad de Ingeniería en Ciencias de la Computación y Telecomunicaciones**  
> Quinto Semestre · 6 horas semanales (4HT + 2HP) · 5 créditos  
> Pre-requisito: INF-220

---

## 🎯 Objetivo General

Modelar bases de datos utilizando una metodología determinada asociada a un paradigma para la solución de problemas reales.

---

## 📂 Contenido del Repositorio

| Unidad | Tema | Horas |
|--------|------|-------|
| [Unidad I](./unidad1/) | Introducción a los Sistemas de Bases de Datos | 12 hs |
| [Unidad II](./unidad2/) | Diseño Conceptual bajo Modelo Orientado a Objetos | 20 hs |
| [Unidad III](./unidad3/) | Modelo Relacional | 18 hs |
| [Unidad IV](./unidad4/) | Lenguaje Estructurado de Consulta (SQL) | 20 hs |
| [Unidad V](./unidad5/) | Normalización y Dependencias Funcionales | 14 hs |
| [Proyecto Final](./proyecto/) | Diseño e implementación de BD caso real | — |

---

## 🗂️ Estructura de cada Unidad

```
unidadX/
├── README.md           ← Teoría completa con diagramas y ejemplos
├── teoria/
│   └── apuntes.md      ← Resumen, ejercicios resueltos y preguntas de examen
└── practica/
    ├── XX_practica.sql ← Scripts SQL ejecutables (SQLite)
    ├── XX_practica.py  ← Scripts Python con sqlite3
    └── enunciados.md   ← Enunciados de ejercicios prácticos
```

---

## ⚙️ Requisitos

### Para las prácticas SQL (Unidades III, IV, V)
```bash
# Opción A: SQLite (incluido en Python, sin instalación)
python3 -c "import sqlite3; print('SQLite OK')"

# Opción B: PostgreSQL
psql --version

# Opción C: MySQL / MariaDB
mysql --version
```

### Para los scripts Python
```bash
python --version  # Python 3.8 o superior
```

> 💡 **Todas las prácticas SQL están escritas para SQLite** (sin instalación adicional), pero incluyen notas de compatibilidad con PostgreSQL y MySQL.

### Herramientas de diagramado recomendadas

| Herramienta | Uso | Acceso |
|-------------|-----|--------|
| [dbdiagram.io](https://dbdiagram.io) | Diagramas ER desde SQL o DBML | Gratuito, web |
| [draw.io / diagrams.net](https://app.diagrams.net) | Diagramas UML y ER manuales | Gratuito, web |
| [DBeaver](https://dbeaver.io) | Cliente SQL + diagramas desde BD real | Gratuito, instalable |
| StarUML | Diagramas de clases UML profesionales | Descarga |

> Para el proyecto final se recomienda **draw.io** (fácil) o **StarUML** (profesional).

---

## 🗺️ Mapa del Curso

```
Unidad I                    Unidad II
¿Qué es una BD?     ──▶    Modelado Conceptual
(SGBD, arquitectura,        (Diagrama de Clases UML,
actores, ventajas)          Asociación, Herencia, Mapeo)
        │
        ▼
Unidad III                  Unidad IV
Modelo Relacional   ──▶    SQL Práctico
(Tablas, claves,            (DDL, DML, DCL,
álgebra relacional)         Consultas, Vistas)
        │
        ▼
Unidad V
Normalización
(1FN → 2FN → 3FN → FNBC → 4FN → 5FN)
        │
        ▼
Proyecto Final
(Caso real: conceptual → relacional → SQL)
```

---

## 📊 Sistema de Evaluación

| Ítem | Descripción | Porcentaje | Unidades |
|------|-------------|-----------|---------|
| 1 | Primer Examen Parcial | 20% | I, II |
| 2 | Segundo Examen Parcial | 20% | III, IV |
| 3 | Proyecto Final | 20% | Aplicación |
| 4 | Examen Final | 40% | Todas |

---

## 📚 Bibliografía

**Básica:**
- Elmasri & Navathe — *Fundamentos de Sistemas de Bases de Datos*, Addison Wesley, 3ª Ed. 2002
- Booch, Rumbaugh & Jacobson — *El Lenguaje Unificado de Modelamiento*, Addison Wesley, 1999

**Complementaria:**
- Date, C.J. — *Introducción a los Sistemas de Bases de Datos*, Addison Wesley, 6ª Ed. 1999
- Silberschatz, Korth & Sudarshan — *Fundamentos de Bases de Datos*, MacGrawHill, 4ª Ed. 2002

---

## 👨‍🏫 Docente

**Ing. Msc. Juan Carlos Peinado Pereira**  
🔗 [github.com/profjcp](https://github.com/profjcp)  
🏛️ UAGRM — Facultad de Ingeniería en Ciencias de la Computación y Telecomunicaciones

---

> 💡 ¿Encontraste un error o tienes una mejora? Abre un **Issue** o envía un **Pull Request**.
