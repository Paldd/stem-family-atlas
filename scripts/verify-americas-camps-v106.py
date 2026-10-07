"""Independent source clauses, prior-row continuity and complete SQLite ZIP verification."""
import collections,csv,datetime,hashlib,json,sqlite3,subprocess,zipfile
from pathlib import Path
from camp_catalog_bridge import integrate
from camp_americas_v106 import NEW
from database_download import package_database
ROOT=Path(__file__).resolve().parents[1];PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v106'
BASE='ed1911191baa568d0082d2212685482e5e0946b3'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def tokens(key,*values):
    t=' '.join((PRIMARY/(key+'.txt')).read_text().split())
    for v in values:assert ' '.join(v.split()) in t,(key,v)
def reader(filename,*values):
    t=json.loads((PRIMARY/filename).read_text())['response']
    for v in values:assert v in t,(filename,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
op={q['slug']:q for q in b['camp_programmes']['profiles']};p={q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3337 and len(old)==3323 and set(old)<=set(ev)
assert all(ev[k]==v for k,v in old.items())
new=[e for k,e in ev.items() if k not in old]
assert collections.Counter(e['camp_dossier_slug'] for e in new)=={'journey-winter-minecraft':1,'journey-winter-robotics':1,'journey-winter-mario':1,'journey-winter-superheroes':1,'kidnetix-winter':1,'explorations-break-tech':2,'explorations-july-general':2,'explorations-summer-tech':5}
assert collections.Counter(e['iso'][0] for e in new)=={'USA':4,'CAN':10}
assert all(e['end']>='2026-10-05' and e['end']>=e['start'] and not e['deadline'] for e in new)
assert len(p)==len(c['profiles'])==778 and set(p)-set(op)==set(NEW) and len(NEW)==9
assert all(p[s]==v for s,v in op.items())
assert [q['id'] for q in c['profiles'][:769]]==[q['id'] for q in b['camp_programmes']['profiles']]
assert [p[s]['id'] for s in NEW]==['CP%03d'%i for i in range(770,779)]
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
assert c['counts']['countries']==39 and c['counts']['swiss']==106 and c['counts']['source_urls']==1215
assert c['shortlist'][:-4]==b['camp_programmes']['shortlist'] and c['gaps'][:-6]==b['camp_programmes']['gaps']
assert len(c['shortlist'])==182 and len(c['gaps'])==185
for q in c['shortlist']:assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
assert sum(e['block']=='Лагеря' for e in ev.values())==2006 and len(c['generated_event_ids'])==1543
assert c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==49
tokens('journey-winter','Winter 2026','Dec 21-23','7-11','$219','$199 early bird','Intro to Robotics: Amazing Amusement Park','Dec 28-31','6-10','$289','$269 early bird','12:00-3:00pm','7-12','LEGO Superheroes','$249','$229 early bird','November 2','up to 20 campers','Vancouver, WA','Beaverton, OR')
tokens('journey-faq','LEGO, robots, Chromebooks and every material','service fee is added at checkout','more than 15 days','$35','If we cancel, you get a full refund')
tokens('journey-refund','15 days','at least 7 days','$35','case-by-case')
assert all(p[s]['confirmed_instruction_languages']==[] for s in NEW if s!='nova-mex-itclub')
for s in ['journey-winter-minecraft','journey-winter-mario']:assert p[s]['family_fit']['oscar']['status']=='later'
for s in ['journey-winter-robotics','journey-winter-superheroes']:assert p[s]['family_fit']['oscar']['status']=='conditional'
assert p['journey-winter-superheroes']['themes']==['engineering']
tokens('steamup-winter','December 21, 2026 - January 1, 2027','Closed 12/24, 12,25, 12/31, 1/1','November 15, 2026','$84 per week','$1.85 per minute','5 to 15','3 through 15')
tokens('steamup-thanks','November 23, 2026 - November 27, 2026','Closed Thursday 11/26/26','Starting at $250')
tokens('steamup-spring','March 15, 2027 - March 19, 2027','Starting at $250 per week')
assert all(p[s]==op[s] for s in ['steamup-thanksgiving','steamup-winter','steamup-spring'])
tokens('kidnetix-winter','December 21 - December 31, 2026','8:30AM - 4:30PM','$175/ 2 Weeks EARLY BIRD','4 - 12','may build and experiment with LEGO robotics')
assert 'robotics' not in p['kidnetix-winter']['themes']
ke=next(e for e in new if e['camp_dossier_slug']=='kidnetix-winter');assert 'attendance_weekdays' not in ke
tokens('nova-mex-itcamp','IT Club de Verano 2025','21 de julio','5 semanas','IT Club Invierno','Español','8-15 años','Gauss 12','Lego Education Prime','todo el material lo proveemos nosotros','un lunch')
assert p['nova-mex-itclub']['confirmed_instruction_languages']==['ES'] and p['nova-mex-itclub']['timing']['sessions']==[] and p['nova-mex-itclub']['price']['year']==2025
assert p['nova-mex-itclub']['family_fit']['oscar']['status']=='later'
reader('explorations-primary-web.json','Winter Break Camp 2026','December 28 - January 1','Spring Break Camp 2027','March 1- 5','Robotics, and Video Game Design','3D Printing, and Video Game Design','485$/week','6591 Somerled','10% administration fee','10 days prior','25$/day','5.00$/per minute','Rates for 2026')
reader('explorations-registration-primary-web.json','Winter Camp 2026-27','Spring Camp 2027','Summer Camp 2027','July 5-16','July 19-30','August 16-20','August 23-27','first day of the program','kindergarten','completed grade 1','Activities from previous years include','July 6 - July 17','785$/session')
tokens('explorations-age6','Kindergarten','Summer Camp 2027','July 5-16','July 19-30','$785','2290 Cavendish','8:00-8:45','3:30-4:00','4:00-6:00')
tokens('explorations-age9','Summer Camp 2027','June 28 - July 02','July 5-16','July 19-30','Aug 2-6','Aug 9-13','Aug 16-20','Robots & Engineering','Aug 23-27','$545','3D Printing & Engineering')
ts=p['explorations-summer-tech']['timing']['session_details'];assert [v['start'] for v in ts]==['2027-06-28','2027-08-02','2027-08-09','2027-08-16','2027-08-23']
assert '545' in ts[-1]['price'] and all('445' in v['price'] for v in ts[:-1])
assert all('6591Somerled' in e['city'] for e in new if e['camp_dossier_slug'] in ['explorations-break-tech','explorations-summer-tech'])
be=next(e for e in new if e['camp_dossier_slug']=='explorations-break-tech' and e['start'].startswith('2026'));assert be['osc'].startswith('Нет')
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
for f,v in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/f).read_text())==v
manifest=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text());zb=(ROOT/'dist/downloads/STEM_database.zip').read_bytes()
assert manifest['complete_database'] and len(zb)==manifest['archive_bytes'] and hashlib.sha256(zb).hexdigest()==manifest['archive_sha256']
with zipfile.ZipFile(ROOT/'dist/downloads/STEM_database.zip') as z:
    assert z.namelist()==['STEM_database.sqlite','README.txt'] and z.testzip() is None
    body=z.read('STEM_database.sqlite');assert manifest['sqlite_sha256'] in z.read('README.txt').decode()
assert len(body)==manifest['sqlite_bytes'] and hashlib.sha256(body).hexdigest()==manifest['sqlite_sha256']
assert len(body)>26214400 and not manifest['raw_download_available'] and not (ROOT/'dist/downloads/STEM_database.sqlite').exists()
extracted=PRIMARY/'verified-full.sqlite';extracted.write_bytes(body);con=sqlite3.connect(extracted)
assert con.execute('PRAGMA page_size').fetchone()[0]==1024
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
        delta=rows-now;assert {r[0] for r in delta}<={'USA','CAN','MEX'}
        for r in delta:
            q=con.execute('SELECT * FROM countries WHERE iso=?',(r[0],)).fetchone();assert r[:3]==q[:3]
oc.close();con.close()
# Exercise both availability branches against the real complete SQLite; ZIP bytes are deterministic.
for name,limit,available in [('remove-oversize',1,False),('retain-at-boundary',len(body),True)]:
    folder=PRIMARY/'packaging-check'/name;folder.mkdir(parents=True,exist_ok=True);raw=folder/'STEM_database.sqlite';raw.write_bytes(body)
    m=package_database(raw,max_file_bytes=limit)
    assert m['raw_download_available']==available and raw.exists()==available
    assert m['archive_sha256']==manifest['archive_sha256'] and m['sqlite_sha256']==manifest['sqlite_sha256']
    with zipfile.ZipFile(folder/'STEM_database.zip') as z:assert z.read('STEM_database.sqlite')==body
assert all(f.stat().st_size<=26214400 for f in (ROOT/'dist').rglob('*') if f.is_file()),'Static per-file limit'
rows=lambda raw:{r['id']:r for r in csv.DictReader(raw.decode('utf-8-sig').splitlines())}
path='dist/downloads/STEM_catalog.csv';oldcsv=rows(prior(path));newcsv=rows((ROOT/path).read_bytes());assert len(newcsv)==3337 and all(newcsv[k]==v for k,v in oldcsv.items())
md=(ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.md').read_text()
for s in NEW:assert p[s]['provider'] in md and p[s]['editorial_reason'] in md
def calendar(value):
    out={};t=value.decode().replace('\r\n ','').replace('\r\n\t','')
    for block in t.split('BEGIN:VEVENT')[1:]:
        f={s.split(':',1)[0]:s.split(':',1)[1] for s in block.split('END:VEVENT')[0].splitlines() if ':' in s};assert f['UID'] not in out;out[f['UID']]=f
    return out
path='dist/downloads/STEM_подтвержденные_даты.ics';oldcal=calendar(prior(path));now=calendar((ROOT/path).read_bytes())
assert len(now)==2591 and len(oldcal)==2577 and set(oldcal)<=set(now)
for uid,v in oldcal.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
assert set(now)-set(oldcal)=={'stem-'+e['id']+'@family-stem.local' for e in new}
for e in new:
    f=now['stem-'+e['id']+'@family-stem.local'];assert f['DTSTART;VALUE=DATE']==e['start'].replace('-','')
    assert f['DTEND;VALUE=DATE']==(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d') and f['STATUS']=='TENTATIVE'
expo='dist/downloads/STEM_крупные_выставки.ics';oe=calendar(prior(expo));ne=calendar((ROOT/expo).read_bytes());assert len(ne)==104 and set(oe)==set(ne)
for uid,v in oe.items():assert {k:x for k,x in ne[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==106
assert {q['id'] for q in bp['requirements']}=={q['id'] for q in plan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==bp[k],k
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
assert plan['complete_database_download']==manifest
for stem in ['americas-camp-audit-v106','americas-camp-source-receipts-v106']:
    v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
    assert not any(v['external_actions'].values())
    if 'sources' in v:
        assert len(v['sources'])==23 and len(v['dossier_source_urls_added'])==12 and sum(q.get('status')==200 for q in v['sources'])==17
        for q in v['sources']:
            if q['body_snapshot_retained']:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_americas_camp_audit_v106.json' in js
html=(ROOT/'dist/index.html').read_text();assert 'data-ui-version="106"' in html and 'href="downloads/STEM_database.zip"' in html and 'href="downloads/STEM_database.sqlite"' not in html
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(s for s in js.splitlines() if s.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:''};
FUNCTIONS
const fresh=new Set(NEW);const result=()=>new Set(filtered().filter(p=>fresh.has(p.slug)).map(p=>p.slug));
const check=(names)=>{const a=result(),b=new Set(names);if(a.size!==b.size||[...a].some(s=>!b.has(s)))throw Error(JSON.stringify([...a]));};
check(NEW);cs.language='EN';check([]);cs.language='ES';check(['nova-mex-itclub']);cs.language='';cs.child='both';check(['journey-winter-robotics','journey-winter-superheroes','kidnetix-winter','explorations-break-tech','explorations-july-general','explorations-summer-tech']);
cs.phase='2027';check(['explorations-break-tech','explorations-july-general','explorations-summer-tech']);
cs.phase='';cs.child='';cs.country='USA';check(NEW.slice(0,4));cs.country='CAN';check(['kidnetix-winter','explorations-break-tech','explorations-july-general','explorations-summer-tech']);
cs.country='MEX';check(['nova-mex-itclub']);cs.country='';cs.theme='robotics';check(['journey-winter-robotics','nova-mex-itclub','explorations-break-tech','explorations-summer-tech']);
console.log('family/language/year/country/theme filters passed');
""".replace('FUNCTIONS',funcs).replace('NEW',json.dumps(NEW))
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
print(json.dumps(dict(status='passed',version=106,new_dossiers=9,new_calendar_rows=14,new_family_ics=14,dossiers=778,countries=39,source_urls=1215,events=3337,camp_learning_records=2006,complete_database_zip_bytes=manifest['archive_bytes'],goal='active'),ensure_ascii=False))
