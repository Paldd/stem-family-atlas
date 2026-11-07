/* Exercise the actual bilingual catalogue filters against the reviewed Achieve snapshot. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert/strict');
const root=path.resolve(__dirname,'..');
for(const lang of ['','es/']){
 const base=path.join(root,'dist',lang),d={window:{}};
 vm.runInNewContext(fs.readFileSync(path.join(base,'assets/data.js'),'utf8'),d);
 const DATA=d.window.STEM_DATA,load=name=>JSON.parse(fs.readFileSync(path.join(base,'downloads/STEM_achieve_global_'+name+'_v198.json'),'utf8'));
 const native=load('native'),inventory=load('inventory'),audit=load('audit');
 const by=id=>DATA.events.find(e=>e.id===id),row=pid=>inventory.linked_events.find(e=>e.provider_id===pid),item=pid=>by(row(pid).catalogue_id);
 const profile=DATA.league_guide.profiles.find(p=>p.id==='recf-achieve');
 assert.equal(inventory.linked_events.length,355);assert.equal(inventory.preview_events.length,5);
 assert.equal(new Set([...inventory.linked_events,...inventory.preview_events].map(r=>r.event_code)).size,360);
 assert.equal(native.new_events.length,360);assert.equal(native.new_events.filter(e=>e.block===(lang?'Competiciones':'Соревнования')).length,355);
 assert.equal(profile.categories.length,2);assert.equal(by(native.programme_hub_id).team_min,1);assert.equal(by(native.programme_hub_id).start,'');
 for(const id of [35,171,173])assert(!row(id).catalogue_id,'Adult volunteer training stays outside child camp catalogue');
 for(const id of [41,42,235,506,700]){assert.equal(item(id).block,lang?'Campamentos':'Лагеря');assert.equal(item(id).participation,'workshop');}
 for(const id of [912,924]){assert.equal(item(id).block,lang?'Competiciones':'Соревнования');assert.equal(item(id).scope,'regional');}
 for(const p of inventory.linked_events.filter(p=>p.catalogue_id)){
  const e=by(p.catalogue_id);assert.equal(e.team_min,[559,1048].includes(p.provider_id)?null:1);
  assert.equal(e.languages.includes('EN'),[706,707].includes(p.provider_id),'Only explicit oral-language evidence admits EN');
 }
 for(const id of audit.military_restricted_ids){assert.equal(item(id).admission_kind,'school_selection');assert.equal(row(id).admission_flags.includes('jrotc_only'),true);}
 assert(!row(559).admission_flags.includes('jrotc_only'),'Mixed JROTC/TSA/UIL affiliation is not JROTC-only');
 for(const id of [...audit.school_verification_ids,...audit.school_organization_only_ids,...audit.conference_membership_ids])assert.equal(item(id).admission_kind,'school_selection');
 for(const id of audit.registered_kansas_only_ids)assert.equal(item(id).admission_kind,'invitation');
 for(const id of audit.official_signature_provider_ids){assert.equal(item(id).scope,'international');assert(row(id).admission_flags.includes('official_signature_directory'));}
 assert(audit.official_signature_provider_ids.includes(710),'Korea Signature is verified even without Qualification metadata');
 for(const id of [279,1048])assert.equal(item(id).scope,'national');
 for(const id of [478,772])assert.equal(item(id).scope,'international');
 assert.equal(item(1048).deadline,'');assert.equal(row(1048).published_disputed_deadline,'2027-03-07');
 assert.equal(item(146).start,'');assert.equal(item(559).team_min,null);
 for(const id of audit.remote_provider_ids){assert.equal(item(id).iso.length,0);assert.equal(item(id).admission_kind,'invitation');assert(row(id).remote);}
 assert.equal(audit.remote_provider_ids.length,15);
 for(const id of [706,707]){assert.equal(row(id).remote,false);assert.equal(item(id).languages[0],'EN');}
 assert.equal(item(707).start,'2027-03-15');assert.equal(item(707).end,'2027-03-17');assert.equal(item(706).start,'2027-03-18');assert.equal(item(706).end,'2027-03-20');
 assert.equal(item(772).deadline,'2027-01-30','Through explicitly marks registration close');
 for(const id of [706,707,1090,655])assert.equal(row(id).deadline_role,'payment','Single registration date must not become closing date');
 for(const id of ['C2231','C2232']){assert.equal(by(id).deadline,'2027-02-19');assert.equal(by(id).languages[0],'EN');assert(by(id).deadline_history.length);}
 for(const id of ['C2095','L626']){assert.equal(by(id).deadline,'');assert(by(id).deadline_history.length);}
 for(const p of inventory.preview_events){const e=by(p.catalogue_id);assert.equal(e.start,p.start);assert.equal(e.end,p.end);assert.equal(e.deadline,'');assert.equal(e.date_precision,'published_preview');}
 const ambiguous=inventory.preview_events.find(p=>p.event_code==='ACH20262423');assert.equal(by(ambiguous.catalogue_id).team_min,null);
 assert.equal(by('C1882').title.includes('Achieve'),false,'KNRC VEX record remains a separate programme');
 for(const [i,deadline] of ['2027-03-01','2027-03-31'].entries()){const e=by(native.programme_milestone_ids[i]);assert.equal(e.deadline,deadline);assert.equal(e.start,'');assert.equal(e.participation,'programme_milestone');}
 const app=fs.readFileSync(path.join(base,'assets/app.js'),'utf8'),code=app.slice(app.indexOf('function filtered(){'),app.indexOf('function addDays('));
 if(lang)vm.runInNewContext(fs.readFileSync(path.join(base,'assets/fit-text.js'),'utf8'),d);
 const state={view:'catalog',query:'',routeIsos:[],excluded:true,sort:'date'},c={EVENTS:DATA.events,DATA,state,window:d.window,DIRECTIONS:{matches:()=>true},TODAY:'2026-11-06',foldSearch:s=>String(s).toLowerCase()};vm.createContext(c);
 const fitCode=app.split('\n').find(line=>line.startsWith('const yes='))+'\n'+app.slice(app.indexOf('function fits('),app.indexOf('function filtered(){'));vm.runInContext(fitCode+'\n'+code,c);
 state.league='recf-achieve';const ids=new Set(Array.from(c.filtered(),e=>e.id));assert(native.new_events.every(e=>ids.has(e.id)),'All source additions reachable via dedicated league profile');
 state.language='EN';const importedIds=new Set(native.new_events.map(e=>e.id));
 assert.deepEqual(new Set(Array.from(c.filtered(),e=>e.id).filter(id=>importedIds.has(id))),new Set([item(706).id,item(707).id]),'New records without oral-language evidence do not pass EN filter');
 Object.assign(state,{language:'',kid:'conditional'});const conditional=new Set(Array.from(c.filtered(),e=>e.id));assert(conditional.has(item(1010).id),'Unknown Indigenous status stays conditional without nationality inference');
 for(const id of audit.military_restricted_ids)assert(!conditional.has(item(id).id),'JROTC-only route is not an open conditional family entry');
 Object.assign(state,{kid:'',scope:'international',country:'KOR'});assert(c.filtered().some(e=>e.id===item(710).id));
 console.log((lang||'ru')+': Achieve source inventory, ages, school/membership gates, international routes, explicit language, payment roles, previews and shipped filters passed');
}
