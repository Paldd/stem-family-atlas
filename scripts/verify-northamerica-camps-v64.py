"""Protect existing family records and audit new dates/grades/language evidence."""
import json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
BASE='e17b7fcf81ddd42cc54139f369d9c512533ea474'
def oldfile(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(oldfile('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};rows={e['id']:e for e in d['events']}
assert len(rows)==len(d['events'])==2111 and all(rows[k]==v for k,v in old.items())
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[k]==b[k],k
p={x['slug']:x for x in d['camp_programmes']['profiles']};oldp={x['slug']:x for x in b['camp_programmes']['profiles']}
assert all(p[k]==v for k,v in oldp.items()) and len(p)==152 and len(set(p)-set(oldp))==11
counts=d['camp_programmes']['counts'];assert counts['countries']==28 and counts['swiss']==25 and counts['source_urls']==291
assert len(d['camp_programmes']['generated_event_ids'])==317 and d['camp_programmes']['integration']['reused_legacy_events']==50
assert sum(e['block']=='Лагеря' for e in rows.values())==780
assert len(d['camp_programmes']['shortlist'])==23
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==d['camp_programmes']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==json.loads((ROOT/'data/research-plan.json').read_text())
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[e for e in rows.values() if e['id'] not in old];assert len(new)==34
allowed={'general','science','robotics','coding','sport','languages','art','ai','entrepreneurship'}
for slug in set(p)-set(oldp):
 q=p[slug];assert q['checked']=='2026-10-05' and set(q['themes'])<=allowed
 assert q['timing']['status'] in ['published_2027','partial_2027','next_unannounced']
 assert not q['related_event_ids'],'No shared-brand or similar-title fuzzy merges'
 assert all(s['checked']=='2026-10-05' and s['url'].startswith('https://') for s in q['sources'])
assert all(e['checked']=='2026-10-05' and e['block']=='Лагеря' for e in new)
astro=p['astrocamp-junior'];assert len(astro['timing']['sessions'])==3
assert not any(s[0] in ['2027-08-01','2027-08-02'] for s in astro['timing']['sessions'])
assert '1–7' in astro['timing']['label'] and '2–7' in astro['timing']['label'] and '7–12' in astro['age'] and '7–13' in astro['age']
assert not astro['confirmed_instruction_languages'] and astro['family_fit']['oscar']['status']=='conditional'
assert '60' in astro['price']['extras'] and astro['themes']==['general','science','sport']
assert len(p['frenchwoods-regular']['timing']['sessions'])==10
assert '8 800' in p['frenchwoods-regular']['price']['label'] and '8 400' in p['frenchwoods-regular']['price']['label']
assert p['frenchwoods-trial']['confirmed_instruction_languages']==['EN'] and p['frenchwoods-trial']['language_evidence_role']=='camp_life'
assert '250' in p['frenchwoods-trial']['price']['deposit'] and '1 750' in p['frenchwoods-trial']['price']['deposit']
assert not p['tic-robotics']['timing']['sessions'] and not p['tic-robotics']['confirmed_instruction_languages']
assert '1-й класс' in p['tic-robotics']['age'] and 'чтении' in p['tic-robotics']['family_fit']['oscar']['detail']
assert 'сентябре 2026' in p['ponacka-oneweek']['age'] and len(p['ponacka-oneweek']['timing']['sessions'])==6
assert p['ponacka-oneweek']['family_fit']['matvey']['status']=='unknown'
assert len(p['ponacka-twoweek']['timing']['sessions'])==4 and '1 июля 2027' in p['ponacka-twoweek']['age']
for k in ['ponacka-oneweek','ponacka-twoweek','ponacka-fourweek']:
 assert not p[k]['confirmed_instruction_languages'] and 'HST' in p[k]['price']['label'] and '300' in p[k]['price']['deposit']
assert p['ponacka-fourweek']['family_fit']['oscar']['status']=='later'
assert len(p['destination-canada']['timing']['sessions'])==5 and p['destination-canada']['family_fit']['matvey']['status']=='conditional'
assert 'USD' in p['destination-canada']['price']['label'] and p['destination-canada']['confirmed_instruction_languages']==['EN']
sw=p['swallowdale-forest'];assert sw['timing']['precision']=='season_window' and not any(x['event_ids'] for x in sw['calendar_links'])
assert sw['price']['year'] is None and sw['family_fit']['oscar']['status']=='later'
for k,n in [('ciss-ai-lab',2),('ciss-entrepreneurs',1)]:
 assert len(p[k]['timing']['sessions'])==n and p[k]['price']['year'] is None
 assert all(p[k]['family_fit'][x]['status']=='later' for x in ['matvey','oscar']) and p[k]['confirmed_instruction_languages']==['EN']
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2111
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==152;con.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
  assert f['UID'] not in out
  out[f['UID']]=(f.get('DTSTART;VALUE=DATE',f.get('DTSTART')),f.get('DTEND;VALUE=DATE',f.get('DTEND')))
 return out
fn='dist/downloads/STEM_подтвержденные_даты.ics';before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1436 and len(now)==1467 and all(now.get(k)==v for k,v in before.items()) and len(set(now)-set(before))==31
for e in new:
 included='stem-'+e['id']+'@family-stem.local' in now
 assert included!=(e['camp_dossier_slug'] in ['ciss-ai-lab','ciss-entrepreneurs'])
fn='dist/downloads/STEM_крупные_выставки.ics';assert calendar((ROOT/fn).read_bytes())==calendar(oldfile(fn)) and len(calendar(oldfile(fn)))==104
print(json.dumps(dict(prior_events_preserved=2077,prior_dossiers_preserved=141,new_dossiers=11,new_catalogue_dates=34,dossiers=152,countries=28,swiss=25,official_urls=291,family_ical=1467,exhibition_ical=104,sqlite='ok',bridge='idempotent'),ensure_ascii=False))
