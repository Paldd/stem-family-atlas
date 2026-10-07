"""Independent primary facts, preservation, calendar and complete portable-export checks."""
import collections,csv,hashlib,io,json,sqlite3,subprocess,zipfile
from camp_northamerica_v114 import ROOT,BASE,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-northamerica-primary-v114'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clauses(key,*values):
 t=' '.join((P/(key+'.txt')).read_text().split())
 for v in values:assert ' '.join(v.split()) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'asof','events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={p['slug']:p for p in b['camp_programmes']['profiles']};z={p['slug']:p for p in d['camp_programmes']['profiles']}
assert len(a)==846 and len(z)==861 and set(z)-set(a)==set(NEW)
assert [s for s in a if z[s]!=a[s]]==UPDATED and len({p['id'] for p in z.values()})==861
assert d['camp_programmes']['shortlist'][:200]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==203
assert d['camp_programmes']['gaps'][:213]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==220
e={q['id']:q for q in b['events']};v={q['id']:q for q in d['events']}
updated=set()
assert len(e)==3433 and e.keys()<=v.keys() and {k for k in e if e[k]!=v[k]}==updated and len(v)-len(e)==57
assert collections.Counter(q['block'] for q in v.values())=={'Соревнования':1153,'События':189,'Лагеря':2148}
oldsrc={s['url']:s for s in b['sources']};newsrc={s['url']:s for s in d['sources']};assert all(newsrc[u]==s for u,s in oldsrc.items())
assert d['camp_planning']['offers']==b['camp_planning']['offers'] and len(d['camp_planning']['offers'])==17
for slug in NEW:
 p=z[slug];assert p['checked']=='2026-10-06' and all(q['checked']=='2026-10-06' for q in p['sources'])
 assert p['confirmed_instruction_languages']==[],slug
 assert p['id'] not in {q['id'] for q in a.values()}
 assert len(p['timing']['sessions'])==len(p['calendar_links'])
assert sum(len(z[slug]['timing']['sessions']) for slug in NEW)==57
assert len(z['onondaga-general']['timing']['sessions'])==6
assert not any('B2' in q['label'] for q in z['onondaga-general']['timing']['session_details'])
for slug in ['ncc-morning','coder-eastcobb-robocode']:assert z[slug]['timing']['sessions']==[] and z[slug]['calendar_links']==[]
assert z['hurontario-intro']['family_fit']['matvey']['status']=='not_eligible'
assert z['ncc-main']['family_fit']['oscar']['status']=='later'
assert z['ncc-morning']['family_fit']['matvey']['status']=='not_eligible'
assert z['mondamin-fatherson']['formats']==['family','boarding']
for slug in NEW[10:14]:
 for q in z[slug]['timing']['session_details']:
  if q['start']<'2027':assert q['family_fit']['oscar']['status']=='later'
  else:assert q['family_fit']['oscar']['status']=='conditional'
assert all(q['family_fit']['matvey']['status']==q['family_fit']['oscar']['status']=='later' for q in z['mondamin-regular']['timing']['session_details'] if 'MiniII' in q['label'])
reader=json.loads((P/'public-reader-onondaga-dates.json').read_text())
for phrase in ['2027 Session','Jincis (born in 2017-2021)','August 14 – August 27','August 8 – August 21','$5,665','$5,395','after February 15, 2027']:assert phrase in reader,phrase
clauses('hurontario-dates','Registration for Summer 2027 is OPEN','5-8 yrs','Sunday, July 11 – Saturday, July 17, 2027','Sunday, August 8 – Saturday, August 14, 2027','$1,990 +HST','$3,650 +HST')
for key in ['hurontario-two-2026','hurontario-intro-2026']:clauses(key,'Fees are set in Canadian dollars.','$70 +HST each way','registration fee of $300')
clauses('hurontario-faq','registration fee is non-refundable','partial refund will be made up to June 1st')
clauses('mondamin-dates','2027 Sessions','5th - 8th grade (before camp)','For ages 11-14','For ages 7-11','Boys may attend for one year only','$6,300.00')
clauses('mondamin-fatherson','May 21-23, 2027','August 13-15, 2027','only one guardian','only bring boys','$900 per father–son pair','$300 for each additional son','including moms')
clauses('ncc-dates','2027 Tuition','$1,450.00','$1,195.00','$400.00','July 11-July 16','June 13-June 18')
clauses('ncc-morning','only to 6 to 8 year olds','$350.00 per week minus $50','ratio is only 3:1')
clauses('ncc-curriculum','take home the Arduino kit',"program a simulated 'robot' icon on the screen",'All other languages are offered weekly to campers ages 9-18.')
clauses('ncc-registration','60 days after the transaction','within ten days of start of camp','No refunds for late arrival or early withdrawal')
clauses('coder-pasadena','11/23/2026','12/21-12/24/2026','+$145 for robot','Block Coding for 7-10','Python for 10+','21 days','7 days','May 31, 2026')
clauses('coder-eastcobb','Ages 6-9','Holiday Camp Sale Ends October 1st!','mBot')
assert '2026' not in (P/'coder-eastcobb.txt').read_text()
clauses('lohikan-main','summer of 2026 our final season of camp operations','expected to be finalized in 2027','Camp Morasha')
assert (P/'lohikan-main.html').read_bytes()==(P/'lohikan-dates.html').read_bytes()==(P/'lohikan-international.html').read_bytes()
mini=json.loads((P/'public-reader-snapshot.json').read_text())
for phrase in ['AGES 5-15 • $1350 + HST','AGES 5-9 • $875 (HST Exempt)','July 11-17','August 22-28','Bible teaching','$350 cancellation fee']:assert phrase in mini,phrase
receipt=json.loads((ROOT/'data/northamerica-camps-source-receipts-v114.json').read_text())
assert len(receipt['sources'])==36 and sum(q.get('status')==200 for q in receipt['sources'])==26 and not any(receipt['external_actions'].values())
assert len(receipt['reader_snapshots'])==3
for q in receipt['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
for q in receipt['reader_snapshots']:
 raw=(P/q['private_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert sum(q.get('raw_filename','').endswith('.pdf') for q in receipt['sources'])==3
vr=receipt['visual_review'];assert vr['new_visual_pdf_checks']==6 and vr['pdf_pages_text_extracted']==24
for key,pages in vr['rendered_pages'].items():
 for page in pages:assert (P/f'{key}-p{page}.png').stat().st_size>0
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
 assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as q:
  assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry']);assert m[ext+'_sha256'] in q.read('README.txt').decode()
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
 return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json');assert json.loads(js)==d
f=P/'verified-v114.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v113.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
allowed={'countries':{'USA','CAN'},'metadata':{'completeness_audit','camp_focus','camp_planning'},'events':updated,'camp_programmes':set()}
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
assert oa.keys()<=na.keys() and len(na)==2707 and len(na.keys()-oa.keys())==56
assert {k for k in oa if oa[k]!=na[k]}=={'stem-'+k+'@family-stem.local' for k in updated}
for k in oa:
 if oa[k]!=na[k]:assert {f for f in oa[k] if oa[k][f]!=na[k][f]}=={'DESCRIPTION'}
assert all(any(z[slug]['id'] in uid for slug in NEW) for uid in na.keys()-oa.keys())
name='dist/downloads/STEM_крупные_выставки.ics';assert calendar(prior(name))==calendar((ROOT/name).read_bytes()) and len(calendar((ROOT/name).read_bytes()))==104
for name in ['STEM_catalog.csv','STEM_календарь_2026_2027.csv','STEM_крупные_выставки.csv']:
 f=ROOT/'dist/downloads'/name
 if f.exists():
  oldrows=list(csv.DictReader(io.StringIO(prior('dist/downloads/'+name).decode('utf-8-sig'))));newrows=list(csv.DictReader(io.StringIO(f.read_text(encoding='utf-8-sig'))))
  missing=[r for r in oldrows if r not in newrows]
  assert all(any(ident in r.values() for ident in updated) for r in missing),name
plan=json.loads((ROOT/'data/research-plan.json').read_text());oldplan=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==114
assert {q['id'] for q in plan['requirements']}=={q['id'] for q in oldplan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==oldplan[k],k
assert plan['complete_database_download']==sm and plan['complete_json_download']==jm
assert d['coverage_summary']['fully_audited_countries']==0 and not plan['latest_validation']['worldwide_complete']
for stem in ['research-plan','northamerica-camps-audit-v114','northamerica-camps-source-receipts-v114']:
 assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for k in ['events','camp_programmes','camp_planning','league_guide']:assert web[k]==d[k]
html=(ROOT/'dist/index.html').read_text();assert 'data-ui-version="114"' in html and 'STEM_northamerica_camps_audit_v114.json' in html
for f in ROOT.joinpath('dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['data.js','camp-planning.js','camp-programmes.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['camp-planning.js','camp-programmes.css']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=114,old_event_ids_preserved=3433,old_event_objects_unchanged=3433,updated_event_ids=[],new_event_ids=sorted(v.keys()-e.keys()),old_dossier_ids_preserved=846,old_dossier_objects_unchanged=846,new_dossiers=15,total_dossiers=861,complete_sqlite=True,complete_json=True,all17family_budget_offers_unchanged=True,family_ics=2707,exhibition_ics=104,goal='active',new_visual_pdf_checks=6)
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
