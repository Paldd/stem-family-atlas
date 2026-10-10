'use strict';
// Same stable record IDs and browser-local plans in both language editions.
(function languageLinks() {
 const sync = () => document.querySelectorAll('[data-atlas-language]').forEach(link => {
  const target = link.dataset.atlasLanguage;
  const current = document.documentElement.lang;
  const base = target === current ? './' : target === 'es' ? 'es/' : '../';
  link.href = base + location.search + location.hash;
  link.setAttribute('aria-current', target === current ? 'page' : 'false');
 });
 sync();
 addEventListener('hashchange', sync);
 addEventListener('popstate', sync);
 document.addEventListener('input', () => queueMicrotask(sync));
 document.addEventListener('change', () => queueMicrotask(sync));
 document.addEventListener('click', event => {
  if(event.target.closest('[data-atlas-language]')) sync();
 }, true);
 document.addEventListener('click', () => queueMicrotask(sync));
})();
