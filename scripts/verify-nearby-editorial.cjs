/* Exercise shipped sibling prices, source conflicts and exact holiday/age gates. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert/strict');
const ROOT=path.resolve(__dirname,'..');
for(const lang of ['','es/']){
 const base=path.join(ROOT,'dist',lang),c={window:{},URL,Intl,Date,Set,WeakMap};vm.createContext(c);
 vm.runInContext(fs.readFileSync(path.join(base,'assets/camp-planning.js'),'utf8'),c);const M=c.window.STEM_CAMP_PLANNER;
 const d={window:{}};vm.runInNewContext(fs.readFileSync(path.join(base,'assets/data.js'),'utf8'),d);const D=d.window.STEM_DATA;
 const p=id=>{const v=D.camp_programmes.profiles.find(p=>p.id===id);assert(v,id);return v;};
 const o=id=>{const v=D.camp_planning.offers.find(o=>o.id===id);assert(v,id);return v;};
 const totals={'coyote-winter-two-siblings-2026':5940,'coyote-pascua-two-siblings-2027':11700,'ojo-ciego-two-weeks-two-2027':41100,'santa-ursula-seven-days-two-2027':103400,'santa-ursula-extended-two-2027':197000,'fod-family-parallel-2027-01-25':120000};
 for(const [id,amount]of Object.entries(totals)){
  const offer=o(id),e=M.estimate(offer);assert.equal(e.published,amount,id);assert(e.missing.length>0&&!e.complete,'Camp charge is not the whole family trip');
 }
 const winter=o('coyote-winter-two-siblings-2026');assert.equal(winter.payment_schedule.advance,1980);assert.equal(winter.payment_schedule.balance,3960);
 assert.equal(M.estimate(winter).published,winter.payment_schedule.advance+winter.payment_schedule.balance,'Advance must not be added twice');
 assert.notEqual(M.estimate(winter).published,5610,'Two-child calculator selects sibling discount, not two single early fees');
 assert.equal(winter.discount_second,0,'A total-family discount must not be applied again to the second child');
 assert.equal(p('CP614').availability.status,'unconfirmed');assert.equal(o('coyote-pascua-two-siblings-2027').availability.status,'unconfirmed');
 assert.equal(p('CP614').timing.sessions.length,1);assert.equal(p('CP614').timing.sessions[0][0],'2027-03-29');
 assert.equal(p('CP615').timing.sessions.length,0,'Month-only Pro must not acquire invented exact dates');
 assert(M.matchesMonth(p('CP615'),'2027-07'));assert(!M.matchesMonth(p('CP615'),'2027-08'));
 assert(M.matchesMonth(p('CP614'),'2027-03')&&M.matchesMonth(p('CP614'),'2027-04')&&M.matchesMonth(p('CP614'),'2027-08'));
 assert(!D.events.some(e=>e.camp_programme_id==='CP615'),'Month-only Pro must not create calendar events');
 assert.equal(p('CP615').family_fit.oscar.status,'later');
 const ex=p('CP612');assert.equal(ex.price.terms_validity.season,2027);assert.equal(ex.price.terms_validity.enrollment_from,'2026-11-01');
 assert.equal(ex.price.registration_fee.display_amount,200);assert.equal(ex.price.registration_fee.paid_at_registration,100);
 assert(ex.price.registration_fee.currency_unconfirmed&&ex.price.registration_fee.included_in_course_fee_unconfirmed);
 assert.deepEqual(Array.from(ex.confirmed_instruction_languages),['ES']);assert.equal(ex.language_evidence_role,'language_lessons');
 for(let i=1124;i<=1130;i++)assert.equal(p('CP'+i).confirmed_instruction_languages.length,0,'Spanish form does not confirm oral instruction');
 assert.equal(p('CP1124').family_fit.matvey.status,'not_eligible');assert.equal(p('CP1124').family_fit.oscar.status,'conditional');
 const a=p('CP1129').timing.session_details[0],b=p('CP1130').timing.session_details[0];
 assert.equal(a.start,'2027-01-25');assert.equal(a.sessions[0].start_time,'13:00');assert.equal(b.start,'2027-01-11');
 assert(b.start<a.start,'Nivel 4 precedes Nivel 3 in this season; no automatic sequential ladder');
 const q=o('fod-family-parallel-2027-01-25');assert.equal(q.format,'day');assert.deepEqual(Array.from(q.sessions[0]),['2027-01-25','2027-01-29']);
 assert.equal(p('CP1126').family_fit.matvey.status,'conditional');assert.equal(p('CP1126').family_fit.oscar.status,'conditional');
 const native=JSON.parse(fs.readFileSync(path.join(base,'downloads/STEM_camp_nearby_editorial_native_v194.json'),'utf8'));
 for(const u of native.deadline_updates){const e=D.events.find(e=>e.id===u.event_id);assert.equal(e.deadline,u.deadline);assert.equal(e.deadline_label,u.deadline_label);}
 assert.equal(native.deadline_updates.length,2);
 const sel=D.camp_programmes.editorial_selection;assert.equal(sel.coverage.reviewed,57);assert.equal(sel.coverage.refresh_pending,4);assert.equal(sel.reviews.length,61);
 for(const id of native.modified_raw_profile_ids)assert.equal(sel.reviews.find(r=>r.programme_id===id).criteria.length,7);
 const gate=M.editorialAssessment(p('CP614'),'general','both',sel,'2026-11-06');assert.equal(gate.season,3);assert(gate.gates.length>=2,'Admission conflict and unknown language must remain visible');
 assert.equal(M.sortProfiles([p('CP614'),p('CP613')],'recommend_general','both','2026-11-06',sel)[0].id,'CP613','An unconfirmed Pascua intake must rank behind the open winter alternative');
 console.log((lang||'ru')+': sibling tariffs, advances, registration terms, admission conflict, oral-language evidence and exact holiday age/time gates passed');
}
