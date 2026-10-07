"""Independent retained-source parsing, calendar eligibility and published-v83 preservation."""
import hashlib,json,re,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v84'
BASE='3587a9bd56dbfbe98d584fb1bd2d8bf2c32eb4d8'
def before(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def raw(key):return (PRIMARY/(key+'.txt')).read_text()
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};events={e['id']:e for e in d['events']}
assert len(old)==2797 and len(events)==len(d['events'])==2823
assert all(events.get(k)==v for k,v in old.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==b[key],key
c=d['camp_programmes'];p={q['slug']:q for q in c['profiles']};op={q['slug']:q for q in b['camp_programmes']['profiles']}
assert len(op)==448 and len(p)==464 and all(p[k]==v for k,v in op.items())
assert c['profiles'][:448]==b['camp_programmes']['profiles']
assert c['counts']['countries']==34 and c['counts']['source_urls']==727 and c['counts']['swiss']==69
for iso,n in [('CHE',69),('FRA',39),('ESP',31),('TWN',25),('SGP',56),('JPN',23),('KOR',10),('PHL',2),('USA',44),('CAN',57),('CRI',10),('MEX',25)]:
    assert sum(q['iso']==iso for q in p.values())==n
assert sum(e['block']=='Лагеря' for e in events.values())==1492
assert len(c['generated_event_ids'])==1029 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==27
assert len(c['shortlist'])==102 and c['shortlist'][:98]==b['camp_programmes']['shortlist']
assert c['gaps'][:-4]==b['camp_programmes']['gaps']
assert all(len(s['slugs'])==len(set(s['slugs'])) and all(k in p for k in s['slugs']) for s in c['shortlist'][-4:])
new=[e for k,e in events.items() if k not in old]
assert len(new)==26 and all(e['block']=='Лагеря' and e['checked']=='2026-10-05' for e in new)
def rows(slug):return [e for e in new if e['camp_dossier_slug']==slug]
def pairs(slug):return {(e['start'],e['end']) for e in rows(slug)}
expected={'walt-whitman-pioneer':1,'walt-whitman-regular':3,'walt-whitman-family':1,
          'champions-one-week':5,'champions-regular':11,'walden-regular':3,'walden-explorer':1,'walden-long-weekend':1}
assert {s:len(rows(s)) for s in expected}==expected and {e['camp_dossier_slug'] for e in new}==set(expected)
months={'May':5,'June':6,'July':7,'Jul':7,'August':8,'Aug':8}
def date(month,day):return f'2027-{months[month]:02d}-{int(day):02d}'

# Parse every dated Camp Champions term and its fee from the independently retained HTML text.
t=re.sub(r'\s+',' ',raw('champions-rates'))
assert 'Dates & Rates Summer 2027' in t
terms=re.findall(r'Sunday, (May|June|July|August) (\d{1,2})\s*[—–]\s*Saturday, (May|June|July|Aug|August) (\d{1,2}) \$(\d+) \$(\d+)',t)
assert len(terms)==16
source_terms={(date(m,a),date(n,z)):(int(cost),int(dep)) for m,a,n,z,cost,dep in terms}
catalog_terms={(e['start'],e['end']):e for s in ['champions-one-week','champions-regular'] for e in rows(s)}
assert set(catalog_terms)==set(source_terms)
for pair,(cost,dep) in source_terms.items():
    e=catalog_terms[pair];amount_text=re.sub(r'[,\s]','',e['cost'])
    assert str(cost) in amount_text and str(dep) in amount_text
assert 'finishing Kindergarten-11th grade' in t and 'finishing 3rd grade or younger' in t and 'finishing 8th grade or younger' in t
assert 'finishing 2nd through 11th grade' in t and 'Combine any three 2-week sessions' in t
assert not p['champions-regular']['confirmed_instruction_languages'] and not p['champions-one-week']['confirmed_instruction_languages']
assert not any('six-week' in e['title'].lower() for e in rows('champions-regular'))
early=[e for e in rows('champions-one-week') if e['start']<'2027-06-27']
assert len(early)==2 and all('Grade 3' in e['age'] for e in early)
assert all('Grade 8' in e['age'] for e in rows('champions-one-week') if e not in early)
assert all('Grade 2' in e['age'] for e in rows('champions-regular') if 'Triple' in e['title'] or 'Combo 5' in e['title'])
assert 'deposit is non-refundable after February 1' in t and 'Less than 30 days' in t and '91 or more' in t
cf=raw('champions-current-families');assert 'Summer 2027' in cf and 'preparing for camp in 2026' in cf and 'automatic fee' in cf.lower()
assert 'optional additions' in t and 'Campanion' in p['champions-regular']['price']['extras']
assert '2026 family camp' in raw('champions-family') and 'September 25th - September 27th' in raw('champions-family')
assert '6 or more' in raw('champions-family') and '$499.50' in raw('champions-family') and not p['champions-family']['timing']['sessions']

# Three regular Whitman dates are read from the source table, not a four-week rule.
t=re.sub(r'\s+',' ',raw('walt-preparing'))
assert 'Important Dates & Rates for 2027' in t
w=re.findall(r'(?:Full Session|1st Session|2nd Session|Pioneer 1) (June|July) (\d+) - (July|August) (\d+) \$([\d,]+)',t)
assert len(w)==4
assert {(date(m,a),date(n,z)) for m,a,n,z,_ in w}==pairs('walt-whitman-regular')|pairs('walt-whitman-pioneer')
assert {int(v.replace(',','')) for *_,v in w}=={17600,12150,9400,2000}
wp=raw('walt-pioneer');assert 'finishing first and second grade' in wp.lower()
assert 'currently in 2nd and 3rd grades' in raw('walt-faq') and 'finishing 4th through 7th grades' in raw('walt-faq')
wf=raw('walt-family');assert '2027' in wf and 'August 16' in wf and '20' in wf and '$1000' in wf and '$500' in wf
assert pairs('walt-whitman-family')=={('2027-08-16','2027-08-20')}
assert all(not p[s]['confirmed_instruction_languages'] for s in ['walt-whitman-pioneer','walt-whitman-regular','walt-whitman-family'])

# Own-reader Walden proof retains the direct403, closed availability, currency and contract conflicts.
t=raw('walden-rates-web');assert 'for Summer 2027' in t and 'Registration is Closed' in t
wa=re.findall(r'Jul (\d+) (?:\d+ weeks|3 days)—(Jul|Aug) (\d+)',t)
assert len(wa)==5 and {(date('Jul',a),date(m,z)) for a,m,z in wa}==pairs('walden-regular')|pairs('walden-explorer')|pairs('walden-long-weekend')
assert 'For kids completing Grade 2 (Colours)' in t and 'For kids completing Grade 1 (Colours)' in t and 'Senior Kindergarten' in t
assert 'full payment in the case of the Walden Long Weekend' in t and '13% HST' in t and '3% processing' in t
assert 'Canadian or U.S. Dollars' in t and 'outside of Canada and the U.S. may vary' in t and 'non-refundable for any reason whatsoever' in t
for s in ['walden-regular','walden-explorer','walden-long-weekend']:
    assert all(e['availability']['status']=='closed' and e['participation']=='residential' for e in rows(s))
    assert all('waitlist' in e['entry'] for e in rows(s))
    assert not p[s]['confirmed_instruction_languages']

# 2026 and year-unlabelled programmes stay out of2027 dates; language is scoped to the actual programme.
assert 'Summer Calendar 2026' in raw('nominingue-calendar') and 'Camp Nominingue operates in English' in raw('nominingue-faq')
assert '7 -10 years' in raw('nominingue-rates') and 'Up to Grade 4' in raw('nominingue-rates') and '$1,875' in raw('nominingue-rates')
assert '7 to 9 year olds' in raw('nominingue-faq') and 'In 2018' in raw('nominingue-faq')
for s in ['nominingue-junior','nominingue-regular']:
    assert p[s]['confirmed_instruction_languages']==['EN'] and p[s]['language_evidence_role']=='camp_life' and not p[s]['timing']['sessions']
    assert p[s]['price']['year'] is None
assert '2026' in raw('nominingue-family') and '$520' in raw('nominingue-family') and '$350' in raw('nominingue-family')
assert not p['nominingue-family']['confirmed_instruction_languages'] and not p['nominingue-family']['timing']['sessions']
t=raw('ico-kids');assert 'June 1 to August 21, 2026' in t and '100% in Spanish' in t and 'six students' in t and 'after the 5th week' in t
assert all('USD '+str(v) in t for v in [300,560,780,960]) and 'fully refundable until 14 days' in raw('ico-faq')
assert p['ico-oaxaca-kids']['confirmed_instruction_languages']==['ES'] and not p['ico-oaxaca-kids']['timing']['sessions']
t=raw('intercultura-2027-pdf');assert '2027 PRICE LIST' in t and '$365/wk' in t and '$380/wk' in t and '$3,650' in t
it=raw('intercultura-terms');assert 'USD $150' in it and 'USD $250' in it and '20% non-refundable deposit' in it
assert '8 -12 OR 13-17' in raw('intercultura-family') and 'children under 8 years old' in raw('intercultura-apartments')
for s in ['intercultura-heredia-kids','intercultura-samara-kids']:
    assert p[s]['family_fit']['oscar']['status']=='not_eligible' and p[s]['confirmed_instruction_languages']==['ES']
    assert p[s]['timing']['status']=='partial_2027' and not p[s]['timing']['sessions']
assert '13' in p['intercultura-teen-adventure']['age'] and not p['intercultura-teen-adventure']['timing']['sessions']
assert 'janeiro de 2027' in raw('acampark-holidays') and '05 a 16 anos' in raw('acampark-holidays')
assert not any('timbalaia' in s or 'acampark' in s for s in set(p)-set(op))

report=json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text())
again=json.loads(json.dumps(d));integrate(again,report);assert again==d
for file,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:
    assert json.loads((ROOT/'dist/downloads'/file).read_text())==wanted
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2823 and con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==464
con.close()
def calendar(v):
    out={};t=v.decode().replace('\r\n ','').replace('\r\n\t','')
    for ch in t.split('BEGIN:VEVENT')[1:]:
        f={line.split(':',1)[0]:line.split(':',1)[1] for line in ch.split('END:VEVENT')[0].splitlines() if ':' in line}
        assert f['UID'] not in out;out[f['UID']]=f
    return out
file='dist/downloads/STEM_подтвержденные_даты.ics';prior=calendar(before(file));now=calendar((ROOT/file).read_bytes())
assert len(prior)==2128 and len(now)==2149 and set(prior)<=set(now)
for uid,v in prior.items():assert all(now[uid].get(k)==v.get(k) for k in ['DTSTART;VALUE=DATE','DTEND;VALUE=DATE'])
eligible=[e for e in new if e.get('availability',{}).get('status')!='closed']
assert len(eligible)==21 and set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in eligible}
file='dist/downloads/STEM_крупные_выставки.ics';expo=calendar((ROOT/file).read_bytes());oe=calendar(before(file))
assert len(expo)==104 and set(expo)==set(oe)
for uid,v in oe.items():assert {k:x for k,x in expo[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==84
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version83' in plan['previous_goal_turn_classification']['evidence']
assert {q['id'] for q in bp['requirements']}<={q['id'] for q in plan['requirements']}
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert plan['camp_catalog_integration']['dossiers']==464 and d['coverage_summary']['fully_audited_countries']==0
for stem in ['americas-camp-audit-v84','americas-camp-source-receipts-v84']:
    val=json.loads((ROOT/'data'/f'{stem}.json').read_text())
    assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==val
    assert not any(val['external_actions'].values())
assert len(val['sources'])==31 and sum(v.get('status')==200 for v in val['sources'])==29
assert len(val['dossier_source_urls_added'])==24 and len(val['visual_primary_reads'])==1
for v in val['sources']:
    if v.get('status')==200:assert v['body_snapshot_retained'] and hashlib.sha256((PRIMARY/v['raw_filename']).read_bytes()).hexdigest()==v['sha256']
assert 'data-ui-version="84"' in (ROOT/'dist/index.html').read_text()
assert 'STEM_americas_camp_audit_v84.json' in (ROOT/'dist/assets/camp-programmes.js').read_text()
print(json.dumps(dict(passed=True,preserved_events=2797,preserved_dossier_ids=448,new_dossiers=16,new_calendar_rows=26,new_family_ics=21,
    events=2823,dossiers=464,family_ics=2149,exhibition_ics=104,worldwide_complete=False)))
