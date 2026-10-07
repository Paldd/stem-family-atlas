"""Independent retained primary reads, eligibility, language filter and preservation checks."""
import hashlib, json, re, sqlite3, subprocess
from datetime import datetime, date
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT.parent/'stem-family-atlas-work/camps-primary-v86'
BASE = '3585725a3011b0e34d825786540ed906be4cce35'
NODE = '/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def before(file):
    return subprocess.check_output(['git','show',BASE+':'+file],cwd=ROOT)
def raw(key):
    return (PRIMARY/(key+'.txt')).read_text()
def compact(t):
    return re.sub(r'\s+','',t)
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};events={e['id']:e for e in d['events']}
assert len(old)==2959 and len(events)==len(d['events'])==2966
assert all(events.get(k)==v for k,v in old.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==b[key],key
c=d['camp_programmes'];p={q['slug']:q for q in c['profiles']};op={q['slug']:q for q in b['camp_programmes']['profiles']}
assert len(op)==487 and len(p)==505 and all(p[k]==v for k,v in op.items())
assert c['profiles'][:487]==b['camp_programmes']['profiles']
assert c['counts']['countries']==35 and c['counts']['source_urls']==771 and c['counts']['swiss']==78
for iso,n in [('CHE',78),('FRA',41),('ESP',43),('TWN',29),('SGP',61),('JPN',28),('KOR',10),('MYS',4),('USA',44),('CAN',57),('CRI',10),('MEX',25)]:
    assert sum(q['iso']==iso for q in p.values())==n,(iso,n)
assert len(c['shortlist'])==111 and c['shortlist'][:106]==b['camp_programmes']['shortlist']
assert c['gaps'][:-5]==b['camp_programmes']['gaps']
assert all(len(s['slugs'])==len(set(s['slugs'])) and all(k in p for k in s['slugs']) for s in c['shortlist'][-5:])
new=[e for k,e in events.items() if k not in old]
assert len(new)==7 and all(e['block']=='Лагеря' and e['checked']=='2026-10-05' for e in new)
assert sum(e['block']=='Лагеря' for e in events.values())==1635
assert len(c['generated_event_ids'])==1172 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==35
def rows(slug):return [e for e in new if e['camp_dossier_slug']==slug]
def pairs(slug):return {(e['start'],e['end']) for e in rows(slug)}

# Independently derive dates/durations/prices from the separate residential/day source sections.
t=raw('gep-winter-2027');assert 'Year\n                2027' in t
parts={'board':t.split('Residential\n',1)[1].split('Day Camp\n',1)[0],
       'day':t.split('Day Camp\n',1)[1].split('Typical Day Schedule',1)[0]}
pattern=r'(Winter Camp [12]|Signature Winter Camp)\n([^\n]+)\n(\d+) days duration\nRM\n([\d,]+)'
for fmt,body in parts.items():
    parsed=[]
    for label,period,days,amount in re.findall(pattern,body):
        found=re.fullmatch(r'(\d+) (\w+)(?: (2027))? (?:-|→) (\d+) (\w+) 2027',period)
        assert found,period
        a=datetime.strptime(f'{found[1]} {found[2]} 2027','%d %b %Y').date()
        z=datetime.strptime(f'{found[4]} {found[5]} 2027','%d %b %Y').date()
        assert (z-a).days+1==int(days)
        parsed.append((a.isoformat(),z.isoformat(),int(amount.replace(',',''))))
    assert len(parsed)==3
    assert pairs('gep-winter-'+fmt)=={(a,z) for a,z,n in parsed}
    for e in rows('gep-winter-'+fmt):
        n=next(n for a,z,n in parsed if (a,z)==(e['start'],e['end']))
        assert f'RM{n}' in compact(e['cost']).replace(',','')
        assert e['languages']==['EN'] and e['language_mode']=='primary'
        assert not e['priority'].startswith('P4')
        if fmt=='day':
            assert e['participation']=='day_camp' and e['date_scope']=='day_camp_window'
            assert e.get('attendance_weekdays',[])==[]
        else:assert e['participation']=='residential'
assert '9 to 14' in t and 'Campers learn in English' in t
sp=raw('gep-spring-2027');assert '26 Mar - 2 Apr 2027\n8 days duration\nRM\n7,326' in sp
assert '9 to 16' in sp and 'own laptop' in sp and '1:10' in sp
assert pairs('gep-spring-board')=={('2027-03-26','2027-04-02')} and 'RM7326' in compact(rows('gep-spring-board')[0]['cost'])
for slug in ['gep-winter-board','gep-winter-day','gep-spring-board']:
    assert p[slug]['family_fit']['matvey']['status']=='conditional' and p[slug]['family_fit']['oscar']['status']=='later'
terms=compact(raw('gep-terms-pdf-layout'))
assert 'RM800perdayorpartthereof' in terms and 'within3hoursofnotification' in terms
assert 'morethan60businessdays' in terms and 'cancellationfeeofRM1,000' in terms
assert 'BritishSummerSchool' in terms and 'RM2,000' in terms and 'creditnotevalidforone(1)year' in terms
assert 'T&CVersion–May2026' in terms
assert 'Bandar Enstek' in raw('epsom-campus-contact') and 'Negeri Sembilan' in raw('epsom-campus-contact')
wild=raw('gep-wild-minds');assert '11 to 17' in wild and 'B1' in wild and 'Sold Out' in wild
assert 'International flights to and from Malaysia are not included' in wild
assert 'air travel between the Epsom College and Borneo campuses are included' in wild
assert p['gep-wild-minds-board']['timing']['status']=='published_2026' and not p['gep-wild-minds-board']['timing']['sessions']

# Japanese 2026 programmes and actual grade restrictions, not inferred birthyear/grade.
exp=raw('canacad-experience');dis=raw('canacad-discovery')
assert 'Pre-K – Grade 6' in exp and '¥75,000' in exp and '¥140,000' in exp
assert 'VEX' in exp and '4 periods' in exp and 'skills in English' in exp
assert '3,500 JPY per registered student' in exp and 'Registration is valid for 5 years' in exp
assert '¥11,000' in exp and '¥9,000' in exp
assert 'Pre-K – Grade 12' in dis and '¥118,000' in dis and '¥8,000/session' in dis
assert 'no language requirements' in dis.lower() and 'Pre-K' in dis and 'Canadian Academy' in dis
assert 'JPY157000' in compact(p['canadian-academy-summer-experience']['price']['label'])
assert 'JPY287000' in compact(p['canadian-academy-summer-experience']['price']['label'])
assert 'JPY259000' in compact(p['canadian-academy-summer-discovery']['price']['label'])
assert (118000+8000+3500)*2==259000 and (75000+3500)*2==157000
ai=raw('canacad-ai');ja=raw('canacad-ai-scratch');math=raw('canacad-ib-math')
assert 'Grades6-12' in compact(ai) and '$1,200 USD' in ai
assert 'Grades8-12' in compact(ja) and '¥60,000' in ja
assert 'Japanese with English translation' in ja and 'English-based AI program' in ja and 'hackathon' in ja
assert 'Grades10-11' in compact(math) and 'Grades9-11' in compact(math) and '¥60,000' in math
assert all(v in compact(math) for v in ['10:00-11:30','12:30-13:30','14:00-15:00'])
assert sum([1.5,1,1])*5==17.5
assert p['canadian-academy-ai-from-scratch']['confirmed_instruction_languages']==['JA']
assert p['canadian-academy-ai-from-scratch']['confirmed_support_languages']==['EN']
assert p['canadian-academy-inspirit-ai']['confirmed_instruction_languages']==['EN']
assert p['canadian-academy-summer-discovery']['confirmed_instruction_languages']==[]
for slug in ['canadian-academy-inspirit-ai','canadian-academy-ai-from-scratch','canadian-academy-ib-math-mastery']:
    assert all(v['status']=='unknown' for v in p[slug]['family_fit'].values())
assert all(q['formats']==['day'] and q['timing']['status']=='published_2026' and not q['timing']['sessions'] for s,q in p.items() if s.startswith('canadian-academy-'))

# Read-only public forms: preliminary prices, grades, weekends and a preserved typo.
j=compact(raw('tais-2027-reservation'));t=compact(raw('tais-2027-school-reservation'))
assert '8歲~11歲' in j and '一年級~國小五年級' in j and '35,000' in j and '58000' in j and '非進行正式報名' in j
assert '12-17歲' in t and '70,000' in t and '48,000' in t and '25,000' in t and '62,00' in t and '每週五下午返家' in t
assert '2,000' in j and '2,000' in t
for slug in ['tais-junior-board','tais-junior-day','tais-teen-board','tais-teen-day']:
    assert p[slug]['timing']['status']=='partial_2027' and not p[slug]['timing']['sessions']
    assert p[slug]['language_evidence_role']=='language_lessons' and p[slug]['confirmed_instruction_languages']==['EN']
assert '62,00' in p['tais-teen-board']['price']['label'] and '62 000' not in p['tais-teen-board']['price']['label']
assert p['tais-junior-board']['family_fit']['oscar']['status']=='later'
assert '8歲~12歲' in compact(raw('tais-summer-school'))

# Course prices include actual GST; total camp presence and curriculum hours differ.
for key,expected in [('codinglab-scratch-1',[('435','474.15'),('485','528.65'),('845','921.05')]),
                     ('codinglab-app-1',[('470','512.30'),('795','866.55'),('865','942.85')]),
                     ('codinglab-python-1',[('470','512.30'),('795','866.55'),('865','942.85')])]:
    body=raw(key)
    amounts=re.findall(r'\$(\d+) \(\$(\d+\.\d+) w/GST\)',body)
    assert amounts[:3]==expected,(key,amounts[:3])
    for base,total in amounts[:3]:assert round(float(base)*1.09,2)==float(total)
    assert 'All materials and equipment provided' in body and 'Maximum 1:8' in body
    assert '21 hours total' in body and 'Lunch and snacks provided' in body
faq=raw('codinglab-sg-faq');jr=raw('codinglab-sg-preschool')
assert 'entering Primary 1' in faq and '10-hour class' in faq and '20-hour class' in faq
assert 'only through our partner preschools' in jr and 'Photon' in jr and '1:6' in jr
assert 'Passed the placement test' in raw('codinglab-python-1')
for slug in ['codinglab-sg-junior-partner','codinglab-sg-scratch-camp','codinglab-sg-app-camp','codinglab-sg-python-camp']:
    assert p[slug]['confirmed_instruction_languages']==[] and not p[slug]['timing']['sessions']
graph=raw('graphite-holiday');assert '23–25 November' in graph and '7–9 December' in graph
assert '9:30 AM – 12:00 PM' in graph and '3 Days • 1.5 Hours' in graph and 'September Holiday' in graph
assert not p['graphite-sg-roblox-code-avengers']['timing']['sessions']
off=compact(raw('minecraft-official-2026-layout'));coach=raw('codinglab-minecraft-cup')
assert '2027年4月1日時点' in off and '未就学児含む' in off and '1～40' in off and '海外' in off
assert '2026年9月7日' in off and '2027年2月14日' in off and 'デジタルものづくり協議会' in off
assert '1 April 2026' in coach and '975.55 w GST' in coach and 'P102 Scratch 2' in coach and '18 Hours' in coach
assert len(raw('tyas-camp-details').strip())==34 and '2026' in raw('tyas-camp-details')

# Isolated production predicate, including translation-only and absent-array cases.
js=(ROOT/'dist/assets/camp-programmes.js').read_text()
fn=re.search(r'function matchesLanguage\(p,selected\)\{[^\n]+\}',js).group(0)
test=fn+"\nconst assert=require('node:assert/strict');const ja={confirmed_instruction_languages:['JA'],confirmed_support_languages:['EN']};assert.equal(matchesLanguage(ja,'EN'),false);assert.equal(matchesLanguage(ja,'EN-support'),true);assert.equal(matchesLanguage(ja,'JA'),true);assert.equal(matchesLanguage(ja,''),true);assert.equal(matchesLanguage({},'EN-support'),false);assert.equal(matchesLanguage({confirmed_instruction_languages:['EN']},'EN'),true);assert.equal(matchesLanguage({confirmed_instruction_languages:['EN']},'EN-support'),false);assert.equal(matchesLanguage({confirmed_instruction_languages:['RU']},'RU'),true);"
subprocess.run([NODE,'-e',test],check=True,cwd=ROOT)
assert 'matchesLanguage(p,cs.language)' in js and 'value="EN-support"' in js and 'value="RU"' in js

# SQLite, public JSON, integration and prior calendar content remain consistent.
report=json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text())
again=json.loads(json.dumps(d));integrate(again,report);assert again==d
for file,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:
    assert json.loads((ROOT/'dist/downloads'/file).read_text())==wanted
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2966 and con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==505
con.close()
def calendar(v):
    out={};t=v.decode().replace('\r\n ','').replace('\r\n\t','')
    for ch in t.split('BEGIN:VEVENT')[1:]:
        f={line.split(':',1)[0]:line.split(':',1)[1] for line in ch.split('END:VEVENT')[0].splitlines() if ':' in line}
        assert f['UID'] not in out;out[f['UID']]=f
    return out
file='dist/downloads/STEM_подтвержденные_даты.ics';prior=calendar(before(file));now=calendar((ROOT/file).read_bytes())
assert len(prior)==2233 and len(now)==2240 and set(prior)<=set(now)
for uid,v in prior.items():
    assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
assert set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in new}
for e in new:
    if e.get('date_scope')=='day_camp_window':
        summary=now['stem-'+e['id']+'@family-stem.local']['SUMMARY']
        assert '[Окно дневного лагеря · расписание уточнить]' in summary and 'Пн–Пт' not in summary
file='dist/downloads/STEM_крупные_выставки.ics';expo=calendar((ROOT/file).read_bytes());oe=calendar(before(file))
assert len(expo)==104 and set(expo)==set(oe)
for uid,v in oe.items():assert {k:x for k,x in expo[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==86
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version85' in plan['previous_goal_turn_classification']['evidence']
assert {q['id'] for q in bp['requirements']}<={q['id'] for q in plan['requirements']}
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert plan['camp_catalog_integration']['dossiers']==505 and d['coverage_summary']['fully_audited_countries']==0
for stem in ['asia-camp-audit-v86','asia-camp-source-receipts-v86']:
    val=json.loads((ROOT/'data'/f'{stem}.json').read_text())
    assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==val
    assert not any(val['external_actions'].values())
assert len(val['sources'])==41 and sum(v.get('status')==200 for v in val['sources'])==40
assert len(val['dossier_source_urls_added'])==22 and len(val['visual_primary_reads'])==3
for v in val['sources']:
    if v.get('status')==200:assert v['body_snapshot_retained'] and hashlib.sha256((PRIMARY/v['raw_filename']).read_bytes()).hexdigest()==v['sha256']
assert any(v['key']=='rayul-camp' and '404' in v.get('error','') for v in val['sources'])
assert 'data-ui-version="86"' in (ROOT/'dist/index.html').read_text() and 'STEM_asia_camp_audit_v86.json' in js
print(json.dumps(dict(passed=True,preserved_events=2959,preserved_dossiers=487,new_dossiers=18,new_calendar_rows=7,new_family_ics=7,
    events=2966,dossiers=505,family_ics=2240,exhibition_ics=104,worldwide_complete=False)))
