"""Independent primary facts, preservation, calendar and complete portable-export checks."""
import collections,csv,hashlib,io,json,sqlite3,subprocess,zipfile
from camp_latam_v113 import ROOT,BASE,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-latam-primary-v113'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clauses(key,*values):
 t=' '.join((P/(key+'.txt')).read_text().split())
 for v in values:assert ' '.join(v.split()) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'asof','events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={p['slug']:p for p in b['camp_programmes']['profiles']};z={p['slug']:p for p in d['camp_programmes']['profiles']}
assert len(a)==839 and len(z)==846 and set(z)-set(a)==set(NEW)
assert [s for s in a if z[s]!=a[s]]==UPDATED and len({p['id'] for p in z.values()})==846
assert d['camp_programmes']['shortlist'][:197]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==200
assert d['camp_programmes']['gaps'][:208]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==213
e={q['id']:q for q in b['events']};v={q['id']:q for q in d['events']}
updated=set()
assert len(e)==3421 and e.keys()<=v.keys() and {k for k in e if e[k]!=v[k]}==updated and len(v)-len(e)==12
assert collections.Counter(q['block'] for q in v.values())=={'Соревнования':1153,'События':189,'Лагеря':2091}
oldsrc={s['url']:s for s in b['sources']};newsrc={s['url']:s for s in d['sources']};assert all(newsrc[u]==s for u,s in oldsrc.items())
assert d['camp_planning']['offers']==b['camp_planning']['offers'] and len(d['camp_planning']['offers'])==17
for slug in NEW:
 p=z[slug];assert p['checked']=='2026-10-06' and all(q['checked']=='2026-10-06' for q in p['sources'])
 assert p['confirmed_instruction_languages']==[],slug
 assert p['id'] not in {q['id'] for q in a.values()}
 if slug.startswith('talenttec'):
  assert not p['timing']['sessions'] and not p['calendar_links'] and p['price']['year']==2026
  assert p['timing']['status']=='archive_next_unannounced' and p['iso']=='CRI'
 else:
  assert p['timing']['status']=='published_2027' and p['formats']==['boarding'] and p['price']['year']==2027
  assert len(p['timing']['sessions'])==len(p['calendar_links'])
  assert 'код валюты не напечатан' in p['price']['label']
  assert '21:30' in p['programme'] and '3/7/11' in p['programme']
assert z['kajuyali-kuita']['age']=='7–17' and z['kajuyali-kuita']['family_fit']['oscar']['status']=='conditional'
assert z['kajuyali-kiribati']['family_fit']['matvey']['status']=='conditional' and z['kajuyali-kiribati']['family_fit']['oscar']['status']=='later'
for slug in ['kajuyali-aluna','kajuyali-yubarka']:assert all(f['status']=='later' for f in z[slug]['family_fit'].values())
assert z['kajuyali-yakaro']['iso']=='PAN' and z['kajuyali-yakaro']['family_fit']['matvey']['status']=='unknown'
assert '11–17' in z['kajuyali-yakaro']['age'] and '9–17' in z['kajuyali-yakaro']['age']
assert z['talenttec-3d']['family_fit']['oscar']['status']=='later'
assert len(z['programable']['timing']['session_details'])==6 and z['programable']['related_event_ids']==a['programable']['related_event_ids']
assert sum(len(z[slug]['timing']['sessions']) for slug in NEW)==12
clauses('kuita','7 - 17 años','Camps 2027','Del 30 junio a 12 julio','Del 14 julio a 26 julio','Del 28 julio a 9 agosto')
clauses('kiribati','9 - 17 años','siembra de corales','Del 26 junio a 8 julio','Del 10 julio a 22 julio')
clauses('aluna','11 - 17 años','Del 27 junio a 9 julio','Del 11 julio a 23 julio')
clauses('yubarka','11 - 17 años','Panamá','Del 29 junio a 11 julio','Del 13 julio a 25 julio','Del 27 julio a 8 agosto')
clauses('yakaro','11 - 17 años','Del 28 junio a 10 julio','Del 12 julio a 24 julio')
for key in ['kuita','aluna','yubarka','kiribati','yakaro']:
 clauses(key+'-brochure','Fechas y precios 2027','$10.552.300','$11.752.300','$13.496.000','$13.484.000','$16.320.000')
clauses('yakaro-brochure','Actividad no incluida','CERTIFICACIÓN EN BUCEO','PARA BUZOS CERTIFICADOS')
clauses('talenttec-holiday','Julio 2026','Del 07 al 10 de julio','4 a 5 años','6 a 8 años','9 a 12 años','₡14,000','₡16,000','máximo 12 espacios.')
clauses('programable','verano 2027','Júnior 6 a 9 años','Sénior 10 a 13 años','dos experiencias complementarias de 80 minutos','$95.000','MLX90614 por I2C','Bronce a Platino')
receipt=json.loads((ROOT/'data/latam-camps-source-receipts-v113.json').read_text())
assert len(receipt['sources'])==19 and sum(q.get('status')==200 for q in receipt['sources'])==18 and not any(receipt['external_actions'].values())
for q in receipt['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert sum(q.get('raw_filename','').endswith('.pdf') for q in receipt['sources'])==5
assert next(q for q in receipt['sources'] if q['key']=='robotiki-camp')['content_status']=='retrieval_error_no_body'
assert next(q for q in receipt['sources'] if q['key']=='kaju-registration')['content_status']=='registration_shell_not_price_or_admission'
vr=receipt['visual_review'];assert vr['new_visual_pdf_checks']==39
for name,q in vr['documents'].items():
 assert hashlib.sha256((P/(name+'.pdf')).read_bytes()).hexdigest()==q['pdf_sha256']
 for page,sha in q['rendered_page_sha256'].items():assert hashlib.sha256((P/f'{name.removesuffix("-brochure")}-p{page}.png').read_bytes()).hexdigest()==sha
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
 assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as q:
  assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry']);assert m[ext+'_sha256'] in q.read('README.txt').decode()
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
 return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json');assert json.loads(js)==d
f=P/'verified-v113.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v112.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
allowed={'countries':{'COL','PAN'},'metadata':{'completeness_audit','camp_focus','camp_planning'},'events':updated,'camp_programmes':{'CP046'}}
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
 aa=set(o.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'))
 assert {r[0] for r in aa-zz}==allowed.get(name,set()),name
 assert {r[0] for r in aa}<= {r[0] for r in zz},name
assert {q['id']:q for q in d['events']}=={k:json.loads(value) for k,value in c.execute('SELECT id,record_json FROM events')}
assert {q['slug']:q for q in d['camp_programmes']['profiles']}=={k:json.loads(value) for k,value in c.execute('SELECT slug,record_json FROM camp_programmes')}
assert json.loads(c.execute("SELECT value FROM metadata WHERE key='camp_planning'").fetchone()[0])==d['camp_planning'];c.close();o.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for s in t.split('BEGIN:VEVENT')[1:]:
  f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None);assert f['UID'] not in out;out[f['UID']]=f
 return out
name='dist/downloads/STEM_подтвержденные_даты.ics';oa=calendar(prior(name));na=calendar((ROOT/name).read_bytes())
assert oa.keys()<=na.keys() and len(na)==2651 and len(na.keys()-oa.keys())==7
assert {k for k in oa if oa[k]!=na[k]}=={'stem-'+k+'@family-stem.local' for k in updated}
for k in oa:
 if oa[k]!=na[k]:assert {f for f in oa[k] if oa[k][f]!=na[k][f]}=={'DESCRIPTION'}
assert all(any(z[slug]['id'] in uid for slug in ['kajuyali-kuita','kajuyali-kiribati','kajuyali-yakaro']) for uid in na.keys()-oa.keys())
name='dist/downloads/STEM_крупные_выставки.ics';assert calendar(prior(name))==calendar((ROOT/name).read_bytes()) and len(calendar((ROOT/name).read_bytes()))==104
for name in ['STEM_catalog.csv','STEM_календарь_2026_2027.csv','STEM_крупные_выставки.csv']:
 f=ROOT/'dist/downloads'/name
 if f.exists():
  oldrows=list(csv.DictReader(io.StringIO(prior('dist/downloads/'+name).decode('utf-8-sig'))));newrows=list(csv.DictReader(io.StringIO(f.read_text(encoding='utf-8-sig'))))
  missing=[r for r in oldrows if r not in newrows]
  assert all(any(ident in r.values() for ident in updated) for r in missing),name
plan=json.loads((ROOT/'data/research-plan.json').read_text());oldplan=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==113
assert {q['id'] for q in plan['requirements']}=={q['id'] for q in oldplan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==oldplan[k],k
assert plan['complete_database_download']==sm and plan['complete_json_download']==jm
assert d['coverage_summary']['fully_audited_countries']==0 and not plan['latest_validation']['worldwide_complete']
for stem in ['research-plan','latam-camps-audit-v113','latam-camps-source-receipts-v113']:
 assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for k in ['events','camp_programmes','camp_planning','league_guide']:assert web[k]==d[k]
html=(ROOT/'dist/index.html').read_text();assert 'data-ui-version="113"' in html and 'STEM_latam_camps_audit_v113.json' in html
for f in ROOT.joinpath('dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['data.js','camp-planning.js','camp-programmes.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['camp-planning.js','camp-programmes.css']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=113,old_event_ids_preserved=3421,old_event_objects_unchanged=3421,updated_event_ids=[],new_event_ids=sorted(v.keys()-e.keys()),old_dossier_ids_preserved=839,old_dossier_objects_unchanged=838,new_dossiers=7,total_dossiers=846,complete_sqlite=True,complete_json=True,all17family_budget_offers_unchanged=True,family_ics=2651,exhibition_ics=104,goal='active',new_visual_pdf_checks=39)
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
