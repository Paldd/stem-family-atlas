"""Preserve the published atlas and verify real availability/age distinctions."""
import json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
BASE='fa7b404a93fef05041e415c69fb16a76dd39ca8c'
def oldfile(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(oldfile('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={x['id']:x for x in b['events']};ev={x['id']:x for x in d['events']}
assert len(old)==2254 and len(ev)==len(d['events'])==2295
assert all(ev.get(k)==v for k,v in old.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
p={x['slug']:x for x in d['camp_programmes']['profiles']};op={x['slug']:x for x in b['camp_programmes']['profiles']}
assert len(p)==221 and len(set(p)-set(op))==23 and all(p[k]==v for k,v in op.items())
c=d['camp_programmes'];assert c['counts']['countries']==28 and c['counts']['swiss']==35 and c['counts']['source_urls']==391
assert sum(x['block']=='Лагеря' for x in ev.values())==964
assert len(c['generated_event_ids'])==501 and c['integration']['reused_legacy_events']==58 and c['integration']['seasonal_windows']==12
assert len(c['shortlist'])==35 and c['shortlist'][:31]==b['camp_programmes']['shortlist']
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==c
plan=json.loads((ROOT/'data/research-plan.json').read_text())
assert plan['status']=='active' and plan['previous_goal_turn_classification']['classification']=='progress'
assert 'Version67' in plan['previous_goal_turn_classification']['evidence']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[x for k,x in ev.items() if k not in old];assert len(new)==41
assert all(x['block']=='Лагеря' and x['checked']=='2026-10-05' for x in new)
for slug in set(p)-set(op):
 q=p[slug];assert q['iso'] in ['USA','CAN'] and q['checked']=='2026-10-05' and not q['related_event_ids']
 assert all(x['checked']==q['checked'] and x['url'].startswith('https://') for x in q['sources'])
 assert q['formats'] in [['day'],['boarding']]
assert len(p['cody-general']['timing']['sessions'])==7 and p['cody-general']['family_fit']['oscar']['status']=='conditional'
assert p['cody-general']['confirmed_instruction_languages']==['EN'] and p['cody-general']['language_evidence_role']=='camp_life'
assert not p['birch-hill']['confirmed_instruction_languages'] and len(p['birch-hill']['timing']['sessions'])==6
assert p['birch-hill']['family_fit']['oscar']['status']=='candidate' and 'входят deposit' in p['birch-hill']['price']['deposit']
assert len(p['weequahic-general']['timing']['sessions'])==3 and '8 400' in p['weequahic-general']['price']['label'] and '14 450' in p['weequahic-general']['price']['label']
assert all(x['themes']==['general','sport','art','science'] for x in new if x['camp_dossier_slug']=='weequahic-general')
assert p['manitou-first-short']['eligibility_birth_years']==[2019,2020] and p['manitou-first-short']['family_fit']['matvey']['status']=='not_eligible'
assert p['manitou-second-short']['eligibility_birth_years']==list(range(2013,2021))
assert p['manitou-rookie-day']['eligibility_birth_years']==[2019,2020,2021] and p['manitou-rookie-day']['formats']==['day']
assert p['manitou-rookie-day']['family_fit']['matvey']['status']=='not_eligible'
for slug in ['manitou-long','manitou-first-short','manitou-second-short','manitou-rookie-day']:
 q=p[slug];assert q['confirmed_instruction_languages']==['EN'] and q['language_evidence_role']=='camp_life' and '13%' in q['price']['extras']
 assert '10 Camp Road' in q['place'] and '110 Camp Road' not in q['place']
ow=[q for k,q in p.items() if k.startswith('openworld-')];assert len(ow)==6
assert all(q['formats']==['day'] and not q['timing']['sessions'] and q['price']['year']==2026 and not q['confirmed_instruction_languages'] and q['timing']['status']=='partial_2027' for q in ow)
assert all(q['family_fit']['matvey']['status']=='not_eligible' and q['family_fit']['oscar']['status']=='candidate' for q in ow if q['slug'].startswith('openworld-explore-'))
assert all(q['family_fit']['matvey']['status']=='candidate' and q['family_fit']['oscar']['status']=='later' for q in ow if not q['slug'].startswith('openworld-explore-'))
assert p['robotfun-camps']['family_fit']['matvey']['status']==p['robotfun-camps']['family_fit']['oscar']['status']=='unknown'
for slug in ['rns-steam','rns-junior-coding','rns-senior-coding']:assert p[slug]['formats']==['day'] and not p[slug]['timing']['sessions'] and p[slug]['price']['year']==2026 and not p[slug]['confirmed_instruction_languages']
for slug,n in [('science-north-sudbury',7),('science-north-thunder',8)]:
 q=p[slug];assert len(q['timing']['sessions'])==n and q['confirmed_instruction_languages']==['EN'] and q['price']['season']=='2026/27'
 assert ['2026-12-21','2026-12-23'] in q['timing']['sessions'] and ['2026-12-29','2026-12-31'] in q['timing']['sessions']
 assert ['2027-03-15','2027-03-19'] in q['timing']['sessions']
 for x in new:
  if x['camp_dossier_slug']==slug:assert x['date_scope']=='day_camp_window' and x['attendance_weekdays']==['MO','TU','WE','TH','FR']
assert p['science-north-robo-ready']['timing']['sessions']==[['2026-11-20','2026-11-20']]
assert '9–11' in p['science-north-robo-ready']['timing']['label'] and len([x for x in new if x['camp_dossier_slug']=='science-north-robo-ready'])==1
closed={'science-north-beebots','science-north-cubetto'}
for slug in closed:
 q=p[slug];assert q['price']['year'] is None and q['confirmed_instruction_languages']==['EN']
 assert q['timing']['session_details'][0]['availability']['status']=='closed'
assert not p['science-north-robokids']['timing']['sessions'] and p['science-north-robokids']['family_fit']['oscar']['status']=='later'
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2295 and con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==221;con.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
  assert f['UID'] not in out;out[f['UID']]=(f.get('DTSTART;VALUE=DATE',f.get('DTSTART')),f.get('DTEND;VALUE=DATE',f.get('DTEND')))
 return out
fn='dist/downloads/STEM_подтвержденные_даты.ics';before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1585 and len(now)==1624 and len(set(now)-set(before))==39 and all(now.get(k)==v for k,v in before.items())
for x in new:assert ('stem-'+x['id']+'@family-stem.local' in now)==(x['camp_dossier_slug'] not in closed)
fn='dist/downloads/STEM_крупные_выставки.ics';assert calendar((ROOT/fn).read_bytes())==calendar(oldfile(fn)) and len(calendar(oldfile(fn)))==104
assert d['coverage_summary']['fully_audited_countries']==0
for stem in ['northamerica-camp-audit-v68','northamerica-camp-source-receipts-v68']:
 source=json.loads((ROOT/('data/'+stem+'.json')).read_text())
 assert json.loads((ROOT/('dist/downloads/STEM_'+stem.replace('-','_')+'.json')).read_text())==source
print(json.dumps(dict(prior_events_unchanged=2254,prior_dossiers_unchanged=198,new_dossiers=23,new_calendar_rows=41,new_family_ical=39,closed_workshops_excluded=2,openworld_without_new_dates=6,events=2295,dossiers=221,countries=28,official_urls=391,family_ical=1624,exhibition_ical=104,sqlite='ok',bridge='idempotent',worldwide_goal='active'),ensure_ascii=False))
