"""Independent new-source clauses, age/price/date gates and worldwide preservation."""
import collections,csv,hashlib,io,json,re,sqlite3,subprocess,zipfile
from camp_northamerica_v122 import ROOT,BASE,NEW
P=ROOT.parent/'stem-family-atlas-work/camp-americas-primary-v122'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clause(key,*values):
 t=re.sub(r'\s+','',(P/(key+'.txt')).read_text())
 for v in values:assert re.sub(r'\s+','',v) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={q['slug']:q for q in b['camp_programmes']['profiles']};z={q['slug']:q for q in d['camp_programmes']['profiles']}
assert len(a)==915 and len(z)==932 and z.keys()-a.keys()==set(NEW) and all(z[k]==v for k,v in a.items())
assert d['camp_programmes']['shortlist'][:221]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==224
assert d['camp_programmes']['gaps'][:250]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==257
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
expected={}
for slug in NEW:
 p=z[slug]
 for start,end in p['timing']['sessions']:expected[p['id']+'-'+start.replace('-','')+'-'+end.replace('-','')]=(start,end,slug)
assert len(expected)==58 and len(now)==3657 and now.keys()-old.keys()==expected.keys() and all(now[k]==v for k,v in old.items())
assert collections.Counter(q['block'] for q in now.values())=={'Соревнования':1153,'События':189,'Лагеря':2315}
for key,(start,end,slug) in expected.items():
 e=now[key];assert (e['start'],e['end'],e['camp_dossier_slug'])==(start,end,slug)
 assert start>='2027-01-01' and e['level']=='D — обучение' and e['languages']==[] and e['language_mode']=='unconfirmed'
 if 'family' in z[slug]['formats']:assert e['participation']=='residential' and 'boarding' in z[slug]['timing']['session_details'][0]['formats']
 if slug=='interlochen-arts-discovery':assert e['date_precision']=='published_rule' and e['date_rule'] and e['attendance_weekdays']==['MO','TU','WE','TH','FR']
assert len(z['canaqua-shortstay']['timing']['sessions'])==9 and z['canaqua-shortstay']['timing']['session_details'][1]['age']=='5–11'
assert len(z['canaqua-parent-child']['timing']['sessions'])==2 and 'Sept20' in z['canaqua-parent-child']['programme'].replace(' ','')
for slug in ['canaqua-intro','canaqua-four-weeks','canaqua-film','interlochen-junior-exploration','interlochen-junior-visual']:assert z[slug]['family_fit']['oscar']['status']=='later'
assert z['canaqua-film']['themes']==['art'] and 'robotics' not in z['watitoh-2027']['themes']
assert all(q['status']=='unknown' for q in z['watitoh-2027']['family_fit'].values())
assert '2017–2021' in z['kandalore-one-week']['age'] and '2016–2020' in z['kandalore-prep-junior']['age']
assert '2390' in z['kandalore-one-week']['price']['label'] and '5830' in z['kandalore-prep-junior']['price']['label']
assert 'не установлены' in z['canaqua-shortstay']['price']['label'] and 'Family' in z['canaqua-family']['price']['deposit']
assert 'ПОСЛЕ' in z['watitoh-2027']['age'] and 'ДО' in z['interlochen-junior-visual']['age']
assert z['interlochen-arts-discovery']['timing']['sessions'][0]==['2027-06-21','2027-06-25'] and z['interlochen-arts-discovery']['timing']['sessions'][-1]==['2027-08-02','2027-08-06']
for slug in NEW:
 assert z[slug]['checked']=='2026-10-06' and all(s['checked']=='2026-10-06' for s in z[slug]['sources']) and z[slug]['confirmed_instruction_languages']==[]
 assert not any('2027-09-20' in row for row in z[slug]['timing']['sessions'])
assert d['camp_planning']==b['camp_planning'] and len(d['camp_planning']['offers'])==43
osrc={q['url']:q for q in b['sources']};nsrc={q['url']:q for q in d['sources']};assert all(nsrc[k]==v for k,v in osrc.items())
clause('canaqua-oneweek','Sun June 27th – Fri July 2, 2027','5-11','$1950','8-15','Lunch is included daily','Sibling discounts do not apply to day camp')
clause('canaqua-traditional','6-14','9-14','$3625','$6175','non-refundable $200','Family Camps','A 2% processing fee')
clause('canaqua-film','9 to 15','three periods','Aug 21 – Fri Aug 27 2027','$1950')
clause('canaqua-family','$895','up to 5/same household','Sun Sept 20, 2027','$395/pair','off grid Summit Village')
clause('interlochen-exploration','June 27, 2027 to July 10, 2027','$5,300','Junior (Grades 3-6)','January 15, 2027')
clause('interlochen-visual','four hours','does not require a portfolio','Ceramics','$5,300')
clause('interlochen-main','current grade level, not the grade they will be entering in the fall following Camp')
clause('interlochen-day','current 2026-2027 1st graders through 6th graders','June 21 to Friday, August 6','$425','$100','Summer 2026','Summer 2027 to be announced soon')
clause('interlochen-camp-int','$65 non-refundable fee')
clause('interlochen-int-faq','B1/B2 visas are not permitted','F-1 visa with an I-20','only able to pick up students','TVC')
clause('cayuga-fees','Sunday, June 26 to Saturday, August 7, 2027','$4,200','$120','only mandatory charge','$250','after April 30th')
clause('cayuga-junior','1st through 8th grade','13 years old and younger')
clause('cayuga-young','first to fourth grade','two college-aged counselors')
clause('watitoh-fees','June 26 – Friday, August 13, 2027','$14,950','$11,500','5th grade and younger','10/01/2026','7-10 days','not permitted at camp')
r=json.loads((ROOT/'data/northamerica-camps-source-receipts-v122.json').read_text());assert len(r['sources'])==35 and sum(q.get('status')==200 for q in r['sources'])==29 and not any(r['external_actions'].values())
for q in r['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
raw=(P/'web-reader-kandalore.txt').read_bytes();assert hashlib.sha256(raw).hexdigest()==r['reader_snapshot_sha256'] and b'2017-2021' in raw and b'5,830' in raw
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
 assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as q:
  assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry'])
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
 return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json');assert json.loads(js)==d
f=P/'verified-v122.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v121.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
changes={}
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
 aa=set(o.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'));removed={r[0] for r in aa-zz}
 allowed={'metadata':{'camp_focus','completeness_audit'},'countries':{'CAN','USA'}}.get(name,set())
 assert removed<=allowed,(name,removed);assert {r[0] for r in aa}<={r[0] for r in zz},name
 if removed:changes[name]=sorted(removed)
assert c.execute('SELECT count(*) FROM events').fetchone()[0]==3657 and c.execute('SELECT count(*) FROM camp_programmes').fetchone()[0]==932
c.close();o.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for s in t.split('BEGIN:VEVENT')[1:]:
  f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None)
  assert f['UID'] not in out;out[f['UID']]=f
 return out
for name,count in [('STEM_подтвержденные_даты.ics',2872),('STEM_крупные_выставки.ics',104)]:
 aa=calendar(prior('dist/downloads/'+name));zz=calendar((ROOT/'dist/downloads'/name).read_bytes())
 assert len(zz)==count and all(zz[k]==v for k,v in aa.items()) and len(zz)-len(aa)==(58 if count==2872 else 0)
 assert all(any(e in uid for e in expected) for uid in zz.keys()-aa.keys())
for name in ['STEM_catalog.csv','STEM_country_coverage.csv']:
 def rows(raw):return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
 aa=rows(prior('dist/downloads/'+name));zz=rows((ROOT/'dist/downloads'/name).read_bytes());key='id' if name=='STEM_catalog.csv' else 'iso'
 x={q[key]:q for q in aa};y={q[key]:q for q in zz};assert all(y[k]==v for k,v in x.items() if key=='id' or k not in ['CAN','USA'])
 assert y.keys()-x.keys()==(expected.keys() if key=='id' else set())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for key in ['events','camp_programmes','camp_planning','league_guide','family_strategy']:assert web[key]==d[key]
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']=='active' and plan['native_goal_status']=='active' and plan['next_research']==json.loads(prior('data/research-plan.json'))['next_research']
assert plan['latest_validation']['fully_audited_countries']==0 and plan['latest_validation']['worldwide_complete'] is False
for stem in ['research-plan','northamerica-camps-audit-v122','northamerica-camps-source-receipts-v122']:assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
assert 'data-ui-version="122"' in (ROOT/'dist/index.html').read_text()
for f in (ROOT/'dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['camp-planning.js','camp-programmes.js','data.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['nearby-participation.js','nearby-participation.css','experience.js']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
assert (ROOT/'dist/assets/camp-planning.js').read_bytes()==prior('dist/assets/camp-planning.js')
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=122,all_prior_events_preserved=3599,all_prior_dossiers_preserved=915,all_prior_budget_objects_preserved=43,new_dossiers=17,new_calendar_rows=58,complete_sqlite=True,complete_json=True,sqlite_allowed_updated_keys=changes,family_ical=2872,exhibition_ical=104,worldwide_scope_preserved=True,goal='active')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
