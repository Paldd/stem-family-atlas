"""Meaningful preservation, programme eligibility and calendar integration checks."""
import json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
BASE='4916e69c616e19d5c70d550723c73ba8374de1c6'
def oldfile(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(oldfile('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
assert len(old)==2483 and len(ev)==len(d['events'])==2550
assert all(ev.get(k)==v for k,v in old.items() if k!='L143')
allowed={'checked','city','age','entry','cost','proof','note','deadline_note'}
assert {k for k in set(ev['L143'])|set(old['L143']) if ev['L143'].get(k)!=old['L143'].get(k)}==allowed
assert (ev['L143']['start'],ev['L143']['end'])==('2027-01-25','2027-01-29')
assert 'оплата и депозит не условие' in ev['L143']['entry'] and 'начальные классы' in ev['L143']['entry']
assert '96' in ev['L143']['city'] and '8 800' in ev['L143']['cost']
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[k]==b[k],k
c=d['camp_programmes'];p={x['slug']:x for x in c['profiles']};op={x['slug']:x for x in b['camp_programmes']['profiles']}
assert len(op)==322 and len(p)==347 and all(p.get(k)==v for k,v in op.items())
newslugs=set(p)-set(op);assert len(newslugs)==25
assert [p[k]['id'] for k in p if k in op]==[op[k]['id'] for k in op]
assert c['counts']['countries']==32 and c['counts']['swiss']==53 and c['counts']['source_urls']==532
for iso,count in [('FRA',33),('ESP',27),('TWN',21),('SGP',45),('JPN',14),('KOR',7)]:assert sum(x['iso']==iso for x in p.values())==count
assert sum(x['block']=='Лагеря' for x in ev.values())==1219
assert len(c['generated_event_ids'])==756 and c['integration']['reused_legacy_events']==65 and c['integration']['seasonal_windows']==18
assert len(c['shortlist'])==67 and c['shortlist'][:63]==b['camp_programmes']['shortlist']
for name,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/name).read_text())==wanted
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[x for k,x in ev.items() if k not in old];assert len(new)==67 and all(x['block']=='Лагеря' and x['checked']=='2026-10-05' for x in new)
def rows(s):return [x for x in new if x['camp_dossier_slug']==s]
weeks=[('2026-11-23','2026-11-27'),('2026-11-30','2026-12-04'),('2026-12-07','2026-12-11'),('2026-12-14','2026-12-18'),('2027-01-04','2027-01-08')]
empire=[s for s in newslugs if s.startswith('empire-') and s!='empire-post-psle'];assert len(empire)==10
for s in empire:
 assert [(x['start'],x['end']) for x in rows(s)]==weeks
 assert p[s]['confirmed_instruction_languages']==['EN'] and p[s]['price']['season']=='2026/27'
 assert p[s]['price']['year'] is None and 'SGD 430' in p[s]['price']['label']
 assert all(t.strip()==t for t in p[s]['themes'])
 assert all(x['attendance_weekdays']==['MO','TU','WE','TH','FR'] for x in rows(s))
assert p['empire-kubo']['family_fit']['matvey']['status']=='not_eligible' and p['empire-kubo']['family_fit']['oscar']['status']=='conditional'
assert p['empire-scratch']['family_fit']['matvey']['status']=='conditional' and p['empire-scratch']['age']=='7–9'
assert 'Tinkercad' in p['empire-3d']['programme'] and '10–16' in p['empire-3d']['programme']
assert p['empire-alvik']['age']=='11–12'
assert all(p[s]['family_fit'][k]['status']=='later' for s in ['empire-alvik','empire-unity','empire-ml'] for k in ['matvey','oscar'])
q=p['empire-post-psle'];assert not q['confirmed_instruction_languages'] and '570' in q['price']['label'] and 'закончились 04.10.2026' in q['price']['label']
assert len(rows(q['slug']))==1 and rows(q['slug'])[0]['start']=='2026-10-12' and '8–9' in q['family_fit']['matvey']['detail']
assert not any(x['id']=='L015' for x in new)
for s,price in [('lab-ai-young','230'),('lab-ai-mario','390')]:
 assert len(rows(s))==5 and not p[s]['confirmed_instruction_languages'] and price in p[s]['price']['label']
 assert 'без ISO' in p[s]['price']['label'] and p[s]['timing']['variant_keyed']
 assert len({x['id'] for x in rows(s)})==5
assert not any('jurong' in x['city'].lower() for x in rows('lab-ai-mario'))
assert not rows('grove-flight')
q=p['grove-flight'];assert q['confirmed_instruction_languages']==['EN'] and 'НЕ условие' in q['price']['deposit']
assert q['calendar_links']==[dict(start='2027-01-25',end='2027-01-29',kind='existing_programme',event_ids=['L143'])]
q=p['brown-ai-scientist'];assert 'G1–G3' in q['age'] and not q['confirmed_instruction_languages'] and 'G4' in q['family_fit']['matvey']['detail']
assert rows(q['slug'])[0]['start']=='2027-01-25' and rows(q['slug'])[0]['end']=='2027-02-03'
q=p['irobo-frozen'];assert len(rows(q['slug']))==3 and len({x['city'] for x in rows(q['slug'])})==2
assert not q['confirmed_instruction_languages'] and 'iOS' in q['price']['extras'] and 'laptop' in q['programme']
for s,role in [('wenzao-drama','camp_life'),('wenzao-languages','language_lessons')]:
 assert p[s]['language_evidence_role']==role and p[s]['confirmed_instruction_languages']==['EN']
 assert len(rows(s))==1 and rows(s)[0]['start']=='2027-01-21' and rows(s)[0]['end']=='2027-01-29'
archives=['asij-chofu','asij-roppongi','aoba-hikarigaoka','aoba-meguro','raim-junk','raim-octo','raim-ari']
for s in archives:assert not rows(s) and not p[s]['timing']['sessions'] and p[s]['price']['year']==2026 and p[s]['timing']['status']=='next_unannounced'
assert '2 апреля' in p['asij-chofu']['age'] and '126 000' in p['asij-chofu']['price']['label']
assert '131 000' in p['aoba-hikarigaoka']['price']['extras'] and '163 500' in p['aoba-hikarigaoka']['price']['extras']
assert 'PDF' in p['aoba-meguro']['family_fit']['oscar']['detail']
for s in ['raim-junk','raim-octo','raim-ari']:assert not p[s]['confirmed_instruction_languages'] and '1–3' in p[s]['age']

def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
  assert f['UID'] not in out;out[f['UID']]=f
 return out
fn='dist/downloads/STEM_подтвержденные_даты.ics';before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1805 and len(now)==1857 and len(set(now)-set(before))==52
for uid,prior in before.items():
 assert now[uid].get('DTSTART;VALUE=DATE')==prior.get('DTSTART;VALUE=DATE')
 assert now[uid].get('DTEND;VALUE=DATE')==prior.get('DTEND;VALUE=DATE')
for x in new:assert ('stem-'+x['id']+'@family-stem.local' in now)==(x['camp_dossier_slug'] not in ['empire-alvik','empire-unity','empire-ml'])
fn='dist/downloads/STEM_крупные_выставки.ics';ex=calendar((ROOT/fn).read_bytes());oldex=calendar(oldfile(fn))
assert len(ex)==104 and set(ex)==set(oldex)
for uid,prior in oldex.items():assert {k:v for k,v in ex[uid].items() if k!='DTSTAMP'}=={k:v for k,v in prior.items() if k!='DTSTAMP'}
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2550 and con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==347
con.close()
plan=json.loads((ROOT/'data/research-plan.json').read_text())
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==76
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version75' in plan['previous_goal_turn_classification']['evidence']
assert plan['camp_catalog_integration']['dossiers']==347 and plan['camp_catalog_integration']['generated_calendar_entries']==756
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['asia-camp-audit-v76','asia-camp-source-receipts-v76']:
 a=json.loads((ROOT/('data/'+stem+'.json')).read_text());assert json.loads((ROOT/('dist/downloads/STEM_'+stem.replace('-','_')+'.json')).read_text())==a
assert len(a['verified_new_dossier_urls'])==16 and all(v is False for v in a['external_actions'].values())
html=(ROOT/'dist/index.html').read_text();assert 'data-ui-version="76"' in html and '?v=75' not in html
assert 'STEM_asia_camp_audit_v76.json' in (ROOT/'dist/assets/camp-programmes.js').read_text()
print(json.dumps(dict(passed=True,preserved_events=2482,corrected_legacy_rows=1,preserved_dossier_ids=322,new_dossiers=25,
 new_calendar_rows=67,new_family_ics=52,events=2550,dossiers=347,family_ics=1857,exhibition_ics=104,worldwide_complete=False)))
