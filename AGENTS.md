# AGENTS.md — Curso de Programación Orientada a Objetos con Python

## Naturaleza

Este repositorio es un **curso práctico de 16 semanas de Programación Orientada a Objetos con Python**, no una aplicación única.

El curso está organizado en **3 unidades** y **semanas** autocontenidas. Cada semana incluye teoría, presentación, ejemplo ejecutable, ejercicios por niveles y preguntas frecuentes.

```text
unidad-01-fundamentos-poo/                 (semanas 1–5)
unidad-02-relaciones-herencia-polimorfismo/ (semanas 6–11)
unidad-03-gui-integracion/                 (semanas 12–16)
ejercicios-formativos/                     (refuerzo por unidad)
docs/                                      (planeador y referencias)
```

Cada semana:

```text
semana-XX-nombre/
├── semana-XX.md
├── README.md
├── html/slides.html
├── ejemplo-guiado/
├── ejercicios/ejercicios.md
└── dudas/dudas.md
```

Las semanas de evaluación son carpetas de proyecto:

```text
proyecto-unidad-01/            (semana 5)
proyecto-unidad-02/            (semana 11)
proyecto-integrador-unidad-03/ (semana 15)
```

---

## Enfoque pedagógico

El curso debe ser **altamente práctico**.

Prioridad:

```text
entender → practicar → construir → documentar → presentar
```

La temática principal es **videojuegos**: personajes, equipos, inventarios, combates por turnos, tiendas, partidas y un arcade final. La **banca** aparece como dominio secundario (cuentas, clientes, transacciones) para mostrar transferencia de conceptos.

El curso debe poder desarrollarse desde Linux, Windows y macOS.

Herramientas:

```text
Python 3.12+ · Visual Studio Code · Tkinter · Git + GitHub · EVA/LMS
```

---

## Duración y calendario

```text
16 semanas · 3 unidades · 3 proyectos
```

| Unidad | Semanas | Tema | Evaluación |
|---|---|---|---|
| 1 — Fundamentos de POO | 1–5 | Clases, objetos, atributos, métodos, constructores, encapsulamiento | P1 (25%) |
| 2 — Relaciones y polimorfismo | 6–11 | Asociación, agregación, composición, herencia, ABC, Protocol, polimorfismo | P2 (30%) |
| 3 — GUI e integración | 12–16 | Tkinter, ttk, layouts, formularios, eventos, MVC, JSON | P3 (45%) |

Calendario:

```text
S1:  Introducción al curso y a Python
S2:  Metodologías y paradigmas
S3:  Clases, objetos y atributos
S4:  Métodos, constructores y encapsulamiento
S5:  Evaluación 1 — P1
S6:  Relaciones entre clases
S7:  Agregación y composición
S8:  Herencia
S9:  Clases abstractas
S10: Polimorfismo
S11: Evaluación 2 — P2
S12: Arquitectura de GUI
S13: Componentes y organización visual
S14: Eventos e integración de una aplicación OO
S15: Evaluación 3 — P3
S16: Retroalimentación y cierre
```

---

## Stack principal

```text
Lenguaje: Python 3.12+
Editor: Visual Studio Code
UI: Tkinter + ttk (biblioteca estándar)
Persistencia: JSON (stdlib); sqlite3 opcional
Control de versiones: Git + GitHub
Entregas: EVA/LMS institucional
```

Sin dependencias externas obligatorias. No usar PyQt, CustomTkinter, Django, Flask, ORM ni frameworks en el material base.

---

## Comandos base

```bash
# Verificar Python
python3 --version

# Verificar Tkinter
python3 -c "import tkinter; print(tkinter.TkVersion)"

# Entorno virtual
python3 -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows

# Ejecutar un ejemplo
python3 ejemplo.py

# Comprobar sintaxis
python3 -m py_compile ejemplo.py

# Servir el sitio
python3 -m http.server 8000
# abrir http://localhost:8000

# Git
git status
git add .
git commit -m "mensaje"
```

---

## Convención de nombres

```text
semana-01-introduccion-curso-python
semana-02-metodologias-paradigmas
semana-03-clases-objetos-atributos
semana-04-metodos-constructores-encapsulamiento
semana-06-relaciones-clases
semana-07-agregacion-composicion
semana-08-herencia
semana-09-clases-abstractas
semana-10-polimorfismo
semana-12-arquitectura-gui
semana-13-componentes-organizacion-visual
semana-14-eventos-integracion-oo
semana-16-cierre-retroalimentacion
```

Archivos principales:

```text
semana-XX.md
README.md
html/slides.html
ejemplo-guiado/README.md + .py
ejercicios/ejercicios.md
dudas/dudas.md
```

No renombrar carpetas sin actualizar `data.js`.

---

## Reglas para los ejemplos

Cada ejemplo debe:

- Ejecutarse con `python3 archivo.py` en Linux, Windows y macOS.
- Usar solo la biblioteca estándar.
- Incluir un bloque `if __name__ == "__main__":` con un demo que no dependa de `input()` (o con datos simulados).
- Tener type hints simples, docstrings breves y comentarios útiles, no excesivos.
- Mostrar primero lo simple y mejorar progresivamente.
- Evitar complejidad empresarial innecesaria.
- En la unidad 3, abrir una ventana Tkinter real y funcionar sin dependencias externas.
- No dejar `__pycache__/`, `.venv/`, JSON generados ni archivos temporales versionados.

Antes de dar un ejemplo por terminado:

```bash
python3 -m py_compile ejemplo.py
python3 ejemplo.py
```

En ejemplos Tkinter, si no hay display:

```bash
python3 -m py_compile archivo.py
# y documentar que la verificación fue de sintaxis/importación
```

---

## Reglas para los ejercicios

Cada semana tiene tres niveles:

```text
Nivel 1: básico
Nivel 2: intermedio
Nivel 3: reto
```

Cada ejercicio incluye:

```text
- Enunciado
- Requisitos
- Entrada esperada
- Salida esperada
- Criterios de evaluación (checkboxes)
```

Los ejercicios deben ser resolubles con lo visto hasta esa semana. El reto de la semana 10 es obligatorio: **arcade de duelo por turnos 1 vs 1**, donde el jugador elige entre guerrero, mago y arquero, la máquina elige otro y combaten por turnos con un bucle polimórfico.

---

## Evaluación

```text
P1 (Semana 5):  Creador de personajes RPG (consola, individual)      25%
P2 (Semana 11): Arcade de combate por turnos (consola, equipos 2–3)  30%
P3 (Semana 15): Arcade con interfaz gráfica (equipos 2–3)            45%

Nota final = P1 × 0.25 + P2 × 0.30 + P3 × 0.45
```

Dentro de cada proyecto, sus dos criterios CE pesan 50/50:
P1 → CE1.1/CE1.2 · P2 → CE2.1/CE2.2 · P3 → CE3.1/CE3.2.

Requisitos mínimos del P3:

```text
- Al menos 2 entidades relacionadas
- CRUD completo
- Arquitectura por capas: modelos / datos / servicios / vistas
- Tkinter + ttk, sin dependencias externas
- Eventos con command y al menos un bind
- Validaciones visuales y reglas de negocio separadas
- Persistencia JSON tolerante a errores
- README profesional + video demo + sustentación individual
```

Política: proyecto que no ejecuta → máximo 3.0 · copia → 0 · sustentación obligatoria por integrante.

---

## Sitio estático del curso

SPA sin build step:

```text
index.html
landing.css
landing.js
data.js
engine/slides.css
engine/slides.js
```

Convenciones:

- Hash routing: `#/semana-07/doc`, `#/semana-07/slides`, `#/proyecto-p2`, `#/formativo-u1`.
- Cada entrada de semana en `data.js` incluye `dir`, `doc`, `title`, `desc` y `tags`.
- Los slides viven en `html/slides.html`, autocontenidos, con `../../../engine/slides.css` y `../../../engine/slides.js`.
- `landing.js` extrae los `.slide` del HTML y los renderiza dentro del SPA.
- Estética oscura Tokio Nights (ver `DESIGN.md`).
- Al crear o mover semanas, actualizar SIEMPRE `data.js` y verificar rutas.

Verificación del sitio:

```bash
python3 -m http.server 8000
# abrir http://localhost:8000 y recorrer las 16 semanas
```

---

## Redacción del contenido

- Español neutro con acentos.
- Teoría de 1.200–1.800 palabras por semana.
- 12–16 slides por semana.
- Callouts: `:::info`, `:::success`, `:::warning`, `:::error`, `:::reto`.
- Código Python 3.12 válido, sin APIs inventadas.
- No mencionar C#, .NET, Avalonia, ADO.NET ni SQLite como obligatorio.
- Cada semana debe indicar su mediación TIC: Python, VS Code, EVA/LMS, Git y repositorio de código.

---

## Filosofía del curso

El estudiante termina con tres proyectos de portafolio y una comprensión sólida de la POO aplicada. No sacrificar comprensión por exceso de herramientas.

```text
entender → practicar → construir → documentar → presentar
```
