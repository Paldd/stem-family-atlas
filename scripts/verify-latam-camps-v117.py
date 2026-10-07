"""Source clause and full-object preservation checks for the selected LatinAmerican pass."""
import collections,csv,hashlib,io,json,re,sqlite3,subprocess,zipfile
from camp_latam_v117 import ROOT,BASE,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-latam-primary-v117'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clauses(key,*values,compact=False):
 raw=(P/(key+'.txt')).read_text();norm=(lambda t:re.sub(r'\s+','',t)) if compact else (lambda t:' '.join(t.split()))
 for v in values:assert norm(v) in norm(raw),(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'asof','events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={p['slug']:p for p in b['camp_programmes']['profiles']};z={p['slug']:p for p in d['camp_programmes']['profiles']}
assert len(a)==883 and len(z)==890 and set(z)-set(a)==set(NEW)
assert [s for s in a if z[s]!=a[s]]==UPDATED and len({p['id'] for p in z.values()})==890
assert d['camp_programmes']['shortlist'][:211]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==215
assert d['camp_programmes']['gaps'][:233]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==240
e={q['id']:q for q in b['events']};v={q['id']:q for q in d['events']}
assert len(e)==3553 and e.keys()<=v.keys() and all(e[k]==v[k] for k in e) and len(v)-len(e)==2
assert collections.Counter(q['block'] for q in v.values())=={'Соревнования':1153,'События':189,'Лагеря':2213}
oldsrc={s['url']:s for s in b['sources']};newsrc={s['url']:s for s in d['sources']}
assert all(newsrc[u]==s for u,s in oldsrc.items())
assert d['camp_planning']['offers']==b['camp_planning']['offers'] and len(d['camp_planning']['offers'])==27
for slug in NEW:
 p=z[slug];assert p['checked']=='2026-10-06' and all(s['checked']=='2026-10-06' for s in p['sources'])
 assert p['confirmed_instruction_languages']==(['EN'] if slug==NEW[6] else []),slug
 assert len(p['timing']['sessions'])==len(p['calendar_links'])
assert all(not z[s]['timing']['sessions'] for s in NEW[:6])
assert z[NEW[6]]['timing']['sessions']==[['2027-08-23','2027-08-25'],['2027-08-25','2027-08-27']]
assert z[NEW[6]]['formats']==['unknown'] and z[NEW[6]]['language_evidence_role']=='camp_life'
assert z[NEW[6]]['family_fit']['matvey']['status']=='conditional' and z[NEW[6]]['family_fit']['oscar']['status']=='later'
assert all(z[NEW[3]]['family_fit'][x]['status']=='later' for x in ['matvey','oscar'])
assert z[NEW[4]]['family_fit']['oscar']['status']=='later' and z[NEW[0]]['price']['year'] is None
clauses('met-corotu','We welcome non-MET students as well!','LEGO® WeDo 2.0','LEGO® Mindstorms® Educational','Cost per week is $250 for MET students and $275 for non-MET students.','additional $50 per week per student','Morning snack and lunch')
clauses('met-corotu-es','Información de costos y transporte estarán disponibles pronto.')
clauses('camohmila-programmes','Por cada 10 acampantes','Campamentos familiares','periodo vacacional de diciembre.','Club Deportivo YMCA-Campamento-Club Deportivo YMCA','Servicio médico y seguro contra accidentes')
clauses('camohmila-services','Capacidad de 2 a 5 personas.','Literas (8 a 22 personas)','Sin pasar la noche en Camohmila.')
clauses('camohmila-rules','23:00','15:00','13:00','Excepto perros guía.')
clauses('mustakis-cyt','Estudiantes de 12 a 17 años','Taller Robótica Educativa Intensivo')
clauses('mustakis-faq','séptimo básico y tercer año','100% gratuita para los seleccionados','computador, celular, robots','pierdes tu cupo',compact=True)
clauses('mustakis-rm','INSCRIPCIONES CERRADAS','Jóvenes de 12 a 17 años')
clauses('itstep-camp','7 a 16 años','8-15 años','$2,350 pesos por semana','$2,200.00 pesos por semana','Las comidas están disponibles pero no están incluidas en el precio.','Blender')
clauses('rukamalon','6 a 12 años','1,5 horas','Devolución 100% hasta 7 días','Devolución 50% en los últimos 7 días','Dibujo digital requiere tablet / celular')
clauses('gapper-home','AGOSTO','2027','23/8 a las 10 hs','25/8 a las 14 hs','25/8 a las 18 hs','27/8 a las 15 hs')
clauses('gapper-proposal','3 días de inmersión total en inglés','9 a 12 años','Intituciones','o individuales','VILLA CARLOS PAZ')
receipt=json.loads((ROOT/'data/latam-camps-source-receipts-v117.json').read_text())
assert len(receipt['sources'])==39 and sum(q.get('status')==200 for q in receipt['sources'])==29
assert not any(receipt['external_actions'].values())
for q in receipt['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert sum(q.get('raw_filename','').endswith('.pdf') for q in receipt['sources'])==3
vr=receipt['visual_review'];assert vr['new_visual_pdf_checks']==6 and vr['pdf_pages_text_extracted']==17
for key,pages in vr['rendered_pages'].items():
 for page in pages:assert (P/(f'{key}.png' if key=='camohmila-rules' else f'{key}-{page}.png')).stat().st_size>0
for q in vr['images']:
 raw=(P/(q['key']+'.png')).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
def portable(name,ext):
    m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
    assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
    with zipfile.ZipFile(io.BytesIO(raw)) as q:
        assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt']
        body=q.read(m[ext+'_entry']);assert m[ext+'_sha256'] in q.read('README.txt').decode()
    assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
    assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
    return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json')
assert json.loads(js)==d
f=P/'verified-v117.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v116.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"))
assert schema(c)==schema(o)
allowed={'countries':{'ARG'},'metadata':{'completeness_audit','camp_focus','camp_planning'}}
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
    aa=set(o.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'))
    assert {r[0] for r in aa-zz}==allowed.get(name,set()),name
    assert {r[0] for r in aa}<={r[0] for r in zz},name
assert {q['id']:q for q in d['events']}=={k:json.loads(value) for k,value in c.execute('SELECT id,record_json FROM events')}
assert {q['slug']:q for q in d['camp_programmes']['profiles']}=={k:json.loads(value) for k,value in c.execute('SELECT slug,record_json FROM camp_programmes')}
assert json.loads(c.execute("SELECT value FROM metadata WHERE key='camp_planning'").fetchone()[0])==d['camp_planning']
c.close();o.close()
def calendar(raw):
    t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
    for s in t.split('BEGIN:VEVENT')[1:]:
        f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v}
        f.pop('DTSTAMP',None);assert f['UID'] not in out;out[f['UID']]=f
    return out
name='dist/downloads/STEM_подтвержденные_даты.ics';oa=calendar(prior(name));na=calendar((ROOT/name).read_bytes())
assert len(oa)==2768 and oa.keys()<=na.keys() and len(na)==2770 and all(oa[k]==na[k] for k in oa)
newuids=na.keys()-oa.keys();assert len(newuids)==2
assert all(any(z[s]['id'] in uid for s in [NEW[6]]) for uid in newuids)
assert not any(z[s]['id'] in uid for s in [NEW[3]] for uid in na)
name='dist/downloads/STEM_крупные_выставки.ics'
assert calendar(prior(name))==calendar((ROOT/name).read_bytes()) and len(calendar((ROOT/name).read_bytes()))==104
for name in ['STEM_catalog.csv','STEM_календарь_2026_2027.csv','STEM_крупные_выставки.csv']:
    f=ROOT/'dist/downloads'/name
    if f.exists():
        oldrows=list(csv.DictReader(io.StringIO(prior('dist/downloads/'+name).decode('utf-8-sig'))))
        newrows=list(csv.DictReader(io.StringIO(f.read_text(encoding='utf-8-sig'))))
        assert all(r in newrows for r in oldrows),name
plan=json.loads((ROOT/'data/research-plan.json').read_text());oldplan=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==117
assert {q['id'] for q in plan['requirements']}=={q['id'] for q in oldplan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==oldplan[k],k
assert plan['complete_database_download']==sm and plan['complete_json_download']==jm
assert d['coverage_summary']['fully_audited_countries']==0 and not plan['latest_validation']['worldwide_complete']
for stem in ['research-plan','latam-camps-audit-v117','latam-camps-source-receipts-v117']:
    assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for k in ['events','camp_programmes','camp_planning','league_guide']:assert web[k]==d[k]
assert 'data-ui-version="117"' in (ROOT/'dist/index.html').read_text()
for f in ROOT.joinpath('dist').rglob('*'):
    if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['data.js','camp-planning.js','camp-programmes.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['camp-planning.js','camp-programmes.css']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=117,old_event_objects_unchanged=3553,new_calendar_records=2,old_dossier_objects_unchanged=883,new_dossiers=7,total_dossiers=890,complete_sqlite=True,complete_json=True,old27budget_offers_unchanged=True,family_ics=2770,exhibition_ics=104,no_unknown_currency_invoice_created=True,unknown_lodging_retained=True,new_visual_pdf_checks=6,goal='active')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
