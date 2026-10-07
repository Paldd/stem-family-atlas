"""Verify v136 against selected primary clauses and the committed v135 exports."""
import hashlib, io, json, re, sqlite3, subprocess, unicodedata, zipfile
from collections import Counter
from datetime import date, timedelta
from camp_asia_v136 import ROOT, BASE, NEW

P = ROOT.parent / 'stem-family-atlas-work/camp-eastasia-primary-v136'

def prior(path):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT)

def norm(text):
    return ''.join(unicodedata.normalize('NFKC', text).lower().split())

def clause(file, *words):
    text = norm((P / (file + '.txt')).read_text())
    for word in words:
        assert norm(word) in text, (file, word)

b = json.loads(prior('data/catalog.json'))
d = json.loads((ROOT / 'data/catalog.json').read_text())
op = {p['slug']: p for p in b['camp_programmes']['profiles']}
np = {p['slug']: p for p in d['camp_programmes']['profiles']}
oe = {e['id']: e for e in b['events']}
ne = {e['id']: e for e in d['events']}
assert len(op) == 1102 and len(np) == 1119 and set(np) - set(op) == set(NEW)
updated_profiles = {'jasmine-nola', 'jasmine-winter-block'}
assert all(op[s] == np[s] for s in op if s not in updated_profiles)
assert {k for k in np['jasmine-nola'] if np['jasmine-nola'][k] != op['jasmine-nola'][k]} == {'timing', 'price', 'sources', 'checked', 'calendar_links'}
assert {k for k in np['jasmine-winter-block'] if np['jasmine-winter-block'][k] != op['jasmine-winter-block'][k]} == {'price', 'sources', 'checked'}
old_price = op['jasmine-winter-block']['price']
assert {k: v for k, v in old_price.items() if k != 'deposit'} == {k: v for k, v in np['jasmine-winter-block']['price'].items() if k != 'deposit'}
for field in ['sessions', 'session_details']:
    assert np['jasmine-nola']['timing'][field][:-1] == op['jasmine-nola']['timing'][field]
assert {k: v for k, v in np['jasmine-nola']['price'].items() if k != 'label'} == {k: v for k, v in op['jasmine-nola']['price'].items() if k != 'label'}
assert re.findall(r'\d+', np['jasmine-nola']['price']['label']) == re.findall(r'\d+', op['jasmine-nola']['price']['label'])
assert 'не базовый тариф' in np['jasmine-nola']['price']['label']
changed = {k for k in oe if oe[k] != ne[k]}
assert changed == {e['id'] for e in b['events'] if e.get('camp_dossier_slug') in updated_profiles}
assert len(changed) == 6 and len(oe) == 3829 and len(ne) == 3847
assert all(oe[k] == ne[k] for k in oe if k not in changed)
for k in changed:
    fields = {f for f in ne[k] if ne[k][f] != oe[k][f]}
    assert fields == ({'references', 'checked', 'note'} if k.startswith('CP730-') else {'period', 'references', 'checked'})
    for f in ['start', 'end', 'deadline', 'age', 'cost', 'gear', 'priority']:
        assert oe[k][f] == ne[k][f], (k, f)
    for f in ['cost', 'gear']:
        assert re.findall(r'\d+(?:[,.]\d+)*', oe[k][f]) == re.findall(r'\d+(?:[,.]\d+)*', ne[k][f])
added = {k: ne[k] for k in set(ne) - set(oe)}
assert len(added) == 18 and all(e['block'] == 'Лагеря' for e in added.values())
assert Counter(e['block'] for e in d['events']) == dict(Соревнования=1168, События=207, Лагеря=2472)

# Independent date/grade/price tuples from the selected individual course pages.
courses = [
    ('isa-typjzs1', '2026-12-26', '2026-12-26', '2–4', 12800, '2026-11-21'),
    ('isa-typjzs4', '2026-12-27', '2026-12-27', '2–4', 12800, '2026-11-22'),
    ('isa-ospjza2', '2026-12-26', '2026-12-26', '3–6', 11000, '2026-11-21'),
    ('isa-ngpjza1', '2026-12-27', '2026-12-27', '3–6', 11000, '2026-11-22'),
    ('isa-kyoto', '2026-12-26', '2026-12-28', '3–6', 29800, '2026-11-21'),
    ('isa-typjz33', '2026-12-28', '2026-12-28', '3–9', 15800, '2026-11-23'),
    ('isa-typjbt1', '2027-01-04', '2027-01-05', '3–5', 44000, '2026-11-28'),
    ('isa-ngpjbj3', '2026-12-25', '2026-12-27', '4–9', 59000, '2026-11-20'),
    ('isa-typjbj9', '2026-12-26', '2026-12-28', '4–9', 59000, '2026-11-21'),
    ('isa-typjbj1', '2027-01-04', '2027-01-06', '4–9', 59000, '2026-11-30'),
    ('isa-typjbj0', '2027-01-04', '2027-01-06', '4–9', 59000, '2026-11-30'),
    ('isa-ospjbj3', '2027-01-04', '2027-01-06', '4–9', 53000, '2026-11-30'),
    ('isa-ospjbj4', '2027-01-04', '2027-01-06', '4–9', 57000, '2026-11-30'),
    ('isa-fkpjbj3', '2027-01-09', '2027-01-11', '4–9', 51000, '2026-12-05'),
    ('isa-sdpjbuk', '2026-12-30', '2026-12-31', '5–12', 49800, '2026-11-25'),
    ('isa-typjbo4', '2026-12-25', '2026-12-28', '4–9', 245000, '2026-11-20'),
]
isa_events = []
for slug, (file, start, end, grade, price, deadline) in zip(NEW[:16], courses):
    profile = np[slug]
    events = [e for e in added.values() if e.get('camp_dossier_slug') == slug]
    assert len(events) == 1
    e = events[0]; isa_events.append(e)
    assert (e['start'], e['end'], e['deadline']) == (start, end, deadline)
    assert grade in e['age'] and profile['iso'] == 'JPN'
    assert profile['family_fit']['oscar']['status'] == 'later'
    assert profile['family_fit']['matvey']['status'] == ('later' if grade == '5–12' else 'conditional')
    assert profile['confirmed_instruction_languages'] == ['EN']
    day = date.fromisoformat(start); last = date.fromisoformat(end); due = date.fromisoformat(deadline)
    clause(file, f'{day.year}年{day.month}月{day.day}日', f'{last.month}月{last.day}日', f'小学{grade.split("–")[0]}年', f'{price:,}円', f'{due.year}年{due.month}月{due.day}日')
    assert e['date_scope'] == 'camp_session' and e['source'] == profile['timing']['session_details'][0]['source']
clause('isa-typjbt1', '誤：2027年1月4日～1月6日（2泊3日）', '正：2027年1月4日～1月5日（1泊2日）', '2026年11月30日', '2026年11月28日', '食物アレルギー対応：不可')
drama = np['isa-drama-shinkiba']
assert '30 ноября' in drama['timing']['label'] and '28 ноября' in drama['timing']['label']
assert '30 ноября' in isa_events[6]['proof'] and '28 ноября' in isa_events[6]['action']
clause('isa-typjbj0', '9～14人部屋', '食物アレルギー対応：不可')
clause('isa-ospjbj3', '催行決定', '53,000円')
clause('isa-typjz33', '15,800円', '17,800円', '集合7:40/解散18:00', '集合8:40/解散17:00', '集合9:40/解散16:00')
clause('isa-terms', '日帰り旅行型プログラム (ISA×TGGスペシャルプログラム)', '10日目にあたる日以降', '全ての宿泊型プログラム', '20日目にあたる日以降', '遅刻・早退・⽋席に対する返金はございません', '全額')
clause('isa-typjbo4', '245,000円', '275,000円', '335,000円', '195,000円', '225,000円', '285,000円', 'お二人が同じホストファミリーに滞在できることを確約', 'お一人でお申し込みの場合')
assert np['isa-okinawa-homestay']['language_evidence_role'] == 'camp_life'
assert '155' not in np['isa-okinawa-homestay']['price']['label']
assert not np['isa-kyoto-winter']['timing']['session_details'][0].get('attendance_weekdays')

clause('jasmine-magic', '2027/01/25–01/29', '國小 1–4 年級（報名當下正在就讀的年級）', '授課英文、環境雙語', 'NT$13,800', 'NT$12,800', '2026/10/16', '每梯限額 30 人', '含午餐與保險', '每件 NT$300', '同一學員第二梯起', '需要用火、高溫', '第一版的測試紀錄')
clause('jasmine-rail', '2027/01/25–01/29', '2027/07/26–07/30', 'NT$16,800', 'NT$15,800', '5 天・含 1 夜（D4、瑞芳）', '不使用行李箱', '全程有領隊同行')
magic = np['jasmine-magic-winter']; winter = ne['CP729-20270125-20270129-winter-rail']
assert magic['formats'] == ['day'] and magic['language_evidence_role'] == 'bilingual'
assert all(magic['family_fit'][child]['status'] == 'conditional' for child in ['matvey', 'oscar'])
assert winter['priority'].startswith('P4') and 'Mandarin' in winter['priority']
assert 'одна ночь' in winter['gear'] and '4500/6000' in winter['note']
assert d['camp_planning']['offers'][:-2] == b['camp_planning']['offers']
for o, price in zip(d['camp_planning']['offers'][-2:], [12800, 13800]):
    assert o['slug'] == 'jasmine-magic-winter' and o['currency'] == 'TWD'
    assert o['base_by_child'] == {'matvey': price, 'oscar': price}
    assert sum(o['base_by_child'].values()) == price * 2
    assert o['optional'][0]['amount'] == 600 and o['discount_second'] == 0
    assert o['unknown_required'] and o['unknown_trip'] and not o['required']
for field in ['school_focus', 'school_history', 'schools', 'development_routes', 'leagues', 'family_strategy', 'league_guide']:
    assert d[field] == b[field], field
assert len(d['league_guide']['profiles']) == 144
assert d['camp_programmes']['family_review']['entries'][:-2] == b['camp_programmes']['family_review']['entries']
assert d['camp_programmes']['family_review']['coverage'] == dict(candidates=66, countries=16, fully_audited_countries=0)
assert d['camp_programmes']['shortlist'][:-2] == b['camp_programmes']['shortlist']
assert d['camp_programmes']['gaps'][:-1] == b['camp_programmes']['gaps']
assert 'EN/ES/RU преподавание не заявлено' in d['camp_programmes']['gaps'][-1]['detail']
assert not any('Seoul STEAM' in p['provider'] for p in np.values())
clause('ewha-application', '초등학교 2학년 ~ 6학년 60명', '40명 이상 확정', '2027년 1월 4일', '1월 22일', '재외동포 아동의 한국어', 'STEAM Program 5')
clause('jasmine-winter', '95%', '90%', '80%', '70%', '50%')
assert '95%' in np['jasmine-winter-block']['price']['deposit']
assert '41+' in np['jasmine-winter-block']['price']['deposit']
receipts = json.loads((ROOT / 'data/asia-camps-source-receipts-v136.json').read_text())
assert len(receipts['sources']) == 27 and not any(receipts['external_actions'].values())
bodies = [r for r in receipts['sources'] if r.get('http_status') == 200]
assert len(bodies) == 25
for r in bodies:
    raw = (P / r['raw_filename']).read_bytes()
    assert len(raw) == r['bytes'] and hashlib.sha256(raw).hexdigest() == r['sha256']
from pypdf import PdfReader
assert len(PdfReader(P / 'isa-terms.pdf').pages) == 4
with zipfile.ZipFile(P / 'ewha-application.docx') as z:
    assert 'word/document.xml' in z.namelist()
assert (P / 'ewha-brochure.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n')

def blocks(raw):
    matches = re.findall(br'BEGIN:VEVENT\r\n.*?END:VEVENT\r\n', raw, re.S)
    out = {re.search(br'(?m)^UID:([^\r\n]+)', v).group(1): v for v in matches}
    assert len(out) == len(matches)
    return out

raw = (ROOT / 'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes()
assert not re.search(br'(?<!\r)\n', raw)
assert all(len(line) <= 75 for line in raw.split(b'\r\n'))
for line in raw.split(b'\r\n'): line.decode('utf-8')
before = blocks(prior('dist/downloads/STEM_подтвержденные_даты.ics')); after = blocks(raw)
assert len(before) == 3033 and len(after) == 3064
changed_uids = {('stem-' + k + '@family-stem.local').encode() for k in changed}
assert all(before[k] == after[k] for k in before if k not in changed_uids)
for k in changed_uids:
    for field in [b'UID', b'DTSTART;VALUE=DATE', b'DTEND;VALUE=DATE']:
        expression = br'(?m)^' + re.escape(field) + br':[^\r\n]+'
        assert re.findall(expression, before[k]) == re.findall(expression, after[k])
included = [e for e in added.values() if not e['priority'].startswith('P4')]
expected = {('stem-' + e['id'] + '@family-stem.local').encode() for e in included}
expected |= {('stem-' + e['id'] + '-deadline@family-stem.local').encode() for e in included if e['deadline']}
assert len(included) == 16 and len(expected) == 31 and set(after) - set(before) == expected
for e in included:
    v = after[('stem-' + e['id'] + '@family-stem.local').encode()]
    assert ('DTSTART;VALUE=DATE:' + e['start'].replace('-', '')).encode() in v
    assert ('DTEND;VALUE=DATE:' + (date.fromisoformat(e['end']) + timedelta(days=1)).strftime('%Y%m%d')).encode() in v
assert (ROOT / 'dist/downloads/STEM_крупные_выставки.ics').read_bytes() == prior('dist/downloads/STEM_крупные_выставки.ics')

def portable(meta, kind):
    m = json.loads((ROOT / 'dist/downloads' / meta).read_text()); a = (ROOT / 'dist/downloads' / m['download']).read_bytes()
    assert m['complete_database'] and len(a) == m['archive_bytes'] and hashlib.sha256(a).hexdigest() == m['archive_sha256']
    with zipfile.ZipFile(io.BytesIO(a)) as z:
        assert z.testzip() is None and z.namelist() == [m[kind + '_entry'], 'README.txt']
        body = z.read(m[kind + '_entry'])
    assert len(body) == m[kind + '_bytes'] and hashlib.sha256(body).hexdigest() == m[kind + '_sha256']
    assert m['raw_download_available'] == (len(body) <= 26214400)
    return body

assert json.loads(portable('STEM_database_json_download.json', 'json')) == d
sql = portable('STEM_database_download.json', 'sqlite'); assert len(sql) > 26214400
(P / 'verified-v136.sqlite').write_bytes(sql)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as z:
    (P / 'baseline-v135.sqlite').write_bytes(z.read('STEM_database.sqlite'))
c = sqlite3.connect(P / 'verified-v136.sqlite'); oc = sqlite3.connect(P / 'baseline-v135.sqlite')
assert c.execute('PRAGMA integrity_check').fetchone()[0] == 'ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
assert {k: json.loads(v) for k, v in c.execute('SELECT id,record_json FROM events')} == ne
assert {json.loads(v)['slug']: json.loads(v) for v, in c.execute('SELECT record_json FROM camp_programmes')} == np
tables = [x[0] for x in oc.execute("SELECT name FROM sqlite_master WHERE type='table'")]
assert tables == [x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
for t in tables:
    a = oc.execute('SELECT * FROM ' + t).fetchall(); z = c.execute('SELECT * FROM ' + t).fetchall()
    if t == 'metadata':
        assert {k for k, v in a if dict(z)[k] != v} == {'completeness_audit', 'camp_planning', 'camp_focus', 'camp_family_review'}
    elif t == 'events':
        zm = {v[0]: v for v in z}; assert all(v == zm[v[0]] for v in a if v[0] not in changed)
        assert all(v[:9] == zm[v[0]][:9] and v[10] == zm[v[0]][10] for v in a if v[0] in changed)
    elif t == 'camp_programmes':
        updated_ids = {np[s]['id'] for s in updated_profiles}; zm = {v[0]: v for v in z}
        assert all(v == zm[v[0]] for v in a if v[0] not in updated_ids)
        assert all(v[:4] == zm[v[0]][:4] for v in a if v[0] in updated_ids)
    elif t == 'countries':
        zm = {v[0]: v for v in z}; assert all(v == zm[v[0]] for v in a if v[0] not in {'JPN', 'TWN'})
        for v in a:
            if v[0] not in {'JPN', 'TWN'}: continue
            y = zm[v[0]]; assert v[:3] == y[:3]
            r = json.loads(v[3]); increase = 16 if v[0] == 'JPN' else 2
            r['camps'] += increase; r['dated'] += increase; assert r == json.loads(y[3])
    elif t in ['sources', 'event_countries', 'event_themes', 'camp_programme_sources', 'camp_programme_events']:
        assert set(a) <= set(z), t
    else:
        assert a == z, t
c.close(); oc.close()
plan = json.loads((ROOT / 'data/research-plan.json').read_text()); bp = json.loads(prior('data/research-plan.json'))
for field in ['human_scope_expansion', 'next_research']: assert plan[field] == bp[field]
assert plan['status'] == plan['native_goal_status'] == 'active'
assert plan['current_publication']['status'] == 'prepared_local_not_published'
assert plan['latest_validation']['version'] == 136 and plan['latest_validation']['fully_audited_countries'] == 0
assert json.loads((P / 'native-site-check.json').read_text())['structuredContent']['error_data']['code'] == 404
assert json.loads((ROOT / '.openai/hosting.json').read_text())['project_id'] == 'appgprj_6abd44bca1348191809b7260dcb46d87'
result = dict(version=136, status='passed', baseline_commit=BASE,
    unchanged_event_objects=3823, updated_event_objects=6, unchanged_dossiers=1100,
    unchanged_budget_objects=57, unchanged_guide_profiles=144, new_dossiers=17,
    new_calendar_rows=18, new_budget_scenarios=2, source_bodies_hash_verified=25,
    old_ics_blocks_byte_identical=3027, old_updated_ics_dates_and_uids_preserved=6,
    new_ics_entries=31, exhibition_ics_byte_identical=True, complete_sqlite_bytes=len(sql),
    complete_json_matches_catalog=True, old_sqlite_entity_rows_preserved_except_six_scoped_events_and_two_dossiers=True,
    school_grade_not_birth_year=True, drama_date_correction_and_deadline_conflict_preserved=True,
    kyoto_weekend_dates_included=True, magic_english_teaching_bilingual_environment=True,
    early_not_sibling_discount=True, nola_one_included_night_not_extra_summer_price=True,
    nola_mandarin_and_grade5_hills_not_in_family_ics=True, korea_steam_title_not_english_robotics_proof=True,
    unchanged_worldwide_goal_scope=True, goal='active', worldwide_complete=False,
    publication='prepared_local_not_published')
(P / 'independent-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result))
