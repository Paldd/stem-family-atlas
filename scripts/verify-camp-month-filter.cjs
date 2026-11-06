// Announced months must be searchable without becoming fabricated session days.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
for (const language of ['', 'es/']) {
  const context = {window: {}, URL, Intl, Date, Set, WeakMap};
  vm.runInNewContext(fs.readFileSync(path.join(root, 'dist', language, 'assets/camp-planning.js'), 'utf8'), context);
  const planner = context.window.STEM_CAMP_PLANNER;
  const profiles = JSON.parse(fs.readFileSync(path.join(root, 'dist', language, 'downloads/STEM_camp_programmes_deep_2026_2027.json'), 'utf8')).profiles;
  const actual = profiles.find(p => p.id === 'CP1410');
  assert(actual, 'Agora Andorra dossier must exist');
  for (const month of actual.timing.announced_months || []) {
    assert.equal(planner.matchesMonth(actual, month), true);
  }
  const announced = {timing: {announced_months: ['2027-07'], sessions: [], session_details: []}};
  assert.equal(planner.matchesMonth(announced, '2027-07'), true);
  assert.equal(planner.matchesMonth(announced, '2027-06'), false);
  assert.equal(planner.matchesMonth(announced, '2027-08'), false);
  assert.equal(planner.periods(announced).length, 0, 'A month announcement is not a session');
  assert.equal(announced.timing.session_details.length, 0);
  const archive = {timing: {sessions: [['2026-07-05', '2026-07-26']]}};
  assert.equal(planner.matchesMonth(archive, '2027-07'), false, 'Old season must not roll forward');
  const crossing = {timing: {sessions: [['2027-03-30', '2027-04-02']]}};
  assert.equal(planner.matchesMonth(crossing, '2027-03'), true);
  assert.equal(planner.matchesMonth(crossing, '2027-04'), true);
  assert.equal(planner.matchesMonth(crossing, '2027-05'), false);
  for (const invalid of ['2027-13', '2027-00', '2027-7', '2027-07-01']) {
    assert.equal(planner.matchesMonth(announced, invalid), false);
  }
  assert.equal(planner.matchesMonth({timing: {sessions: []}}, '2027-07'), false);
  assert.equal(planner.matchesMonth(announced, ''), true);
  console.log((language || 'ru') + ': month-only filtering, real periods and old-season isolation passed');
}
