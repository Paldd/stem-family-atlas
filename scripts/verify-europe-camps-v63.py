"""Preservation, campus reuse, future age gates and exported-calendar evidence."""
import json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
BASE='2786c5bac4f8a622f1ab737aa6236764e20095ba'
def oldfile(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(oldfile('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};rows={e['id']:e for e in d['events']}
assert len(rows)==len(d['events'])==2077 and all(rows[k]==v for k,v in old.items())
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[k]==b[k],k
p={x['slug']:x for x in d['camp_programmes']['profiles']};oldp={x['slug']:x for x in b['camp_programmes']['profiles']}
assert all(p[k]==v for k,v in oldp.items()) and len(p)==141 and len(set(p)-set(oldp))==16
assert d['camp_programmes']['counts']['countries']==28 and d['camp_programmes']['counts']['swiss']==25
assert d['camp_programmes']['counts']['source_urls']==262
assert len(d['camp_programmes']['generated_event_ids'])==283 and d['camp_programmes']['integration']['reused_legacy_events']==50
assert sum(e['block']=='Лагеря' for e in rows.values())==746
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==d['camp_programmes']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==json.loads((ROOT/'data/research-plan.json').read_text())
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[e for e in rows.values() if e['id'] not in old];assert len(new)==36
assert all(e['checked']=='2026-10-05' and e['block']=='Лагеря' for e in new)
g=p['techspark-games'];assert len(g['timing']['sessions'])==25 and len(g['calendar_links'])==25
assert sum(x['kind']=='existing_programme' for x in g['calendar_links'])==22
# Same-date July sessions in three cities must preserve only their own stable IDs.
for variant,link in zip(g['timing']['session_details'],g['calendar_links']):
 assert link['start']==variant['start'] and link['end']==variant['end']
 if link['kind']=='existing_programme':
  assert link['event_ids']==variant['legacy_event_ids'] and len(link['event_ids'])==1
  event=rows[link['event_ids'][0]];assert event['source']==variant['source']
 else:assert variant['place']==rows[link['event_ids'][0]]['city']
py=p['techspark-python'];assert len(py['timing']['sessions'])==24
assert not any(v['start']=='2027-10-11' for v in py['timing']['session_details'])
assert sum(v.get('availability',{}).get('status')=='closed' for v in py['timing']['session_details'])==1
assert all(v['family_fit']['matvey']['status']=='later' for v in py['timing']['session_details'] if v['start']<'2027-01-01')
lego=p['techspark-lego'];assert not lego['timing']['sessions'] and '6+' in lego['age'] and '12+' in lego['age']
assert lego['price']['year'] is None
assert p['lyceum-board']['confirmed_instruction_languages']==['EN'] and p['lyceum-board']['price']['year']==2027
assert len(p['lyceum-board']['timing']['sessions'])==3 and '12 800' in p['lyceum-board']['price']['label'] and '400' in p['lyceum-board']['price']['label']
assert p['lyceum-junior']['age']=='6–9' and len(p['lyceum-junior']['timing']['sessions'])==4
assert p['lyceum-junior']['themes']==['general','languages','sport']
assert p['champittet-leadership']['family_fit']['matvey']['status']=='later' and p['champittet-leadership']['family_fit']['oscar']['status']=='later'
assert p['saintcharles-camp']['price']['year'] is None and not p['saintcharles-camp']['timing']['sessions']
assert p['roches-ai']['price']['year']==2026 and p['roches-ai']['family_fit']['matvey']['status']=='later'
assert p['jm-juniors']['family_fit']['matvey']['status']=='not_eligible'
assert p['jm-scientists']['themes']==['robotics','coding','science'] and '8–9' in p['jm-campers']['age']
for k in ['jm-juniors','jm-campers','jm-scientists']:
 assert 'мае 2027' in p[k]['timing']['label'] and p[k]['timing']['sessions']==[] and p[k]['price']['year']==2026
assert 'НЕ' in p['saintdenis-kids']['timing']['label'] and not p['saintdenis-kids']['timing']['sessions']
for k in ['life-tech','stgeorge-barcelona','chester-english','ai-alicante']:
 assert p[k]['price']['year']==2026 and not p[k]['timing']['sessions']
assert '200' in p['stgeorge-barcelona']['price']['deposit'] and '750' in p['chester-english']['price']['deposit']
assert p['ai-alicante']['family_fit']['oscar']['status']=='unknown'
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2077
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==141
con.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
  assert f['UID'] not in out
  out[f['UID']]=(f.get('DTSTART;VALUE=DATE',f.get('DTSTART')),f.get('DTEND;VALUE=DATE',f.get('DTEND')))
 return out
fn='dist/downloads/STEM_подтвержденные_даты.ics';before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1406 and len(now)==1436 and all(now.get(k)==v for k,v in before.items())
assert len(set(now)-set(before))==30
for e in new:
 included='stem-'+e['id']+'@family-stem.local' in now
 excluded=e.get('availability',{}).get('status')=='closed' or (e['mat'].startswith('Нет') and e['osc'].startswith('Нет'))
 assert included!=excluded,(e['id'],included,excluded)
fn='dist/downloads/STEM_крупные_выставки.ics';assert calendar((ROOT/fn).read_bytes())==calendar(oldfile(fn)) and len(calendar(oldfile(fn)))==104
print(json.dumps(dict(prior_events_preserved=2041,prior_dossiers_preserved=125,new_dossiers=16,new_catalogue_dates=36,reused_campus_dates=22,dossiers=141,countries=28,swiss=25,official_urls=262,family_ical=1436,exhibition_ical=104,sqlite='ok',bridge='idempotent'),ensure_ascii=False))
