"""Independent preservation, source-body, eligibility and portable-export checks."""
import collections,datetime,hashlib,json,re,sqlite3,subprocess,csv,io
from pathlib import Path
from camp_catalog_bridge import integrate
from camp_americas_v97 import NEW
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v97'
BASE='18bf9653ad5e00376ba303b9d2994f1873cb0603'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def tokens(key,*values):
    t=(PRIMARY/(key+'.txt')).read_text()
    for v in values:assert v in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
op={q['slug']:q for q in b['camp_programmes']['profiles']};p={q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3184 and len(old)==3153 and set(old)<=set(ev)
assert all(ev[k]==v for k,v in old.items())
new=[e for k,e in ev.items() if k not in old]
assert len(new)==31 and collections.Counter(e['camp_dossier_slug'] for e in new)=={'pali-general':9,'pali-mini':9,'wenonah-regular':6,'wenonah-one':4,'wenonah-five':1,'wenonah-wee':1,'calgary-winter':1}
assert all(e['start']>='2026-10-05' and not e['deadline'] for e in new)
assert len(p)==664 and set(p)-set(op)==set(NEW)
assert [q['id'] for q in c['profiles'][:645]]==[q['id'] for q in b['camp_programmes']['profiles']]
assert [p[s]['id'] for s in NEW]==['CP%03d'%i for i in range(646,665)]
assert all(p[slug]==q for slug,q in op.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
assert c['counts']['countries']==37 and c['counts']['swiss']==86 and c['counts']['source_urls']==1046
assert c['shortlist'][:-4]==b['camp_programmes']['shortlist'] and c['gaps'][:-4]==b['camp_programmes']['gaps']
assert len(c['shortlist'])==154
for q in c['shortlist']:assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
assert sum(e['block']=='Лагеря' for e in ev.values())==1853 and len(c['generated_event_ids'])==1390
assert c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==39

# Dates/grades/fees are checked against retained independent public-source reads.
tokens('pali-dates','2027 Dates','June 13 - June 19','August 8 - August 14','7 day, 6 night','no added fees')
tokens('pali-news','Mini Camp is growing for Summer 2027','all 9 summer sessions')
tokens('pali-mini','ages 6 to 8','four day, three night','13-16','8-11','three staff members for up to nine')
tokens('pali-faq','$150 per week','2/1/2027: 100% refund','3/1/2027: 75% refund','4/1/2027: 50% refund')
tokens('pali-spanish','verano de 2023','hablar inglés');tokens('pali-russian','лета 2023 года')
tokens('pali-robotics','Ages 8-16','VEXcode','Autonomous Navigation','distance and color sensing')
assert len(p['pali-general']['timing']['sessions'])==len(p['pali-mini']['timing']['sessions'])==9
assert p['pali-general']['family_fit']['matvey']['status']=='candidate' and p['pali-general']['family_fit']['oscar']['status']=='later'
assert p['pali-mini']['family_fit']['matvey']['status']=='not_eligible' and p['pali-mini']['family_fit']['oscar']['status']=='candidate'
assert not p['pali-robotics']['timing']['sessions'] and not p['pali-robotics']['calendar_links']
assert all(not p[s]['confirmed_instruction_languages'] for s in ['pali-general','pali-mini','pali-robotics'])
assert 'не найден' in p['pali-mini']['price']['label'] and 'Mini' in p['pali-general']['price']['label']
for s,days in [('pali-general',7),('pali-mini',4)]:
    for a,z in p[s]['timing']['sessions']:assert (datetime.date.fromisoformat(z)-datetime.date.fromisoformat(a)).days+1==days
web=(PRIMARY/'wenonah-web-tool-evidence.txt').read_text()
for t in ['December 31, 2027','13% HST','July 4 – 31','August 30 – September 3','August 30 – September 1','$6350','$3650','$1960','$ 1300','$500','$75 for WEEnonah','Deposit of $100','October 1, 2026','all program instruction is in English','cannot promise this','within 18 months']:assert t in web,t
for s in ['wenonah-regular','wenonah-one','wenonah-five','wenonah-wee']:assert p[s]['confirmed_instruction_languages']==['EN'] and 'валюта' in p[s]['price']['label']
assert all(v['status']=='candidate' for v in p['wenonah-five']['family_fit'].values())
assert p['wenonah-wee']['family_fit']['oscar']['status']=='candidate' and p['wenonah-wee']['family_fit']['matvey']['status']=='not_eligible'
assert '$100' in p['wenonah-wee']['price']['deposit'] and '$75' in p['wenonah-wee']['price']['deposit']
for base,gross in [(6350,7175.50),(3650,4124.50),(1960,2214.80),(1300,1469),(500,565)]:assert round(base*1.13,2)==gross
assert p['wenonah-five']['timing']['sessions']==[['2027-08-30','2027-09-03']]
assert p['wenonah-wee']['timing']['sessions']==[['2027-08-30','2027-09-01']]

tokens('sciencequest','now-complete 2026','updates on our 2027','SK - Grade 1','Grades 2-3','Grades 4-8','$350/week','$365/week','$330/week','$280/week','$292/week','$264/week','will not be coding at a computer','June 29 - July 3','August 3 - August 7','non-refundable deposit')
tokens('sfu-summer','From $322 / WEEK','From $186 / WEEK','Elite Engineers','Brick Builders Lab','Digital Defenders','C/C++ Programming')
tokens('sfu-faq','upcoming 2026/2027 school year','do not allow','More than a week','$35 admin fee','$10 transfer fee','lunch and snacks')
grade_slugs=[s for s in NEW if s.startswith(('sciencequest-','sfu-','calgary-'))]
assert len(grade_slugs)==12
for s in grade_slugs:
    assert all(f['status']=='unknown' for f in p[s]['family_fit'].values()),s
    assert not p[s]['confirmed_instruction_languages'],s
past=[v for s in NEW for v in p[s]['timing']['sessions'] if v[1]<'2026-10-05'];assert len(past)==16
for s in [x for x in NEW if x.startswith(('sciencequest-','sfu-'))]:assert not p[s]['calendar_links'] and p[s]['price']['year']==2026
for s,key in [('calgary-early-engineering','calgary-early-engineering'),('calgary-early-technology','calgary-early-technology'),('calgary-engineering101','calgary-engineering101')]:
    tokens(key,"don't have any offerings",'entering in the fall');assert not p[s]['calendar_links']
tokens('calgary-engineering101','LEGO® SPIKE®','do not sponsor','3D printing','VR technology')
tokens('calgary-winter','Dec 2026','December 21-23','Gr. 3-5','Entering Grade 6','F26YMWB301','$260.00','13 Spots Available','swim test')
assert p['calgary-winter']['timing']['sessions']==[['2026-12-21','2026-12-23']]
assert (PRIMARY/'liota-home.txt').read_text().strip()=='Liota Summer Camp'  # Title only, no programme/fee body.

again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
for f,v in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/f).read_text())==v
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert {json.loads(v)['id']:json.loads(v) for v, in con.execute('SELECT record_json FROM events')}==ev
assert {json.loads(v)['slug']:json.loads(v) for v, in con.execute('SELECT record_json FROM camp_programmes')}==p;con.close()
csvrows=list(csv.DictReader((ROOT/'dist/downloads/STEM_catalog.csv').read_text().splitlines()));assert len(csvrows)==3184
md=(ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.md').read_text()
for s in NEW:assert p[s]['provider'] in md and p[s]['editorial_reason'] in md
def calendar(value):
    out={};t=value.decode().replace('\r\n ','').replace('\r\n\t','')
    for block in t.split('BEGIN:VEVENT')[1:]:
        f={s.split(':',1)[0]:s.split(':',1)[1] for s in block.split('END:VEVENT')[0].splitlines() if ':' in s};assert f['UID'] not in out;out[f['UID']]=f
    return out
for file,total in [('STEM_подтвержденные_даты.ics',2445),('STEM_крупные_выставки.ics',104)]:
    oldcal=calendar(prior('dist/downloads/'+file));now=calendar((ROOT/'dist/downloads'/file).read_bytes())
    assert set(oldcal)<=set(now) and len(now)==total
    for uid,v in oldcal.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
    if total==2445:
        assert set(now)-set(oldcal)=={'stem-'+e['id']+'@family-stem.local' for e in new}
        for e in new:
            f=now['stem-'+e['id']+'@family-stem.local'];assert f['DTSTART;VALUE=DATE']==e['start'].replace('-','')
            assert f['DTEND;VALUE=DATE']==(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d')
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==97
assert {q['id'] for q in bp['requirements']}=={q['id'] for q in plan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==bp[k],k
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['americas-camp-audit-v97','americas-camp-source-receipts-v97']:
    v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
    assert not any(v['external_actions'].values())
    if 'sources' in v:
        assert len(v['sources'])==32 and len(v['dossier_source_urls_added'])==25
        assert sum(q['retrieval_method']=='direct_http' for q in v['sources'])==25
        assert sum(q.get('status')==200 for q in v['sources'])==22
        assert sum(bool(q.get('error')) for q in v['sources'])==3
        assert sum(q['retrieval_method']=='web_tool_selected_primary_clauses' for q in v['sources'])==7
        for q in v['sources']:
            if q.get('sha256'):assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_americas_camp_audit_v97.json' in js
assert 'data-ui-version="97"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(s for s in js.splitlines() if s.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:''};
FUNCTIONS
cs.child='both';let found=new Set(filtered().map(p=>p.slug));if(!found.has('wenonah-five'))throw Error('FiveBoth');for(const s of NEW)if(s!=='wenonah-five'&&found.has(s))throw Error('falseBoth '+s);
cs.child='oscar';found=new Set(filtered().map(p=>p.slug));for(const s of ['pali-mini','wenonah-wee','wenonah-five'])if(!found.has(s))throw Error('Oscar '+s);for(const s of ['pali-general','pali-robotics','wenonah-one','wenonah-regular','calgary-winter'])if(found.has(s))throw Error('falseOscar '+s);
cs.child='';cs.phase='2027';found=new Set(filtered().map(p=>p.slug));for(const s of ['pali-general','pali-mini','wenonah-five','wenonah-wee'])if(!found.has(s))throw Error('2027 '+s);for(const s of ['pali-robotics','calgary-winter','sciencequest-robotics','sfu-brick-builders','calgary-engineering101'])if(found.has(s))throw Error('false2027 '+s);
cs.phase='';cs.language='EN';found=new Set(filtered().map(p=>p.slug));for(const s of NEW)if(found.has(s)!==s.startsWith('wenonah-'))throw Error('language '+s);
cs.language='ES';found=new Set(filtered().map(p=>p.slug));for(const s of NEW)if(found.has(s))throw Error('falseES '+s);
cs.language='';cs.format='online';found=new Set(filtered().map(p=>p.slug));if(found.size!==1||!found.has('pueblo-eduplai-online'))throw Error('oldOnline');
""".replace('FUNCTIONS',funcs).replace('NEW',json.dumps(NEW))
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(verified=True,events=3184,dossiers=664,new_dossiers=19,new_calendar_rows=31,prior_events_unchanged=3153,prior_dossiers_unchanged=645,family_ics=2445,source_urls=1046,worldwide_complete=False)))
