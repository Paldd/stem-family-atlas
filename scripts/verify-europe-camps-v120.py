"""Independent source, child-gate, price and complete database checks."""
import collections,csv,hashlib,io,json,re,sqlite3,subprocess,zipfile
from camp_europe_v120 import ROOT,BASE,NEW,NEW_IDS,AUTUMN
P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v120'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clause(key,*values):
 t=re.sub(r'\s+','',(P/(key+'.txt')).read_text())
 for v in values:assert re.sub(r'\s+','',v) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'asof','events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={q['slug']:q for q in b['camp_programmes']['profiles']};z={q['slug']:q for q in d['camp_programmes']['profiles']}
assert len(a)==890 and len(z)==897 and z.keys()-a.keys()==set(NEW) and all(z[k]==v for k,v in a.items())
assert d['camp_programmes']['shortlist'][:215]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==217
assert d['camp_programmes']['gaps'][:240]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==244
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
expected={'CP892-20261019-20261023','CP892-20261026-20261030','CP893-20261019-20261023','CP893-20261026-20261030'}
assert len(now)==3559 and now.keys()-old.keys()==expected and all(now[k]==v for k,v in old.items())
assert collections.Counter(q['block'] for q in now.values())=={'Соревнования':1153,'События':189,'Лагеря':2217}
osrc={q['url']:q for q in b['sources']};nsrc={q['url']:q for q in d['sources']};assert all(nsrc[k]==v for k,v in osrc.items())
for slug in NEW:
 p=z[slug];assert p['checked']=='2026-10-06' and all(s['checked']=='2026-10-06' for s in p['sources'])
 assert p['confirmed_instruction_languages']==(['EN'] if slug==NEW[0] else ['EN','FR'] if slug in NEW[1:3] else [])
 assert p['timing']['sessions']==(AUTUMN if slug in NEW[1:3] else [])
assert z[NEW[0]]['formats']==['family'] and z[NEW[0]]['price']['year'] is None
assert z[NEW[2]]['family_fit']['matvey']['status']=='not_eligible' and z[NEW[2]]['age'].startswith('3–6')
assert z[NEW[3]]['family_fit']['matvey']['status']=='not_eligible' and z[NEW[4]]['family_fit']['oscar']['status']=='later'
assert z[NEW[5]]['family_fit']['matvey']['status']=='conditional' and '10-летия' in z[NEW[5]]['family_fit']['matvey']['detail']
assert all(z[s]['timing']['status']=='archive_next_unannounced' for s in NEW[3:])
m=d['camp_planning'];assert m['version']==120 and len(m['offers'])==43 and m['offers'][:35]==b['camp_planning']['offers']
offers={q['id']:q for q in m['offers']};assert [q['id'] for q in m['offers'][35:]]==NEW_IDS
costs=dict(zip(NEW_IDS,[2470,5060,2470,4260,2470,4260,787,395]))
for ident,cost in costs.items():
 q=offers[ident];assert sum(q['base_by_child'].values())+sum(x['amount'] for x in q['required'])==cost
 assert set(q['children'])==set(q['base_by_child']) and q['currency']=='EUR' and q['discount_second']==0
 assert q['slug'] in z and q['format'] in z[q['slug']]['formats'] and q['unknown_required']
assert offers[NEW_IDS[7]]['children']==['oscar'] and 'matvey' not in offers[NEW_IDS[7]]['base_by_child']
assert offers[NEW_IDS[6]]['base_by_child']=={'matvey':450,'oscar':337}
assert len(offers[NEW_IDS[1]]['sessions'])==3 and len(offers[NEW_IDS[3]]['sessions'])==4 and len(offers[NEW_IDS[5]]['sessions'])==2
assert offers[NEW_IDS[0]]['sessions'][0]==['2027-07-05','2027-07-16'] and offers[NEW_IDS[1]]['sessions'][0]==['2027-07-04','2027-07-17']
assert not any(x['id']=='daily_bus' or x['id']=='local_roundtrip' for x in offers[NEW_IDS[4]]['optional'])
clause('country-kids-children','English-speaking team','english speaking team','12 years old')
clause('country-kids-package','7,490','family of four')
clause('country-kids-terms','30% deposit','eight weeks prior','9 weeks','€300','Full holiday insurance')
clause('country-kids-faq','no additional cost','we do not offer lunch service on Saturday')
clause('pari-convention','3 à 10 ans','27 enfants','Ekilibre')
clause('pari-ranelagh','3 ans et jusqu’à 6 ans inclus','16 enfants','49 rue du Ranelagh')
clause('pari-convention-autumn-pdf','2026-2027','450€','337€','360€','270€','certificat médical','19 au 23 octobre 2026','26 au 30 octobre 2026','français et en anglais')
clause('pari-ranelagh-autumn-pdf','395€','296€','lunch box','enfants externes')
clause('etopia-main','2026','6 a 8 años','8 a 11 años','10 a 13 años','12 a 15 años','130 €','27€','5€')
clause('etopia-advanced','10 a 13 años','autónoma','sensores','programación por bloques','el contenido y el temario son los mismos')
clause('playcode-university','6 y los 16 años','22, 23, 25 y 26 de junio','115€','135€','LEGO, Arduino, drones, Micro:Bit, Edison, Delightex')
clause('enforex-2027-pdf','PRICES AND DATES 2027','€ 2.495','€ 2.095','€ 1.200','€ 35 one-time','€ 850','€ 250/$ 300 deposit','€ 300 per week','5-18 y.','Monday - Friday 9 am-8 pm')
r=json.loads((ROOT/'data/europe-camps-source-receipts-v120.json').read_text());assert len(r['sources'])==27 and sum(q.get('status')==200 for q in r['sources'])==24
assert r['new_visual_pdf_checks']==10 and r['pdf_pages_text_extracted']==57 and not any(r['external_actions'].values())
for q in r['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
for key,pages in r['visual_pdf_pages'].items():
 for page in pages:assert (P/f'{key}-visual-{page}.png').stat().st_size>0
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
 assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as q:
  assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry'])
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
 return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json');assert json.loads(js)==d
f=P/'verified-v120.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v119.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
changes={}
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
 aa=set(o.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'))
 removed={r[0] for r in aa-zz}
 allowed={'metadata':{'camp_planning','camp_focus','completeness_audit'},'countries':{'FRA'}}.get(name,set())
 assert removed<=allowed,(name,removed)
 assert {r[0] for r in aa}<={r[0] for r in zz},name
 if removed:changes[name]=sorted(removed)
assert json.loads(c.execute("SELECT value FROM metadata WHERE key='camp_planning'").fetchone()[0])==m
assert c.execute('SELECT count(*) FROM events').fetchone()[0]==3559 and c.execute('SELECT count(*) FROM camp_programmes').fetchone()[0]==897
c.close();o.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for s in t.split('BEGIN:VEVENT')[1:]:
  f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None)
  assert f['UID'] not in out;out[f['UID']]=f
 return out
for name,count in [('STEM_подтвержденные_даты.ics',2774),('STEM_крупные_выставки.ics',104)]:
 a=calendar(prior('dist/downloads/'+name));zcal=calendar((ROOT/'dist/downloads'/name).read_bytes())
 assert len(zcal)==count and all(zcal[k]==v for k,v in a.items())
 assert len(zcal)-len(a)==(4 if count==2774 else 0)
 assert all(any(e in uid for e in expected) for uid in zcal.keys()-a.keys())
for name in ['STEM_catalog.csv','STEM_country_coverage.csv']:
 def rows(raw):return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
 aa=rows(prior('dist/downloads/'+name));zz=rows((ROOT/'dist/downloads'/name).read_bytes());key='id' if name=='STEM_catalog.csv' else 'iso'
 x={q[key]:q for q in aa};y={q[key]:q for q in zz};assert all(y[k]==v for k,v in x.items() if name!='STEM_country_coverage.csv' or k!='FRA')
 assert y.keys()-x.keys()==(expected if key=='id' else set())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for key in ['events','camp_programmes','camp_planning','league_guide','family_strategy']:assert web[key]==d[key]
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']=='active' and plan['native_goal_status']=='active' and plan['next_research']==json.loads(prior('data/research-plan.json'))['next_research']
assert plan['latest_validation']['fully_audited_countries']==0 and plan['latest_validation']['worldwide_complete'] is False
for stem in ['research-plan','europe-camps-audit-v120','europe-camps-source-receipts-v120']:
 assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
assert 'data-ui-version="120"' in (ROOT/'dist/index.html').read_text()
for f in (ROOT/'dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['camp-planning.js','camp-programmes.js','data.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['nearby-participation.js','nearby-participation.css','experience.js']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
assert 'if(replacingForm)return;' in (ROOT/'dist/assets/camp-planning.js').read_text()
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=120,all_prior_events_preserved=3555,all_prior_dossiers_preserved=890,all_prior_budget_objects_preserved=35,new_dossiers=7,new_calendar_rows=4,new_partial_budget_scenarios=8,complete_sqlite=True,complete_json=True,sqlite_allowed_updated_keys=changes,family_ical=2774,exhibition_ical=104,worldwide_scope_preserved=True,goal='active')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
