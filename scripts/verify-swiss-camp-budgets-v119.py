"""Independent source, fee, child-gate and full database preservation checks."""
import collections,hashlib,io,json,re,sqlite3,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT.parent/'stem-family-atlas-work/camp-swiss-primary-v119'
BASE='1dc04cb6c894ca9be2f738e47a13b260608751ac'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clause(key,*needles):
 t=re.sub(r'\s+','',(P/(key+'.txt')).read_text())
 for s in needles:assert re.sub(r'\s+','',s) in t,(key,s)
d=json.loads((ROOT/'data/catalog.json').read_text());b=json.loads(prior('data/catalog.json'))
assert {k:v for k,v in d.items() if k!='camp_planning'}=={k:v for k,v in b.items() if k!='camp_planning'}
assert len(d['events'])==3555 and len(d['camp_programmes']['profiles'])==890
assert collections.Counter(q['block'] for q in d['events'])=={'Соревнования':1153,'События':189,'Лагеря':2213}
m=d['camp_planning'];assert m['version']==119 and m['offers'][:27]==b['camp_planning']['offers']
assert {k:v for k,v in m.items() if k not in ['version','asof','offers']}=={k:v for k,v in b['camp_planning'].items() if k not in ['version','asof','offers']}
costs={'suisse-day-five':2000,'suisse-board-matvey':4400,'suisse-board-both-seven':8800,'lovell-winter-day':3900,'lovell-winter-board':5400,'lyceum-junior-week':2000,'garenne-winter-integration-day':15000,'garenne-winter-integration-board':15900}
offers={q['id']:q for q in m['offers']};assert set(q['id'] for q in m['offers'][27:])==set(costs)
assert len(offers)==len(m['offers'])==35
for ident,amount in costs.items():
 q=offers[ident];assert q['currency']=='CHF' and sum(q['base_by_child'].values())+sum(x['amount'] for x in q['required'])==amount
 assert q['unknown_required'] and all(x['unit']=='amount' and x['min']==0 for x in q['unknown_required'])
 assert q['discount_second']==0 and q['checked']=='2026-10-06'
 assert set(q['base_by_child'])==set(q['children'])
profiles={q['slug']:q for q in d['camp_programmes']['profiles']}
assert all(q['slug'] in profiles and q['format'] in profiles[q['slug']]['formats'] for q in m['offers'][27:])
assert len({q['slug'] for q in m['offers']})==25
assert offers['suisse-board-matvey']['children']==['matvey'] and 'oscar' not in offers['suisse-board-matvey']['base_by_child']
assert 'после 7-летия' in offers['suisse-board-both-seven']['gate'] and 'пока ему 9' in offers['lyceum-junior-week']['gate']
assert offers['suisse-day-five']['period_type']=='season_window' and offers['suisse-day-five']['optional'][0]['amount']==200
assert len(offers['lovell-winter-day']['sessions'])==14 and len(offers['lovell-winter-board']['sessions'])==11
assert not any(a.startswith('2027-01-1') or a.startswith('2027-01-2') for a,_ in offers['lovell-winter-board']['sessions'])
for ident in ['garenne-winter-integration-day','garenne-winter-integration-board']:
 assert offers[ident]['price_basis']=='from' and offers[ident]['sessions'][-1]==['2027-03-07','2027-03-19']
 assert 'во вторую неделю лыж нет' in offers[ident]['gate']
clause('suisse-day-prices','200 CHF','1000 CHF','21 June 2027','13 August 2027','120 CHF per night')
clause('suisse-day','ages of 5 and 17','20 CHF per day, return, per camper')
clause('suisse-board-overview','7 – 11 YEARS OLD','15 – 17 YEARS OLD')
clause('suisse-dates','Summer 2027','CHF 4400','Saturday 19 June','Saturday 14 August','Comprehensive camper insurance')
clause('suisse-faq','CHF 500','four weeks','100 CHF per adult','from Camp Suisse to Aigle Train Station','09h00 and 16h00','11h00 am and 17h00')
clause('suisse-policy-pdf','registered with a GP in their home country','summary does not form part of your contract of insurance')
clause('suisse-terms-pdf','BA-DF-04-18-1.0','Confirmation Invoice','four weeks')
clause('lovell-pdf','ages of 5 to 16','CHF 2,600.00','CHF 1,900.00','CHF 100.00 / week','CHF 50.00 / week','No boarding spaces available.','30 days before','ski and snowboard rentals','medical insurance','transportation to and from the ski hill','or Language Lessons')
clause('lyceum-pdf','6 — 9 years','5 — 9 July 2027','26 — 30 July 2027','CHF 1,000','No overnight stay')
clause('lyceum-junior','16 lessons','health and accident insurance','29 – 15','14 or less','St. Moritz and Madulain')
clause('garenne-winter','Ages 5 to 14',"CHF 7'500", "CHF 7'950",'08:30-16:00','at least two ski sessions per week','07.03.2027 - 19.03.2027 (no skiing in the second week)')
clause('altitude-booking-day','2027','6 to 14 Years Old')
assert 'value="2027-06-28"' in (P/'altitude-booking-day.html').read_text()
clause('altitude-terms','do not provide any form of insurance','20% deposit','31st May')
receipt=json.loads((ROOT/'data/swiss-camp-budget-source-receipts-v119.json').read_text())
assert len(receipt['sources'])==20 and sum(q.get('status')==200 for q in receipt['sources'])==19
assert not any(receipt['external_actions'].values()) and receipt['new_visual_pdf_checks']==5
for q in receipt['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
for f in ['lovell-visual-1.png','lovell-visual-2.png','lyceum-visual-1.png','suisse-policy-visual-1.png','suisse-terms-visual-2.png']:assert (P/f).stat().st_size>0
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
 assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert z.testzip() is None and z.namelist()==[m[ext+'_entry'],'README.txt'];body=z.read(m[ext+'_entry'])
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
 return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json')
assert json.loads(js)==d
f=P/'verified-v119.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as z:oldsql=z.read('STEM_database.sqlite')
f=P/'baseline-v118.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda z:sorted(z.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
 aa=set(o.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'))
 assert {r[0] for r in aa-zz}==({'camp_planning'} if name=='metadata' else set()),name
 assert {r[0] for r in aa}<={r[0] for r in zz},name
assert json.loads(c.execute("SELECT value FROM metadata WHERE key='camp_planning'").fetchone()[0])==m
c.close();o.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for s in t.split('BEGIN:VEVENT')[1:]:
  f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None)
  assert f['UID'] not in out;out[f['UID']]=f
 return out
for name,n in [('STEM_подтвержденные_даты.ics',2770),('STEM_крупные_выставки.ics',104)]:
 p='dist/downloads/'+name;assert calendar(prior(p))==calendar((ROOT/p).read_bytes()) and len(calendar(prior(p)))==n
for name in ['STEM_catalog.csv','STEM_календарь_2026_2027.csv','STEM_крупные_выставки.csv']:
 f=ROOT/'dist/downloads'/name
 if f.exists():assert f.read_bytes()==prior('dist/downloads/'+name),name
plan=json.loads((ROOT/'data/research-plan.json').read_text());oldplan=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==119
assert {q['id'] for q in plan['requirements']}=={q['id'] for q in oldplan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria','next_research']:assert plan[k]==oldplan[k],k
assert plan['complete_database_download']==sm and plan['complete_json_download']==jm
assert not plan['latest_validation']['worldwide_complete'] and d['coverage_summary']['fully_audited_countries']==0
for stem in ['research-plan','swiss-camp-budgets-audit-v119','swiss-camp-budget-source-receipts-v119']:
 assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for k in ['events','camp_programmes','camp_planning','league_guide','family_strategy']:assert web[k]==d[k]
assert 'data-ui-version="119"' in (ROOT/'dist/index.html').read_text()
for f in (ROOT/'dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['camp-planning.js','camp-programmes.js','data.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['nearby-participation.js','nearby-participation.css','experience.js']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=119,all_events_unchanged=3555,all_dossiers_unchanged=890,prior_budget_objects_unchanged=27,new_partial_budget_scenarios=8,complete_sqlite=True,complete_json=True,worldwide_scope_preserved=True,family_ical=2770,exhibition_ical=104,goal='active')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
