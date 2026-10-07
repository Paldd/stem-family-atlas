'use strict';
// Themes come from structured catalogue tags. Colour never expresses admission or ranking.
window.STEM_DIRECTIONS = (() => {
 const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const groups = [
  {id:'robotics',label:'Робототехника',icon:'⚙',color:'#1d4ed8',tint:'#eff6ff',tags:['robotics']},
  {id:'ai',label:'Искусственный интеллект',icon:'✦',color:'#6d28d9',tint:'#f5f3ff',tags:['ai']},
  {id:'coding',label:'Программирование',shortLabel:'Код и программы',icon:'</>',color:'#0f766e',tint:'#f0fdfa',tags:['coding']},
  {id:'science',label:'Наука и инженерия',icon:'◉',color:'#15803d',tint:'#f0fdf4',tags:['science','engineering','maths']},
  {id:'technology',label:'Технологии и maker',icon:'◇',color:'#92400e',tint:'#fffbeb',tags:['technology','makers','stem','electronics']},
  {id:'games',label:'Игры и геймдизайн',icon:'◈',color:'#0e7490',tint:'#ecfeff',tags:['games','chess']},
  {id:'languages',label:'Языки',icon:'文',color:'#9a3412',tint:'#fff7ed',tags:['languages','language']},
  {id:'art',label:'Искусство и дизайн',icon:'✎',color:'#a21caf',tint:'#fdf4ff',tags:['art','arts','music','design']},
  {id:'sport',label:'Спорт',icon:'⚑',color:'#be123c',tint:'#fff1f2',tags:['sport']},
  {id:'nature',label:'Природа и приключения',icon:'❋',color:'#365314',tint:'#f7fee7',tags:['nature','adventure','outdoor']},
  {id:'entrepreneurship',label:'Бизнес и лидерство',icon:'↗',color:'#854d0e',tint:'#fefce8',tags:['entrepreneurship','business','leadership']},
  {id:'culture',label:'Культура',icon:'◎',color:'#4338ca',tint:'#eef2ff',tags:['culture']},
  {id:'general',label:'Общий отдых',icon:'☀',color:'#475569',tint:'#f1f5f9',tags:['general']}
 ];
 const fallback = {id:'unclassified',label:'Тема уточняется',icon:'·',color:'#475569',tint:'#f1f5f9',tags:[]};
 const byTag = new Map(groups.flatMap(g => g.tags.map(t => [t,g])));
 const labels = Object.fromEntries(groups.flatMap(g => g.tags.map(t => [t,g.label])));
 Object.assign(labels,{engineering:'Инженерия',maths:'Математика',science:'Наука и эксперименты',makers:'Maker / создание вещей',stem:'STEM / STEAM',electronics:'Электроника',music:'Музыка',design:'Дизайн',chess:'Шахматы',adventure:'Приключения',outdoor:'Активный отдых',entrepreneurship:'Предпринимательство',business:'Бизнес',leadership:'Лидерство'});
 const directions = tags => groups.filter(g => (tags || []).some(t => g.tags.includes(t)));
 const primary = tags => directions(tags)[0] || fallback;
 const attributes = tags => {const g = primary(tags);return `data-direction="${g.id}" style="--direction:${g.color};--direction-tint:${g.tint}"`;};
 const chip = g => `<span class="direction-chip" style="--direction:${g.color};--direction-tint:${g.tint}"><span class="direction-icon" aria-hidden="true">${escape(g.icon)}</span>${escape(g.label)}</span>`;
 const chips = tags => {const selected=directions(tags);return `<div class="direction-chips" aria-label="Тематика программы">${(selected.length?selected:[fallback]).map(chip).join('')}</div>`;};
 const matches = (tags, selection) => !selection || (groups.find(g => g.id===selection)?.tags || [selection]).some(t => (tags || []).includes(t));
 const options = () => groups.map(g => `<option value="${g.id}">${escape(g.label)}</option>`).join('') + '<optgroup label="Точные темы">' + Object.entries(labels).filter(([tag]) => !groups.some(g=>g.id===tag)).map(([tag,label])=>`<option value="${tag}">${escape(label)} · точная тема</option>`).join('') + '</optgroup>';
 const legend = (scope, selected='') => `<details class="direction-legend" open><summary>Направления в цвете<span>Нажмите, чтобы выбрать тему</span></summary><p>Цвет обозначает тематику. Все темы смешанной программы указаны в карточке; цвет не означает рейтинг, язык или допуск ребёнка.</p><div class="direction-choices" role="group" aria-label="Выбрать направление"><button type="button" class="direction-choice direction-all" data-direction-scope="${scope}" data-direction-filter="" aria-pressed="${!selected}">Все направления</button>${groups.map(g => `<button type="button" class="direction-choice" data-direction-scope="${scope}" data-direction-filter="${g.id}" aria-label="${escape(g.label)}" title="${escape(g.label)}" aria-pressed="${selected===g.id}" style="--direction:${g.color};--direction-tint:${g.tint}"><span class="direction-icon" aria-hidden="true">${escape(g.icon)}</span>${escape(g.shortLabel||g.label)}</button>`).join('')}</div></details>`;
 const sync = (root, selected) => root?.querySelectorAll('[data-direction-filter]').forEach(button => button.setAttribute('aria-pressed',String(button.dataset.directionFilter===selected)));
 const kinds = {competition:['🏆','Соревнование'],event:['◈','Событие / выставка'],camp:['☀','Лагерь / обучение'],school:['▦','Школа / пансион']};
 const kind = id => {const k=kinds[id];return k?`<span class="atlas-kind atlas-kind-${id}"><span aria-hidden="true">${k[0]}</span>${k[1]}</span>`:'';};
 return {groups,labels,directions,primary,attributes,chips,matches,options,legend,sync,kind};
})();
