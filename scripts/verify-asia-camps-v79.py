"""Verify stable identities, source/age boundaries and real calendar coverage."""
import json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
BASE='041a7a448142dbfc71a58a19e6640fd7c2cda419'
def before(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
b=json.loads(before('data/catalog.json'))
d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};events={e['id']:e for e in d['events']}
assert len(old)==2604 and len(events)==len(d['events'])==2621
assert all(events.get(k)==v for k,v in old.items())
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[k]==b[k],k
c=d['camp_programmes'];p={q['slug']:q for q in c['profiles']};op={q['slug']:q for q in b['camp_programmes']['profiles']}
assert len(op)==376 and len(p)==389
assert {k for k,v in op.items() if p[k]!=v}=={'nullspace','camp-sfs'}
assert all(p[k]['id']==v['id'] for k,v in op.items())
assert [q['id'] for q in c['profiles'][:376]]==[q['id'] for q in b['camp_programmes']['profiles']]
newslugs=set(p)-set(op);assert len(newslugs)==13
assert c['counts']['countries']==33 and c['counts']['source_urls']==604 and c['counts']['swiss']==59
for iso,n in [('TWN',23),('SGP',52),('JPN',17),('KOR',8),('FRA',35),('ESP',28)]:
    assert sum(q['iso']==iso for q in p.values())==n
assert sum(e['block']=='Лагеря' for e in events.values())==1290
assert len(c['generated_event_ids'])==827 and c['integration']['reused_legacy_events']==66 and c['integration']['seasonal_windows']==25
assert len(c['shortlist'])==82 and c['shortlist'][:78]==b['camp_programmes']['shortlist']
assert all(len(s['slugs'])==len(set(s['slugs'])) and all(k in p for k in s['slugs']) for s in c['shortlist'][-4:])
new=[e for k,e in events.items() if k not in old]
assert len(new)==17 and all(e['block']=='Лагеря' and e['checked']=='2026-10-05' for e in new)
def rows(slug):return [e for e in new if e['camp_dossier_slug']==slug]
for slug,n in [('see-future-dreamers',3),('see-esl-engineering',1),('nullspace-ev3-holiday',5),
               ('nullspace-ai-comic',3),('nullspace-ai-game',3),('oyis-winter-intensive',2)]:
    assert len(rows(slug))==n and len({e['id'] for e in rows(slug)})==n
    assert len({v['variant_key'] for v in p[slug]['timing']['session_details']})==n
for slug in ['see-future-dreamers','see-esl-engineering']:
    assert p[slug]['confirmed_instruction_languages']==['EN'] and p[slug]['language_evidence_role']=='primary'
    assert all((e['start'],e['end'])==('2027-01-25','2027-01-29') for e in rows(slug))
    assert '11.10.2026' in p[slug]['price']['label'] and 'insurance' in p[slug]['price']['extras']
assert 'Grades 3–6' in p['see-esl-engineering']['age'] and 'Grade 2' in p['see-esl-engineering']['age']
assert p['see-esl-engineering']['family_fit']['oscar']['status']=='conditional'
assert 'программируемая робототехника не заявлена' in p['see-esl-engineering']['programme']
null=[s for s in newslugs if s.startswith('nullspace-')];assert len(null)==7
for s in null:assert not p[s]['confirmed_instruction_languages']
assert all(e['attendance_weekdays']==['MO','TU','WE','TH'] for e in rows('nullspace-ev3-holiday'))
assert {(e['start'],e['end']) for e in rows('nullspace-ev3-holiday')}=={('2026-12-21','2026-12-24'),('2026-12-28','2026-12-31')}
for s in ['nullspace-ai-comic','nullspace-ai-game']:
    assert {e['start'] for e in rows(s)}=={'2026-10-12','2026-10-13'}
    assert all(e['start']==e['end'] for e in rows(s))
    assert p[s]['family_fit']['oscar']['status']=='later' and '137,50' in p[s]['price']['label']
for s in ['nullspace-minecraft-holiday','nullspace-3d-holiday','nullspace-stem-holiday','nullspace-fll-novice',
          'ea-summer-immersion-junior','ea-summer-immersion-primary','sfs-sailing']:
    assert not p[s]['timing']['sessions'] and not rows(s)
assert p['nullspace-minecraft-holiday']['price']['year']==p['nullspace-3d-holiday']['price']['year']==2026
assert '5×2' in p['nullspace-stem-holiday']['timing']['label'] and 'четырёхдневный' in p['nullspace-stem-holiday']['timing']['label']
assert '15 или 20' in p['nullspace-stem-holiday']['editorial_reason']
assert '30 часов / 12' in p['nullspace-fll-novice']['programme'] and 'опыт не требуется' in p['nullspace-fll-novice']['programme']
assert p['nullspace-fll-novice']['price']['year'] is None and p['nullspace-fll-novice']['family_fit']['oscar']['status']=='later'
assert p['oyis-winter-intensive']['confirmed_instruction_languages']==['EN'] and p['oyis-winter-intensive']['price']['year'] is None
assert {(e['start'],e['end']) for e in rows('oyis-winter-intensive')}=={('2026-12-14','2026-12-18'),('2026-12-21','2026-12-25')}
assert '20 октября' in p['oyis-winter-intensive']['timing']['label'] and 'других стран' in p['oyis-winter-intensive']['accommodation']
for s in ['ea-summer-immersion-junior','ea-summer-immersion-primary']:
    assert p[s]['price']['year']==2026 and p[s]['confirmed_instruction_languages']==['EN']
    assert p[s]['language_evidence_role']=='camp_life' and '2027' in p[s]['timing']['label']
assert 'зарегистрированному классу' in p['camp-sfs']['age'] and 'другой англоязычной школы' in p['camp-sfs']['questions'][0]
assert not p['sfs-sailing']['confirmed_instruction_languages'] and '2–5' in p['sfs-sailing']['age']
assert c['gaps'][:-4]==b['camp_programmes']['gaps']

# Canonical and downloadable data, as well as the shared bridge, must agree.
report=json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text())
again=json.loads(json.dumps(d));integrate(again,report);assert again==d
for file,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:
    assert json.loads((ROOT/'dist/downloads'/file).read_text())==wanted
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2621
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==389
con.close()

def calendar(raw):
    out={};t=raw.decode().replace('\r\n ','').replace('\r\n\t','')
    for ch in t.split('BEGIN:VEVENT')[1:]:
        fields={line.split(':',1)[0]:line.split(':',1)[1] for line in ch.split('END:VEVENT')[0].splitlines() if ':' in line}
        assert fields['UID'] not in out;out[fields['UID']]=fields
    return out
file='dist/downloads/STEM_подтвержденные_даты.ics';prior=calendar(before(file));now=calendar((ROOT/file).read_bytes())
assert len(prior)==1939 and len(now)==1956 and len(set(now)-set(prior))==17
for uid,oldcal in prior.items():
    assert now[uid].get('DTSTART;VALUE=DATE')==oldcal.get('DTSTART;VALUE=DATE')
    assert now[uid].get('DTEND;VALUE=DATE')==oldcal.get('DTEND;VALUE=DATE')
assert set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in new}
file='dist/downloads/STEM_крупные_выставки.ics';expo=calendar((ROOT/file).read_bytes());oldexpo=calendar(before(file))
assert len(expo)==104 and set(expo)==set(oldexpo)
for uid,val in oldexpo.items():
    assert {k:v for k,v in expo[uid].items() if k!='DTSTAMP'}=={k:v for k,v in val.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text())
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==79
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version78' in plan['previous_goal_turn_classification']['evidence']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert plan['camp_catalog_integration']['dossiers']==389 and d['coverage_summary']['fully_audited_countries']==0
for stem in ['asia-camp-audit-v79','asia-camp-source-receipts-v79']:
    val=json.loads((ROOT/'data'/f'{stem}.json').read_text())
    assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==val
    assert not any(val['external_actions'].values())
assert len(val['verified_new_dossier_urls'])==17 and len(val['sources'])==24
assert sum(v.get('status')==200 for v in val['sources'])==18
assert 'data-ui-version="79"' in (ROOT/'dist/index.html').read_text()
assert 'STEM_asia_camp_audit_v79.json' in (ROOT/'dist/assets/camp-programmes.js').read_text()
print(json.dumps(dict(passed=True,preserved_events=2604,preserved_dossier_ids=376,new_dossiers=13,updated_dossiers=2,
    new_calendar_rows=17,new_family_ics=17,events=2621,dossiers=389,family_ics=1956,exhibition_ics=104,worldwide_complete=False)))
