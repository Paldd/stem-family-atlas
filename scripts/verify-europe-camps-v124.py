"""Independent primary clause and complete-export preservation checks."""
import collections,csv,hashlib,io,json,re,sqlite3,subprocess,zipfile
from camp_europe_v124 import ROOT,BASE,NEW,NEW_IDS
P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v124'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clause(key,*values):
 t=re.sub(r'\s+','',(P/(key+'.txt')).read_text())
 for v in values:assert re.sub(r'\s+','',v) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={q['slug']:q for q in b['camp_programmes']['profiles']};z={q['slug']:q for q in d['camp_programmes']['profiles']}
assert len(a)==950 and len(z)==966 and z.keys()-a.keys()==set(NEW) and all(z[k]==v for k,v in a.items())
assert d['camp_programmes']['shortlist'][:227]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==230
assert d['camp_programmes']['gaps'][:265]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==272
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']};expected={}
for slug in NEW:
 p=z[slug]
 for start,end in p['timing']['sessions']:expected[p['id']+'-'+start.replace('-','')+'-'+end.replace('-','')]=(start,end,slug)
assert len(expected)==9 and len(now)==3667 and now.keys()-old.keys()==expected.keys() and all(now[k]==v for k,v in old.items())
assert collections.Counter(q['block'] for q in now.values())=={'Соревнования':1153,'События':189,'Лагеря':2325}
for key,(start,end,slug) in expected.items():
 e=now[key];assert (e['start'],e['end'],e['camp_dossier_slug'])==(start,end,slug)
 assert e['start']>='2026-10-12' and e['end']<='2026-10-27' and e['languages']==['EN'] and e['admission_kind']=='open_application'
 assert e['language_mode']==('primary' if slug=='simply-thriller' else 'camp_life')
 assert e['date_precision']==('published_rule' if slug=='simply-thriller' else 'published_session')
 if slug=='simply-thriller':assert '2026–27' in e['date_rule']
for slug in NEW:
 p=z[slug];assert p['checked']=='2026-10-06' and all(s['checked']=='2026-10-06' for s in p['sources'])
 if slug not in NEW[:7]:assert p['timing']['sessions']==[]
assert all(z[k]['family_fit']['matvey']['status']=='not_eligible' for k in ['iil-multi-junior','iil-lego-halloween','simply-mini-camps','lne-paris-holidays'])
assert z['lne-geneva-holidays']['family_fit']['matvey']['status']=='unknown'
assert z['osi-junior-robot-fr']['confirmed_instruction_languages']==[] and 'Français' in z['osi-junior-robot-fr']['language']
assert z['osi-swiss-drone']['confirmed_instruction_languages']==['EN'] and 'после 7' in z['osi-swiss-drone']['family_fit']['oscar']['detail']
assert all(z[k]['confirmed_instruction_languages']==[] for k in ['muncyt-electrones','muncyt-neutrones','muncyt-protones'])
assert all(z[k]['price']['year']==2026 for k in ['lne-paris-holidays','lne-geneva-holidays','eib-jonchere-how','muncyt-electrones'])
p=d['camp_planning'];assert len(p['offers'])==46 and p['offers'][:43]==b['camp_planning']['offers']
assert [q['id'] for q in p['offers'][43:]]==NEW_IDS and p['version']==124
assert [q['base_by_child'] for q in p['offers'][43:]]==[{'matvey':350},{'oscar':550},{'matvey':595}]
assert p['offers'][44]['optional']==[{'id':'latecare','label':'Оскардо 18:00 ·75CHF завсю 5-дневную неделю','amount':75}] or p['offers'][44]['optional'][0]['amount']==75
osrc={q['url']:q for q in b['sources']};nsrc={q['url']:q for q in d['sources']};assert all(nsrc[k]==v for k,v in osrc.items())
clause('iil-ai','8-13 y.o.','19-23.10.2026','350.00','No prerequisites','will NOT be able to have lunch','105 / week')
clause('iil-multi','3 to 6','CHF 550 per week','CHF625','CHF 125 per day','26 and 27 October','Lunch as well as morning and afternoon snacks')
clause('iil-lego','5-7 y.o.','110.00','26-27.10.2026','motorised technical models','+30chf for the two days')
clause('iil-chem','8-13','120.00','26-27.10.2026','copper and zinc','LED')
clause('iil-dance','6-9','300.00','19-23.10.2026')
clause('iil-music','6-9','275.00','19-23.10.2026','pBuzz')
clause('iil-main','bilingual (English / French ) environment')
clause('iil-terms','For children living abroad','third-party insurance','CHF 50','between 15 and 30','less than 15','French version is legally binding')
clause('simply-camps','All of our camps are delivered in English','Young Performers (7-11','Zurich | Oct 12 - Oct 16','Geneva (Versoix) | Oct 19 - Oct 23','CHF595.00','Mini camps for ages 4 to 6','1.09.25')
clause('simply-public','2026-27 Timetable','Halloween Creative Studio','45.00','non refundable deposit of 25%')
clause('simply-terms','Parents must provide packed lunches','No refunds are issued within 30 days','90%')
clause('lne-camps','Suitable for ages 3–7','27th to 30th April 2026','Full day: 400€','Half day: 250€','qualified native English and bilingual staff')
clause('lne-paris-pdf','From 3 - 7','500€ per week','picnic lunch')
clause('lne-geneva-pdf','630.- CHF / week for external students','600.- CHF / week for school students','no prorated fees','From 4 years old','Our camps are bilingual')
clause('muncyt-summer-pdf','34 niños y niñas','curso que han realizado en 2025/2026','1.º, 2.º y 3er.','4.º, 5.º y 6.º','LEGO MÓVIL','conceptos básicos de mecánica','ROBOMAKERS','3 días naturales','7 días antes')
clause('muncyt-announce','170 € / semana','20%','no serán acumulables')
clause('osi-swiss-drone','Age 7-9','Age 10-12','Languages offered','English','Kuspo Center','two, four, or eight')
clause('osi-junior-robots','Robot et Drone spécial 7 - 10 ans','Langues Proposées :','Français','deux créneaux scientifiques','trois à six lits')
clause('tecladies-camps','filles* âgées de 12 à 15 ans scolarisées en Suisse','19 au vendredi 23 octobre 2026','Français','CHF 250','CHF 100')
clause('eib-jonchere-correct-pdf','6 AU 10 JUILLET 2026','3 TO 11','French/ English bilingual camp','€595','€60','€220','€100')
r=json.loads((ROOT/'data/europe-camps-source-receipts-v124.json').read_text());assert len(r['sources'])==28 and sum(q.get('status')==200 for q in r['sources'])==27 and not any(r['external_actions'].values())
for q in r['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
 assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as q:
  assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry'])
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
 return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json');assert json.loads(js)==d
f=P/'verified-v124.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v123.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
changes={}
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
 aa=set(o.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'));removed={r[0] for r in aa-zz}
 allowed={'metadata':{'camp_focus','completeness_audit','camp_planning'},'countries':{'CHE'}}.get(name,set())
 assert removed<=allowed,(name,removed);assert {r[0] for r in aa}<={r[0] for r in zz},name
 if removed:changes[name]=sorted(removed)
assert c.execute('SELECT count(*) FROM events').fetchone()[0]==3667 and c.execute('SELECT count(*) FROM camp_programmes').fetchone()[0]==966
c.close();o.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for s in t.split('BEGIN:VEVENT')[1:]:
  f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None)
  assert f['UID'] not in out;out[f['UID']]=f
 return out
for name,count in [('STEM_подтвержденные_даты.ics',2882),('STEM_крупные_выставки.ics',104)]:
 aa=calendar(prior('dist/downloads/'+name));zz=calendar((ROOT/'dist/downloads'/name).read_bytes())
 assert len(zz)==count and all(zz[k]==v for k,v in aa.items()) and len(zz)-len(aa)==(9 if count==2882 else 0)
 assert all(any(e in uid for e in expected) for uid in zz.keys()-aa.keys())
for name in ['STEM_catalog.csv','STEM_country_coverage.csv']:
 def rows(raw):return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
 aa=rows(prior('dist/downloads/'+name));zz=rows((ROOT/'dist/downloads'/name).read_bytes());key='id' if name=='STEM_catalog.csv' else 'iso'
 x={q[key]:q for q in aa};y={q[key]:q for q in zz};assert all(y[k]==v for k,v in x.items() if key=='id' or k!='CHE')
 assert y.keys()-x.keys()==(expected.keys() if key=='id' else set())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for key in ['events','camp_programmes','camp_planning','league_guide','family_strategy']:assert web[key]==d[key]
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']=='active' and plan['native_goal_status']=='active' and plan['next_research']==json.loads(prior('data/research-plan.json'))['next_research']
assert plan['latest_validation']['fully_audited_countries']==0 and plan['latest_validation']['worldwide_complete'] is False
for stem in ['research-plan','europe-camps-audit-v124','europe-camps-source-receipts-v124']:assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
assert 'data-ui-version="124"' in (ROOT/'dist/index.html').read_text()
for f in (ROOT/'dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['camp-planning.js','camp-programmes.js','data.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['nearby-participation.js','nearby-participation.css','experience.js','camp-planning.js']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=124,all_prior_events_preserved=3658,all_prior_dossiers_preserved=950,all_prior_budget_objects_preserved=43,new_dossiers=16,new_calendar_rows=9,complete_sqlite=True,complete_json=True,sqlite_allowed_updated_keys=changes,family_ical=2882,exhibition_ical=104,worldwide_scope_preserved=True,goal='active')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
