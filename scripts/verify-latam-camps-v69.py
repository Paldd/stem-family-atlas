"""Preserve prior records and verify starts, age gates and closed intake."""
import json, sqlite3, subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT = Path(__file__).resolve().parents[1]
BASE = 'b11a9168576e7800dc055467eaae31faaf8bba9a'
def oldfile(name):
    return subprocess.check_output(['git', 'show', BASE+':'+name], cwd=ROOT)
b = json.loads(oldfile('data/catalog.json'))
d = json.loads((ROOT/'data/catalog.json').read_text())
old = {x['id']: x for x in b['events']}
ev = {x['id']: x for x in d['events']}
assert len(old) == 2295 and len(ev) == len(d['events']) == 2321
assert all(ev.get(k) == v for k, v in old.items())
for key in ['league_guide', 'development_routes', 'schools', 'school_history', 'family_context', 'family_strategy', 'top_picks']:
    assert d[key] == b[key], key
c = d['camp_programmes']
p = {x['slug']: x for x in c['profiles']}
op = {x['slug']: x for x in b['camp_programmes']['profiles']}
assert len(p) == 242 and len(set(p)-set(op)) == 21
assert all(p.get(k) == v for k, v in op.items())
assert c['counts']['countries'] == 29 and c['counts']['swiss'] == 35 and c['counts']['source_urls'] == 409
assert sum(x['country'] == 'Франция' for x in p.values()) == 23
assert sum(x['country'] == 'Испания' for x in p.values()) == 19
assert sum(x['block'] == 'Лагеря' for x in ev.values()) == 990
assert len(c['generated_event_ids']) == 527 and c['integration']['reused_legacy_events'] == 58 and c['integration']['seasonal_windows'] == 12
assert len(c['shortlist']) == 39 and c['shortlist'][:35] == b['camp_programmes']['shortlist']
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text()) == d
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text()) == c
again = json.loads(json.dumps(d))
integrate(again, json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()))
assert again == d
new = [x for k, x in ev.items() if k not in old]
assert len(new) == 26 and all(x['block'] == 'Лагеря' and x['checked'] == '2026-10-05' for x in new)
for slug in set(p)-set(op):
    q = p[slug]
    assert q['iso'] in ['MEX', 'PER', 'COL', 'BRA'] and q['checked'] == '2026-10-05' and not q['related_event_ids']
    assert all(x['checked'] == q['checked'] and x['url'].startswith('https://') for x in q['sources'])
astra = {'astra-evkids': ('5–12', 5, None), 'astra-ev3': ('8–16', 4, None),
         'astra-arduino': ('10–17', 4, 2026), 'astra-electronica': ('10–16', 4, 2026), 'astra-esp32': ('12–17', 4, 2026)}
for slug, (age, n, year) in astra.items():
    q = p[slug]
    assert q['age'] == age and not q['confirmed_instruction_languages']
    assert q['timing']['status'] == 'partial_2027' and q['timing']['start_only']
    assert len(q['timing']['sessions']) == n and q['price']['year'] == year and 'Octubre' in q['price']['label']
    assert '2027 не подтверждена' in q['price']['label'] and '75 минут' in q['timing']['session_details'][0]['label']
    for v in q['timing']['session_details']:
        assert v['start'] == v['end'] and v['date_scope'] == 'activity_start'
        assert v['price'] == 'Тариф января 2027 не подтверждён'
        assert v['source'].endswith('?nivel='+slug.removeprefix('astra-'))
assert p['astra-evkids']['timing']['sessions'][-1] == ['2027-01-10', '2027-01-10']
assert p['astra-arduino']['family_fit']['matvey']['status'] == p['astra-electronica']['family_fit']['matvey']['status'] == 'conditional'
assert p['astra-esp32']['family_fit']['matvey']['status'] == p['astra-esp32']['family_fit']['oscar']['status'] == 'later'
mex = [x for k, x in p.items() if k not in op and x['iso'] == 'MEX']
assert len(mex) == 12 and all(not q['timing']['sessions'] and q['timing']['status'] == 'next_unannounced' and q['price']['year'] == 2026 and not q['confirmed_instruction_languages'] for q in mex)
assert p['machinecare-inicial']['age'] == '5–6' and p['machinecare-starter']['age'] == '6–8' and p['machinecare-explorer']['age'] == '9–11' and p['machinecare-deployer']['age'] == '12+'
assert p['machinecare-deployer']['family_fit']['matvey']['status'] == 'later'
assert p['trex-petit']['family_fit']['matvey']['status'] == 'not_eligible'
assert p['trex-vgames']['family_fit']['matvey']['status'] == 'candidate'
for slug in ['geeks-summer', 'geeks-chihuahua']:
    assert p[slug]['family_fit']['matvey']['status'] == p[slug]['family_fit']['oscar']['status'] == 'unknown'
assert 'IVA сверху' in p['irox-summer']['price']['label'] and p['unam-incubot']['age'] == '10–17'
assert p['llanada-co-day']['timing']['sessions'] == [['2026-10-05', '2026-10-09']] and p['llanada-co-day']['age'] == '6–12'
assert p['llanada-co-board']['timing']['sessions'] == [['2026-10-04', '2026-10-10']] and p['llanada-co-board']['age'] == '7–16'
assert 'не подтверждены' in p['llanada-co-board']['accommodation'] and 'недоступен' in p['llanada-co-board']['accommodation']
assert not any(s['url'].endswith('/sleepaway/') for s in p['llanada-co-board']['sources'])
assert next(x for x in new if x['camp_dossier_slug'] == 'llanada-co-day')['attendance_weekdays'] == ['MO', 'TU', 'WE', 'TH', 'FR']
q = p['international-camp-br']
assert q['confirmed_instruction_languages'] == ['EN'] and q['language_evidence_role'] == 'camp_life'
assert not q['timing']['sessions'] and q['price']['year'] is None and q['timing']['status'] == 'next_unannounced'
q = p['replago-general']
assert len(q['timing']['session_details']) == 3 and q['price']['year'] == 2027 and not q['confirmed_instruction_languages']
assert q['timing']['session_details'][-1]['availability']['status'] == 'closed'
assert '10 422' in q['price']['label'] and 6*1737 == 10422 > 9727
assert '11 142' in q['price']['label'] and 6*1857 == 11142 > 10400
assert '12 732' in q['price']['label'] and 6*2122 == 12732 > 11886
def calendar(raw):
    t = raw.decode().replace('\r\n ', '').replace('\r\n\t', '')
    out = {}
    for ch in t.split('BEGIN:VEVENT')[1:]:
        f = {x.split(':', 1)[0]: x.split(':', 1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert f['UID'] not in out
        out[f['UID']] = f
    return out
fn = 'dist/downloads/STEM_подтвержденные_даты.ics'
before = calendar(oldfile(fn)); now = calendar((ROOT/fn).read_bytes())
assert len(before) == 1624 and len(now) == 1645 and len(set(now)-set(before)) == 21
for uid, prior in before.items():
    assert now[uid].get('DTSTART;VALUE=DATE') == prior.get('DTSTART;VALUE=DATE') and now[uid].get('DTEND;VALUE=DATE') == prior.get('DTEND;VALUE=DATE')
for x in new:
    uid = 'stem-'+x['id']+'@family-stem.local'
    eligible = x['camp_dossier_slug'] != 'astra-esp32' and x.get('availability', {}).get('status') != 'closed'
    assert (uid in now) == eligible
    if uid in now and x['date_scope'] == 'activity_start':
        assert now[uid]['SUMMARY'].startswith('[Начало · полный период уточнить]')
        assert 'Тариф января 2027 не подтверждён' in x['cost']
fn = 'dist/downloads/STEM_крупные_выставки.ics'
exhibitions = calendar((ROOT/fn).read_bytes()); oldex = calendar(oldfile(fn))
assert len(exhibitions) == 104 and set(exhibitions) == set(oldex)
for uid, prior in oldex.items():
    assert exhibitions[uid].get('DTSTART;VALUE=DATE') == prior.get('DTSTART;VALUE=DATE') and exhibitions[uid].get('DTEND;VALUE=DATE') == prior.get('DTEND;VALUE=DATE')
con = sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0] == 2321 and con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0] == 242
con.close()
plan = json.loads((ROOT/'data/research-plan.json').read_text())
assert plan['status'] == plan['native_goal_status'] == 'active' and plan['latest_validation']['version'] == 69
assert plan['previous_goal_turn_classification']['classification'] == 'progress' and 'Version68' in plan['previous_goal_turn_classification']['evidence']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text()) == plan
assert d['coverage_summary']['fully_audited_countries'] == 0
for stem in ['latam-camp-audit-v69', 'latam-camp-source-receipts-v69']:
    source = json.loads((ROOT/('data/'+stem+'.json')).read_text())
    assert json.loads((ROOT/('dist/downloads/STEM_'+stem.replace('-', '_')+'.json')).read_text()) == source
print(json.dumps(dict(prior_events_unchanged=2295, prior_dossiers_unchanged=221, new_dossiers=21, new_calendar_rows=26, new_family_ical=21, course_starts=21, waitlist_excluded=1, both_too_young_excluded=4, events=2321, dossiers=242, countries=29, official_urls=409, family_ical=1645, exhibition_ical=104, sqlite='ok', bridge='idempotent', worldwide_goal='active'), ensure_ascii=False))
