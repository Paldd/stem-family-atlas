"""Independent primary-clause checks and complete export/object preservation."""
import collections,csv,hashlib,io,json,re,sqlite3,subprocess,zipfile
from camp_asia_v125 import ROOT,BASE,NEW,NEW_IDS
P=ROOT.parent/'stem-family-atlas-work/camp-asia-primary-v125'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clause(key,*values):
 t=re.sub(r'\s+','',(P/(key+'.txt')).read_text())
 for v in values:assert re.sub(r'\s+','',v) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={q['slug']:q for q in b['camp_programmes']['profiles']};z={q['slug']:q for q in d['camp_programmes']['profiles']}
assert len(a)==966 and len(z)==980 and z.keys()-a.keys()==set(NEW) and all(z[k]==v for k,v in a.items())
assert d['camp_programmes']['shortlist'][:230]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==233
assert d['camp_programmes']['gaps'][:272]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==281
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']};expected={}
for slug in NEW:
 p=z[slug]
 for start,end in p['timing']['sessions']:expected[p['id']+'-'+start.replace('-','')+'-'+end.replace('-','')]=(start,end,slug)
assert len(expected)==28 and len(now)==3695 and now.keys()-old.keys()==expected.keys() and all(now[k]==v for k,v in old.items())
assert collections.Counter(q['block'] for q in now.values())=={'Соревнования':1153,'События':189,'Лагеря':2353}
for key,(start,end,slug) in expected.items():
 e=now[key];assert (e['start'],e['end'],e['camp_dossier_slug'])==(start,end,slug)
 assert e['date_precision']=='published_session' and e['date_scope']=='camp_session'
 if slug.startswith('hwa-winter'):
  assert e['languages']==['EN'] and e['language_mode']=='bilingual' and e['start']!='2027-02-15'
  if start=='2027-02-01':assert end=='2027-02-04' and 'короткой недели' in e['cost']
 elif slug=='kti-gmi-winter':
  assert e['iso']==['MYS'] and e['language_mode']=='primary' and e['availability']['status']=='closed' and e['admission_kind']=='organization_route' and 'заполнен' in e['entry']
 elif slug=='stark-science-research':assert e['admission_kind']=='organization_route' and e['languages']==[]
 else:assert e['languages']==[] and e['language_mode']=='unconfirmed'
for slug in NEW:
 p=z[slug];assert p['checked']=='2026-10-06' and all(s['checked']=='2026-10-06' for s in p['sources'])
assert z['kti-gmi-winter']['availability']['status']=='closed'
assert z['stark-tinker-winter']['family_fit']['matvey']['status']=='unknown'
assert z['stark-science-research']['family_fit']['matvey']['status']=='unknown'
assert all(z[s]['confirmed_instruction_languages']==[] for s in NEW[:3]+NEW[7:12])
assert all(z[s]['family_fit']['matvey']['status']=='later' and z[s]['family_fit']['oscar']['status']=='later' for s in [NEW[5],NEW[6],NEW[13]])
assert z['ulc-junior-camp']['timing']['sessions']==z['ulc-teen-winter']['timing']['sessions']==[]
p=d['camp_planning'];assert len(p['offers'])==48 and p['offers'][:46]==b['camp_planning']['offers']
assert [q['id'] for q in p['offers'][46:]]==NEW_IDS and p['version']==125
assert [q['base_by_child'] for q in p['offers'][46:]]==[{'matvey':1490,'oscar':1490},{'matvey':2850,'oscar':2850}]
assert all(q['discount_second']==0 and q['currency']=='SGD' and q['unknown_required'] for q in p['offers'][46:])
osrc={q['url']:q for q in b['sources']};nsrc={q['url']:q for q in d['sources']};assert all(nsrc[k]==v for k,v in osrc.items())
clause('stark-tinker','2027／1／30','2／3','09:00','16:00','12,500','國小一～六年級','概念設計稿','1／30、1／31')
clause('stark-winter','09:00–17:00','寒暑假平日限定','保留 7 天','退還 90%','退還 50%')
clause('stark-neuro','約小三 ～ 小六','68 頁','9,900','09:00 – 17:00','前測','後測')
clause('stark-research','國小四年級','小史塔克常態班學員','VSTC','2 至 3','42 小時','22,000','25,000','30,000','10,000','僅接受轉帳','無法使用儲值')
clause('stark-gmi-linked','報名已額滿','99,000','10 – 15','全英文授課','Mercure Kuala Lumpur Trion','週末照常上課','機票','KUKA','只參觀、不操作')
clause('hwa-winter','15 – 16 Feb 2027','1,490','2,850','first 50','15 Oct 2026','Excludes registration','9% GST')
clause('hwa-brochure','15 Feb - 19 Feb 2027','S$1490','S$2850','INCLUSION','Registration fee','meal fee','accident insurance fee','UOI (English)','UOI (Chinese)','4 Feb','Half day')
clause('hwa-refund','48 hours','30 days','200','12 months','No refunds','GST')
clause('hwa-application','Accommodation','After School Care','Language Proficiency','Mandarin','Grade 1','Grade 12')
clause('kids-calendar-layout','Mystic School','October, 12','Spooktacular','November, 23','Mini Detective','December 4','Lit & Lines','December, 7','December, 14','9:00am','3:00pm')
clause('ulc-junior','aged 5-12+','3-10 students','level test','English abilities','10','31 July')
clause('ulc-camps','13 to 18','subject to client verification','Mid-December to Early January (Dates TBC)','$580/Week','$980/Week','20 – 31 July 2026')
clause('sja-grade3','2025-2026','VEX GO','VEXcode GO','Bumper Switch','overnight camping trip at school')
clause('sja-grade4','2025-2026','VEX GO','VEXcode GO','multi-day camps')
r=json.loads((ROOT/'data/asia-camps-source-receipts-v125.json').read_text());assert len(r['sources'])==31 and sum(q.get('status')==200 for q in r['sources'])==18 and not any(r['external_actions'].values())
for q in r['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
reader=(P/'web-reader-kids-clauses.json').read_text();assert '4 to 8' in reader and 'No membership required' in reader and 'fifty' not in reader and '50%' in reader
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
 assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as q:
  assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry'])
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
 return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json');assert json.loads(js)==d
f=P/'verified-v125.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v124.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
changes={}
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
 aa=set(o.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'));removed={r[0] for r in aa-zz}
 allowed={'metadata':{'camp_focus','completeness_audit','camp_planning'},'countries':{'TWN','SGP','MYS'}}.get(name,set())
 assert removed<=allowed,(name,removed);assert {r[0] for r in aa}<={r[0] for r in zz},name
 if removed:changes[name]=sorted(removed)
assert c.execute('SELECT count(*) FROM events').fetchone()[0]==3695 and c.execute('SELECT count(*) FROM camp_programmes').fetchone()[0]==980
c.close();o.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for s in t.split('BEGIN:VEVENT')[1:]:
  f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None)
  assert f['UID'] not in out;out[f['UID']]=f
 return out
for name,count in [('STEM_подтвержденные_даты.ics',2897),('STEM_крупные_выставки.ics',104)]:
 aa=calendar(prior('dist/downloads/'+name));zz=calendar((ROOT/'dist/downloads'/name).read_bytes())
 assert len(zz)==count and all(zz[k]==v for k,v in aa.items()) and len(zz)-len(aa)==(15 if count==2897 else 0)
 assert all(any(e in uid for e in expected) for uid in zz.keys()-aa.keys())
 if count==2897:
  exported={e for e in expected if any(e in uid for uid in zz.keys()-aa.keys())}
  eligible={e for e,(_,_,slug) in expected.items() if slug not in ['kti-gmi-winter','hwa-winter-myp','hwa-winter-upper']}
  assert exported==eligible and len(exported)==15
for name in ['STEM_catalog.csv','STEM_country_coverage.csv']:
 def rows(raw):return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
 aa=rows(prior('dist/downloads/'+name));zz=rows((ROOT/'dist/downloads'/name).read_bytes());key='id' if name=='STEM_catalog.csv' else 'iso'
 x={q[key]:q for q in aa};y={q[key]:q for q in zz};assert all(y[k]==v for k,v in x.items() if key=='id' or k not in ['TWN','SGP','MYS'])
 assert y.keys()-x.keys()==(expected.keys() if key=='id' else set())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for key in ['events','camp_programmes','camp_planning','league_guide','family_strategy']:assert web[key]==d[key]
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']=='active' and plan['native_goal_status']=='active' and plan['next_research']==json.loads(prior('data/research-plan.json'))['next_research']
assert plan['latest_validation']['fully_audited_countries']==0 and plan['latest_validation']['worldwide_complete'] is False
for stem in ['research-plan','asia-camps-audit-v125','asia-camps-source-receipts-v125']:assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
assert 'data-ui-version="125"' in (ROOT/'dist/index.html').read_text()
for f in (ROOT/'dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['camp-planning.js','camp-programmes.js','data.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['nearby-participation.js','nearby-participation.css','experience.js','camp-planning.js']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=125,all_prior_events_preserved=3667,all_prior_dossiers_preserved=966,all_prior_budget_objects_preserved=46,new_dossiers=14,new_calendar_rows=28,complete_sqlite=True,complete_json=True,sqlite_allowed_updated_keys=changes,family_ical=2897,exhibition_ical=104,worldwide_scope_preserved=True,goal='active')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
