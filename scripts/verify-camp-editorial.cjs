// Exercise published recommendation logic, actual filters and escaped dossier rendering.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
class FixedDate extends Date{constructor(...args){super(...(args.length?args:['2026-11-06T18:00:00Z']));}static now(){return Date.parse('2026-11-06T18:00:00Z');}}
for(const lang of ['', 'es/']){
 const base=path.join(root,'dist',lang),guide=JSON.parse(fs.readFileSync(path.join(base,'downloads/STEM_camp_programmes_deep_2026_2027.json'),'utf8'));
 const selection=guide.editorial_selection;
 assert(selection&&selection.coverage.reviewed>=24&&selection.coverage.refresh_pending>=3);
 assert.equal(selection.reviews.length,selection.coverage.review_dossiers);assert.equal(selection.coverage.total_dossiers,guide.profiles.length);
 assert.equal(new Set(selection.reviews.map(r=>r.programme_id)).size,selection.reviews.length);
 for(const r of selection.reviews){assert.equal(new Set(r.criteria.map(c=>c.key)).size,7);assert(r.criteria.every(c=>selection.states[c.state]));assert(guide.profiles.some(p=>p.id===r.programme_id));}
 const directions={matches:(themes,selected)=>!selected||themes.includes(selected),attributes:()=>'',chips:()=>'',kind:()=>''};
 const context={window:{STEM_DIRECTIONS:directions},document:{getElementById:()=>({})},URL,Intl,Date:FixedDate,Set,WeakMap,Map};
 vm.createContext(context);
 if(lang){const app=fs.readFileSync(path.join(base,'assets/app.js'),'utf8');const fold=app.match(/^const foldSearch=.*;$/m);assert(fold);vm.runInContext(fold[0],context);}
 vm.runInContext(fs.readFileSync(path.join(base,'assets/camp-planning.js'),'utf8'),context);const M=context.window.STEM_CAMP_PLANNER;
 let ui=fs.readFileSync(path.join(base,'assets/camp-programmes.js'),'utf8');const end=' init();\n})();';assert(ui.includes(end));
 ui=ui.replace(end,' window.TEST_CAMP_UI={filtered,card,editorialSummary,editorialDetails,editorialMethod,state:cs,setGuide:value=>{guide=value;}};\n})();');
 vm.runInContext(ui,context);const U=context.window.TEST_CAMP_UI;U.setGuide(guide);
 const editorialFile='STEM_camp_editorial_selection_v'+selection.version+'.json';assert(U.editorialMethod().includes(editorialFile),'Editorial download must refer to the current reviewed collection');assert.deepEqual(JSON.parse(fs.readFileSync(path.join(base,'downloads',editorialFile),'utf8')),selection);
 const reset=()=>Object.assign(U.state,{query:'',country:'',theme:'',format:'',child:'',phase:'',language:'',month:'',sort:'listed',review:''});
 reset();assert.equal(U.filtered().length,guide.profiles.length,'Editorial feature must retain all dossiers');
 U.state.review='reviewed';assert.equal(U.filtered().length,selection.reviews.length);
 Object.assign(U.state,{country:'JPN',child:'both',language:'EN',month:'2026-12',sort:'recommend_engineering'});
 assert.deepEqual(Array.from(U.filtered().map(p=>p.id)),['CP122','CP031','CP386'],'The three reviewed Japanese December programmes must pass the combined filters, with the matched coding track first');
 Object.assign(U.state,{country:'CHE',child:'oscar',language:'',month:''});
 const young=Array.from(U.filtered().map(p=>p.id));assert(!young.includes('CP012')&&!young.includes('CP622'),'Older technical courses must not pass Oscar filter');
 reset();Object.assign(U.state,{country:'CAN',child:'oscar',review:'reviewed',sort:'recommend_future'});assert(U.filtered().some(p=>p.id==='CP152'),'Future routes must remain visible for the selected child despite current age');
 reset();
 const p={id:'synthetic',provider:'Fixture',family_fit:{matvey:{status:'candidate'},oscar:{status:'candidate'}},confirmed_instruction_languages:['EN'],timing:{sessions:[['2027-07-01','2027-07-07']]},price:{currency:'USD',amount:1}};
 const make=(id,patch={})=>({...structuredClone(p),id,...patch});
 const ready=make('ready'),tooYoung=make('too-young',{family_fit:{matvey:{status:'candidate'},oscar:{status:'later'}}}),support=make('support',{confirmed_instruction_languages:[],confirmed_support_languages:['EN']}),archive=make('archive',{timing:{status:'published_2027',sessions:[['2026-07-01','2026-07-07']]}});
 const testSelection={goal_labels:{engineering:'Engineering',future:'Future',value:'Value'},reviews:[ready,tooYoung,support,archive].map(x=>({programme_id:x.id,status:'reviewed',goals:{engineering:{tier:x.id==='ready'?'alternative':'priority'}}})),value_policy:'Full trip cost unknown'};
 const input=[tooYoung,support,archive,ready],before=JSON.stringify(input);
 const order=M.sortProfiles(input,'recommend_engineering','both','2026-11-06',testSelection);
 assert.equal(order[0].id,'ready','Age, language and current dates must precede a more favorable editorial tier');
 assert.equal(JSON.stringify(input),before,'Sorting must not mutate source records');
 assert.equal(M.editorialAssessment(support,'engineering','both',testSelection,'2026-11-06').language,1,'EN support does not prove instructional EN');
 assert.equal(M.editorialAssessment(archive,'engineering','both',testSelection,'2026-11-06').season,2,'A 2027 heading must not roll old dates forward');
 const unknown=M.editorialAssessment(make('unreviewed'),'engineering','both',testSelection,'2026-11-06');assert.equal(unknown.tier,'unreviewed');assert(!Object.hasOwn(unknown,'score'));
 assert.equal(M.editorialAssessment(ready,'value','both',testSelection,'2026-11-06').tier,'not_rated','Unknown full-trip value must not become a cheapness ranking');
 const prices=input.map(x=>({...x,price:{currency:x.id==='ready'?'CHF':'JPY',amount:x.id==='ready'?9999999:1}}));
 assert.deepEqual(Array.from(M.sortProfiles(prices,'recommend_engineering','both','2026-11-06',testSelection).map(p=>p.id)),Array.from(order.map(p=>p.id)),'Cross-currency numbers must not drive quality order');
 for(const goal of Object.keys(selection.goal_labels)){
  const state={sort:'recommend_'+goal,review:'reviewed',country:'CHE',child:'oscar',month:'2027-07'};
  const url=M.filterURL('https://example.test/?camp=old#schools',state),restored=M.readFilters(url,guide.profiles,{},{});
  assert.equal(restored.sort,state.sort);assert.equal(restored.review,'reviewed');assert.equal(restored.country,'CHE');assert.equal(restored.child,'oscar');assert.equal(restored.month,'2027-07');assert(!new URL(url).searchParams.has('camp'));
 }
 for(const r of selection.reviews){const p=guide.profiles.find(p=>p.id===r.programme_id);const html=U.card(p);assert(html.includes('cp-editorial-details'));assert(!html.includes('undefined'));}
 const unsafe=structuredClone(guide.profiles.find(p=>p.id==='CP031'));const modified=structuredClone(guide);modified.editorial_selection.reviews.find(r=>r.programme_id==='CP031').summary='<img src=x onerror=attack()>';U.setGuide(modified);
 const html=U.editorialDetails(unsafe);assert(!html.includes('<img src=x'));assert(html.includes('&lt;img'));
 U.setGuide(guide);reset();Object.assign(U.state,{sort:'recommend_engineering',review:'reviewed'});
 const sorted=U.filtered();assert.equal(new Set(sorted.map(p=>p.id)).size,selection.reviews.length);
 console.log((lang||'ru')+': editorial gates, review coverage, actual combined filters, eight shareable goals, source preservation and escaped evidence passed');
}
