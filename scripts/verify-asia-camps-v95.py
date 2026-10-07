"""Independent source/date/fee checks plus preservation and portable calendar checks."""
import collections, datetime, hashlib, json, re, sqlite3, subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
from camp_asia_v95 import NEW, UPDATED

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT.parent/'stem-family-atlas-work/camps-primary-v95'
BASE = 'dfc36a921a2030d2d0090c77314d256b100b2cd7'
NODE = '/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def before(path): return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def raw(key): return (PRIMARY/(key+'.txt')).read_text()
b = json.loads(before('data/catalog.json'));d = json.loads((ROOT/'data/catalog.json').read_text());c = d['camp_programmes']
old = {e['id']:e for e in b['events']};ev = {e['id']:e for e in d['events']}
op = {p['slug']:p for p in b['camp_programmes']['profiles']};p = {q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3140 and len(old)==3123 and set(old)<=set(ev)
assert all(ev[k]==e for k,e in old.items())
new = [e for k,e in ev.items() if k not in old]
assert len(new)==17 and collections.Counter(e['camp_dossier_slug'] for e in new)=={'whizz-lpe':4,'whizz-nlcs':1,'whizz-smash':2,'mind-ai-sprint':5,'mind-ai-story':5}
assert len(p)==631 and set(p)-set(op)==set(NEW)
assert [q['id'] for q in c['profiles'][:622]]==[q['id'] for q in b['camp_programmes']['profiles']]
assert [p[s]['id'] for s in NEW]==['CP%03d'%i for i in range(623,632)]
for slug,q in op.items():
    if slug not in UPDATED: assert p[slug]==q,slug
    else:
        for key in ['id','slug','iso','country','related_event_ids','calendar_links','confirmed_instruction_languages']:
            assert p[slug].get(key)==q.get(key),(slug,key)
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==b[key],key
assert c['counts']['countries']==37 and c['counts']['swiss']==86 and c['counts']['source_urls']==992
assert c['shortlist'][:-4]==b['camp_programmes']['shortlist'] and c['gaps'][:-4]==b['camp_programmes']['gaps']
assert len(c['shortlist'])==146
for q in c['shortlist']: assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
assert sum(e['block']=='Лагеря' for e in ev.values())==1809 and len(c['generated_event_ids'])==1346
assert c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==39

# Independently match exact campus/track selector entries, not the broad7week header.
campus_rows = collections.defaultdict(set)
for campus in ['donghu','keelung']:
    body = raw('ilri-'+campus+'-form')
    for token in ['2026','升小一','小四以上','13,200','9500','1000','六月底','需自備','需另外加購機器人','18:00','100']:
        assert token in body,(campus,token)
    tail = body.split('選擇梯次',1)[1].split('優惠方案',1)[0]
    for line in tail.splitlines():
        match = re.search(r'(\d+)/(\d+)\([^)]*\)-(\d+)/(\d+)\([^)]*\)',line)
        if not match: continue
        m,a,n,z = map(int,match.groups())
        track = 'roblox' if 'Roblox' in line else 'minecraft' if 'Minecraft' in line else 'lego'
        campus_rows[track].add((campus,f'2026-{m:02d}-{a:02d}',f'2026-{n:02d}-{z:02d}'))
assert {k:len(v) for k,v in campus_rows.items()}=={'lego':8,'minecraft':5,'roblox':4}
for track,want in campus_rows.items():
    q = p['ilri-'+track]
    got = {(v['variant_key'].split('-')[0],v['start'],v['end']) for v in q['timing']['session_details']}
    assert got==want,(track,got^want)
    assert q['timing']['status']=='archive_next_unannounced' and not q['calendar_links']
    assert all(x['status']=='unknown' for x in q['family_fit'].values())
assert 'Teaching is in English and Chinese' in raw('ilri-home')
assert p['ilri-lego']['confirmed_instruction_languages']==['EN'] and p['ilri-lego']['language_evidence_role']=='bilingual'
assert all(p[s]['confirmed_instruction_languages']==[] for s in ['ilri-minecraft','ilri-roblox'])
assert 'English-based learning environment' in raw('tcs-steam') and '2026/02/02-2026/02/06' in raw('tcs-steam')
assert 'NTD19,000' in raw('tcs-steam') and 'materials fees($2,000)' in raw('tcs-steam')
assert p['tcs-steam-winter']['confirmed_instruction_languages']==['EN'] and not p['tcs-steam-winter']['calendar_links']
assert all(x['status']=='unknown' for x in p['tcs-steam-winter']['family_fit'].values())

l26 = raw('whizz-2026-observed');l27 = raw('whizz-2027-observed')
for text in ['19 – 23 October 2026','26 – 30 October 2026','Ages 4 – 6 years old','7 to 12 years old (NEW)']:assert text in l26,text
for text in ['22 – 26 February 2027','01 – 05 March 2027','Camp Dates: Choose an option (no actual dates in selector)','July 2026']:assert text in l27,text
assert {v['start'] for v in p['whizz-lpe']['timing']['session_details']}=={'2026-10-19','2026-10-26','2027-02-22','2027-03-01'}
assert '450.00' in raw('whizz-nlcs-observed') and '4–6 years old' in raw('whizz-nlcs-observed')
assert '$340.00 through $400.00' in raw('whizz-smash-observed') and '$50 off total camp fees' in raw('whizz-smash-observed')
assert not any(e['start']>='2026-11-01' for e in new if e['camp_dossier_slug']=='whizz-smash')
assert all(p[s]['confirmed_instruction_languages']==[] for s in ['whizz-lpe','whizz-nlcs','whizz-smash','mind-ai-sprint','mind-ai-story'])
assert all('SGD' not in p[s]['price']['label'] for s in ['whizz-lpe','whizz-nlcs','whizz-smash'])

weekdates = {('2026-11-23','2026-11-27'),('2026-11-30','2026-12-03'),('2026-12-14','2026-12-18'),('2026-12-21','2026-12-24'),('2026-12-28','2026-12-31')}
for slug,key in [('mind-ai-sprint','mind-sprint-actual-course'),('mind-ai-story','mind-story')]:
    text = raw(key)
    for phrase in ['23 Nov – 27 Nov','30 Nov – 3rd Dec','14 Dec – 18 Dec','21 Dec – 24 Dec','28 Dec – 31 Dec']:assert phrase in text
    assert set(map(tuple,p[slug]['timing']['sessions']))==weekdates
assert 'year-end 2026' in raw('mind-home') and '4 Days of 3hr $600' in raw('mind-story')
assert 'After Early Bird Period = $800' in raw('mind-story') and 'AM 1000-1300' in raw('mind-story') and '14:00 - 17:00' in raw('mind-story')
assert 'PM 1400-1600\n28 Dec – 31 Dec\n4 Days of 3hr' in raw('mind-sprint-actual-course')
last = p['mind-ai-sprint']['timing']['session_details'][-1]
assert '8 или 12' in last['label'] and 'неизвестна' in last['price']
assert 'unable to provide refunds' in raw('mind-faq')
assert p['mind-ai-story']['family_fit']['oscar']['status']==p['mind-ai-sprint']['family_fit']['oscar']['status']=='later'
harrow = raw('harrow-winter')
for phrase in ['08:40 - 10:30','10:45 - 11:40','13:00 - 15:40','352,000 for Current','13 – 19 December 2026','20:30 - 21:30']:
    assert phrase in harrow,phrase
assert 5*((10*60+30)-(8*60+40)+(11*60+40)-(10*60+45))==825
assert 5*((15*60+40)-13*60)==800
assert '13 ч 45' in p['harrow-appi']['programme'] and '13 ч 20' in p['harrow-appi']['programme']
assert '2016 Summer Series' in raw('branksome-camp-pdf') and '2016-17 Academic Year' in raw('branksome-camp-pdf')
assert len(list(PRIMARY.glob('*page*.png')))==1

again = json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
for file,want in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:
    assert json.loads((ROOT/'dist/downloads'/file).read_text())==want
con = sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert {json.loads(v)['id']:json.loads(v) for v, in con.execute('SELECT record_json FROM events')}==ev
assert {json.loads(v)['slug']:json.loads(v) for v, in con.execute('SELECT record_json FROM camp_programmes')}==p;con.close()
def calendar(value):
    out = {};text = value.decode().replace('\r\n ','').replace('\r\n\t','')
    for block in text.split('BEGIN:VEVENT')[1:]:
        fields = {line.split(':',1)[0]:line.split(':',1)[1] for line in block.split('END:VEVENT')[0].splitlines() if ':' in line}
        assert fields['UID'] not in out;out[fields['UID']] = fields
    return out
for file,total in [('STEM_подтвержденные_даты.ics',2401),('STEM_крупные_выставки.ics',104)]:
    prior = calendar(before('dist/downloads/'+file));now = calendar((ROOT/'dist/downloads'/file).read_bytes())
    assert set(prior)<=set(now) and len(now)==total
    for uid,v in prior.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
    if total==2401:
        assert set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in new}
        for e in new:
            f = now['stem-'+e['id']+'@family-stem.local']
            assert f['DTSTART;VALUE=DATE']==e['start'].replace('-','')
            assert f['DTEND;VALUE=DATE']==(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d')
plan = json.loads((ROOT/'data/research-plan.json').read_text());bp = json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==95
assert {q['id'] for q in bp['requirements']}=={q['id'] for q in plan['requirements']}
for key in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[key]==bp[key],key
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['asia-camp-audit-v95','asia-camp-source-receipts-v95']:
    v = json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
    assert not any(v['external_actions'].values())
    if 'sources' in v:
        assert len(v['sources'])==37 and len(v['dossier_source_urls_added'])==17
        assert sum(q['retrieval_method']=='direct_http' and q.get('status')==200 for q in v['sources'])==21
        assert sum(q.get('content_status')=='soft_404_not_programme' for q in v['sources'])==2
        for q in v['sources']:
            if q.get('raw_filename'):assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
        pdf = next(q for q in v['sources'] if q['key']=='branksome-camp-pdf')
        assert pdf['pdf_metadata']['Pages']=='6' and '2016' in pdf['pdf_metadata']['CreationDate']
js = (ROOT/'dist/assets/camp-programmes.js').read_text()
assert 'STEM_asia_camp_audit_v95.json' in js and 'archive_next_unannounced' in js and 'data-ui-version="95"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs = '\n'.join(line for line in js.splitlines() if line.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test = """const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:'EN'};
FUNCTIONS
let found=new Set(filtered().map(p=>p.slug));
for(const s of ['whizz-lpe','whizz-nlcs','whizz-smash','mind-ai-sprint','mind-ai-story','ilri-minecraft','ilri-roblox'])if(found.has(s))throw Error('falseEN '+s);
for(const s of ['ilri-lego','tcs-steam-winter','harrow-appi'])if(!found.has(s))throw Error('missingEN '+s);
cs.language='';cs.child='both';found=new Set(filtered().map(p=>p.slug));
for(const s of ['ilri-lego','ilri-minecraft','ilri-roblox','tcs-steam-winter','whizz-smash','mind-ai-sprint','mind-ai-story','harrow-appi'])if(found.has(s))throw Error('falseBoth '+s);
for(const s of ['whizz-lpe','whizz-nlcs'])if(!found.has(s))throw Error('missingBoth '+s);
cs.child='';cs.phase='archive_next_unannounced';found=new Set(filtered().map(p=>p.slug));
if(found.size!==4||!found.has('tcs-steam-winter'))throw Error('archive phase');
cs.phase='2027';found=new Set(filtered().map(p=>p.slug));
if(!found.has('whizz-lpe')||found.has('ilri-lego')||found.has('tcs-steam-winter'))throw Error('false2027');
cs.phase='';cs.country='SGP';cs.theme='games';found=new Set(filtered().map(p=>p.slug));if(!found.has('mind-ai-sprint'))throw Error('games filter');
""".replace('FUNCTIONS',funcs)
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(verified=True,events=3140,dossiers=631,new_dossiers=9,deepened_dossiers=1,new_calendar_rows=17,
    prior_events_unchanged=3123,prior_dossiers_unchanged=621,family_ics=2401,source_urls=992,worldwide_complete=False)))
