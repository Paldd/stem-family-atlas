'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'..'),clone=x=>JSON.parse(JSON.stringify(x)),checks=[];
for(const lang of ['','es/']){
 const context={window:{},Intl,Date,Set,Map,WeakMap,URL};vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(root,'dist',lang,'assets/camp-planning.js'),'utf8'),context);
 const M=context.window.STEM_CAMP_PLANNER,guide=JSON.parse(fs.readFileSync(path.join(root,'dist',lang,'downloads/STEM_camp_programmes_deep_2026_2027.json'),'utf8'));
 const day='2026-11-06',profiles=guide.profiles.filter(p=>p.iso==='CRI');
 const pairs=M.pairedSessions(profiles,'',day);
 assert.equal(pairs.length,5);assert(pairs.every(p=>p.price.amount===120000&&p.price.currency==='CRC'&&p.price.tax_included));
 assert(pairs.every(p=>p.matvey.profile.id!=='CP1124'&&p.matvey.profile.id!=='CP1125'));
 assert.equal(M.pairedSessions(profiles,'2026-12',day).length,1);assert.equal(M.pairedSessions(profiles,'2027-01',day).length,4);assert.equal(M.pairedSessions(profiles,'2027-02',day).length,0);
 assert.equal(M.pairedSessions(profiles,'','2027-02-01').length,0);
 assert(pairs.every(p=>p.matvey.times.length===5&&p.matvey.times.every(t=>t[1]==='08:00'&&t[2]==='12:00'&&t[3]==='America/Costa_Rica')));
 const dec=pairs.find(p=>p.start==='2026-12-07');assert.equal(dec.matvey.profile.id,'CP1127');assert.equal(dec.oscar.profile.id,'CP1124');
 const seed=[clone(dec.matvey.profile),clone(dec.oscar.profile)];for(const p of seed)p.timing.session_details=p.timing.session_details.filter(v=>v.start==='2026-12-07');
 function run(change){const p=clone(seed);change(p);return M.pairedSessions(p,'',day);}
 assert.equal(run(p=>delete p[0].pairing).length,0);
 assert.equal(run(p=>delete p[0].pairing.verified_source).length,0);
 assert.equal(run(p=>p[1].iso='MEX').length,0);
 assert.equal(run(p=>p[1].pairing.venue_id='another-campus').length,0);
 assert.equal(run(p=>p[1].timing.session_details[0].sessions[0].end_time='13:00').length,0);
 assert.equal(run(p=>p[1].timing.session_details[0].sessions[0].timezone='America/Mexico_City').length,0);
 assert.equal(run(p=>p[1].timing.session_details[0].sessions[0].timezone='Invalid/Zone').length,0);
 assert.equal(run(p=>p[1].timing.session_details[0].sessions.push(p[1].timing.session_details[0].sessions[0])).length,0);
 assert.equal(run(p=>p[0].timing.session_details[0].family_fit.matvey.status='not_eligible').length,0);
 assert.equal(run(p=>p[0].timing.session_details[0].availability={status:'closed'}).length,0);
 assert.equal(run(p=>{for(const a of p){a.timing.session_details[0].start=a.timing.session_details[0].end='2027-02-30';a.timing.session_details[0].sessions=[{date:'2027-02-30',start_time:'08:00',end_time:'12:00',timezone:'America/Costa_Rica'}];}}).length,0);
 assert.equal(run(p=>{for(const a of p)a.pairing.fee.amount='60000';})[0].price.amount,120000);
 assert.equal(run(p=>p[0].timing.session_details.push(clone(p[0].timing.session_details[0]))).length,1);
 assert.equal(run(p=>delete p[1].pairing.fee)[0].price,null);
 const singapore=guide.profiles.filter(p=>p.iso==='SGP');
 const allSingaporePairs=M.pairedSessions(singapore,'',day);
 const singaporePairs=allSingaporePairs.filter(p=>p.matvey.profile.slug.startsWith('worklab-yearend-spike-')&&
   p.oscar.profile.slug.startsWith('worklab-yearend-apprentice-'));
 assert.equal(singaporePairs.length,19);
 assert.equal(M.pairedSessions(singapore,'2026-11',day).length,15);
 assert.equal(M.pairedSessions(singapore,'2026-12',day).length,30);
 assert.equal(M.pairedSessions(singapore,'2027-01',day).length,5);
 assert(singaporePairs.every(p=>p.matvey.profile.slug.startsWith('worklab-yearend-spike-')&&
   p.oscar.profile.slug.startsWith('worklab-yearend-apprentice-')&&
   p.matvey.profile.confirmed_instruction_languages.join()==='EN'&&
   p.oscar.profile.confirmed_instruction_languages.join()==='EN'&&p.price===null&&
   p.matvey.times.length===4&&p.matvey.times.every(t=>t[1]==='09:30'&&t[2]==='12:00'&&t[3]==='Asia/Singapore')));
 assert(singaporePairs.every(p=>!p.matvey.times.some(t=>['2026-12-25','2027-01-01'].includes(t[0]))));
 assert.deepEqual(new Set(singaporePairs.map(p=>p.venue)),new Set([
   'Singapore · Forum The Shopping Mall','Singapore · UE Square','Singapore · Coronation Shopping Plaza']));
 const minecraft=allSingaporePairs.filter(p=>p.matvey.profile.slug==='worklab-yearend-minecraft');
 assert.equal(allSingaporePairs.length,43);
 const meta=allSingaporePairs.filter(p=>p.matvey.profile.slug.startsWith('meta-space-exploratory-'));
 assert.equal(meta.length,12);
 assert(meta.every(p=>p.oscar.profile.slug.startsWith('meta-space-junior-')&&
   p.matvey.profile.pairing.venue_id===p.oscar.profile.pairing.venue_id&&
   p.price.amount===878&&p.price.currency==='SGD'&&p.price.tax_included&&
   p.matvey.times.length===3&&p.matvey.times.every(t=>t[1]==='09:00'&&t[2]==='12:00'&&t[3]==='Asia/Singapore')));
 const lccl=allSingaporePairs.filter(p=>p.matvey.profile.slug==='lccl-fundamentals');
 assert.equal(lccl.length,4);
 assert(lccl.every(p=>p.oscar.profile.slug==='lccl-early'&&p.price.amount===1200&&p.price.currency==='SGD'&&
   p.matvey.times.length===5&&p.matvey.times.every(t=>t[1]==='14:30'&&t[2]==='17:30'&&t[3]==='Asia/Singapore')));
 assert([...meta,...lccl].every(p=>[p.matvey,p.oscar].every(({profile})=>!profile.confirmed_instruction_languages.length)));
 assert.equal(minecraft.length,7);
 assert(minecraft.every(p=>p.oscar.profile.slug==='worklab-yearend-apprentice-forum'&&
   p.venue==='Singapore · Forum The Shopping Mall'&&p.price===null&&
   p.matvey.times.length===4&&p.matvey.times.every(t=>t[1]==='09:30'&&t[2]==='12:00'&&t[3]==='Asia/Singapore')));
 const optional=allSingaporePairs.filter(p=>p.oscar.profile.slug==='worklab-yearend-minecraft');
 assert.equal(optional.length,1);
 assert.equal(optional[0].start,'2027-01-04');
 assert.equal(optional[0].matvey.profile.slug,'worklab-yearend-spike-forum');
 assert.equal(optional[0].oscar.variant.family_fit.oscar.status,'conditional');
 checks.push({language:lang||'ru',singapore_family_pairs:43,real_family_pairs:5,month_and_past_filter:true,verified_shared_venue_required:true,exact_days_hours_timezone_required:true,variant_age_gate:true,invalid_dates_and_closed_groups_excluded:true,known_fee_units_only:true});
}
console.log(JSON.stringify(checks));
