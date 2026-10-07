"""Preserve prior work and check the new source-specific calendar/admission risks."""
import json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1];BASE='d40d30c58c0a1fa34cd02a443cef2d1eea67bfcf'
def oldfile(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(oldfile('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
assert len(old)==2589 and len(ev)==len(d['events'])==2604 and all(ev.get(k)==v for k,v in old.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
c=d['camp_programmes'];p={x['slug']:x for x in c['profiles']};op={x['slug']:x for x in b['camp_programmes']['profiles']}
assert len(op)==363 and len(p)==376
assert all(p[k]['id']==v['id'] for k,v in op.items())
assert all(p[k]==v for k,v in op.items() if k not in ['montana-zug','madrid-chess-robotics'])
assert c['counts']['countries']==33 and c['counts']['source_urls']==587
for iso,n in [('CHE',59),('FRA',35),('ESP',28),('GBR',5),('TWN',21),('SGP',45),('JPN',14),('KOR',7)]:assert sum(x['iso']==iso for x in p.values())==n
assert len(c['generated_event_ids'])==810 and c['integration']['reused_legacy_events']==66 and c['integration']['seasonal_windows']==25
assert len(c['shortlist'])==78 and c['shortlist'][:72]==b['camp_programmes']['shortlist']
for name,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/name).read_text())==wanted
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[v for k,v in ev.items() if k not in old];assert len(new)==15 and all(e['block']=='Лагеря' and e['checked']=='2026-10-05' for e in new)
def rows(s):return [e for e in new if e['camp_dossier_slug']==s]
z=p['montana-zug'];assert len(rows('montana-zug'))==2 and z['price']['year']==2027 and z['timing']['precision']=='published_sessions'
assert z['timing']['sessions']==[['2027-07-04','2027-07-17'],['2027-07-04','2027-07-24']]
assert '4 800' in z['price']['label'] and '8 900' in z['price']['label'] and 'дополнительный' in z['price']['deposit']
assert z['language_evidence_role']=='language_lessons' and z['confirmed_instruction_languages']==['EN']
assert not rows('ecolint-intro-robotics') and p['ecolint-intro-robotics']['related_event_ids']==['L296']
assert p['ecolint-intro-robotics']['calendar_links'][0]['event_ids']==['L296']
for s in ['ecolint-intro-robotics','ecolint-science','ecolint-film','ecolint-multiactivity-half']:
 assert p[s]['confirmed_instruction_languages']==['EN','FR'] and p[s]['language_evidence_role']=='bilingual'
assert p['ecolint-film']['family_fit']['matvey']['status']=='conditional' and '9-летия' in p['ecolint-film']['family_fit']['matvey']['detail']
for s,n in [('ecolint-science',1),('ecolint-film',1),('ecolint-multiactivity-half',1),('stgeorge-winter-day',1),('stgeorge-winter-board',1),('lpb-issy-movers',4),('lpb-issy-juniors',4)]:assert len(rows(s))==n
assert p['stgeorge-winter-board']['family_fit']['matvey']['status']=='conditional'
for s in ['stgeorge-winter-day','stgeorge-winter-board']:
 assert p[s]['family_fit']['oscar']['status']=='later' and not p[s]['confirmed_instruction_languages'] and '2023' in p[s]['price']['deposit']
for s in ['lpb-issy-movers','lpb-issy-juniors']:
 assert p[s]['confirmed_instruction_languages']==['EN'] and '259' in p[s]['price']['label'] and 'конфликт' in p[s]['price']['label']
 assert all(e['date_scope']=='day_camp_window' and e['attendance_weekdays']==['MO','TU','WE','TH','FR'] for e in rows(s))
assert p['lpb-issy-juniors']['family_fit']['oscar']['status']=='later'
assert not rows('samiad-multiactivity') and len(p['samiad-multiactivity']['calendar_links'])==6
assert p['samiad-multiactivity']['timing']['precision']=='season_window' and p['samiad-multiactivity']['confirmed_instruction_languages']==['EN']
for s in ['funtech-mod-day','funtech-redstone-day','funtech-tonbridge-board']:
 assert not rows(s) and not p[s]['timing']['sessions'] and p[s]['price']['year'] is None and not p[s]['confirmed_instruction_languages']
 assert p[s]['related_event_ids']==['L012']
assert p['funtech-tonbridge-board']['family_fit']['oscar']['status']=='later'
for s in ['madrid-chess-robotics','madrid-manga']:
 assert not rows(s) and p[s]['confirmed_instruction_languages']==['ES'] and p[s]['timing']['precision']=='season_window'
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
  assert f['UID'] not in out;out[f['UID']]=f
 return out
fn='dist/downloads/STEM_подтвержденные_даты.ics';before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1924 and len(now)==1939 and len(set(now)-set(before))==15
for uid,v in before.items():
 assert now[uid].get('DTSTART;VALUE=DATE')==v.get('DTSTART;VALUE=DATE')
 assert now[uid].get('DTEND;VALUE=DATE')==v.get('DTEND;VALUE=DATE')
for e in new:assert 'stem-'+e['id']+'@family-stem.local' in now
fn='dist/downloads/STEM_крупные_выставки.ics';ex=calendar((ROOT/fn).read_bytes());oldex=calendar(oldfile(fn));assert len(ex)==104 and set(ex)==set(oldex)
for uid,v in oldex.items():assert {k:z for k,z in ex[uid].items() if k!='DTSTAMP'}=={k:z for k,z in v.items() if k!='DTSTAMP'}
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite');assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2604 and con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==376;con.close()
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==78
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version77' in plan['previous_goal_turn_classification']['evidence']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['europe-camp-audit-v78','europe-camp-source-receipts-v78']:
 a=json.loads((ROOT/('data/'+stem+'.json')).read_text());assert json.loads((ROOT/('dist/downloads/STEM_'+stem.replace('-','_')+'.json')).read_text())==a
assert len(a['verified_new_dossier_urls'])==29 and len(a['sources'])==43 and sum(v.get('status')==200 for v in a['sources'])==42
assert all(v is False for v in a['external_actions'].values())
html=(ROOT/'dist/index.html').read_text();assert 'data-ui-version="78"' in html and '?v=77' not in html
assert 'STEM_europe_camp_audit_v78.json' in (ROOT/'dist/assets/camp-programmes.js').read_text()
print(json.dumps(dict(passed=True,preserved_events=2589,preserved_dossier_ids=363,new_dossiers=13,updated_dossiers=2,new_calendar_rows=15,new_family_ics=15,
 events=2604,dossiers=376,family_ics=1939,exhibition_ics=104,worldwide_complete=False)))
