"""Independent primary date parsing, eligibility/language and previous-data preservation."""
import collections,datetime,hashlib,json,re,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v89'
BASE='96223ed18e24d8cbbd13a321f23b9918a22f6b0e'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def before(file):return subprocess.check_output(['git','show',BASE+':'+file],cwd=ROOT)
def raw(key):return (PRIMARY/(key+'.txt')).read_text()
def compact(s):return re.sub(r'\s+','',s)
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};events={e['id']:e for e in d['events']}
assert len(old)==2997 and len(events)==len(d['events'])==3037 and set(old)<=set(events)
assert all(events[k]==v for k,v in old.items())
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
 assert d[k]==b[k],k
c=d['camp_programmes'];p={q['slug']:q for q in c['profiles']};op={q['slug']:q for q in b['camp_programmes']['profiles']}
assert len(op)==547 and len(p)==len(c['profiles'])==575
assert [q['id'] for q in c['profiles'][:547]]==[q['id'] for q in b['camp_programmes']['profiles']]
for slug,q in op.items():
 if slug!='typa':assert p[slug]==q,slug
 else:
  assert p[slug]['id']==q['id'] and p[slug]['timing']==q['timing'] and p[slug]['price']==q['price']
  assert p[slug]['calendar_links']==q['calendar_links'] and p[slug]['related_event_ids']==q['related_event_ids']
  assert p[slug]['sources'][:-1]==q['sources'] and p[slug]['questions'][:-1]==q['questions']
assert c['counts']['countries']==36 and c['counts']['source_urls']==862 and c['counts']['swiss']==84
assert len(c['shortlist'])==124 and c['shortlist'][:119]==b['camp_programmes']['shortlist']
assert c['gaps'][:-4]==b['camp_programmes']['gaps']
assert all(len(s['slugs'])==len(set(s['slugs'])) and all(k in p for k in s['slugs']) for s in c['shortlist'][-5:])
new=[e for k,e in events.items() if k not in old]
fresh={k:q for k,q in p.items() if k not in op}
assert len(new)==40 and len(fresh)==28 and [q['id'] for q in fresh.values()]==['CP%03d'%i for i in range(548,576)]
assert collections.Counter(q['iso'] for q in fresh.values())==dict(JPN=12,SGP=8,TWN=6,KOR=2)
assert sum(e['block']=='Лагеря' for e in events.values())==1706
assert len(c['generated_event_ids'])==1243 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==35
# Japan winter dates/English/extra fees versus undated GSA and archived summer.
t=raw('evergreen-winter');assert '14th - 18th December 2026' in t and '2nd - 6th January 2027' in t
assert 'All communications, operations, and managements of the camps will be in English.' in raw('evergreen-faq')
assert all(x in t for x in ['¥175,000','¥24,400','¥11,220','¥3,275','¥4,730'])
w=p['evergreen-hakuba-winter'];assert w['confirmed_instruction_languages']==['EN'] and w['language_evidence_role']=='primary'
assert w['timing']['sessions']==[['2026-12-14','2026-12-18'],['2027-01-02','2027-01-06']]
assert 175000+24400+11220+3275*2+4730==221900 and '221900' in compact(w['price']['label'])
assert w['family_fit']['matvey']['status']=='conditional' and w['family_fit']['oscar']['status']=='later'
summer=[q for k,q in fresh.items() if k.startswith('evergreen-hakuba-') and k!=w['slug']]
assert len(summer)==9 and all(not q['timing']['sessions'] and q['price']['year']==2026 for q in summer)
assert all('robotics' not in q['themes'] and q['confirmed_instruction_languages']==['EN'] for q in summer)
assert 'last 3 years' in raw('evergreen-expedition-sample') or 'last 3 years' in (PRIMARY/'evergreen-expedition-sample.txt').read_text()
for slug in ['gsa-tachikawa-elementary','gsa-tachikawa-kindergarten']:
 assert not p[slug]['timing']['sessions'] and p[slug]['price']['year'] is None
 assert p[slug]['timing']['status']=='next_unannounced' and p[slug]['confirmed_instruction_languages']==['EN']
assert 'all taught in English' in raw('gsa-kindergarten') and '¥88:000' in raw('gsa-elementary')
assert '2027' not in raw('gsa-elementary') and '2027' not in raw('gsa-kindergarten')
# No SOR December placeholders promoted to dates/English/official league.
t=raw('sor-holiday');assert '8th-11th September' in t and 'XX December 2026' in t
assert 'All credit purchases are non-refundable and non-transferable' in t and 'before GST' in t
for slug in ['sor-rescue','sor-rumble','sor-spin','sor-vexgo']:
 assert not p[slug]['timing']['sessions'] and p[slug]['confirmed_instruction_languages']==[]
assert 'RECF' in p['sor-vexgo']['programme']
# Independently parse complete CT source date pairs; no hardcoded date mirroring.
months={'Oct':10,'Nov':11,'Dec':12}
ct=[]
for slug,key in [('computhink-roblox-teens','computhink-roblox'),('computhink-python-minecraft-teens','computhink-python'),('computhink-ai-app-teens','computhink-ai'),('computhink-g3-python','computhink-g3')]:
 t=raw(key);pairs=[]
 for a,m,y,z,n,yy in re.findall(r'(\d{1,2})\s+(Oct|Nov|Dec)\s+(2026)\s*–\s*(\d{1,2})\s+(Oct|Nov|Dec)\s+(2026)',t):
  pairs.append((f'{y}-{months[m]:02d}-{int(a):02d}',f'{yy}-{months[n]:02d}-{int(z):02d}'))
 actual=[(e['start'],e['end']) for e in new if e['camp_dossier_slug']==slug]
 assert actual and collections.Counter(actual)==collections.Counter(pairs),(slug,pairs,actual)
 assert '$467' in t and all(v['status']=='later' for v in p[slug]['family_fit'].values())
 assert p[slug]['confirmed_instruction_languages']==[]
 ct.extend(e for e in new if e['camp_dossier_slug']==slug)
assert len(ct)==15 and 'Sec 2 students who have confirmed' in raw('computhink-g3')
# Taiwanese course date pairs independently parsed, including weekends/campus repetitions.
iro=[]
for slug,key,price in [('irobo-speed-mechanics','irobo-spm','4700'),('irobo-boost-ice','irobo-boost1','5200'),('irobo-boost-treasure','irobo-boost2','5200'),('irobo-star-voyager','irobo-spike','5400'),('irobo-python-basic','irobo-python','5600')]:
 t=raw(key);pairs=[(f'2027-{int(m):02d}-{int(a):02d}',f'2027-{int(n):02d}-{int(z):02d}') for m,a,n,z in re.findall(r'(\d)/(\d{1,2})\([^)]*\)－(\d)/(\d{1,2})\([^)]*\)',t)]
 rows=[e for e in new if e['camp_dossier_slug']==slug]
 assert rows and collections.Counter((e['start'],e['end']) for e in rows)==collections.Counter(pairs)
 assert len({v['variant_key'] for v in p[slug]['timing']['session_details']})==len(rows)
 assert p[slug]['confirmed_instruction_languages']==[] and all('attendance_weekdays' not in e for e in rows)
 assert price in t and price in p[slug]['price']['label']
 iro.extend(rows)
assert len(iro)==20 and any(datetime.date.fromisoformat(e['start']).weekday()==5 for e in iro)
assert p['irobo-python-basic']['family_fit']['matvey']['status']=='unknown'
assert p['irobo-star-voyager']['family_fit']['oscar']['status']=='unknown'
# NTUE primary guide is an English document, not confirmed English instruction.
n=p['ntue-mandarin-winter'];assert n['confirmed_instruction_languages']==['ZH'] and n['language_evidence_role']=='language_lessons'
assert n['timing']['sessions']==[['2026-12-28','2027-01-08']] and '9' in n['programme'] and '01Jan' in n['programme']
assert all(x in n['price']['deposit'] for x in ['1/3','1/2']) and 34000*2==68000
assert '8至12人' in compact(raw('ntue-faq')) and '不提供學生住宿' in raw('ntue-faq')
assert '三分之一' in raw('ntue-faq')
# Older/religious Korean candidates excluded from current family calendar.
ik=p['intercamp-seoul-winter'];assert 'aged from 14 to 18' in raw('intercamp-home')
assert ik['language_evidence_role']=='language_lessons' and ik['confirmed_instruction_languages']==['EN','KO']
assert all(v['status']=='later' for v in ik['family_fit'].values())
wk=p['wolko-winter-english'];assert 'January 11–16, 2027' in raw('wolko-register') and 'Upcoming' in raw('wolko-register')
assert 'Gospel' in raw('wolko-camp') and 'discipleship' in raw('wolko-camp') and 'Христианский' in wk['programme']
assert wk['timing']['status']=='partial_2027' and all(v['status']=='later' for v in wk['family_fit'].values())
# Atomic TYPA curriculum is printed Summer2026, not a2027 announcement.
ty=(PRIMARY/'typa-magazine-layout.txt').read_text();assert 'Summer Tech' in ty and '2026' in ty and 'Curious Explorers' in ty
assert '15–18 июня' in p['typa']['programme'] and '2027 ещё не объявлен' in p['typa']['programme']
# Idempotent integrated public data/database, complete previous calendar preservation.
report=json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text());again=json.loads(json.dumps(d));integrate(again,report);assert again==d
for file,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:
 assert json.loads((ROOT/'dist/downloads'/file).read_text())==wanted
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==3037 and con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==575;con.close()
def calendar(v):
 out={};t=v.decode().replace('\r\n ','').replace('\r\n\t','')
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={l.split(':',1)[0]:l.split(':',1)[1] for l in ch.split('END:VEVENT')[0].splitlines() if ':' in l}
  assert f['UID'] not in out;out[f['UID']]=f
 return out
family=[e for e in new if e['camp_dossier_slug']=='evergreen-hakuba-winter' or e['camp_dossier_slug'].startswith('irobo-') or e['camp_dossier_slug']=='ntue-mandarin-winter']
assert len(family)==23
for file,total,previous in [('STEM_подтвержденные_даты.ics',2279,2256),('STEM_крупные_выставки.ics',104,104)]:
 f='dist/downloads/'+file;prior=calendar(before(f));now=calendar((ROOT/f).read_bytes());assert len(prior)==previous and len(now)==total and set(prior)<=set(now)
 for uid,v in prior.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
 if total==2279:
  assert set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in family}
  assert all(not any(e['id'] in uid for uid in now) for e in ct+[e for e in new if e['camp_dossier_slug'] in ['intercamp-seoul-winter','wolko-winter-english']])
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==89
assert {q['id'] for q in bp['requirements']}<={q['id'] for q in plan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:
 assert plan[k]==bp[k],k
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert plan['camp_catalog_integration']['dossiers']==575 and d['coverage_summary']['fully_audited_countries']==0
for stem in ['asia-camp-audit-v89','asia-camp-source-receipts-v89']:
 v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
 assert not any(v['external_actions'].values())
 if 'sources' in v:
  assert len(v['sources'])==42 and sum(q.get('status')==200 for q in v['sources'])==40
  assert len(v['image_primary_reads'])==5 and len(v['visual_pdf_reads'])==5 and len(v['dossier_source_urls_added'])==33
  for q in v['sources']+v['image_primary_reads']:
   if q.get('status')==200:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
  errors={q['key'] for q in v['sources'] if q.get('status')!=200};assert errors=={'rotary-taiwan','sor-terms'}
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_asia_camp_audit_v89.json' in js and 'STEM_europe_camp_audit_v88.json' in js
assert 'data-ui-version="89"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
# Exercise the real UI language/filter functions with current dossiers.
funcs='\n'.join(line for line in js.splitlines() if line.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:'EN'};
FUNCTIONS
const found=new Set(filtered().map(p=>p.slug));
for(const p of guide.profiles.filter(p=>p.id>='CP548'&&p.id<='CP575')){
 const expected=p.slug.startsWith('evergreen-')||p.slug.startsWith('gsa-')||p.slug.startsWith('intercamp-')||p.slug.startsWith('wolko-');
 if(found.has(p.slug)!==expected)throw Error('EN filter '+p.slug);
}
cs.country='TWN';if(filtered().some(p=>p.slug.startsWith('irobo-speed')||p.slug.startsWith('ntue-mandarin')))throw Error('unconfirmed Taiwan EN');
cs.country='';cs.language='';cs.child='both';if(filtered().some(p=>['computhink-roblox-teens','intercamp-seoul-winter','wolko-winter-english'].includes(p.slug)))throw Error('later age route');
""".replace('FUNCTIONS',funcs)
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(verified=True,events=3037,dossiers=575,new_dossiers=28,deepened_dossiers=1,unchanged_prior_events=2997,new_dated_rows=40,new_family_ics=23,family_ics=2279,source_urls=862,worldwide_complete=False)))
