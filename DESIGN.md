# DESIGN.md — Sistema de diseño y arquitectura del sitio

Documento técnico del sitio estático del curso **Programación Orientada a Objetos con Python**. No hay build step: HTML, CSS y JavaScript planos.

---

## 1. Arquitectura de archivos

```text
index.html        → esqueleto con 3 vistas y topbar
landing.css       → todos los estilos del SPA
landing.js        → routing, render de landing, markdown y slides
data.js           → COURSE, UNITS, PROJECTS, FORMATIVE, CRITERIA, RESOURCES
engine/
  slides.css      → estilos de presentaciones autocontenidas
  slides.js       → navegación de slides standalone
```

Contenido: 16 semanas en 3 unidades, 3 proyectos evaluables, 3 archivos de ejercicios formativos y material de referencia en `docs/`.

---

## 2. Sistema de color — Tokio Nights

Variables globales en `:root` de `landing.css`:

```css
--bg-base:    #1a1b2e;
--bg-panel:   #24283b;
--bg-hover:   #2f3346;
--text:       #c0caf5;
--text-strong:#ffffff;
--text-muted: #565f89;
--cyan:       #7dcfff;
--blue:       #7aa2f7;
--purple:     #9d7cd8;
--green:      #9ece6a;
--orange:     #ff9e64;
--red:        #f7768e;
--yellow:     #e0af68;
--border:     #3b4261;
--code-bg:    #1f2335;
```

### Asignación por unidad

| Unidad | Clase | Color | Uso |
|---|---|---|---|
| 1 — Fundamentos de POO | `.u1` | `--cyan` | Badge, tarjeta, nodo del calendario |
| 2 — Relaciones y polimorfismo | `.u2` | `--blue` | Badge, tarjeta, nodo del calendario |
| 3 — GUI e integración | `.u3` | `--purple` | Badge, tarjeta, nodo del calendario |

Los badges de evaluación usan naranja (`--orange`) para los proyectos y rojo (`--red`) para semanas de cierre/evaluación.

El fondo combina dos gradientes radiales sutiles (azul y violeta) sobre `--bg-base`.

---

## 3. Tipografía

```css
font-family: 'Inter', system-ui, -apple-system, sans-serif;   /* cuerpo */
font-family: 'JetBrains Mono', monospace;                      /* código, números */
```

Cargadas desde Google Fonts en `index.html` (`Inter` 400–800 y `JetBrains Mono` 400–700).

### Jerarquía en documentos Markdown

| Elemento | Tamaño | Peso | Color |
|---|---|---|---|
| h1 | 1.9rem | 800 | `--text-strong` |
| h2 | 1.28rem | 700 | `--cyan` |
| h3 | 1.03rem | 700 | `--blue` |
| h4 | .9rem | 700 | `--purple` |
| p | .9rem | 400 | `--text` |
| code inline | .8em | — | `--orange` |
| pre code | .78rem | — | `--text` |

### Jerarquía en slides

| Elemento | Tamaño | Color |
|---|---|---|
| h1 | 2.55rem (móvil: 1.85/1.6) | `--text-strong` |
| h2 | 1.95rem (móvil: 1.45/1.3) | `--text-strong` |
| h3 | 1.25rem | `--cyan` |
| p / li | .98rem | `--text` |
| pre | .78rem | `--text` |
| eyebrow | .68rem, 700 | `--purple` |

---

## 4. Layout y vistas

El SPA tiene tres vistas controladas por `landing.js`:

```css
#landing-view  → display: block (por defecto)
#markdown-view → display: flex con .show
#slides-view   → display: flex con .show
```

### Topbar (fijo, 56px)

```css
.topbar {
  position: fixed;
  height: 56px;
  background: rgba(26, 27, 46, .82);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(255, 255, 255, .05);
}
```

Elementos: toggle de sidebar, botón Inicio, marca, indicador de ruta.

### Sidebar

- Ancho: `292px`, scroll propio, posición fija.
- Glassmorphism: `rgba(36,40,59,.35)` + `blur(14px)`.
- Desktop: clase `.hidden` → `translateX(-100%)` y el main pasa a `margin-left: 0`.
- Mobile (<768px): oculto por defecto; clase `.open` lo desliza y aparece un overlay.
- Árbol: unidad → semanas (`details/summary`) → 5 acciones. Luego proyectos, ejercicios formativos y enlace a evaluación.

### Landing

- `max-width: 1120px`, centrado, padding 32px.
- Hero con badge, título, subtítulo, meta, 4 stats y CTA.
- Secciones: ruta (3 tarjetas de unidad), calendario (16 semanas), evaluación, proyectos, recursos, stack y footer.
- Grids: `repeat(auto-fit, minmax(...))` para tarjetas, calendario y recursos.

---

## 5. Glassmorphism

| Componente | Fondo | Blur | Borde |
|---|---|---|---|
| Topbar | `rgba(26,27,46,.82)` | 14px | `.05` |
| Sidebar | `rgba(36,40,59,.35)` | 14px | `.05` |
| Tarjetas de unidad | `rgba(36,40,59,.42)` | 12px | `.06` |
| Stats del hero | `rgba(36,40,59,.45)` | 16px | `.06` |
| Toolbar | `rgba(26,27,46,.82)` | 8px | `.05` |
| Controles de slides | `rgba(36,40,59,.9)` | 10px | `.09` |

---

## 6. Tarjetas

Base:

```css
background: rgba(36,40,59,.42);
backdrop-filter: blur(12px);
border-radius: 16px;
border: 1px solid rgba(255,255,255,.06);
```

Hover: `translateY(-3px)`, sombra `0 14px 34px rgba(0,0,0,.3)` y borde más visible.

Las tarjetas de unidad llevan una barra lateral de 3px con el color de la unidad (`::before`).

---

## 7. Slides

### Autocontenidas (`html/slides.html`)

Estructura:

```html
<main class="deck">
  <section class="slide slide--title is-active">...</section>
  <section class="slide">...</section>
  ...
</main>
<div class="controls">
  <button id="prev">◀</button>
  <span id="counter">1 / N</span>
  <div id="dots"></div>
  <button id="next">▶</button>
</div>
<script src="../../../engine/slides.js"></script>
```

`engine/slides.js`:

- Botones prev/next.
- Teclado: `ArrowLeft`, `ArrowRight`, `PageUp`, `PageDown`, `Home`, `End`, `Space`.
- Touch: swipe horizontal (>55px).
- Dots clicables.
- Transición `fadeIn` de .26s.

### Dentro del SPA

`landing.js` hace `fetch` del HTML, lo parsea con `DOMParser`, extrae todos los `.slide` y los inserta en `#slidesStage`. Luego reutiliza sus propios controles, dots y atajos de teclado. No usa iframe.

---

## 8. Render de Markdown

Proceso en `landing.js`:

1. `fetch(url)` del `.md`.
2. Preprocesar callouts.
3. `marked.parse()` con `gfm: true`.
4. `hljs.highlightElement()` en cada `pre code`.
5. Envolver tablas en un contenedor con scroll horizontal.
6. Abrir enlaces externos en pestaña nueva.

### Callouts

Sintaxis:

```md
:::info
Texto.
:::
```

Tipos: `info`, `success`, `warning`, `error`, `reto`.

| Tipo | Borde / acento |
|---|---|
| info | `--blue` |
| success | `--green` |
| warning | `--orange` |
| error | `--red` |
| reto | `--purple` |

También se acepta `[!warning]` al inicio de una línea.

### Comparaciones

Se puede usar HTML dentro del Markdown:

```html
<div class="comparison">
  <div>Procedural</div>
  <div>POO</div>
</div>
```

---

## 9. Hash routing

Formato:

```text
#/semana-01/doc
#/semana-10/slides
#/semana-14/example
#/proyecto-p1
#/formativo-u2
#/eval
```

Parseo:

```js
/^#\/semana-(\d+)\/(\w+)$/
/^#\/proyecto-(p\d+)$/
/^#\/formativo-(\w+)$/
```

Acciones por semana:

| Acción | Archivo |
|---|---|
| `doc` | `{dir}/{week.doc}` (`semana-XX.md`) |
| `slides` | `{dir}/html/slides.html` |
| `example` | `{dir}/ejemplo-guiado/README.md` |
| `exercises` | `{dir}/ejercicios/ejercicios.md` |
| `faq` | `{dir}/dudas/dudas.md` |

Proyectos: `{dir}/README.md`. Formativos: ruta directa del `.md`.

Al navegar se actualiza el hash, se marca el sidebar, se cambia el indicador de ruta y se hace scroll al inicio. `hashchange` vuelve a resolver la ruta, lo que permite atrás/adelante del navegador.

---

## 10. Estados de UI

| Estado | Implementación |
|---|---|
| Sidebar oculto (desktop) | `.hidden` |
| Sidebar abierto (mobile) | `.open` + overlay `.open` |
| Semana activa | `.active` en `summary` |
| Acción activa | `.active` en enlace del submenú |
| Vista activa | `.show` en `#markdown-view` / `#slides-view` |
| Slide activo | `.is-active` |
| Dot activo | `.is-active` |
| Botón deshabilitado | `disabled` |
| Landing visible | `#landing-view` con `display:block` |
| Carga / error | `.md-state` |
| Botón Inicio | `disabled` en landing |

---

## 11. Responsive

| Breakpoint | Cambios |
|---|---|
| ≤980px | Evaluación pasa a una columna |
| ≤768px | Sidebar fijo deslizante, grids a 1 columna, toolbar compacta, tipografía reducida, slides con menos padding, comparaciones a 1 columna |
| ≤480px | Marca sin texto, hero más pequeño, stats a ancho completo, slides compactos |
| prefers-reduced-motion | Animaciones y scroll suave desactivados |

---

## 12. Animaciones

| Componente | Propiedad | Duración |
|---|---|---|
| Tarjetas hover | transform, box-shadow, border | .2s |
| Sidebar | transform, opacity | .3s |
| Slide | opacity, translateY | .26–.28s |
| Enlaces / botones | background, color | .15–.2s |
| Dots | background, transform | .18s |

---

## 13. Datos (`data.js`)

```js
COURSE      // metadatos, descripción y stack
UNITS[]     // { id, num, title, short, color, desc, result, tags, weeks[] }
PROJECTS[]  // { id, num, unit, weight, title, desc, dir, doc, tags, modality, criteria }
FORMATIVE[] // { id, title, desc, dir, tag }
CRITERIA[]  // { code, unit, weight, label }
RESOURCES[] // { title, desc, url, label }
```

Cada semana dentro de `UNITS` incluye:

```js
{ num, dir, doc, title, desc, tags }
```

Regla: al crear o mover una semana hay que actualizar `data.js` y verificar que existan `dir`, `doc`, `html/slides.html`, `ejemplo-guiado/README.md`, `ejercicios/ejercicios.md` y `dudas/dudas.md`.

---

## 14. Dependencias externas (CDN)

| Recurso | CDN | Propósito |
|---|---|---|
| marked.js | jsDelivr | Markdown → HTML |
| highlight.js 11.9 | cdnjs | Resaltado de código |
| atom-one-dark | cdnjs | Tema de resaltado |
| Inter | Google Fonts | Tipografía de cuerpo |
| JetBrains Mono | Google Fonts | Tipografía de código |

No hay frameworks, bundler ni proceso de compilación. El sitio funciona con cualquier servidor estático.
