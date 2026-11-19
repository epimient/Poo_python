# Curso de Programación con .NET

16 semanas - 3 unidades - C# - POO - Avalonia UI - ADO.NET - SQLite

## Descripcion

Curso practico de programacion con .NET. Desde fundamentos de C# hasta construir un sistema de escritorio completo con interfaces graficas (Avalonia UI), Programacion Orientada a Objetos y acceso a datos con ADO.NET y SQLite. Enfoque en resolucion de problemas reales.

Cada semana incluye: teoria en markdown, slides navegables, ejemplo guiado funcional, ejercicios por niveles y seccion de dudas frecuentes.

## Evaluacion — 100% por proyectos

| Proyecto | Unidad | Peso | Que | Cuando |
|---|---|---|---|---|
| P1 | Fundamentos | 25% | App de consola individual | Semana 5 |
| P2 | POO + Avalonia | 30% | App de escritorio grupal | Semana 11 |
| P3 | Datos + Integracion | 45% | Proyecto integrador final | Semana 15 |

**Formula:** Nota Final = P1 x 0.25 + P2 x 0.30 + P3 x 0.45

No hay examenes escritos: cada unidad se cierra construyendo software.

## Calendario — 10 ago al 25 nov

| Semana | Fechas | Tema |
|---|---|---|
| 1 | 10-16 ago | Introduccion al curso y plataforma .NET |
| 2 | 17-23 ago | Fundamentos del lenguaje C# |
| 3 | 24-30 ago | Control de flujo y colecciones |
| 4 | 31 ago-6 sep | Metodos, modularidad y manejo de excepciones |
| 5 | 7-13 sep | **Evaluacion Unidad 1 — Proyecto P1** |
| 6 | 14-20 sep | Introduccion a la POO |
| 7 | 21-27 sep | Encapsulamiento y relaciones entre clases |
| 8 | 28 sep-4 oct | Herencia, interfaces y polimorfismo |
| 9 | 5-11 oct | Introduccion a Avalonia UI |
| 10 | 12-18 oct | Eventos, validacion y navegacion con Avalonia |
| 11 | 19-25 oct | **Evaluacion Unidad 2 — Proyecto P2** |
| 12 | 26 oct-1 nov | Fundamentos de acceso a datos con ADO.NET |
| 13 | 2-8 nov | Comandos y recuperacion de informacion |
| 14 | 9-15 nov | Operaciones CRUD y organizacion por capas |
| 15 | 16-22 nov | **Proyecto Integrador Final — P3** |
| 16 | 23-25 nov | Retroalimentacion y cierre del curso |

## Unidades

| Unidad | Semanas | Contenido | Producto |
|---|---|---|---|
| 1 — Fundamentos C# | 1-5 | .NET, SDK, CLI, variables, tipos, operadores, condicionales, ciclos, colecciones, metodos, excepciones | App de consola (P1) |
| 2 — POO e Interfaces Graficas | 6-11 | Clases, objetos, constructores, encapsulamiento, herencia, polimorfismo, interfaces, Avalonia UI, eventos, validacion, navegacion | App de escritorio (P2) |
| 3 — Datos e Integracion | 12-16 | ADO.NET, SQLite, comandos, DataReader, parametros SQL, CRUD, arquitectura por capas | Sistema integrador completo (P3) |

## Proyectos evaluables

**P1 (individual) — App de consola:** resuelve una problematica real aplicando logica, metodos, colecciones y manejo de errores.

**P2 (equipos 2-3) — App de escritorio:** sistema con al menos 3 clases relacionadas, formularios validados y navegacion, construido con POO + Avalonia UI.

**P3 (equipos 2-3) — Proyecto Integrador:** el mismo nivel de calidad llevado a produccion academica: 2 entidades relacionadas con CRUD completo, SQLite via ADO.NET, arquitectura por capas (Modelos / Datos / Vistas) y sustentacion individual.

Problematicas sugeridas para P2/P3: biblioteca, agenda medica, inventario comercial, gimnasio, veterinaria, restaurante.

## Stack tecnologico

| Tecnologia | Version | Uso |
|---|---|---|
| .NET SDK | 8 LTS | Plataforma de desarrollo |
| C# | 12 | Lenguaje de programacion |
| Avalonia UI | 11.x | Interfaces graficas multiplataforma |
| Microsoft.Data.Sqlite / ADO.NET | 9.x | Acceso a datos |
| SQLite | — | Base de datos embebida |
| Visual Studio Code | — | Editor de codigo |
| Git + GitHub | — | Control de versiones |

## Repositorios del curso

| Repositorio | Contenido |
|---|---|
| **Este repositorio** | 16 semanas con slides, ejemplos, ejercicios internos y sitio web SPA |
| **ejercicios-formativos** | Ejercicios formativos de practica (solo enunciados) |
| **curso-proyecto-grupoX** | Cada grupo crea su propio repositorio para P2 y P3 |

## Estructura del repositorio

```
/
├── unidad-01-fundamentos-csharp/          (semanas 1-5)
│   ├── semana-01-introduccion-curso-dotnet/
│   ├── semana-02-fundamentos-csharp/
│   ├── semana-03-control-flujo-colecciones/
│   ├── semana-04-metodos-modularidad-excepciones/
│   └── proyecto-unidad-01/
├── unidad-02-poo-avalonia/                (semanas 6-11)
│   ├── semana-06-intro-poo/
│   ├── semana-07-encapsulamiento-relaciones/
│   ├── semana-08-herencia-interfaces-polimorfismo/
│   ├── semana-09-intro-avalonia-ui/
│   ├── semana-10-eventos-validacion-navegacion/
│   └── proyecto-unidad-02/
├── unidad-03-datos-proyecto-integrador/   (semanas 12-16)
│   ├── semana-12-adonet-fundamentos/
│   ├── semana-13-comandos-recuperacion/
│   ├── semana-14-crud-capas/
│   ├── proyecto-integrador-unidad-03/
│   └── semana-16-cierre-retroalimentacion/
├── ejercicios-formativos/                  (ejercicios formativos)
├── _archivo/                              (material de versiones anteriores)
├── engine/                                (motor de slides)
├── index.html                             (sitio web SPA)
├── landing.css                            (estilos del sitio web)
├── landing.js                             (logica del sitio web)
├── data.js                                (datos del curso)
├── AGENTS.md                              (guia del curso para IA)
├── DESIGN.md                              (sistema de diseno visual)
└── README.md                              (este archivo)
```

Cada semana sigue esta estructura:

```
semana-XX-nombre/
├── semana-XX.md               (teoria completa)
├── html/slides.html           (presentacion navegable)
├── ejemplo-guiado/            (codigo de ejemplo funcional)
├── ejercicios/                (3 niveles: basico, intermedio, reto)
├── dudas/dudas.md             (preguntas frecuentes)
└── README.md                  (guia rapida de la semana)
```

## Como navegar el curso

**Opcion 1 — Sitio web SPA (recomendado):**

```bash
python -m http.server 8000
```

Abrir `http://localhost:8000`. Navega entre semanas y acciones (doc, slides, example, exercises, faq) con hash routing.

**Opcion 2 — Leer los markdowns:** cada semana tiene su `semana-XX.md`.

**Opcion 3 — Slides:** cada semana tiene `html/slides.html` navegable por teclado y touch.

## Requisitos de instalacion

```bash
# Verificar que .NET SDK este instalado
dotnet --version

# Instalar plantillas de Avalonia (para las semanas 9-11)
dotnet new install Avalonia.Templates

# Clonar el repositorio
git clone https://github.com/epimient/Profundizaci-n_en_NET.git
cd "Profundizaci-n_en_NET"
```

Todo el curso se desarrolla igual en Linux, Windows y macOS.

## Politica de entregas

- Los proyectos se entregan en las fechas del calendario (avance obligatorio + entrega final)
- Proyecto que no compila con `dotnet build`: nota maxima 3.0
- Trabajos copiados entre companeros: 0 automatico
- Sustentacion obligatoria: cada integrante debe explicar cualquier parte del codigo

## Licencia

Uso educativo. Proyecto de aprendizaje.
