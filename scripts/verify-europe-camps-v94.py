"""Check primary age/date/fee evidence, seasonal isolation and catalogue preservation."""
import collections, hashlib, json, re, sqlite3, subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
from camp_europe_v94 import UPDATED

ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v94'
BASE='186b283a2b4ca00f6161bf1457b9fc0bc8fb624b'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def before(file):return subprocess.check_output(['git','show',BASE+':'+file],cwd=ROOT)
def raw(key):return (PRIMARY/(key+'.txt')).read_text()
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
op={p['slug']:p for p in b['camp_programmes']['profiles']};p={q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3123 and len(old)==3121 and set(old)<=set(ev)
changed={k for k in old if ev[k]!=old[k]};new=[e for k,e in ev.items() if k not in old]
assert len(changed)==40 and len(new)==2
assert collections.Counter(ev[k]['camp_dossier_slug'] for k in changed)=={'les-elfes':26,'la-garenne':10,'village-leysin':4}
for k,e in old.items():
 if k not in changed:assert ev[k]==e
 else:
  for field in ['id','start','end','deadline','date_scope','date_precision','iso']:assert ev[k].get(field)==e.get(field),(k,field)
  if e.get('camp_dossier_slug')=='les-elfes' and 'Летний' not in e['title']:
   assert {k:v for k,v in ev[k].items() if k!='references'}=={k:v for k,v in e.items() if k!='references'},'Winter/Spring Summer terms leaked'
assert len(p)==len(c['profiles'])==622 and len(op)==621 and p['village-leysin-stem']['id']=='CP622'
assert [q['id'] for q in c['profiles'][:621]]==[q['id'] for q in b['camp_programmes']['profiles']]
for slug,q in op.items():
 if slug not in UPDATED:assert p[slug]==q,slug
 else:
  for k in ['id','slug','iso','country','related_event_ids','calendar_links','confirmed_instruction_languages']:assert p[slug].get(k)==q.get(k),(slug,k)
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[k]==b[k],k
assert c['counts']['countries']==37 and c['counts']['swiss']==86 and c['counts']['source_urls']==975
assert len(c['shortlist'])==142 and c['gaps'][:-3]==b['camp_programmes']['gaps']
for i,q in enumerate(b['camp_programmes']['shortlist']):
 if q['label'] not in ['Швейцария · разные возрастные треки','Швейцария · школа, ski и инженерная опция']:assert c['shortlist'][i]==q,q['label']
for q in c['shortlist']:assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
assert sum(e['block']=='Лагеря' for e in ev.values())==1792
assert len(c['generated_event_ids'])==1329 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==39

# Independently read exact2027 dates/ages/prices from actual operator bodies.
stem=raw('village-stem');junior=raw('village-junior')
assert 'ages 10-17' in stem and 'ages 7-9' in junior
dates=re.findall(r'(June|July|August) (\d+)(?:st|nd|rd|th) to (June|July|August) (\d+)(?:st|nd|rd|th) (2027)\s+-\s+Price\s+CHF (\d+)',stem)
assert len(dates)==2 and all(x[-1]=='5500' for x in dates)
assert {e['start'] for e in new}=={'2027-07-04','2027-07-18'} and {e['end'] for e in new}=={'2027-07-17','2027-07-31'}
assert all(e['camp_dossier_slug']=='village-leysin-stem' and not e['deadline'] and e['languages']==[] and e['language_mode']=='unconfirmed' and e['osc']=='Нет сейчас; будущая возрастная ступень' for e in new)
assert all(set(e['themes'])=={'robotics','coding','engineering'} for e in new)
assert 'Salzburg' in stem and 'Austria Overview Page' in stem and 'Swiss Alpine Centre' in stem
assert 'will remain at camp' in stem and 'sensors' in stem
assert 'ratio of 1:4' in junior and len(re.findall(r'Price\s+CHF \d+',junior))==4
rows=[e for e in ev.values() if e.get('camp_dossier_slug')=='village-leysin']
assert len(rows)==4 and all(e['age']==p['village-leysin']['age'] and 'robotics' not in e['themes'] and 'coding' not in e['themes'] and 'Junior Adventure' in e['title'] for e in rows)
assert all(p[s]['confirmed_instruction_languages']==[] for s in ['village-leysin','village-leysin-stem','garenne-robotics-workshop'])
elf=raw('elfes-summer-pdf')
for t in ['SUMMER CAMP 2027','Registration fees *','150.-','120.-','Shelter Building','6+ incl.','CHF 1,000 deposit','CHF 1,000 applies per claim']:assert t in elf,t
assert '5140' in re.sub(r'\s','',p['les-elfes']['price']['label']) and '10280' in re.sub(r'\s','',p['les-elfes']['price']['label'])
assert 4750+150+2*120==5140 and 2*(4750+150+2*120)==10280
summer=[e for e in ev.values() if e.get('camp_dossier_slug')=='les-elfes' and 'Летний' in e['title']]
assert len(summer)==6 and all('Shelter Building' in e['note'] and 'ТОЛЬКО ЛЕТО 2027' in e['note'] and '150' in e['note'] and '120' in e['note'] for e in summer)
assert p['les-elfes']['confirmed_instruction_languages']==['EN']
g=raw('garenne-summer');section=g.split('Extras 5-9 Years old',1)[1].split('10-12 Years old',1)[0]
assert 'ROBOTICS & 3D DESIGN' in section and '3 sessions' in section
assert 'ROBOTICS (Ages 8-12)' in raw('garenne-form') and 'Robotics & 3D Printing – CHF 500' in raw('garenne-form')
gc=raw('garenne-conditions');gw=raw('garenne-workshop')
assert 'EXTRAS for 8 to 12' in gc and 'Robotics: 3 sessions' in gc and '65 days or more' in gc
assert 'Three Sessions of Innovation' in gw and 'two sessions of learning' in gw and 'Coding in Python' in gw
assert p['garenne-robotics-workshop']['family_fit']['oscar']['status']=='later'
assert 'menu 10' not in p['la-garenne']['questions'][0] and 'прежнее' not in p['garenne-robotics-workshop']['questions'][0]
ilc=raw('ilc-prices')
for t in ['7,990 CHF','8,190 CHF','200 CHF','70 CHF / week','for 2 weeks stay mandatory','1 to 2 people: 350 CHF / transfer']:assert t in ilc,t
assert 2*7990+2*200+2*2*70+2*350==17360
assert 7990+8190+2*200+2*2*70+2*350==17560
assert p['ilc']['price']['year'] is None and p['ilc']['timing']['sessions']==[]
assert '1000 CHF' in raw('ilc-terms') and '5%' in raw('ilc-terms') and '25%' in raw('ilc-terms')
assert '30.04.2026' in raw('tecs-discounts') and 'TECS 2026' in raw('tecs-catalogs')
assert p['tecs-puerto-kids']['price']['year'] is None and p['tecs-puerto-kids']['timing']['sessions']==[]

again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
for file,want in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/file).read_text())==want
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert {json.loads(v)['id']:json.loads(v) for v, in con.execute('SELECT record_json FROM events')}==ev
assert {json.loads(v)['slug']:json.loads(v) for v, in con.execute('SELECT record_json FROM camp_programmes')}==p;con.close()
def calendar(value):
 out={};t=value.decode().replace('\r\n ','').replace('\r\n\t','')
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={line.split(':',1)[0]:line.split(':',1)[1] for line in ch.split('END:VEVENT')[0].splitlines() if ':' in line}
  assert f['UID'] not in out;out[f['UID']]=f
 return out
for file,total in [('STEM_подтвержденные_даты.ics',2384),('STEM_крупные_выставки.ics',104)]:
 prior=calendar(before('dist/downloads/'+file));now=calendar((ROOT/'dist/downloads'/file).read_bytes());assert set(prior)<=set(now) and len(now)==total
 for uid,v in prior.items():
  eid=uid.removeprefix('stem-').removesuffix('@family-stem.local')
  if eid not in changed:assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
  else:
   for key in ['UID','DTSTART;VALUE=DATE','DTEND;VALUE=DATE']:assert now[uid][key]==v[key],uid
 if total==2384:assert set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in new}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==94
assert {q['id'] for q in bp['requirements']}=={q['id'] for q in plan['requirements']}
for key in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[key]==bp[key],key
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['europe-camp-audit-v94','europe-camp-source-receipts-v94']:
 v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
 assert not any(v['external_actions'].values())
 if 'sources' in v:
  assert len(v['sources'])==24 and all(q.get('status')==200 for q in v['sources']) and len(v['dossier_source_urls_added'])==10
  assert sum(q.get('raw_filename','').endswith('.pdf') for q in v['sources'])==6
  for q in v['sources']:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
  meta={q['key']:q.get('pdf_metadata',{}) for q in v['sources']}
  assert '2026' in meta['village-conditions']['Title'] and '2026' in meta['village-leysin-booklet']['Title']
assert len(list(PRIMARY.glob('*page*.png')))==9
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_europe_camp_audit_v94.json' in js and 'data-ui-version="94"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(line for line in js.splitlines() if line.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:'EN'};
FUNCTIONS
let found=new Set(filtered().map(p=>p.slug));
for(const s of ['village-leysin','village-leysin-stem','garenne-robotics-workshop'])if(found.has(s))throw Error('falseEN '+s);
for(const s of ['les-elfes','la-garenne','ilc','tecs-puerto-kids'])if(!found.has(s))throw Error('missingEN '+s);
cs.language='';cs.child='both';found=new Set(filtered().map(p=>p.slug));
for(const s of ['village-leysin-stem','garenne-robotics-workshop'])if(found.has(s))throw Error('falseBoth '+s);
cs.child='';cs.country='CHE';cs.theme='robotics';found=new Set(filtered().map(p=>p.slug));
if(found.has('village-leysin')||!found.has('village-leysin-stem'))throw Error('Junior/STEM merged');
""".replace('FUNCTIONS',funcs)
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(verified=True,events=3123,dossiers=622,new_dossiers=1,deepened_dossiers=6,new_calendar_rows=2,corrected_existing_rows=40,prior_events_unchanged=3081,family_ics=2384,source_urls=975,worldwide_complete=False)))
