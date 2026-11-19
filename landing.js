/* ============================================================
   landing.js — SPA del curso POO con Python
   Routing por hash, render de markdown y presentaciones.
   ============================================================ */

(function () {
  'use strict';

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  const els = {
    landing: $('#landing-view'),
    markdownView: $('#markdown-view'),
    slidesView: $('#slides-view'),
    mdBody: $('#mdBody'),
    mdTitle: $('#mdTitle'),
    mdBadge: $('#mdBadge'),
    mdRawBtn: $('#mdRawBtn'),
    slidesStage: $('#slidesStage'),
    slidesTitle: $('#slidesTitle'),
    slideCounter: $('#slideCounter'),
    slideDots: $('#slideDots'),
    slidePrev: $('#slidePrev'),
    slideNext: $('#slideNext'),
    slidesControls: $('#slidesControls'),
    slidesFullBtn: $('#slidesFullBtn'),
    sidebar: $('#sidebar'),
    sidebarTree: $('#sidebarTree'),
    sidebarToggle: $('#sidebarToggle'),
    sidebarOverlay: $('#sidebarOverlay'),
    homeBtn: $('#homeBtn'),
    brandBtn: $('#brandBtn'),
    pathIndicator: $('#pathIndicator')
  };

  marked.setOptions({ gfm: true, breaks: false });

  const state = {
    slides: [],
    slideIndex: 0,
    currentSlideSource: '',
    currentRawUrl: '',
    activeHash: ''
  };

  /* ------------------------------------------------------------
     Utilidades
     ------------------------------------------------------------ */
  const allWeeks = () => UNITS.flatMap(u => u.weeks.map(w => ({ ...w, unit: u })));
  const findWeek = num => allWeeks().find(w => w.num === Number(num));
  const findProject = id => PROJECTS.find(p => p.id === id);
  const findFormative = id => FORMATIVE.find(f => f.id === id);

  const unitById = id => UNITS.find(u => u.id === id);

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function pad(n) { return String(n).padStart(2, '0'); }

  function setPath(text) { els.pathIndicator.textContent = text; }

  function closeMobileSidebar() {
    els.sidebar.classList.remove('open');
    els.sidebarOverlay.classList.remove('open');
  }

  /* ------------------------------------------------------------
     Sidebar
     ------------------------------------------------------------ */
  function buildSidebar() {
    const parts = [];
    parts.push('<div class="tree-group"><a class="tree-link" data-home="1" href="#/"><span>⌂</span><span>Inicio del curso</span></a></div>');

    UNITS.forEach(unit => {
      parts.push(`
        <div class="tree-group">
          <button class="tree-unit ${unit.id}" data-unit-toggle="${unit.id}" aria-expanded="true">
            <span class="unit-num">${unit.num}</span>
            <span>${escapeHtml(unit.short)}</span>
            <span class="chev">▾</span>
          </button>
          <div class="tree-items" data-unit-items="${unit.id}">
      `);
      const project = PROJECTS.find(p => p.unit === unit.id);
      const entries = unit.weeks.map(week => ({ type: 'week', num: week.num, week }));
      if (project) entries.push({ type: 'project', num: project.num, project });
      entries.sort((a, b) => a.num - b.num);

      entries.forEach(entry => {
        if (entry.type === 'week') {
          const week = entry.week;
          parts.push(`
            <details class="tree-item" data-week-item="${week.num}">
              <summary><span class="week-num">${pad(week.num)}</span><span>${escapeHtml(week.title)}</span></summary>
              <div class="tree-subs">
                <a href="#/semana-${week.num}/doc" data-week="${week.num}" data-action="doc">Documento</a>
                <a href="#/semana-${week.num}/slides" data-week="${week.num}" data-action="slides">Slides</a>
                <a href="#/semana-${week.num}/example" data-week="${week.num}" data-action="example">Ejemplo guiado</a>
                <a href="#/semana-${week.num}/exercises" data-week="${week.num}" data-action="exercises">Ejercicios</a>
                <a href="#/semana-${week.num}/faq" data-week="${week.num}" data-action="faq">FAQ</a>
              </div>
            </details>
          `);
        } else {
          const p = entry.project;
          parts.push(`
            <a class="tree-link" href="#/proyecto-${p.id}" data-project="${p.id}">
              <span>${p.id.toUpperCase()} · ${escapeHtml(p.title.split('·')[1].trim())}</span>
              <span class="tag">${p.weight}%</span>
            </a>
          `);
        }
      });
      parts.push('</div></div>');
    });

    parts.push(`
      <div class="tree-group">
        <button class="tree-unit" data-unit-toggle="formativos" aria-expanded="true">
          <span class="unit-num">★</span><span>Ejercicios formativos</span><span class="chev">▾</span>
        </button>
        <div class="tree-items" data-unit-items="formativos">
          ${FORMATIVE.map(f => `<a class="tree-link" href="#/formativo-${f.id}" data-formative="${f.id}"><span>${escapeHtml(f.title)}</span><span class="tag">${f.tag}</span></a>`).join('')}
        </div>
      </div>
      <div class="tree-group">
        <a class="tree-link" href="#/eval" data-eval-link="1"><span>◎</span><span>Evaluación y rúbrica</span></a>
      </div>
    `);

    els.sidebarTree.innerHTML = parts.join('');

    $$('[data-unit-toggle]', els.sidebarTree).forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.unitToggle;
        const items = $(`[data-unit-items="${key}"]`, els.sidebarTree);
        const expanded = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!expanded));
        items.hidden = expanded;
      });
    });

    $$('.tree-item', els.sidebarTree).forEach(item => {
      item.addEventListener('toggle', () => {
        if (!item.open) return;
        $$('.tree-item', els.sidebarTree).forEach(other => {
          if (other !== item) other.open = false;
        });
      });
    });
  }

  function clearSidebarActive() {
    $$('.tree-subs a, .tree-link', els.sidebarTree).forEach(a => a.classList.remove('active'));
    $$('.tree-item summary', els.sidebarTree).forEach(s => s.classList.remove('active'));
  }

  function markSidebar(weekNum, action) {
    clearSidebarActive();
    if (!weekNum) return;
    const item = $(`[data-week-item="${weekNum}"]`, els.sidebarTree);
    if (item) {
      item.open = true;
      const summary = $('summary', item);
      if (summary) summary.classList.add('active');
    }
    if (action) {
      const link = $(`[data-week="${weekNum}"][data-action="${action}"]`, els.sidebarTree);
      if (link) link.classList.add('active');
    }
  }

  /* ------------------------------------------------------------
     Vistas
     ------------------------------------------------------------ */
  function showOnly(target) {
    els.landing.style.display = 'none';
    els.markdownView.classList.remove('show');
    els.slidesView.classList.remove('show');
    if (target === 'landing') {
      els.landing.style.display = 'block';
    } else if (target === 'markdown') {
      els.markdownView.classList.add('show');
    } else if (target === 'slides') {
      els.slidesView.classList.add('show');
    }
  }

  function showLanding(scrollTarget) {
    showOnly('landing');
    els.homeBtn.disabled = true;
    setPath('Inicio');
    clearSidebarActive();
    closeMobileSidebar();
    window.scrollTo({ top: 0, behavior: 'auto' });
    if (scrollTarget) {
      setTimeout(() => {
        const node = document.getElementById(scrollTarget);
        if (node) node.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 60);
    }
  }

  /* ------------------------------------------------------------
     Markdown
     ------------------------------------------------------------ */
  const ACTION_LABELS = {
    doc: 'Documento',
    example: 'Ejemplo guiado',
    exercises: 'Ejercicios',
    faq: 'Preguntas frecuentes'
  };

  function preprocessCallouts(md) {
    const labels = {
      info: 'Nota',
      success: 'Bien',
      warning: 'Ojo',
      error: 'Error',
      reto: 'Reto'
    };

    let out = md.replace(/^:::(\w+)[ \t]*\r?\n([\s\S]*?)^:::[ \t]*$/gm, (match, type, body) => {
      const safeType = labels[type] ? type : 'info';
      return `<div class="callout callout--${safeType}"><span class="callout-title">${labels[safeType]}</span>\n\n${body}\n\n</div>`;
    });

    out = out.replace(/^\[!(\w+)\][ \t]*(.*)$/gm, (match, type, text) => {
      const safeType = labels[type] ? type : 'info';
      return `<div class="callout callout--${safeType}"><span class="callout-title">${labels[safeType]}</span>\n\n${text}\n\n</div>`;
    });

    return out;
  }

  function renderMarkdown(md) {
    const html = marked.parse(preprocessCallouts(md));
    els.mdBody.innerHTML = html;

    $$('pre code', els.mdBody).forEach(block => {
      try { hljs.highlightElement(block); } catch (e) { /* noop */ }
    });

    $$('a', els.mdBody).forEach(a => {
      const href = a.getAttribute('href') || '';
      if (/^https?:\/\//i.test(href)) {
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
      }
    });

    $$('table', els.mdBody).forEach(table => {
      if (table.parentElement && table.parentElement.classList.contains('table-wrap')) return;
      const wrap = document.createElement('div');
      wrap.className = 'table-wrap';
      wrap.style.overflowX = 'auto';
      table.parentNode.insertBefore(wrap, table);
      wrap.appendChild(table);
    });
  }

  function showMarkdownState(kind, url, message) {
    const label = kind === 'error' ? 'No se pudo cargar el documento' : 'Cargando…';
    els.mdBody.innerHTML = `<div class="md-state"><strong>${label}</strong>${message ? escapeHtml(message) : ''}<br><code>${escapeHtml(url)}</code></div>`;
  }

  async function openMarkdown(url, options) {
    const { title, badge, rawUrl } = options;
    showOnly('markdown');
    els.mdTitle.textContent = title;
    els.mdBadge.textContent = badge;
    els.mdBody.innerHTML = '';
    showMarkdownState('loading', url);
    state.currentRawUrl = rawUrl || url;
    els.mdRawBtn.disabled = false;
    window.scrollTo({ top: 0, behavior: 'auto' });

    try {
      const res = await fetch(url, { cache: 'no-store' });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const md = await res.text();
      renderMarkdown(md);
    } catch (err) {
      showMarkdownState('error', url, err.message);
    }
  }

  async function openWeekWeek(week, action) {
    const unit = unitById(week.unit.id);
    markSidebar(week.num, action);
    setPath(`Unidad ${unit.num} · Semana ${pad(week.num)} · ${ACTION_LABELS[action] || action}`);

    if (action === 'slides') {
      openSlides(`${week.dir}/html/slides.html`, week.title);
      return;
    }

    let url;
    let badge = ACTION_LABELS[action] || action;
    let title = week.title;

    if (action === 'doc') url = `${week.dir}/${week.doc}`;
    else if (action === 'example') url = `${week.dir}/ejemplo-guiado/README.md`;
    else if (action === 'exercises') url = `${week.dir}/ejercicios/ejercicios.md`;
    else if (action === 'faq') url = `${week.dir}/dudas/dudas.md`;

    if (!url) { showLanding(); return; }
    await openMarkdown(url, { title, badge, rawUrl: url });
  }

  async function openProject(id) {
    const project = findProject(id);
    if (!project) { showLanding(); return; }
    clearSidebarActive();
    const link = $(`[data-project="${id}"]`, els.sidebarTree);
    if (link) link.classList.add('active');
    const unit = unitById(project.unit);
    setPath(`Unidad ${unit.num} · ${project.id.toUpperCase()} · Proyecto`);
    closeMobileSidebar();
    await openMarkdown(`${project.dir}/${project.doc}`, {
      title: project.title,
      badge: `Proyecto · ${project.weight}%`,
      rawUrl: `${project.dir}/${project.doc}`
    });
  }

  async function openFormative(id) {
    const item = findFormative(id);
    if (!item) { showLanding(); return; }
    clearSidebarActive();
    const link = $(`[data-formative="${id}"]`, els.sidebarTree);
    if (link) link.classList.add('active');
    setPath(`Ejercicios formativos · ${item.tag}`);
    closeMobileSidebar();
    await openMarkdown(item.dir, {
      title: item.title,
      badge: 'Refuerzo',
      rawUrl: item.dir
    });
  }

  /* ------------------------------------------------------------
     Slides
     ------------------------------------------------------------ */
  async function openSlides(url, title) {
    showOnly('slides');
    closeMobileSidebar();
    els.slidesTitle.textContent = title;
    els.slidesStage.innerHTML = '<div class="md-state">Cargando presentación…</div>';
    els.slidesControls.hidden = true;
    state.currentSlideSource = url;
    state.slides = [];
    state.slideIndex = 0;
    els.slidesFullBtn.disabled = false;

    try {
      const res = await fetch(url, { cache: 'no-store' });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const html = await res.text();
      const doc = new DOMParser().parseFromString(html, 'text/html');
      let slides = $$('.slide', doc).map(s => s.outerHTML);
      if (!slides.length) {
        const deck = $('.deck', doc);
        if (deck) slides = $$('.slide', deck).map(s => s.outerHTML);
      }
      if (!slides.length) throw new Error('La presentación no contiene slides.');
      state.slides = slides;
      els.slidesStage.innerHTML = slides.join('');
      buildDots();
      goToSlide(0);
      els.slidesControls.hidden = false;
    } catch (err) {
      els.slidesStage.innerHTML = `<div class="md-state"><strong>No se pudo cargar la presentación</strong>${escapeHtml(err.message)}<br><code>${escapeHtml(url)}</code></div>`;
      els.slideDots.innerHTML = '';
      els.slideCounter.textContent = '0 / 0';
    }
  }

  function buildDots() {
    els.slideDots.innerHTML = state.slides.map((_, i) =>
      `<button class="dot" data-dot="${i}" aria-label="Ir al slide ${i + 1}"></button>`
    ).join('');
  }

  function goToSlide(index) {
    if (!state.slides.length) return;
    const total = state.slides.length;
    state.slideIndex = Math.max(0, Math.min(index, total - 1));
    $$('.slide', els.slidesStage).forEach((slide, i) => {
      slide.classList.toggle('is-active', i === state.slideIndex);
    });
    $$('.dot', els.slideDots).forEach((dot, i) => {
      dot.classList.toggle('is-active', i === state.slideIndex);
    });
    els.slideCounter.textContent = `${state.slideIndex + 1} / ${total}`;
    els.slidePrev.disabled = state.slideIndex === 0;
    els.slideNext.disabled = state.slideIndex === total - 1;
    const active = $('.slide.is-active', els.slidesStage);
    if (active) active.scrollTop = 0;
  }

  function nextSlide() { goToSlide(state.slideIndex + 1); }
  function prevSlide() { goToSlide(state.slideIndex - 1); }

  /* ------------------------------------------------------------
     Landing
     ------------------------------------------------------------ */
  function renderLanding() {
    const weeksTotal = allWeeks().length + PROJECTS.length;
    const schedule = [];

    UNITS.forEach(unit => {
      unit.weeks.forEach(w => schedule.push({ type: 'week', num: w.num, title: w.title, unit, ref: w }));
      PROJECTS.filter(p => p.unit === unit.id).forEach(p => {
        schedule.push({ type: 'project', num: p.num, title: p.title, unit, project: p });
      });
    });
    schedule.sort((a, b) => a.num - b.num);

    const unitCards = UNITS.map(unit => {
      const project = PROJECTS.find(p => p.unit === unit.id);
      const chips = unit.weeks.map(w =>
        `<button class="week-chip" data-go-week="${w.num}" title="${escapeHtml(w.title)}">S${pad(w.num)}</button>`
      ).join('');
      const projectChip = project
        ? `<button class="week-chip is-project" data-go-project="${project.id}" title="${escapeHtml(project.title)}">${project.id.toUpperCase()}</button>`
        : '';
      return `
        <article class="unit-card ${unit.id}">
          <div class="unit-top">
            <span class="unit-kicker">Unidad ${unit.num}</span>
            <span class="unit-weeks-count">${unit.weeksLabel}</span>
          </div>
          <h3>${escapeHtml(unit.title)}</h3>
          <p>${escapeHtml(unit.desc)}</p>
          <div class="week-chips">${chips}${projectChip}</div>
          <div class="week-chips">
            ${unit.tags.slice(0, 4).map(t => `<span class="week-chip" style="cursor:default">${escapeHtml(t)}</span>`).join('')}
          </div>
          <div class="unit-foot">
            <span>${escapeHtml(unit.result.split('·')[0].trim())}</span>
            <button data-go-week="${unit.weeks[0].num}">Empezar →</button>
          </div>
        </article>
      `;
    }).join('');

    const scheduleRows = schedule.map(item => {
      const unit = item.unit;
      if (item.type === 'project') {
        return `
          <button class="schedule-item ${unit.id} is-project" data-go-project="${item.project.id}">
            <span class="schedule-week">S${pad(item.num)}</span>
            <span class="schedule-title">${escapeHtml(item.title)}</span>
            <span class="schedule-tag">${item.project.id.toUpperCase()} · ${item.project.weight}%</span>
          </button>
        `;
      }
      const isClose = item.num === 16;
      return `
        <button class="schedule-item ${unit.id} ${isClose ? 'is-eval' : ''}" data-go-week="${item.num}">
          <span class="schedule-week">S${pad(item.num)}</span>
          <span class="schedule-title">${escapeHtml(item.title)}</span>
          <span class="schedule-tag">${isClose ? 'Cierre' : 'U' + unit.num}</span>
        </button>
      `;
    }).join('');

    const evalRows = PROJECTS.map(p => {
      const unit = unitById(p.unit);
      return `
        <tr>
          <td><strong>${p.id.toUpperCase()}</strong></td>
          <td>${escapeHtml(unit.short)}</td>
          <td>${escapeHtml(p.modality)}</td>
          <td class="w">${p.weight}%</td>
        </tr>
      `;
    }).join('');

    const criteriaRows = CRITERIA.map(c => {
      const unit = unitById(c.unit);
      return `
        <div class="criterion ${unit.id}">
          <span class="code">${c.code}</span>
          <span>${escapeHtml(c.label)}</span>
          <span class="bar"><i style="width:${(c.weight / 20) * 100}%"></i></span>
          <span>${c.weight}%</span>
        </div>
      `;
    }).join('');

    const projectCards = PROJECTS.map(p => `
      <article class="project-card" data-go-project="${p.id}">
        <div class="project-head">
          <span class="project-id">${p.id.toUpperCase()}</span>
          <span class="project-weight">${p.weight}% · ${escapeHtml(p.modality)}</span>
        </div>
        <h3>${escapeHtml(p.title.split('·')[1].trim())}</h3>
        <p>${escapeHtml(p.desc)}</p>
        <div class="project-tags">${p.tags.map(t => `<span>${escapeHtml(t)}</span>`).join('')}</div>
        <span class="project-open">Abrir enunciado →</span>
      </article>
    `).join('');

    const resourceCards = RESOURCES.map(r => `
      <a class="res-item" href="${r.url}" target="_blank" rel="noopener noreferrer">
        <strong>${escapeHtml(r.title)}</strong>
        <span>${escapeHtml(r.desc)}</span>
        <em>${escapeHtml(r.label)} ↗</em>
      </a>
    `).join('');

    const stackChips = COURSE.stack.map(s => `<span class="stack-chip"><b>·</b> ${escapeHtml(s)}</span>`).join('');

    els.landing.innerHTML = `
      <div class="landing-wrap">
        <header class="hero">
          <span class="hero-badge">Curso completo · 16 semanas</span>
          <h1>Programación <span>Orientada a Objetos</span> con Python</h1>
          <p class="hero-sub">${escapeHtml(COURSE.description)}</p>
          <div class="hero-meta">
            <span>3 unidades</span>
            <span>3 proyectos</span>
            <span>Videojuegos + banca</span>
            <span>Consola → escritorio</span>
          </div>
          <div class="hero-stats">
            <div class="stat"><strong>16</strong><span>semanas</span></div>
            <div class="stat"><strong>3</strong><span>unidades</span></div>
            <div class="stat"><strong>3</strong><span>proyectos</span></div>
            <div class="stat"><strong>100%</strong><span>práctico</span></div>
          </div>
          <div class="hero-actions">
            <button class="btn btn-primary" data-go-week="1">Empezar la semana 1 <span class="arrow">→</span></button>
            <button class="btn" data-scroll="evaluacion">Ver evaluación</button>
            <button class="btn" data-scroll="proyectos">Proyectos</button>
          </div>
        </header>

        <section class="section" id="ruta">
          <div class="section-head">
            <div class="section-eyebrow">Ruta de aprendizaje</div>
            <h2 class="section-title">Tres unidades, un videojuego completo</h2>
            <p class="section-lead">Cada unidad cierra con un proyecto. Empiezas con objetos aislados, sigues con jerarquías que combaten entre sí y terminas con una aplicación de escritorio con interfaz gráfica.</p>
          </div>
          <div class="unit-grid">${unitCards}</div>
        </section>

        <section class="section" id="calendario">
          <div class="section-head">
            <div class="section-eyebrow">Calendario</div>
            <h2 class="section-title">Las 16 semanas</h2>
            <p class="section-lead">Semanas de contenido, semanas de evaluación y cierre. Haz clic en cualquier semana para abrir su documento principal.</p>
          </div>
          <div class="schedule-grid">${scheduleRows}</div>
          <p class="section-lead" style="margin-top:12px">16 semanas en total: ${weeksTotal - PROJECTS.length} semanas de contenido · ${PROJECTS.length} proyectos evaluables.</p>
        </section>

        <section class="section" id="evaluacion">
          <div class="section-head">
            <div class="section-eyebrow">Evaluación</div>
            <h2 class="section-title">100% por proyectos</h2>
            <p class="section-lead">Sin exámenes escritos. Cada unidad se cierra construyendo software y sustentándolo. Los criterios CE provienen del planeador oficial del curso.</p>
          </div>
          <div class="eval-grid">
            <div class="eval-card">
              <h3>Pesos y modalidad</h3>
              <table class="eval-table">
                <thead><tr><th>Proyecto</th><th>Unidad</th><th>Modalidad</th><th>Peso</th></tr></thead>
                <tbody>${evalRows}</tbody>
              </table>
              <h3 style="margin-top:20px">Criterios del planeador</h3>
              <div class="criteria-list">${criteriaRows}</div>
            </div>
            <div class="formula-card">
              <h3>Nota final</h3>
              <div class="formula">
                <span><strong>Nota</strong> = P1 × 0.25</span>
                <span style="padding-left:64px">+ P2 × 0.30</span>
                <span style="padding-left:64px">+ P3 × 0.45</span>
              </div>
              <p class="formula-note">Dentro de cada proyecto, sus dos criterios CE pesan 50/50. La rúbrica cualitativa de cada entrega se encuentra en el enunciado del proyecto.</p>
              <div class="criteria-list">
                <div class="criterion u1"><span class="code">P1</span><span>CE1.1 + CE1.2</span><span class="bar"><i style="width:25%"></i></span><span>25%</span></div>
                <div class="criterion u2"><span class="code">P2</span><span>CE2.1 + CE2.2</span><span class="bar"><i style="width:30%"></i></span><span>30%</span></div>
                <div class="criterion u3"><span class="code">P3</span><span>CE3.1 + CE3.2</span><span class="bar"><i style="width:45%"></i></span><span>45%</span></div>
              </div>
              <p class="formula-note">Política: un proyecto que no ejecuta obtiene máximo 3.0. Copia entre compañeros: 0. Sustentación obligatoria por integrante.</p>
            </div>
          </div>
        </section>

        <section class="section" id="proyectos">
          <div class="section-head">
            <div class="section-eyebrow">Proyectos</div>
            <h2 class="section-title">Tres entregas, tres niveles</h2>
            <p class="section-lead">De una app de consola individual a un arcade completo con interfaz gráfica. Todos los enunciados incluyen requisitos, rúbrica y checklist de sustentación.</p>
          </div>
          <div class="project-grid">${projectCards}</div>
        </section>

        <section class="section" id="recursos">
          <div class="section-head">
            <div class="section-eyebrow">Recursos</div>
            <h2 class="section-title">Para seguir aprendiendo</h2>
          </div>
          <div class="res-grid">${resourceCards}</div>
        </section>

        <section class="section" id="stack">
          <div class="section-head">
            <div class="section-eyebrow">Stack</div>
            <h2 class="section-title">Herramientas del curso</h2>
            <p class="section-lead">Todo funciona en Linux, Windows y macOS. Sin instalaciones más allá de Python y VS Code.</p>
          </div>
          <div class="stack-row">${stackChips}</div>
        </section>

        <footer class="footer">
          <span>Curso de Programación Orientada a Objetos · Python</span>
          <span>16 semanas · 3 unidades · 3 proyectos</span>
          <span>Uso educativo</span>
        </footer>
      </div>
    `;

    bindLandingEvents();
  }

  function bindLandingEvents() {
    $$('[data-go-week]', els.landing).forEach(btn => {
      btn.addEventListener('click', () => {
        location.hash = `#/semana-${btn.dataset.goWeek}/doc`;
      });
    });
    $$('[data-go-project]', els.landing).forEach(btn => {
      btn.addEventListener('click', () => {
        location.hash = `#/proyecto-${btn.dataset.goProject}`;
      });
    });
    $$('[data-scroll]', els.landing).forEach(btn => {
      btn.addEventListener('click', () => {
        const target = document.getElementById(btn.dataset.scroll);
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  /* ------------------------------------------------------------
     Routing
     ------------------------------------------------------------ */
  function route() {
    const hash = location.hash;
    state.activeHash = hash;

    if (!hash || hash === '#' || hash === '#/' || hash === '#') {
      showLanding();
      return;
    }

    let m = hash.match(/^#\/semana-(\d+)\/(\w+)$/);
    if (m) {
      const week = findWeek(Number(m[1]));
      if (week) {
        closeMobileSidebar();
        openWeekWeek(week, m[2]);
        return;
      }
    }

    m = hash.match(/^#\/proyecto-(p\d+)$/i);
    if (m) {
      closeMobileSidebar();
      openProject(m[1].toLowerCase());
      return;
    }

    m = hash.match(/^#\/formativo-(\w+)$/i);
    if (m) {
      closeMobileSidebar();
      openFormative(m[1].toLowerCase());
      return;
    }

    if (hash === '#/eval') {
      showLanding('evaluacion');
      return;
    }

    showLanding();
  }

  /* ------------------------------------------------------------
     Eventos globales
     ------------------------------------------------------------ */
  function bindGlobalEvents() {
    window.addEventListener('hashchange', route);

    els.homeBtn.addEventListener('click', () => {
      history.pushState(null, '', location.pathname + location.search);
      route();
    });

    els.brandBtn.addEventListener('click', () => {
      history.pushState(null, '', location.pathname + location.search);
      route();
    });

    els.sidebarToggle.addEventListener('click', () => {
      if (window.innerWidth <= 768) {
        const open = els.sidebar.classList.toggle('open');
        els.sidebarOverlay.classList.toggle('open', open);
      } else {
        els.sidebar.classList.toggle('hidden');
      }
    });

    els.sidebarOverlay.addEventListener('click', closeMobileSidebar);

    els.sidebarTree.addEventListener('click', ev => {
      const link = ev.target.closest('a');
      if (!link) return;
      if (link.dataset.home) {
        ev.preventDefault();
        history.pushState(null, '', location.pathname + location.search);
        route();
        return;
      }
      if (link.dataset.project) closeMobileSidebar();
      if (link.dataset.formative) closeMobileSidebar();
      if (link.dataset.evalLink) closeMobileSidebar();
    });

    els.mdRawBtn.addEventListener('click', () => {
      if (state.currentRawUrl) window.open(state.currentRawUrl, '_blank', 'noopener');
    });

    els.slidesFullBtn.addEventListener('click', () => {
      if (state.currentSlideSource) window.open(state.currentSlideSource, '_blank', 'noopener');
    });

    els.slidePrev.addEventListener('click', prevSlide);
    els.slideNext.addEventListener('click', nextSlide);

    els.slideDots.addEventListener('click', ev => {
      const dot = ev.target.closest('[data-dot]');
      if (dot) goToSlide(Number(dot.dataset.dot));
    });

    document.addEventListener('keydown', ev => {
      if (!els.slidesView.classList.contains('show')) return;
      const tag = (ev.target.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
      if (ev.key === 'ArrowRight' || ev.key === 'PageDown') {
        ev.preventDefault();
        nextSlide();
      } else if (ev.key === 'ArrowLeft' || ev.key === 'PageUp') {
        ev.preventDefault();
        prevSlide();
      } else if (ev.key === 'Home') {
        ev.preventDefault();
        goToSlide(0);
      } else if (ev.key === 'End') {
        ev.preventDefault();
        goToSlide(state.slides.length - 1);
      }
    });

    let touchStartX = 0;
    els.slidesStage.addEventListener('touchstart', ev => {
      touchStartX = ev.changedTouches[0].clientX;
    }, { passive: true });
    els.slidesStage.addEventListener('touchend', ev => {
      const delta = ev.changedTouches[0].clientX - touchStartX;
      if (Math.abs(delta) > 55) {
        if (delta < 0) nextSlide();
        else prevSlide();
      }
    }, { passive: true });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 768) {
        els.sidebar.classList.remove('open');
        els.sidebarOverlay.classList.remove('open');
      }
    });
  }

  /* ------------------------------------------------------------
     Init
     ------------------------------------------------------------ */
  function init() {
    buildSidebar();
    renderLanding();
    bindGlobalEvents();
    route();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
