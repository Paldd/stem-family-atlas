/* Check the shipped family filters against classroom, university and advanced drone rules. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert/strict');
const root=path.resolve(__dirname,'..');
for(const lang of ['','es/']){
 const base=path.join(root,'dist',lang),d={window:{}};vm.runInNewContext(fs.readFileSync(path.join(base,'assets/data.js'),'utf8'),d);const DATA=d.window.STEM_DATA;
 const load=n=>JSON.parse(fs.readFileSync(path.join(base,'downloads/STEM_recf_remaining_'+n+'_v199.json'),'utf8'));
 const native=load('native'),inventory=load('inventory'),audit=load('audit');
 const by=id=>DATA.events.find(e=>e.id===id),row=pid=>inventory.linked_events.find(r=>r.provider_id===pid),item=pid=>by(row(pid).catalogue_id),profile=id=>DATA.league_guide.profiles.find(p=>p.id===id);
 assert.equal(native.new_events.length,38);assert.equal(inventory.linked_events.length,35);assert.equal(inventory.preview_events.length,0);
 assert.equal(inventory.linked_events.filter(r=>r.programme==='inspire').length,8);assert.equal(inventory.linked_events.filter(r=>r.programme==='pro').length,27);
 assert.equal(inventory.aggregate_recf_snapshot.total,871);assert.equal(inventory.aggregate_recf_snapshot.detailed,855);assert.equal(inventory.aggregate_recf_snapshot.previews,16);
 assert.equal(audit.current_full_portal_revalidation,false,'Counts from dated programme snapshots are not fresh verification of every portal page');
 for(const p of inventory.linked_events){const e=by(p.catalogue_id);assert.equal(e.languages.length,0);assert.equal(e.team_min,p.programme==='inspire'?1:2);}
 const launch=profile('recf-launch'),inspire=profile('recf-inspire'),pro=profile('recf-adc-pro');
 assert.equal(launch.event_ids.length,0,'A classroom game is not a fabricated camp or dated tournament');assert(launch.age_tags.includes('6')&&launch.age_tags.includes('9'));
 assert(launch.categories[0].team.includes('90')&&launch.categories[0].team.includes('50–40'));assert(launch.hardware.includes('16 × 16 × 16'));
 assert.deepEqual(Array.from(inspire.age_tags),['university']);assert(!pro.age_tags.includes('6')&&!pro.age_tags.includes('9'));
 assert.equal(item(145).start,'');assert.equal(item(145).reported_start,'2027-01-21');assert.equal(item(145).reported_end,'2027-01-22');
 assert.equal(item(738).start,'');assert.equal(item(738).reported_start,'2027-05-22');assert.equal(item(738).reported_deadline,'2027-05-01');assert.equal(item(738).deadline,'');
 assert.equal(item(738).visitor_policy,'restricted');assert(row(738).admission_flags.includes('foreign_adults_18_plus_excluded'));
 assert.equal(item(229).admission_kind,'school_selection');assert.equal(item(229).team_min,2,'Eight is the event team threshold, not students per team');assert(row(229).admission_flags.includes('jrotc_only_despite_open_metadata'));
 assert.notEqual(item(1056).admission_kind,'school_selection','Hosting AFJROTC is not an exclusion rule');assert.notEqual(item(948).admission_kind,'school_selection','Conference in a title does not prove membership restrictions');
 assert.equal(item(457).scope,'international');assert(row(457).admission_flags.includes('official_signature_directory'));
 assert.equal(row(159).practice_competition,true);assert.equal(item(159).start,'2026-10-23');
 const learning=by(inventory.learning_event_id);assert.equal(learning.block,lang?'Campamentos':'Лагеря');assert.equal(learning.participation,'workshop');assert.equal(learning.start,'2026-10-21');assert.equal(learning.end,'2026-10-22');assert.equal(learning.parent_event_id,item(159).id);assert.equal(learning.team_min,null);
 for(const id of [312,1003])assert.equal(item(id).scope,'national');assert.equal(item(773).scope,'international');
 const app=fs.readFileSync(path.join(base,'assets/app.js'),'utf8'),code=app.slice(app.indexOf('function filtered(){'),app.indexOf('function addDays('));
 if(lang)vm.runInNewContext(fs.readFileSync(path.join(base,'assets/fit-text.js'),'utf8'),d);
 const state={view:'catalog',query:'',routeIsos:[],excluded:true,sort:'date'},c={EVENTS:DATA.events,DATA,state,window:d.window,DIRECTIONS:{matches:()=>true},TODAY:'2026-11-06',foldSearch:s=>String(s).toLowerCase()};vm.createContext(c);
 const fitCode=app.split('\n').find(l=>l.startsWith('const yes='))+'\n'+app.slice(app.indexOf('function fits('),app.indexOf('function filtered(){'));vm.runInContext(fitCode+'\n'+code,c);
 for(const id of ['recf-inspire','recf-adc-pro']){state.league=id;const ids=new Set(Array.from(c.filtered(),e=>e.id));assert(profile(id).event_ids.every(e=>ids.has(e)));state.language='EN';assert.equal(c.filtered().length,0,'English documentation does not prove oral judging language');state.language='';}
 state.league='recf-launch';assert.equal(c.filtered().length,0);
 state.league='recf-inspire';state.kid='conditional';assert.equal(c.filtered().length,0,'University status cannot become conditional elementary entry');
 state.league='recf-adc-pro';const conditional=new Set(Array.from(c.filtered(),e=>e.id));assert(!conditional.has(item(229).id)&&!conditional.has(item(738).id));
 console.log((lang||'ru')+': classroom resource, university status, advanced team and gear gates, source date conflicts, venue restrictions, training split and actual filters passed');
}
