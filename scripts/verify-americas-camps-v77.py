"""Preserve existing work and test source-specific admission/calendar risks."""
import json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1];BASE='1207b5344138cd2d7a7d950aa5c8353f75bbece2'
def oldfile(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(oldfile('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
assert len(old)==2550 and len(ev)==len(d['events'])==2589
assert all(ev.get(k)==v for k,v in old.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
c=d['camp_programmes'];p={x['slug']:x for x in c['profiles']};op={x['slug']:x for x in b['camp_programmes']['profiles']}
assert len(op)==347 and len(p)==363 and all(p.get(k)==v for k,v in op.items())
assert [p[k]['id'] for k in p if k in op]==[op[k]['id'] for k in op]
assert c['counts']['countries']==33 and c['counts']['source_urls']==558
for iso,n in [('CHE',53),('FRA',33),('ESP',27),('TWN',21),('SGP',45),('JPN',14),('KOR',7)]:assert sum(x['iso']==iso for x in p.values())==n
assert len(c['generated_event_ids'])==795 and c['integration']['reused_legacy_events']==65 and c['integration']['seasonal_windows']==19
assert len(c['shortlist'])==72 and c['shortlist'][:67]==b['camp_programmes']['shortlist']
for name,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/name).read_text())==wanted
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[v for k,v in ev.items() if k not in old];assert len(new)==39 and all(e['block']=='Лагеря' and e['checked']=='2026-10-05' for e in new)
def rows(slug):return [e for e in new if e['camp_dossier_slug']==slug]
assert len(rows('olympia-regular'))==5 and rows('olympia-regular')[-1]['end']=='2027-08-06'
assert len(rows('olympia-spark'))==2 and '10-летия' in p['olympia-spark']['family_fit']['matvey']['detail']
assert len(rows('winaukee-rookie'))==1 and 'Grades1–4' in p['winaukee-rookie']['age']
assert 'закончился 01.10.2026' in p['winaukee-rookie']['price']['extras']
assert len(rows('eagle-ridge-leadership'))==10 and '120/125' in c['gaps'][-4]['detail']
for s,n in [('cedar-mini',6),('cedar-regular',4)]:
 assert len(rows(s))==n and p[s]['confirmed_instruction_languages']==['EN'] and p[s]['language_evidence_role']=='camp_life'
 assert p[s]['price']['year'] is None and '2026' in p[s]['price']['deposit']
assert not rows('cuddles-winter') and p['cuddles-winter']['timing']['precision']=='season_window'
assert not p['cuddles-winter']['confirmed_instruction_languages'] and 'ISO-валюта неизвестна' in p['cuddles-winter']['price']['label']
for s in ['integem-junior','integem-young']:
 assert not rows(s) and p[s]['confirmed_instruction_languages']==['EN'] and p[s]['price']['year'] is None
 assert 'остаются' in p[s]['programme'] and not p[s]['timing']['sessions']
assert p['integem-junior']['family_fit']['matvey']['status']=='not_eligible' and p['integem-young']['family_fit']['oscar']['status']=='later'
assert len(rows('wildroots-marine'))==4 and not any(e['start']=='2027-03-22' for e in rows('wildroots-marine'))
assert p['wildroots-marine']['family_fit']['matvey']['status']=='unknown' and not p['wildroots-marine']['confirmed_instruction_languages']
for s in ['ucr-pacific-archive','utp-tecnocamp-archive','galileo-cuenca']:assert not rows(s) and not p[s]['timing']['sessions']
assert p['ucr-pacific-archive']['related_event_ids']==['L120'] and '2025' in p['ucr-pacific-archive']['timing']['label']
assert p['utp-tecnocamp-archive']['family_fit']['oscar']['status']=='unknown'
assert 'не совпадает' in p['galileo-cuenca']['timing']['label']
lesson_dates=set()
for s in ['cube-grade1','cube-grade45']:
 assert len(rows(s))==2 and not p[s]['confirmed_instruction_languages'] and 'CA$275' in p[s]['price']['label']
 for e in rows(s):
  assert e['date_scope']=='session_days' and len(e['sessions'])==8
  assert all(v['timezone']=='America/Toronto' for v in e['sessions'])
  lesson_dates.update(v['date'] for v in e['sessions'])
assert len(lesson_dates)==16 and not {'2027-02-13','2027-05-22'}&lesson_dates
assert any('formaldiagnosis' in g['detail'] for g in c['gaps'][-4:])
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
  assert f['UID'] not in out;out[f['UID']]=f
 return out
fn='dist/downloads/STEM_подтвержденные_даты.ics';before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1857 and len(now)==1924 and len(set(now)-set(before))==67
for uid,v in before.items():
 assert now[uid].get('DTSTART;VALUE=DATE')==v.get('DTSTART;VALUE=DATE')
 assert now[uid].get('DTEND;VALUE=DATE')==v.get('DTEND;VALUE=DATE')
for e in new:
 if e['date_scope']=='session_days':
  assert 'stem-'+e['id']+'@family-stem.local' not in now
  for v in e['sessions']:assert 'stem-'+e['id']+'-'+v['date']+'@family-stem.local' in now
 else:assert 'stem-'+e['id']+'@family-stem.local' in now
fn='dist/downloads/STEM_крупные_выставки.ics';ex=calendar((ROOT/fn).read_bytes());oldex=calendar(oldfile(fn));assert len(ex)==104 and set(ex)==set(oldex)
for uid,v in oldex.items():assert {k:z for k,z in ex[uid].items() if k!='DTSTAMP'}=={k:z for k,z in v.items() if k!='DTSTAMP'}
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite');assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2589 and con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==363;con.close()
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==77
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version76' in plan['previous_goal_turn_classification']['evidence']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['americas-camp-audit-v77','americas-camp-source-receipts-v77']:
 a=json.loads((ROOT/('data/'+stem+'.json')).read_text());assert json.loads((ROOT/('dist/downloads/STEM_'+stem.replace('-','_')+'.json')).read_text())==a
assert len(a['verified_new_dossier_urls'])==26 and len(a['sources'])==29 and sum(v.get('status')==200 for v in a['sources'])==28
assert all(v is False for v in a['external_actions'].values())
html=(ROOT/'dist/index.html').read_text();assert 'data-ui-version="77"' in html and '?v=76' not in html
assert 'STEM_americas_camp_audit_v77.json' in (ROOT/'dist/assets/camp-programmes.js').read_text()
ui=(ROOT/'dist/assets/camp-programmes.js').read_text()
assert 'Отдельные занятия:' in ui and 'Кружок · ' in ui and 'variant.sessions.length' in ui
print(json.dumps(dict(passed=True,preserved_events=2550,preserved_dossier_ids=347,new_dossiers=16,new_calendar_rows=39,new_family_ics=67,
 events=2589,dossiers=363,family_ics=1924,exhibition_ics=104,worldwide_complete=False)))
