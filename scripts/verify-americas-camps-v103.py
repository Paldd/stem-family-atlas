"""Independent source, complete old-record preservation and interactive-filter verification."""
import collections,csv,datetime,hashlib,json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
from camp_americas_v103 import NEW
ROOT=Path(__file__).resolve().parents[1];PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v103'
BASE='2ea55367db46f906261caeba97825a2a13d2b93d'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def tokens(key,*values):
    t=' '.join((PRIMARY/(key+'.txt')).read_text().split())
    for v in values:assert ' '.join(v.split()) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
op={q['slug']:q for q in b['camp_programmes']['profiles']};p={q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3287 and len(old)==3274 and set(old)<=set(ev)
assert all(ev[k]==v for k,v in old.items())
new=[e for k,e in ev.items() if k not in old]
assert collections.Counter(e['camp_dossier_slug'] for e in new)=={'pipiol-summer-one':1,'pipiol-summer-two':1,'techknow-pokemon':2,'techknow-minecraft':2,'langmobile-younger':7}
assert collections.Counter(e['iso'][0] for e in new)=={'MEX':2,'USA':4,'CAN':7}
assert all(e['end']>='2026-10-05' and e['end']>=e['start'] and not e['deadline'] for e in new)
assert len(p)==745 and set(p)-set(op)==set(NEW) and len(NEW)==15
assert all(p[s]==v for s,v in op.items())
assert [q['id'] for q in c['profiles'][:730]]==[q['id'] for q in b['camp_programmes']['profiles']]
assert [p[s]['id'] for s in NEW]==['CP%03d'%i for i in range(731,746)]
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
assert c['counts']['countries']==39 and c['counts']['swiss']==99 and c['counts']['source_urls']==1158
assert c['shortlist'][:-3]==b['camp_programmes']['shortlist'] and c['gaps'][:-4]==b['camp_programmes']['gaps']
assert len(c['shortlist'])==171
for q in c['shortlist']:assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
assert sum(e['block']=='Лагеря' for e in ev.values())==1956 and len(c['generated_event_ids'])==1493
assert c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==46
tokens('kupugani','Camp Kupugani is permanently closed','Swift Nature Camp')
tokens('swift-home','ages 6-15')
tokens('holland-description','A formal diagnosis must be provided','provide their own 1:1 support')
tokens('holland-winter','Winter 2027','Junior Robotics','January 20 to February 24, 2027','Snow Makeup Day: March 3, 2027')
tokens('holland-march','March Break 2027','Monday March 15 - Friday March 19, 2027','Fee: $475 + HST','8–14 years of age','45-minute')
assert not any(s.startswith(('kupugani','swift-','holland-','rooted-')) for s in NEW)
tokens('pipiol-one','Verano 1, 2027','4 al 17 de julio','6 a 16 años','$84,000 pesos')
tokens('pipiol-two','Verano 2, 2027','19 al 31 de julio','6 a 16 años','$78,400 pesos')
tokens('pipiol-home','4 a 17 años','7 y 15 años','no se permiten celulares','MiniKids')
tokens('pipiol-contract','Tres alimentos diarios','cuando así se estipule','30 días naturales','20 días naturales','30%','menor a 20 días','20 días hábiles','archivos audiovisuales')
assert 84000*2==168000 and 78400*2==156800
assert all(p[s]['confirmed_instruction_languages']==[] for s in ['pipiol-summer-one','pipiol-summer-two'])
tokens('bc-mexico','Summer 2026','100% en inglés','6 a 11 años','MXN 5,096','MXN 9,479','MXN 13,148','MXN 16,307','MXN 20,384','22 de junio','9:15 - 13:30')
assert not p['bc-mexico-innovators']['timing']['sessions'] and p['bc-mexico-innovators']['price']['year']==2026
tokens('science-world-knowledge','Camps admission is based on year of birth','2020','2016 & 2017','Grades are only provided as a guideline','basic proficiency in English','Only book one camp of each type','$35 admin fee')
tokens('science-world-summer','June 29 – September 4, 2026','no camp on July 2','no camp on July 7','$474.95','$549.95','$384.95','$439.95','$25 for 5-day camps','$20 for 4-day camps')
tokens('science-world-field','July 6 – August 28, 2026','8:30am – 3:00pm','$369.95 – $524.95','Grades 2 – 3','Grades 4 – 5')
tokens('science-world-winter','returning Fall 2026','In the past few years')
assert all(not p[s]['timing']['sessions'] for s in ['sw-little-wonders','sw-curious-creators','sw-field-science'])
assert p['sw-little-wonders']['family_fit']['matvey']['status']=='not_eligible' and p['sw-curious-creators']['family_fit']['oscar']['status']=='not_eligible'
tokens('techknow-home','December 22, 2025')
tokens('techknow-winter','Winter 2026','Ages 6-9','Ages 5-8','Codey Rocky')
tokens('techknow-pricing','25%','December 4, 2026','before December 1, 2026','$25 processing fee','through September 2027','90% refund and a 10% credit')
tokens('techknow-glen','395 Addison Street','Dec 21 - Dec 24','Pokemon LEGO Masters','Dec 28 - Dec 31','Minecraft Big Builders','$465/wk','$105/week')
tokens('techknow-sunset','999 Brotherhood Way','Dec 21 - Dec 23','Minecraft Big Builders','Dec 28 - Dec 30','Pokemon LEGO Masters','$355/wk','$80/week')
tokens('techknow-modern-faq','maximum of 20 students','2-3 teachers','max of 9:1','own building kits and computers','bring his/her own lunch')
assert 2*(465+105)==1140
for s in ['techknow-pokemon','techknow-minecraft']:
    assert p[s]['confirmed_instruction_languages']==[] and len(p[s]['timing']['session_details'])==2
    for v in p[s]['timing']['session_details']:
        assert ('395 Addison Street' if v['variant_key']=='glen' else '999 Brotherhood Way') in v['place']
tokens('laurus-summer','Ages 5–11','75-Minute','11 Activity Categories','131 Bloor St W','Dates, pricing, and schedules are coming soon')
tokens('laurus','7 STAs','Full bilingual + French Immersion Camp')
tokens('roboiq-camp','English, Math, Robotics','18 Crown Steel Dr','9005 Leslie St','Opening In Progress')
assert p['laurus-youth']['language_evidence_role']=='partial_bilingual' and p['roboiq-holidays']['language_evidence_role']=='language_lessons'
assert not p['laurus-youth']['timing']['sessions'] and not p['roboiq-holidays']['timing']['sessions']
tokens('eli-montreal','12 to 17 years old','15 language lessons per week','July 4, 2027','August 1, 2027')
tokens('eli-brochure','Junior Students (Ages 12-13)','15 weekly lessons','One wash and dry per week','July 4, 2027','August 1, 2027')
tokens('eli-handbook','University of Toronto, Victoria Campus','Ages 7–11','June 27 – August 15, 2027','45 minutes per lesson','No classes on July 1 & August 2','no formal classes','non-refundable registration deposit of $250','21 days prior','14 calendar days','ages 14–17')
tokens('eli-toronto','Senior students aged 15 and older','June 27, 2027','August 15, 2027')
tokens('eli-family','English classes for parents are completely optional','children 7 years of age or older','child younger than seven','final package and price will depend')
for s in ['eli-toronto-primary','eli-montreal-junior','eli-toronto-family','langmobile-older']:
    assert p[s]['timing']['precision']=='season_window' and all(x['kind']=='season_window' for x in p[s]['calendar_links'])
lang=json.loads((PRIMARY/'langmobile-web-fresh.json').read_text())
for v in ['Summer 2027','June 28 – July 2','August 9 – August 13','2027 Programming to be announced soon','305$ / Week','5 to 12 years old','100% English']:assert v in lang,v
assert p['langmobile-younger']['age']=='5–6' and p['langmobile-younger']['family_fit']['matvey']['status']=='later'
assert len(p['langmobile-younger']['timing']['sessions'])==7 and p['langmobile-younger']['timing']['sessions'][-1][1]=='2027-08-13'
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
        delta=rows-now;assert {r[0] for r in delta}=={'MEX','USA','CAN'}
        for r in delta:
            q=con.execute('SELECT * FROM countries WHERE iso=?',(r[0],)).fetchone();assert r[:3]==q[:3]
oc.close();con.close()
assert all(f.stat().st_size<=26214400 for f in (ROOT/'dist').rglob('*') if f.is_file()),'Static per-file limit'
rows=lambda raw:{r['id']:r for r in csv.DictReader(raw.decode('utf-8-sig').splitlines())}
path='dist/downloads/STEM_catalog.csv';oldcsv=rows(prior(path));newcsv=rows((ROOT/path).read_bytes());assert len(newcsv)==3287 and all(newcsv[k]==v for k,v in oldcsv.items())
md=(ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.md').read_text()
for s in NEW:assert p[s]['provider'] in md and p[s]['editorial_reason'] in md
def calendar(value):
    out={};t=value.decode().replace('\r\n ','').replace('\r\n\t','')
    for block in t.split('BEGIN:VEVENT')[1:]:
        f={s.split(':',1)[0]:s.split(':',1)[1] for s in block.split('END:VEVENT')[0].splitlines() if ':' in s};assert f['UID'] not in out;out[f['UID']]=f
    return out
path='dist/downloads/STEM_подтвержденные_даты.ics';oldcal=calendar(prior(path));now=calendar((ROOT/path).read_bytes())
assert len(now)==2543 and len(oldcal)==2530 and set(oldcal)<=set(now)
for uid,v in oldcal.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
assert set(now)-set(oldcal)=={'stem-'+e['id']+'@family-stem.local' for e in new}
for e in new:
    f=now['stem-'+e['id']+'@family-stem.local'];assert f['DTSTART;VALUE=DATE']==e['start'].replace('-','')
    assert f['DTEND;VALUE=DATE']==(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d') and f['STATUS']=='TENTATIVE'
expo='dist/downloads/STEM_крупные_выставки.ics';oe=calendar(prior(expo));ne=calendar((ROOT/expo).read_bytes());assert len(ne)==104 and set(oe)==set(ne)
for uid,v in oe.items():assert {k:x for k,x in ne[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==103
assert {q['id'] for q in bp['requirements']}=={q['id'] for q in plan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==bp[k],k
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['americas-camp-audit-v103','americas-camp-source-receipts-v103']:
    v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
    assert not any(v['external_actions'].values())
    if 'sources' in v:
        assert len(v['sources'])==44 and len(v['dossier_source_urls_added'])==26 and sum(q.get('status')==200 for q in v['sources'])==36
        for q in v['sources']:
            if q.get('status')==200:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
        for q in v['web_reader_fallbacks']:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_americas_camp_audit_v103.json' in js
assert 'data-ui-version="103"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(s for s in js.splitlines() if s.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:''};
FUNCTIONS
const fresh=new Set(NEW);const result=()=>new Set(filtered().filter(p=>fresh.has(p.slug)).map(p=>p.slug));
const check=(names)=>{const a=result(),b=new Set(names);if(a.size!==b.size||[...a].some(s=>!b.has(s)))throw Error(JSON.stringify([...a]));};
check(NEW);cs.language='EN';check(['bc-mexico-innovators','sw-little-wonders','sw-curious-creators','sw-field-science','laurus-youth','roboiq-holidays','eli-toronto-primary','eli-montreal-junior','eli-toronto-family','langmobile-younger','langmobile-older']);
cs.language='ES';check([]);cs.language='';cs.child='both';check(['pipiol-summer-one','pipiol-summer-two','bc-mexico-innovators','techknow-pokemon','techknow-minecraft','laurus-youth','eli-toronto-primary','eli-toronto-family','langmobile-older']);
cs.phase='2027';check(['pipiol-summer-one','pipiol-summer-two','laurus-youth','eli-toronto-primary','eli-toronto-family','langmobile-older']);
cs.phase='';cs.child='';cs.country='MEX';check(['pipiol-summer-one','pipiol-summer-two','bc-mexico-innovators']);
cs.country='USA';check(['techknow-pokemon','techknow-minecraft']);console.log('family/language/year/country filters passed');
""".replace('FUNCTIONS',funcs).replace('NEW',json.dumps(NEW))
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(status='passed',version=103,new_dossiers=15,new_calendar_rows=13,new_family_ics=13,dossiers=745,countries=39,source_urls=1158,events=3287,camp_learning_records=1956,goal='active'),ensure_ascii=False))
