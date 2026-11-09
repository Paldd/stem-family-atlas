const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

for (const locale of ['', 'es']) {
  const read = name => readFileSync(path.resolve(__dirname, '../dist', locale, 'assets', name), 'utf8');
  const app = read('app.js');
  const card = app.slice(app.indexOf('function card(e)'), app.indexOf('\n', app.indexOf('function card(e)')));
  const details = app.slice(app.indexOf('function exhibitionHighlights('), app.indexOf('function relatedEventLinks('));
  const blank = () => '';
  const context = vm.createContext({
    window: { bestBadge: blank },
    favoriteIds: new Set(), state: { view: 'exhibitions', compare: new Set() },
    DIRECTIONS: { attributes: blank, chips: blank }, shortTitles: {},
    esc: value => String(value ?? ''), classes: blank, art: blank, icon: blank,
    dateText: blank, shortDate: date => date, visitorBadge: blank, campLanguageBadge: blank,
    addDays: () => '2027-04-18',
    kidChip: blank, campDossierLink: blank,
  });
  vm.runInContext(read('atlas-core.js'), context);
  vm.runInContext(card + '\n' + details, context);

  const exhibition = { id: 'sample', exhibition_tier: 'test', exhibitor_note: 'Exhibitor note' };
  for (const highlights of [undefined, [], ['Robotics', 'AI'], 'Robotics']) {
    const event = { ...exhibition, highlights };
    const summary = Array.isArray(highlights) ? highlights.join(' · ') : highlights;
    assert(context.card(event).includes(`<p class="card-description">${summary || event.exhibitor_note}</p>`));
    assert(!context.exhibitionDetails(event).includes('href=""'));
  }
  const directory = 'https://example.com/exhibitors';
  assert(context.exhibitionDetails({ ...exhibition, exhibitor_directory_url: directory }).includes(`href="${directory}"`));
  const day = { date: '2027-04-17', start_time: '11:30', end_time: '18:00', ical_timed: true,
    start_utc: '2027-04-17T09:30:00Z', end_utc: '2027-04-17T16:00:00Z' };
  assert(context.exhibitionDetails({ ...exhibition, public_days: ['2027-04-16', day] })
    .includes('2027-04-16, 2027-04-17 · 11:30–18:00'));
  const singleDay = { id: 'sample', start: day.date, end: day.date, public_days: [day] };
  const occurrences = (event, asof = day.date) =>
    Array.from(context.exhibitionCalendarOccurrences(event, asof), bounds => Array.from(bounds));
  assert.deepEqual(occurrences(singleDay), [['sample', '20270417T093000Z', '20270417T160000Z', true]]);
  assert.deepEqual(occurrences({ ...singleDay, public_days: [day.date] }),
    [['sample', '2027-04-17', '2027-04-18', false]]);
  const secondDay = { ...day, date: '2027-04-18', start_utc: '2027-04-18T09:30:00Z', end_utc: '2027-04-18T16:00:00Z' };
  const twoDays = { ...singleDay, end: secondDay.date, public_days: [day, secondDay] };
  const nextOccurrence = ['sample-visit-2027-04-18', '20270418T093000Z', '20270418T160000Z', true];
  assert.deepEqual(occurrences(twoDays), [['sample', '20270417T093000Z', '20270417T160000Z', true], nextOccurrence]);
  assert.deepEqual(occurrences(twoDays, secondDay.date), [nextOccurrence]);
  const afternoon = { ...day, start_utc: '2027-04-17T16:30:00Z', end_utc: '2027-04-17T18:00:00Z' };
  const twoSlots = { ...singleDay, public_days: [day, afternoon] };
  assert.deepEqual(occurrences(twoSlots), [['sample', '20270417T093000Z', '20270417T160000Z', true],
    ['sample-visit-2027-04-17-2', '20270417T163000Z', '20270417T180000Z', true]]);
  const exhibitions = context.window.STEM_DATA.events.filter(event => event.exhibition_tier);
  assert(exhibitions.length > 0);
  for (const event of exhibitions) {
    assert(context.card(event).includes(`data-id="${event.id}"`));
    assert(context.exhibitionDetails(event).includes('exhibition-admission'));
  }
  console.log(`${locale || 'ru'}: ${exhibitions.length} exhibition cards and details render`);
}
