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
  const types = {public:"de la Comisión",private:"Privado",private_industry:"red privada de la industria"};
  const tiers = {world_result:"Hay un resultado mundial.",national_result:"hay un resultado nacional",other_result:"hay un resultado competitivo",programme:"programa · no se han establecido victorias"};
  const fitNames = {candidate:"candidato a la etapa diurna",future:"futuro secundario",unknown:"edad / entrada de la página"};
  const ibNames = {candidate:'candidate',authorized_registry:"autorizado · registro IB",school_report:"por el mensaje de la escuela",school_report_authorized:"la autorización por el mensaje de la escuela"};
  const provenance = {organizer_report:"mensaje del organizador",organizer_protocol:"el protocolo oficial del organizador",school_report:"mensaje de la escuela",school_operator_report:"comunicación de la red escolar / operador"};
  const sourceKind = {school:"escuela",public_school:"escuela pública",registry:"el manual oficial",organizer:"organizador de la competencia",school_operator:"red escolar / operador",historical_registry:"lista histórica del Estado",government:"el manual de información",school_team:"equipo escolar",regional_organizer:"organizador regional"};
  const q = sel => document.querySelector(sel);
  const safe = x => String(x ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const ibText = s => s.ib_programmes.length ? s.ib_programmes.map(x=>x.programme+' · '+ibNames[x.status]).join('; ') : "IB no ha sido confirmado";
  const options = (items,label) => `<option value="">${label}</option>`+items.map(([v,t])=>`<option value="${safe(v)}">${safe(t)}</option>`).join('');
  const field = (key,label,items,all) => `<label>${label}<select data-school-filter="${key}" aria-label="${label}">${options(items,all)}</select></label>`;
  function matched(s) {
    if(territory.length && !territory.includes(s.iso)) return false;
    const pick=window.bestPickFor('school',s.id);
    if(filters.best&&(!pick||(filters.best!=='all'&&pick.horizon!==filters.best)))return false;
    if(filters.query && !foldSearch(JSON.stringify(s)).includes(foldSearch(filters.query))) return false;
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
  const chip = (s,k,name) => `<span class="school-fit ${s.fit[k]}">${name} · ${s.fit[k]==='candidate'?"candidato diurno":s.fit[k]==='future'?"más tarde":"aclarar"}</span>`;
  function card(s) {
    const r = s.results[0];
    return `<article class="school-card" data-school-id="${s.id}"><div class="school-card-top ${s.evidence}"><span>${safe(s.country)}</span><span class="school-number">${s.id}</span><div class="school-campus-mark" aria-hidden="true">▥<span>⚙</span></div><p>${safe(types[s.school_type])}</p></div><div class="school-card-body"><span class="school-place">${safe(s.city)}</span><h3>${safe(s.name)}</h3>${window.bestBadge('school',s.id)}${window.STEM_DIRECTIONS.kind('school')}<span class="school-evidence ${s.evidence}">${safe(tiers[s.evidence])}</span><p class="school-result">${r?safe(r.season+' · '+r.league+' · '+r.award):"Las clases / programas STEM confirmadas. Las victorias requieren una verificación."}</p><div class="school-kids">${chip(s,'mat',"Matvey")}${chip(s,'osc',"Oscar")}</div><p class="school-card-note">${safe(s.ages)}</p><div class="school-card-tags"><span>${s.instruction_languages.length?"Idioma: "+s.instruction_languages.join(' / ')+" · escalón en el archivo":"Idioma de enseñanza por confirmar"}</span><span>${s.boarding==='yes'?"pensión · edad por separado":s.boarding==='no'?'Day school':"no se ha establecido el pensión"}</span></div><div class="school-card-actions"><button class="button secondary" data-school-open="${s.id}">Dossier ↗</button><button class="school-compare-button" data-school-compare="${s.id}" aria-pressed="${selected.has(s.id)}">${selected.has(s.id)?"✓ Seleccionado":"＋ Comparar"}</button></div></div></article>`;
  }
  function renderComparison() {
    const node=q('#school-comparison');
    if(!selected.size) {node.hidden=true;node.innerHTML='';return;}
    const a=schools.filter(s=>selected.has(s.id));
    const rows=[["País / tipo",s=>s.country+' · '+types[s.school_type]],["Matvey / Oscar",s=>fitNames[s.fit.mat]+' / '+fitNames[s.fit.osc]],["Resultado",s=>s.results.map(r=>r.season+' · '+r.league+' · '+r.stage+' · '+r.award).join('; ')||"No se ha establecido la victoria"],["fuente de resultados",s=>s.results.map(r=>provenance[r.provenance]).join('; ')||"programa de la escuela"],["lengua / escalón",s=>s.language_note],['IB',ibText],["Programa residencial",s=>s.boarding_note],["Admisión",s=>s.admissions],["Precio",s=>s.cost]];
    node.hidden=false;node.innerHTML=`<div class="school-comparison-title"><h3>comparar ${a.length} de 3</h3><button class="text-button" data-school-compare-clear>Borrar</button></div><div class="school-table-scroll" tabindex="0" aria-label="Comparación de las escuelas, recorra la tabla"><table><caption class="sr-only">comparación de las escuelas seleccionadas</caption><thead><tr><th scope="col">la verificación</th>${a.map(s=>`<th scope="col">${safe(s.name)}<button data-school-compare="${s.id}" aria-label="Quitar ${safe(s.name)} de la comparación">quitar ×</button></th>`).join('')}</tr></thead><tbody>${rows.map(([title,fn])=>`<tr><th scope="row">${title}</th>${a.map(s=>`<td>${safe(fn(s))}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  }
  function render() {
    if(!focus || !q('#schools-view')) return;
    if(!initialized) {
      const countries=[...new Map(schools.map(s=>[s.iso,s.country])).entries()].sort((a,b)=>a[1].localeCompare(b[1],'es'));
      const regions=[...new Set(schools.map(s=>s.region))].sort().map(x=>[x,x]);
      q('#school-filters').innerHTML=`<label class="school-search">nombre, ciudad, liga<input type="search" data-school-filter="query" placeholder="TAS, IB, robotics, México…" aria-label="Buscar escuelas"></label>`+
        field('country',"país de la escuela",countries,`Todos ${countries.length} de los países investigados`)+field('region',"región de la escuela",regions,"todas las regiones")+
        field('best',"la selección de la redacción",[['all',"Todas las recomendaciones"],['now',"Considerar ahora"],['future',"futuras orientaciones"]],"toda la lista de la escuela")+field('type',"tipo de escuela",[['public',"de la Comisión"],['private',"red privada / industrial"]],"todos los tipos")+
        field('fit',"horizonte de edad",[['both',"los candidatos diarios para ambos"],['mat',"Matvey · candidato diurno"],['osc',"Oscar · candidato diurno"],['future',"futuro secundario"]],"Todos los niveles")+
        field('language',"lengua confirmada · escalón en el archivo",[['EN',"English · en el nivel indicado"],['ES',"Español · en el nivel indicado"],['RU',"ruso · en el nivel indicado"]],"cualquier / especificar")+
        field('ib',"Programa IB",[['any',"cualquier marca IB"],['registry',"se ha leído la autorización en el registro IB"],['candidate',"Hay un programa de candidato."]],"cualquier programa")+
        field('boarding',"Internado del colegio",[['yes',"hay un pensión · edad por separado"],['no',"día de escuela confirmada"],['unknown',"no se ha establecido el pensión"]],"Cualquier modalidad")+
        field('evidence',"prueba del resultado",Object.entries(tiers).concat([['organizer',"hay un protocolo del organizador"]]),"todos los niveles de pruebas");
      q('#school-stats').innerHTML=`<div><strong>${schools.length}</strong><span>escuelas · lista investigada</span></div><div><strong>${focus.counts.countries}</strong><span>de los países · 6 continentes</span></div><button data-school-preset="world"><strong>${focus.counts.world_result}</strong><span>escuelas con resultados mundiales</span></button><button data-school-preset="boarding"><strong>${focus.counts.boarding}</strong><span>Pension · edad en el archivo</span></button>`;
      q('#school-routes').innerHTML=focus.routes.map((r,i)=>`<article><span class="school-route-step">0${i+1}</span><h3>${safe(r.name)}</h3><p>${safe(r.detail)}</p><div>${r.ids.map(id=>`<button data-school-open="${id}">${safe(schools.find(s=>s.id===id).name)} ↗</button>`).join('')}</div></article>`).join('');
      q('#school-method').innerHTML=focus.methodology.map(x=>`<li>${safe(x)}</li>`).join('');
      q('#school-gaps').innerHTML=focus.gaps.map(x=>`<li>${safe(x)}</li>`).join('');
      q('#school-coverage').textContent=`las escuelas se han investigado parcialmente en ${focus.counts.countries} de ${window.STEM_DATA.countries.length} de los países y territorios. ${window.STEM_DATA.countries.length-focus.counts.countries} No tengo tarjetas de escuela.. de los países totalmente auditados: 0.`;
      initialized=true;
    }
    q('#school-filters').querySelectorAll('[data-school-filter]').forEach(x=>{if(x.value!==filters[x.dataset.schoolFilter])x.value=filters[x.dataset.schoolFilter];});
    const a=schools.filter(matched);
    q('#school-count').textContent=`Se muestran ${a.length} de ${schools.length} colegios.${territory.length ? " el territorio de la pista: "+territoryLabel+". Restablecer elimina esta restricción." : ''} candidato significa la etapa de la escuela encontrada; la clase, la lengua del equipo, la selección y el lugar requieren confirmación.`;
    q('#school-cards').innerHTML=a.length?a.map(card).join(''):`<div class="school-empty"><h3>no están en la lista de investigación</h3><p>Es un vacío en el paseo actual, no una prueba de ausencia de escuelas.</p><button class="button secondary" data-school-reset>Restablecer filtros</button></div>`;
    renderComparison();
    window.renderSchoolHistory?.();
  }
  function open(id) {
    const s=schools.find(x=>x.id===id); if(!s)return;
    const part=(title,value)=>`<section><h3>${title}</h3><p>${safe(value)}</p></section>`;
    q('#school-dialog-content').innerHTML=`<p class="section-kicker">${safe(s.country)} · ${safe(types[s.school_type])} · ${s.id}</p><h2>${safe(s.name)}</h2><p class="school-dialog-location">${safe(s.city)} · verificado ${s.checked}</p><span class="school-evidence ${s.evidence}">${safe(tiers[s.evidence])}</span><p class="school-dossier-intro">${safe(s.curriculum)}</p><div class="school-kids">${chip(s,'mat',"Matvey")}${chip(s,'osc',"Oscar")}</div><div class="school-dossier-grid">${part("edad y clase",s.ages+' '+s.fit.note)}${part("Idioma de enseñanza",s.language_note)}${part("Residencial / de día",s.boarding_note)}${part("IB y el programa",ibText(s))}${part("robótica y equipo",s.programme)}${part("laboratorios y equipos",s.labs)}${part("y programación",s.ai)}${part("Cómo solicitar admisión",s.admissions)}${part("el costo · año es importante",s.cost)}</div><section class="school-results-section"><h3>resultados del equipo</h3>${s.results.length?s.results.map(r=>`<article><span>${safe(r.season)} · ${safe(r.league)}</span><h4>${safe(r.award)}</h4><p>${safe(r.stage)} · ${safe(r.team)}${r.team_id?' · team '+safe(r.team_id):''}</p><p class="school-result-limit">${safe(r.limit)}</p><a href="${safe(r.source)}" target="_blank" rel="noopener">${safe(provenance[r.provenance])} ↗</a></article>`).join(''):"<p>No hay premios en este pase. La presencia de clases o laboratorios no prueba la victoria.</p>"}</section><section class="school-source-list"><h3>las fuentes y lo que confirman</h3>${s.sources.map(x=>`<article><a href="${safe(x.url)}" target="_blank" rel="noopener">${safe(x.title)} ↗</a><p>${safe(x.claim)}</p><small>${safe(sourceKind[x.kind]||x.kind)} · verificado ${x.checked}</small></article>`).join('')}</section><section class="school-open-questions"><h3>comprobar antes de elegir</h3><ul>${s.questions.map(x=>`<li>${safe(x)}</li>`).join('')}</ul><p>${safe(s.verification)}</p></section>`;
    const dialog=q('#school-dialog');dialog.showModal();dialog.scrollTop=0;
  }
  window.openAtlasSchool = open;
  document.addEventListener('input',event=>{const el=event.target;if(el.dataset.schoolFilter==='query'){filters.query=el.value;render();}});
  document.addEventListener('change',event=>{const el=event.target;if(el.dataset.schoolFilter){filters[el.dataset.schoolFilter]=el.value;if(['country','region'].includes(el.dataset.schoolFilter)){territory=[];territoryLabel='';}render();}});
  document.addEventListener('click',event=>{
    const b=event.target.closest('button');if(!b)return;
    if(b.dataset.schoolOpen)open(b.dataset.schoolOpen);
    if(b.dataset.schoolCompare){const id=b.dataset.schoolCompare;if(selected.has(id))selected.delete(id);else if(selected.size<3)selected.add(id);else{window.notify("elige hasta tres escuelas para la comparación.");return;}render();}
    if(b.hasAttribute('data-school-compare-clear')){selected.clear();render();}
    if(b.hasAttribute('data-school-reset')){territory=[];territoryLabel='';Object.keys(filters).forEach(k=>filters[k]='');render();}
    if(b.dataset.schoolPreset){territory=[];territoryLabel='';Object.keys(filters).forEach(k=>filters[k]='');if(b.dataset.schoolPreset==='world')filters.evidence='world_result';if(b.dataset.schoolPreset==='boarding')filters.boarding='yes';render();q('#school-filters').scrollIntoView({behavior:'smooth',block:'start'});}
  });
  window.renderSchools=render;
})();
