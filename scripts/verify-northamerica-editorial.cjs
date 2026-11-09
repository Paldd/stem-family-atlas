/* Exercise real camp estimates, language/age filters and sourced multiweek dates. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
for(const lang of ['', 'es/']){
 const base=path.join(root,'dist',lang),d={window:{}};vm.runInNewContext(fs.readFileSync(path.join(base,'assets/data.js'),'utf8'),d);const D=d.window.STEM_DATA;
 const guide=D.camp_programmes,sel=guide.editorial_selection;
 const context={window:{STEM_DIRECTIONS:{matches:(themes,selected)=>!selected||themes.includes(selected),attributes:()=>'',chips:()=>'',kind:()=>''}},document:{getElementById:()=>({})},URL,Intl,Date,Set,WeakMap,Map};vm.createContext(context);
 if(lang){const app=fs.readFileSync(path.join(base,'assets/app.js'),'utf8');const fold=app.match(/^const foldSearch=.*;$/m);assert(fold);vm.runInContext(fold[0],context);}
 vm.runInContext(fs.readFileSync(path.join(base,'assets/camp-planning.js'),'utf8'),context);const M=context.window.STEM_CAMP_PLANNER;
 let ui=fs.readFileSync(path.join(base,'assets/camp-programmes.js'),'utf8');const end=' if(!document.getElementById(\'camps-view\').hidden)window.mountCampDossiers();\n})();';assert(ui.includes(end));ui=ui.replace(end,' window.TEST_CAMP_UI={filtered,card,editorialDetails,state:cs,setGuide:value=>{guide=value;}};\n})();');vm.runInContext(ui,context);const U=context.window.TEST_CAMP_UI;U.setGuide(guide);
 const p=id=>{const x=guide.profiles.find(p=>p.id===id);assert(x,id);return x;},o=id=>{const x=D.camp_planning.offers.find(o=>o.id===id);assert(x,id);return x;};
 const totals={'ussrc-space-matvey-2027':1699,'ussrc-robotics-matvey-2027':1699,'aviation-family-onsite-three-2027':2397,'aviation-family-offsite-three-2027':2097,'ilsc-ubc-1w-boarding-matvey-2027':3335,'ilsc-ubc-1w-day-matvey-2027':1605,'ilsc-ubc-2w-boarding-matvey-2027':5880,'bricklabs-robotics-matvey-2027':1650,'bricklabs-creative-matvey-2027':1650,'arowhon-mini-two-2027':1400,'arowhon-regular-two-weeks-two-2027':10250,'catalina-one-week-matvey-2027':3750,'astrocamp-one-week-two-2027':5800,'frenchwoods-session1-early-two-2027':13400,'frenchwoods-trial-early-two-2027':4000};
 for(const[id,amount]of Object.entries(totals)){const e=M.estimate(o(id));assert.equal(e.published,amount,id);assert(e.missing.length>=4&&!e.complete,'Known camp cash requirement is not a full family trip');assert(e.lines.every(l=>Number.isFinite(l.amount)),id+' finite amounts');}
 assert.equal(M.estimate(o('aviation-family-onsite-three-2027'),{},['second_adult']).published,3196);
 assert.equal(M.estimate(o('aviation-family-offsite-three-2027'),{},['second_adult']).published,2796);
 assert.equal(M.estimate(o('ilsc-ubc-1w-day-matvey-2027'),{},['day_meals']).published,1785);
 assert.equal(M.estimate(o('arowhon-mini-two-2027'),{},['mini_bus_return_two']).published,1800);
 assert.equal(M.estimate(o('arowhon-regular-two-weeks-two-2027'),{},['regular_bus_return_two']).published,10950);
 assert.equal(M.estimate(o('astrocamp-one-week-two-2027'),{},['ont_return_two']).published,6040);
 for(const id of ['ilsc-ubc-1w-boarding-matvey-2027','ilsc-ubc-2w-boarding-matvey-2027']){const a=o(id);assert.equal(a.required.length,1);assert.equal(a.required[0].amount,100);assert(a.required[0].refundable&&a.required[0].once_per_stay);assert(!a.required.some(c=>c.amount===350),'Included registration advance is not another charge');}
 assert.equal(p('CP081').price.year,null,'Old 315 quote is not confirmed 2027 tuition');assert(p('CP081').previous_price_terms.label.includes('315'));assert(!D.camp_planning.offers.some(x=>x.slug===p('CP081').slug),'No invented current Next budget');
 assert.equal(p('CP037').price.amount,1699);assert.equal(p('CP079').price.currency,'CAD');
 const ilsc=p('CP039'),sessions=D.events.filter(e=>e.camp_programme_id==='CP039');assert.equal(ilsc.timing.precision,'published_sessions');assert.equal(sessions.length,21);assert.equal(ilsc.timing.session_details.length,21);
 for(let n=1;n<=6;n++){
  const options=ilsc.timing.session_details.filter(s=>s.duration_weeks===n);assert.equal(options.length,7-n);
  for(const s of options){assert.equal(new Date(s.start+'T12:00:00Z').getUTCDay(),0);assert.equal((Date.parse(s.end)-Date.parse(s.start))/86400000,7*n);assert(s.end<='2027-08-08');assert.equal(s.source,ilsc.timing.verified_session_source);assert(s.date_rule);}
 }
 assert(sessions.every(e=>e.date_precision==='published_rule'&&e.date_rule&&e.languages.includes('EN')));
 assert(sessions.every(e=>e.osc!==e.mat),'Oscar cannot inherit Matvey age eligibility');assert(!M.matchesMonth(ilsc,'2027-02'));assert(M.matchesMonth(ilsc,'2027-08'));
 const reset=()=>Object.assign(U.state,{query:'',country:'',theme:'',format:'',child:'',phase:'',language:'',month:'',sort:'listed',review:''});
 reset();Object.assign(U.state,{country:'CAN',child:'matvey',language:'EN',month:'2027-07'});assert(U.filtered().some(p=>p.id==='CP039'));
 U.state.child='oscar';assert(!U.filtered().some(p=>p.id==='CP039'));U.state.child='both';assert(!U.filtered().some(p=>p.id==='CP039'));
 reset();U.state.language='EN';for(const id of ['CP035','CP038','CP079','CP080','CP081','CP084','CP085','CP086','CP142'])assert(!U.filtered().some(p=>p.id===id),id+' English website/riding does not prove instruction');
 assert(U.filtered().some(p=>p.id==='CP143'));assert(U.filtered().some(p=>p.id==='CP144'));
 reset();Object.assign(U.state,{country:'CAN',child:'oscar',month:'2027-07'});assert(!U.filtered().some(p=>['CP079','CP080'].includes(p.id)));
 const gate=M.editorialAssessment(p('CP037'),'engineering','matvey',sel,'2026-11-06');assert(gate.gates.length>0,'Grade-dependent candidate keeps eligibility gate');
 const native=JSON.parse(fs.readFileSync(path.join(base,'downloads/STEM_camp_northamerica_editorial_native_v195.json'),'utf8'));
 for(const u of native.deadline_updates){const e=D.events.find(e=>e.id===u.event_id);assert.equal(e.deadline,u.deadline);assert.equal(e.deadline_label,u.deadline_label);assert(e.start>e.deadline);}
 assert.equal(native.deadline_updates.length,4);assert.equal(sel.coverage.reviewed,71);assert.equal(sel.coverage.refresh_pending,4);assert.equal(sel.reviews.length,75);assert.equal(sel.external_institutional_sources.length,10);assert.equal(sel.independent_reviews.length,0);
 for(const id of native.modified_raw_profile_ids){const review=sel.reviews.find(r=>r.programme_id===id);assert.equal(review.criteria.length,7);assert(U.editorialDetails(p(id)).includes('cp-editorial'),'Editorial evidence renders');}
 console.log((lang||'ru')+': 15 partial budgets, paid adult, one-time refundable cash, credited advances, 21 multiweek options, language and grade gates, current/old quotes and four early-price reminders passed');
}
