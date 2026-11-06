/* Exercise shipped family estimates and actual Asian age/date/availability evidence. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert/strict');
const ROOT=path.resolve(__dirname,'..');
for(const lang of ['','es/']){
 const base=path.join(ROOT,'dist',lang),c={window:{},URL,Intl,Date,Set,WeakMap};vm.createContext(c);
 vm.runInContext(fs.readFileSync(path.join(base,'assets/camp-planning.js'),'utf8'),c);const M=c.window.STEM_CAMP_PLANNER;
 const d={window:{}};vm.runInNewContext(fs.readFileSync(path.join(base,'assets/data.js'),'utf8'),d);const D=d.window.STEM_DATA;
 const p=id=>{const x=D.camp_programmes.profiles.find(p=>p.id===id);assert(x,id);return x;};
 const o=id=>{const x=D.camp_planning.offers.find(o=>o.id===id);assert(x,id);return x;};
 for(const n of [1,2]){
  assert.equal(M.estimate(o(`grove-flight-2027-${n}-children`)).published,9700*n);
  assert.equal(M.estimate(o(`elev8-five-days-${n}-children`)).published,120175*n);
  assert(!o(`elev8-five-days-${n}-children`).sessions.some(s=>s[0]==='2026-12-28'),'Four days do not receive the five-day tariff');
  assert.equal(M.estimate(o(`oyis-winter-2026-${n}-children`)).published,66000*n);
 }
 const light=o('lighthouse-winter-mixed-siblings-five');assert.equal(M.estimate(light).published,44500);
 assert.equal(light.required.find(x=>x.id==='go_deposit').amount,2000);assert.equal(M.estimate(light,{},['lunch']).published,46700);
 assert.equal(M.estimate(o('see-2027-fju-mixed-siblings')).published,30600,'Two siblings are not the group of three or a completed early-bird enrollment');
 assert.equal(M.estimate(o('dcamps-daewon-two-children-2027')).published,1978000,'Post-camp refund must not reduce initial payment');
 for(const id of ['grove-flight-2027-2-children','lighthouse-winter-mixed-siblings-five','see-2027-fju-mixed-siblings','dcamps-daewon-two-children-2027'])assert(M.estimate(o(id)).missing.length>0&&!M.estimate(o(id)).complete,'Partial camp charges are not the full family trip');
 const robo=p('CP069').timing.session_details.filter(s=>s.start>='2026-11-06');assert.equal(robo.length,2);
 assert.equal(robo[0].start,'2026-12-21');assert.equal(robo[0].family_fit.matvey.status,'not_eligible');assert.equal(robo[0].family_fit.oscar.status,'candidate');
 assert.equal(robo[1].start,'2026-12-28');assert.equal(robo[1].family_fit.matvey.status,'candidate');assert.equal(robo[1].family_fit.oscar.status,'later');
 const unknown=p('CP875'),sel=D.camp_programmes.editorial_selection;
 assert.equal(unknown.availability.status,'unconfirmed');assert.equal(unknown.family_fit.matvey.status,'unknown');assert.equal(unknown.family_fit.oscar.status,'unknown');
 const a=M.editorialAssessment(unknown,'general','both',sel,'2026-11-06');assert.equal(a.tier,'deferred');assert.equal(a.season,3);assert.equal(a.age,2);
 const announcements=D.events.filter(e=>e.camp_programme_id==='CP875');assert.equal(announcements.length,3);assert(announcements.every(e=>e.date_precision==='announced_window'&&e.date_rule));
 for(const id of ['beaumont-sg-five','beaumont-sg-four'])assert.equal(o(id).availability.status,'unconfirmed');
 const native=JSON.parse(fs.readFileSync(path.join(base,'downloads/STEM_camp_asia_editorial_native_v193.json'),'utf8'));
 for(const update of native.deadline_updates){const e=D.events.find(e=>e.id===update.event_id);assert.equal(e.deadline,update.deadline);assert.equal(e.deadline_label,update.deadline_label);}
 assert.equal(native.deadline_updates.length,4);
 console.log((lang||'ru')+': tax, materials, refundable deposit, sibling fees, delayed refund, disjoint robotics weeks, withdrawn-source gates and four deadlines passed');
}
