"""Independent preservation, child gates, source and full portable database checks."""
import collections,csv,hashlib,io,json,re,sqlite3,subprocess,zipfile
from camp_asia_v121 import ROOT,BASE,NEW
P=ROOT.parent/'stem-family-atlas-work/camp-asia-primary-v121'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clause(key,*values):
 t=re.sub(r'\s+','',(P/(key+'.txt')).read_text())
 for v in values:assert re.sub(r'\s+','',v) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={q['slug']:q for q in b['camp_programmes']['profiles']};z={q['slug']:q for q in d['camp_programmes']['profiles']}
assert len(a)==897 and len(z)==915 and z.keys()-a.keys()==set(NEW) and all(z[k]==v for k,v in a.items())
assert d['camp_programmes']['shortlist'][:217]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==221
assert d['camp_programmes']['gaps'][:244]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==250
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
five=[('20261123','20261127'),('20261130','20261204'),('20261207','20261211'),('20261214','20261218')]
three=[('20261123','20261125'),('20261130','20261202'),('20261207','20261209'),('20261214','20261216')]
two=[('20261126','20261127'),('20261203','20261204'),('20261210','20261211'),('20261217','20261218')]
expected={f'CP{i}-{x}-{y}' for i in range(898,908) for x,y in (three if i in [900,905] else two if i in [902,907] else five)}
assert len(now)==3599 and now.keys()-old.keys()==expected and all(now[k]==v for k,v in old.items())
assert collections.Counter(q['block'] for q in now.values())=={'Соревнования':1153,'События':189,'Лагеря':2257}
assert all(q['start'].startswith('2026-') and q['end']<='2026-12-18' and q['level']=='D — обучение' and q['languages']==[] for k,q in now.items() if k in expected)
osrc={q['url']:q for q in b['sources']};nsrc={q['url']:q for q in d['sources']};assert all(nsrc[k]==v for k,v in osrc.items())
for slug in NEW:
 p=z[slug];assert p['checked']=='2026-10-06' and all(s['checked']=='2026-10-06' for s in p['sources'])
 assert p['timing']['sessions']==([] if not slug.startswith('roboto-') else p['timing']['sessions'])
 if slug.startswith('roboto-'):
  assert len(p['timing']['sessions'])==4 and p['formats']==['day'] and not p['confirmed_instruction_languages']
  assert p['family_fit']['matvey']['status']=='conditional' and p['family_fit']['oscar']['status']=='not_eligible'
  assert 'Код валюты' in p['price']['label']
assert z['roboto-junior-inventor']['timing']['sessions'][0]==['2026-11-23','2026-11-27']
assert 'robotics' not in z['roboto-junior-creator']['themes'] and 'robotics' not in z['roboto-young-creator']['themes']
assert 'ai' not in z['roboto-junior-coder']['themes'] and 'Dash' in z['roboto-junior-coder']['programme']
assert z['taipei-kids-theme-camps']['confirmed_instruction_languages']==['EN','ZH'] and '20%' in z['taipei-kids-theme-camps']['language']
assert all(v['status']=='later' for v in z['one-step-maker']['family_fit'].values())
assert z['malvern-tokyo-british-council']['confirmed_instruction_languages']==['EN'] and '10-летия' in z['malvern-tokyo-british-council']['family_fit']['matvey']['detail']
for slug in ['malvern-tokyo-arts','malvern-tokyo-orchestra','malvern-tokyo-musical']:
 assert z[slug]['confirmed_instruction_languages']==[] and z[slug]['price']['year']==2026 and 'Full' in z[slug]['timing']['label']
assert z['malvern-tokyo-orchestra']['family_fit']['oscar']['status']=='later' and 'Prep 4' in z['malvern-tokyo-orchestra']['age']
assert 'Prep 6' in z['malvern-tokyo-musical']['age'] and '12 100' in z['malvern-tokyo-arts']['price']['label']
assert z['csa-space-challenge']['timing']['sessions']==[] and z['csa-space-challenge']['confirmed_instruction_languages']==[]
assert z['connected-jeju-global-it']['formats']==['family'] and z['connected-jeju-global-it']['price']['year']==2025 and z['connected-jeju-global-it']['confirmed_instruction_languages']==['EN']
assert d['camp_planning']==b['camp_planning'] and len(d['camp_planning']['offers'])==43
clause('tka-theme-camps','Target Age Group: 3–12 years old','20%','taught in English','NT$1,000','NT$1,200')
clause('onestep-main','12-16','2026','雙語','免費參加','3D')
clause('malvern-summer','Prep School Summer ARTS Camp (Full)','Orchestra Camp (Full)','The Malvern Musical Academy (Full)','Age: 6-9')
clause('malvern-bc-pdf-pdf-text','Tue 21 July – Fri 24 July 2026','75,600','92,000','6-7 years old','8-9 years old','minimum number','100%','all in English')
clause('csa-camp','December','7–12','240','360','600','$299','$416','$554','$715')
clause('csa-dec-pdf-pdf-text','MAY / JUNE 2026','7 – 18')
clause('csa-refund','digital','March 11, 2026')
clause('connected-jeju-ru','2025','от 5 до 12 лет','обязательное сопровождение родителя','100% на английском')
clause('connected-jeju-seminar','July 13 – August 2, 2025','Ages 5 to 12','Shinhwa World Resort')
for key,fee,age in [('malvern-arts-current-pdf-ocr','88,000','5 - 11'),('malvern-orchestra-current-pdf-ocr','88,000','8 - 12'),('malvern-musical-current-pdf-ocr','176,000','10-18')]:clause(key,fee,age,'12,100','5,500','May 7th, 2026')
r=json.loads((ROOT/'data/asia-camps-source-receipts-v121.json').read_text());assert len(r['sources'])==45 and sum(q.get('status')==200 for q in r['sources'])==31 and not any(r['external_actions'].values())
for q in r['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
for name in r['visual_pdf_files']+r['private_reader_files']:assert (P/name).stat().st_size>0
assert len(r['visual_pdf_files'])==11 and sum(x['ocr_pages'] for x in r['pdf_extraction'])==40
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
 assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as q:
  assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry'])
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
 return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json');assert json.loads(js)==d
f=P/'verified-v121.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v120.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
changes={}
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
 aa=set(o.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'));removed={r[0] for r in aa-zz}
 allowed={'metadata':{'camp_focus','completeness_audit'},'countries':{'SGP'}}.get(name,set())
 assert removed<=allowed,(name,removed);assert {r[0] for r in aa}<={r[0] for r in zz},name
 if removed:changes[name]=sorted(removed)
assert c.execute('SELECT count(*) FROM events').fetchone()[0]==3599 and c.execute('SELECT count(*) FROM camp_programmes').fetchone()[0]==915
c.close();o.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for s in t.split('BEGIN:VEVENT')[1:]:
  f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None)
  assert f['UID'] not in out;out[f['UID']]=f
 return out
for name,count in [('STEM_подтвержденные_даты.ics',2814),('STEM_крупные_выставки.ics',104)]:
 aa=calendar(prior('dist/downloads/'+name));zz=calendar((ROOT/'dist/downloads'/name).read_bytes())
 assert len(zz)==count and all(zz[k]==v for k,v in aa.items()) and len(zz)-len(aa)==(40 if count==2814 else 0)
 assert all(any(e in uid for e in expected) for uid in zz.keys()-aa.keys())
for name in ['STEM_catalog.csv','STEM_country_coverage.csv']:
 def rows(raw):return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
 aa=rows(prior('dist/downloads/'+name));zz=rows((ROOT/'dist/downloads'/name).read_bytes());key='id' if name=='STEM_catalog.csv' else 'iso'
 x={q[key]:q for q in aa};y={q[key]:q for q in zz};assert all(y[k]==v for k,v in x.items() if key=='id' or k!='SGP')
 assert y.keys()-x.keys()==(expected if key=='id' else set())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for key in ['events','camp_programmes','camp_planning','league_guide','family_strategy']:assert web[key]==d[key]
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']=='active' and plan['native_goal_status']=='active' and plan['next_research']==json.loads(prior('data/research-plan.json'))['next_research']
assert plan['latest_validation']['fully_audited_countries']==0 and plan['latest_validation']['worldwide_complete'] is False
for stem in ['research-plan','asia-camps-audit-v121','asia-camps-source-receipts-v121']:assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
assert 'data-ui-version="121"' in (ROOT/'dist/index.html').read_text()
for f in (ROOT/'dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['camp-planning.js','camp-programmes.js','data.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['nearby-participation.js','nearby-participation.css','experience.js']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
oldplanner=prior('dist/assets/camp-planning.js').decode()
assert (ROOT/'dist/assets/camp-planning.js').read_text()==oldplanner.replace("phase:new Set(['2027','published_2026','next_unannounced','archive_next_unannounced'])","phase:new Set(['2027','published_2026','partial_2026','next_unannounced','archive_next_unannounced'])")
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=121,all_prior_events_preserved=3559,all_prior_dossiers_preserved=897,all_prior_budget_objects_preserved=43,new_dossiers=18,new_calendar_rows=40,complete_sqlite=True,complete_json=True,sqlite_allowed_updated_keys=changes,family_ical=2814,exhibition_ical=104,worldwide_scope_preserved=True,goal='active')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
