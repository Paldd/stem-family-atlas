'use strict';
(() => {
  const fields=['query','country','theme','format','child','phase','language','month','sort'];
  const searchCache=new WeakMap();
  const number=v=>v!==''&&v!=null&&Number.isFinite(Number(v))&&Number(v)>=0?Number(v):null;
  const money=(n,currency)=>new Intl.NumberFormat('es',{style:'currency',currency,maximumFractionDigits:2}).format(n);
  function today(){const parts=new Intl.DateTimeFormat('en-US',{timeZone:'America/Costa_Rica',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date());const get=k=>parts.find(p=>p.type===k).value;return `${get('year')}-${get('month')}-${get('day')}`;}
  function periods(p){return (p.sessions||p.timing?.sessions||[]).filter(s=>Array.isArray(s)&&/^\d{4}-\d{2}-\d{2}$/.test(s[0])&&/^\d{4}-\d{2}-\d{2}$/.test(s[1]));}
  function matchesMonth(p,month){if(!month)return true;if(!/^\d{4}-(0[1-9]|1[0-2])$/.test(month))return false;const first=month+'-01';const end=new Date(Date.UTC(Number(month.slice(0,4)),Number(month.slice(5,7)),0)).toISOString().slice(0,10);return periods(p).some(([s,e])=>s<=end&&e>=first);}
  function nextDate(p,day=today()){const dates=periods(p).filter(([,end])=>end>=day).map(([start])=>start<day?day:start);return dates.sort()[0]||'9999-12-31';}
  function searchText(p){if(!searchCache.has(p))searchCache.set(p,foldSearch(JSON.stringify(p)));return searchCache.get(p);}
  function sortProfiles(profiles,sort,child,day=today()){
    const a=profiles.slice();const value={candidate:2,conditional:1,later:0,unknown:0,not_eligible:-1};
    const fit=p=>{const ks=child==='matvey'||child==='oscar'?[child]:['matvey','oscar'];return Math.min(...ks.map(k=>value[p.family_fit?.[k]?.status]??0));};
    if(sort==='name')return a.sort((p,q)=>p.provider.localeCompare(q.provider,'es'));
    if(sort==='age')return a.sort((p,q)=>fit(q)-fit(p)||nextDate(p,day).localeCompare(nextDate(q,day)));
    if(sort==='upcoming')return a.sort((p,q)=>nextDate(p,day).localeCompare(nextDate(q,day)));
    return a;
  }
  function filterURL(href,state){const u=new URL(href);u.searchParams.delete('camp');for(const k of fields){u.searchParams.delete('camp_'+k);if(state[k]&&!(k==='sort'&&state[k]==='upcoming'))u.searchParams.set('camp_'+k,state[k]);}u.hash='camps';return u.href;}
  function readFilters(href,profiles,themes,formats){const p=new URL(href).searchParams;const out={};const allowed={country:new Set(profiles.map(p=>p.iso)),theme:new Set(Object.keys(themes)),format:new Set(Object.keys(formats)),child:new Set(['both','matvey','oscar']),phase:new Set(['2027','published_2026','partial_2026','next_unannounced','archive_next_unannounced']),language:new Set(['EN','ES','RU','EN-support']),sort:new Set(['upcoming','age','name','listed'])};for(const k of fields){const v=p.get('camp_'+k);if(v==null)continue;if(k==='query')out[k]=v.slice(0,200);else if(k==='month'&&/^(2026|2027)-(0[1-9]|1[0-2])$/.test(v))out[k]=v;else if(allowed[k]?.has(v))out[k]=v;}return out;}
  function estimate(offer,inputs={},selected=[]){
    const lines=[];const missing=[];const rejected=[];const add=(label,amount,kind)=>lines.push({label,amount:Math.round(amount*100)/100,kind});
    for(const [k,base] of Object.entries(offer.base_by_child))add((k==='matvey'?"Matvey":"Oscar")+" · el precio base",base,'published');
    if(offer.discount_second)add("descuento al segundo hijo en el precio básico",-offer.base_by_child.oscar*offer.discount_second,'published');
    for(const c of offer.required)add(c.label,c.amount,'published');
    for(const c of offer.unknown_required){
      if(c.unit==='matvey_age'){const amount=c.rates[String(inputs.matvey_age)];if(amount==null)missing.push(c.label+" Seleccione la edad de Matvey para el inicio");else add(c.label,amount,'published');}
      else {const v=number(inputs[c.id]);if(v==null||v<c.min||(c.unit==='child_days'&&!Number.isInteger(v)))missing.push(c.label);else add(c.label,v*c.rate,c.unit==='child_days'?'published':'entered');}
    }
    for(const c of offer.optional){if(!selected.includes(c.id))continue;const age=number(inputs.matvey_age);if(c.min_matvey_age&&(age==null||age<c.min_matvey_age)){rejected.push(c.label+" Necesita una edad confirmada "+c.min_matvey_age+'+');continue;}add(c.label,c.amount,'published');}
    for(const k of offer.unknown_trip){const value=number(inputs[k]);if(value==null)missing.push({travel:"vuelo y transporte local",lodging:"vivienda y gastos de los padres",misc:"Otras opciones, dinero en el bolsillo y gastos"}[k]);else add({travel:"su evaluación · vuelo y transporte",lodging:"su evaluación de la vivienda de sus padres",misc:"su evaluación · otros gastos"}[k],value,'entered');}
    const published=lines.filter(l=>l.kind==='published').reduce((s,l)=>s+l.amount,0);const entered=lines.filter(l=>l.kind==='entered').reduce((s,l)=>s+l.amount,0);
    return {lines,published:Math.round(published*100)/100,entered:Math.round(entered*100)/100,total:Math.round((published+entered)*100)/100,missing,rejected,complete:false};
  }
  const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function mountBudget(root,data,openCamp){
    if(!data?.offers?.length)return null;
    const panel=document.createElement('details');panel.className='cp-budget';panel.id='cp-family-budget';
    panel.innerHTML=`<summary>la estimación de Matvey y Oscar · ${data.offers.length} de los escenarios verificados</summary><div class="cp-budget-inner"><p>El precio del campamento, los pagos adicionales obligatorios y los gastos de viaje se muestran por separado.</p><label class="cp-budget-picker">programa y formato<select data-budget-offer>${data.offers.map(o=>`<option value="${esc(o.id)}">${esc(o.label)}</option>`).join('')}</select></label><div data-budget-form></div><div data-budget-output role="status" aria-live="polite" aria-atomic="true"></div></div>`;
    const inputs={},selected=new Set();let offer=data.offers[0],replacingForm=false;
    const renderOutput=()=>{
      panel.querySelectorAll('[data-budget-value]').forEach(el=>{inputs[el.dataset.budgetValue]=el.value;});
      panel.querySelectorAll('[data-budget-option]').forEach(el=>{const c=offer.optional.find(c=>c.id===el.dataset.budgetOption);const a=number(inputs.matvey_age);el.disabled=!!(c.min_matvey_age&&(a==null||a<c.min_matvey_age));if(el.disabled)el.checked=false;el.checked?selected.add(c.id):selected.delete(c.id);});
      const v=estimate(offer,inputs,[...selected]);
      panel.querySelector('[data-budget-output]').innerHTML=`<div class="cp-budget-totals"><div><span>los componentes publicados</span><strong>${esc((offer.price_basis==='from'?"desde ":'')+money(v.published,offer.currency))}</strong></div><div><span>con el gasto introducido</span><strong>${esc((offer.price_basis==='from'?"desde ":'')+money(v.total,offer.currency))}</strong></div></div><ul class="cp-budget-breakdown">${v.lines.map(l=>`<li><span>${esc(l.label)}${l.kind==='entered'?" · introducido por usted":''}</span><b>${esc(money(l.amount,offer.currency))}</b></li>`).join('')}</ul>${v.missing.length?`<p class="cp-budget-gap">No se ha tenido en cuenta: ${v.missing.map(esc).join('; ')}.</p>`:''}<p>El resultado se mantiene preliminar: la entrada, el lugar y la factura final se confirman por separado.</p>`;
    };
    const renderForm=()=>{
      replacingForm=true;try {
      selected.clear();for(const k of Object.keys(inputs))delete inputs[k];
      const needsAge=offer.unknown_required.some(c=>c.unit==='matvey_age')||offer.optional.some(c=>c.min_matvey_age);
      const numeric=offer.unknown_required.filter(c=>c.unit!=='matvey_age');
      panel.querySelector('[data-budget-form]').innerHTML=`<p class="cp-budget-dates"><b>${offer.period_type==='season_window'?"ventana de temporada · semana en concreto para elegir:":"los períodos para este tipo de tarifa:"}</b> ${offer.sessions.map(s=>s.map(v=>esc(v.split('-').reverse().join('.'))).join('–')).join('; ')}. Confirmar disponibilidad de plazas por separado.</p><p class="cp-budget-gate">${esc(offer.gate)}</p>${offer.scope?`<p class="cp-budget-scope">${esc(offer.scope)}</p>`:''}<p><b>Incluido:</b> ${esc(offer.included)}</p><div class="cp-budget-inputs">${needsAge?"<label>Matvey edad en el primer día<select data-budget-value=\"matvey_age\"><option value=\"\">Seleccione su edad</option><option value=\"9\">9 años</option><option value=\"10\">10 años</option></select></label>":''}${numeric.map(c=>`<label>${esc(c.label)}${c.unit==='child_days'?"<small>Por ejemplo, 14 + 14 = 28. el número de días pagados, confirme en la factura.</small>":`<small>el importe de la ${esc(offer.currency)} por el revestimiento / cuota elegido.</small>`}<input type="number" inputmode="decimal" min="${c.min}" step="${c.unit==='child_days'?'1':'0.01'}" data-budget-value="${esc(c.id)}" placeholder="no se ha establecido"></label>`).join('')}${[['travel',"vuelo y transporte local"],['lodging',"vivienda y gastos de los padres"],['misc',"otras opciones y gastos"]].map(([k,t])=>`<label>${t} · ${esc(offer.currency)}<input type="number" inputmode="decimal" min="0" step="0.01" data-budget-value="${k}" placeholder="su evaluación"></label>`).join('')}</div>${offer.optional.length?`<fieldset class="cp-budget-options"><legend>opciones adicionales</legend>${offer.optional.map(c=>`<label><input type="checkbox" data-budget-option="${esc(c.id)}">${esc(c.label)} · ${esc(money(c.amount,offer.currency))}${c.min_matvey_age?`<small>sólo disponible después ${c.min_matvey_age}- Es el aniversario de Matvey.</small>`:''}</label>`).join('')}</fieldset>`:''}<p class="cp-budget-contract">${esc(offer.deposit_note)}</p><div class="cp-budget-sources">${offer.sources.map((url,i)=>`<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">fuente oficial ${i+1}</a>`).join('')}<button type="button" data-budget-camp>el archivo completo del campamento</button></div>`;
      } finally {replacingForm=false;}
      renderOutput();
    };
    // Replacing focused fields can synchronously dispatch their pending change.
    // Those events belong to the previous offer and must not use the new one.
    panel.addEventListener('input',e=>{if(!replacingForm&&e.target.dataset.budgetValue)renderOutput();});
    panel.addEventListener('change',e=>{if(replacingForm)return;if(e.target.hasAttribute('data-budget-offer')){offer=data.offers.find(o=>o.id===e.target.value);renderForm();}else if(e.target.dataset.budgetValue||e.target.dataset.budgetOption)renderOutput();});
    panel.addEventListener('click',e=>{if(e.target.closest('[data-budget-camp]'))openCamp(offer.slug);});
    renderForm();
    return {panel,open(slug,month){const a=data.offers.filter(o=>o.slug===slug);offer=a.find(o=>matchesMonth(o,month))||a[0];if(!offer)return;panel.querySelector('[data-budget-offer]').value=offer.id;renderForm();panel.open=true;panel.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});panel.querySelector('[data-budget-offer]').focus({preventScroll:true});}};
  }
  window.STEM_CAMP_PLANNER={today,periods,matchesMonth,nextDate,searchText,sortProfiles,filterURL,readFilters,estimate,mountBudget};
})();
