"""Check source clauses, family gates and complete preservation of the previous Atlas."""
import collections,csv,hashlib,io,json,re,sqlite3,subprocess,zipfile
from camp_asia_v116 import ROOT,BASE,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-asia-primary-v116'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clauses(key,*values,compact=False):
    raw=(P/(key+'.txt')).read_text()
    norm=(lambda t:re.sub(r'\s+','',t)) if compact else (lambda t:' '.join(t.split()))
    for v in values:assert norm(v) in norm(raw),(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'asof','events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={p['slug']:p for p in b['camp_programmes']['profiles']};z={p['slug']:p for p in d['camp_programmes']['profiles']}
assert len(a)==874 and len(z)==883 and set(z)-set(a)==set(NEW)
assert [s for s in a if z[s]!=a[s]]==UPDATED and len({p['id'] for p in z.values()})==883
assert d['camp_programmes']['shortlist'][:207]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==211
assert d['camp_programmes']['gaps'][:226]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==233
e={q['id']:q for q in b['events']};v={q['id']:q for q in d['events']}
assert len(e)==3543 and e.keys()<=v.keys() and all(e[k]==v[k] for k in e) and len(v)-len(e)==10
assert collections.Counter(q['block'] for q in v.values())=={'Соревнования':1153,'События':189,'Лагеря':2211}
oldsrc={s['url']:s for s in b['sources']};newsrc={s['url']:s for s in d['sources']}
assert all(newsrc[u]==s for u,s in oldsrc.items())
assert d['camp_planning']['offers'][:24]==b['camp_planning']['offers'] and len(d['camp_planning']['offers'])==27
assert len({q['slug'] for q in d['camp_planning']['offers']})==19
for slug in NEW:
    p=z[slug]
    assert p['checked']=='2026-10-06' and all(s['checked']=='2026-10-06' for s in p['sources'])
    assert p['confirmed_instruction_languages']==([] if slug==NEW[8] else ['EN']),slug
    assert len(p['timing']['sessions'])==len(p['calendar_links'])
assert sum(len(z[s]['timing']['sessions']) for s in NEW)==10
for slug in [NEW[1],NEW[7],NEW[8]]:assert not z[slug]['timing']['sessions']
assert z[NEW[0]]['language_evidence_role']=='camp_life'
assert z[NEW[4]]['language_evidence_role']=='language_lessons'
assert z[NEW[7]]['language_evidence_role']=='bilingual'
assert all(x['family_fit']['oscar']['status']=='later' for x in [z[NEW[3]],z[NEW[4]]])
assert all(x['family_fit'][child]['status']=='later' for x in [z[NEW[5]],z[NEW[6]]] for child in ['matvey','oscar'])
assert z[NEW[2]]['family_fit']['oscar']['status']=='conditional'
assert z[NEW[0]]['timing']['sessions'][1]==['2026-12-21','2026-12-24']
clauses('beaumont-book','Magic 21 Dec - 24 Dec, 9am - 3pm','Active 21 Dec - 24 Dec, 9am - 3pm','SGD 110.00')
clauses('beaumont-nexus','20 hours of immersive English learning','New Camp Dates Will Be Announced Soon!')
clauses('beaumont-faq','Lunch is ONLY provided during Summer Camps','7 working days','good level of English')
clauses('beaumont-sg-terms-pdf','SG$ 20 per child per day','SG$ 100 per child per week','3.5%','seven days','not an insurance product',compact=True)
clauses('dcamps-winter-early1','2027.01.04(월) ~ 01.08(금)','초등학교 4-6학년','초등학교 1-6학년','989,000원','1,790,000원','9/18일까지만')
clauses('dcamps-winter-day','2027. 01. 11 (월) ~ 01. 15 (금)','09:00 - 14:30')
clauses('dcamps-winter-board','2인 1실','주간 근무(09:00-21:00) / 야간 대기(21:00- 익일 09:00)')
clauses('dcamps-faq','단, 안전과 관련된 부분은 모국어인 한국어로 안내합니다.','초등 1~3학년','초등 4~6학년')
clauses('dcamps-curriculum','Ringbit Car with Microbit','Codable LEGO','Artificial Intelligence:')
clauses('gamja-jeju','2027년 1월 27일','2월 15일 (4주)','390만원','초등학교 3학년')
clauses('isak-summer','July 18th, 2027 - July 31st, 2027 (14 days)','3850 USD / 600,000 JPY','December 7th 2026 through 31st January, 2027','April 25th, 2026')
clauses('isak-winter','December 26-30, 2026','1380 USD','¥2,000','October 13th, 2026','Application closes on October 21.')
clauses('mit-summer','Chinese in the morning','3 hours of focussed English immersion','12,500 NTD/wk','5% sibling discount','Current elementary grades 1-6')
clauses('mit-terms','request the ½ refund','a single week','government-mandated closures')
clauses('mit-winter','Specialist Chinese Instructors','Grades 1-6')
clauses('tis-summer','we will not be offering the TIS Summer Programme in 2026','Looking Forward to 2027')
offers={q['id']:q for q in d['camp_planning']['offers']}
assert sum(offers['beaumont-sg-five']['base_by_child'].values())==1100
assert sum(offers['beaumont-sg-four']['base_by_child'].values())==880
assert offers['beaumont-sg-five']['optional'][0]['amount']==200 and offers['beaumont-sg-four']['optional'][0]['amount']==160
assert offers['dcamps-daewon-matvey']['base_by_child']=={'matvey':989000}
assert offers['dcamps-daewon-matvey']['children']==['matvey']
receipt=json.loads((ROOT/'data/asia-camps-source-receipts-v116.json').read_text())
assert len(receipt['sources'])==36 and sum(q.get('status')==200 for q in receipt['sources'])==32
assert not any(receipt['external_actions'].values())
for q in receipt['sources']:
    if q['body_snapshot_retained']:
        raw=(P/q['raw_filename']).read_bytes()
        assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert sum(q.get('raw_filename','').endswith('.pdf') for q in receipt['sources'])==3
vr=receipt['visual_review'];assert vr['new_visual_pdf_checks']==8 and vr['pdf_pages_text_extracted']==13
for key,pages in vr['rendered_pages'].items():
    for page in pages:assert (P/f'{key}-{page}.png').stat().st_size>0
def portable(name,ext):
    m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
    assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
    with zipfile.ZipFile(io.BytesIO(raw)) as q:
        assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt']
        body=q.read(m[ext+'_entry']);assert m[ext+'_sha256'] in q.read('README.txt').decode()
    assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
    assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
    return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json')
assert json.loads(js)==d
f=P/'verified-v116.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v115.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"))
assert schema(c)==schema(o)
allowed={'countries':{'SGP','KOR','JPN'},'metadata':{'completeness_audit','camp_focus','camp_planning'}}
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
    aa=set(o.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'))
    assert {r[0] for r in aa-zz}==allowed.get(name,set()),name
    assert {r[0] for r in aa}<={r[0] for r in zz},name
assert {q['id']:q for q in d['events']}=={k:json.loads(value) for k,value in c.execute('SELECT id,record_json FROM events')}
assert {q['slug']:q for q in d['camp_programmes']['profiles']}=={k:json.loads(value) for k,value in c.execute('SELECT slug,record_json FROM camp_programmes')}
assert json.loads(c.execute("SELECT value FROM metadata WHERE key='camp_planning'").fetchone()[0])==d['camp_planning']
c.close();o.close()
def calendar(raw):
    t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
    for s in t.split('BEGIN:VEVENT')[1:]:
        f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v}
        f.pop('DTSTAMP',None);assert f['UID'] not in out;out[f['UID']]=f
    return out
name='dist/downloads/STEM_подтвержденные_даты.ics';oa=calendar(prior(name));na=calendar((ROOT/name).read_bytes())
assert len(oa)==2760 and oa.keys()<=na.keys() and len(na)==2768 and all(oa[k]==na[k] for k in oa)
newuids=na.keys()-oa.keys();assert len(newuids)==8
assert all(any(z[s]['id'] in uid for s in NEW[:1]+NEW[2:5]) for uid in newuids)
assert not any(z[s]['id'] in uid for s in NEW[5:7] for uid in na)
name='dist/downloads/STEM_крупные_выставки.ics'
assert calendar(prior(name))==calendar((ROOT/name).read_bytes()) and len(calendar((ROOT/name).read_bytes()))==104
for name in ['STEM_catalog.csv','STEM_календарь_2026_2027.csv','STEM_крупные_выставки.csv']:
    f=ROOT/'dist/downloads'/name
    if f.exists():
        oldrows=list(csv.DictReader(io.StringIO(prior('dist/downloads/'+name).decode('utf-8-sig'))))
        newrows=list(csv.DictReader(io.StringIO(f.read_text(encoding='utf-8-sig'))))
        assert all(r in newrows for r in oldrows),name
plan=json.loads((ROOT/'data/research-plan.json').read_text());oldplan=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==116
assert {q['id'] for q in plan['requirements']}=={q['id'] for q in oldplan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==oldplan[k],k
assert plan['complete_database_download']==sm and plan['complete_json_download']==jm
assert d['coverage_summary']['fully_audited_countries']==0 and not plan['latest_validation']['worldwide_complete']
for stem in ['research-plan','asia-camps-audit-v116','asia-camps-source-receipts-v116']:
    assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for k in ['events','camp_programmes','camp_planning','league_guide']:assert web[k]==d[k]
assert 'data-ui-version="116"' in (ROOT/'dist/index.html').read_text()
for f in ROOT.joinpath('dist').rglob('*'):
    if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['data.js','camp-planning.js','camp-programmes.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['camp-planning.js','camp-programmes.css']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=116,old_event_objects_unchanged=3543,new_calendar_records=10,
    old_dossier_objects_unchanged=874,new_dossiers=9,total_dossiers=883,complete_sqlite=True,complete_json=True,
    old24budget_offers_unchanged=True,new_partial_budget_scenarios=3,family_ics=2768,exhibition_ics=104,
    future_uwc_excluded_from_current_family_ics=True,no_free_oscar_assumed=True,new_visual_pdf_checks=8,goal='active')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
