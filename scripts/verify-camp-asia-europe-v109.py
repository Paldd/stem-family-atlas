"""Independent preservation/export/source gates for this bounded pass."""
import collections,csv,hashlib,io,json,sqlite3,subprocess,zipfile
from camp_asia_europe_v109 import ROOT,BASE,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-asia-europe-primary-v109'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clauses(key,*values):
 t=' '.join((P/(key+'.txt')).read_text().split())
 for v in values:assert ' '.join(v.split()) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
assert {k:v for k,v in d.items() if k not in ['camp_programmes','sources','source_count','events']}=={k:v for k,v in b.items() if k not in ['camp_programmes','sources','source_count','events']}
a={p['slug']:p for p in b['camp_programmes']['profiles']};z={p['slug']:p for p in d['camp_programmes']['profiles']}
assert len(a)==778 and len(z)==798 and set(z)-set(a)==set(NEW)
assert {s for s in a if a[s]!=z[s]}==set(UPDATED)
assert all(a[s]['id']==z[s]['id'] for s in a)
assert len({p['id'] for p in z.values()})==798
assert len(d['camp_programmes']['shortlist'])==185 and len(d['camp_programmes']['gaps'])==190
assert d['camp_programmes']['shortlist'][:182]==b['camp_programmes']['shortlist'] and d['camp_programmes']['gaps'][:185]==b['camp_programmes']['gaps']
assert d['camp_programmes']['generated_event_ids']==b['camp_programmes']['generated_event_ids']
e={q['id']:q for q in b['events']};v={q['id']:q for q in d['events']}
assert e.keys()==v.keys() and {k for k in e if e[k]!=v[k]}=={'L183'}
assert v['L183']['languages']==[] and not v['L183']['start'] and not v['L183']['deadline']
assert collections.Counter(q['block'] for q in v.values())=={'Соревнования':1153,'События':189,'Лагеря':2006}
oldsrc={q['url']:q for q in b['sources']};newsrc={q['url']:q for q in d['sources']};assert all(newsrc[u]==q for u,q in oldsrc.items()) and len(newsrc)-len(oldsrc)==14
for s in NEW:
 p=z[s];assert p['timing']['sessions']==[] and not p['calendar_links']
 assert p['checked']=='2026-10-05' and p['price']['year'] in [None,2026]
 if p['iso']=='SGP':assert p['formats']==['day'] and p['confirmed_instruction_languages']==(['EN'] if s=='xcl-eal' else [])
assert z['xcl-future-engineers']['family_fit']['oscar']['status']=='later'
assert all(z[s]['family_fit']['matvey']['status']=='not_eligible' for s in ['xcl-stem-juniors','xcl-junior-coding','xcl-multi-young'])
assert z['american-british-damian']['family_fit']['matvey']['status']=='later'
assert z['american-manga-ayrolle']['price']['year']==2026 and '779' in z['american-manga-ayrolle']['price']['label']
assert all(z[s]['price']['year'] is None for s in ['xcl-generative-ai','xcl-design-thinking','xcl-minecraft-two','xcl-science-explorers','xcl-entrepreneurship-101','xcl-multi-adventure','xcl-stem-juniors'])
clauses('xcl-code','For ages 10 to 15 years','Date: Jul 6 to 10','Date: Summer 2026','$710','$750','$760','VEX robotics')
clauses('xcl-schedule','FOR AGES 7 to 15','May 15, 2026')
clauses('xcl-engineering','For ages 6 to 8 & 9 to 11 years','take home their very own custom-built toys','$760')
clauses('xcl-juniors','AGES 4 TO 7','Dates: June 29 to Jul 3','$720')
clauses('xcl-game','For ages 7 to 9 years old','For ages 7 to 14 years','Dates: TBC','For ages 10 to 14 years','laptop and login account','MidJourney')
clauses('xcl-entrepreneur','For ages 8 to 12 years','Date: TBC','Date: Summer 2026','wireframes for a mobile app')
clauses('xcl-steam','June 22 to 26 & Jul 13 to 17 2026')
clauses('xcl-science','For ages 7 to 11 years','aged 7 to 12','Take-Home Projects:')
clauses('xcl-multi','For ages 5 to 8 years old','For ages 9 to 14 years','teacher and coach availability')
clauses('xcl-faq','$120 per week','minimum of 6 riders','full or partial refund','potty trained','low level of English')
clauses('xcl-terms-correct','3 working days','no cancellations or refunds','at least 10 days','same season','Medical and Accident Insurance','not provide coverage')
clauses('american-manga-intake','10-14 ans','12 juil','17 juil 2026','779','pour 6 jours','Complet','60€','voyagera seul','10 heures de cours')
clauses('american-british-intake','11-15 ans','749','1 469','24 juil 2026','5 ou 12 nuits','60€','voyagera seul')
clauses('respira-tech','de 50 participantes','1 SEMANA','78€','90€','102€','Navidad 2026 – 2027')
r=json.loads((ROOT/'data/camp-asia-europe-source-receipts-v109.json').read_text());assert len(r['sources'])==27 and sum(q.get('status')==200 for q in r['sources'])==26 and not any(r['external_actions'].values())
for q in r['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes();assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as q:
  assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry']);assert m[ext+'_sha256'] in q.read('README.txt').decode()
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 f=ROOT/'dist/downloads'/m[ext+'_entry'];assert f.exists()==m['raw_download_available'];assert f.exists()==(len(body)<=26214400)
 if f.exists():assert f.read_bytes()==body
 return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json');assert json.loads(js)==d
f=P/'verified-v109.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v108.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
changed_ids={z[s]['id'] for s in UPDATED}
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
 old=list(o.execute('SELECT * FROM "'+name+'"'));new=list(c.execute('SELECT * FROM "'+name+'"'));aa=set(old);zz=set(new)
 if name=='events':
  assert {r[0] for r in old}=={r[0] for r in new};assert {r[0] for r in aa-zz}=={r[0] for r in zz-aa}=={'L183'}
 elif name=='camp_programmes':
  assert {r[0] for r in aa-zz}==changed_ids and len(zz-aa)==22
 elif name in ['sources','camp_programme_sources']:assert aa<=zz
 else:assert aa==zz,name
assert {q['id']:q for q in d['events']}=={k:json.loads(value) for k,value in c.execute('SELECT id,record_json FROM events')}
assert {q['slug']:q for q in d['camp_programmes']['profiles']}=={k:json.loads(value) for k,value in c.execute('SELECT slug,record_json FROM camp_programmes')}
assert json.loads(c.execute("SELECT value FROM metadata WHERE key='camp_planning'").fetchone()[0])==b['camp_planning'];c.close();o.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for s in t.split('BEGIN:VEVENT')[1:]:
  f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None);assert f['UID'] not in out;out[f['UID']]=f
 return out
for name,n in [('STEM_подтвержденные_даты.ics',2593),('STEM_крупные_выставки.ics',104)]:
 p='dist/downloads/'+name;assert calendar(prior(p))==calendar((ROOT/p).read_bytes()) and len(calendar((ROOT/p).read_bytes()))==n
for name in ['STEM_catalog.csv','STEM_календарь_2026_2027.csv','STEM_крупные_выставки.csv']:
 p=ROOT/'dist/downloads'/name
 if p.exists():
  a=list(csv.DictReader(io.StringIO(prior('dist/downloads/'+name).decode('utf-8-sig'))));zv=list(csv.DictReader(io.StringIO(p.read_text(encoding='utf-8-sig'))));assert len(a)==len(zv)
  assert all(vv==ww or vv.get('id')=='L183' or vv.get('ID')=='L183' for vv,ww in zip(a,zv)),name
plan=json.loads((ROOT/'data/research-plan.json').read_text());oldplan=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==109
assert {q['id'] for q in plan['requirements']}=={q['id'] for q in oldplan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==oldplan[k],k
assert plan['complete_database_download']==sm and plan['complete_json_download']==jm
assert d['coverage_summary']['fully_audited_countries']==0 and not plan['latest_validation']['worldwide_complete']
for stem in ['research-plan','camp-asia-europe-audit-v109','camp-asia-europe-source-receipts-v109']:
 assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for k in ['events','camp_programmes','camp_planning','league_guide']:assert web[k]==d[k]
html=(ROOT/'dist/index.html').read_text();assert 'data-ui-version="109"' in html and 'href="downloads/STEM_database_json.zip"' in html and 'STEM_camp_asia_europe_audit_v109.json' in html
for f in ROOT.joinpath('dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['data.js','camp-planning.js','camp-programmes.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['camp-planning.js','camp-programmes.js','camp-programmes.css']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=109,old_event_ids_preserved=3348,corrected_event_ids=['L183'],old_dossiers_preserved=778,updated_dossiers=UPDATED,new_dossiers=20,total_dossiers=798,complete_sqlite=True,complete_json=True,family_ics=2593,exhibition_ics=104,goal='active',new_visual_pdf_checks=0)
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
