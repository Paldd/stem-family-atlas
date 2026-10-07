"""Independent source clauses, prior-record preservation and interactive filters."""
import collections,csv,datetime,hashlib,json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
from camp_asia_v105 import NEW
ROOT=Path(__file__).resolve().parents[1];PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v105'
BASE='17bed4437b7ae7b932ee0f1f67245116c80d960e'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def tokens(key,*values):
    t=' '.join((PRIMARY/(key+'.txt')).read_text().split())
    for v in values:assert ' '.join(v.split()) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
op={q['slug']:q for q in b['camp_programmes']['profiles']};p={q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3323 and len(old)==3309 and set(old)<=set(ev)
assert all(ev[k]==v for k,v in old.items())
new=[e for k,e in ev.items() if k not in old]
assert collections.Counter(e['camp_dossier_slug'] for e in new)=={'hcc-korea-winter':1,'traidhos-winter-english':5,'traidhos-junior-nature':2,'fcis-winter-boarding':3,'fcis-winter-day':3}
assert collections.Counter(e['iso'][0] for e in new)=={'KOR':1,'THA':7,'MYS':6}
assert all(e['end']>='2026-10-05' and e['end']>=e['start'] and not e['deadline'] for e in new)
assert len(p)==769 and set(p)-set(op)==set(NEW) and len(NEW)==11
assert all(p[s]==v for s,v in op.items())
assert [q['id'] for q in c['profiles'][:758]]==[q['id'] for q in b['camp_programmes']['profiles']]
assert [p[s]['id'] for s in NEW]==['CP%03d'%i for i in range(759,770)]
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
assert c['counts']['countries']==39 and c['counts']['swiss']==106 and c['counts']['source_urls']==1203
assert c['shortlist'][:-4]==b['camp_programmes']['shortlist'] and c['gaps'][:-6]==b['camp_programmes']['gaps']
assert len(c['shortlist'])==178 and len(c['gaps'])==179
for q in c['shortlist']:assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
assert sum(e['block']=='Лагеря' for e in ev.values())==1992 and len(c['generated_event_ids'])==1529
assert c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==49
tokens('hcc-winter','4~9학년','₩3,000,000','2026년 12월 21일부터 2027년 1월 2일까지')
tokens('crimson-partners','THE PRINCETON REVIEW WRITING AND LEADERSHIP CAMP','Co-hosted by The Harvard Crimson and The Princeton Review','SEOUL, KOREA','9TH-12TH GRADE')
assert all(p['hcc-korea-winter']['family_fit'][x]['status']=='later' for x in ['matvey','oscar'])
assert ev['CP759-20261221-20270102']['attendance_weekdays']==[] if 'attendance_weekdays' in ev['CP759-20261221-20270102'] else True
tokens('edventure-winter-faq','Will the off-mountain activities and lessons be conducted in English?','all our MnK guest services are conducted in English','day camp only','3 day consecutive program')
tokens('edventure-winter','December 12, 2026 - January 9, 2027','February 1, 2027 - February 17, 2027')
tokens('edventure-terms','14 to 7 days','20%','¥10,000 per child','¥5,000 per change','100%')
tokens('edventure-summer','Summer Camp 2026','Summer Camp 2027 is open')
tokens('edventure-family','One parent per child joins daily activities','Parents provide transportation for all activities','¥4,900','camp is in English')
tokens('edventure-residential','9 years and up','6 nights & 7 days','10–12 years old','up to four campers','All meals are included')
for s in ['edventure-summer-family','edventure-yotei-residential']:
    assert p[s]['timing']['sessions']==[] and p[s]['price']['year'] is None
tokens('nbs-price','14th December 2026 to 28th February 2027','¥24,000','¥23,000','¥105,000','Qualified, English','5 day minimum')
tokens('nbs-terms','must be toilet trained','Minimum age for children in group snowboard lessons is 8','Lift tickets must be purchased','Cancellation 14-7 days = 50% fee','website supersedes all print content')
for s,windows in [('edventure-winter-club',2),('nbs-niseko-kids',1)]:
    assert p[s]['timing']['precision']=='season_window' and len(p[s]['calendar_links'])==windows
    assert all(q['kind']=='season_window' and q['event_ids']==[] for q in p[s]['calendar_links'])
tokens('nac-programme','July 27 - 31','August 17 - 21','￥75,000','￥40,000','Raft Building','Maximum 20 kids')
tokens('nac-day','August 17 (Mon.) – August 19 (Wed.)','2026')
assert p['nac-niseko-day']['price']['year']==2026 and p['nac-niseko-day']['confirmed_instruction_languages']==[] and p['nac-niseko-day']['timing']['sessions']==[]
tokens('imagine-hokkaido','150,000','2026','6.5','English')
tokens('imagine-terms','Imagine credit','12-48 hours','full refund')
assert p['imagine-hokkaido-summer']['language_evidence_role']=='partial_bilingual' and p['imagine-hokkaido-summer']['price']['year']==2026 and not p['imagine-hokkaido-summer']['timing']['sessions']
tokens('traidhos-winter','9 - 14','THB 33,000','31 January – 6 February 2027','7 – 13 February 2027','14 – 20 February 2027','21 – 27 February 2027','Sibling as well as multi-week discounts are not applicable')
tokens('traidhos-faq','English Camp teachers are fully-qualified English speakers','illness is not covered','1 staff to 10 campers','Counsellors sleep in adjoining rooms')
for s in ['traidhos-nature-wonder','traidhos-nature-everywhere']:tokens(s,'4 – 8','THB 12,000','2 snacks / day','Winter Day Camp 2026')
assert p['traidhos-junior-nature']['confirmed_instruction_languages']==[] and p['traidhos-junior-nature']['family_fit']['matvey']['status']=='not_eligible'
tokens('fcis-winter','Ages 10–15 (born 2011–2017)','Ages 7–15 (born 2011–2020)','RM 19,000','RM 10,000','RM 14,000','RM 7,000','12 December 2026','22 January–4 February','native-speaking teachers','Prime Camp')
assert p['fcis-winter-boarding']['family_fit']['oscar']['status']=='not_eligible'
assert p['fcis-winter-day']['family_fit']['oscar']['status']=='conditional'
assert len(p['fcis-winter-boarding']['timing']['session_details'])==3 and len(p['fcis-winter-day']['timing']['session_details'])==3
tokens('campasia-book','Oct 19-23','Robotics Makerspace','$725.00','Ages 6-8')
pdfmeta=subprocess.check_output(['pdfinfo',str(PRIMARY/'campasia-dec3.pdf')]).decode();assert '2018' in pdfmeta and 'Pages:           13' in pdfmeta
tokens('campasia-dec3','LEGO Robotics (WeDo)','Wednesday','Thursday','Friday')
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
for f,v in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/f).read_text())==v
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite');assert con.execute('PRAGMA page_size').fetchone()[0]==1024
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert {json.loads(v)['id']:json.loads(v) for v, in con.execute('SELECT record_json FROM events')}==ev
assert {json.loads(v)['slug']:json.loads(v) for v, in con.execute('SELECT record_json FROM camp_programmes')}==p
oldfile=PRIMARY/'baseline.sqlite';oldfile.write_bytes(prior('dist/downloads/STEM_database.sqlite'));oc=sqlite3.connect(oldfile)
schema=lambda db:sorted(db.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"))
assert schema(oc)==schema(con)
for name, in oc.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
    rows=set(oc.execute('SELECT * FROM "'+name+'"'));now=set(con.execute('SELECT * FROM "'+name+'"'))
    if name not in ['metadata','countries']:assert rows<=now,name
    elif name=='metadata':assert {r[0] for r in rows-now}=={'completeness_audit','camp_focus'}
    else:
        delta=rows-now;assert {r[0] for r in delta}<={'JPN','KOR','THA','MYS'}
        for r in delta:
            q=con.execute('SELECT * FROM countries WHERE iso=?',(r[0],)).fetchone();assert r[:3]==q[:3]
oc.close();con.close()
assert all(f.stat().st_size<=26214400 for f in (ROOT/'dist').rglob('*') if f.is_file()),'Static per-file limit'
rows=lambda raw:{r['id']:r for r in csv.DictReader(raw.decode('utf-8-sig').splitlines())}
path='dist/downloads/STEM_catalog.csv';oldcsv=rows(prior(path));newcsv=rows((ROOT/path).read_bytes());assert len(newcsv)==3323 and all(newcsv[k]==v for k,v in oldcsv.items())
md=(ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.md').read_text()
for s in NEW:assert p[s]['provider'] in md and p[s]['editorial_reason'] in md
def calendar(value):
    out={};t=value.decode().replace('\r\n ','').replace('\r\n\t','')
    for block in t.split('BEGIN:VEVENT')[1:]:
        f={s.split(':',1)[0]:s.split(':',1)[1] for s in block.split('END:VEVENT')[0].splitlines() if ':' in s};assert f['UID'] not in out;out[f['UID']]=f
    return out
path='dist/downloads/STEM_подтвержденные_даты.ics';oldcal=calendar(prior(path));now=calendar((ROOT/path).read_bytes())
assert len(now)==2577 and len(oldcal)==2564 and set(oldcal)<=set(now)
for uid,v in oldcal.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
family=[e for e in new if e['camp_dossier_slug']!='hcc-korea-winter']
assert set(now)-set(oldcal)=={'stem-'+e['id']+'@family-stem.local' for e in family}
for e in family:
    f=now['stem-'+e['id']+'@family-stem.local'];assert f['DTSTART;VALUE=DATE']==e['start'].replace('-','')
    assert f['DTEND;VALUE=DATE']==(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d') and f['STATUS']=='TENTATIVE'
expo='dist/downloads/STEM_крупные_выставки.ics';oe=calendar(prior(expo));ne=calendar((ROOT/expo).read_bytes());assert len(ne)==104 and set(oe)==set(ne)
for uid,v in oe.items():assert {k:x for k,x in ne[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==105
assert {q['id'] for q in bp['requirements']}=={q['id'] for q in plan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==bp[k],k
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['asia-camp-audit-v105','asia-camp-source-receipts-v105']:
    v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
    assert not any(v['external_actions'].values())
    if 'sources' in v:
        assert len(v['sources'])==32 and len(v['dossier_source_urls_added'])==23 and sum(q.get('status')==200 for q in v['sources'])==31
        for q in v['sources']:
            if q.get('status')==200:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_asia_camp_audit_v105.json' in js
assert 'data-ui-version="105"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(s for s in js.splitlines() if s.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:''};
FUNCTIONS
const fresh=new Set(NEW);const result=()=>new Set(filtered().filter(p=>fresh.has(p.slug)).map(p=>p.slug));
const check=(names)=>{const a=result(),b=new Set(names);if(a.size!==b.size||[...a].some(s=>!b.has(s)))throw Error(JSON.stringify([...a]));};
check(NEW);cs.language='EN';check(NEW.filter(s=>!['nac-niseko-day','traidhos-junior-nature'].includes(s)));
cs.language='ES';check([]);cs.language='';cs.child='both';check(['edventure-winter-club','edventure-summer-family','nbs-niseko-kids','nac-niseko-day','imagine-hokkaido-summer','fcis-winter-day']);
cs.phase='2027';check(['edventure-winter-club','nbs-niseko-kids','fcis-winter-day']);
cs.phase='';cs.child='';cs.country='KOR';check(['hcc-korea-winter']);cs.country='THA';check(['traidhos-winter-english','traidhos-junior-nature']);
cs.country='MYS';check(['fcis-winter-boarding','fcis-winter-day']);
console.log('family/language/year/country filters passed');
""".replace('FUNCTIONS',funcs).replace('NEW',json.dumps(NEW))
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
print(json.dumps(dict(status='passed',version=105,new_dossiers=11,new_calendar_rows=14,new_family_ics=13,new_season_windows=3,dossiers=769,countries=39,source_urls=1203,events=3323,camp_learning_records=1992,goal='active'),ensure_ascii=False))
