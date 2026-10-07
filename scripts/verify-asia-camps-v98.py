"""Independent preserved-content, programme-source and export verification."""
import collections,csv,datetime,hashlib,json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
from camp_asia_v98 import NEW
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v98'
BASE='c4a58064e7408f84e367bc4e427b77f653f2d024'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def tokens(key,*values):
    t=(PRIMARY/(key+'.txt')).read_text()
    for v in values:assert v in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
op={q['slug']:q for q in b['camp_programmes']['profiles']};p={q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3205 and len(old)==3184 and set(old)<=set(ev)
assert all(ev[k]==v for k,v in old.items())
new=[e for k,e in ev.items() if k not in old]
counts=collections.Counter(e['camp_dossier_slug'] for e in new)
assert counts=={'laurus-winter-prek':7,'laurus-winter-primary':1,'laurus-winter-secondary':1,
               'alv-taipei-winter':1,'alv-shilin-winter':1,'alv-banqiao-winter':1,'alv-kaohsiung-winter':1,
               'alv-manila-winter':1,'smis-jeju-winter':2,'tenten-clark-english':1,'tenten-clark-maths':1,'tenten-korea-six':1,'tenten-korea-speech':2}
assert all(e['start']>='2026-10-05' and e['end']>=e['start'] for e in new)
assert len(p)==680 and set(p)-set(op)==set(NEW)
assert [q['id'] for q in c['profiles'][:664]]==[q['id'] for q in b['camp_programmes']['profiles']]
assert [p[s]['id'] for s in NEW]==['CP%03d'%i for i in range(665,681)]
assert all(p[slug]==q for slug,q in op.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
assert c['counts']['countries']==37 and c['counts']['swiss']==86 and c['counts']['source_urls']==1066
assert c['shortlist'][:-4]==b['camp_programmes']['shortlist'] and c['gaps'][:-4]==b['camp_programmes']['gaps']
assert len(c['shortlist'])==158
for q in c['shortlist']:assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
assert sum(e['block']=='Лагеря' for e in ev.values())==1874 and len(c['generated_event_ids'])==1411
assert c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==42

tokens('laurus-index','Dec 14 (Mon) – Dec 18 (Fri)','¥85,000','¥100,000','¥104,000','separate entrance fee','all winter programmes are open to external students','ages 11–15')
tokens('laurus-prek-en','December 21 (Mon) – 25 (Fri), 2026','All-English Environment','¥13,000','¥17,000','¥6,000','¥5,000','¥1,000','¥740','December 14, 2026','Tuesday, December 15','Musashi-Shinjo','will not host Winter Camp','summer camp')
pre=p['laurus-winter-prek'];assert len(pre['timing']['sessions'])==7
assert all(v['deadline']=='2026-12-14' and v['attendance_weekdays']==['MO','TU','WE','TH','FR'] for v in pre['timing']['session_details'])
assert not any('shinjo' in v['variant_key'] for v in pre['timing']['session_details'])
assert pre['family_fit']['matvey']['status']=='not_eligible' and pre['family_fit']['oscar']['status']=='candidate'
assert p['laurus-winter-primary']['family_fit']['oscar']['status']=='conditional'
assert all(q['status']=='later' for q in p['laurus-winter-secondary']['family_fit'].values())
for s in ['taas-adventurer1','taas-adventurer2','taas-pathfinder']:
    assert p[s]['timing']['precision']=='season_window' and p[s]['timing']['sessions']==[['2027-07-05','2027-07-30']]
    assert not any(q['event_ids'] for q in p[s]['calendar_links'])
    assert p[s]['price']['year']==2026 and '2020' in p[s]['price']['deposit']
    assert p[s]['language_evidence_role']=='language_lessons'
    assert all(f['status']=='unknown' for f in p[s]['family_fit'].values())
tokens('taas-lv1','2026','1st & 2nd','41500','05.31.2026')
tokens('taas-lv2','3rd & 4th','41500');tokens('taas-lv3','5th & 6th','41500')
tokens('taas-policy','Valid date: March 1 – July 31, 2020','90%','70%')
tokens('taas-calendar','Summer School for 2027 is: July 5 - July 30')
visual=json.loads((PRIMARY/'visual-source-notes.json').read_text())
assert len(visual)==6 and sum(q['pages_visual_checked'] for q in visual)==24
for q in visual:
    f=PRIMARY/(q['key']+'.pdf');assert f.read_bytes().startswith(b'%PDF') and hashlib.sha256(f.read_bytes()).hexdigest()==q['pdf_sha256']
    for page in q['selected_pages_one_based']:assert (PRIMARY/f"{q['key']}-{page}.png").exists()
for s in ['alv-taipei-winter','alv-shilin-winter','alv-banqiao-winter','alv-kaohsiung-winter']:
    assert p[s]['timing']['sessions']==[['2027-01-25','2027-01-29']] and p[s]['confirmed_instruction_languages']==['EN']
    assert 'Grade 1–3' in p[s]['age'] and '10 300' in p[s]['price']['label'] and '16 680' in p[s]['price']['label']
    assert all(q['status']=='unknown' for q in p[s]['family_fit'].values())
assert 9800+500==10300 and 9800*.8+500==8340 and 2*8340==16680
assert p['alv-manila-winter']['timing']['sessions']==[['2027-01-23','2027-02-01']]
assert '7 nights' in p['alv-manila-winter']['timing']['label'] and 'не подписана NT$' in p['alv-manila-winter']['price']['label']
assert p['alv-manila-winter']['language_evidence_role']=='camp_life'
tokens('smis-jeju','2027.01.05 — 01.24','2027.01.27 — 02.15','390만원','초3 — 중2','2–4인','수업료 · 숙박비 · 식대','개인 용돈 10만원','원어민 ESL','AI · STEAM')
assert p['smis-jeju-winter']['language_evidence_role']=='language_lessons'
tokens('tenten','2027 겨울 모집 요강','예비 초4~중3','예비 초4~중1','530','510','710','410','99% English','한국식 영문법','여행자보험 · SSP','최종 금액과 할인 조건')
for s in ['tenten-clark-english','tenten-clark-maths']:
    a,z=p[s]['timing']['sessions'][0];assert (datetime.date.fromisoformat(z)-datetime.date.fromisoformat(a)).days+1==29
    assert p[s]['language_evidence_role']=='camp_life'
a,z=p['tenten-korea-speech']['timing']['sessions'][1];assert (datetime.date.fromisoformat(z)-datetime.date.fromisoformat(a)).days+1==20
for s in NEW:
    assert p[s]['confirmed_instruction_languages']==['EN']
    if s not in ['laurus-winter-prek','laurus-winter-primary','laurus-winter-secondary']:
        assert all(f['status']=='unknown' for f in p[s]['family_fit'].values())
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
for f,v in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/f).read_text())==v
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert {json.loads(v)['id']:json.loads(v) for v, in con.execute('SELECT record_json FROM events')}==ev
assert {json.loads(v)['slug']:json.loads(v) for v, in con.execute('SELECT record_json FROM camp_programmes')}==p
# Native publish rejected the original v98 SQLite file just over the file limit.
# Compare the complete logical dump to that pushed export, including every table
# and schema item, rather than only checking the new storage setting.
oldfile=PRIMARY.parent/'sqlite-size-v98/before-storage-optimisation.sqlite'
oldfile.write_bytes(subprocess.check_output(['git','show','a05df400e60292cc3ea46eea1379b6ab8d62b2a8:dist/downloads/STEM_database.sqlite'],cwd=ROOT))
oldcon=sqlite3.connect(oldfile)
def sqlhash(db):
    h=hashlib.sha256()
    for line in db.iterdump():h.update((line+'\n').encode())
    return h.hexdigest()
assert sqlhash(oldcon)==sqlhash(con),'All SQLite tables/schema/rows retained after storage optimisation'
oldcon.close();con.close()
assert all(f.stat().st_size<=26214400 for f in (ROOT/'dist').rglob('*') if f.is_file()),'Static hosting per-file limit'
assert len(list(csv.DictReader((ROOT/'dist/downloads/STEM_catalog.csv').read_text(encoding='utf-8-sig').splitlines())))==3205
md=(ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.md').read_text()
for s in NEW:assert p[s]['provider'] in md and p[s]['editorial_reason'] in md
def calendar(value):
    out={};t=value.decode().replace('\r\n ','').replace('\r\n\t','')
    for block in t.split('BEGIN:VEVENT')[1:]:
        f={s.split(':',1)[0]:s.split(':',1)[1] for s in block.split('END:VEVENT')[0].splitlines() if ':' in s};assert f['UID'] not in out;out[f['UID']]=f
    return out
oldcal=calendar(prior('dist/downloads/STEM_подтвержденные_даты.ics'))
now=calendar((ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes())
assert len(now)==2466 and set(oldcal)<=set(now)
for uid,v in oldcal.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
eligible=[e for e in new if e['camp_dossier_slug']!='laurus-winter-secondary']
assert len(eligible)==20
delta=set(now)-set(oldcal);baseuids={'stem-'+e['id']+'@family-stem.local' for e in eligible}
deadlines=delta-baseuids;assert len(deadlines)==1 and next(iter(deadlines)).endswith('-deadline@family-stem.local')
assert now[next(iter(deadlines))]['DTSTART;VALUE=DATE']=='20261214'
for e in eligible:
    f=now['stem-'+e['id']+'@family-stem.local'];assert f['DTSTART;VALUE=DATE']==e['start'].replace('-','')
    assert f['DTEND;VALUE=DATE']==(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d')
expo='dist/downloads/STEM_крупные_выставки.ics';oe=calendar(prior(expo));ne=calendar((ROOT/expo).read_bytes());assert len(ne)==104 and set(oe)==set(ne)
for uid,v in oe.items():assert {k:x for k,x in ne[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==98
assert {q['id'] for q in bp['requirements']}=={q['id'] for q in plan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==bp[k],k
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['asia-camp-audit-v98','asia-camp-source-receipts-v98']:
    v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
    assert not any(v['external_actions'].values())
    if 'sources' in v:
        assert len(v['sources'])==27 and len(v['dossier_source_urls_added'])==20
        assert sum(q.get('status')==200 for q in v['sources'])==24 and sum(bool(q.get('error')) for q in v['sources'])==3
        for q in v['sources']:
            if q.get('sha256'):assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_asia_camp_audit_v98.json' in js
assert 'data-ui-version="98"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(s for s in js.splitlines() if s.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:''};
FUNCTIONS
const fresh=new Set(NEW);const current=()=>new Set(filtered().filter(p=>fresh.has(p.slug)).map(p=>p.slug));
cs.child='both';let found=current();if(found.size!==1||!found.has('laurus-winter-primary'))throw Error('both');
cs.child='oscar';found=current();if(found.size!==2||!found.has('laurus-winter-primary')||!found.has('laurus-winter-prek'))throw Error('oscar');
cs.child='matvey';found=current();if(found.size!==1||!found.has('laurus-winter-primary'))throw Error('matvey');
cs.child='';cs.phase='2027';found=current();if(found.size!==13||[...found].some(s=>s.startsWith('laurus-')))throw Error('phase');
cs.phase='';cs.language='EN';found=current();if(found.size!==16)throw Error('language');
cs.language='ES';if(current().size)throw Error('falseES');cs.language='EN-support';if(current().size)throw Error('falseSupport');
cs.language='';cs.format='boarding';if(current().size!==6)throw Error('boarding');
cs.format='';cs.country='TWN';if(current().size!==7)throw Error('Taiwan');
""".replace('FUNCTIONS',funcs).replace('NEW',json.dumps(NEW))
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(verified=True,events=3205,dossiers=680,new_dossiers=16,new_calendar_rows=21,prior_events_unchanged=3184,prior_dossiers_unchanged=664,family_ics=2466,source_urls=1066,worldwide_complete=False)))
