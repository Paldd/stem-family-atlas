"""Independent primary-clause checks, full exports and prior object preservation."""
import collections,csv,hashlib,io,json,re,sqlite3,subprocess,zipfile
from camp_americas_v126 import ROOT,BASE,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-americas-primary-v126'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
clause_failures=[]
def clause(key,*values):
 norm=lambda t:re.sub(r'\s+','',t).casefold().replace('–','-').replace('—','-')
 t=norm((P/(key+'.txt')).read_text())
 for v in values:
  if norm(v) not in t:clause_failures.append((key,v))
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={q['slug']:q for q in b['camp_programmes']['profiles']};z={q['slug']:q for q in d['camp_programmes']['profiles']}
assert len(a)==980 and len(z)==999 and z.keys()-a.keys()==set(NEW)
assert [k for k,v in a.items() if z[k]!=v]==UPDATED
assert d['camp_programmes']['shortlist'][:233]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==236
assert d['camp_programmes']['gaps'][:281]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==289
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']};expected={}
for slug in NEW:
 p=z[slug]
 if p['timing']['precision']=='season_window':continue
 for start,end in p['timing']['sessions']:expected[p['id']+'-'+start.replace('-','')+'-'+end.replace('-','')]=(start,end,slug)
assert len(expected)==46 and len(now)==3741 and now.keys()-old.keys()==expected.keys() and all(now[k]==v for k,v in old.items())
assert collections.Counter(q['block'] for q in now.values())=={'Соревнования':1153,'События':189,'Лагеря':2399}
for key,(start,end,slug) in expected.items():
 e=now[key];assert (e['start'],e['end'],e['camp_dossier_slug'])==(start,end,slug)
 assert e['date_precision']=='published_session' and e['languages']==[] and e['language_mode']=='unconfirmed'
 if slug in ['frost-pathfinders','frost-lego-day','frost-inventors-day']:
  assert e['date_scope']=='day_camp_window' and e['attendance_weekdays']==['MO','TU','WE','TH','FR']
 else:assert e['date_scope']=='camp_session'
 if slug in ['frost-family-weekends','frost-family-farm']:assert e['participation']=='residential' and 'ответственным взрослым' in e['entry']
 if slug=='frost-lego-day':assert e['age']==('Grades 2–3' if start=='2027-06-28' else 'Grades 3–5') and 'robotics' not in e['themes']
 if slug=='frost-inventors-day':assert e['age']==('Grades 4–5' if start=='2027-07-05' else 'Grades 2–3')
 if slug=='frost-family-farm' and start.startswith('2027'):assert 'неизвестна' in e['cost']
for slug in NEW:
 p=z[slug];assert p['checked']=='2026-10-06' and all(s['checked']=='2026-10-06' for s in p['sources'])
 assert p['confirmed_instruction_languages']==(['EN'] if slug=='cisv-mexico-village-route' else [])
for slug in ['frost-sugarloaf','frost-seedlings','explora-kids','explora-xtreme','explora-parent-child','coderev-minecraft','coderev-roblox','coderev-revrobots','cisv-mexico-village-route']:
 assert z[slug]['timing']['sessions']==[]
assert z['frost-winter-family']['timing']['precision']=='season_window' and all(x['kind']=='season_window' and not x['event_ids'] for x in z['frost-winter-family']['calendar_links'])
assert all(z[s]['family_fit']['matvey']['status']==z[s]['family_fit']['oscar']['status']=='later' for s in ['explora-xtreme','cisv-mexico-village-route'])
assert all(z[s]['family_fit']['oscar']['status']=='later' for s in ['frost-durango','coderev-roblox','coderev-revrobots'])
assert z['envision-winter-audit']['timing']['sessions']==[] and z['envision-winter-audit']['id']=='CP299'
assert d['camp_planning']==b['camp_planning'] and len(d['camp_planning']['offers'])==48
osrc={q['url']:q for q in b['sources']};nsrc={q['url']:q for q in d['sources']};assert all(nsrc[k]==v for k,v in osrc.items())
clause('inned-camps','Winter 2026','Mon 21 to Wed 23 December','Mon 28 to Wed 30 December','5 to 12','JK through Grade 6','$240','$450','open to any child','Builds change')
clause('inned-terms','Enrollment Agreement','LOL Playlab')
clause('frost-traditional-fees','2027 Camp Tuition Fees','June 27th','July 9th','July 11th','July 23rd','Aug 8th','Aug 20th','5%','$3367','$3199','$2862','$1852','$1759','$1574','$2080','$1937','$1733','March 1st','70%','June 1st')
clause('frost-traditional','grades 2-3','Sessions 1A, 1B, 4A & 4B')
clause('frost-farm','entering grades 2–10','1A (girls+)','1B (boys+)','4A (girls+)','4B (boys+)','grades 2-4')
clause('frost-day','2027 Summer','June 28 – July 2','Aug 16 – Aug 20','Aug 23 – Aug 27','Pathfinders (Grades 1-5)','Week 1 • LEGO® Masters (Grades 2-3)','Week 3 • LEGO® Masters (Grades 3-5)',"Week 2 • Inventor's Workshop (Grades 4-5)","Week 8 • Inventor's Garage (Grades 2-3)")
clause('frost-day-fees','2026','$485','$400','$315','$495','$410','$325','Grahamsville','May 1')
clause('frost-family','Oct 9-12, 2026','December 4-6, 2026','January 15-18, 2027','May 21-23, 2027','East Valley Ranch','May 28-31, 2027','June 4-6, 2027','June 11-13, 2027','$285','$380','one full-paying guest')
clause('frost-lodging-prices','2026-27','2 NIGHTS (4 MEALS)','3 NIGHTS (7 MEALS)','$225','$300','$345','$518','$355','$525','$1,420','$2,090','age 5 & under')
clause('frost-family-prices','December 27 , 2026 - January 2, 2027','$225 $300 $385 $465 $545','$407 $611 $712 $814 $930','$173 $259 $302 $345 $395','Price Per Cabin','2-night minimum','Thursday','12:30 pm','$14','$13','Saturday 1/2')
clause('explora-kids','6','12');clause('explora-xtremo','13','17');clause('explora-verano','VERANO 2027','13-18 JULIO','20-25 JULIO')
clause('coderev-courses','Courses 2024','6-10','8-10','Arduino','simulator','140','$50')
clause('coderev-winter','Wed','Dec 25','Dec 22');clause('coderev-santa','369.99','492.99','125')
clause('coderev-service','1 week','one calendar year','3 weeks')
clause('cisv-mx','inglés');clause('cisv-village','11','28','21')
clause('hb-description-correct','formal diagnosis','1:1 support','December 31')
assert not clause_failures,clause_failures
assert (P/'museo-api.txt').read_text().strip()=='[]' and (P/'museo-root-api.txt').read_text().strip()=='[]'
r=json.loads((ROOT/'data/americas-camps-source-receipts-v126.json').read_text());assert len(r['sources'])==64 and sum(q.get('status')==200 for q in r['sources'])==56 and not any(r['external_actions'].values())
for q in r['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert next(q for q in r['sources'] if q['key']=='frost-handbook')['content_status']=='challenge_not_programme_evidence'
assert next(q for q in r['sources'] if q['key']=='frost-school-break')['content_status']=='soft_404_not_programme_evidence'
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
 assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as q:
  assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry'])
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
 return body
sql=portable('STEM_database_download.json','sqlite');js=portable('STEM_database_json_download.json','json');assert json.loads(js)==d
f=P/'verified-v126.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v125.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
changes={}
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
 aa=set(o.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'));removed={r[0] for r in aa-zz}
 allowed={'metadata':{'camp_focus','completeness_audit'},'countries':{'USA','CAN','MEX'},'camp_programmes':{'CP299'}}.get(name,set())
 assert removed<=allowed,(name,removed);assert {r[0] for r in aa}<={r[0] for r in zz},name
 if removed:changes[name]=sorted(removed)
assert c.execute('SELECT count(*) FROM events').fetchone()[0]==3741 and c.execute('SELECT count(*) FROM camp_programmes').fetchone()[0]==999
c.close();o.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for s in t.split('BEGIN:VEVENT')[1:]:
  f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None)
  assert f['UID'] not in out;out[f['UID']]=f
 return out
for name,count in [('STEM_подтвержденные_даты.ics',2943),('STEM_крупные_выставки.ics',104)]:
 aa=calendar(prior('dist/downloads/'+name));zz=calendar((ROOT/'dist/downloads'/name).read_bytes())
 assert len(zz)==count and all(zz[k]==v for k,v in aa.items()) and len(zz)-len(aa)==(46 if count==2943 else 0)
 assert all(any(e in uid for e in expected) for uid in zz.keys()-aa.keys())
 if count==2943:assert {e for e in expected if any(e in uid for uid in zz.keys()-aa.keys())}==set(expected)
for name in ['STEM_catalog.csv','STEM_country_coverage.csv']:
 def rows(raw):return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
 aa=rows(prior('dist/downloads/'+name));zz=rows((ROOT/'dist/downloads'/name).read_bytes());key='id' if name=='STEM_catalog.csv' else 'iso'
 x={q[key]:q for q in aa};y={q[key]:q for q in zz};assert all(y[k]==v for k,v in x.items() if key=='id' or k not in ['USA','CAN','MEX'])
 assert y.keys()-x.keys()==(expected.keys() if key=='id' else set())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for key in ['events','camp_programmes','camp_planning','league_guide','family_strategy']:assert web[key]==d[key]
plan=json.loads((ROOT/'data/research-plan.json').read_text());prev=json.loads(prior('data/research-plan.json'))
assert plan['status']=='active' and plan['native_goal_status']=='active' and plan['next_research']==prev['next_research']
assert [x['id'] for x in plan['requirements']]==[x['id'] for x in prev['requirements']]
assert plan['latest_validation']['fully_audited_countries']==0 and plan['latest_validation']['worldwide_complete'] is False
assert plan['current_publication']['status']=='prepared_local_not_published' and plan['current_publication']['last_confirmed_published_version']==125
for stem in ['research-plan','americas-camps-audit-v126','americas-camps-source-receipts-v126']:assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
assert 'data-ui-version="126"' in (ROOT/'dist/index.html').read_text()
for f in (ROOT/'dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['camp-planning.js','camp-programmes.js','data.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['nearby-participation.js','nearby-participation.css','experience.js','camp-planning.js','app.js']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=126,all_prior_events_preserved=3695,unchanged_prior_dossiers=979,updated_prior_dossiers=UPDATED,all_prior_budget_objects_preserved=48,new_dossiers=19,new_calendar_rows=46,complete_sqlite=True,complete_json=True,sqlite_allowed_updated_keys=changes,family_ical=2943,exhibition_ical=104,worldwide_scope_preserved=True,goal='active',publication='prepared_local_not_published')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
