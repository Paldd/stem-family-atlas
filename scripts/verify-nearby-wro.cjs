/* Run the shipped league/history code with small DOM adapters; no browser claim. */
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const ROOT=path.resolve(__dirname,'..');const reports=[];
const escape=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const lang of ['','es/']){
 const dataContext={window:{}};vm.runInNewContext(fs.readFileSync(path.join(ROOT,'dist',lang,'assets/data.js'),'utf8'),dataContext);const DATA=dataContext.window.STEM_DATA;
 const nodes=new Map(),listeners={};
 const node=id=>{if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',value:'',hidden:false,dataset:{},setAttribute(){},querySelectorAll(){return[]},addEventListener(){},scrollIntoView(){}});return nodes.get(id)};
 const document={querySelector:node,querySelectorAll:()=>[],getElementById:id=>node('#'+id),addEventListener:(name,fn)=>(listeners[name]??=[]).push(fn)};
 const c={DATA,EVENTS:DATA.events,esc:escape,document,window:{STEM_DATA:DATA,bestBadge:()=>'',STEM_DIRECTIONS:{attributes:()=>'',chips:()=>''}},$:node,$$:()=>[]};vm.createContext(c);
 vm.runInContext(fs.readFileSync(path.join(ROOT,'dist',lang,'assets/leagues.js'),'utf8'),c);
 for(const p of DATA.league_guide.profiles){const html=c.leagueCard(p);assert(!html.includes('undefined'));assert(html.includes(`data-guide-detail="${p.id}"`));}
 for(const id of ['wro-panama-local','wro-mexico-junior','wro-guatemala-local','wro-colombia-local']){
  const p=DATA.league_guide.profiles.find(p=>p.id===id);assert(p);assert(c.leagueCard(p).includes('https://'));
 }
 assert.equal(DATA.league_guide.profiles.find(p=>p.id==='wro-panama-local').categories.length,8);
 for(const id of ['wro-panama-local','wro-guatemala-local','wro-colombia-local'])for(const category of DATA.league_guide.profiles.find(p=>p.id===id).categories){for(const key of ['name','age','age_rule','team','hardware','entry'])assert(category[key],id+' missing '+key);assert(DATA.events.some(e=>e.id===category.event_id));}
 vm.runInContext(fs.readFileSync(path.join(ROOT,'dist',lang,'assets/school-history.js'),'utf8'),c);c.window.renderSchoolHistory();
 const select=(key,value)=>(listeners.change||[]).forEach(fn=>fn({target:{dataset:{historyFilter:key},value}}));
 const query=value=>(listeners.input||[]).forEach(fn=>fn({target:{dataset:{historyFilter:'query'},value}}));
 const html=()=>node('#history-results').innerHTML;const count=()=>(html().match(/<tr><td>\d{4}<\/td>/g)||[]).length;
 select('league','');assert.equal(count(),DATA.school_history.results.length);assert(!html().includes('undefined'));
 assert(!html().includes('institutional_primary_report')&&!html().includes('organizer_report'));
 select('level','qualification');assert.equal(count(),DATA.school_history.results.filter(r=>r.level==='qualification').length);
 const generic=lang?'Clasificación para la siguiente etapa':'Квалификация к следующему этапу';assert(html().includes(generic));
 query('GTM-');assert.equal(count(),12);assert(!html().includes('data-school-open='));
 query('California Open');assert.equal(count(),6);assert(!html().includes('Квалификация на Worlds'));
 select('kind','school');assert.equal(count(),4);
 select('kind','unresolved');assert.equal(count(),2);assert(!html().includes('data-school-open='));
 select('kind','');query('GTM-');assert.equal(count(),12);select('level','world_match');assert.equal(count(),0);
 select('level','qualification');assert.equal(count(),12);
 for(const id of ['C2061','C2062'])assert.equal(DATA.events.find(e=>e.id===id).participation,'programme_milestone');
 const participationCode=fs.readFileSync(path.join(ROOT,'dist',lang,'assets/app.js'),'utf8');assert(participationCode.includes('programme_milestone:'));
 const filterCode=participationCode.slice(participationCode.indexOf('function filtered(){'),participationCode.indexOf('function addDays('));
 const state={view:'catalog',query:'',routeIsos:[],country:'PAN',participation:'programme_milestone',excluded:true,sort:'date'};
 const fc={EVENTS:DATA.events,DATA,state,window:{},DIRECTIONS:{matches:()=>true},fits:()=>true,TODAY:'2026-11-06',foldSearch:s=>String(s).toLowerCase()};vm.createContext(fc);vm.runInContext(filterCode,fc);
 assert.deepEqual(Array.from(fc.filtered(),e=>e.id),['C2061','C2062']);
 Object.assign(state,{participation:'team',dates:'upcoming',league:'wro-panama-local'});const activeTeams=Array.from(fc.filtered(),e=>e.id);assert.equal(activeTeams.length,13);assert(activeTeams.includes('C008')&&activeTeams.includes('C2049')&&!activeTeams.includes('C2061'));
 reports.push({language:lang?'es':'ru',league_profiles:DATA.league_guide.profiles.length,history_results:DATA.school_history.results.length,new_qualification_rows:12,california_open_rows:6,school_and_unresolved_filters:true,source_labels_human_readable:true,no_qualification_promoted_to_world_title:true});
}
console.log(JSON.stringify({checks:reports}));
