"""Primary date/fee boundaries, preservation, exports and family filters."""
import collections,datetime,hashlib,json,re,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v93'
BASE='b8d62c95ab3e34a15f9e389a957caca9792b3758'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def before(file):return subprocess.check_output(['git','show',BASE+':'+file],cwd=ROOT)
def raw(key):return (PRIMARY/(key+'.txt')).read_text()
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
op={p['slug']:p for p in b['camp_programmes']['profiles']};p={q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3121 and len(old)==3097 and set(old)<=set(ev)
assert all(ev[k]==v for k,v in old.items()),'Previous event changed'
assert len(p)==len(c['profiles'])==621 and len(op)==611
assert [q['id'] for q in c['profiles'][:611]]==[q['id'] for q in b['camp_programmes']['profiles']]
for slug,q in op.items():
 if slug!='ciberbots':assert p[slug]==q,slug
 else:
  for k in ['id','slug','iso','country','related_event_ids','calendar_links','confirmed_instruction_languages','price','accommodation']:assert p[slug].get(k)==q.get(k),(slug,k)
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[k]==b[k],k
assert c['counts']['countries']==37 and c['counts']['swiss']==85 and c['counts']['source_urls']==965
assert len(c['shortlist'])==140 and c['shortlist'][:137]==b['camp_programmes']['shortlist']
assert c['gaps'][:-4]==b['camp_programmes']['gaps']
for q in c['shortlist'][-3:]:assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
assert not any(any(s.startswith('icc-young-') for s in q['slugs']) for q in c['shortlist'])
fresh={s:q for s,q in p.items() if s not in op};new=[e for k,e in ev.items() if k not in old]
assert len(fresh)==10 and len(new)==24 and [q['id'] for q in fresh.values()]==['CP%03d'%i for i in range(612,622)]
assert collections.Counter(q['iso'] for q in fresh.values())==dict(CRI=1,MEX=3,CAN=1,USA=5)
assert collections.Counter(e['camp_dossier_slug'] for e in new)==dict([('tamarindo-elementary',9),('coyote-short',2),('coyote-junior',1),('cube-winter-makers',1),('icc-young-drone',3),('icc-young-engineering',2),('icc-young-vex',2),('icc-young-ai',2),('icc-young-raspberry',2)])
assert sum(e['block']=='Лагеря' for e in ev.values())==1790
assert len(c['generated_event_ids'])==1327 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==39
def rows(slug):return [e for e in new if e['camp_dossier_slug']==slug]
for e in new:
 assert e['start']>=d['asof'] and e['start']<=e['end']
 if e['deadline']:datetime.date.fromisoformat(e['deadline'])
# Parse only the current2027FAQ list; hidden2026weeks are independently present.
t=raw('tamarindo-kids');assert 'Monday June 15, 2026' in t and '2027 kids weeks:' in t
part=t.split('2027 kids weeks:',1)[1]
starts=[datetime.datetime.strptime(a+' '+n+' '+y,'%B %d %Y').date() for a,n,y in re.findall(r'Week \d+: Monday, (June|July|August) (\d+), (2027)',part)]
assert len(starts)==9 and {a.isoformat() for a in starts}=={e['start'] for e in rows('tamarindo-elementary')}
for e in rows('tamarindo-elementary'):
 a=datetime.date.fromisoformat(e['start']);z=datetime.date.fromisoformat(e['end'])
 assert a.weekday()==0 and z==a+datetime.timedelta(days=4) and e['date_precision']=='published_rule' and e['date_rule']
 assert e['languages']==['ES'] and e['language_mode']=='language_lessons' and not e['deadline']
for value in ['10 hours/week','(Ages 5–10)','$797','Monday through Friday']:assert value in t,value
assert p['tamarindo-elementary']['language_evidence_role']=='language_lessons'
terms=raw('tamarindo-terms');assert 'November 1st, 2025' in terms and 'end of the 2026 camp season' in terms and '$100 (50%' in terms
for value in ['$155','$170','$205','6 nights','14+ nights = 15%','28+ nights = 30%']:assert value in raw('tamarindo-lodging'),value
assert 2*797+6*155==2524 and '2 524' in p['tamarindo-elementary']['price']['label'] and '2027' in p['tamarindo-elementary']['price']['deposit']
# Current rendered primary observations explicitly differ from the server draft.
observ=json.loads((PRIMARY/'rendered-observations.json').read_text());render={q['key']:q for q in observ['observations']}
assert 'July 5-16, 2027' in render['harmony-rendered-current']['observed_text']
assert 'REF.2026' in render['coyote-rendered-current']['observed_text'] and '6500' in render['coyote-rendered-current']['observed_text']
for value in ['$7,100','$5,300','TBD']:assert value in raw('coyote-home'),value
assert {(e['start'],e['end']) for e in rows('coyote-short')}=={('2026-10-30','2026-11-02'),('2026-12-21','2026-12-23')}
assert {(e['start'],e['end']) for e in rows('coyote-junior')}=={('2027-03-29','2027-04-03')}
assert not p['coyote-pro']['calendar_links'] and p['coyote-pro']['family_fit']['oscar']['status']=='later'
for slug in ['coyote-short','coyote-junior','coyote-pro']:
 assert not p[slug]['confirmed_instruction_languages']
 assert '30%' in p[slug]['price']['deposit'] and 'ваучером6' in p[slug]['price']['deposit'].replace(' ','')
 assert '4–6' in p[slug]['accommodation'] and '3–4' in p[slug]['accommodation']
 assert '5–18' in p[slug]['price']['extras'] and all(not e['deadline'] for e in rows(slug))
assert p['coyote-junior']['availability']['status']==p['coyote-pro']['availability']['status']=='waitlist'
assert 'REF.2026' in p['coyote-junior']['price']['label'] and '8 500' in p['coyote-pro']['price']['label']
assert '6-летия' in p['coyote-short']['family_fit']['oscar']['detail']
# Independently parse all11own cards, actualdates/prices/deadlines and copieddancebody.
keys=['icc-drone','icc-engineering','icc-vex','icc-ai','icc-raspberry']+['icc-y'+str(n) for n in range(6,12)]
icc=[e for e in new if e['camp_dossier_slug'].startswith('icc-young-')]
assert len(icc)==11
for key in keys:
 t=raw(key);m=re.search(r'Dates:\s*(\d+/\d+/2027).*? - (\d+/\d+/2027)',t)
 assert m,key
 pair=tuple(datetime.datetime.strptime(a,'%m/%d/%Y').date().isoformat() for a in m.groups())
 e=next(e for e in icc if (e['start'],e['end'])==pair)
 deadline=re.search(r'Registration will end on (\d+/\d+/2027) at 10:00 AM',t);assert deadline,key
 assert datetime.datetime.strptime(deadline[1],'%m/%d/%Y').date().isoformat()==e['deadline']==e['start']
 for value in ['$429','$419','Ages 5 - 14','$70','$99','$60','This session has openings','Bolly']:assert value in t,(key,value)
 assert not e['languages'] and e['language_mode']=='unconfirmed' and e['availability']['status']=='open'
 assert 'конфликтует' in e['proof']
assert 429+70+60+99==658 and 2*658==1316
for slug in [s for s in fresh if s.startswith('icc-young-')]:
 assert '1 316' in p[slug]['price']['label'] and 'не установлена' in p[slug]['price']['deposit']
 assert 'НЕ подтверждены' in p[slug]['programme'] and not p[slug]['confirmed_instruction_languages']
for key in ['icc-refund','icc-faq']:assert len(raw(key).splitlines())<35
# Cube is actualwinter rather than regularclasses, schoolgrade rather thanbirthyear.
t=raw('cube-winter')
for value in ['December 21-23, 2026','$255 + HST','$275 + HST','$112.50 + HST','going into Grade 2 as of September 2026','March Break 2026','short answer is no','$65']:assert value in t,value
q=p['cube-winter-makers'];assert 275+112.5==387.5 and '387.50' in q['price']['label']
assert all(q['family_fit'][k]['status']=='unknown' for k in ['matvey','oscar']) and not q['confirmed_instruction_languages']
assert '65 Glen Manor Drive' in t and 'July 1, 2026' in t and rows(q['slug'])[0]['date_scope']=='camp_session'
assert {(e['start'],e['end']) for e in rows(q['slug'])}=={('2026-12-21','2026-12-23')}
assert all(p['ciberbots']['family_fit'][k]['status']=='unknown' for k in ['matvey','oscar'])
assert p['ciberbots']['timing']['status']=='partial_2026_27' and not p['ciberbots']['calendar_links']
for value in ['2027','Diciembre 2026','Pascua','Verano']:assert value in raw('ciberbots-services'),value
assert '9.048,50' in raw('nr-2027-contract') and 'segunda semana' in raw('nr-2027-contract')
assert '7 - 11: Christmas Camp' in raw('oaktree-calendar') or '7 – 11: Christmas Camp' in raw('oaktree-calendar') or '7 - 11' in raw('oaktree-calendar')
assert all(s not in fresh for s in ['harmony','oaktree','nr-holidays','robotiki'])
# Bridge idempotence and complete data/SQLite/export agreement, oldICS preserved.
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
for file,want in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/file).read_text())==want
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert {json.loads(v)['id']:json.loads(v) for v, in con.execute('SELECT record_json FROM events')}==ev
assert {json.loads(v)['slug']:json.loads(v) for v, in con.execute('SELECT record_json FROM camp_programmes')}==p;con.close()
def calendar(value):
 out={};t=value.decode().replace('\r\n ','').replace('\r\n\t','')
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={line.split(':',1)[0]:line.split(':',1)[1] for line in ch.split('END:VEVENT')[0].splitlines() if ':' in line}
  assert f['UID'] not in out;out[f['UID']]=f
 return out
for file,total in [('STEM_подтвержденные_даты.ics',2382),('STEM_крупные_выставки.ics',104)]:
 prior=calendar(before('dist/downloads/'+file));now=calendar((ROOT/'dist/downloads'/file).read_bytes());assert set(prior)<=set(now) and len(now)==total
 for uid,v in prior.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
 if total==2382:
  expected={'stem-'+e['id']+'@family-stem.local' for e in new}|{'stem-'+e['id']+'-deadline@family-stem.local' for e in icc}
  assert set(now)-set(prior)==expected and len(expected)==35
  for e in icc:assert now['stem-'+e['id']+'-deadline@family-stem.local']['DTSTART;VALUE=DATE']==e['deadline'].replace('-','')
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==93
assert {q['id'] for q in bp['requirements']}<={q['id'] for q in plan['requirements']}
for key in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[key]==bp[key],key
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['americas-camp-audit-v93','americas-camp-source-receipts-v93']:
 v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
 assert not any(v['external_actions'].values())
 if 'sources' in v:
  assert len(v['sources'])==37 and sum(q.get('status')==200 for q in v['sources'])==29 and len(v['dossier_source_urls_added'])==24
  assert sum(q.get('raw_filename','').endswith('.pdf') for q in v['sources'])==2
  for q in v['sources']+v['additional_retrieval_methods']:
   if q.get('raw_filename'):assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
  assert len(v['additional_retrieval_methods'])==3 and all(q['retrieval_method']=='rendered_primary_observation' for q in v['additional_retrieval_methods'])
assert len(list(PRIMARY.glob('*page*.png')))==3
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_americas_camp_audit_v93.json' in js and 'Лист ожидания' in js and 'data-ui-version="93"' in (ROOT/'dist/index.html').read_text()
assert "!['closed','not_open_yet','waitlist'].includes(p.availability?.status)" in js
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(line for line in js.splitlines() if line.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:'EN'};
FUNCTIONS
const found=new Set(filtered().map(p=>p.slug));
for(const p of guide.profiles.filter(p=>p.id>='CP612'&&p.id<='CP621'))if(found.has(p.slug))throw Error('falseEN '+p.slug);
cs.language='ES';const es=new Set(filtered().map(p=>p.slug));
for(const p of guide.profiles.filter(p=>p.id>='CP612'&&p.id<='CP621'))if(es.has(p.slug)!==(p.slug==='tamarindo-elementary'))throw Error('falseES '+p.slug);
cs.language='';cs.child='both';const both=new Set(filtered().map(p=>p.slug));
for(const s of ['ciberbots','coyote-pro','cube-winter-makers'])if(both.has(s))throw Error('falseBoth '+s);
for(const s of ['tamarindo-elementary','coyote-short','coyote-junior'])if(!both.has(s))throw Error('missingBoth '+s);
""".replace('FUNCTIONS',funcs)
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(verified=True,events=3121,dossiers=621,new_dossiers=10,deepened_dossiers=1,new_calendar_rows=24,new_family_ics=35,prior_events_unchanged=3097,family_ics=2382,source_urls=965,worldwide_complete=False)))
