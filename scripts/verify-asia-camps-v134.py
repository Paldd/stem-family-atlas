"""Verify preservation, selected primary clauses and complete portable exports."""
import hashlib, io, json, re, sqlite3, subprocess, zipfile
from collections import Counter
from decimal import Decimal
from camp_asia_v134 import ROOT, BASE, NEW, AYLA

P = ROOT.parent / 'stem-family-atlas-work/camp-asia-primary-v134'

def prior(name):
    return subprocess.check_output(['git', 'show', BASE + ':' + name], cwd=ROOT)

b = json.loads(prior('data/catalog.json'))
d = json.loads((ROOT / 'data/catalog.json').read_text())
old = {p['slug']: p for p in b['camp_programmes']['profiles']}
new = {p['slug']: p for p in d['camp_programmes']['profiles']}
assert len(old) == 1098 and len(new) == 1102 and set(new) - set(old) == set(NEW)
assert all(old[s] == new[s] for s in old if s != 'ayla-tokyo')
ayla_old, ayla = old['ayla-tokyo'], new['ayla-tokyo']
assert {k for k in ayla_old if ayla_old[k] != ayla[k]} == {'programme', 'timing', 'price', 'sources', 'checked'}
assert len(ayla['timing']['session_details']) == len(ayla_old['timing']['session_details']) == 24
for x, y in zip(ayla_old['timing']['session_details'], ayla['timing']['session_details']):
    assert {k: v for k, v in x.items() if k != 'price'} == {k: v for k, v in y.items() if k != 'price'}
    assert y['price'] == x['price'].replace('Extended 09–15:', 'Regular 09–15:')
assert {k: v for k, v in ayla_old['timing'].items() if k != 'session_details'} == {k: v for k, v in ayla['timing'].items() if k != 'session_details'}
for x, y in zip(ayla_old['sources'], ayla['sources']):
    assert y == (dict(x, checked='2026-10-06') if x['url'] == AYLA else x)
assert ayla['price']['label'] == ayla_old['price']['label'].replace('Extended 5 дней', 'Regular09–15 5 дней')
assert ayla['price']['extras'] == ayla_old['price']['extras'].replace('Extended 200 000 / Super 220 000', 'Extended09–17 200 000 / Super Extended09–18 220 000')
assert {k: v for k, v in ayla['price'].items() if k not in ['label', 'extras']} == {k: v for k, v in ayla_old['price'].items() if k not in ['label', 'extras']}

oe = {e['id']: e for e in b['events']}
ne = {e['id']: e for e in d['events']}
ayla_ids = {k for k, e in oe.items() if e.get('camp_dossier_slug') == 'ayla-tokyo'}
assert len(oe) == 3806 and len(ne) == 3808 and len(ayla_ids) == 24
assert all(oe[k] == ne[k] for k in oe if k not in ayla_ids)
for k in ayla_ids:
    x, y = oe[k], ne[k]
    assert {f for f in x if x[f] != y[f]} <= {'gear', 'cost', 'checked', 'note'}
    for f in ['gear', 'cost', 'note']:
        numeric_text = y[f]
        if f == 'note':
            numeric_text = numeric_text.replace('Extended09–17', 'Extended').replace('Super Extended09–18', 'Super')
        assert re.findall(r'\d+(?:[,.]\d+)*', x[f]) == re.findall(r'\d+(?:[,.]\d+)*', numeric_text), (k, f)
added = {k: ne[k] for k in set(ne) - set(oe)}
assert set(added) == {'CP1099-20261121-20261126', 'CP1102-20261123-20261125'}
assert all(e['block'] == 'Лагеря' and e['date_scope'] == 'camp_session' for e in added.values())
assert Counter(e['block'] for e in d['events']) == dict(Соревнования=1157, События=197, Лагеря=2454)
assert added['CP1099-20261121-20261126']['deadline'] == '2026-11-15'
assert not added['CP1102-20261123-20261125']['deadline']

for slug in NEW:
    p = new[slug]
    assert p['confirmed_instruction_languages'] == [] and 'не установлен' in p['language']
assert new[NEW[0]]['price']['unit'] == 'unconfirmed'
assert new[NEW[0]]['family_fit']['oscar']['status'] == 'later'
assert new[NEW[1]]['family_fit']['oscar']['status'] == 'conditional'
assert new[NEW[1]]['family_fit']['matvey']['status'] == 'unknown'
assert new[NEW[1]]['timing']['precision'] == 'season_window'
assert all(link['kind'] == 'season_window' and not link['event_ids'] for link in new[NEW[1]]['calendar_links'])
assert not new[NEW[2]]['calendar_links']
assert new[NEW[1]]['timing']['sessions'] == [['2026-11-21', '2026-11-26']]
assert not new[NEW[2]]['timing']['sessions'] and 'после девятого' in new[NEW[2]]['family_fit']['matvey']['detail']
assert '20:00/20:30' in new[NEW[3]]['timing']['session_details'][0]['label']
assert 'SGD принята по местному контексту' in new[NEW[3]]['price']['label']
assert d['camp_planning']['offers'][:-1] == b['camp_planning']['offers'] and len(d['camp_planning']['offers']) == 57
q = d['camp_planning']['offers'][-1]
assert q['id'] == 'nature-quest-both-standard' and q['currency'] == 'SGD' and q['price_year'] == 2026
assert Decimal('356') * Decimal('1.09') == Decimal('388.04')
assert q['base_by_child'] == {'matvey': 388.04, 'oscar': 388.04} and sum(q['base_by_child'].values()) == 776.08
assert q['unknown_required'] and q['unknown_trip'] and not q['required'] and not q['optional']
for field in ['school_focus', 'school_history', 'schools', 'development_routes', 'leagues', 'family_strategy', 'league_guide']:
    assert d[field] == b[field], field
assert len(d['league_guide']['profiles']) == 142
review = d['camp_programmes']['family_review']
assert review['coverage'] == dict(candidates=64, countries=16, fully_audited_countries=0)
assert review['entries'][:-2] == b['camp_programmes']['family_review']['entries']
assert d['camp_programmes']['shortlist'][:-2] == b['camp_programmes']['shortlist']
assert d['camp_programmes']['gaps'][:-3] == b['camp_programmes']['gaps']

def clause(file, *words):
    def norm(s):
        return ''.join(s.lower().replace('–', '-').replace('’', "'").split())
    t = norm((P / (file + '.txt')).read_text())
    for word in words:
        assert norm(word) in t, (file, word)

clause('edutech-course', 'ages 7 to 15', 'November 21 to 26, 2026', '5th Family AI Ideathon', '5–6-year-old builders joining with their parents', 'transportation', 'all meals (lunches, dinners and coffee breaks)', 'Registration and payment by 15 November', '$1,500.00')
clause('edutech-industry', '48.5 supervised hours', 'S$200 - S$1,500', 'changes by organiser that has yet to be reviewed', '21 Nov 2026, Saturday', '26 Nov 2026, Thursday')
clause('edutech-home', 'AI for Tweens (ages 9 to 14)', '2-hour customised weekend classes on a rolling basis', '18 September midnight')
clause('nature-quest', '23 November 2026', '24 November 2026', '25 November 2026', '5 - 10 Years Old', '$356.00 / per pax (before GST)', '$145.00 / per pax (before GST)', '31 Oct 2026', '9AM - 8PM', '8:30pm (25 Nov)', '131 Pasir Ris Road', '21 Beach View')
clause('ayla-camp', '1 Day Prime 9 - 13:00 ¥8,000 per day', '1 Day Regular 9 - 15:00 ¥10,000 per day', '1 Day Extended 9 - 17:00 ¥12,000 per day', '1 Day Super Extended 9 - 18:00 ¥13,000 per day', 'non-refundable and non-transferable', '10% consumption tax')
clause('sg-gst', 'Standard-rated supplies (9% GST)')
receipts = json.loads((ROOT / 'data/asia-camps-source-receipts-v134.json').read_text())
assert len(receipts['sources']) == 11 and not any(receipts['external_actions'].values())
for r in receipts['sources']:
    raw = (P / r['raw_filename']).read_bytes()
    assert r['status'] == 200 and len(raw) == r['bytes'] and hashlib.sha256(raw).hexdigest() == r['sha256']

def blocks(raw):
    matches = re.findall(br'BEGIN:VEVENT\r\n.*?END:VEVENT\r\n', raw, re.S)
    out = {re.search(br'(?m)^UID:([^\r\n]+)', v).group(1): v for v in matches}
    assert len(out) == len(matches)
    return out

raw = (ROOT / 'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes()
assert not re.search(br'(?<!\r)\n', raw)
assert all(len(line) <= 75 for line in raw.split(b'\r\n'))
for line in raw.split(b'\r\n'):
    line.decode('utf-8')
before = blocks(prior('dist/downloads/STEM_подтвержденные_даты.ics'))
after = blocks(raw)
assert len(before) == 3022 and len(after) == 3025
modified = {('stem-' + k + '@family-stem.local').encode() for k in ayla_ids}
assert all(before[k] == after[k] for k in before if k not in modified)
for k in modified:
    for field in [b'UID', b'DTSTART;VALUE=DATE', b'DTEND;VALUE=DATE']:
        expression = br'(?m)^' + re.escape(field) + br':[^\r\n]+'
        assert re.findall(expression, before[k]) == re.findall(expression, after[k])
expected = {('stem-' + k + '@family-stem.local').encode() for k in added}
expected.add(b'stem-CP1099-20261121-20261126-deadline@family-stem.local')
assert set(after) - set(before) == expected
assert (ROOT / 'dist/downloads/STEM_крупные_выставки.ics').read_bytes() == prior('dist/downloads/STEM_крупные_выставки.ics')

def portable(meta, kind):
    m = json.loads((ROOT / 'dist/downloads' / meta).read_text())
    a = (ROOT / 'dist/downloads' / m['download']).read_bytes()
    assert m['complete_database'] and len(a) == m['archive_bytes'] and hashlib.sha256(a).hexdigest() == m['archive_sha256']
    with zipfile.ZipFile(io.BytesIO(a)) as z:
        assert z.testzip() is None and z.namelist() == [m[kind + '_entry'], 'README.txt']
        body = z.read(m[kind + '_entry'])
    assert len(body) == m[kind + '_bytes'] and hashlib.sha256(body).hexdigest() == m[kind + '_sha256']
    assert m['raw_download_available'] == (len(body) <= 26214400)
    return body

assert json.loads(portable('STEM_database_json_download.json', 'json')) == d
sql = portable('STEM_database_download.json', 'sqlite')
(P / 'verified-v134.sqlite').write_bytes(sql)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as z:
    (P / 'baseline-v133.sqlite').write_bytes(z.read('STEM_database.sqlite'))
c, oc = sqlite3.connect(P / 'verified-v134.sqlite'), sqlite3.connect(P / 'baseline-v133.sqlite')
assert c.execute('PRAGMA integrity_check').fetchone()[0] == 'ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
tables = [x[0] for x in oc.execute("SELECT name FROM sqlite_master WHERE type='table'")]
assert tables == [x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
for t in tables:
    a, z = oc.execute('SELECT * FROM ' + t).fetchall(), c.execute('SELECT * FROM ' + t).fetchall()
    if t == 'metadata':
        am, zm = dict(a), dict(z)
        assert {k for k in am if am[k] != zm[k]} == {'camp_family_review', 'camp_focus', 'completeness_audit', 'camp_planning'}
    elif t == 'events':
        zm = {v[0]: v for v in z}
        assert all(x == zm[x[0]] for x in a if x[0] not in ayla_ids)
        for x in a:
            if x[0] in ayla_ids:
                y = zm[x[0]]
                assert x[:9] == y[:9] and x[10] == y[10]
                assert json.loads(y[11]) == ne[x[0]]
    elif t == 'camp_programmes':
        zm = {v[0]: v for v in z}
        assert all(x == zm[x[0]] for x in a if x[0] != 'CP183')
        x, y = next(x for x in a if x[0] == 'CP183'), zm['CP183']
        assert x[:4] == y[:4] and json.loads(y[5]) == ayla
    elif t == 'countries':
        assert [v for v in a if v[0] != 'SGP'] == [v for v in z if v[0] != 'SGP']
        x, y = next(v for v in a if v[0] == 'SGP'), next(v for v in z if v[0] == 'SGP')
        assert x[:3] == y[:3]
        record = json.loads(x[3]); record['camps'] += 2; record['dated'] += 2
        assert record == json.loads(y[3])
    elif t in ['sources', 'event_countries', 'event_themes', 'camp_programme_sources', 'camp_programme_events']:
        assert set(a) <= set(z), t
    else:
        assert a == z, t
c.close(); oc.close()

plan, bp = json.loads((ROOT / 'data/research-plan.json').read_text()), json.loads(prior('data/research-plan.json'))
for field in ['human_scope_expansion', 'next_research']:
    assert plan[field] == bp[field], field
assert plan['status'] == plan['native_goal_status'] == 'active'
assert plan['current_publication']['status'] == 'prepared_local_not_published'
assert plan['latest_validation']['version'] == 134 and plan['latest_validation']['fully_audited_countries'] == 0
assert json.loads((P / 'native-site-check.json').read_text())['structuredContent']['error_data']['code'] == 404
result = dict(version=134, status='passed', baseline_commit=BASE,
    unchanged_event_objects=3782, updated_ayla_event_objects=24, unchanged_dossiers=1097,
    unchanged_budget_objects=56, unchanged_guide_profiles=142, new_dossiers=4,
    new_calendar_rows=2, new_budget_scenarios=1, source_bodies_hash_verified=11,
    old_ics_blocks_byte_identical=2998, old_ayla_ics_dates_and_uids_preserved=24,
    new_ics_entries=3, exhibition_ics_byte_identical=True,
    complete_sqlite_bytes=len(sql), complete_json_matches_catalog=True,
    all_old_sqlite_entity_rows_preserved_except_scoped_ayla_tariff_update=True,
    young_family_component_not_full_camp_admission=True, ideathon_exact_day_not_invented=True,
    unknown_fee_unit_not_multiplied=True, english_site_not_instruction_language=True,
    invoice_currency_and_pickup_time_conflict_preserved=True, standard_gst_math_verified=True,
    unchanged_worldwide_goal_scope=True, goal='active', worldwide_complete=False,
    publication='prepared_local_not_published')
(P / 'independent-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result))
