/* Permanent schools have their own filters; they never become dated events. */
(() => {
  const schools = window.STEM_DATA.schools || [];
  const focus = window.STEM_DATA.school_focus;
  const selected = new Set();
  let filters = {best:'',query:'',country:'',region:'',type:'',fit:'',language:'',ib:'',boarding:'',evidence:''};
  let initialized = false;
  let territory = [];
  let territoryLabel = '';
  window.focusAtlasSchools = (isos, label, child) => {
    Object.keys(filters).forEach(k=>filters[k]='');
    territory = Array.isArray(isos) ? isos.filter(x=>schools.some(s=>s.iso===x)) : [];
    territoryLabel = typeof label==='string' ? label : '';
    filters.fit = ['both','mat','osc'].includes(child) ? child : '';
    render();
  };
  const types = {public:'Государственная',private:'Частная',private_industry:'Частная · сеть индустрии'};
  const tiers = {world_result:'Есть мировой результат',national_result:'Есть национальный результат',other_result:'Есть соревновательный результат',programme:'Программа · победы не установлены'};
  const fitNames = {candidate:'Кандидат в дневную ступень',future:'Будущая secondary',unknown:'Возраст / вход уточнить'};
  const ibNames = {candidate:'candidate',authorized_registry:'авторизовано · IB registry',school_report:'по сообщению школы',school_report_authorized:'авторизация по сообщению школы'};
  const provenance = {organizer_report:'Сообщение организатора',organizer_protocol:'Официальный протокол организатора',school_report:'Сообщение школы',school_operator_report:'Сообщение школьной сети / оператора'};
  const sourceKind = {school:'Школа',public_school:'Государственная школа',registry:'Официальный справочник',organizer:'Организатор соревнования',school_operator:'Школьная сеть / оператор',historical_registry:'Исторический государственный перечень',government:'Государственный справочник',school_team:'Школьная команда',regional_organizer:'Региональный организатор'};
  const q = sel => document.querySelector(sel);
  const safe = x => String(x ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const ibText = s => s.ib_programmes.length ? s.ib_programmes.map(x=>x.programme+' · '+ibNames[x.status]).join('; ') : 'IB не подтверждён';
  const options = (items,label) => `<option value="">${label}</option>`+items.map(([v,t])=>`<option value="${safe(v)}">${safe(t)}</option>`).join('');
  const field = (key,label,items,all) => `<label>${label}<select data-school-filter="${key}" aria-label="${label}">${options(items,all)}</select></label>`;
  function matched(s) {
    if(territory.length && !territory.includes(s.iso)) return false;
    const pick=window.bestPickFor('school',s.id);
    if(filters.best&&(!pick||(filters.best!=='all'&&pick.horizon!==filters.best)))return false;
    if(filters.query && !JSON.stringify(s).toLocaleLowerCase().includes(filters.query.toLocaleLowerCase())) return false;
    if(filters.country && s.iso!==filters.country) return false;
    if(filters.region && s.region!==filters.region) return false;
    if(filters.type && (filters.type==='private' ? !s.school_type.startsWith('private') : s.school_type!==filters.type)) return false;
    if(filters.language && !s.instruction_languages.includes(filters.language)) return false;
    if(filters.boarding && s.boarding!==filters.boarding) return false;
    if(filters.evidence==='organizer' && !s.results.some(r=>r.provenance==='organizer_protocol')) return false;
    if(filters.evidence && filters.evidence!=='organizer' && s.evidence!==filters.evidence) return false;
    if(filters.ib==='any' && !s.ib_programmes.length) return false;
    if(filters.ib==='registry' && !s.ib_programmes.some(x=>x.status==='authorized_registry')) return false;
    if(filters.ib==='candidate' && !s.ib_programmes.some(x=>x.status==='candidate')) return false;
    if(filters.fit==='both' && !(s.fit.mat==='candidate' && s.fit.osc==='candidate')) return false;
    if(filters.fit==='mat' && s.fit.mat!=='candidate') return false;
    if(filters.fit==='osc' && s.fit.osc!=='candidate') return false;
    if(filters.fit==='future' && !(s.fit.mat==='future' || s.fit.osc==='future')) return false;
    return true;
  }
  const chip = (s,k,name) => `<span class="school-fit ${s.fit[k]}">${name} · ${s.fit[k]==='candidate'?'дневной кандидат':s.fit[k]==='future'?'позже':'уточнить'}</span>`;
  function card(s) {
    const r = s.results[0];
    return `<article class="school-card" data-school-id="${s.id}"><div class="school-card-top ${s.evidence}"><span>${safe(s.country)}</span><span class="school-number">${s.id}</span><div class="school-campus-mark" aria-hidden="true">▥<span>⚙</span></div><p>${safe(types[s.school_type])}</p></div><div class="school-card-body"><span class="school-place">${safe(s.city)}</span><h3>${safe(s.name)}</h3>${window.bestBadge('school',s.id)}${window.STEM_DIRECTIONS.kind('school')}<span class="school-evidence ${s.evidence}">${safe(tiers[s.evidence])}</span><p class="school-result">${r?safe(r.season+' · '+r.league+' · '+r.award):'Подтверждены занятия / STEM-программа. Победы требуют проверки.'}</p><div class="school-kids">${chip(s,'mat','Матвей')}${chip(s,'osc','Оскар')}</div><p class="school-card-note">${safe(s.ages)}</p><div class="school-card-tags"><span>${s.instruction_languages.length?'Язык: '+s.instruction_languages.join(' / ')+' · ступень в досье':'Язык преподавания уточнить'}</span><span>${s.boarding==='yes'?'Пансион · возраст отдельно':s.boarding==='no'?'Day school':'Пансион не установлен'}</span></div><div class="school-card-actions"><button class="button secondary" data-school-open="${s.id}">Досье ↗</button><button class="school-compare-button" data-school-compare="${s.id}" aria-pressed="${selected.has(s.id)}">${selected.has(s.id)?'✓ Выбрана':'＋ Сравнить'}</button></div></div></article>`;
  }
  function renderComparison() {
    const node=q('#school-comparison');
    if(!selected.size) {node.hidden=true;node.innerHTML='';return;}
    const a=schools.filter(s=>selected.has(s.id));
    const rows=[['Страна / тип',s=>s.country+' · '+types[s.school_type]],['Матвей / Оскар',s=>fitNames[s.fit.mat]+' / '+fitNames[s.fit.osc]],['Результат',s=>s.results.map(r=>r.season+' · '+r.league+' · '+r.stage+' · '+r.award).join('; ')||'Победы не установлены'],['Источник результата',s=>s.results.map(r=>provenance[r.provenance]).join('; ')||'Программа школы'],['Язык / ступень',s=>s.language_note],['IB',ibText],['Пансион',s=>s.boarding_note],['Приём',s=>s.admissions],['Стоимость',s=>s.cost]];
    node.hidden=false;node.innerHTML=`<div class="school-comparison-title"><h3>Сравнение · ${a.length} из 3</h3><button class="text-button" data-school-compare-clear>Очистить</button></div><div class="school-table-scroll" tabindex="0" aria-label="Сравнение школ, прокрутите таблицу"><table><caption class="sr-only">Сравнение выбранных школ</caption><thead><tr><th scope="col">Проверка</th>${a.map(s=>`<th scope="col">${safe(s.name)}<button data-school-compare="${s.id}" aria-label="Убрать ${safe(s.name)} из сравнения">Убрать ×</button></th>`).join('')}</tr></thead><tbody>${rows.map(([title,fn])=>`<tr><th scope="row">${title}</th>${a.map(s=>`<td>${safe(fn(s))}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  }
  function render() {
    if(!focus || !q('#schools-view')) return;
    if(!initialized) {
      const countries=[...new Map(schools.map(s=>[s.iso,s.country])).entries()].sort((a,b)=>a[1].localeCompare(b[1],'ru'));
      const regions=[...new Set(schools.map(s=>s.region))].sort().map(x=>[x,x]);
      q('#school-filters').innerHTML=`<label class="school-search">Название, город, лига<input type="search" data-school-filter="query" placeholder="TAS, IB, robotics, México…" aria-label="Поиск школ"></label>`+
        field('country','Страна школы',countries,`Все ${countries.length} исследованных стран`)+field('region','Регион школы',regions,'Все регионы')+
        field('best','Редакционная подборка',[['all','Все рекомендации'],['now','Рассматривать сейчас'],['future','Будущие ориентиры']],'Весь школьный список')+field('type','Тип школы',[['public','Государственная'],['private','Частная / индустриальная сеть']],'Все типы')+
        field('fit','Возрастной горизонт',[['both','Дневные кандидаты для обоих'],['mat','Матвей · дневной кандидат'],['osc','Оскар · дневной кандидат'],['future','Будущая secondary']],'Все ступени')+
        field('language','Подтверждённый язык · ступень в досье',[['EN','English · на указанной ступени'],['ES','Español · на указанной ступени'],['RU','Русский · на указанной ступени']],'Любой / уточнить')+
        field('ib','IB-программа',[['any','Любая IB-отметка'],['registry','Авторизация прочитана в IB registry'],['candidate','Есть candidate-программа']],'Любая программа')+
        field('boarding','Пансион школы',[['yes','Есть пансион · возраст отдельно'],['no','Подтверждённая day school'],['unknown','Пансион не установлен']],'Любой режим')+
        field('evidence','Доказательство результата',Object.entries(tiers).concat([['organizer','Есть протокол организатора']]),'Все уровни доказательств');
      q('#school-stats').innerHTML=`<div><strong>${schools.length}</strong><span>школ · исследованный список</span></div><div><strong>${focus.counts.countries}</strong><span>стран · 6 континентов</span></div><button data-school-preset="world"><strong>${focus.counts.world_result}</strong><span>школ с мировым результатом ↗</span></button><button data-school-preset="boarding"><strong>${focus.counts.boarding}</strong><span>пансиона · возраст в досье ↗</span></button>`;
      q('#school-routes').innerHTML=focus.routes.map((r,i)=>`<article><span class="school-route-step">0${i+1}</span><h3>${safe(r.name)}</h3><p>${safe(r.detail)}</p><div>${r.ids.map(id=>`<button data-school-open="${id}">${safe(schools.find(s=>s.id===id).name)} ↗</button>`).join('')}</div></article>`).join('');
      q('#school-method').innerHTML=focus.methodology.map(x=>`<li>${safe(x)}</li>`).join('');
      q('#school-gaps').innerHTML=focus.gaps.map(x=>`<li>${safe(x)}</li>`).join('');
      q('#school-coverage').textContent=`Школы исследованы частично в ${focus.counts.countries} из ${window.STEM_DATA.countries.length} стран и территорий. Остальные ${window.STEM_DATA.countries.length-focus.counts.countries} ещё без школьных карточек. Полностью проаудированных стран: 0.`;
      initialized=true;
    }
    q('#school-filters').querySelectorAll('[data-school-filter]').forEach(x=>{if(x.value!==filters[x.dataset.schoolFilter])x.value=filters[x.dataset.schoolFilter];});
    const a=schools.filter(matched);
    q('#school-count').textContent=`Показано ${a.length} из ${schools.length} школ.${territory.length ? ' Территория трека: '+territoryLabel+'. Сброс снимает это ограничение.' : ''} «Кандидат» означает найденную школьную ступень; класс, язык команды, отбор и место требуют подтверждения.`;
    q('#school-cards').innerHTML=a.length?a.map(card).join(''):`<div class="school-empty"><h3>Таких школ пока нет в исследованном списке</h3><p>Это пробел текущего прохода, а не доказательство отсутствия школ.</p><button class="button secondary" data-school-reset>Сбросить фильтры</button></div>`;
    renderComparison();
    window.renderSchoolHistory?.();
  }
  function open(id) {
    const s=schools.find(x=>x.id===id); if(!s)return;
    const part=(title,value)=>`<section><h3>${title}</h3><p>${safe(value)}</p></section>`;
    q('#school-dialog-content').innerHTML=`<p class="section-kicker">${safe(s.country)} · ${safe(types[s.school_type])} · ${s.id}</p><h2>${safe(s.name)}</h2><p class="school-dialog-location">${safe(s.city)} · проверено ${s.checked}</p><span class="school-evidence ${s.evidence}">${safe(tiers[s.evidence])}</span><p class="school-dossier-intro">${safe(s.curriculum)}</p><div class="school-kids">${chip(s,'mat','Матвей')}${chip(s,'osc','Оскар')}</div><div class="school-dossier-grid">${part('Возраст и класс',s.ages+' '+s.fit.note)}${part('Язык преподавания',s.language_note)}${part('Пансион / day',s.boarding_note)}${part('IB и программа',ibText(s))}${part('Робототехника и команда',s.programme)}${part('Лаборатории и оборудование',s.labs)}${part('ИИ и программирование',s.ai)}${part('Как поступить',s.admissions)}${part('Стоимость · год важен',s.cost)}</div><section class="school-results-section"><h3>Результаты команды</h3>${s.results.length?s.results.map(r=>`<article><span>${safe(r.season)} · ${safe(r.league)}</span><h4>${safe(r.award)}</h4><p>${safe(r.stage)} · ${safe(r.team)}${r.team_id?' · team '+safe(r.team_id):''}</p><p class="school-result-limit">${safe(r.limit)}</p><a href="${safe(r.source)}" target="_blank" rel="noopener">${safe(provenance[r.provenance])} ↗</a></article>`).join(''):'<p>В этом проходе награды не установлены. Наличие занятий или лаборатории не доказывает победу.</p>'}</section><section class="school-source-list"><h3>Источники и что они подтверждают</h3>${s.sources.map(x=>`<article><a href="${safe(x.url)}" target="_blank" rel="noopener">${safe(x.title)} ↗</a><p>${safe(x.claim)}</p><small>${safe(sourceKind[x.kind]||x.kind)} · проверено ${x.checked}</small></article>`).join('')}</section><section class="school-open-questions"><h3>Проверить перед выбором</h3><ul>${s.questions.map(x=>`<li>${safe(x)}</li>`).join('')}</ul><p>${safe(s.verification)}</p></section>`;
    const dialog=q('#school-dialog');dialog.showModal();dialog.scrollTop=0;
  }
  window.openAtlasSchool = open;
  document.addEventListener('input',event=>{const el=event.target;if(el.dataset.schoolFilter==='query'){filters.query=el.value;render();}});
  document.addEventListener('change',event=>{const el=event.target;if(el.dataset.schoolFilter){filters[el.dataset.schoolFilter]=el.value;if(['country','region'].includes(el.dataset.schoolFilter)){territory=[];territoryLabel='';}render();}});
  document.addEventListener('click',event=>{
    const b=event.target.closest('button');if(!b)return;
    if(b.dataset.schoolOpen)open(b.dataset.schoolOpen);
    if(b.dataset.schoolCompare){const id=b.dataset.schoolCompare;if(selected.has(id))selected.delete(id);else if(selected.size<3)selected.add(id);else{window.notify('Выберите до трёх школ для сравнения.');return;}render();}
    if(b.hasAttribute('data-school-compare-clear')){selected.clear();render();}
    if(b.hasAttribute('data-school-reset')){territory=[];territoryLabel='';Object.keys(filters).forEach(k=>filters[k]='');render();}
    if(b.dataset.schoolPreset){territory=[];territoryLabel='';Object.keys(filters).forEach(k=>filters[k]='');if(b.dataset.schoolPreset==='world')filters.evidence='world_result';if(b.dataset.schoolPreset==='boarding')filters.boarding='yes';render();q('#school-filters').scrollIntoView({behavior:'smooth',block:'start'});}
  });
  window.renderSchools=render;
})();
