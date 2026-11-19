# AGENTS.md — Curso de Programación con .NET

## Naturaleza

Este repositorio es un **curso práctico de 16 semanas de Programación con .NET**, no una aplicación única.

El curso está organizado en **3 unidades** y **semanas** de clase. Cada semana es autocontenida e incluye explicación, ejemplo guiado, ejercicios y recursos de apoyo.

Estructura general:

```txt
unidad-01-fundamentos-csharp/          (semanas 1-5)
unidad-02-poo-avalonia/                (semanas 6-11)
unidad-03-datos-proyecto-integrador/   (semanas 12-16)
ejercicios-formativos/                  (ejercicios formativos)
_archivo/                              (material archivado de versiones anteriores)
```

Cada semana sigue una estructura similar:

```txt
semana-XX-nombre/
├── semana-XX.md
├── html/slides.html
├── ejemplo-guiado/
├── ejercicios/
├── dudas/
└── README.md
```

Las semanas de evaluación son carpetas de proyecto:

```txt
proyecto-unidad-01/            (semana 5)
proyecto-unidad-02/            (semana 11)
proyecto-integrador-unidad-03/ (semana 15)
```

---

## Enfoque pedagógico

El curso debe ser **altamente práctico**.

El objetivo es enseñar programación con C#, .NET, Programación Orientada a Objetos, interfaces gráficas con Avalonia UI y acceso a datos con ADO.NET + SQLite.

El curso debe poder desarrollarse desde:

* Linux
* Windows
* macOS

Herramienta principal recomendada:

```txt
Visual Studio Code + .NET SDK
```

---

## Duración y calendario

```txt
16 semanas · 3 unidades · lunes a viernes
10 de agosto al 25 de noviembre
```

| Unidad | Semanas | Tema | Evaluación |
|--------|---------|------|------------|
| 1 — Fundamentos C# | 1-5 | .NET, sintaxis, control de flujo, métodos | P1 (25%) |
| 2 — POO e Interfaces | 6-11 | Clases, encapsulamiento, herencia, polimorfismo, Avalonia UI | P2 (30%) |
| 3 — Datos e Integración | 12-16 | ADO.NET, SQLite, CRUD, capas, proyecto integrador | P3 (45%) |

Calendario:

```txt
S1:  Introducción al curso y plataforma .NET        (10-16 ago)
S2:  Fundamentos del lenguaje C#                    (17-23 ago)
S3:  Control de flujo y colecciones                 (24-30 ago)
S4:  Métodos, modularidad y manejo de excepciones   (31 ago-6 sep)
S5:  Evaluación Unidad 1 — Proyecto P1              (7-13 sep)
S6:  Introducción a la POO                          (14-20 sep)
S7:  Encapsulamiento y relaciones entre clases      (21-27 sep)
S8:  Herencia, interfaces y polimorfismo            (28 sep-4 oct)
S9:  Introducción a Avalonia UI                     (5-11 oct)
S10: Eventos, validación y navegación               (12-18 oct)
S11: Evaluación Unidad 2 — Proyecto P2              (19-25 oct)
S12: Fundamentos de acceso a datos con ADO.NET      (26 oct-1 nov)
S13: Comandos y recuperación de información         (2-8 nov)
S14: Operaciones CRUD y organización por capas      (9-15 nov)
S15: Proyecto Integrador Final                      (16-22 nov)
S16: Retroalimentación y cierre                     (23-25 nov)
```

---

## Stack principal

```txt
Lenguaje: C# (.NET 8 LTS)
Editor: Visual Studio Code
Control de versiones: Git + GitHub
UI: Avalonia UI 11.x
Base de datos: SQLite
Acceso a datos: ADO.NET (Microsoft.Data.Sqlite) — sin ORM
```

Nota importante: los ejemplos Avalonia usan paquetes serie **11.x** (no 12.x) porque el SDK .NET 8 no soporta aún los analizadores de Avalonia 12. Fijar versiones en los `.csproj`.

---

## Comandos base de .NET CLI

Crear proyecto de consola:

```bash
dotnet new console -n MiApp
cd MiApp
dotnet run
```

Instalar plantillas Avalonia:

```bash
dotnet new install Avalonia.Templates
dotnet new avalonia.app -o MiAppGrafica
```

Agregar SQLite:

```bash
dotnet add package Microsoft.Data.Sqlite
```

Compilar / ejecutar / restaurar:

```bash
dotnet build
dotnet run
dotnet restore
```

Ejecutar el sitio web localmente:

```bash
python -m http.server 8000
# abrir http://localhost:8000
```

---

## Convención de nombres

Usar nombres claros y ordenados:

```txt
semana-01-introduccion-curso-dotnet
semana-02-fundamentos-csharp
semana-03-control-flujo-colecciones
...
semana-14-crud-capas
semana-16-cierre-retroalimentacion
```

Los archivos principales se llaman:

```txt
semana-XX.md
README.md
html/slides.html
ejemplo-guiado/
ejercicios/ejercicios.md (básico + intermedio + reto en un solo archivo)
dudas/dudas.md
```

Excepciones históricas (NO renombrar): dentro de `semana-02-fundamentos-csharp` conviven `clase-01.md` (ya dictada, intocable) con sus materiales parte-2 (`parte-2-*.md`, `ejemplo-parte2/`, `ejercicios-parte2/`, `html-parte2/`). La vista doc de esa semana apunta a `semana-02.md` (índice).

---

## Reglas para los ejemplos

Cada ejemplo debe:

* Compilar y ejecutar correctamente con `dotnet run` en Linux/Windows/macOS.
* Incluir su `.csproj` (sin depender de soluciones externas).
* No dejar carpetas `bin/`, `obj/` ni bases `.db` generadas commiteadas.
* Tener comentarios útiles, no excesivos.
* Mostrar primero lo simple y mejorar progresivamente.
* Evitar complejidad empresarial innecesaria.

En semanas de base de datos, probar siempre ejecutar dos veces para verificar persistencia.

---

## Reglas para ejercicios

Cada semana tiene ejercicios de tres niveles:

```txt
Nivel 1: básico
Nivel 2: intermedio
Nivel 3: reto
```

Cada ejercicio incluye:

```txt
- Enunciado
- Requisitos
- Entrada esperada
- Salida esperada
- Criterios de evaluación (checkboxes)
```

---

## Evaluación

La evaluación es **100% por proyectos** (sin exámenes escritos):

```txt
P1 (Semana 5):  App de consola individual          25%
P2 (Semana 11): App de escritorio Avalonia equipos 30%
P3 (Semana 15): Proyecto integrador final equipos  45%

Nota Final = P1 × 0.25 + P2 × 0.30 + P3 × 0.45
```

Requisitos mínimos del P3 (integrador):

```txt
- Al menos 2 entidades relacionadas
- CRUD completo de las entidades principales
- Arquitectura por capas: Modelos / Datos (Repositories) / Vistas
- Todo valor de usuario viaja por parámetros SQL
- Navegación entre vistas con ContentControl
- Validaciones visuales y reglas de negocio separadas
- README profesional + video demo + sustentación individual
```

Política: proyecto que no compila → máximo 3.0 · copia → 0 · sustentación obligatoria por integrante.

---

## Sitio estático del curso

SPA sin build step. Archivos principales:

```txt
index.html
landing.css
landing.js
data.js
engine/
```

Convenciones del sitio:

* Hash routing: `#/clase-07/doc`, `#/clase-07/slides`
* Cada entrada de semana en `data.js` incluye campo `doc` con el nombre del markdown principal (normalmente `semana-XX.md`)
* Los slides viven en `html/slides.html` de cada semana, autocontenidos (array JS `const slides = [{title, content}]`)
* Sección de evaluación en el landing lista P1/P2/P3 con enlaces a sus enunciados (`navigateToProjectDoc`)
* Estética oscura estilo Tokio Night (ver DESIGN.md)

Al crear o mover semanas, actualizar SIEMPRE `data.js` (UNITS con dirs reales) y verificar que `landing.js` resuelva las rutas.

---

## Filosofía del curso

Este curso enseña a construir software funcional con .NET.

La prioridad es:

```txt
entender → practicar → construir → documentar → presentar
```

No sacrificar comprensión por exceso de herramientas. El estudiante termina con un sistema completo (POO + Avalonia + SQLite) publicable como portafolio.
