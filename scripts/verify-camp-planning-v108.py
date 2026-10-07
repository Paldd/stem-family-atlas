"""Check selected source clauses, full old-record preservation and portable data."""
import collections,csv,hashlib,io,json,sqlite3,subprocess,zipfile
from pathlib import Path
from camp_planning_v108 import ROOT,BASE,build
P=ROOT.parent/'stem-family-atlas-work/camp-planning-primary-v108'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT)
def clauses(key,*values):
    text=' '.join((P/(key+'.txt')).read_text().split())
    for v in values:assert ' '.join(v.split()) in text,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
assert {k:v for k,v in d.items() if k!='camp_planning'}==b
assert d['camp_planning']==build()
assert len(d['events'])==3348 and len(d['camp_programmes']['profiles'])==778
assert collections.Counter(e['block'] for e in d['events'])=={'Соревнования':1153,'События':189,'Лагеря':2006}
assert len(d['league_guide']['profiles'])==141 and len(d['camp_programmes']['shortlist'])==182
assert {o['slug'] for o in d['camp_planning']['offers']}<=set(p['slug'] for p in d['camp_programmes']['profiles'])
clauses('leselfes-contract',"4'990.-","6'500.-",'Registration fees *','Health & accident insurance/week *','150.-','120.-','Robotics','10+','180.-','Shelter Building','incl.','return ticket','190.-','non-',"refundable deposit of CHF 1'000",'30 days','minus the CHF 1,000 deposit')
clauses('leselfes-summer','aged 6 to 17')
clauses('garenne-contract','5-12 Year Olds - Dates and Fees','CHF 7’200','CHF 6’550','Monday to Saturday in the first week and Monday to Friday in the second week','EXTRAS for 8 to 12 Year Olds','Robotics: 3 sessions exploring the world of 3D design and computing','Health Insurance per day','CHF 10','Weekly pocket money Ages 5-9 / Ages 10-12','CHF 30 / CHF 50','discount of 10%','all be either boarding students or day students','65 days or more')
clauses('garenne-form','Health and medical insurance is invoiced at CHF 10 per day and is compulsory for non-Swiss residents.')
clauses('garenne-main','If parents plan to stay in the local area during Summer Camp, their child must attend as a Day Student.')
clauses('tasis-fees','Ages 7–10','Ages 4–6','CHF 9,200','CHF 4,500','CHF 3,500','15:00','17:30','2027')
clauses('tasis-faq','we do not allow siblings or friends to room together','Enrollment deposits are not refundable at any time','May 15','seven days','accident/health insurance','Day students who are not residents of Switzerland can purchase')
clauses('ermitage-camp','fallcamp2026.png','4-6 and 7-10 years old','610€ per week','135€ per day','19','23')
r=json.loads((ROOT/'data/camp-planning-source-receipts-v108.json').read_text())
assert len(r['sources'])==10 and sum(q.get('status')==200 for q in r['sources'])==9
assert not any(r['external_actions'].values())
for q in r['sources']:
    if q['body_snapshot_retained']:
        raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
w=(P/'primary-web-reader.json').read_bytes();assert hashlib.sha256(w).hexdigest()==r['primary_reader']['sha256']
assert 'Total lines: 0' in json.loads(w)['response'] and '2026' in json.loads(w)['response']
for name,pages in [('leselfes-contract',[1,2]),('garenne-contract',[3,4,7,8,9])]:assert all((P/f'{name}-page-{v}.png').stat().st_size>1000 for v in pages)
def portable(manifest,ext):
    m=json.loads((ROOT/'dist/downloads'/manifest).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
    assert m['complete_database'] and len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256']
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        assert z.testzip() is None and z.namelist()==[m[ext+'_entry'],'README.txt']
        body=z.read(m[ext+'_entry']);assert m[ext+'_sha256'] in z.read('README.txt').decode()
    assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
    f=ROOT/'dist/downloads'/m[ext+'_entry'];assert f.exists()==m['raw_download_available']
    if f.exists():assert f.read_bytes()==body
    return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json')
assert json.loads(js)==d
db=P/'verified-v108.sqlite';db.write_bytes(sql);c=sqlite3.connect(db)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as z:oldsql=z.read('STEM_database.sqlite')
oldf=P/'baseline-v107.sqlite';oldf.write_bytes(oldsql);o=sqlite3.connect(oldf)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"))
assert schema(c)==schema(o)
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
    a=set(o.execute('SELECT * FROM "'+name+'"'));z=set(c.execute('SELECT * FROM "'+name+'"'));assert a<=z,name
    if name=='metadata':assert {row[0] for row in z-a}=={'camp_planning'}
    else:assert a==z,name
assert json.loads(c.execute("SELECT value FROM metadata WHERE key='camp_planning'").fetchone()[0])==d['camp_planning']
c.close();o.close()
for p in ['STEM_catalog.csv','STEM_календарь_2026_2027.csv','STEM_крупные_выставки.csv']:
    f=ROOT/'dist/downloads'/p
    if f.exists():assert list(csv.DictReader(io.StringIO(f.read_text(encoding='utf-8-sig'))))==list(csv.DictReader(io.StringIO(prior('dist/downloads/'+p).decode('utf-8-sig')))),p
def calendar(raw):
    t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
    for s in t.split('BEGIN:VEVENT')[1:]:
        f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v}
        f.pop('DTSTAMP',None);assert f['UID'] not in out;out[f['UID']]=f
    return out
for name,n in [('STEM_подтвержденные_даты.ics',2593),('STEM_крупные_выставки.ics',104)]:
    p='dist/downloads/'+name;a=calendar(prior(p));z=calendar((ROOT/p).read_bytes());assert a==z and len(z)==n
plan=json.loads((ROOT/'data/research-plan.json').read_text());old=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==108
assert plan['previous_goal_turn_classification']['classification']=='progress' and BASE in plan['previous_goal_turn_classification']['evidence']
assert {q['id'] for q in plan['requirements']}=={q['id'] for q in old['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==old[k],k
assert not plan['latest_validation']['worldwide_complete'] and d['coverage_summary']['fully_audited_countries']==0
assert plan['complete_database_download']==sm and plan['complete_json_download']==jm
for stem in ['research-plan','camp-planning-audit-v108','camp-planning-source-receipts-v108']:
    assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for k in ['camp_programmes','camp_planning','events','league_guide']:assert web[k]==d[k]
html=(ROOT/'dist/index.html').read_text();assert 'data-ui-version="108"' in html and html.index('assets/camp-planning.js?v=108')<html.index('assets/camp-programmes.js?v=108')
assert 'href="downloads/STEM_database_json.zip"' in html and 'STEM_camp_planning_audit_v108.json' in html
for f in ROOT.joinpath('dist').rglob('*'):
    if f.is_file():assert f.stat().st_size<=26214400,(str(f),f.stat().st_size)
for name in ['data.js','camp-planning.js','camp-programmes.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
fc=json.loads((P/'functional-check.json').read_text());assert fc['status']=='passed' and fc['real_chromium_offline_dom'] and fc['external_network_requests']==0
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=108,all_old_data_preserved=True,events=3348,camp_dossiers=778,budget_scenarios=9,family_ics=2593,exhibition_ics=104,complete_sqlite=True,complete_json=True,goal='active')
(P/'independent-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
