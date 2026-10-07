"""Independent source, complete old-record preservation and interactive-filter verification."""
import collections,csv,datetime,hashlib,json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
from camp_europe_v104 import NEW
ROOT=Path(__file__).resolve().parents[1];PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v104'
BASE='22b81c011ffbf31d33a1b6c1f5f428d44b1c4eef'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def tokens(key,*values):
    t=' '.join((PRIMARY/(key+'.txt')).read_text().split())
    for v in values:assert ' '.join(v.split()) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
op={q['slug']:q for q in b['camp_programmes']['profiles']};p={q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3309 and len(old)==3287 and set(old)<=set(ev)
assert all(ev[k]==v for k,v in old.items())
new=[e for k,e in ev.items() if k not in old]
assert collections.Counter(e['camp_dossier_slug'] for e in new)=={'ensr-lausanne-holidays':10,'ensr-futuremakers':1,'spark-deep-freeze':1,'spark-science-sport':1,'xlabs-geneva-engineers':1,'xlabs-geneva-forensic':1,'ecolem-english-summer':2,'iab-youth-summer':5}
assert collections.Counter(e['iso'][0] for e in new)=={'CHE':15,'FRA':2,'ESP':5}
assert all(e['end']>='2026-10-05' and e['end']>=e['start'] and not e['deadline'] for e in new)
assert len(p)==758 and set(p)-set(op)==set(NEW) and len(NEW)==13
assert all(p[s]==v for s,v in op.items())
assert [q['id'] for q in c['profiles'][:745]]==[q['id'] for q in b['camp_programmes']['profiles']]
assert [p[s]['id'] for s in NEW]==['CP%03d'%i for i in range(746,759)]
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
assert c['counts']['countries']==39 and c['counts']['swiss']==106 and c['counts']['source_urls']==1180
assert c['shortlist'][:-3]==b['camp_programmes']['shortlist'] and c['gaps'][:-5]==b['camp_programmes']['gaps']
assert len(c['shortlist'])==174
for q in c['shortlist']:assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
assert sum(e['block']=='Лагеря' for e in ev.values())==1978 and len(c['generated_event_ids'])==1515
assert c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==46
tokens('ensr-holiday','30 March - 2 April 2027','5-9 April 2027','1-2 July 2027','16-20 August 2027','23-24 August 2027','FutureMakers','13 to 18','CHF 1,250','in English')
tokens('ensr-form-young','CHF 135.-/day','CHF 95.-/half-day','CHF 60.-/half-day','36 months','2026 Automn Holiday camps')
tokens('ensr-form-older','CHF 140 .-/day','These camps are open to ENSR students as well as children who do not attend the school','No refund will be made nor substitute day','Health, accident and civil responsibility insurances are compulsory')
assert p['ensr-lausanne-holidays']['confirmed_instruction_languages']==[] and p['ensr-lausanne-holidays']['price']['year']==2026
assert len(p['ensr-lausanne-holidays']['timing']['sessions'])==10
assert all(p['ensr-futuremakers']['family_fit'][x]['status']=='later' for x in ['matvey','oscar'])
tokens('tandem-holiday','Camps are only available for children attending Tandem-IMS','26th-30th April 2027','15th - 19th February 2027')
assert not any('tandem' in s or 'numerique' in s or 'sanpatricio' in s for s in NEW)
tokens('spark-index','750 CHF','795 CHF','26th - 30th April 2027','5th - 9th April 2026','camp is led in English','maximum of 20 children','Booking opening soon')
tokens('spark-deep-freeze','15-19th February 2027','based on last year','Age 5-11')
tokens('spark-sport','13th - 17th July 2026','Suurstoffi 41c','based on last year')
tokens('spark-book-freeze','24 spots left','750 Swiss francs','15–29 days','14 days or fewer','48 hours','electronic light-up Northern Lights')
tokens('spark-terms','CHF 100 administrative fee','72 hours','20 CHF per hour per child','15-minute intervals','conducted in English')
assert p['spark-science-sport']['timing']['sessions']==[['2027-04-26','2027-04-30']]
tokens('xlabs-index','19-23 October 2026','15-19 February 2027','8-12','bilingual French-English','CHF 375.-','CHF 595.-','CHF 25/hour','bring a lunchbox')
web=json.loads((PRIMARY/'xlabs-web-reader.json').read_text())
for x in ['Build a Solar-Powered Boat','Launch a Rocket','Decode Secret Messages','simulated blood-typing','5b. Cancellation by client (Camps)','Effective date: January 01, 2019','Between 30 days and 10 days','medical certificate']:assert x in web,x
for s in ['xlabs-geneva-engineers','xlabs-geneva-forensic']:assert p[s]['language_evidence_role']=='partial_bilingual' and p[s]['confirmed_instruction_languages']==['EN']
tokens('hif-spring','12–17 years','10-30 April 2027','21 Days / 20 Nights','14 nights','7 nights','CHF 6,985','CHF 300','CHF 500','CHF 1,000')
tokens('hif-spring-de','30. März bis 10. April 2027')
assert not p['hif-spring-journey']['timing']['sessions']
for k in ['eisb-chess','eisb-science']:tokens(k,'Julio 2027','2019–2012','antes del 1 de junio del 2026','Familias externas')
tokens('eisb-science','Actividades en inglés guiadas por profesores')
tokens('eisb-english','2022–2012','Inmersión lingüística en inglés')
tokens('eisb-spanish','2020–2014','Actividades íntegramente en español')
for s in ['eisb-chess-robotics','eisb-scientific-talent']:assert p[s]['family_fit']['oscar']['status']=='not_eligible'
assert p['eisb-chess-robotics']['confirmed_instruction_languages']==[]
for s in NEW:
 if s.startswith('eisb-'):assert not p[s]['timing']['sessions'] and p[s]['price']['year'] is None
tokens('ecolem-summer','July 5–16, 2027','100% English','3 to 7','July 16, 2027 (4 days)','395 €','335 €','+ 90 €','bring their own lunchbox','welcome all children')
assert p['ecolem-english-summer']['price']['year'] is None and p['ecolem-english-summer']['family_fit']['matvey']['status']=='not_eligible'
tokens('iab-short','28 Jun – 30 Jul 2027','All classes are taught in English','Summer 2026','€210','26 - 30 July')
tokens('iab-camp','Summer Camp Dates 2026','Mon 22 June','fluent in Spanish','10% off for two siblings','Ages 12+')
assert p['iab-youth-summer']['price']['year']==2026 and len(p['iab-youth-summer']['timing']['sessions'])==5
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
for f,v in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/f).read_text())==v
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite');assert con.execute('PRAGMA page_size').fetchone()[0]==1024
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert {json.loads(v)['id']:json.loads(v) for v, in con.execute('SELECT record_json FROM events')}==ev
assert {json.loads(v)['slug']:json.loads(v) for v, in con.execute('SELECT record_json FROM camp_programmes')}==p
oldfile=PRIMARY/'baseline.sqlite';oldfile.write_bytes(prior('dist/downloads/STEM_database.sqlite'));oc=sqlite3.connect(oldfile)
schema=lambda db:sorted(db.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"))
assert schema(oc)==schema(con)
for name, in oc.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
    rows=set(oc.execute('SELECT * FROM "'+name+'"'));now=set(con.execute('SELECT * FROM "'+name+'"'))
    if name not in ['metadata','countries']:assert rows<=now,name
    elif name=='metadata':assert {r[0] for r in rows-now}=={'completeness_audit','camp_focus'}
    else:
        delta=rows-now;assert {r[0] for r in delta}=={'CHE','FRA','ESP'}
        for r in delta:
            q=con.execute('SELECT * FROM countries WHERE iso=?',(r[0],)).fetchone();assert r[:3]==q[:3]
oc.close();con.close()
assert all(f.stat().st_size<=26214400 for f in (ROOT/'dist').rglob('*') if f.is_file()),'Static per-file limit'
rows=lambda raw:{r['id']:r for r in csv.DictReader(raw.decode('utf-8-sig').splitlines())}
path='dist/downloads/STEM_catalog.csv';oldcsv=rows(prior(path));newcsv=rows((ROOT/path).read_bytes());assert len(newcsv)==3309 and all(newcsv[k]==v for k,v in oldcsv.items())
md=(ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.md').read_text()
for s in NEW:assert p[s]['provider'] in md and p[s]['editorial_reason'] in md
def calendar(value):
    out={};t=value.decode().replace('\r\n ','').replace('\r\n\t','')
    for block in t.split('BEGIN:VEVENT')[1:]:
        f={s.split(':',1)[0]:s.split(':',1)[1] for s in block.split('END:VEVENT')[0].splitlines() if ':' in s};assert f['UID'] not in out;out[f['UID']]=f
    return out
path='dist/downloads/STEM_подтвержденные_даты.ics';oldcal=calendar(prior(path));now=calendar((ROOT/path).read_bytes())
assert len(now)==2564 and len(oldcal)==2543 and set(oldcal)<=set(now)
for uid,v in oldcal.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
assert set(now)-set(oldcal)=={'stem-'+e['id']+'@family-stem.local' for e in new if e['camp_dossier_slug']!='ensr-futuremakers'}
for e in new:
    if e['camp_dossier_slug']=='ensr-futuremakers':continue
    f=now['stem-'+e['id']+'@family-stem.local'];assert f['DTSTART;VALUE=DATE']==e['start'].replace('-','')
    assert f['DTEND;VALUE=DATE']==(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d') and f['STATUS']=='TENTATIVE'
expo='dist/downloads/STEM_крупные_выставки.ics';oe=calendar(prior(expo));ne=calendar((ROOT/expo).read_bytes());assert len(ne)==104 and set(oe)==set(ne)
for uid,v in oe.items():assert {k:x for k,x in ne[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==104
assert {q['id'] for q in bp['requirements']}=={q['id'] for q in plan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==bp[k],k
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['europe-camp-audit-v104','europe-camp-source-receipts-v104']:
    v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
    assert not any(v['external_actions'].values())
    if 'sources' in v:
        assert len(v['sources'])==29 and len(v['dossier_source_urls_added'])==22 and sum(q.get('status')==200 for q in v['sources'])==26
        for q in v['sources']:
            if q.get('status')==200:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
        for q in v['web_reader_fallbacks']:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_europe_camp_audit_v104.json' in js
assert 'data-ui-version="104"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(s for s in js.splitlines() if s.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:''};
FUNCTIONS
const fresh=new Set(NEW);const result=()=>new Set(filtered().filter(p=>fresh.has(p.slug)).map(p=>p.slug));
const check=(names)=>{const a=result(),b=new Set(names);if(a.size!==b.size||[...a].some(s=>!b.has(s)))throw Error(JSON.stringify([...a]));};
check(NEW);cs.language='EN';check(['ensr-futuremakers','spark-deep-freeze','spark-science-sport','xlabs-geneva-engineers','xlabs-geneva-forensic','eisb-english-summer','eisb-scientific-talent','ecolem-english-summer','iab-youth-summer']);
cs.language='ES';check(['eisb-spanish-summer']);cs.language='';cs.child='both';check(['ensr-lausanne-holidays','spark-deep-freeze','spark-science-sport','eisb-english-summer','eisb-spanish-summer','iab-youth-summer']);
cs.phase='2027';check(['ensr-lausanne-holidays','spark-deep-freeze','spark-science-sport','eisb-english-summer','eisb-spanish-summer','iab-youth-summer']);
cs.phase='';cs.child='';cs.country='FRA';check(['ecolem-english-summer']);cs.country='ESP';check(['eisb-english-summer','eisb-spanish-summer','eisb-chess-robotics','eisb-scientific-talent','iab-youth-summer']);
console.log('family/language/year/country filters passed');
""".replace('FUNCTIONS',funcs).replace('NEW',json.dumps(NEW))
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(status='passed',version=104,new_dossiers=13,new_calendar_rows=22,new_family_ics=21,dossiers=758,countries=39,source_urls=1180,events=3309,camp_learning_records=1978,goal='active'),ensure_ascii=False))
