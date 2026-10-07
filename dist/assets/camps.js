'use strict';
const languageModeLabels={camp_life:'Основной язык лагерной жизни; язык каждого курса уточнить',primary:'Основной язык курса подтверждён',bilingual:'Билингвальный технический курс',materials:'Язык самостоятельных учебных материалов',support:'Помощь на втором языке',language_lessons:'Отдельные языковые уроки',unconfirmed:'Язык технического курса уточнить',unclassified:'Роль языка ещё не проверена'};
function campLanguageLabel(e){return e.materials_only?'Учебные материалы на '+(e.languages||[]).join(' / ')+' · самостоятельно':languageModeLabels[e.language_mode||'unclassified']}
function campLanguageBadge(e){return e.block==='Лагеря'?`<span class="camp-language ${['primary','bilingual','materials'].includes(e.language_mode)?'confirmed':''}">${esc(campLanguageLabel(e))}</span>`:''}
function campLanguageDetail(e){return e.language_mode?`<span class="language-detail">${esc(campLanguageLabel(e))}${e.support_languages?.length?' · '+esc(e.support_languages.join(' / ')):''}</span>`:''}
function drawCamps(a){
 const f=DATA.camp_focus,c=f.counts;
 $('#camp-verdict').textContent=f.conclusion;
 $('#camp-stats').innerHTML=[['records',c.records,'карточки программ'],['boarding',c.boarding,'вариантов с проживанием'],['instruction',c.family_instruction,'EN / ES / RU как язык курса*'],['support',c.family_support,'с прямой EN / ES / RU помощью*']].map(([key,n,label])=>`<div class="camp-stat"><strong>${n}</strong><span>${esc(label)}</span></div>`).join('');
 $('#camp-summary').textContent=`${a.length} показано с вашими фильтрами · ${c.regular} регулярных программ в общей базе. *Язык подробно проверен у части записей; RU-курсов с прямым доказательством преподавания пока ${c.ru_instruction}. Русский сайт не подтверждает язык занятия.`;
 $('#camp-routes').innerHTML=f.routes.map(r=>`<article class="camp-route"><h3>${esc(r.name)}</h3><p>${esc(r.detail)}</p><div class="camp-route-links">${r.ids.map(id=>{const e=EVENTS.find(x=>x.id===id);return e?`<button class="text-button" data-open="${esc(id)}">${esc(e.provider||shortTitles[e.id]||e.title)} · ${esc(id)} ${icon('arrow')}</button>`:''}).join('')}</div></article>`).join('');
 $('#camp-gaps').innerHTML=f.gaps.map(s=>`<li>${esc(s)}</li>`).join('');
 $('#camp-cards').innerHTML=a.length?a.map(card).join(''):empty();
 $('#camp-results-heading').textContent=`Программы по вашим условиям · ${a.length}`;
}
document.addEventListener('click',event=>{
 const button=event.target.closest('[data-camp-preset]');if(!button)return;
 const preset=button.dataset.campPreset;
 if(preset==='projects'){
   reset();setView('catalog');state.campProjects=true;state.block='Соревнования';render();
   $('#catalog-view').scrollIntoView({behavior:'smooth',block:'start'});return;
 }
 reset();setView('camps');
 if(preset==='boarding')state.participation='boarding';
 if(preset==='day')state.participation='day_camp';
 if(preset==='english')Object.assign(state,{language:'EN',languageMode:'instruction'});
 if(preset==='spanish')Object.assign(state,{language:'ES',languageMode:'instruction'});
 if(preset==='russian')Object.assign(state,{language:'RU',languageMode:'instruction'});
 if(preset==='support')state.languageMode='support';
 render();$('#camp-cards').scrollIntoView({behavior:'smooth',block:'start'});
});
