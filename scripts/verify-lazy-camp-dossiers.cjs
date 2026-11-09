const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

async function verifyEdition(locale) {
  const base = path.resolve(__dirname, '../dist', locale);
  const read = name => readFileSync(path.join(base, name), 'utf8');
  const html = read('index.html');
  const version = html.match(/data-ui-version="(\d+)"/)[1];
  const reportPath = 'downloads/STEM_camp_programmes_deep_2026_2027.json';
  const report = JSON.parse(read(reportPath));
  const slug = report.profiles[0].slug;
  assert(html.includes('src="assets/atlas-core.js?v=' + version + '"'));
  const app = read('assets/app.js');
  assert.match(app, /if\(state\.view==='camps'\)\{\s*drawCamps\(a\);\s*window\.mountCampDossiers\?\.\(\)/);

  // Use the real initializer. Substitute the DOM-heavy rendering calls
  // to isolate routing, asynchronous loading, caching and failure states.
  const source = read('assets/camp-programmes.js');
  const render = 'mountWorkspace();mountFamilyReview();drawCountryMap();renderScenario();renderCards();';
  const jump = 'if(slug)jump(slug);';
  assert(source.includes(render) && source.includes(jump));
  const code = source.replace(render, 'window.testRender(guide);')
    .replace(jump, jump.replace('jump(slug)', 'window.testJump(slug)'));

  function mount(hidden, search = '', failure = false) {
    const root = { innerHTML: '', addEventListener() {} };
    const view = { hidden };
    const requests = [], rendered = [], jumped = [];
    let finish;
    const window = {
      testRender: data => rendered.push(data),
      testJump: slug => jumped.push(slug),
    };
    const context = {
      window, URLSearchParams, location: { search },
      document: {
        body: { dataset: { uiVersion: version } },
        getElementById: id => id === 'camp-deep-guide' ? root : view,
      },
      fetch: url => {
        requests.push(url);
        return new Promise(resolve => {
          finish = () => resolve({ ok: !failure, json: async () => report });
        });
      },
    };
    vm.createContext(context);
    for (const dependency of ['directions', 'camp-planning'])
      vm.runInContext(read('assets/' + dependency + '.js'), context);
    vm.runInContext(code, context);
    return { window, root, view, requests, rendered, jumped, finish: () => finish() };
  }

  const landing = mount(true);
  assert.deepEqual(landing.requests, [], 'A non-camp route must not fetch dossiers');
  landing.view.hidden = false;
  const loading = landing.window.mountCampDossiers();
  assert.equal(landing.window.mountCampDossiers(), loading, 'Repeated renders must share the request');
  assert.deepEqual(landing.requests, [reportPath + '?v=' + version]);
  landing.finish();
  await loading;
  assert(landing.rendered.length === 1 && landing.rendered[0] === report, landing.root.innerHTML.slice(0, 240));
  assert.equal(landing.window.mountCampDossiers(), loading);

  const deepLink = mount(false, '?camp=' + encodeURIComponent(slug));
  assert.deepEqual(deepLink.requests, [reportPath + '?v=' + version]);
  deepLink.finish();
  await deepLink.window.mountCampDossiers();
  assert.deepEqual(deepLink.jumped, [slug], 'A cold dossier URL must open after the fetch');

  const leave = mount(false, '?camp=' + encodeURIComponent(slug));
  leave.view.hidden = true;
  leave.finish();
  await leave.window.mountCampDossiers();
  assert.deepEqual(leave.jumped, [], 'Leaving during the fetch must not scroll back to camps');
  leave.view.hidden = false;
  await leave.window.mountCampDossiers();
  assert.deepEqual(leave.jumped, [slug], 'Returning to the same URL must follow its pending dossier');
  await leave.window.mountCampDossiers();
  assert.deepEqual(leave.jumped, [slug], 'A render must not reopen an already applied dossier');


  const error = mount(false, '', true);
  error.finish();
  await error.window.mountCampDossiers();
  assert(error.root.innerHTML.includes(reportPath.replace('.json', '.md')));
  assert.deepEqual(error.rendered, []);
  console.log((locale || 'ru') + ': camp requests deferred, shared, versioned and deep links preserved');
}

(async () => {
  for (const locale of ['', 'es']) await verifyEdition(locale);
})().catch(error => { console.error(error); process.exitCode = 1; });
