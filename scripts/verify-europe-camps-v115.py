"""Verify primary clauses, preserve all prior objects and check complete portable exports."""
import collections,csv,hashlib,io,json,re,sqlite3,subprocess,zipfile
from camp_europe_v115 import ROOT,BASE,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v115'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):
    return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clauses(key,*values,compact=False):
    raw=(P/(key+'.txt')).read_text()
    norm=(lambda t:re.sub(r'\s+','',t)) if compact else (lambda t:' '.join(t.split()))
    for v in values:
        assert norm(v) in norm(raw),(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'asof','events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={p['slug']:p for p in b['camp_programmes']['profiles']};z={p['slug']:p for p in d['camp_programmes']['profiles']}
assert len(a)==861 and len(z)==874 and set(z)-set(a)==set(NEW)
assert [s for s in a if z[s]!=a[s]]==UPDATED and len({p['id'] for p in z.values()})==874
assert d['camp_programmes']['shortlist'][:203]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==207
assert d['camp_programmes']['gaps'][:220]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==226
e={q['id']:q for q in b['events']};v={q['id']:q for q in d['events']}
assert len(e)==3490 and e.keys()<=v.keys() and all(e[k]==v[k] for k in e) and len(v)-len(e)==53
assert collections.Counter(q['block'] for q in v.values())=={'Соревнования':1153,'События':189,'Лагеря':2201}
oldsrc={s['url']:s for s in b['sources']};newsrc={s['url']:s for s in d['sources']}
assert all(newsrc[u]==s for u,s in oldsrc.items())
assert d['camp_planning']['offers'][:17]==b['camp_planning']['offers'] and len(d['camp_planning']['offers'])==24
assert len({q['slug'] for q in d['camp_planning']['offers']})==17
for slug in NEW:
    p=z[slug]
    assert p['checked']=='2026-10-06' and all(q['checked']=='2026-10-06' for q in p['sources'])
    assert p['confirmed_instruction_languages']==([] if slug in [NEW[2],NEW[5],NEW[6]] else ['EN']),slug
    assert p['id'] not in {q['id'] for q in a.values()}
    assert len(p['timing']['sessions'])==len(p['calendar_links'])
assert sum(len(z[slug]['timing']['sessions']) for slug in NEW)==55
for slug in NEW[:2]:
    assert z[slug]['timing']['precision']=='season_window'
    assert all(not q['event_ids'] and q['kind']=='season_window' for q in z[slug]['calendar_links'])
for slug in NEW[7:10]:
    assert z[slug]['timing']['sessions']==[] and z[slug]['timing']['status']=='archive_next_unannounced'
assert z[NEW[4]]['family_fit']['oscar']['status']=='later'
for slug in NEW[5:7]:
    assert all(q['status']=='unknown' for q in z[slug]['family_fit'].values())
startrows=[q for q in v.values() if q['id'] not in e and q['date_scope']=='activity_start']
assert len(startrows)==27 and all(q['start']==q['end'] for q in startrows)
assert all(q['attendance_weekdays']==[] for slug in NEW[11:] for q in z[slug]['timing']['session_details'])
clauses('prefleuri-winter-flyer','Du10.01.2027au19.03.2027','séjourminimumde2semaines','15heures',compact=True)
clauses('prefleuri-winter-conditions','CHF6’750','CHF24’400','Aucuncoursdelanguenicoursacadémiquessurcettepériode',compact=True)
clauses('prefleuri-paris-conditions','CHF2’500','CHF4’000','AlleretretourCHF350',compact=True)
clauses('academicus-winter','15.02-19.02.2027','22.02 - 26.02.2027','785CHF','Maximum 7 participants','conducted entirely in English')
clauses('academicus-autumn-real','12.10-16.10.2026','Maximum 8 participants','785CHF')
clauses('frilingue-winter','17.01 / 24.01 / 31.01 / 07.02 / 14.02 / 21.02 / 28.02.2027','1200 CHF','8-17','12 hours')
clauses('frilingue-family','FAMILY WORKATION: 500 CHF','FAMILY CAMP: 800 CHF','20 December 2026 to 16 January 2027','Unfortunately it\'s not possible to register your kid(s) on this page.')
clauses('frilingue-terms','13 to 7 days','80 %','7 to 1 day(s)','100 %','24-month guarantee','does not, however, guarantee 24-hour supervision')
clauses('lamiranda-real-handbook-retry','Bornin2018,2018&2019','Bornin2013,2014&2015','25thJune-18thJuly','312€',compact=True)
clauses('lamiranda-real-terms','depósito de 150€','29 de mayo de 2026','que sean alumnos del colegio')
clauses('malherbe-autumn-programme','confidentinreadingandwritinginEnglish','Morningsonly(9am-12pm):280€',compact=True)
clauses('living-holidays','Dates de l’année 2026-2027','du 19/10 au 30/10','du 05/07 au 23/07','enseignants de langue maternelle anglaise','fermés à Noël et en août')
clauses('living-2027-fees','Année scolaire 2026-2027','358,40 €','37,60 €','396 €','240 €','2ème enfant : -10%')
offers={q['id']:q for q in d['camp_planning']['offers']}
assert sum(offers['prefleuri-winter-two']['base_by_child'].values())==13500
assert sum(offers['prefleuri-ski-one']['base_by_child'].values())+offers['prefleuri-ski-one']['optional'][0]['amount']==5700
assert sum(offers['academicus-week']['base_by_child'].values())==1570
assert sum(offers['living-full']['base_by_child'].values())==792 and offers['living-full']['discount_second']==0
assert offers['living-half']['discount_second']==0
receipt=json.loads((ROOT/'data/europe-camps-source-receipts-v115.json').read_text())
assert len(receipt['sources'])==38 and sum(q.get('status')==200 for q in receipt['sources'])==32
assert not any(receipt['external_actions'].values())
for q in receipt['sources']:
    if q['body_snapshot_retained']:
        raw=(P/q['raw_filename']).read_bytes()
        assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert sum(q.get('raw_filename','').endswith('.pdf') for q in receipt['sources'])==8
vr=receipt['visual_review'];assert vr['new_visual_pdf_checks']==21 and vr['pdf_pages_text_extracted']==34
for key,pages in vr['rendered_pages'].items():
    for page in pages:
        f=P/f'{key}-p{page}.png'
        if not f.exists():f=P/f'{key}-{page}.png'
        assert f.stat().st_size>0

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
f=P/'verified-v115.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v114.sqlite';f.write_bytes(oldsql);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"))
assert schema(c)==schema(o)
allowed={'countries':{'CHE','FRA'},'metadata':{'completeness_audit','camp_focus','camp_planning'}}
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
assert len(oa)==2707 and oa.keys()<=na.keys() and len(na)==2760 and len(na.keys()-oa.keys())==53
assert all(oa[k]==na[k] for k in oa)
for row in startrows:
    f=na['stem-'+row['id']+'@family-stem.local']
    assert 'Начало' in f['SUMMARY'] and f['DTSTART;VALUE=DATE']==row['start'].replace('-','')
assert all(any(z[slug]['id'] in uid for slug in NEW) for uid in na.keys()-oa.keys())
name='dist/downloads/STEM_крупные_выставки.ics'
assert calendar(prior(name))==calendar((ROOT/name).read_bytes()) and len(calendar((ROOT/name).read_bytes()))==104
for name in ['STEM_catalog.csv','STEM_календарь_2026_2027.csv','STEM_крупные_выставки.csv']:
    f=ROOT/'dist/downloads'/name
    if f.exists():
        oldrows=list(csv.DictReader(io.StringIO(prior('dist/downloads/'+name).decode('utf-8-sig'))))
        newrows=list(csv.DictReader(io.StringIO(f.read_text(encoding='utf-8-sig'))))
        assert all(r in newrows for r in oldrows),name
plan=json.loads((ROOT/'data/research-plan.json').read_text());oldplan=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==115
assert {q['id'] for q in plan['requirements']}=={q['id'] for q in oldplan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:
    assert plan[k]==oldplan[k],k
assert plan['complete_database_download']==sm and plan['complete_json_download']==jm
assert d['coverage_summary']['fully_audited_countries']==0 and not plan['latest_validation']['worldwide_complete']
for stem in ['research-plan','europe-camps-audit-v115','europe-camps-source-receipts-v115']:
    assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for k in ['events','camp_programmes','camp_planning','league_guide']:assert web[k]==d[k]
html=(ROOT/'dist/index.html').read_text();assert 'data-ui-version="115"' in html and 'STEM_europe_camps_audit_v115.json' in html
for f in ROOT.joinpath('dist').rglob('*'):
    if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['data.js','camp-planning.js','camp-programmes.js']:
    subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['camp-planning.js','camp-programmes.css']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=115,old_event_objects_unchanged=3490,new_calendar_records=53,
            old_dossier_objects_unchanged=861,new_dossiers=13,total_dossiers=874,complete_sqlite=True,complete_json=True,
            old17family_budget_offers_unchanged=True,new_partial_budget_scenarios=7,family_ics=2760,exhibition_ics=104,
            explicit_start_markers=27,new_visual_pdf_checks=21,goal='active')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
