/* ============================================================
   engine/slides.js — navegación de presentaciones autocontenidas
   ============================================================ */

(function () {
  'use strict';

  const slides = Array.from(document.querySelectorAll('.slide'));
  if (!slides.length) return;

  const prev = document.getElementById('prev');
  const next = document.getElementById('next');
  const counter = document.getElementById('counter');
  const dotsWrap = document.getElementById('dots');
  let index = 0;
  let touchX = 0;

  dotsWrap.innerHTML = slides.map((_, i) =>
    `<button type="button" data-dot="${i}" aria-label="Ir al slide ${i + 1}"></button>`
  ).join('');

  const dots = Array.from(dotsWrap.querySelectorAll('[data-dot]'));

  function goTo(i) {
    index = Math.max(0, Math.min(i, slides.length - 1));
    slides.forEach((slide, n) => slide.classList.toggle('is-active', n === index));
    dots.forEach((dot, n) => dot.classList.toggle('is-active', n === index));
    counter.textContent = `${index + 1} / ${slides.length}`;
    prev.disabled = index === 0;
    next.disabled = index === slides.length - 1;
    const active = slides[index];
    if (active) active.scrollTop = 0;
  }

  prev.addEventListener('click', () => goTo(index - 1));
  next.addEventListener('click', () => goTo(index + 1));
  dotsWrap.addEventListener('click', ev => {
    const dot = ev.target.closest('[data-dot]');
    if (dot) goTo(Number(dot.dataset.dot));
  });

  document.addEventListener('keydown', ev => {
    const tag = (ev.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
    if (ev.key === 'ArrowRight' || ev.key === 'PageDown' || ev.key === ' ') {
      ev.preventDefault();
      goTo(index + 1);
    } else if (ev.key === 'ArrowLeft' || ev.key === 'PageUp') {
      ev.preventDefault();
      goTo(index - 1);
    } else if (ev.key === 'Home') {
      ev.preventDefault();
      goTo(0);
    } else if (ev.key === 'End') {
      ev.preventDefault();
      goTo(slides.length - 1);
    }
  });

  document.addEventListener('touchstart', ev => {
    touchX = ev.changedTouches[0].clientX;
  }, { passive: true });
  document.addEventListener('touchend', ev => {
    const delta = ev.changedTouches[0].clientX - touchX;
    if (Math.abs(delta) > 55) {
      if (delta < 0) goTo(index + 1);
      else goTo(index - 1);
    }
  }, { passive: true });

  goTo(0);
})();
