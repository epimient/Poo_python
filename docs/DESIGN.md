# Design.md — Technical Design System

## 1. Arquitectura de archivos

```
index.html        → Skeleton (59 líneas, 3 vistas ocultas por display:none)
landing.css       → Todos los estilos del SPA (314 líneas)
landing.js        → SPA logic (routing, renderizado, sidebar, navegación)
data.js           → Datos UNITS + PROJECTS + EXERCISES + RESOURCES (constantes, no lógica)
engine/
  slides.css      → Estilos del deck de slides (437 líneas)
  slides.js       → Navegación slides (flechas, swipe, teclado)
```

No hay build step. CSS plano, sin preprocesadores. JS vanilla sin frameworks.

Contenido del curso: 16 semanas en 3 unidades (`unidad-01-fundamentos-csharp/`, `unidad-02-poo-avalonia/`, `unidad-03-datos-proyecto-integrador/`) + 3 proyectos evaluables (P1/P2/P3). Material anterior archivado en `_archivo/`.

---

## 2. Sistema de color — Tokio Nights

### Variables CSS globales (en `:root`)

```css
--bg-base:    #1a1b2e;   /* fondo principal */
--bg-panel:   #24283b;   /* tarjetas, paneles, slides */
--bg-hover:   #2f3346;   /* hover states */
--text:       #c0caf5;   /* texto principal */
--text-muted: #565f89;   /* texto secundario, breadcrumbs */
--cyan:       #7dcfff;   /* acentos primarios, links, badges */
--blue:       #7aa2f7;   /* headers nivel 3, slides variant */
--purple:     #9d7cd8;   /* headers nivel 4, eyebrows */
--green:      #9ece6a;   /* callout success, Unidad 4 */
--orange:     #ff9e64;   /* inline code blocks, callout warning */
--red:        #f7768e;   /* errores, callout error */
--yellow:     #e0af68;   /* folder icons */
--border:     #3b4261;   /* bordes de paneles, separadores */
--code-bg:    #1f2335;   /* fondo de bloques de código */
```

### Asignación por Unidad

Cada unidad (`u1`–`u3`) tiene un color de acento:

| Unidad | Clase CSS | Color | Uso |
|--------|-----------|-------|-----|
| 1 — Fundamentos C# | `.u1` | `--cyan` | Badge, header line, numbering |
| 2 — POO e Interfaces | `.u2` | `--blue` | Badge, header line, numbering |
| 3 — Datos e Integración | `.u3` | `--purple` | Badge, header line, numbering |

El selector `.u4` (`--green`) permanece en `landing.css` pero sin uso: las semanas de cierre y proyectos heredan el color de su unidad.

Implementado con selectores por clase de unidad en `landing.css:85-88` y `153-156`.

Badges de evaluación: `.eval-badge--n1/n2/n3` se reutilizan como **P1/P2/P3** (tabla de evaluación del landing y sidebar de Proyectos). `--n4` queda sin uso.

---

## 3. Tipografía

### Fuentes

```css
font-family: 'Inter', system-ui, -apple-system, sans-serif;   /* cuerpo */
font-family: 'JetBrains Mono', monospace;                      /* código, stats, números */
```

Cargadas via Google Fonts preconnect en `index.html`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
```

### Jerarquía tipográfica (markdown view)

| Elemento | Tamaño | Peso | Color |
|----------|--------|------|-------|
| h1 | 1.8rem | 700 | `#fff` |
| h2 | 1.3rem | 600 | `--cyan` |
| h3 | 1.05rem | 600 | `--blue` |
| h4 | 0.95rem | 600 | `--purple` |
| p | 0.92rem | 400 | `--text` |
| code inline | 0.82rem | — | `--orange` |
| pre code | 0.82rem | — | `--text` |

### Jerarquía tipográfica (slides)

| Elemento | Tamaño | Peso | Color |
|----------|--------|------|-------|
| h1 | 48px (→32→26) | — | `--text` |
| h2 | 36px (→26→22) | — | `--text` |
| h3 | 26px (→20) | — | `--cyan` |
| p/li | 20px (→17) | — | `--text` |
| pre | 16px (→14) | — | `--text` |
| eyebrow | 13px | 700 | `--purple` |

---

## 4. Layout y vistas

### SPA con 3 vistas

Renderizadas por `landing.js`, controladas via `display:none` ↔ `display:flex/block`:

```css
#landing-view  → block (por defecto)
#iframe-view   → flex   (slides HTML)
#markdown-view → flex   (documentos .md)
```

### Top bar (fijo, 52px)

```css
.topbar {
  height: 52px; min-height: 52px;
  background: rgba(26,27,46,.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255,255,255,.05);
}
```

Elementos: sidebar toggle, home button, brand, path indicator.

### Sidebar

- `width: 280px`, scroll propio
- Glassmorphism: `background: rgba(36,40,59,.35); backdrop-filter: blur(14px);`
- Colapsable: clase `.hidden` → `margin-left: -280px; opacity:0; pointer-events:none`
- En mobile (<768px): posición fixed, transición `left` en lugar de `margin-left`

### Árbol del sidebar

Structure: `tree-group` > `tree-unit` + `tree-item` (details/summary) > `tree-subs` (links)

- 3 unidades con sus semanas (16 en total)
- 5 sub-acciones por semana: Slides, Documento, Ejemplo guiado, Ejercicios, FAQ
- Item especial **Evaluacion** → scroll a `#eval-section`
- Grupo **Ejercicios Formativos** (N1, N2)
- Grupo **Proyectos** (P1, P2, P3) → `navigateToProjectDoc`

### Landing view (hero + cards + resources)

- `max-width: 1100px`, centrado
- Hero: badge + título + subtitle + meta + hero-stats (glassmorphism, inline-flex)
- Cards grid: `grid-template-columns: repeat(auto-fill, minmax(260px, 1fr))`
  - Variant `.c5`: `minmax(190px, 1fr)` (Unidad con 5+ clases)
  - Variant `.c2`: `minmax(280px, 1fr)` (Unidad con ≤2 clases)
- Resources grid: `repeat(auto-fill, minmax(200px, 1fr))`

---

## 5. Sistema de glassmorphism

Aplicado en: sidebar, cards, hero stats, toolbar, resources.

Patrón consistente:

```css
background: rgba(36, 40, 59, .35);   /* bg-panel con alpha variable */
backdrop-filter: blur(12px);          /* blur variable según contexto */
border: 1px solid rgba(255,255,255,.05..08);
```

| Componente | Alpha bg | Blur | Opacidad borde |
|------------|----------|------|----------------|
| Topbar | .85 | 12px | .05 |
| Sidebar | .35 | 14px | .05 |
| Cards | .40 | 12px | .06 |
| Hero stats | .45 | 16px | .06 |
| Toolbars | .70 | 8px | .05 |

---

## 6. Cards

Estado base:

```css
background: rgba(36,40,59,.4);
backdrop-filter: blur(12px);
border-radius: 14px;
border: 1px solid rgba(255,255,255,.06);
padding: 20px;
cursor: pointer;
transition: transform .2s, box-shadow .2s, border-color .2s;
```

Hover: `translateY(-3px); box-shadow: 0 10px 32px rgba(0,0,0,.35); border-color: rgba(255,255,255,.12)`

Contenido: número (2rem, acento unidad), título (1rem, 600, #fff), descripción (.82rem, text-muted), tags (flex wrap, pill style).

---

## 7. Sistema de slides

### Estructura HTML

```html
<div class="deck">
  <div class="slide slide--title is-active" data-slide>
    <p class="eyebrow">...</p>
    <h1>...</h1>
    <p class="subtitle">...</p>
    <p class="author">...</p>
  </div>
  ...más slides...
</div>
<div class="controls">
  <button id="prev">◀</button>
  <span id="counter">1 / N</span>
  <div id="dots">...</div>
  <button id="next">▶</button>
</div>
```

### Navegación (slides.js)

- Botones prev/next
- Teclado: `ArrowLeft` / `ArrowRight` + `Space`
- Touch: swipe horizontal (>50px delta)
- Dots click
- Transición: `fadeIn` 0.25s (opacity + translateY)

### Variantes de slide

| Clase | Color borde | Fondo | Uso |
|-------|-------------|-------|-----|
| `.slide--title` | `--blue` | gradient `#1f2335`→`#24283b` | Portada |
| `.slide` (default) | `--border` | `--bg-panel` | Contenido |

### Componentes de slide

| Componente | Clase CSS | Color |
|------------|-----------|-------|
| Eyebrow | `.eyebrow` | `--purple` (title: `--cyan`) |
| Subtítulo | `.subtitle` | `--text-muted` |
| Author | `.author` | `--text-muted` + `--border` top |
| Inline code | `code` | `--orange` sobre `--code-bg` |
| Code blocks | `pre` | `border-left: 3px solid --blue` |
| Flow items | `.flow-item` | `--cyan` |
| Comparison der | `.comparison div:last-child` | `--green` bg |
| Comparison izq | `.comparison div:first-child` | `--red` bg |
| Callouts | `.callout--info/ok/warn/err` | `--blue/green/orange/red` left border |

### Botonera de navegación (controls)

Posición fixed, centrada abajo, glassmorphism bg-panel con `box-shadow: 0 4px 16px rgba(0,0,0,.3)`. Dots de `8px` con `--cyan` activo.

---

## 8. Markdown rendering

### Proceso (landing.js)

```javascript
1. fetch(url) → md text
2. Regex: :::tipo → <div class="callout callout--tipo">
3. Regex: [!tipo] → <div class="callout callout--tipo">
4. marked.parse(html, {breaks:true, gfm:true})
5. hljs.highlightElement() en cada <pre><code>
```

### Callouts (markdown view)

```css
.callout--info    → border-left var(--blue),   bg rgba(122,162,247,.08)
.callout--success → border-left var(--green),  bg rgba(158,206,106,.08)
.callout--warning → border-left var(--orange), bg rgba(255,158,100,.08)
.callout--error   → border-left var(--red),    bg rgba(247,118,142,.08)
```

### Comparison blocks (markdown view)

`grid-template-columns: 1fr 1fr`, con padding 12-16px, bordes `rgba(255,255,255,.06)`, bg `rgba(255,255,255,.03)`.

---

## 9. Hash routing

### Formato

```
#/clase-07/doc
#/clase-04/slides
#/ejercicio-01
#/proyecto-p1        (también #/proyecto → abre P3)
```

### Parseo (landing.js)

```javascript
location.hash.match(/^#\/clase-(\d+)\/(\w+)$/)
location.hash.match(/^#\/ejercicio-(\d+)$/)
location.hash.match(/^#\/proyecto-(p\d+)$/)
```

### Navegación

- `navigateTo(clsNum, action)` → actualiza hash con `history.replaceState`, carga vista, highlight en sidebar, push a `navStack`
- `navigateToExercise(id)` → carga `EXERCISES[i].dir/README.md`
- `navigateToProjectDoc(id)` → carga `{PROJECTS[i].dir}/{PROJECTS[i].doc}` (enunciados P1/P2/P3)
- `showLanding()` → limpia `navStack`, restaura hash a `.`
- `hashchange` event → resetea `navStack`, navega desde hash
- Initial hash restore en carga inicial

### Sub-acciones por clase

| action | pathFor | Vista |
|--------|---------|-------|
| `slides` | `{dir}/html/slides.html` | slides nativos — se extrae el array `slides = [{title, content}]` del deck y se renderiza dentro del SPA (sin iframe), con navegación prev/next y flechas del teclado |
| `doc` | `{dir}/{classData.doc}` — campo por semana en data.js, normalmente `semana-XX.md` | markdown |
| `example` | `{dir}/ejemplo-guiado/README.md` | markdown |
| `exercises` | `{dir}/ejercicios/ejercicios.md` (básico + intermedio + reto en un solo archivo; fallback: `ejercicio-01-basico.md` si no existe) | markdown |
| `faq` | `{dir}/dudas/dudas.md` | markdown |

---

## 10. Estados de UI

| Estado | Implementación |
|--------|---------------|
| Sidebar oculta | `.hidden` class toggle |
| Sidebar highlight | `.active` en `tree-subs a` |
| Slide activo | `.is-active` en `.slide` |
| Botón disabled | Atributo `disabled` en controls |
| Landing oculta | `display:none` |
| Vista activa | `.show` en `#iframe-view` / `#markdown-view` |
| Nav stack vacío | `homeBtn.disabled = true` |
| Dots activos | `.is-active` en `.dot` |

---

## 11. Responsive breakpoints

| Breakpoint | Cambios |
|------------|---------|
| ≤768px | Sidebar fixed (left), cards→1col, hero-stats wrap, padding reducido |
| ≤780px (slides) | Slide padding reducido, h1→32px, h2→26px, flows→2col, comparisons→1col |
| ≤480px (slides) | h1→26px, flows→1col |

---

## 12. Animaciones y transiciones

| Componente | Propiedad | Duración | Timing |
|------------|-----------|----------|--------|
| Card hover | transform, box-shadow, border-color | .2s | ease |
| Sidebar toggle | margin-left, opacity | .3s | ease |
| Slide fadeIn | opacity, translateY | .25s | ease |
| Tree item hover | background | .15s | — |
| Links hover | color | .2s | — |
| Button hover | background, border-color | .2s | — |
| Dot active | background | .2s | — |
| Scrollbar | (none, always visible on hover) | — | — |

---

## 13. Scrollbar personalizado

```css
.sidebar::-webkit-scrollbar, .main::-webkit-scrollbar { width: 6px }
.sidebar::-webkit-scrollbar-track, .main::-webkit-scrollbar-track { background: transparent }
.sidebar::-webkit-scrollbar-thumb, .main::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px }
```

Solo WebKit. Sin personalización Firefox.

---

## 14. Dependencias externas (CDN)

| Recurso | CDN | Propósito |
|---------|-----|-----------|
| marked.js | cdn.jsdelivr.net/npm/marked | Markdown → HTML |
| highlight.js | cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0 | Syntax highlighting |
| atom-one-dark theme | (mismo CDN) | Tema highlight |
| Inter font | Google Fonts | Tipografía cuerpo |
| JetBrains Mono | Google Fonts | Tipografía código |
