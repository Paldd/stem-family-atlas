"""Independent primary evidence, age/price boundaries and full preservation."""
import hashlib,json,re,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v87'
BASE='d2451482d9480851f92ac41b9c9b48965f417adb'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def before(file):return subprocess.check_output(['git','show',BASE+':'+file],cwd=ROOT)
def raw(k):return (PRIMARY/(k+'.txt')).read_text()
def compact(s):return re.sub(r'\s+','',s)
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};events={e['id']:e for e in d['events']}
assert len(old)==2966 and len(events)==len(d['events'])==2975
assert all(events.get(k)==v for k,v in old.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
c=d['camp_programmes'];p={q['slug']:q for q in c['profiles']};op={q['slug']:q for q in b['camp_programmes']['profiles']}
assert len(op)==505 and len(p)==529 and all(p[k]==v for k,v in op.items())
assert c['profiles'][:505]==b['camp_programmes']['profiles']
assert c['counts']['countries']==35 and c['counts']['source_urls']==804 and c['counts']['swiss']==78
assert len(c['shortlist'])==115 and c['shortlist'][:111]==b['camp_programmes']['shortlist']
assert c['gaps'][:-4]==b['camp_programmes']['gaps']
assert all(len(s['slugs'])==len(set(s['slugs'])) and all(k in p for k in s['slugs']) for s in c['shortlist'][-4:])
new=[e for k,e in events.items() if k not in old]
assert len(new)==9 and {e['camp_dossier_slug'] for e in new}=={'sloane-day','sloane-board'}
assert sum(e['block']=='Лагеря' for e in events.values())==1644
assert len(c['generated_event_ids'])==1181 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==35
# Parse published rows independently, rather than reproducing author input.
t=raw('sloane-rates')
board=t.split('Two Week Sessions:',1)[1].split('One Week Session:',1)[0]
parsed=re.findall(r'Session (\d)\n([^\n]+)\n\$([\d,]+)\n\$([\d,]+)\n\$([\d,]+)',board)
assert [(n,period) for n,period,*_ in parsed]==[('1','June 27 - July 10'),('2','July 11 - 24'),('3','July 25 - August 7'),('4','August 8 - 21')]
assert all([int(x.replace(',','')) for x in row[2:]]==[3045,2795,2545] for row in parsed)
day=t.split('Day Camp (Rising K-6th Grade)',1)[1]
parsedday=re.findall(r'Session ([A-E])\n([^\n]+)\n\$([\d,]+)\n\$([\d,]+)\n\$([\d,]+)',day)
assert len(parsedday)==5
assert all([int(x.replace(',','')) for x in row[2:]]==([560,520,480] if row[0]=='E' else [1115,1040,965]) for row in parsedday)
sd=raw('sloane-day');assert all(x in sd for x in ['$1085','$1010','$935','$545','$505','$465'])
assert 'unable to be split' in sd and 'four 4-week' in sd and 'June 4 - July 10' in t
assert all(x in p['sloane-day']['price']['label'] for x in ['1 115','1 085','560','545'])
def pairs(slug):return {(e['start'],e['end']) for e in new if e['camp_dossier_slug']==slug}
assert pairs('sloane-board')=={('2027-06-27','2027-07-10'),('2027-07-11','2027-07-24'),('2027-07-25','2027-08-07'),('2027-08-08','2027-08-21')}
assert pairs('sloane-day')=={('2027-06-28','2027-07-09'),('2027-07-12','2027-07-23'),('2027-07-26','2027-08-06'),('2027-08-09','2027-08-20'),('2027-08-23','2027-08-27')}
assert all(e['start']!='2027-06-04' for e in new)
for e in new:
    assert e['languages']==['EN'] and e['language_mode']=='camp_life'
    if e['camp_dossier_slug']=='sloane-day':assert e['attendance_weekdays']==['MO','TU','WE','TH','FR'] and e['date_scope']=='day_camp_window'
si=raw('sloane-international');assert 'practice their English' in si and 'ONLY available to/from JFK or LaGuardia' in si and 'medical insurance' in si
dh=raw('sloane-day-handbook-layout');bh=raw('sloane-board-handbook-layout')
assert 'Monday-Friday' in dh and 'March 1st' in dh and 'May 1st' in bh
assert 'non-refundable after March 1st' in compact(dh).replace('non-refundableafter','non-refundable after') or 'Deposits are non-refundable after March 1st' in dh
assert 'physician documented medical cases' in dh and 'do not include health and accident insurance' in dh
assert 'robotics' not in p['sloane-day']['themes']
# Real grades remain unknown; English page/manual never promoted to instruction proof.
fresh=[q for s,q in p.items() if s not in op]
for q in fresh:
    if q['iso'] in ['USA','CAN']:
        assert all(v['status']=='unknown' for v in q['family_fit'].values())
        if not q['slug'].startswith('sloane-'):assert q['confirmed_instruction_languages']==[] and q['timing']['status']=='published_2026' and not q['timing']['sessions']
assert sum(q['iso']=='USA' for q in fresh)==15 and sum(q['iso']=='CAN' for q in fresh)==7 and sum(q['iso']=='MEX' for q in fresh)==2
assert all(x in compact(raw('berkeley-toy')) for x in ['Grades1','$1295','2026'])
assert 'hand-powered' in raw('berkeley-arcade') and 'Grades 3 & 4' in raw('berkeley-contraptions')
assert '$1,550' in raw('berkeley-nano') and '$1,350' in raw('berkeley-residential') and 1550+1350==2900
assert 'Friday, July 9' in raw('berkeley-nano') and '07/05/2026 - 07/10/2026' in raw('berkeley-residential')
assert '2900' in compact(p['berkeley-nano-board']['price']['label'])
cu=compact(raw('cu-raw'));assert all(compact(x) in cu for x in ['ROBOT PLAYGROUND','AI LAB','ARDUINO: AN INTRODUCTION','COMPUTER SCIENCE AND ROBOTICS','SparkFun XRP','take home your own Arduino kit'])
assert '2027' in raw('cu-summer') and 'December' in raw('cu-summer') 
assert 'minimum of 5 years' in raw('cu-parent-en-layout')
uw=raw('waterloo-summer');assert 'Fall 2026' in uw and 'Summer 2026 is now closed' in uw and '$362' in uw and '$290' in uw
assert 'Spike Prime' in raw('waterloo-discovery-b-layout') and 'Faraday' in raw('waterloo-discovery-b-layout')
assert 'automatically' not in p['waterloo-esq-discovery']['language'].lower()
assert '$25' in raw('waterloo-paid-policy') and 'May 29, 2026' in raw('waterloo-paid-policy')
assert '80%' in raw('western-faq') and 'at least 14 days' in raw('western-faq')
assert 'twice' in raw('western-themes') and 'does not include new content' in raw('western-themes')
mx=raw('mex-robotitos');assert 'Edades de 8 – 14' in mx and 'de 6 a 14' in mx and '$3000.00' in mx
assert p['robotitos-apaxco-summer']['price']['year'] is None and not p['robotitos-apaxco-summer']['timing']['sessions'] and p['robotitos-apaxco-summer']['family_fit']['oscar']['status']=='later'
assert 'no cuenta con sucursales ni imparte cursos o talleres de verano' in raw('robotix-faq') and 'no contamos con inscripciones individuales' in raw('robotix-faq')
# Integration, public files, SQLite and calendar preservation.
report=json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text());again=json.loads(json.dumps(d));integrate(again,report);assert again==d
for file,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/file).read_text())==wanted
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite');assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2975 and con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==529;con.close()
def calendar(v):
    out={};t=v.decode().replace('\r\n ','').replace('\r\n\t','')
    for ch in t.split('BEGIN:VEVENT')[1:]:
        f={line.split(':',1)[0]:line.split(':',1)[1] for line in ch.split('END:VEVENT')[0].splitlines() if ':' in line};assert f['UID'] not in out;out[f['UID']]=f
    return out
for file,total,previous in [('STEM_подтвержденные_даты.ics',2249,2240),('STEM_крупные_выставки.ics',104,104)]:
    f='dist/downloads/'+file;prior=calendar(before(f));now=calendar((ROOT/f).read_bytes());assert len(prior)==previous and len(now)==total and set(prior)<=set(now)
    for uid,v in prior.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
    if total==2249:
        assert set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in new}
        for e in new:
            f=now['stem-'+e['id']+'@family-stem.local'];assert e['start'].replace('-','') in str(f)
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==87
assert {q['id'] for q in bp['requirements']}<={q['id'] for q in plan['requirements']}
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert plan['camp_catalog_integration']['dossiers']==529 and d['coverage_summary']['fully_audited_countries']==0
for stem in ['americas-camp-audit-v87','americas-camp-source-receipts-v87']:
    val=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==val
    assert not any(val['external_actions'].values())
    if 'sources' in val:
        assert len(val['sources'])==44 and len(val['visual_primary_reads'])==4 and len(val['image_sources'])==2
        for v in val['sources']:
            if v.get('status')==200:assert hashlib.sha256((PRIMARY/v['raw_filename']).read_bytes()).hexdigest()==v['sha256']
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_americas_camp_audit_v87.json' in js and 'STEM_asia_camp_audit_v86.json' in js
assert 'data-ui-version="87"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
print(json.dumps(dict(verified=True,events=2975,dossiers=529,new_dossiers=24,new_dated_rows=9,family_ics=2249,source_urls=804,worldwide_complete=False)))
