"""Independent source-date/cohort checks and complete v81 preservation."""
import hashlib,json,re,sqlite3,subprocess
from datetime import date,timedelta
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v82'
BASE='8bac850381d6661e830b6f030e23f7490d970ac2'
def before(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def raw(key):return (PRIMARY/(key+'.txt')).read_text()
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};events={e['id']:e for e in d['events']}
assert len(old)==2741 and len(events)==len(d['events'])==2780
assert all(events.get(k)==v for k,v in old.items())
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[k]==b[k],k
c=d['camp_programmes'];p={q['slug']:q for q in c['profiles']};op={q['slug']:q for q in b['camp_programmes']['profiles']}
assert len(op)==415 and len(p)==432 and all(p[k]==v for k,v in op.items())
assert c['profiles'][:415]==b['camp_programmes']['profiles']
assert c['counts']['countries']==33 and c['counts']['source_urls']==681 and c['counts']['swiss']==69
for iso,n in [('CHE',69),('FRA',39),('ESP',31),('DEU',11),('AUT',3),('NLD',5),('TWN',23),('SGP',52),('JPN',17),('KOR',8),('USA',38),('CAN',51),('CRI',7),('MEX',24)]:
    assert sum(q['iso']==iso for q in p.values())==n
assert sum(e['block']=='Лагеря' for e in events.values())==1449
assert len(c['generated_event_ids'])==986 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==27
assert len(c['shortlist'])==94 and c['shortlist'][:90]==b['camp_programmes']['shortlist']
assert c['gaps'][:-4]==b['camp_programmes']['gaps']
assert all(len(s['slugs'])==len(set(s['slugs'])) and all(k in p for k in s['slugs']) for s in c['shortlist'][-4:])
new=[e for k,e in events.items() if k not in old]
assert len(new)==39 and all(e['block']=='Лагеря' and e['checked']=='2026-10-05' for e in new)
def rows(slug):return [e for e in new if e['camp_dossier_slug']==slug]
def pairs(slug):return {(e['start'],e['end']) for e in rows(slug)}
expected={'ensr-junior-languages':3,'ensr-junior-multisport':3,'cjsa-languages-sports':6,'cjsa-little-fun':6,
          'frilingue-braunwald-language':7,'frilingue-braunwald-family':7,'bell-geneva-explorer':3,'british-council-paris-primary':4}
assert {s:len(rows(s)) for s in expected}==expected and {e['camp_dossier_slug'] for e in new}==set(expected)
assert len(set(p)-set(op))==17

# Derive dates from independent primary snapshots, rather than the authored sessions.
def dotted(v):return date.fromisoformat('-'.join(reversed(v.split('.')))).isoformat()
t=raw('ensr-registration');assert '2027 Summer Camp Details' in t
source_pairs={(dotted(a),dotted(z)) for a,z in re.findall(r'(\d{2}\.\d{2}\.2027)\s*-\s*(\d{2}\.\d{2}\.2027)',t)}
assert len(source_pairs)==3
for slug in ['ensr-junior-languages','ensr-junior-multisport']:assert pairs(slug)==source_pairs
assert 'Junior' in raw('ensr') and '8' in raw('ensr') and '11' in raw('ensr')
assert 'Summer Camp 2026' in raw('ensr-pdf') and '28.06 – 04.07.2026' in raw('ensr-pdf')
assert 'EU/EEA/Switzerland' in t and 'CHF 150' in t and 'CHF 345' in t
assert '2026' in p['ensr-junior-languages']['price']['deposit'] and not p['ensr-junior-multisport']['confirmed_instruction_languages']
assert all(p[s]['family_fit']['oscar']['status']=='later' for s in ['ensr-junior-languages','ensr-junior-multisport'])
for slug,key,age in [('cjsa-languages-sports','cjsa','Ages 9 to 17'),('cjsa-little-fun','cjsa-junior','Ages 8 to 10')]:
    t=raw(key);assert 'Dates été 2027' in t and age in t
    pp={(f'2027-{am}-{a}',f'2027-{zm}-{z}') for a,am,z,zm in re.findall(r'(\d{2})\.(\d{2}) au (\d{2})\.(\d{2})',t)}
    assert len(pp)==6 and pairs(slug)==pp and not any(a=='2027-08-01' for a,z in pp)
    assert all('attendance_weekdays' not in e for e in rows(slug))
assert "3 semaines : CHF 1'500.-" in raw('cjsa-junior')
assert '08h30 à 18h00' in raw('cjsa-faq') and '20th to 11th' in raw('cjsa-faq')

for slug,key,age in [('frilingue-braunwald-language','frilingue-braunwald','8-17 Years'),('frilingue-braunwald-family','frilingue-family','6-17 & 18+ Years')]:
    t=raw(key);assert age in t and '27.06 / 04.07 / 11.07 / 18.07 / 25.07 / 01.08 / 08.08.2027' in t
    line=next(x for x in t.splitlines() if x.startswith('27.06 /'))
    starts=[date(2027,int(m),int(a)) for a,m in re.findall(r'(\d{2})\.(\d{2})(?:\.2027)?',line)]
    assert pairs(slug)=={(a.isoformat(),(a+timedelta(days=6)).isoformat()) for a in starts}
    assert all(e['date_precision']=='published_rule' and e['date_rule'] for e in rows(slug))
assert p['frilingue-braunwald-family']['family_fit']['oscar']['status']=='conditional'
assert p['frilingue-braunwald-language']['family_fit']['oscar']['status']=='later'
t=raw('frilingue-braunwald');assert 'minimum of 3' in t and 'lessons will be in English' in t and 'bring your own laptop' in t
assert 'Monday, Wednesday, and Friday' in t and '150 CHF per week' in t
q=p['frilingue-braunwald-coding'];assert q['parent_programme_slug']=='frilingue-braunwald-language'
assert not q['timing']['sessions'] and not q['calendar_links'] and q['language_evidence_role']=='primary'
assert all('coding' not in e['themes'] for e in rows('frilingue-braunwald-language'))
t=raw('frilingue-family');assert '500 CHF' in t and '1400 CHF' in t and '1800 CHF' in t
assert 'activities, excursions and evening programmes are not included' in t
assert '7 to 1 day' in raw('frilingue-terms') and '13 to 7 days' in raw('frilingue-terms')

for slug,key in [('altitude-day-junior','altitude-day'),('altitude-residential-junior','altitude-residential')]:
    assert '2027' not in raw(key) and not p[slug]['timing']['sessions'] and p[slug]['price']['year'] is None
assert '7 – 14 years old' in raw('altitude-residential') and 'September 2012 to June 2020' in raw('altitude-booking')
assert '2025' in raw('altitude-booking') and 'do not provide any form of insurance' in raw('altitude-terms')
bell=set();months={'October':'10','February':'02','April':'04'}
for key in ['bell-autumn','bell-winter','bell-spring']:
    t=raw(key);assert '4 - 10 years old' in t and '415 CHF' in t and '725 CHF' in t
    a,z,m,y=re.search(r'(\d+) - (\d+) (October|February|April) (2026|2027)',t).groups()
    bell.add((f'{y}-{months[m]}-{int(a):02}',f'{y}-{months[m]}-{int(z):02}'))
assert pairs('bell-geneva-explorer')==bell
assert all(e['attendance_weekdays']==['MO','TU','WE','TH','FR'] for e in rows('bell-geneva-explorer'))
t=raw('bc-primary-web');assert 'CE1 au CM2' in t and '799' in t and '11 rue Cler' in t
months={'octobre':'10','février':'02','avril':'04','juillet':'07'}
bc={(f'{y}-{months[m]}-{int(a):02}',f'{y}-{months[m]}-{int(z):02}') for a,z,m,y in re.findall(r'(\d+)[–-](\d+) (octobre|février|avril|juillet) (2026|2027)',t)}
assert len(bc)==4 and pairs('british-council-paris-primary')==bc
assert p['british-council-paris-primary']['family_fit']['oscar']['status']=='unknown'
assert 'Brochure coming soon' in raw('kidooland-prices') and 'Stages Vacances 2027' in raw('kidooland-prices')
assert '100% English immersion' in raw('kidooland-holidays') and 'Holidaymakers' in raw('kidooland-holidays')
for slug in ['kidooland-activate','kidooland-advance','kidooland-elevate']:
    assert not p[slug]['timing']['sessions'] and p[slug]['price']['year'] is None
t=raw('englishsummer-tech');assert '905 euros' in t and '8 días' in t and 'Mínimo 10 alumnos' in t
assert '15h por semana' in t and 'LEGO WeDo' in t and 'LEGO Mindstorms' in t
for slug in ['englishsummer-tech','englishsummer-multiactivity','englishsummer-alive']:
    assert not p[slug]['timing']['sessions'] and p[slug]['price']['year'] is None
assert 'febrero de 2025' in raw('englishsummer-payment')
assert p['englishsummer-tech']['related_event_ids']==['L006'] and p['englishsummer-tech']['language_evidence_role']=='language_lessons'

report=json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text())
again=json.loads(json.dumps(d));integrate(again,report);assert again==d
for file,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:
    assert json.loads((ROOT/'dist/downloads'/file).read_text())==wanted
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2780
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==432
con.close()
def calendar(v):
    out={};t=v.decode().replace('\r\n ','').replace('\r\n\t','')
    for ch in t.split('BEGIN:VEVENT')[1:]:
        f={line.split(':',1)[0]:line.split(':',1)[1] for line in ch.split('END:VEVENT')[0].splitlines() if ':' in line}
        assert f['UID'] not in out;out[f['UID']]=f
    return out
file='dist/downloads/STEM_подтвержденные_даты.ics';prior=calendar(before(file));now=calendar((ROOT/file).read_bytes())
assert len(prior)==2073 and len(now)==2112 and set(prior)<=set(now)
for uid,v in prior.items():assert all(now[uid].get(k)==v.get(k) for k in ['DTSTART;VALUE=DATE','DTEND;VALUE=DATE'])
assert set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in new}
file='dist/downloads/STEM_крупные_выставки.ics';expo=calendar((ROOT/file).read_bytes());oe=calendar(before(file))
assert len(expo)==104 and set(expo)==set(oe)
for uid,v in oe.items():assert {k:x for k,x in expo[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==82
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version81' in plan['previous_goal_turn_classification']['evidence']
assert {q['id'] for q in bp['requirements']}<={q['id'] for q in plan['requirements']}
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert plan['camp_catalog_integration']['dossiers']==432 and d['coverage_summary']['fully_audited_countries']==0
for stem in ['europe-camp-audit-v82','europe-camp-source-receipts-v82']:
    val=json.loads((ROOT/'data'/f'{stem}.json').read_text())
    assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==val
    assert not any(val['external_actions'].values())
assert len(val['sources'])==36 and sum(v.get('status')==200 for v in val['sources'])==33
assert len(val['dossier_source_urls_added'])==28 and len(val['visual_primary_reads'])==1
for v in val['sources']:
    if v.get('status')==200:
        file=next((PRIMARY/(v['key']+ext) for ext in ['.html','.pdf'] if (PRIMARY/(v['key']+ext)).exists()))
        if v['body_snapshot_retained']:
            assert file.name==v['raw_filename'] and hashlib.sha256(file.read_bytes()).hexdigest()==v['sha256']
        else:
            assert v['key']=='kidooland-holidays' and v['raw_filename'] is None and v['snapshot_note']
            assert hashlib.sha256(file.read_bytes()).hexdigest()!=v['sha256']
assert sum(v.get('body_snapshot_retained') is True for v in val['sources'])==32
assert sum(v.get('body_snapshot_retained') is False for v in val['sources'])==1
assert 'data-ui-version="82"' in (ROOT/'dist/index.html').read_text()
assert 'STEM_europe_camp_audit_v82.json' in (ROOT/'dist/assets/camp-programmes.js').read_text()
print(json.dumps(dict(passed=True,preserved_events=2741,preserved_dossier_ids=415,new_dossiers=17,new_calendar_rows=39,new_family_ics=39,
    events=2780,dossiers=432,family_ics=2112,exhibition_ics=104,worldwide_complete=False)))
