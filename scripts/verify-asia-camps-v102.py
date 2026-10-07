"""Independent source clauses, old-record preservation and calendar/filter audit."""
import collections,csv,datetime,hashlib,json,re,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
from camp_asia_v102 import NEW
ROOT=Path(__file__).resolve().parents[1];PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v102'
BASE='54610f96af67effeba81351194db4aaa61d08fdf'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def tokens(key,*values):
    t=' '.join((PRIMARY/(key+'.txt')).read_text().split())
    for v in values:assert ' '.join(v.split()) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
op={q['slug']:q for q in b['camp_programmes']['profiles']};p={q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3274 and len(old)==3255 and set(old)<=set(ev)
assert all(ev[k]==v for k,v in old.items())
new=[e for k,e in ev.items() if k not in old]
assert collections.Counter(e['camp_dossier_slug'] for e in new)=={'dulwich-lita-festive':2,'dulwich-finland-winter':3,'harrow-hk-ecobot':1,'harrow-hk-sleigh':1,'harrow-guangzhou-auto':1,'harrow-myoko-ski':1,'jasmine-build':1,'jasmine-shop':1,'jasmine-discovery':1,'jasmine-micro':1,'jasmine-nola':5,'jasmine-winter-block':1}
assert collections.Counter(e['iso'][0] for e in new)=={'CHN':3,'FIN':3,'HKG':2,'JPN':1,'TWN':10}
assert all(e['end']>='2026-10-05' and e['end']>=e['start'] and not e['deadline'] for e in new)
assert len(p)==730 and set(p)-set(op)==set(NEW) and len(NEW)==23
assert all(p[s]==v for s,v in op.items())
assert [q['id'] for q in c['profiles'][:707]]==[q['id'] for q in b['camp_programmes']['profiles']]
assert [p[s]['id'] for s in NEW]==['CP%03d'%i for i in range(708,731)]
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
assert c['counts']['countries']==39 and c['counts']['swiss']==99 and c['counts']['source_urls']==1132
assert c['shortlist'][:-4]==b['camp_programmes']['shortlist'] and c['gaps'][:-5]==b['camp_programmes']['gaps']
assert len(c['shortlist'])==168
for q in c['shortlist']:assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
assert sum(e['block']=='Лагеря' for e in ev.values())==1943 and len(c['generated_event_ids'])==1480
assert c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==42
tokens('dulwich-camps','Y5–Y7 / G4–G6','3–5 October 2026','3–7 October 2026','RMB 6,500','RMB 10,800','Maximum 30 students','11–17 years','19–24 December / 26–31 December 2026','RMB 14,800','RMB 12,850','English as the main language','RMB 40,800','domestic flights within Finland','parent-child participation')
assert not p['dulwich-ai-film']['timing']['sessions']
assert len(p['dulwich-lita-festive']['timing']['sessions'])==2 and all(p['dulwich-lita-festive']['family_fit'][k]['status']=='later' for k in ['matvey','oscar'])
assert len(p['dulwich-finland-winter']['timing']['sessions'])==3 and p['dulwich-finland-winter']['formats']==['family']
tokens('ycyw-primary','Ages 6-14','Students in Y1-8','10800 RMB','Students in G4-12','RMB 10,960','RMB 12,100','RMB 14,660','RMB 15,280','same price as internal student','VEX-IQ','13800 RMB','Students in G4-9')
tokens('ycyw-index','Open to all students aged 2-18','bilingual environment')
for s in ['ycis-beijing-vex','ywies-beijing-vexiq','ywies-tongxiang-vex']:
    assert p[s]['confirmed_instruction_languages']==[] and not p[s]['timing']['sessions']
assert p['ycis-shanghai-english']['language_evidence_role']=='language_lessons'
tokens('mandarin-inn','English','Mandarin','Lunch','3,800','7,220','10,260','12,920','1:6','missed days cannot be rescheduled')
assert not p['mandarininn-shanghai']['timing']['sessions'] and p['mandarininn-shanghai']['family_fit']['oscar']['status']=='later'
tokens('tinycode-home','English Instruction','15 June to 28 August 2026','HKD 5,280','HKD 3,432','per student','Ages 6–8','Ages 7–11','Ages 8–12','8–10','10 and above','All hardware provided','16‑class learning roadmap','ChatGPT API')
tokens('tinycode-terms','Last Updated: April 2026','full payment','No refunds will be issued','seven (7) days','No more than one (1) class','Typhoon Signal No. 8')
assert 3432*2==6864 and 5280*2==10560
for s in ['tinycode-scratch','tinycode-robot','tinycode-games','tinycode-ai']:assert not p[s]['timing']['sessions'] and p[s]['price']['year']==2026
tokens('harrow-ecobot','21–24 December 2026','6-8 years old','HK$8,980.00','Healthy lunches each day, plus snacks','English','9:00 AM – 4:00 PM')
tokens('harrow-sleigh','21–24 December 2026','9-12 years','HK$8,980.00','basic level of English','Healthy lunches each day, plus snacks')
tokens('harrow-auto','21-26 December 2026','8-13 years','HK$12,500.00','Harrow Guangzhou','Three healthy meals','Public Liability Insurance','English','electric racing kart')
tokens('harrow-ski','21-26 December 2026','10-16 years','HK$23,800.00','5 nights','equipment rental','Helmet rental','Narita or Haneda','winter sports','Personal ski clothing','emergency evacuation','1:5 Student-to-Staff Ratio')
tokens('harrow-policies','30 September 2026','40% refund','4% administrative','1 November 2026','1 October 2026','all fees paid are non-refundable','local phone number','No change of booking will be offered')
offers=json.loads((PRIMARY/'public-offer-notes.json').read_text());assert len(offers)==4
for q in offers:
    h=(PRIMARY/(q['key']+'.html')).read_bytes();assert hashlib.sha256(h).hexdigest()==q['source_sha256']
    v=json.loads(re.findall('<script type="application/ld\\+json">(.*?)</script>',h.decode(),re.S)[-1])
    assert v['offers']==q['offers'] and all(x['availability']=='http://schema.org/InStock' and x['priceCurrency']=='HKD' for x in q['offers'])
    assert '"available":true' in h.decode()
assert all(p['harrow-myoko-ski']['family_fit'][k]['status']=='later' for k in ['matvey','oscar'])
assert p['harrow-guangzhou-auto']['iso']=='CHN' and p['harrow-hk-ecobot']['iso']=='HKG'
tokens('tc-home','Ages 9–15','5 days, 4 nights','2027 pre-booking open')
tokens('tc-2027','NT$1,000','7 天','費用還沒公布','不是全美語課')
tokens('tc-camp','NT$20,900','NT$17,500','2026/8/22–8/26','公共意外險')
assert not p['tc-city-ambassador']['timing']['sessions'] and p['tc-city-ambassador']['price']['year']==2026
tokens('jasmine','Grades mean the school year your child is attending at the time of registration','2027-07-05','2027-08-06','NT$13,800','NT$19,800','including breakfast, excluding dinner','NT$4,500','one designated English-speaking support contact','primarily in Mandarin')
tokens('jasmine-calendar','含住宿合計 NT$21,300','報名當下正在就讀的年級','午餐、晚餐由孩子使用自己的零用金購買','2 天遊覽車','不重複收費')
tokens('jasmine-build','2027/7/5–7/9','國小 2–4','不用','英文','木片')
tokens('jasmine-shop','價格怎麼訂、庫存怎麼算','用中文講','午餐、材料與保險已含','每件 300','整梯 1,000','NT$13,800')
tokens('jasmine-discovery','國小 4 年級–國一','NT$13,800','用中文','讓別人試','3 位外籍老師')
tokens('jasmine-micro','2027/8/2–8/6','國小 2–4','NT$13,800','同桌','用中文','每個孩子有自己的顯微鏡')
tokens('jasmine-block','2027/1/21–1/22','國小 1–5','NT$6,800','NT$6,300','2026/10/16','不教程式','不必自備電腦或平板','午餐與保險已含','兩天梯次不販售整梯延時接送方案')
assert 13800+6000==19800 and 16800+4500==21300 and 12600+600==13200
assert p['jasmine-nola']['confirmed_instruction_languages']==[] and p['jasmine-nola']['confirmed_support_languages']==['EN']
for s in ['jasmine-build','jasmine-shop','jasmine-discovery','jasmine-micro','jasmine-winter-block']:
    assert p[s]['language_evidence_role']=='partial_bilingual' and p[s]['family_fit']['oscar']['status']=='unknown'
assert len(p['jasmine-nola']['timing']['sessions'])==5 and not any(e['deadline']=='2026-10-16' for e in new)
for key in ['korea-ltl','ltl-japan','ltl-taiwan']:tokens(key,'2027 BOOKINGS OPEN','7 to 11-year-olds','11 to 17-year-olds','12 to 17-year-olds')
tokens('kdw-program','SEPTEMBER / OCTOBER 2026','Lunch & snacks provided','August 31st','Bishan')
assert not any(s.startswith(('ltl-','aseeder-','kdw-')) for s in NEW)
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
        delta=rows-now;assert {r[0] for r in delta}=={'CHN','HKG','FIN','JPN','TWN'}
        for r in delta:
            q=con.execute('SELECT * FROM countries WHERE iso=?',(r[0],)).fetchone();assert r[:3]==q[:3]
oc.close();con.close()
assert all(f.stat().st_size<=26214400 for f in (ROOT/'dist').rglob('*') if f.is_file()),'Static per-file limit'
rows=lambda raw:{r['id']:r for r in csv.DictReader(raw.decode('utf-8-sig').splitlines())}
path='dist/downloads/STEM_catalog.csv';oldcsv=rows(prior(path));newcsv=rows((ROOT/path).read_bytes());assert len(newcsv)==3274 and all(newcsv[k]==v for k,v in oldcsv.items())
md=(ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.md').read_text()
for s in NEW:assert p[s]['provider'] in md and p[s]['editorial_reason'] in md
def calendar(value):
    out={};t=value.decode().replace('\r\n ','').replace('\r\n\t','')
    for block in t.split('BEGIN:VEVENT')[1:]:
        f={s.split(':',1)[0]:s.split(':',1)[1] for s in block.split('END:VEVENT')[0].splitlines() if ':' in s};assert f['UID'] not in out;out[f['UID']]=f
    return out
path='dist/downloads/STEM_подтвержденные_даты.ics';oldcal=calendar(prior(path));now=calendar((ROOT/path).read_bytes())
assert len(now)==2530 and len(oldcal)==2514 and set(oldcal)<=set(now)
for uid,v in oldcal.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
family=[e for e in new if e['camp_dossier_slug'] not in ['dulwich-lita-festive','harrow-myoko-ski']]
assert set(now)-set(oldcal)=={'stem-'+e['id']+'@family-stem.local' for e in family}
for e in family:
    f=now['stem-'+e['id']+'@family-stem.local'];assert f['DTSTART;VALUE=DATE']==e['start'].replace('-','')
    assert f['DTEND;VALUE=DATE']==(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d') and f['STATUS']=='TENTATIVE'
expo='dist/downloads/STEM_крупные_выставки.ics';oe=calendar(prior(expo));ne=calendar((ROOT/expo).read_bytes());assert len(ne)==104 and set(oe)==set(ne)
for uid,v in oe.items():assert {k:x for k,x in ne[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==102
assert {q['id'] for q in bp['requirements']}=={q['id'] for q in plan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==bp[k],k
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['asia-camp-audit-v102','asia-camp-source-receipts-v102']:
    v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
    assert not any(v['external_actions'].values())
    if 'sources' in v:
        assert len(v['sources'])==33 and len(v['dossier_source_urls_added'])==21
        assert sum(q.get('status')==200 for q in v['sources'])==31
        for q in v['sources']:
            if q.get('status')==200:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_asia_camp_audit_v102.json' in js
assert 'data-ui-version="102"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(s for s in js.splitlines() if s.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:''};
FUNCTIONS
const fresh=new Set(NEW);const result=()=>new Set(filtered().filter(p=>fresh.has(p.slug)).map(p=>p.slug));
const check=(names)=>{const a=result(),b=new Set(names);if(a.size!==b.size||[...a].some(s=>!b.has(s)))throw Error(JSON.stringify([...a]));};
check(NEW);cs.language='EN';check(NEW.filter(s=>!['ycis-beijing-vex','ywies-beijing-vexiq','ywies-tongxiang-vex','jasmine-nola'].includes(s)));
cs.language='EN-support';check(['jasmine-build','jasmine-shop','jasmine-discovery','jasmine-micro','jasmine-nola','jasmine-winter-block']);
cs.language='';cs.child='both';check(['dulwich-finland-winter','tinycode-scratch','tinycode-robot','harrow-hk-ecobot']);
cs.phase='2027';check(['dulwich-finland-winter']);cs.child='';cs.language='EN';check(['dulwich-finland-winter','tc-city-ambassador','jasmine-build','jasmine-shop','jasmine-discovery','jasmine-micro','jasmine-winter-block']);
cs.language='';cs.phase='';cs.country='CHN';check(['dulwich-ai-film','dulwich-lita-festive','ycis-shanghai-english','ycis-beijing-vex','ywies-beijing-vexiq','ywies-tongxiang-vex','mandarininn-shanghai','harrow-guangzhou-auto']);
cs.country='HKG';check(['tinycode-scratch','tinycode-robot','tinycode-games','tinycode-ai','harrow-hk-ecobot','harrow-hk-sleigh']);
console.log('family/language/support/year/country filter verification passed');
""".replace('FUNCTIONS',funcs).replace('NEW',json.dumps(NEW))
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(status='passed',version=102,new_dossiers=23,new_calendar_rows=19,new_family_ics=16,dossiers=730,countries=39,source_urls=1132,events=3274,camp_learning_records=1943,goal='active'),ensure_ascii=False))
