"""Independent primary facts, preservation, calendar and complete portable-export checks."""
import collections,csv,hashlib,io,json,sqlite3,subprocess,zipfile
from camp_asia_v112 import ROOT,BASE,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-asia-primary-v112'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clauses(key,*values):
 t=' '.join((P/(key+'.txt')).read_text().split())
 for v in values:assert ' '.join(v.split()) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'asof','events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={p['slug']:p for p in b['camp_programmes']['profiles']};z={p['slug']:p for p in d['camp_programmes']['profiles']}
assert len(a)==827 and len(z)==839 and set(z)-set(a)==set(NEW)
assert [s for s in a if z[s]!=a[s]]==UPDATED and len({p['id'] for p in z.values()})==839
assert d['camp_programmes']['shortlist'][:193]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==197
assert d['camp_programmes']['gaps'][:203]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==208
e={q['id']:q for q in b['events']};v={q['id']:q for q in d['events']}
updated={'CP676-20270105-20270124','CP676-20270127-20270215'}
assert len(e)==3419 and e.keys()<=v.keys() and {k for k in e if e[k]!=v[k]}==updated and len(v)-len(e)==2
assert collections.Counter(q['block'] for q in v.values())=={'Соревнования':1153,'События':189,'Лагеря':2079}
oldsrc={s['url']:s for s in b['sources']};newsrc={s['url']:s for s in d['sources']};assert all(newsrc[u]==s for u,s in oldsrc.items())
assert d['camp_planning']['offers']==b['camp_planning']['offers'] and len(d['camp_planning']['offers'])==17
for s in NEW:
 p=z[s];assert p['checked']=='2026-10-06' and all(q['checked']=='2026-10-06' for q in p['sources'])
 expected=['EN'] if s in ['winning-sg-aigc','winning-cebu-steam','winning-cebu-family','sunshine-japan-seasonal','kspace-summer','hafs-language-board'] else []
 assert p['confirmed_instruction_languages']==expected,s
 if s not in NEW[:2]:assert not p['timing']['sessions'] and not p['calendar_links'],s
assert z['winning-sg-aigc']['timing']['sessions']==[['2027-01-23','2027-02-01']]
assert all(f['status']=='later' for f in z['winning-sg-aigc']['family_fit'].values())
assert z['winning-cebu-steam']['iso']=='PHL' and z['winning-cebu-family']['iso']=='PHL'
assert z['winning-cebu-steam']['timing']['sessions']==[['2027-01-22','2027-02-03']]
assert z['winning-cebu-steam']['family_fit']['matvey']['status']=='conditional' and z['winning-cebu-steam']['family_fit']['oscar']['status']=='later'
assert z['winning-cebu-steam']['themes']==['stem','engineering','science'] and z['winning-sg-aigc']['themes']==['ai','general','languages']
for s in ['kidchen-autumn-half','kidchen-autumn-full']:assert z[s]['price']['year'] is None
for s in ['kspace-summer','kspace-winter']:assert z[s]['timing']['status']=='archive_next_unannounced'
for s in ['winning-cebu-family','hafs-language-board','smis-jeju-winter']:assert z[s]['language_evidence_role']=='language_lessons'
clauses('winning-sg','2027/01/23~2027/02/01','US$1,000','USD 3,900','兩個主題課程皆採全英語沉浸式教學')
clauses('winning-cebu-school','全程全英文沉浸式學習')
clauses('winning-cebu-poster','10–17 歲','1/22~2/3 2027','1,900美元','2,200美元','175 美元','不得參與STEAM')
clauses('winning-family','2027','6-10歲','10-18歲','English Only Policy')
clauses('young-holiday','AlgoPlay (Recommended for 5-9 years old)','Bricks Challenge (Recommended for 6-12 years old)','Robobricks (Recommended for 8-12 years old)','2 lessons in 3 hours','Not to be brought home','Learn English software engineering terminology')
clauses('kspace-summer-pdf','Summer School 2026','August 31st 2025','¥25,000','¥8,000','¥15,000','instruction is only in English','exclusive of Japanese Consumption Tax','anaphylactic level allergies')
clauses('kspace-winter-pdf','Winter School 2025/26','December 20th 2025','January 3rd 2026','zero cancellation, zero refund policy')
clauses('hafs-faq','영어만 완벽하게 사용하는 것은 불가능합니다.','초등 4, 5, 6학년 / 중등 1, 2학년')
receipt=json.loads((ROOT/'data/asia-camps-source-receipts-v112.json').read_text())
assert len(receipt['sources'])==39 and sum(q.get('status')==200 for q in receipt['sources'])==35 and not any(receipt['external_actions'].values())
for q in receipt['sources']:
 if q['body_snapshot_retained']:
  raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert sum(q.get('raw_filename','').endswith('.pdf') for q in receipt['sources'])==4
assert next(q for q in receipt['sources'] if q['key']=='kidfunfit-main')['content_status']=='empty_http202_body'
assert next(q for q in receipt['sources'] if q['key']=='hafs-notice')['content_status']=='html_notice_shell_zero_posts'
vr=receipt['visual_review'];assert vr['new_visual_pdf_checks']==20
for name,q in vr['documents'].items():
 assert hashlib.sha256((P/(name+'.pdf')).read_bytes()).hexdigest()==q['pdf_sha256']
 for page,sha in q['rendered_page_sha256'].items():assert hashlib.sha256((P/f'{name}-p{page}.png').read_bytes()).hexdigest()==sha
q=receipt['primary_reader_comparison'];raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
def portable(name,ext):
 m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
 assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
 with zipfile.ZipFile(io.BytesIO(raw)) as q:
  assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry']);assert m[ext+'_sha256'] in q.read('README.txt').decode()
 assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
 assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
 return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json');assert json.loads(js)==d
f=P/'verified-v112.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v111.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
allowed={'countries':{'SGP','PHL'},'metadata':{'completeness_audit','camp_focus','camp_planning'},'events':updated,'camp_programmes':{'CP676'}}
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
assert oa.keys()<=na.keys() and len(na)==2644 and len(na.keys()-oa.keys())==1
assert {k for k in oa if oa[k]!=na[k]}=={'stem-'+k+'@family-stem.local' for k in updated}
for k in oa:
 if oa[k]!=na[k]:assert {f for f in oa[k] if oa[k][f]!=na[k][f]}=={'DESCRIPTION'}
assert 'CP829' in next(iter(na.keys()-oa.keys())) and '10' in next(na[k]['SUMMARY'] for k in na.keys()-oa.keys())
name='dist/downloads/STEM_крупные_выставки.ics';assert calendar(prior(name))==calendar((ROOT/name).read_bytes()) and len(calendar((ROOT/name).read_bytes()))==104
for name in ['STEM_catalog.csv','STEM_календарь_2026_2027.csv','STEM_крупные_выставки.csv']:
 f=ROOT/'dist/downloads'/name
 if f.exists():
  oldrows=list(csv.DictReader(io.StringIO(prior('dist/downloads/'+name).decode('utf-8-sig'))));newrows=list(csv.DictReader(io.StringIO(f.read_text(encoding='utf-8-sig'))))
  missing=[r for r in oldrows if r not in newrows]
  assert all(any(ident in r.values() for ident in updated) for r in missing),name
plan=json.loads((ROOT/'data/research-plan.json').read_text());oldplan=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==112
assert {q['id'] for q in plan['requirements']}=={q['id'] for q in oldplan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==oldplan[k],k
assert plan['complete_database_download']==sm and plan['complete_json_download']==jm
assert d['coverage_summary']['fully_audited_countries']==0 and not plan['latest_validation']['worldwide_complete']
for stem in ['research-plan','asia-camps-audit-v112','asia-camps-source-receipts-v112']:
 assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for k in ['events','camp_programmes','camp_planning','league_guide']:assert web[k]==d[k]
html=(ROOT/'dist/index.html').read_text();assert 'data-ui-version="112"' in html and 'STEM_asia_camps_audit_v112.json' in html
for f in ROOT.joinpath('dist').rglob('*'):
 if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['data.js','camp-planning.js','camp-programmes.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['camp-planning.js','camp-programmes.css']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=112,old_event_ids_preserved=3419,old_event_objects_unchanged=3417,updated_event_ids=sorted(updated),new_event_ids=sorted(v.keys()-e.keys()),old_dossier_ids_preserved=827,old_dossier_objects_unchanged=826,new_dossiers=12,total_dossiers=839,complete_sqlite=True,complete_json=True,all17family_budget_offers_unchanged=True,family_ics=2644,exhibition_ics=104,goal='active',new_visual_pdf_checks=20)
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
