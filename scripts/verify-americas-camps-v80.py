"""Preservation and independent primary-calendar verification for v80."""
import json,re,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v80'
BASE='404545dbb212a3d6b841a25ee4531b825aaa1af3'
def before(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};events={e['id']:e for e in d['events']}
assert len(old)==2621 and len(events)==len(d['events'])==2731
assert all(events.get(k)==v for k,v in old.items())
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[k]==b[k],k
c=d['camp_programmes'];p={q['slug']:q for q in c['profiles']};op={q['slug']:q for q in b['camp_programmes']['profiles']}
assert len(op)==389 and len(p)==402 and all(p[k]==v for k,v in op.items())
assert c['profiles'][:389]==b['camp_programmes']['profiles']
newslugs=set(p)-set(op);assert len(newslugs)==13
assert c['counts']['countries']==33 and c['counts']['source_urls']==634 and c['counts']['swiss']==59
for iso,n in [('USA',38),('CAN',51),('CRI',7),('MEX',24),('COL',6),('TWN',23),('SGP',52),('JPN',17),('KOR',8),('FRA',35),('ESP',28)]:
    assert sum(q['iso']==iso for q in p.values())==n
assert sum(e['block']=='Лагеря' for e in events.values())==1400
assert len(c['generated_event_ids'])==937 and c['integration']['reused_legacy_events']==66 and c['integration']['seasonal_windows']==27
assert len(c['shortlist'])==86 and c['shortlist'][:82]==b['camp_programmes']['shortlist']
assert all(len(s['slugs'])==len(set(s['slugs'])) and all(k in p for k in s['slugs']) for s in c['shortlist'][-4:])
assert c['gaps'][:-4]==b['camp_programmes']['gaps']
new=[e for k,e in events.items() if k not in old]
assert len(new)==110 and all(e['block']=='Лагеря' and e['checked']=='2026-10-05' for e in new)
def rows(slug):return [e for e in new if e['camp_dossier_slug']==slug]
expected={'camp-muskoka-general':8,'muskoka-woods-wild':8,'muskoka-woods-venture':8,'robin-hood-day':4,
    'robin-hood-home-away':1,'robot-academy-full-day':2,'stem4-builders':21,'stem4-challengers':19,
    'stem4-engineers':19,'stem4-rookies':19,'ymca-colombia-ycamp':1}
assert {s:len(rows(s)) for s in expected}==expected
assert {e['camp_dossier_slug'] for e in new}==set(expected)
assert p['muskoka-woods-wild']['family_fit']['matvey']['status']=='not_eligible'
assert p['muskoka-woods-venture']['family_fit']['oscar']['status']=='not_eligible'
for s in ['muskoka-woods-wild','muskoka-woods-venture']:
    assert '6 часов' in p[s]['accommodation'] and 'Cabin Chat' in p[s]['accommodation']
    assert '14' in p[s]['price']['deposit'] and '15' in p[s]['price']['deposit']
    assert not p[s]['confirmed_instruction_languages'] and 'ISO' in p[s]['price']['label']
assert p['camp-muskoka-general']['price']['label'].startswith('CAD 1 695')
assert p['robin-hood-home-away']['family_fit']['oscar']['status']=='later' and 'Grades2–4' in p['robin-hood-home-away']['age']
assert {(e['start'],e['end']) for e in rows('robin-hood-day')}=={('2027-07-05','2027-07-16'),('2027-07-19','2027-07-30'),('2027-08-03','2027-08-13'),('2027-08-16','2027-08-27')}
assert '$280' in p['robin-hood-day']['price']['extras'] and '$190' in p['robin-hood-day']['price']['extras']
assert 'HST exempt' in p['robin-hood-day']['price']['extras'] and '31.10.2026' in p['robin-hood-day']['price']['label']
v=p['vgc-junior-family'];assert v['timing']['precision']=='season_window' and not rows(v['slug'])
assert v['confirmed_instruction_languages']==['EN'] and v['language_evidence_role']=='primary'
assert v['formats']==['day','family'] and v['family_fit']['oscar']['status']=='later' and v['price']['year']==2027
assert 'взрослый обязателен' in v['age'] and '2 845' in v['price']['label'] and '9 640' in v['price']['label']
assert '8–9 PDF' in v['price']['label'] and 'Семейный тариф по запросу' in v['price']['label']
assert len(v['calendar_links'])==2 and all(k['kind']=='season_window' and not k['event_ids'] for k in v['calendar_links'])
assert 'после7-летия' in p['stem4-rookies']['family_fit']['oscar']['detail']
for s in ['stem4-challengers','stem4-engineers']:assert p[s]['family_fit']['oscar']['status']=='later'

# Independent comparison to each course's fetched primary date table, including omitted last week.
months={'Jun':'06','Jul':'07','Aug':'08'}
for slug in ['stem4-builders','stem4-challengers','stem4-engineers','stem4-rookies']:
    t=(PRIMARY/(slug+'.txt')).read_text();t=re.sub(r'\s+',' ',t)
    ranges=set(re.findall(r'(Jun|Jul|Aug) (\d+) – (Jun|Jul|Aug) (\d+)',t))
    observed={('2027-'+months[a]+'-'+b.zfill(2),'2027-'+months[x]+'-'+y.zfill(2)) for a,b,x,y in ranges}
    summer=[e for e in rows(slug) if e['start']>='2027-06-01']
    assert {(e['start'],e['end']) for e in summer}==observed
    assert all(sum((e['start'],e['end'])==q for e in summer)==2 for q in observed)
    assert 'spring break, Apr 12–16' in t and len([e for e in rows(slug) if e['start']=='2027-04-12'])==1
    details=p[slug]['timing']['session_details'];assert len(details)==len({r['variant_key'] for r in details})
    assert all(e['attendance_weekdays']==['MO','TU','WE','TH','FR'] for e in rows(slug))
    assert not p[slug]['confirmed_instruction_languages'] and p[slug]['availability']['status']=='unknown'
    assert 'Опубликованные' not in p[slug]['availability']['label'] and 'остаётся' in p[slug]['price']['included']
spring=(PRIMARY/'stem4-spring.txt').read_text();assert 'Apr 12 – Apr 16' in spring and 'Spring 2027' in spring
assert '$570' in p['lincoln-epic-archive']['price']['label'] and not p['lincoln-epic-archive']['timing']['sessions']
assert p['lincoln-epic-archive']['price']['year']==2026 and p['lincoln-epic-archive']['confirmed_instruction_languages']==['ES','EN']
for k in ['matvey','oscar']:assert p['lincoln-epic-archive']['family_fit'][k]['status']=='later'
y=p['ymca-colombia-ycamp'];assert y['confirmed_instruction_languages']==['EN'] and y['price']['year']==2026
assert y['family_fit']['oscar']['status']=='later' and '8–13' in y['age']
assert [(e['start'],e['end']) for e in rows(y['slug'])]==[('2026-11-29','2026-12-04')]
assert 'Santandercito' in y['place'] and 'COP1 950 000' in y['price']['label'] and '2027' in y['timing']['label']
assert not p['robot-academy-full-day']['confirmed_instruction_languages'] and p['robot-academy-full-day']['price']['year'] is None

report=json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text())
again=json.loads(json.dumps(d));integrate(again,report);assert again==d
for file,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:
    assert json.loads((ROOT/'dist/downloads'/file).read_text())==wanted
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2731
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==402
con.close()
def calendar(raw):
    out={};t=raw.decode().replace('\r\n ','').replace('\r\n\t','')
    for ch in t.split('BEGIN:VEVENT')[1:]:
        fields={line.split(':',1)[0]:line.split(':',1)[1] for line in ch.split('END:VEVENT')[0].splitlines() if ':' in line}
        assert fields['UID'] not in out;out[fields['UID']]=fields
    return out
file='dist/downloads/STEM_подтвержденные_даты.ics';prior=calendar(before(file));now=calendar((ROOT/file).read_bytes())
assert len(prior)==1956 and len(now)==2066 and len(set(now)-set(prior))==110
for uid,oldcal in prior.items():
    assert now[uid].get('DTSTART;VALUE=DATE')==oldcal.get('DTSTART;VALUE=DATE')
    assert now[uid].get('DTEND;VALUE=DATE')==oldcal.get('DTEND;VALUE=DATE')
assert set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in new}
file='dist/downloads/STEM_крупные_выставки.ics';expo=calendar((ROOT/file).read_bytes());oldexpo=calendar(before(file))
assert len(expo)==104 and set(expo)==set(oldexpo)
for uid,val in oldexpo.items():assert {k:v for k,v in expo[uid].items() if k!='DTSTAMP'}=={k:v for k,v in val.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text())
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==80
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version79' in plan['previous_goal_turn_classification']['evidence']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert plan['camp_catalog_integration']['dossiers']==402 and d['coverage_summary']['fully_audited_countries']==0
for stem in ['americas-camp-audit-v80','americas-camp-source-receipts-v80']:
    val=json.loads((ROOT/'data'/f'{stem}.json').read_text())
    assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==val
    assert not any(val['external_actions'].values())
assert len(val['verified_new_dossier_urls'])==30 and len(val['sources'])==36 and sum(v.get('status')==200 for v in val['sources'])==30
assert 'data-ui-version="80"' in (ROOT/'dist/index.html').read_text()
assert 'STEM_americas_camp_audit_v80.json' in (ROOT/'dist/assets/camp-programmes.js').read_text()
print(json.dumps(dict(passed=True,preserved_events=2621,preserved_dossier_ids=389,new_dossiers=13,new_calendar_rows=110,
    events=2731,dossiers=402,family_ics=2066,exhibition_ics=104,worldwide_complete=False)))
