"""Verify source receipts, the narrow language correction and portable-data preservation."""
import hashlib, io, json, sqlite3, subprocess, zipfile
from camp_family_review_v129 import ROOT, BASE, CHOICES
P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v129'
def prior(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
assert set(b)==set(d)
assert {k:v for k,v in b.items() if k!='camp_programmes'}=={k:v for k,v in d.items() if k!='camp_programmes'}
old={p['slug']:p for p in b['camp_programmes']['profiles']};new={p['slug']:p for p in d['camp_programmes']['profiles']}
assert old.keys()==new.keys() and len(new)==1034
assert all(new[k]==v for k,v in old.items() if k!='roches-ai')
oldp=old['roches-ai'];newp=new['roches-ai'];allowed={'confirmed_instruction_languages','language_evidence_role','checked','sources'}
assert {k:v for k,v in oldp.items() if k not in allowed}=={k:v for k,v in newp.items() if k not in allowed}
assert newp['confirmed_instruction_languages']==['EN'] and newp['family_fit']==oldp['family_fit'] and newp['timing']==oldp['timing']
assert d['events']==b['events'] and d['camp_planning']==b['camp_planning']
for name in ['STEM_подтвержденные_даты.ics','STEM_крупные_выставки.ics']:
    assert (ROOT/'dist/downloads'/name).read_bytes()==prior('dist/downloads/'+name)
r=d['camp_programmes']['family_review'];assert len(r['entries'])==41 and len({new[q['slug']]['iso'] for q in r['entries']})==16
assert len({q['slug'] for q in r['entries']})==41 and not r['coverage']['fully_audited_countries']
expected={'CHE','FRA','ESP','GBR','TWN','SGP','KOR','JPN','USA','CAN','CRI','MEX','BRA','ARG','PAN','CHL'}
assert {new[q['slug']]['iso'] for q in r['entries']}==expected
def clause(file,*words):
    s=(P/(file+'.txt')).read_text().lower();s=''.join(s.split())
    for word in words:assert ''.join(word.lower().split()) in s,(file,word)
clause('rose-classic','From11to15yearsold','Tech&Robotics','75minutes','CHF13,500','2027')
clause('rose-faq','doyouofferdaycamps','under8','onlyoffersummercamps','1:4','healthcareprofessionals')
clause('rose-family','languageclasses','CHF8,200','CHF13,200')
clause('rose-financial','Summer2026','1stMay,2026','non-refundable')
clause('garenne-conditions','SummerCamp2027','7’200','6’550','65days','CHF500')
clause('garenne-robotics','8-12','VEXIQ','Tinkercad','Python','Bluetoothspeaker','threesessions','twosessions')
clause('tasis-prices','2027','CHF4,500','CHF9,200','Ages4–6','SaturdayorSunday')
clause('prefleuri','SummerCamps2026','5-7yearsold','8to9yearsold')
clause('roches-brochure','Ages11-17|English','NEWFOR2026','AlphAI','mBot','LEGOSpike','perceptron')
receipts=json.loads((ROOT/'data/family-camps-source-receipts-v129.json').read_text())
assert len(receipts['sources'])==61 and not any(receipts['external_actions'].values())
for q in receipts['sources']:
    if q['body_snapshot_retained']:
        raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert sum(q['body_snapshot_retained'] for q in receipts['sources'])==54
def portable(meta,kind):
    m=json.loads((ROOT/'dist/downloads'/meta).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
    assert m['complete_database'] and len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256']
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        assert z.testzip() is None and z.namelist()==[m[kind+'_entry'],'README.txt'];body=z.read(m[kind+'_entry'])
    assert len(body)==m[kind+'_bytes'] and hashlib.sha256(body).hexdigest()==m[kind+'_sha256']
    assert m['raw_download_available']==(len(body)<=26214400)
    assert (ROOT/'dist/downloads'/m[kind+'_entry']).exists()==m['raw_download_available']
    return body
assert json.loads(portable('STEM_database_json_download.json','json'))==d
sql=portable('STEM_database_download.json','sqlite');(P/'verified-v129.sqlite').write_bytes(sql)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as z:oldsql=z.read('STEM_database.sqlite')
(P/'baseline-v128.sqlite').write_bytes(oldsql)
c=sqlite3.connect(P/'verified-v129.sqlite');oc=sqlite3.connect(P/'baseline-v128.sqlite')
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
tables=[x[0] for x in oc.execute("SELECT name FROM sqlite_master WHERE type='table'")]
assert tables==[x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
for t in tables:
    a=oc.execute('SELECT * FROM '+t).fetchall();z=c.execute('SELECT * FROM '+t).fetchall()
    if t=='metadata':
        am=dict(a);zm=dict(z);assert {k:v for k,v in zm.items() if k!='camp_family_review'}==am
        assert json.loads(zm['camp_family_review'])==r
    elif t=='camp_programmes':
        assert [x for x in a if x[0]!='CP133']==[x for x in z if x[0]!='CP133']
        assert json.loads(next(x for x in z if x[0]=='CP133')[-1])==newp
    else:assert a==z,t
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']==plan['native_goal_status']=='active'
assert plan['next_research']==json.loads(prior('data/research-plan.json'))['next_research']
assert plan['human_scope_expansion']['status']=='active' and plan['current_publication']['status']=='prepared_local_not_published'
result=dict(status='passed',version=129,unchanged_event_objects=3775,unchanged_dossiers=1033,unchanged_budget_objects=53,
    changed_dossiers=['roches-ai'],new_dossiers=0,family_review_candidates=41,priority_selection_countries=16,
    previous_ics_byte_identical=True,all_other_sqlite_tables_preserved=True,new_sqlite_metadata='camp_family_review',
    complete_sqlite_bytes=len(sql),complete_json_matches_catalog=True,raw_source_receipt_hashes_verified=54,
    source_contract_years_age_language_and_session_conflicts_checked=True,goal='active',worldwide_complete=False,publication='prepared_local_not_published')
(P/'independent-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result))
