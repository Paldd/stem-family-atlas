/* Child-specific planning from selected official sources, with no booking action. */
(() => {
  'use strict';
  const data = window.STEM_DATA?.family_strategy?.nearby_participation_v118;
  if (!data) return;
  const additional = window.STEM_DATA.family_strategy.nearby_participation_v135;
  const events = new Map(window.STEM_DATA.events.map(e => [e.id, e]));
  const safe = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let child = 'family', showClosed = false, budget = 'both-have-equipment';
  const modeNames = {check:"el permiso de comprobar",existing_only:"sólo la participación previamente registrada",visitor:"visita familiar",prepare:"Prepararse para la temporada",closed:"El plazo de los nuevos equipos ha pasado."};
  const money = value => new Intl.NumberFormat('es', {minimumFractionDigits:2, maximumFractionDigits:2}).format(value) + ' MXN';
  const date = value => value ? new Intl.DateTimeFormat('es', {day:'numeric',month:'long',year:'numeric',timeZone:'UTC'}).format(new Date(value+'T12:00:00Z')) : "la siguiente fecha no se ha anunciado";
  function cards() {
    const items = data.items.filter(q => (showClosed || q.mode !== 'closed') && (child === 'family' || q.children.includes(child)));
    return `<p class="nearby-count" aria-live="polite">${items.length} de las opciones elegidas · verificación ${safe(data.checked)}</p><div class="nearby-cards">${items.map(q => {
      const e = events.get(q.id), label = e.start ? date(e.start) + (e.end !== e.start ? ' — '+date(e.end) : '') : date('');
      return `<article class="nearby-card" data-nearby-id="${safe(q.id)}"><div class="nearby-card-meta"><span class="nearby-mode ${safe(q.mode)}">${safe(modeNames[q.mode])}</span><small>${safe(e.country)}</small></div><h4>${safe(q.title)}</h4><p class="nearby-date">${safe(label)}</p><p>${safe(q.gate)}</p><details><summary>el siguiente paso y las condiciones</summary><p>${safe(q.step)}</p><p><b>Matvey:</b> ${safe(e.mat)}<br><b>Oscar:</b> ${safe(e.osc)}</p><p><b>El equipo:</b> ${safe(e.format)}</p></details><button type="button" class="button secondary" data-open="${safe(q.id)}">tarjeta completa</button></article>`;
    }).join('')}</div>`;
  }
  function budgetMarkup() {
    const selected = data.budget_scenarios.find(q => q.id === budget);
    const prices = new Map(data.prices.map(p => [p.id,p]));
    return `<section class="nearby-budget" aria-label="cálculo parcial de MakeX"><div><p class="section-kicker">MAKE X · CUOTA Y EQUIPAMIENTO</p><h3>que ya se puede calcular</h3><p>elige el guión. Es parte del presupuesto de la tienda, pero aún falta una cuenta completa del organizador.</p></div><label>El guión<select data-nearby-budget>${data.budget_scenarios.map(q=>`<option value="${safe(q.id)}"${q.id===budget?' selected':''}>${safe(q.title)}</option>`).join('')}</select></label><div class="nearby-budget-result" aria-live="polite"><strong>${money(selected.amount)}</strong><span>el cálculo parcial · ${selected.children.map(c=>c==='matvey'?"Matvey":"Oscar").join(' + ')}</span><p>${safe(selected.detail)}</p><div>${selected.items.map(id=>`<a href="${safe(prices.get(id).url)}" target="_blank" rel="noopener">${money(prices.get(id).amount)} · fuente ↗</a>`).join('')}</div></div><details><summary>¿Qué es lo que debe saber antes de pagar?</summary><p>${safe(data.price_limits)}</p></details></section>`;
  }
  function additionalMarkup() {
    if (!additional) return '';
    const items = additional.items.filter(q => child === 'family' || q.children.includes(child));
    return `<section class="nearby-additional" aria-labelledby="nearby-additional-title"><p class="section-kicker">CATEGORÍA · RESULTADO · PRÓXIMA TEMPORADA</p><h3 id="nearby-additional-title">${safe(additional.title)}</h3><p>${safe(additional.conclusion)}</p><p class="nearby-count" aria-live="polite">${items.length} de las opciones adicionales · de la verificación ${safe(additional.checked)}</p><div class="nearby-cards">${items.map(q => {
      const e = events.get(q.id);
      const timing = e.start ? date(e.start) + (e.end !== e.start ? ' — '+date(e.end) : '') : "el siguiente conjunto no se ha anunciado";
      return `<article class="nearby-card" data-nearby-additional-id="${safe(q.id)}"><div class="nearby-card-meta"><span class="nearby-mode ${e.start ? 'check' : 'prepare'}">${e.start ? "Date tiene · permiso para comprobar" : "preparación de las reglas 2026"}</span><small>${safe(e.country)}</small></div><h4>${safe(q.title)}</h4><p class="nearby-date">${safe(timing)}</p><p>${safe(q.gate)}</p><details><summary>habilidad, resultado y siguiente paso</summary><p>${safe(q.step)}</p><p><b>el resultado:</b> ${safe(e.reward)}</p><p><b>Matvey:</b> ${safe(e.mat)}<br><b>Oscar:</b> ${safe(e.osc)}</p><p><b>El equipo:</b> ${safe(e.format)}</p></details><button type="button" class="button secondary" data-open="${safe(q.id)}">tarjeta completa</button></article>`;
    }).join('')}</div><details class="nearby-season"><summary>límites de edad, idioma y premios</summary><ul>${additional.limits.map(q=>`<li>${safe(q)}</li>`).join('')}</ul></details><p class="nearby-footnote"><a href="downloads/STEM_соревнования_Мексика_мастерские_v135.md" download>Descripción de las fuentes ↓</a> · <button type="button" class="league-link" data-guide-profile="robofest-latam">Categoría de Robofest LATAM →</button> <button type="button" class="league-link" data-guide-profile="bajabot">BajaBot por clases →</button></p></section>`;
  }
  window.nearbyParticipationMarkup = () => `<section id="nearby-participation" class="nearby-panel" aria-labelledby="nearby-title"><header><p class="section-kicker">DEL PLAN A LA PARTICIPACIÓN · 2026–2027</p><h3 id="nearby-title">Comienza por aquí.<br><em>Cada uno tiene su papel.</em></h3><p>${safe(data.conclusion)}</p><small>${safe(data.age_note)}</small></header><div class="nearby-controls"><div role="group" aria-label="para quien buscar el inicio">${[['family',"familia"],['matvey',"Matvey"],['oscar',"Oscar"]].map(([id,title])=>`<button type="button" data-nearby-child="${id}" aria-pressed="${child===id}">${title}</button>`).join('')}</div><label><input type="checkbox" data-nearby-closed${showClosed?' checked':''}> mostrar los términos de los nuevos comandos</label></div><p class="nearby-hint">familia muestra las opciones para cada niño; las categorías de edad y las solicitudes pueden variar.</p><div id="nearby-results">${cards()}</div><div id="nearby-additional">${additionalMarkup()}</div><div id="nearby-budget">${budgetMarkup()}</div><details class="nearby-season"><summary>Cómo organizar las próximas6–8 semanas</summary><ol>${data.next_steps.map(q=>`<li>${safe(q)}</li>`).join('')}</ol></details><p class="nearby-footnote">${safe(data.scope)} <a href="downloads/STEM_nearby_participation_audit_v118.json" download>Fuentes y límites de verificación ↓</a></p></section>`;
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-nearby-child]');
    if (!button) return;
    child = button.dataset.nearbyChild;
    document.querySelectorAll('[data-nearby-child]').forEach(b=>b.setAttribute('aria-pressed', String(b.dataset.nearbyChild===child)));
    document.querySelector('#nearby-results').innerHTML = cards();
    document.querySelector('#nearby-additional').innerHTML = additionalMarkup();
  });
  document.addEventListener('change', event => {
    if (event.target.matches('[data-nearby-closed]')) {showClosed=event.target.checked; document.querySelector('#nearby-results').innerHTML=cards();}
    if (event.target.matches('[data-nearby-budget]')) {budget=event.target.value; document.querySelector('#nearby-budget').innerHTML=budgetMarkup(); document.querySelector('[data-nearby-budget]').focus({preventScroll:true});}
  });
})();
