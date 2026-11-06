/* Exercise mandatory/optional family costs using the shipped calculation helper. */
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const ROOT=path.resolve(__dirname,'..');
for(const lang of ['','es/']){
 const c={window:{},URL,Intl,Date,Set,WeakMap};vm.createContext(c);
 vm.runInContext(fs.readFileSync(path.join(ROOT,'dist',lang,'assets/camp-planning.js'),'utf8'),c);
 const M=c.window.STEM_CAMP_PLANNER;
 const dataContext={window:{}};vm.runInNewContext(fs.readFileSync(path.join(ROOT,'dist',lang,'assets/data.js'),'utf8'),dataContext);
 const offers=dataContext.window.STEM_DATA.camp_planning.offers;
 const offer=id=>{const result=offers.find(o=>o.id===id);assert(result,id);return result};
 for(const id of ['enforex-madrid-two-day','enforex-elviria-two-day','enforex-barcelona-beach-two-weeks-2-children-day']){
  const o=offer(id);assert.equal(M.estimate(o).published,2970,id);
  assert.equal(M.estimate(o,{},['daily_bus']).published,2970,'A previously saved optional bus must not be counted twice');
  assert(!o.optional.some(x=>x.id==='daily_bus'),'Required bus cannot be disabled as an optional extra');
  assert.equal(o.required.filter(x=>x.id==='daily_bus').length,1);
  assert(M.estimate(o).missing.length>0&&!M.estimate(o).complete,'Known camp charges are not the full family trip price');
 }
 assert.equal(M.estimate(offer('enforex-barcelona-beach-two-weeks-1-children-day')).published,1485);
 assert.equal(M.estimate(offer('enforex-salamanca-two-day')).published,2470,'Do not apply a campus-specific bus rule to Salamanca');
 assert.equal(M.estimate(offer('enforex-madrid-two-board')).published,5060);
 assert.equal(M.estimate(offer('enforex-elviria-two-board')).published,4260);
 for(const season of ['winter','spring'])for(const count of [1,2]){
  const o=offer('hopla-'+season+'-2027-'+count+'-children');
  assert.equal(M.estimate(o).published,290*count);
  assert.equal(M.estimate(o,{},['full_care']).published,340*count);
  assert.equal(o.sessions.length,1);assert.equal(o.format,'day');assert(M.estimate(o).missing.length>=3);
 }
 console.log((lang||'ru')+': required bus, no double charge, campus-specific exceptions, boarding and optional aftercare verified');
}
