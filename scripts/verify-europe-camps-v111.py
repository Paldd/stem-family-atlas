"""Independent primary-clause, old-object and complete-export verification."""
import collections,csv,hashlib,io,json,sqlite3,subprocess,zipfile
from camp_europe_v111 import ROOT,BASE,NEW,YOUNG,TEEN,DAYS
P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v111'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clauses(key,*values):
 t=' '.join((P/(key+'.txt')).read_text().split())
 for v in values:assert ' '.join(v.split()) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
changed={'asof','events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in changed}=={k:v for k,v in b.items() if k not in changed}
a={p['slug']:p for p in b['camp_programmes']['profiles']};z={p['slug']:p for p in d['camp_programmes']['profiles']}
assert len(a)==815 and len(z)==827 and set(z)-set(a)==set(NEW)
assert all(z[s]==p for s,p in a.items()) and len({p['id'] for p in z.values()})==827
assert d['camp_programmes']['shortlist'][:189]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==193
assert d['camp_programmes']['gaps'][:197]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==203
e={q['id']:q for q in b['events']};v={q['id']:q for q in d['events']}
assert len(e)==3376 and e.keys()<=v.keys() and all(v[i]==q for i,q in e.items()) and len(v)-len(e)==43
assert collections.Counter(q['block'] for q in v.values())=={'Соревнования':1153,'События':189,'Лагеря':2077}
oldsrc={q['url']:q for q in b['sources']};newsrc={q['url']:q for q in d['sources']};assert all(newsrc[u]==q for u,q in oldsrc.items())
assert d['camp_planning']['offers'][:14]==b['camp_planning']['offers'] and len(d['camp_planning']['offers'])==17
offers={q['id']:q for q in d['camp_planning']['offers']}
for ident,amount,count in [('helen-paris-half',320,8),('helen-paris-full',690,8),('techlab-single-day',60,4)]:
 o=offers[ident];assert o['base_by_child']=={'matvey':amount,'oscar':amount} and len(o['sessions'])==count
 assert not o['discount_second'] and o['unknown_required'][0]['id']=='programme_extras' and o['unknown_trip']==['travel','lodging','misc']
for s in NEW:
 p=z[s];assert p['checked']=='2026-10-06' and all(q['checked']=='2026-10-06' for q in p['sources'])
 assert p['confirmed_instruction_languages']==(['EN'] if s in ['helen-paris15-half','helen-paris15-full','helen-paris15-teens','eyyc-scotland-board'] else [])
 if p['confirmed_instruction_languages']:assert p['language_evidence_role']=='language_lessons'
for s in NEW[:3]:
 assert z[s]['formats']==['unknown']
 rows=[q for q in v.values() if q.get('camp_dossier_slug')==s];assert all(q['participation']=='unconfirmed_program' and q['date_scope']=='camp_session' for q in rows)
assert z['ps-grasse-robot']['timing']['sessions']==[['2026-10-19','2026-10-23']]
assert 'Thymio' in z['ps-grasse-robot']['programme'] and 'Scratch' in z['ps-grasse-robot']['programme']
assert z['ps-grasse-english-science']['family_fit']['oscar']['status']=='not_eligible'
for s in ['helen-paris15-half','helen-paris15-full']:assert z[s]['timing']['sessions']==YOUNG
assert z['helen-paris15-teens']['timing']['sessions']==TEEN and z['helen-paris15-teens']['family_fit']['matvey']['status']=='later'
assert not any(s[0].startswith('2027-06') for s in YOUNG) and len(TEEN)==10
assert z['techlabs-basel-lego']['timing']['sessions']==[['2026-10-05','2026-10-09']]
assert z['techlabs-basel-lego']['availability']['status']=='waitlist'
assert z['techlabs-basel-lego']['timing']['session_details'][0]['availability']['status']=='closed'
assert not z['techlabs-basel-controllers']['timing']['sessions'] and not z['techlabs-basel-controllers']['calendar_links']
p=z['techlabs-flight-board'];assert p['timing']['sessions']==[[f'2027-07-{s:02d}',f'2027-07-{e:02d}'] for s,e in [(3,9),(10,16),(17,23),(24,30)]]
assert p['available_staff_languages']==['EN','DE','FR'] and p['family_fit']['oscar']['status']=='later'
assert '210' in p['price']['label'] and 'субсидии' in p['price']['label'] and 'не установлена' in p['price']['label']
assert z['techlab-barcelona-days']['timing']['sessions']==DAYS
for s,iso in [('eyyc-scotland-board','GBR'),('eyyc-ireland-host','IRL')]:
 assert z[s]['iso']==iso and all(q['status']=='later' for q in z[s]['family_fit'].values())
assert '2299' in z['eyyc-scotland-board']['price']['label'] and '599' in z['eyyc-scotland-board']['price']['label']
assert 'не опубликованы' in z['eyyc-ireland-host']['price']['label']
clauses('planete-robot','8 ans et +','octobre 19 - octobre 23','€220','11 Rue Sans Peur')
clauses('planete-english-a','7 – 12ans','€190','octobre 19 - octobre 23')
clauses('planete-explor','11 – 13 ans','octobre 26 @ 8h00','octobre 30 @ 17h00','€250')
clauses('helen-paris15','100 % en anglais','GS (5 ans)','320€','690€','345€','11-18 ANS','Du 08 au 12 février 2027','Du 21 au 25 juin 2027','lunch box')
clauses('techlabs-lego','LEGO WeDO','Fully booked, entry in waiting list possible','Age 6-9 | Oct. 5-9','450.00 CHF – 924.00 CHF')
clauses('techlabs-flight-register','four different 6-night camp blocks during summer 2027','July 3-9, 2027','July 10–16, 2027','July 17-23, 2027','July 24-30, 2027','90% subsidy','210 CHF','does NOT include travel')
clauses('eyyc-scotland','12 a 17 años','29 de junio - 12 de julio','14 de julio - 27 de julio','2299€','599€')
clauses('eyyc-main','INSCRIPCIONES','2027 ABIERTAS','26 de junio - 24 de julio','30 de junio - 28 de julio')
reader=json.loads((P/'web-reader-fallback.json').read_text());rt=json.dumps(reader,ensure_ascii=False)
for value in ['7 diciembre 2026','8 febrero 2027','14 mayo 2027','18 mayo 2027','2025','6-14 años','60€','9h00-16h00','robot']:
 assert value in rt,value
receipt=json.loads((ROOT/'data/europe-camps-source-receipts-v111.json').read_text())
assert len(receipt['sources'])==32 and sum(q.get('status')==200 for q in receipt['sources'])==25 and not any(receipt['external_actions'].values())
assert len([q for q in receipt['sources'] if q.get('raw_filename','').endswith('.pdf')])==2
for q in receipt['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert next(q for q in receipt['sources'] if q['key']=='aal-courses')['content_status']=='html_shell_no_readable_programme_body'
q=receipt['primary_reader_fallback'];raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
for q in receipt['posters']:
 raw=(P/q['filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert len(receipt['posters'])==4 and len({q['sha256'] for q in receipt['posters']})==3
vr=receipt['visual_review'];assert vr['new_visual_pdf_checks']==16 and vr['new_visual_image_checks']==3
assert vr['techlabs_flight_faq']['reviewed_pages']==[1,2,3,4,5,6]
assert vr['eyyc_brochure']['reviewed_pages']==[1,2,3,4,6,7,10,12,13,14]
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
 assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as q:
  assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry']);assert m[ext+'_sha256'] in q.read('README.txt').decode()
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
 return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json');assert json.loads(js)==d
f=P/'verified-v111.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v110.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
 old=list(o.execute('SELECT * FROM "'+name+'"'));new=list(c.execute('SELECT * FROM "'+name+'"'));aa=set(old);zz=set(new)
 if name=='countries':
  assert {r[0] for r in old}=={r[0] for r in new};assert {r[0] for r in aa-zz}=={r[0] for r in zz-aa}=={'CHE','FRA','ESP','GBR','IRL'}
 elif name=='metadata':
  assert {r[0] for r in old}=={r[0] for r in new};assert {r[0] for r in aa-zz}=={r[0] for r in zz-aa}=={'completeness_audit','camp_focus','camp_planning'}
 else:assert aa<=zz,name
assert {q['id']:q for q in d['events']}=={k:json.loads(value) for k,value in c.execute('SELECT id,record_json FROM events')}
assert {q['slug']:q for q in d['camp_programmes']['profiles']}=={k:json.loads(value) for k,value in c.execute('SELECT slug,record_json FROM camp_programmes')}
assert json.loads(c.execute("SELECT value FROM metadata WHERE key='camp_planning'").fetchone()[0])==d['camp_planning'];c.close();o.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for s in t.split('BEGIN:VEVENT')[1:]:
  f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None);assert f['UID'] not in out;out[f['UID']]=f
 return out
name='dist/downloads/STEM_подтвержденные_даты.ics';oa=calendar(prior(name));na=calendar((ROOT/name).read_bytes())
expired=oa.keys()-na.keys();assert not expired
assert all(oa[k]['DTEND;VALUE=DATE']<='20261006' for k in expired)
assert all(oa[k]==na[k] for k in oa.keys()&na.keys()) and len(na)==2643 and len(na.keys()-oa.keys())==27
assert all('10–11' not in na[k]['SUMMARY'] for k in na.keys()-oa.keys())
name='dist/downloads/STEM_крупные_выставки.ics';assert calendar(prior(name))==calendar((ROOT/name).read_bytes()) and len(calendar((ROOT/name).read_bytes()))==104
for name in ['STEM_catalog.csv','STEM_календарь_2026_2027.csv','STEM_крупные_выставки.csv']:
 f=ROOT/'dist/downloads'/name
 if f.exists():
  arows=list(csv.DictReader(io.StringIO(prior('dist/downloads/'+name).decode('utf-8-sig'))));zrows=list(csv.DictReader(io.StringIO(f.read_text(encoding='utf-8-sig'))))
  assert all(row in zrows for row in arows),name
plan=json.loads((ROOT/'data/research-plan.json').read_text());oldplan=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==111
assert {q['id'] for q in plan['requirements']}=={q['id'] for q in oldplan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==oldplan[k],k
assert plan['complete_database_download']==sm and plan['complete_json_download']==jm
assert d['coverage_summary']['fully_audited_countries']==0 and not plan['latest_validation']['worldwide_complete']
for stem in ['research-plan','europe-camps-audit-v111','europe-camps-source-receipts-v111']:
 assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for k in ['events','camp_programmes','camp_planning','league_guide']:assert web[k]==d[k]
html=(ROOT/'dist/index.html').read_text();assert 'data-ui-version="111"' in html and 'STEM_europe_camps_audit_v111.json' in html and 'href="downloads/STEM_database_json.zip"' in html
for f in ROOT.joinpath('dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['data.js','camp-planning.js','camp-programmes.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['camp-planning.js','camp-programmes.css']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
assert "unknown:'Формат уточняется'" in (ROOT/'dist/assets/camp-programmes.js').read_text()
assert '06 ОКТЯБРЯ 2026' in (ROOT/'dist/assets/camp-programmes.js').read_text()
result=dict(status='passed',version=111,old_event_ids_preserved=3376,new_event_ids=sorted(v.keys()-e.keys()),new_calendar_rows=43,old_dossiers_preserved=815,new_dossiers=12,total_dossiers=827,complete_sqlite=True,complete_json=True,old_family_budget_offers_preserved=14,total_family_budget_offers=17,family_ics=2643,exhibition_ics=104,expired_ics_uids=sorted(expired),goal='active',new_visual_pdf_checks=16,new_visual_image_checks=3)
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
