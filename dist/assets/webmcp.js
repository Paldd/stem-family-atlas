'use strict';
(function registerStemTools(){
 const context=document.modelContext;if(!context?.registerTool)return;
 const lifetime=new AbortController();window.addEventListener('pagehide',()=>lifetime.abort(),{once:true});
 const known=new Set(EVENTS.map(e=>e.id));
 const compact=e=>({id:e.id,title:e.title,country:e.country,start:e.start||null,end:e.end||null,date_status:e.date_status,deadline:e.deadline||null,matvey:e.mat,oscar:e.osc,source:e.source});
 const tools=[
  {name:'filter_stem_calendar',title:'Подобрать STEM-мероприятия',description:'Настроить видимые фильтры семейного календаря и показать совпадения. Не регистрирует семью на мероприятие.',inputSchema:{type:'object',properties:{query:{type:'string',maxLength:200},child:{type:'string',enum:['','mat','osc','both','conditional']},country_iso3:{type:'string'},block:{type:'string',enum:['','Соревнования','События','Лагеря']},dates:{type:'string',enum:['','confirmed','waiting','soon']}},additionalProperties:false},annotations:{readOnlyHint:false,untrustedContentHint:true},execute(input){
   if(!input||typeof input!=='object'||Array.isArray(input))throw Error('Expected an object');
   const allowed=['query','child','country_iso3','block','dates'];if(Object.keys(input).some(k=>!allowed.includes(k)))throw Error('Unknown filter');
   for(const v of Object.values(input))if(typeof v!=='string')throw Error('Filter values must be strings');
   if(input.query?.length>200)throw Error('Query is too long');
   if(input.child!==undefined&&!['','mat','osc','both','conditional'].includes(input.child))throw Error('Unknown child filter');
   if(input.block!==undefined&&!['','Соревнования','События','Лагеря'].includes(input.block))throw Error('Unknown block');
   if(input.dates!==undefined&&!['','confirmed','waiting','soon'].includes(input.dates))throw Error('Unknown date filter');
   if(input.country_iso3&&!COUNTRIES.some(c=>c.iso===input.country_iso3))throw Error('Unknown country ISO3');
   Object.assign(state,{query:input.query??'',kid:input.child??'',country:input.country_iso3??'',block:input.block??'',dates:input.dates??'',region:'',theme:'',language:'',languageMode:'',campProjects:false,scope:'',participation:'',priority:false,excluded:false,limit:12});setView('explore');const a=filtered();return {count:a.length,events:a.slice(0,20).map(compact),registration_changed:false};
  }},
  {name:'read_stem_event',title:'Прочитать условия мероприятия',description:'Получить дату, возрастные условия, команду, технику, путь входа и официальный источник одной карточки без изменения планов.',inputSchema:{type:'object',properties:{id:{type:'string'}},required:['id'],additionalProperties:false},annotations:{readOnlyHint:true,untrustedContentHint:true},execute(input){if(!input||Object.keys(input).some(k=>k!=='id')||!known.has(input.id))throw Error('Unknown event ID');const e=EVENTS.find(e=>e.id===input.id);return {...compact(e),age:e.age,team:e.format,gear:e.gear,language:e.language,language_role:e.language_mode||'unclassified',support_languages:e.support_languages||[],cost:e.cost,entry:e.entry,reward:e.reward,next_step:e.action,checked:e.checked,verification_limit:e.proof,note:e.note}}},
  {name:'save_stem_events_locally',title:'Добавить события в планы браузера',description:'Добавить или убрать карточки из избранного в этом браузере. Это идеи семьи, не регистрация, оплата или подтверждённая поездка.',inputSchema:{type:'object',properties:{ids:{type:'array',items:{type:'string'},minItems:1,maxItems:50},operation:{type:'string',enum:['add','remove']}},required:['ids','operation'],additionalProperties:false},annotations:{readOnlyHint:false,untrustedContentHint:false},execute(input){
   if(!input||Object.keys(input).some(k=>!['ids','operation'].includes(k))||!Array.isArray(input.ids)||!input.ids.length||input.ids.length>50||!['add','remove'].includes(input.operation)||input.ids.some(id=>!known.has(id)))throw Error('Invalid saved-event request');
   const next=new Set(favoriteIds);for(const id of input.ids)input.operation==='add'?next.add(id):next.delete(id);localStorage.setItem('stemAtlasFavorites.v1',JSON.stringify([...next]));favoriteIds=next;render();return {state:'saved_locally_in_this_browser',saved_ids:[...favoriteIds],registration_changed:false};
  }}
 ];
 for(const tool of tools){try{Promise.resolve(context.registerTool(tool,{signal:lifetime.signal})).catch(()=>{})}catch{}}
})();
