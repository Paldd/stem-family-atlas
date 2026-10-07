/* Child-specific planning from selected official sources, with no booking action. */
(() => {
  'use strict';
  const data = window.STEM_DATA?.family_strategy?.nearby_participation_v118;
  if (!data) return;
  const additional = window.STEM_DATA.family_strategy.nearby_participation_v135;
  const events = new Map(window.STEM_DATA.events.map(e => [e.id, e]));
  const safe = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let child = 'family', showClosed = false, budget = 'both-have-equipment';
  const modeNames = {check:'Допуск проверить',existing_only:'Только ранее оформленное участие',visitor:'Семейное посещение',prepare:'Подготовка к сезону',closed:'Срок новых команд прошёл'};
  const money = value => new Intl.NumberFormat('ru-RU', {minimumFractionDigits:2, maximumFractionDigits:2}).format(value) + ' MXN';
  const date = value => value ? new Intl.DateTimeFormat('ru-RU', {day:'numeric',month:'long',year:'numeric',timeZone:'UTC'}).format(new Date(value+'T12:00:00Z')) : 'Следующая дата не объявлена';
  function cards() {
    const items = data.items.filter(q => (showClosed || q.mode !== 'closed') && (child === 'family' || q.children.includes(child)));
    return `<p class="nearby-count" aria-live="polite">${items.length} выбранных вариантов · проверка ${safe(data.checked)}</p><div class="nearby-cards">${items.map(q => {
      const e = events.get(q.id), label = e.start ? date(e.start) + (e.end !== e.start ? ' — '+date(e.end) : '') : date('');
      return `<article class="nearby-card" data-nearby-id="${safe(q.id)}"><div class="nearby-card-meta"><span class="nearby-mode ${safe(q.mode)}">${safe(modeNames[q.mode])}</span><small>${safe(e.country)}</small></div><h4>${safe(q.title)}</h4><p class="nearby-date">${safe(label)}</p><p>${safe(q.gate)}</p><details><summary>Следующий шаг и условия</summary><p>${safe(q.step)}</p><p><b>Матвей:</b> ${safe(e.mat)}<br><b>Оскар:</b> ${safe(e.osc)}</p><p><b>Команда:</b> ${safe(e.format)}</p></details><button type="button" class="button secondary" data-open="${safe(q.id)}">Полная карточка ↗</button></article>`;
    }).join('')}</div>`;
  }
  function budgetMarkup() {
    const selected = data.budget_scenarios.find(q => q.id === budget);
    const prices = new Map(data.prices.map(p => [p.id,p]));
    return `<section class="nearby-budget" aria-label="Частичный расчёт MakeX"><div><p class="section-kicker">MAKE X · ВЗНОС И ТЕХНИКА</p><h3>Что уже можно посчитать</h3><p>Выберите сценарий. Это часть бюджета по данным магазина; полный счёт организатора ещё нужен.</p></div><label>Сценарий<select data-nearby-budget>${data.budget_scenarios.map(q=>`<option value="${safe(q.id)}"${q.id===budget?' selected':''}>${safe(q.title)}</option>`).join('')}</select></label><div class="nearby-budget-result" aria-live="polite"><strong>${money(selected.amount)}</strong><span>Частичный расчёт · ${selected.children.map(c=>c==='matvey'?'Матвей':'Оскар').join(' + ')}</span><p>${safe(selected.detail)}</p><div>${selected.items.map(id=>`<a href="${safe(prices.get(id).url)}" target="_blank" rel="noopener">${money(prices.get(id).amount)} · источник ↗</a>`).join('')}</div></div><details><summary>Что уточнить перед оплатой</summary><p>${safe(data.price_limits)}</p></details></section>`;
  }
  function additionalMarkup() {
    if (!additional) return '';
    const items = additional.items.filter(q => child === 'family' || q.children.includes(child));
    return `<section class="nearby-additional" aria-labelledby="nearby-additional-title"><p class="section-kicker">КАТЕГОРИЯ · РЕЗУЛЬТАТ · СЛЕДУЮЩИЙ СЕЗОН</p><h3 id="nearby-additional-title">${safe(additional.title)}</h3><p>${safe(additional.conclusion)}</p><p class="nearby-count" aria-live="polite">${items.length} дополнительных вариантов · проверка ${safe(additional.checked)}</p><div class="nearby-cards">${items.map(q => {
      const e = events.get(q.id);
      const timing = e.start ? date(e.start) + (e.end !== e.start ? ' — '+date(e.end) : '') : 'Следующий набор не объявлен';
      return `<article class="nearby-card" data-nearby-additional-id="${safe(q.id)}"><div class="nearby-card-meta"><span class="nearby-mode ${e.start ? 'check' : 'prepare'}">${e.start ? 'Дата есть · допуск проверить' : 'Подготовка · правила 2026'}</span><small>${safe(e.country)}</small></div><h4>${safe(q.title)}</h4><p class="nearby-date">${safe(timing)}</p><p>${safe(q.gate)}</p><details><summary>Навык, результат и следующий шаг</summary><p>${safe(q.step)}</p><p><b>Результат:</b> ${safe(e.reward)}</p><p><b>Матвей:</b> ${safe(e.mat)}<br><b>Оскар:</b> ${safe(e.osc)}</p><p><b>Команда:</b> ${safe(e.format)}</p></details><button type="button" class="button secondary" data-open="${safe(q.id)}">Полная карточка ↗</button></article>`;
    }).join('')}</div><details class="nearby-season"><summary>Границы возраста, языка и призов</summary><ul>${additional.limits.map(q=>`<li>${safe(q)}</li>`).join('')}</ul></details><p class="nearby-footnote"><a href="downloads/STEM_соревнования_Мексика_мастерские_v135.md" download>Подробный разбор с источниками ↓</a> · <button type="button" class="league-link" data-guide-profile="robofest-latam">Категории Robofest LATAM →</button> <button type="button" class="league-link" data-guide-profile="bajabot">BajaBot по классам →</button></p></section>`;
  }
  window.nearbyParticipationMarkup = () => `<section id="nearby-participation" class="nearby-panel" aria-labelledby="nearby-title"><header><p class="section-kicker">ОТ ПЛАНА К УЧАСТИЮ · 2026–2027</p><h3 id="nearby-title">Начать рядом.<br><em>У каждого — своя роль.</em></h3><p>${safe(data.conclusion)}</p><small>${safe(data.age_note)}</small></header><div class="nearby-controls"><div role="group" aria-label="Для кого искать старт">${[['family','Семья'],['matvey','Матвей'],['oscar','Оскар']].map(([id,title])=>`<button type="button" data-nearby-child="${id}" aria-pressed="${child===id}">${title}</button>`).join('')}</div><label><input type="checkbox" data-nearby-closed${showClosed?' checked':''}> Показать прошедшие сроки новых команд</label></div><p class="nearby-hint">«Семья» показывает варианты для каждого ребёнка; возрастные категории и заявки могут различаться. Места и допуск ещё нужно подтвердить.</p><div id="nearby-results">${cards()}</div><div id="nearby-additional">${additionalMarkup()}</div><div id="nearby-budget">${budgetMarkup()}</div><details class="nearby-season"><summary>Как построить следующие 6–8 недель</summary><ol>${data.next_steps.map(q=>`<li>${safe(q)}</li>`).join('')}</ol></details><p class="nearby-footnote">${safe(data.scope)} <a href="downloads/STEM_nearby_participation_audit_v118.json" download>Источники и границы проверки ↓</a></p></section>`;
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
