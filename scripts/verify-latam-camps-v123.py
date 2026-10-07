"""Independent source clauses, eligibility gates, calendar semantics and full preservation."""
import collections,csv,hashlib,io,json,re,sqlite3,subprocess,zipfile
from camp_latam_v123 import ROOT,BASE,NEW
P=ROOT.parent/'stem-family-atlas-work/camp-latam-primary-v123'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clause(key,*values):
 t=re.sub(r'\s+','',(P/(key+'.txt')).read_text())
 for v in values:assert re.sub(r'\s+','',v) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={q['slug']:q for q in b['camp_programmes']['profiles']};z={q['slug']:q for q in d['camp_programmes']['profiles']}
assert len(a)==932 and len(z)==950 and z.keys()-a.keys()==set(NEW) and all(z[k]==v for k,v in a.items())
assert d['camp_programmes']['shortlist'][:224]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==227
assert d['camp_programmes']['gaps'][:257]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==265
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
expected={}
for slug in NEW:
 p=z[slug]
 for start,end in p['timing']['sessions']:expected[p['id']+'-'+start.replace('-','')+'-'+end.replace('-','')]=(start,end,slug)
assert len(expected)==1 and len(now)==3658 and now.keys()-old.keys()==expected.keys() and all(now[k]==v for k,v in old.items())
assert collections.Counter(q['block'] for q in now.values())=={'Соревнования':1153,'События':189,'Лагеря':2316}
for key,(start,end,slug) in expected.items():
 e=now[key];assert (e['start'],e['end'],e['camp_dossier_slug'])==('2027-01-04','2027-01-10','manque-chile-2027')
 assert e['admission_kind']=='organization_route' and e['participation']=='unconfirmed_program' and 'IFM-SEI' in e['entry']
 assert e['languages']==[] and e['language_mode']=='unconfirmed' and e['level']=='D — обучение'
 assert 'индивидуальная' in e['entry'] and 'не установлена' in e['entry']
for slug in NEW:
 p=z[slug];assert p['checked']=='2026-10-06' and all(s['checked']=='2026-10-06' for s in p['sources'])
 assert p['timing']['sessions']==([] if slug!='manque-chile-2027' else [['2027-01-04','2027-01-10']])
 assert p['confirmed_instruction_languages']==(['ES'] if slug.startswith('expanish-cr-') else [])
assert z['logiscool-mx-wedo']['formats']==['day'] and z['logiscool-mx-wedo']['age']=='6–9' and 'ДО' in z['logiscool-mx-wedo']['family_fit']['matvey']['detail']
assert all('после 7' in z[k]['family_fit']['oscar']['detail'].lower() for k in ['logiscool-mx-minecraft-design','logiscool-mx-mars','logiscool-mx-heroes'])
assert z['logiscool-mx-ai-creator']['age']=='10+' and z['logiscool-mx-3d']['family_fit']['matvey']['status']=='later'
assert all(z[k]['family_fit']['oscar']['status']=='later' for k in NEW[4:17])
assert all(v['status']=='unknown' for v in z['manque-chile-2027']['family_fit'].values())
assert z['manque-chile-2027']['formats']==['unknown'] and z['pll-colibria-ai']['family_fit']['matvey']['status']=='later'
assert '4°' in z['ucr-cimm-matenciar']['age'] and 'класс' in z['ucr-cimm-matenciar']['family_fit']['matvey']['detail']
assert z['puente-digital-cordoba']['price']['year']==2026 and z['utn-iac-scratch']['price']['year']==2025
assert z['vonbraun-junior-essential']['price']['year'] is None and '1 или 2 дня' in z['vonbraun-junior-essential']['programme']
assert '650' in z['inictel-peru-summer']['price']['label'] and 'пакет' in z['inictel-peru-summer']['price']['label']
for k in ['expanish-cr-boarding','expanish-cr-day']:
 assert z[k]['language_evidence_role']=='language_lessons' and z[k]['timing']['status']=='partial_2027'
 if k.endswith('boarding'):assert 'приостанов' in z[k]['programme']
assert 'Madrid' in z['expanish-cr-day']['programme'] and '15/20' in z['expanish-cr-day']['programme']
assert d['camp_planning']==b['camp_planning'] and len(d['camp_planning']['offers'])==43
osrc={q['url']:q for q in b['sources']};nsrc={q['url']:q for q in d['sources']};assert all(nsrc[k]==v for k,v in osrc.items())
clause('logiscool-mx-wedo','para 6-9 años','El campamento solo está disponible en nuestras ubicaciones presenciales')
for key in ['logiscool-mx-minecraft-design','logiscool-mx-mars','logiscool-mx-heroes']:clause(key,'para 7-14','Android/XBOX/PS4 NO','PC / Mac')
clause('logiscool-mx-multiverse','para 9-12','Roblox Studio','entorno de campamento cerrado sin ninguna publicación pública')
clause('logiscool-mx-ai-creator','para 10+','Duración: 5 días','controles parentales','Máx.: 12 (en línea: 8)')
clause('logiscool-mx-generative','para 9-12','Duración: 5 días')
clause('logiscool-mx-illustration','para 8-10','Máx.: 12 (en línea: 6)')
clause('logiscool-mx-3d','para 12-15','Tinkercad','Duración: 5 días')
clause('logiscool-interlomas-camps','No open Camps','1,500.00 pesos MX','31 de diciembre de 2023','$800.00')
clause('logiscool-contract','no será superior al 30%','ocho días antes','11%','22%','caso certificado')
clause('puente-main','13 julio al 7 agosto 2026','8 a 15','1,499','3,990','999','80 horas','traer su propio refrigerio','Bella Vista','Plaza San José')
clause('utn-scratch','27-02-2025','seis lecciones presenciales','12 estudiantes','escuelas públicas','Para 2025')
clause('ucr-matenciar','9 y 12','4°, 5° o 6°','5 000 colones','Aula 15')
clause('pll-ai','7, 8, 10, 14 y 17 de julio','12 a 15','9:00 a.m. a 12:00','No requiere inscripción previa')
clause('expanish-cr','temporalmente suspendido','se reanudará en 2027','12 a 17','15 clases semanales','20 clases/semana','tutor en Madrid','íntegramente en español','Hotel Faro Arenal')
clause('peru-vonbraun-junior','08 a 11','1 o 2 DÍAS A LA SEMANA','SPIKE ESSENTIAL')
r=json.loads((ROOT/'data/latam-camps-source-receipts-v123.json').read_text());assert len(r['sources'])==29 and sum(q.get('status')==200 for q in r['sources'])==23 and not any(r['external_actions'].values())
for q in r['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
for q in r['private_reader_files']:
 raw=(P/q['filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert b'04 al 10 de enero de 2027' in (P/'primary-reader-1.txt').read_bytes()
assert '650.00' in (P/'v123reader5.json').read_text() and '12 horas' in (P/'v123reader4.json').read_text()
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
 assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as q:
  assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry'])
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
 return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json');assert json.loads(js)==d
f=P/'verified-v123.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v122.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
changes={}
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
 aa=set(o.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'));removed={r[0] for r in aa-zz}
 allowed={'metadata':{'camp_focus','completeness_audit'},'countries':{'CHL'}}.get(name,set())
 assert removed<=allowed,(name,removed);assert {r[0] for r in aa}<={r[0] for r in zz},name
 if removed:changes[name]=sorted(removed)
assert c.execute('SELECT count(*) FROM events').fetchone()[0]==3658 and c.execute('SELECT count(*) FROM camp_programmes').fetchone()[0]==950
c.close();o.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for s in t.split('BEGIN:VEVENT')[1:]:
  f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None)
  assert f['UID'] not in out;out[f['UID']]=f
 return out
for name,count in [('STEM_подтвержденные_даты.ics',2873),('STEM_крупные_выставки.ics',104)]:
 aa=calendar(prior('dist/downloads/'+name));zz=calendar((ROOT/'dist/downloads'/name).read_bytes())
 assert len(zz)==count and all(zz[k]==v for k,v in aa.items()) and len(zz)-len(aa)==(1 if count==2873 else 0)
 assert all(any(e in uid for e in expected) for uid in zz.keys()-aa.keys())
for name in ['STEM_catalog.csv','STEM_country_coverage.csv']:
 def rows(raw):return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
 aa=rows(prior('dist/downloads/'+name));zz=rows((ROOT/'dist/downloads'/name).read_bytes());key='id' if name=='STEM_catalog.csv' else 'iso'
 x={q[key]:q for q in aa};y={q[key]:q for q in zz};assert all(y[k]==v for k,v in x.items() if key=='id' or k!='CHL')
 assert y.keys()-x.keys()==(expected.keys() if key=='id' else set())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for key in ['events','camp_programmes','camp_planning','league_guide','family_strategy']:assert web[key]==d[key]
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']=='active' and plan['native_goal_status']=='active' and plan['next_research']==json.loads(prior('data/research-plan.json'))['next_research']
assert plan['latest_validation']['fully_audited_countries']==0 and plan['latest_validation']['worldwide_complete'] is False
for stem in ['research-plan','latam-camps-audit-v123','latam-camps-source-receipts-v123']:assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
assert 'data-ui-version="123"' in (ROOT/'dist/index.html').read_text()
for f in (ROOT/'dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['camp-planning.js','camp-programmes.js','data.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['nearby-participation.js','nearby-participation.css','experience.js','camp-planning.js']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=123,all_prior_events_preserved=3657,all_prior_dossiers_preserved=932,all_prior_budget_objects_preserved=43,new_dossiers=18,new_calendar_rows=1,complete_sqlite=True,complete_json=True,sqlite_allowed_updated_keys=changes,family_ical=2873,exhibition_ical=104,worldwide_scope_preserved=True,goal='active')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
