/* Verify family-facing distinctions in the shipped ADC records and filters. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert/strict');
const root=path.resolve(__dirname,'..');
for(const lang of ['','es/']){
 const base=path.join(root,'dist',lang),d={window:{}};vm.runInNewContext(fs.readFileSync(path.join(base,'assets/data.js'),'utf8'),d);const DATA=d.window.STEM_DATA;
 const native=JSON.parse(fs.readFileSync(path.join(base,'downloads/STEM_adc_global_native_v197.json'),'utf8')),inventory=JSON.parse(fs.readFileSync(path.join(base,'downloads/STEM_adc_global_inventory_v197.json'),'utf8'));
 const by=id=>DATA.events.find(e=>e.id===id),row=pid=>inventory.linked_events.find(e=>e.provider_id===pid),item=pid=>by(row(pid).catalogue_id),profile=DATA.league_guide.profiles.find(p=>p.id==='drone');
 assert.equal(inventory.linked_events.length,204);assert.equal(inventory.preview_events.length,7);assert.equal(native.new_events.length,210);
 assert.equal(native.new_events.filter(e=>e.block===(lang?'Competiciones':'Соревнования')).length,202);
 assert.equal(by('C031').team_min,1);assert.equal(by('C031').start,'');assert.equal(by('C031').languages.length,0);
 assert.equal(profile.categories.length,3);assert(profile.age_tags.includes('6'));assert(profile.age_tags.includes('9'));
 for(const p of inventory.linked_events){const e=by(p.catalogue_id);assert(e);assert.equal(e.team_min,[245,246,247].includes(p.provider_id)?3:1);assert.equal(e.languages.length,0,'Portal English is not proof of judging language');}
 for(const id of [245,246,247]){assert(row(id).admission_flags.includes('local_team_minimum_three_with_single_team_exception'));assert.equal(item(id).participation,'team');}
 for(const id of [814,330,804,613,779,276,113,778]){assert.equal(item(id).block,lang?'Campamentos':'Лагеря');assert.equal(item(id).participation,'workshop');}
 for(const id of [63,228,257,765,683]){assert.equal(item(id).admission_kind,'school_selection');assert(row(id).admission_flags.includes('jrotc_programme_only'));}
 for(const id of [182,496,741,408,961,112,132,742,806,753])assert(!row(id).admission_flags.includes('jrotc_programme_only'),'Host/title JROTC alone does not exclude ordinary school teams');
 assert.equal(row(63).practice_competition,true,'Body says restricted scrimmage despite Qualifying Event metadata');
 assert.equal(item(228).start,'','Cancelled Friday conflicts with the two-day header; do not import disputed travel dates');
 assert.equal(item(942).start,'2027-01-15');assert.equal(item(942).end,'2027-01-16','Hosted programme dates are not competition dates');
 assert.equal(item(920).iso.length,0);assert.equal(item(920).admission_kind,'invitation');assert.equal(row(920).remote,true);
 assert.equal(item(754).start,item(755).start);assert.notEqual(row(754).grades,row(755).grades);assert.notEqual(item(754).title,item(755).title);
 for(const p of inventory.preview_events){const e=by(p.catalogue_id);assert.equal(e.start,p.start);assert.equal(e.end,p.end);assert.equal(e.deadline,'','Release is not registration deadline');assert.equal(e.date_precision,'published_preview');}
 const kuwait=by('C1883');assert.equal(kuwait.team_min,2);assert.equal(kuwait.team_max,4);assert.equal(kuwait.start,'2027-02-02');assert.equal(kuwait.end,'2027-02-03');assert.equal(kuwait.date_history[0].start,'2027-01-31');assert.equal(kuwait.date_history[0].end,'2027-02-04');
 assert.equal(by('C030').start,'2027-04-25');assert.equal(by('C030').end,'2027-05-07');assert.equal(by('C030').date_history[0].start,'2027-04-27');
 const app=fs.readFileSync(path.join(base,'assets/app.js'),'utf8'),code=app.slice(app.indexOf('function filtered(){'),app.indexOf('function addDays('));
 if(lang)vm.runInNewContext(fs.readFileSync(path.join(base,'assets/fit-text.js'),'utf8'),d);
 const state={view:'catalog',query:'',routeIsos:[],excluded:true,sort:'date'},c={EVENTS:DATA.events,DATA,state,window:d.window,DIRECTIONS:{matches:()=>true},TODAY:'2026-11-06',foldSearch:s=>String(s).toLowerCase()};vm.createContext(c);
 const fitCode=app.split('\n').find(line=>line.startsWith('const yes='))+'\n'+app.slice(app.indexOf('function fits('),app.indexOf('function filtered(){'));vm.runInContext(fitCode+'\n'+code,c);
 state.league='drone';const league=new Set(Array.from(c.filtered(),e=>e.id));assert(native.new_events.every(e=>league.has(e.id)),'All ADC records reachable through league navigation');assert(league.has('C031')&&league.has('C1883'));
 state.language='EN';assert(!c.filtered().some(e=>native.new_events.some(n=>n.id===e.id)),'Unknown oral language must not pass EN filter');
 state.language='';state.admission='school_selection';assert(c.filtered().some(e=>e.id===item(63).id));
 state.admission='';state.participation='individual';assert(c.filtered().some(e=>e.id===item(966).id),'One-student registered teams discoverable, with format conditions retained');
 state.participation='';state.kid='conditional';const conditional=new Set(Array.from(c.filtered(),e=>e.id));assert(conditional.has(item(102).id));assert(!conditional.has(item(63).id),'Restricted JROTC event must not look conditionally open to the brothers');
 console.log((lang||'ru')+': ADC ages/team minimum, grades, JROTC and district gates, practice/training, remote slots, preview releases, Kuwait history, complete inventory and shipped filters passed');
}
