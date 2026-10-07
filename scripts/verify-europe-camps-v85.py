"""Independently parse retained primary prices/dates; preserve the published v84 catalogue."""
import hashlib,json,re,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v85'
BASE='220b513e9720864862294c47f9d633897c8a995a'
def before(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def raw(key):return (PRIMARY/(key+'.txt')).read_text()
def compact(t):return re.sub(r'\s+','',t)
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};events={e['id']:e for e in d['events']}
assert len(old)==2823 and len(events)==len(d['events'])==2959
assert all(events.get(k)==v for k,v in old.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==b[key],key
c=d['camp_programmes'];p={q['slug']:q for q in c['profiles']};op={q['slug']:q for q in b['camp_programmes']['profiles']}
assert len(op)==464 and len(p)==487 and all(p[k]==v for k,v in op.items() if k!='enforex-barcelona')
assert [q['id'] for q in c['profiles'][:464]]==[q['id'] for q in b['camp_programmes']['profiles']]
beach=p['enforex-barcelona'];assert beach['id']=='CP018'
historical=beach['previous_seasons'][0]['record']
assert all(historical[k]==op['enforex-barcelona'][k] for k in historical if k!='timing')
assert historical['timing']=={k:v for k,v in op['enforex-barcelona']['timing'].items() if k!='precision'}
assert c['counts']['countries']==34 and c['counts']['source_urls']==749 and c['counts']['swiss']==78
for iso,n in [('CHE',78),('FRA',41),('ESP',43),('TWN',25),('SGP',56),('JPN',23),('KOR',10),('USA',44),('CAN',57),('CRI',10),('MEX',25)]:
    assert sum(q['iso']==iso for q in p.values())==n
assert sum(e['block']=='Лагеря' for e in events.values())==1628
assert len(c['generated_event_ids'])==1165 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==35
assert len(c['shortlist'])==106 and c['shortlist'][:102]==b['camp_programmes']['shortlist']
assert c['gaps'][:-4]==b['camp_programmes']['gaps']
assert all(len(s['slugs'])==len(set(s['slugs'])) and all(k in p for k in s['slugs']) for s in c['shortlist'][-4:])
new=[e for k,e in events.items() if k not in old]
assert len(new)==136 and all(e['block']=='Лагеря' and e['checked']=='2026-10-05' for e in new)
def rows(slug):return [e for e in new if e['camp_dossier_slug']==slug]
def pairs(slug):return {(e['start'],e['end']) for e in rows(slug)}

# Independently read PDF page33 column positions and dot matrix, not the authoring module's constants.
pdf=raw('enforex-brochure-pdf');pages=pdf.split('\f');table=pages[32]
assert 'PRICES AND DATES 2027' in table and 'Enforex Camps 2027' in table and len(pages)>=36
lines=[s for s in table.splitlines() if '•' in s]
columns=sorted({m.start() for line in lines for m in re.finditer('•',line)})
assert columns==[63,78,95,111,126,141,156,171,187] and len(lines)==13
campuses=['alicante','barcelona','barcelona-centro','madrid','malaga','marbella-centro','marbella-elviria','salamanca','valencia']
months={'JUNE':6,'JULY':7,'AUGUST':8}
dated={s:set() for s in campuses}
for line in lines:
    m=re.search(r'(JUNE|JULY|AUGUST) (\d+)-(?:((?:JUNE|JULY|AUGUST)) )?(\d+)',line)
    assert m,line
    start=f'2027-{months[m[1]]:02d}-{int(m[2]):02d}'
    end=f'2027-{months[m[3] or m[1]]:02d}-{int(m[4]):02d}'
    for campus,col in zip(campuses,columns):
        if len(line)>col and line[col]=='•':dated[campus].add((start,end))
for campus in ['madrid','marbella-elviria','salamanca']:
    for fmt in ['board','day']:assert pairs('enforex-'+campus+'-'+fmt)==dated[campus]
for campus in ['alicante','malaga','barcelona-centro','marbella-centro','valencia']:
    assert pairs('enforex-'+campus+'-teen')==dated[campus]
assert pairs('enforex-barcelona')==dated['barcelona'] and len(rows('enforex-barcelona'))==2*len(dated['barcelona'])==20
assert ('2027-08-15','2027-08-28') not in dated['barcelona'] and ('2027-08-15','2027-08-21') in dated['barcelona']
assert not any(a.startswith('2027-07') and (int(z[-2:])-int(a[-2:])==6) for s in ['barcelona-centro','valencia'] for a,z in dated[s])
assert '€ 35 one-time' in table and 'lasts 45 min.' in table and '€ 600' in table and '€ 300' in table
assert re.search(r'€ 1\.195\s+€ 2\.095\s+€ 3\.295\s+€ 3\.995',table)
assert re.search(r'€ 1\.395\s+€ 2\.495\s+€ 3\.895\s+€ 4\.895',table)
assert '€ 95' in table and '€ 850' in pages[34] and 'No refunds will be granted two weeks before' in pages[34]
assert '6-12' in pages[27] and 'Ages: 5 to 18' in pages[27] and 'Ages: 5 to 16' in pages[21]
assert 'Ages: 5 to 21' in pages[24] and 'Ages: 12 to 21' in pages[25]
for e in new:
    if e['camp_dossier_slug'].startswith('enforex-') and e['camp_dossier_slug']!='enforex-madrid-leadership':
        slug=e['camp_dossier_slug'];campus='barcelona' if slug=='enforex-barcelona' else slug.removeprefix('enforex-').rsplit('-',1)[0]
        fmt=e['participation'];one=(__import__('datetime').date.fromisoformat(e['end'])-__import__('datetime').date.fromisoformat(e['start'])).days==6
        cost=(600 if one else 1200) if fmt=='day_camp' else ((1195 if one else 2095) if campus in ['marbella-elviria','salamanca','valencia'] else (1395 if one else 2495))
        assert f'EUR{cost}' in compact(e['cost']) and f'EUR{cost+35}' in compact(e['cost'])
        assert e['languages']==['EN','ES'] and e['language_mode']=='language_lessons'
        if fmt=='day_camp':
            assert e['attendance_weekdays']==['MO','TU','WE','TH','FR'] and e['date_scope']=='day_camp_window'
        else:assert fmt=='residential' and 'attendance_weekdays' not in e
assert 'EUR4260' in compact(p['enforex-marbella-elviria-board']['price']['extras'])
assert 'EUR5060' in compact(p['enforex-madrid-board']['price']['extras'])
assert all(q['timing']['status']=='published_2027' for q in p.values() if q['slug'].startswith('enforex-'))
assert pairs('enforex-madrid-leadership')=={('2027-07-04','2027-07-17')}
assert '€ 3.950' in pages[31] and 'All in English' in pages[33]
assert all(e['priority'].startswith('P4') for e in rows('enforex-madrid-leadership'))
for key in ['madrid','elviria','salamanca','barcelona','alicante','malaga','barcelona-centro','marbella-centro','valencia']:
    assert '2026' in raw('enforex-'+key)

# Real course windows never expand into assumed weekly admissions/ICS.
expected={
    'alpadia-leysin': [('2027-03-29','2027-04-16'),('2027-06-21','2027-08-06')],
    'alpadia-engelberg':[('2027-06-28','2027-07-30')],
    'alpadia-paris-passy':[('2027-06-28','2027-08-06')],
    'chantemerle-junior-board':[('2027-06-27','2027-08-01')],
    'chantemerle-junior-day':[('2027-06-27','2027-08-01')],
    'chantemerle-junior-halfday':[('2027-06-27','2027-08-01')],
    'chantemerle-maths-physics':[('2027-06-27','2027-07-18')]}
for slug,wanted in expected.items():
    assert [tuple(x) for x in p[slug]['timing']['sessions']]==wanted and p[slug]['timing']['precision']=='season_window' and not rows(slug)
for key,age,dates in [('alpadia-leysin-en','8–17',['29 March – 16 April 2027','21 June – 06 August 2027']),
                     ('alpadia-engelberg-en','10–17',['28 June – 30 July 2027']),
                     ('alpadia-passy-en','13–17',['28 June – 06 August 2027'])]:
    t=raw(key);assert age in t and all(v in t for v in dates) and 'English' in t and '18.45' in t
assert '2026' in raw('alpadia-leysin-fr') and '2026' in raw('alpadia-brochure') and '2026' in raw('alpadia-terms')
assert 'English or French' in raw('alpadia-igny-en') and '28 June – 08 August 2026' in raw('alpadia-igny-en')
assert p['alpadia-paris-igny']['timing']['status']=='published_2026' and not p['alpadia-paris-igny']['timing']['sessions']
assert p['alpadia-engelberg']['family_fit']['matvey']['status']=='conditional'
assert all(p[s]['family_fit']['oscar']['status']=='later' for s in ['alpadia-leysin','alpadia-engelberg'])
for slug in ['alpadia-leysin','alpadia-engelberg','alpadia-paris-passy','alpadia-paris-igny']:
    assert p[slug]['confirmed_instruction_languages']==['EN'] and p[slug]['language_evidence_role']=='language_lessons'
assert not any('alpadia-nice' in s or 'alpadia-biarritz' in s for s in p)

ch=compact(raw('chantemerle-2027-pdf'));fee=compact(raw('chantemerle-fees'));learning=raw('chantemerle-learning')
assert 'Ages6to11(juniors)and12to16(teens)' in ch
assert all(x in ch for x in ['June27thandAugust1st2027','4’950','6’250','7’500','8’900'])
assert '1week=CHF2’800' in fee and 'CHF1’100' in fee and 'CHF1’600' in fee
assert 'CHF8.00/day' in fee and 'CHF800' in fee and '30daysbefore' in fee
assert '2-week programme in English available from July 18th to August 1st, 2027' in learning
assert '2-week programme in English or French available from June 27th to July 18th, 2027' in learning and 'ages 14-17' in learning
assert pairs('chantemerle-leadership')=={('2027-07-18','2027-08-01')}
assert all(p[s]['family_fit']['oscar']['status']=='candidate' for s in ['chantemerle-junior-board','chantemerle-junior-day','chantemerle-junior-halfday'])
assert all(e['priority'].startswith('P4') for e in rows('chantemerle-leadership'))
assert '3D' in raw('chantemerle-activities') and all('robotics' not in p[s]['themes'] for s in ['chantemerle-junior-board','chantemerle-junior-day','chantemerle-junior-halfday'])

ec=raw('englishcamp-ch-dates');prices=raw('englishcamp-ch-prices')
assert '18.04. - 24.04.2027' in ec and '25.04. - 01.05.2027' in ec and '11.- 17. Juli 2027' in ec and '18.- 24. Juli 2027' in ec
assert '9 - 15 Jahren' in ec and 'Frühling / Sommer 2026 & 2027' in prices and '50 CHF pro Rechnung' in prices
assert pairs('englishcamp-switzerland-spring')=={('2027-04-18','2027-04-24'),('2027-04-25','2027-05-01')}
assert pairs('englishcamp-switzerland-summer')=={('2027-07-11','2027-07-17'),('2027-07-18','2027-07-24')}
for s in ['englishcamp-switzerland-spring','englishcamp-switzerland-summer']:
    assert p[s]['family_fit']['matvey']['status']=='candidate' and p[s]['family_fit']['oscar']['status']=='later'
    assert '1430' in p[s]['price']['label'] and all('1430' in e['cost'] for e in rows(s))
assert '2022/23' in prices and 'Zwischen 30 und 10 Tage' in prices

# Data integrity, idempotence and calendar truth for current family vs future tracks.
report=json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text())
again=json.loads(json.dumps(d));integrate(again,report);assert again==d
for file,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:
    assert json.loads((ROOT/'dist/downloads'/file).read_text())==wanted
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2959 and con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==487
con.close()
def calendar(v):
    out={};t=v.decode().replace('\r\n ','').replace('\r\n\t','')
    for ch in t.split('BEGIN:VEVENT')[1:]:
        f={line.split(':',1)[0]:line.split(':',1)[1] for line in ch.split('END:VEVENT')[0].splitlines() if ':' in line}
        assert f['UID'] not in out;out[f['UID']]=f
    return out
file='dist/downloads/STEM_подтвержденные_даты.ics';prior=calendar(before(file));now=calendar((ROOT/file).read_bytes())
assert len(prior)==2149 and len(now)==2233 and set(prior)<=set(now)
for uid,v in prior.items():assert all(now[uid].get(k)==v.get(k) for k in ['DTSTART;VALUE=DATE','DTEND;VALUE=DATE'])
eligible=[e for e in new if not e['priority'].startswith('P4')]
assert len(eligible)==84 and set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in eligible}
assert sum(e['priority'].startswith('P4') for e in new)==52
for e in new:
    if e.get('date_scope')=='day_camp_window':assert '[Окно дневного лагеря' in now['stem-'+e['id']+'@family-stem.local']['SUMMARY']
file='dist/downloads/STEM_крупные_выставки.ics';expo=calendar((ROOT/file).read_bytes());oe=calendar(before(file))
assert len(expo)==104 and set(expo)==set(oe)
for uid,v in oe.items():assert {k:x for k,x in expo[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==85
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version84' in plan['previous_goal_turn_classification']['evidence']
assert {q['id'] for q in bp['requirements']}<={q['id'] for q in plan['requirements']}
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert plan['camp_catalog_integration']['dossiers']==487 and d['coverage_summary']['fully_audited_countries']==0
for stem in ['europe-camp-audit-v85','europe-camp-source-receipts-v85']:
    val=json.loads((ROOT/'data'/f'{stem}.json').read_text())
    assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==val
    assert not any(val['external_actions'].values())
assert len(val['sources'])==32 and sum(v.get('status')==200 for v in val['sources'])==31
assert len(val['dossier_source_urls_added'])==22 and len(val['visual_primary_reads'])==3
for v in val['sources']:
    if v.get('status')==200:assert v['body_snapshot_retained'] and hashlib.sha256((PRIMARY/v['raw_filename']).read_bytes()).hexdigest()==v['sha256']
shell=raw('stgeorge-summer');assert shell=='Inspired Summer Camps' or shell.strip()=='Inspired Summer Camps'
assert '2027' not in (PRIMARY/'stgeorge-summer-app.js').read_text()
assert not any(q['id']>='CP465' and q['slug'].startswith('stgeorge') for q in p.values())
assert 'data-ui-version="85"' in (ROOT/'dist/index.html').read_text()
assert 'STEM_europe_camp_audit_v85.json' in (ROOT/'dist/assets/camp-programmes.js').read_text()
print(json.dumps(dict(passed=True,preserved_events=2823,preserved_dossier_ids=464,unchanged_dossiers=463,new_dossiers=23,updated_dossiers=1,new_calendar_rows=136,new_family_ics=84,
    events=2959,dossiers=487,family_ics=2233,exhibition_ics=104,worldwide_complete=False)))
