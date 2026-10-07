"""Independent primary-clause, preservation and complete-export verification."""
import collections,csv,hashlib,io,json,sqlite3,subprocess,zipfile
from camp_americas_v110 import ROOT,BASE,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-americas-primary-v110'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clauses(key,*values):
 t=' '.join((P/(key+'.txt')).read_text().split())
 for v in values:assert ' '.join(v.split()) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
changed={'asof','events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in changed}=={k:v for k,v in b.items() if k not in changed}
a={p['slug']:p for p in b['camp_programmes']['profiles']};z={p['slug']:p for p in d['camp_programmes']['profiles']}
assert len(a)==798 and len(z)==815 and set(z)-set(a)==set(NEW)
assert all(z[s]==p for s,p in a.items()) and len({p['id'] for p in z.values()})==815
assert d['camp_programmes']['shortlist'][:185]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==189
assert d['camp_programmes']['gaps'][:190]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==197
e={q['id']:q for q in b['events']};v={q['id']:q for q in d['events']}
assert e.keys()<=v.keys() and all(v[i]==q for i,q in e.items()) and len(v)-len(e)==28
assert collections.Counter(q['block'] for q in v.values())=={'Соревнования':1153,'События':189,'Лагеря':2034}
oldsrc={q['url']:q for q in b['sources']};newsrc={q['url']:q for q in d['sources']};assert all(newsrc[u]==q for u,q in oldsrc.items())
assert d['camp_planning']['offers'][:9]==b['camp_planning']['offers'] and len(d['camp_planning']['offers'])==14
offers={q['id']:q for q in d['camp_planning']['offers']}
assert offers['arca-food']['base_by_child']=={} and offers['arca-food']['required'][0]['amount']==497.80
assert offers['arca-no-food']['required'][0]['amount']==427.80
assert offers['cacao-valle']['discount_second']==.05 and offers['cacao-valle']['optional'][0]['amount']==150
assert offers['houston-three-day']['base_by_child']=={'matvey':179.95,'oscar':179.95}
assert len(offers['perot-three-day']['sessions'])==2 and not offers['perot-three-day']['optional']
for s in NEW:
 p=z[s];assert p['checked']=='2026-10-06'
 assert p['confirmed_instruction_languages']==(['EN'] if s in ['arca-english-family','kennedy-space-day'] else [])
 assert all(q['checked']=='2026-10-06' for q in p['sources'])
assert z['houston-multi-young']['family_fit']['oscar']['status']=='conditional'
assert z['houston-multi-middle']['family_fit']['oscar']['status']=='later'
assert z['houston-multi-older']['family_fit']['matvey']['status']=='later'
assert z['houston-multi-preschool']['family_fit']['matvey']['status']=='not_eligible'
assert z['berkana-thor-summer']['timing']['precision']=='season_window' and not any(q['event_ids'] for q in z['berkana-thor-summer']['calendar_links'])
for s in ['berkana-jotun-winter','kennedy-space-day','rf-steam-schools-archive']:
 assert not z[s]['timing']['sessions'] and not z[s]['calendar_links']
assert z['arca-english-family']['timing']['session_details'][0]['attendance_weekdays']==['FR','SA','SU']
ce=next(q for q in v.values() if q.get('camp_dossier_slug')=='cacao-valle-day')
assert ce['start']=='2027-01-04' and ce['end']=='2027-01-08' and ce['date_scope']=='day_camp_window' and not ce.get('attendance_weekdays')
clauses('arca-main','30/10 a 01/11 de 2026','TUDO. EM. INGLÊS.','R$ 497,80','R$ 427,80','valor total para 2 irmãos','Inscrições em breve','escola cristã','horários e o endereço completo serão divulgados em breve','Consulte as condições de cancelamento')
clauses('cacao-day','4 al 8 de enero 2027','martes a sábado','B/. 428','ITBMS incluído','B/.75.00','$406.60','antes del 1 de diciembre de 2026','del 2 al 15 de diciembre de 2026','A partir del 16 de diciembre de 2026')
clauses('berkana-winter','Jötunkamp 2027','Jötunkamp 2026','5 días','19 al 22','17de noviembre de 2026','$6,850','$7,900')
clauses('berkana-summer','Thorskamp 2027','18 de julio al 1ro de agosto','$13,200','$9,900','Descuentos no acumulables','10% de descuento para hermanos','ya ha comenzado')
clauses('berkana-day','Tyrskamp 2027','9am a 8pm','5 al 8 de agosto','$6,200','1ro de junio de 2027','$7,800','$1,200')
clauses('ksc-main','2026','SOLD OUT','June 1, 2017 – May 31, 2019','repeat the same curriculum','speak, read and understand directions in English','five (5) weeks','$50','less than two (2) weeks','51 inches','48 inches')
clauses('perot-main','2026 Discovery Camp schedule','November 23—25','December 21—23 and December 28—30','Grades K-4','Public: $275','Optional Aftercare: $45','additional fee of $75','strictly enforce grade-level','immunization records','less than four weeks','We do not offer refunds')
clauses('rf-steam','2026','10 a 14 años','127.750','23','6','TechnoKids')
reader=json.loads((P/'web-reader-fallback.json').read_text());rt=json.dumps(reader,ensure_ascii=False)
for value in ['October 9, 2026','$79.95','$74.95','$179.95','Engineering Basics','Robotic Exploration','Ages 6-7','Ages 8-9','Ages 10-11','November 23-25, 2026','$34.50','$20','Full refund (for any reason)','Full credit (for any reason)','Summer 2025']:
 assert value in rt,value
receipt=json.loads((ROOT/'data/americas-camps-source-receipts-v110.json').read_text())
assert len(receipt['sources'])==25 and sum(q.get('status')==200 for q in receipt['sources'])==22 and not any(receipt['external_actions'].values())
for q in receipt['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
q=receipt['primary_reader_fallback'];raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
 assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as q:
  assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry']);assert m[ext+'_sha256'] in q.read('README.txt').decode()
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
 return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json');assert json.loads(js)==d
f=P/'verified-v110.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v109.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
 old=list(o.execute('SELECT * FROM "'+name+'"'));new=list(c.execute('SELECT * FROM "'+name+'"'));aa=set(old);zz=set(new)
 if name=='countries':
  assert {r[0] for r in old}=={r[0] for r in new};assert {r[0] for r in aa-zz}=={r[0] for r in zz-aa}=={'USA','MEX','BRA','PAN'}
 elif name=='metadata':
  assert {r[0] for r in old}=={r[0] for r in new};assert {r[0] for r in aa-zz}=={r[0] for r in zz-aa}=={'asof','completeness_audit','camp_focus','camp_planning'}
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
expired=oa.keys()-na.keys();assert len(expired)==2
assert all(oa[k]['DTEND;VALUE=DATE']<='20261006' for k in expired)
assert all(oa[k]==na[k] for k in oa.keys()&na.keys()) and len(na)==2616 and len(na.keys()-oa.keys())==25
assert all('10–11' not in na[k]['SUMMARY'] for k in na.keys()-oa.keys())
name='dist/downloads/STEM_крупные_выставки.ics';assert calendar(prior(name))==calendar((ROOT/name).read_bytes()) and len(calendar((ROOT/name).read_bytes()))==104
for name in ['STEM_catalog.csv','STEM_календарь_2026_2027.csv','STEM_крупные_выставки.csv']:
 f=ROOT/'dist/downloads'/name
 if f.exists():
  arows=list(csv.DictReader(io.StringIO(prior('dist/downloads/'+name).decode('utf-8-sig'))));zrows=list(csv.DictReader(io.StringIO(f.read_text(encoding='utf-8-sig'))))
  assert all(row in zrows for row in arows),name
plan=json.loads((ROOT/'data/research-plan.json').read_text());oldplan=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==110
assert {q['id'] for q in plan['requirements']}=={q['id'] for q in oldplan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==oldplan[k],k
assert plan['complete_database_download']==sm and plan['complete_json_download']==jm
assert d['coverage_summary']['fully_audited_countries']==0 and not plan['latest_validation']['worldwide_complete']
for stem in ['research-plan','americas-camps-audit-v110','americas-camps-source-receipts-v110']:
 assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for k in ['events','camp_programmes','camp_planning','league_guide']:assert web[k]==d[k]
html=(ROOT/'dist/index.html').read_text();assert 'data-ui-version="110"' in html and 'STEM_americas_camps_audit_v110.json' in html and 'href="downloads/STEM_database_json.zip"' in html
for f in ROOT.joinpath('dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['data.js','camp-planning.js','camp-programmes.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['camp-planning.js','camp-programmes.js','camp-programmes.css']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=110,old_event_ids_preserved=3348,new_event_ids=sorted(v.keys()-e.keys()),new_calendar_rows=28,old_dossiers_preserved=798,new_dossiers=17,total_dossiers=815,complete_sqlite=True,complete_json=True,old_family_budget_offers_preserved=9,total_family_budget_offers=14,family_ics=2616,exhibition_ics=104,expired_ics_uids=sorted(expired),goal='active',new_visual_pdf_checks=0)
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
