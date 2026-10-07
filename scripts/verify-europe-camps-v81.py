"""Independent own-date/cohort checks and full previous-catalogue preservation."""
import json,re,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v81'
BASE='1c1ed0c5c34aac0a6c247fa885b16104ac40c4e7'
def before(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};events={e['id']:e for e in d['events']}
assert len(old)==2731 and len(events)==len(d['events'])==2741
assert all(events.get(k)==v for k,v in old.items())
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[k]==b[k],k
c=d['camp_programmes'];p={q['slug']:q for q in c['profiles']};op={q['slug']:q for q in b['camp_programmes']['profiles']}
assert len(op)==402 and len(p)==415 and all(p[k]==v for k,v in op.items())
assert c['profiles'][:402]==b['camp_programmes']['profiles']
assert c['counts']['countries']==33 and c['counts']['source_urls']==653 and c['counts']['swiss']==59
for iso,n in [('DEU',11),('AUT',3),('NLD',5),('CHE',59),('FRA',35),('ESP',28),('TWN',23),('SGP',52),('JPN',17),('KOR',8),('USA',38),('CAN',51),('CRI',7),('MEX',24)]:
    assert sum(q['iso']==iso for q in p.values())==n
assert sum(e['block']=='Лагеря' for e in events.values())==1410
assert len(c['generated_event_ids'])==947 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==27
assert len(c['shortlist'])==90 and c['shortlist'][:86]==b['camp_programmes']['shortlist']
assert c['gaps'][:-4]==b['camp_programmes']['gaps']
assert all(len(s['slugs'])==len(set(s['slugs'])) and all(k in p for k in s['slugs']) for s in c['shortlist'][-4:])
new=[e for k,e in events.items() if k not in old]
assert len(new)==10 and all(e['block']=='Лагеря' and e['checked']=='2026-10-05' for e in new)
def rows(slug):return [e for e in new if e['camp_dossier_slug']==slug]
expected={'salem-kids-2027':1,'landheim-general-2027':1,'stgis-general-2027':2,'stgis-robotics-ai-2027':1,
          'yoyo-fez-july':1,'yoyo-fez-august':1,'yoyo-steglitz-2027':1,'yoyo-ruppin-autumn':1,'yoyo-ruppin-spanish':1}
assert {s:len(rows(s)) for s in expected}==expected
assert {e['camp_dossier_slug'] for e in new}==set(expected)
assert len(set(p)-set(op))==13

# Compare independent cached booking tables, not the authored session list.
for slug,key,stamp,cohort,price in [
    ('yoyo-fez-july','yoyo-fez-dates','19.07. - 23.07.27','6 - 12','429,00 €'),
    ('yoyo-fez-august','yoyo-fez-dates','02.08. - 06.08.27','8 - 13','429,00 €'),
    ('yoyo-steglitz-2027','yoyo-steglitz-dates','02.08. - 06.08.27','8 - 12','419,00 €'),
    ('yoyo-ruppin-autumn','yoyo-autumn-dates','18.10. - 24.10.26','8-15','699,00 €'),
    ('yoyo-ruppin-spanish','yoyo-spanish-dates','08.08. - 13.08.27','12-14','659,00 €')]:
    t=(PRIMARY/(key+'.txt')).read_text();assert stamp in t and cohort in t and price in t
    m=re.fullmatch(r'(\d{2})\.(\d{2})\. - (\d{2})\.(\d{2})\.(\d{2})',stamp)
    a,am,z,zm,y=m.groups();pair=('20'+y+'-'+am+'-'+a,'20'+y+'-'+zm+'-'+z)
    assert {(e['start'],e['end']) for e in rows(slug)}=={pair}
    assert all(e['attendance_weekdays']==['MO','TU','WE','TH','FR'] for e in rows(slug)) if 'fez' in slug or 'steglitz' in slug else True
assert p['yoyo-fez-july']['family_fit']['oscar']['status']=='conditional'
for s in ['yoyo-fez-august','yoyo-steglitz-2027']:assert p[s]['family_fit']['oscar']['status']=='not_eligible'
assert 'Bald buchbar' in p['yoyo-fez-july']['timing']['label']
closed=p['yoyo-ruppin-autumn'];assert closed['availability']['status']=='closed' and rows(closed['slug'])[0]['availability']==closed['availability']
assert 'Ausgebucht' in (PRIMARY/'yoyo-autumn-dates.txt').read_text()
assert 'Saturday' in closed['accommodation'] and '15 дней' in p['yoyo-fez-july']['price']['deposit']
assert p['yoyo-ruppin-spanish']['confirmed_instruction_languages']==['ES','EN']

l=p['landheim-general-2027'];form=(PRIMARY/'landheim-contract.txt').read_text()
assert 'International Summer Camp 2027' in form and '9 – 14 years' in form
assert 'All international students attend one of the German courses.' in form
assert '2,750 €' in form and 'including transfer from/to Munich airport/main station' in form
assert 'Robotics' in form and 'Building AI agents (no-code/low-code)' in form
assert not l['confirmed_instruction_languages'] and 'international students' in l['language']
assert {(e['start'],e['end']) for e in rows(l['slug'])}=={('2027-07-31','2027-08-14')}
assert all('robotics' not in e['themes'] and 'ai' not in e['themes'] for e in rows(l['slug']))
assert 'Summer Camp 2026' in (PRIMARY/'landheim-brochure.txt').read_text()
assert not p['landheim-ai-future']['timing']['sessions'] and p['landheim-ai-future']['price']['year'] is None
assert p['landheim-ai-future']['family_fit']['matvey']['status']=='later'
s=p['salem-kids-2027'];t=(PRIMARY/'salem-kids.txt').read_text()
assert '3.650 €' in t and '9–11' in t and '2027' in t
assert s['price']['year']==2027 and '1 ноября' in s['timing']['label'] and s['language_evidence_role']=='language_lessons'
t=(PRIMARY/'stgis.txt').read_text();assert '12–15 with at least B2 English level' in t and '4,180 €' in t and 'Surcharge 400 EUR' in t
s=p['stgis-robotics-ai-2027'];assert s['price']['label'].startswith('EUR 4 580') and s['family_fit']['matvey']['status']=='later'
assert s['confirmed_instruction_languages']==['EN'] and '404' in s['price']['deposit']
assert {(e['start'],e['end']) for e in rows(s['slug'])}=={('2027-08-08','2027-08-21')}
for slug,eid in [('newtech-autumn-art','L132'),('newtech-christmas-film','L133'),('newtech-christmas-art','L134')]:
    assert not rows(slug) and p[slug]['related_event_ids']==[eid]
    assert p[slug]['calendar_links'][0]['kind']=='existing_programme' and p[slug]['calendar_links'][0]['event_ids']==[eid]
    assert p[slug]['language_evidence_role']=='bilingual' and p[slug]['confirmed_instruction_languages']==['EN','NL']
    assert p[slug]['price']['year'] is None and p[slug]['family_fit']['oscar']['status']=='later'

report=json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text())
again=json.loads(json.dumps(d));integrate(again,report);assert again==d
for file,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:
    assert json.loads((ROOT/'dist/downloads'/file).read_text())==wanted
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2741
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==415
con.close()
def calendar(raw):
    out={};t=raw.decode().replace('\r\n ','').replace('\r\n\t','')
    for ch in t.split('BEGIN:VEVENT')[1:]:
        fields={line.split(':',1)[0]:line.split(':',1)[1] for line in ch.split('END:VEVENT')[0].splitlines() if ':' in line}
        assert fields['UID'] not in out;out[fields['UID']]=fields
    return out
file='dist/downloads/STEM_подтвержденные_даты.ics';prior=calendar(before(file));now=calendar((ROOT/file).read_bytes())
assert len(prior)==2066 and len(now)==2073 and len(set(now)-set(prior))==7 and set(prior)<=set(now)
for uid,val in prior.items():
    assert now[uid].get('DTSTART;VALUE=DATE')==val.get('DTSTART;VALUE=DATE')
    assert now[uid].get('DTEND;VALUE=DATE')==val.get('DTEND;VALUE=DATE')
excluded={'stgis-robotics-ai-2027','yoyo-ruppin-spanish','yoyo-ruppin-autumn'}
assert set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in new if e['camp_dossier_slug'] not in excluded}
file='dist/downloads/STEM_крупные_выставки.ics';expo=calendar((ROOT/file).read_bytes());oldexpo=calendar(before(file))
assert len(expo)==104 and set(expo)==set(oldexpo)
for uid,val in oldexpo.items():assert {k:v for k,v in expo[uid].items() if k!='DTSTAMP'}=={k:v for k,v in val.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text())
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==81
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version80' in plan['previous_goal_turn_classification']['evidence']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert plan['camp_catalog_integration']['dossiers']==415 and d['coverage_summary']['fully_audited_countries']==0
for stem in ['europe-camp-audit-v81','europe-camp-source-receipts-v81']:
    val=json.loads((ROOT/'data'/f'{stem}.json').read_text())
    assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==val
    assert not any(val['external_actions'].values())
assert len(val['sources'])==27 and sum(v.get('status')==200 for v in val['sources'])==23
assert len(val['dossier_source_urls_added'])==19 and len(val['visual_primary_reads'])==1
assert 'data-ui-version="81"' in (ROOT/'dist/index.html').read_text()
assert 'STEM_europe_camp_audit_v81.json' in (ROOT/'dist/assets/camp-programmes.js').read_text()
print(json.dumps(dict(passed=True,preserved_events=2731,preserved_dossier_ids=402,new_dossiers=13,new_calendar_rows=10,new_family_ics=7,
    events=2741,dossiers=415,family_ics=2073,exhibition_ics=104,worldwide_complete=False)))
