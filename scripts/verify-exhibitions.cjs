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
    dateText: blank, shortDate: blank, visitorBadge: blank, campLanguageBadge: blank,
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
  const exhibitions = context.window.STEM_DATA.events.filter(event => event.exhibition_tier);
  assert(exhibitions.length > 0);
  for (const event of exhibitions) {
    assert(context.card(event).includes(`data-id="${event.id}"`));
    assert(context.exhibitionDetails(event).includes('exhibition-admission'));
  }
  console.log(`${locale || 'ru'}: ${exhibitions.length} exhibition cards and details render`);
}
