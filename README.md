# Programación Orientada a Objetos con Python

**16 semanas · 3 unidades · 3 proyectos · Python 3.12 · Tkinter · Git**

---

## Descripción

Curso práctico de Programación Orientada a Objetos con Python. Empieza con clases, objetos y encapsulamiento, continúa con relaciones, herencia, clases abstractas y polimorfismo, y termina construyendo aplicaciones de escritorio con Tkinter, eventos y persistencia.

La temática del curso está centrada en **videojuegos**: personajes, equipos, inventarios, combates por turnos y un arcade final. También se incluyen ejemplos y ejercicios de **banca** para mostrar que los mismos principios se aplican a cualquier dominio.

Cada semana incluye teoría en Markdown, slides navegables, un ejemplo guiado ejecutable, ejercicios por niveles y preguntas frecuentes.

---

## Evaluación — 100% por proyectos

| Proyecto | Unidad | Peso | Qué | Semana |
|---|---|---|---|---|
| **P1** | Fundamentos de POO | 25% | Creador de personajes RPG (consola, individual) | 5 |
| **P2** | Relaciones y polimorfismo | 30% | Arcade de combate por turnos (consola, equipos 2–3) | 11 |
| **P3** | GUI e integración | 45% | Arcade con interfaz gráfica (escritorio, equipos 2–3) | 15 |

**Fórmula:** `Nota final = P1 × 0.25 + P2 × 0.30 + P3 × 0.45`

No hay exámenes escritos: cada unidad se cierra construyendo software y sustentándolo.

Dentro de cada proyecto, sus dos criterios del planeador pesan 50/50:

| Proyecto | Criterios | Peso interno |
|---|---|---|
| P1 | CE1.1 + CE1.2 | 50% / 50% |
| P2 | CE2.1 + CE2.2 | 50% / 50% |
| P3 | CE3.1 + CE3.2 | 50% / 50% |

Los descriptores de desempeño de cada criterio están en el enunciado de cada proyecto.

---

## Calendario de 16 semanas

| Semana | Tema | Producto |
|---|---|---|
| 1 | Introducción al curso y a Python | Primer objeto |
| 2 | Metodologías y paradigmas | Refactor procedural → POO |
| 3 | Clases, objetos y atributos | Party de personajes |
| 4 | Métodos, constructores y encapsulamiento | Combate y cuenta bancaria |
| 5 | **Evaluación 1 — P1** | Creador de personajes RPG |
| 6 | Relaciones entre clases | Equipo y jugadores |
| 7 | Agregación y composición | Inventario y tienda |
| 8 | Herencia | Guerrero, mago y arquero |
| 9 | Clases abstractas | Contratos y `Protocol` |
| 10 | Polimorfismo | Arcade de duelo por turnos |
| 11 | **Evaluación 2 — P2** | Arcade de combate |
| 12 | Arquitectura de GUI | Ventana y layouts |
| 13 | Componentes y organización visual | Formularios validados |
| 14 | Eventos e integración de una app OO | Arena Tkinter + JSON |
| 15 | **Evaluación 3 — P3** | Arcade con interfaz gráfica |
| 16 | Retroalimentación y cierre | Portafolio y sustentación |

---

## Unidades

| Unidad | Semanas | Contenido | Producto |
|---|---|---|---|
| **1 — Fundamentos de POO** | 1–5 | Python, paradigmas, clases, objetos, atributos, métodos, constructores, encapsulamiento | App de consola (P1) |
| **2 — Relaciones y polimorfismo** | 6–11 | Asociación, agregación, composición, herencia, clases abstractas, `Protocol`, polimorfismo | Arcade de consola (P2) |
| **3 — GUI e integración** | 12–16 | Tkinter, ttk, layouts, formularios, eventos, MVC, JSON, integración con POO | App de escritorio (P3) |

### Trazabilidad con el planeador

| Resultado de aprendizaje | Criterios | Proyecto |
|---|---|---|
| **RA1** — Construye clases y objetos con atributos, métodos, constructores y encapsulamiento | CE1.1, CE1.2 | P1 |
| **RA2** — Implementa soluciones con relaciones, herencia, abstractas, interfaces y polimorfismo | CE2.1, CE2.2 | P2 |
| **RA3** — Desarrolla una interfaz gráfica funcional integrada con POO | CE3.1, CE3.2 | P3 |

---

## Stack tecnológico

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.12+ | Lenguaje del curso |
| Visual Studio Code | — | Editor recomendado |
| Tkinter + ttk | stdlib | Interfaces gráficas |
| JSON | stdlib | Persistencia |
| `sqlite3` | stdlib | Extensión opcional en la unidad 3 |
| Git + GitHub | — | Control de versiones y portafolio |
| EVA / LMS | — | Entregas y comunicación |

Sin dependencias externas obligatorias: todo funciona con la biblioteca estándar.

---

## Estructura del repositorio

```text
/
├── index.html                 SPA del curso
├── landing.css                estilos Tokio Nights
├── landing.js                 routing, markdown y slides
├── data.js                    unidades, semanas, proyectos y recursos
├── engine/
│   ├── slides.css             estilos de presentaciones
│   └── slides.js              navegación de slides
├── unidad-01-fundamentos-poo/
│   ├── semana-01-introduccion-curso-python/
│   ├── semana-02-metodologias-paradigmas/
│   ├── semana-03-clases-objetos-atributos/
│   ├── semana-04-metodos-constructores-encapsulamiento/
│   └── proyecto-unidad-01/
├── unidad-02-relaciones-herencia-polimorfismo/
│   ├── semana-06-relaciones-clases/
│   ├── semana-07-agregacion-composicion/
│   ├── semana-08-herencia/
│   ├── semana-09-clases-abstractas/
│   ├── semana-10-polimorfismo/
│   └── proyecto-unidad-02/
├── unidad-03-gui-integracion/
│   ├── semana-12-arquitectura-gui/
│   ├── semana-13-componentes-organizacion-visual/
│   ├── semana-14-eventos-integracion-oo/
│   ├── semana-16-cierre-retroalimentacion/
│   └── proyecto-integrador-unidad-03/
├── ejercicios-formativos/
│   ├── unidad-01.md
│   ├── unidad-02.md
│   └── unidad-03.md
├── docs/                      material de referencia del planeador
├── README.md
├── DESIGN.md
└── AGENTS.md
```

Cada semana sigue esta estructura:

```text
semana-XX-nombre/
├── semana-XX.md               teoría completa
├── html/slides.html           presentación navegable
├── ejemplo-guiado/            código Python ejecutable
├── ejercicios/ejercicios.md   básico, intermedio y reto
├── dudas/dudas.md             preguntas frecuentes
└── README.md                  guía rápida
```

---

## Cómo navegar el curso

### Opción 1 — Sitio web SPA (recomendado)

```bash
python3 -m http.server 8000
```

Abre `http://localhost:8000`. Navega entre semanas y acciones (documento, slides, ejemplo, ejercicios, FAQ) con routing por hash.

### Opción 2 — Leer los Markdown

Cada semana tiene su `semana-XX.md`. Puedes abrirlo con VS Code o cualquier visor de Markdown.

### Opción 3 — Slides

Cada semana tiene `html/slides.html`, navegable con teclado (← →), botones y swipe en móvil.

---

## Requisitos de instalación

```bash
# Verificar Python
python3 --version        # 3.12 o superior

# Verificar Tkinter (incluido en la mayoría de instalaciones)
python3 -c "import tkinter; print(tkinter.TkVersion)"

# Crear y activar entorno virtual (opcional pero recomendado)
python3 -m venv .venv
source .venv/bin/activate      # Linux / macOS
# .venv\Scripts\activate       # Windows

# Verificar Git
git --version

# Clonar el repositorio
git clone <url-del-repositorio>
cd POO_PYTHON
```

En Linux, si Tkinter no está instalado:

```bash
sudo apt install python3-tk
```

Todo el curso se desarrolla igual en Linux, Windows y macOS.

---

## Proyectos evaluables

### P1 — Creador de personajes RPG (individual, 25%)

Aplicación de consola para crear y gestionar personajes con atributos encapsulados, properties, validaciones y menú interactivo.

### P2 — Arcade de combate por turnos (equipos 2–3, 30%)

Videojuego de consola donde guerrero, mago y arquero se enfrentan por turnos. Exige clase abstracta, tres subclases, agregación/composición, `Protocol` y un motor de combate polimórfico.

### P3 — Arcade con interfaz gráfica (equipos 2–3, 45%)

Aplicación de escritorio con Tkinter: CRUD de dos entidades relacionadas, vistas, eventos, validaciones, persistencia JSON y arquitectura por capas. Alternativa de banca: clientes, cuentas y transacciones.

---

## Política de entregas

- Los proyectos se entregan en la fecha indicada; hay revisión de avance y entrega final.
- Un proyecto que no ejecuta con `python3` obtiene como máximo **3.0**.
- Trabajos copiados entre compañeros o equipos: **0 automático**.
- La sustentación es obligatoria: cada integrante debe explicar cualquier parte del código.

---

## Licencia

Uso educativo. Proyecto de aprendizaje.
