'use strict';
const languageModeLabels={camp_life:"la lengua principal de la vida campestre; el idioma de cada curso",primary:"el idioma principal del curso está confirmado",bilingual:"curso técnico bilingüe",materials:"lengua de los materiales de enseñanza independientes",support:"ayuda en otro idioma",language_lessons:"las clases de idiomas individuales",unconfirmed:"Idioma del curso técnico por confirmar",unclassified:"El papel del idioma aún no se ha comprobado."};
function campLanguageLabel(e){return e.materials_only?"de los materiales de enseñanza de "+(e.languages||[]).join(' / ')+" · por su cuenta":languageModeLabels[e.language_mode||'unclassified']}
function campLanguageBadge(e){return e.block==="Campamentos"?`<span class="camp-language ${['primary','bilingual','materials'].includes(e.language_mode)?'confirmed':''}">${esc(campLanguageLabel(e))}</span>`:''}
function campLanguageDetail(e){return e.language_mode?`<span class="language-detail">${esc(campLanguageLabel(e))}${e.support_languages?.length?' · '+esc(e.support_languages.join(' / ')):''}</span>`:''}
function drawCamps(a){
 const f=DATA.camp_focus,c=f.counts;
 $('#camp-verdict').textContent=f.conclusion;
 $('#camp-stats').innerHTML=[['records',c.records,"las tarjetas de los programas"],['boarding',c.boarding,"Opciones de residencia"],['instruction',c.family_instruction,"EN / ES / RU como lengua del curso*"],['support',c.family_support,"con la ayuda directa de EN / ES / RU*"]].map(([key,n,label])=>`<div class="camp-stat"><strong>${n}</strong><span>${esc(label)}</span></div>`).join('');
 $('#camp-summary').textContent=`${a.length} mostrado con sus filtros ${c.regular} *La lengua está detallada en la parte de las inscripciones; los cursos de RU con prueba directa de enseñanza hasta el momento ${c.ru_instruction}. el sitio web ruso no confirma el idioma del curso.`;
 $('#camp-routes').innerHTML=f.routes.map(r=>`<article class="camp-route"><h3>${esc(r.name)}</h3><p>${esc(r.detail)}</p><div class="camp-route-links">${r.ids.map(id=>{const e=EVENTS.find(x=>x.id===id);return e?`<button class="text-button" data-open="${esc(id)}">${esc(e.provider||shortTitles[e.id]||e.title)} · ${esc(id)} ${icon('arrow')}</button>`:''}).join('')}</div></article>`).join('');
 $('#camp-gaps').innerHTML=f.gaps.map(s=>`<li>${esc(s)}</li>`).join('');
 $('#camp-cards').innerHTML=a.length?a.map(card).join(''):empty();
 $('#camp-results-heading').textContent=`programas según sus condiciones ${a.length}`;
}
document.addEventListener('click',event=>{
 const button=event.target.closest('[data-camp-preset]');if(!button)return;
 const preset=button.dataset.campPreset;
 if(preset==='projects'){
   reset();setView('catalog');state.campProjects=true;state.block="Competiciones";render();
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
