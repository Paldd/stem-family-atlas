/* Exercise the shipped event filters and the imported provider distinctions. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert/strict');
const root=path.resolve(__dirname,'..');
for(const lang of ['','es/']){
 const base=path.join(root,'dist',lang),d={window:{}};vm.runInNewContext(fs.readFileSync(path.join(base,'assets/data.js'),'utf8'),d);const DATA=d.window.STEM_DATA;
 const native=JSON.parse(fs.readFileSync(path.join(base,'downloads/STEM_recf_global_native_v196.json'),'utf8')),inventory=JSON.parse(fs.readFileSync(path.join(base,'downloads/STEM_recf_global_inventory_v196.json'),'utf8'));
 const by=id=>DATA.events.find(e=>e.id===id),row=pid=>inventory.linked_events.find(e=>e.provider_id===pid),item=pid=>by(row(pid).catalogue_id);
 assert.equal(native.new_events.length,258);assert.equal(native.new_events.filter(e=>e.block===(lang?'Competiciones':'Соревнования')).length,254);
 assert.equal(inventory.linked_events.length,261);assert.equal(inventory.preview_events.length,4);assert.equal(new Set(inventory.linked_events.map(r=>r.event_code)).size,261);
 for(const id of [170,172,334])assert(!row(id).catalogue_id,'Adult training must not become a child camp');
 for(const id of [58,218,340,582]){assert.equal(item(id).block,lang?'Campamentos':'Лагеря');assert.equal(item(id).participation,'workshop');}
 for(const id of [905,911,927])assert.equal(item(id).scope,'regional','Explicit provincial finals have regional scope');
 for(const id of [714,905,911,927])assert.equal(item(id).block,lang?'Competiciones':'Соревнования','Host type conflict is not a fabricated camp');
 assert.equal(item(144).admission_kind,'school_selection');assert.equal(item(844).admission_kind,'invitation');assert.equal(item(869).admission_kind,'invitation');assert.notEqual(item(805).admission_kind,'school_selection','Middle School only is a grade gate, not a school-organization restriction');
 assert.notEqual(item(561).admission_kind,'invitation','Disqualified from must not match qualified from');
 assert.equal(item(352).date_scope,'league_window');assert.equal(item(465).date_scope,'league_window','Missing type does not make a multi-meeting league continuous attendance');
 assert.equal(item(119).scope,'unclassified');assert.equal(item(119).iso.length,0,'Do not guess a location for a placeholder');
 for(const p of inventory.preview_events){const e=by(p.catalogue_id);assert.equal(e.start,p.start);assert.equal(e.end,p.end);assert.equal(e.deadline,'','Release is not registration deadline');assert.equal(e.date_precision,'published_preview');}
 for(const e of native.new_events)assert.equal(e.languages.length,0,'English portal is not proof of oral judging language');
 assert.equal(by('C030').start,'2027-04-25');assert.equal(by('C030').end,'2027-05-07');assert.equal(by('C030').date_history[0].start,'2027-04-27');assert.equal(by('C030').date_history[0].end,'2027-05-06');assert.equal(by('C030').scope,'international');
 assert.equal(by('C028').start,'');assert.equal(by('C028').end,'');assert(by('C028').city.includes('Las Vegas Convention Center'));assert.deepEqual(Array.from(by('C028').iso),['USA']);assert.equal(by('C019').start,'');
 assert.equal(by('C032').scope,'international');assert.equal(by('C032').start,'2027-04-28');
 const app=fs.readFileSync(path.join(base,'assets/app.js'),'utf8'),code=app.slice(app.indexOf('function filtered(){'),app.indexOf('function addDays('));
 const state={view:'catalog',query:'',routeIsos:[],excluded:true,sort:'date'},c={EVENTS:DATA.events,DATA,state,window:{},DIRECTIONS:{matches:()=>true},fits:()=>true,TODAY:'2026-11-06',foldSearch:s=>String(s).toLowerCase()};vm.createContext(c);vm.runInContext(code,c);
 state.league='recf';const league=new Set(Array.from(c.filtered(),e=>e.id));assert(native.new_events.every(e=>league.has(e.id)),'Every imported event reachable through RECF profile');
 Object.assign(state,{league:'',scope:'international',country:'USA'});const worlds=new Set(Array.from(c.filtered(),e=>e.id));assert(worlds.has('C028')&&worlds.has('C030')&&worlds.has('C032'),'World-route filters include the corrected hubs');
 Object.assign(state,{scope:'',country:'',admission:'invitation',league:'recf'});assert(c.filtered().some(e=>e.id===item(844).id));
 state.admission='';state.language='EN';
 const confirmedEnglish=new Set(['C2231','C2232']);
 const importedEnglish=c.filtered().filter(e=>native.new_events.some(n=>n.id===e.id));
 assert.deepEqual(new Set(importedEnglish.map(e=>e.id)),confirmedEnglish,'Only the two CREATE pages rechecked in v198 explicitly confirm spoken English');
 console.log((lang||'ru')+': complete Engage snapshot, adult/child types, source conflicts, school/invitation gates, league windows, preview releases, independent world venues, sourced date history and actual filters passed');
}
