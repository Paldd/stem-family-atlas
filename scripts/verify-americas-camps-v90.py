"""Independent date/price parsing and previous-worldwide-data preservation."""
import collections,datetime,hashlib,json,re,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v90'
BASE='21d9f87320b8d6b38a5724a3ce475e1c294e4c3b'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def before(f):return subprocess.check_output(['git','show',BASE+':'+f],cwd=ROOT)
def raw(k):return (PRIMARY/(k+'.txt')).read_text()
def compact(s):return re.sub(r'\s+','',s)
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
p={q['slug']:q for q in c['profiles']};op={q['slug']:q for q in b['camp_programmes']['profiles']}
assert len(ev)==len(d['events'])==3071 and len(old)==3037 and set(old)<=set(ev)
assert len(p)==len(c['profiles'])==594 and len(op)==575
assert [q['id'] for q in c['profiles'][:575]]==[q['id'] for q in b['camp_programmes']['profiles']]
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[k]==b[k],k
changed=[k for k,v in old.items() if v!=ev[k]]
assert len(changed)==7 and all(old[k].get('camp_dossier_slug')=='makemake' for k in changed)
for k in changed:
 for field in ['id','start','end','age','mat','osc','themes','languages','participation','source','camp_dossier_slug']:
  assert ev[k][field]==old[k][field],(k,field)
for slug,q in op.items():
 if slug!='makemake':assert p[slug]==q,slug
 else:
  for field in ['id','age','timing','family_fit','calendar_links','related_event_ids']:assert p[slug][field]==q[field],field
  assert [s['url'] for s in p[slug]['sources'][:-1]]==[s['url'] for s in q['sources']]
assert c['counts']['countries']==36 and c['counts']['swiss']==84 and c['counts']['source_urls']==893
assert len(c['shortlist'])==129 and c['shortlist'][:124]==b['camp_programmes']['shortlist']
assert c['gaps'][:-5]==b['camp_programmes']['gaps']
for s in c['shortlist'][-5:]:assert len(s['slugs'])==len(set(s['slugs'])) and all(k in p for k in s['slugs'])
fresh={k:q for k,q in p.items() if k not in op};new=[e for k,e in ev.items() if k not in old]
assert len(fresh)==19 and len(new)==34
assert [q['id'] for q in fresh.values()]==['CP%03d'%i for i in range(576,595)]
assert collections.Counter(q['iso'] for q in fresh.values())==dict(USA=12,CAN=3,MEX=1,CRI=2,CHL=1)
assert sum(e['block']=='Лагеря' for e in ev.values())==1740
assert len(c['generated_event_ids'])==1277 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==39
def rows(slug):return [e for e in new if e['camp_dossier_slug']==slug]
def eventld(key):
 html=(PRIMARY/(key+'.html')).read_text()
 scripts=re.findall(r'<script[^>]*type=["\x27]application/ld\+json["\x27][^>]*>(.*?)</script>',html,re.S)
 return next(v for s in scripts if (v:=json.loads(s)).get('@type')=='Event')
for slug,key in [('star-anibots','star-anibots'),('star-robot-gaming','star-gamebots'),('star-carbots','star-carbots'),('star-ecobots','star-ecobots')]:
 v=eventld(key);rr=rows(slug);assert len(rr)==1
 assert (rr[0]['start'],rr[0]['end'])==(v['startDate'][:10],v['endDate'][:10])
 assert 'Grades 1-2 or 3-6' in v['description'] and '10181 Finch Ave' in v['location']['address']
 assert sorted(float(q['price']) for q in v['offers']['offers'])==[399.75,461.25,563.75,666.25]
 assert all(x in compact(p[slug]['price']['label']) for x in ['399.75','461.25','563.75','666.25'])
 assert p[slug]['confirmed_instruction_languages']==[] and all(v['status']=='unknown' for v in p[slug]['family_fit'].values())
 assert 'ShowMore' in compact(p[slug]['programme']) and 'blocked-page' in p[slug]['programme']
v=eventld('star-battlebots');assert '11/23 - 11/26, 2026' in v['description'] and v['endDate'].startswith('2026-11-27')
assert not rows('star-battlebots') and not p['star-battlebots']['timing']['sessions']
assert all(x in raw('starcode') for x in ['English','Spanish','Russian'])
assert 'nofoodserved' in compact(p['star-anibots']['accommodation']).lower() or 'foodnotserved' in compact(p['star-anibots']['accommodation']).lower()
# RoboLabs source date pairs parsed independently, repeated only for3 named venues.
t=raw('robolabs-camps'); pairs=[]
for month,a,z in re.findall(r'(Nov|Dec)\s+(\d{1,2})\s*–\s*(?:(?:Nov|Dec)\s*)?(\d{1,2})',t):
 pair=(f'2026-{11 if month=="Nov" else 12:02d}-{int(a):02d}',f'2026-{11 if month=="Nov" else 12:02d}-{int(z):02d}')
 if pair not in pairs:pairs.append(pair)
assert len(pairs)==3 and collections.Counter((e['start'],e['end']) for e in rows('robolabs-holiday'))==collections.Counter({pair:3 for pair in pairs})
assert len({e['city'] for e in rows('robolabs-holiday')})==3
assert all(s in t for s in ['$417','$237','$556','$316','$20/hr'])
assert '2025' in t and 'kindergarten through 7th grade' in t and '1st to 12th grade' in t
assert p['robolabs-holiday']['confirmed_instruction_languages']==[]
# Selected browser excerpts are explicitly not a fullrawHTML snapshot.
t=raw('snap-greensboro-browser-excerpts');assert 'not a complete raw HTML snapshot' in t
months={n:i for i,n in enumerate(['January','February','March','April','May','June','July','August','September','October','November','December'],1)}
singles=[f'{y}-{months[m]:02d}-{int(a):02d}' for m,a,y in re.findall(r'^(\w+) (\d{1,2}), (202[67])$',t,re.M)]
# Two price deadlines share the format, so limit to the first10 schedule entries.
assert len(singles[:10])==10
assert sorted(e['start'] for e in rows('snap-greensboro-school-holidays'))==sorted(a for a in singles[:10] if a>='2026-10-05')
ranges=[(f'{y}-{months[m]:02d}-{int(a):02d}',f'{y}-{months[m]:02d}-{int(z):02d}') for m,a,z,y in re.findall(r'^(\w+) (\d{1,2})–(\d{1,2}), (202[67])$',t,re.M)]
assert collections.Counter(ranges)==collections.Counter((e['start'],e['end']) for e in rows('snap-greensboro-winter')+rows('snap-greensboro-spring'))
assert 'Four-day' in t and t.count('3 camp days')==2 and 'staff cannot assist with toileting needs' in t and 'staff cannot administer medication' in t
assert all(not p[k]['confirmed_instruction_languages'] for k in ['snap-greensboro-winter','snap-greensboro-spring','snap-greensboro-school-holidays'])
# Actual attendance from source month/day closures, not a broadholidayrange.
for slug,key in [('steamup-thanksgiving','steamup-thanks'),('steamup-winter','steamup-winter')]:
 t=raw(key);m,a,y,n,z,yy=re.search(r'Duration:\s*(\w+) (\d+), (2026) - (\w+) (\d+), (202[67])',t).groups()
 first=datetime.date(int(y),months[m],int(a));last=datetime.date(int(yy),months[n],int(z))
 closed_text=re.search(r'\(Closed (.*?)\)',t).group(1)
 closed={(int(m),int(d)) for m,d in re.findall(r'(\d{1,2})[/,](\d{1,2})',closed_text)}
 expected=[];dd=first
 while dd<=last:
  if dd.weekday()<5 and (dd.month,dd.day) not in closed:expected.append(dd.isoformat())
  dd+=datetime.timedelta(days=1)
 e=rows(slug)[0];assert e['date_scope']=='session_days' and [s['date'] for s in e['sessions']]==expected
 assert len(expected)==(4 if slug.endswith('thanksgiving') else 6)
 if slug.endswith('winter'):
  assert 'November 15, 2026' in t and e['deadline']=='2026-11-15'
t=raw('steamup-spring');assert 'March 15, 2027 - March 19, 2027' in t and 'K - 5th Grade' in t and '$250 per week' in t
assert (rows('steamup-spring')[0]['start'],rows('steamup-spring')[0]['end'])==('2027-03-15','2027-03-19')
for k in ['steamup-thanks','steamup-winter','steamup-spring']:assert '5 to 15' in raw(k) and ('3 to 15' in raw(k) or '3 through 15' in raw(k))
# Windows remainwindows: no invented individualcampdates.
for slug in ['stemrise-winter-roblox','stemrise-winter-ai','stemrise-winter-research','woods-amora-dominicalito']:
 assert p[slug]['timing']['precision']=='season_window' and not rows(slug) and not p[slug]['confirmed_instruction_languages']
assert 'Markham runs in-person' in raw('stemrise-winter') and 'online cohorts only' in raw('stemrise-winter')
assert 'Dec 20, 2026 – Jan 10, 2027' in raw('stemrise-winter')
assert 'Chinese' in raw('stemrise-refund') and 'prevail' in raw('stemrise-refund')
assert all(v['status']=='later' for v in p['stemrise-winter-research']['family_fit'].values())
# Mexican age/fees from exactlydatedcards; medicallimit, not deductibles.
t=raw('santa-summer');pairs=[(f'{y}-07-{int(a):02d}',f'{y}-07-{int(z):02d}') for a,z,y in re.findall(r'Del (\d+) al (\d+) de julio de (2027)',t)]
assert collections.Counter(pairs)==collections.Counter((e['start'],e['end']) for e in rows('santa-ursula-general'))
assert '$51,700 mxn' in t and '$98,500 MXN' in t and '7 a 15 años' in t
assert '$150,000 PESOS MEXICANOS' in raw('santa-terms') and 'NO CUBRE ENFERMEDADES' in raw('santa-terms')
su=p['santa-ursula-general'];assert '150000MXN' in compact(su['price']['extras']) and '10000' not in compact(su['price']['extras'])
assert not su['confirmed_instruction_languages'] and 51700*2-98500==4900
assert '10–16July' in compact(su['timing']['label']) and '17–23July' in compact(su['timing']['label'])
# Localprogramme/sport boundaries, currentoperationclosure, and actualClassic/Teen.
assert 'January 4 – February 6' in raw('amora-camp') and '2027' in raw('amora-camp') and 'Time\nTo be set' in raw('amora-camp')
assert 'ages 10 –13' in raw('woods-cr') and 'children ages 3 –13' in raw('woods-cr')
assert 'facilitadoras o instructoras' in raw('ucr-call') and 'año 2027' in raw('ucr-call')
assert 'Enero 11 - 15' in raw('real-madrid-week1') and 'Enero 18 - 22' in raw('real-madrid-week2')
assert 'Guácima Abajo' in raw('real-madrid-week1') and not p['avanza-real-madrid-cr']['confirmed_instruction_languages']
assert 'ceased operations effective immediately' in raw('ilac-current').lower()
assert not any('tamwood' in (q['provider']+' '+q['slug']).lower() for q in p.values())
assert 'presently in 2nd to 8th grade' in raw('makemake-rates') and 'presently in Grades 9–11' in raw('makemake-rates')
assert 'Round-trip bus transport from Santiago to camp.' in raw('makemake-rates') and 'Departs Day 1 at 1:00 PM' in raw('makemake-rates')
assert 'Before 20 December 2026' in raw('makemake-refund') and 'minus 21%' in raw('makemake-refund') and 'less 30%' in raw('makemake-refund')
assert 'All activities at Camp Makemake are in English' in raw('makemake-faq') and p['makemake']['confirmed_instruction_languages']==['EN']
assert len(rows('makemake-teen'))==2 and all(v['status']=='later' for v in p['makemake-teen']['family_fit'].values())
# PublicJSON, SQLite and idempotentbridge remain aligned.
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
for f,w in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/f).read_text())==w
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==3071 and con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==594;con.close()
def calendar(v):
 out={};t=v.decode().replace('\r\n ','').replace('\r\n\t','')
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={line.split(':',1)[0]:line.split(':',1)[1] for line in ch.split('END:VEVENT')[0].splitlines() if ':' in line}
  assert f['UID'] not in out;out[f['UID']]=f
 return out
expected=set()
for e in new:
 if e['camp_dossier_slug']=='makemake-teen':continue
 if e.get('date_scope')=='session_days':expected|={'stem-'+e['id']+'-'+s['date']+'@family-stem.local' for s in e['sessions']}
 else:expected.add('stem-'+e['id']+'@family-stem.local')
for f,total in [('STEM_подтвержденные_даты.ics',2320),('STEM_крупные_выставки.ics',104)]:
 prior=calendar(before('dist/downloads/'+f));now=calendar((ROOT/'dist/downloads'/f).read_bytes())
 assert set(prior)<=set(now) and len(now)==total
 for uid,v in prior.items():
  if any('stem-'+k+'@' in uid for k in changed):assert now[uid]['DTSTART;VALUE=DATE']==v['DTSTART;VALUE=DATE'];continue
  assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
 if total==2320:
  added=set(now)-set(prior);assert len(added)==41
  assert expected<=added and len(added-expected)==1
  # Individual winterdays include six visits plus one registrationdeadline, noholidays.
  win=rows('steamup-winter')[0];days={v['DTSTART;VALUE=DATE'] for uid,v in now.items() if uid.startswith('stem-'+win['id']+'-') and not uid.endswith('-deadline@family-stem.local')}
  assert days=={s['date'].replace('-','') for s in win['sessions']}
  assert added-expected=={'stem-'+win['id']+'-deadline@family-stem.local'}
  assert now['stem-'+win['id']+'-deadline@family-stem.local']['DTSTART;VALUE=DATE']=='20261115'
  assert not any(e['id'] in uid for e in rows('makemake-teen') for uid in now)
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==90
assert {q['id'] for q in bp['requirements']}<={q['id'] for q in plan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==bp[k],k
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert d['coverage_summary']['fully_audited_countries']==0 and plan['camp_catalog_integration']['dossiers']==594
for stem in ['americas-camp-audit-v90','americas-camp-source-receipts-v90']:
 v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
 assert not any(v['external_actions'].values())
 if 'sources' in v:
  assert len(v['sources'])==52 and sum(q.get('status')==200 for q in v['sources'])==45 and len(v['dossier_source_urls_added'])==31
  for q in v['sources']+v['browser_primary_reads']:
   if q.get('raw_filename'):assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
  assert v['browser_primary_reads'][0]['capture_kind']=='selected_observed_excerpts_not_full_html'
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_americas_camp_audit_v90.json' in js and 'STEM_asia_camp_audit_v89.json' in js
assert 'data-ui-version="90"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(line for line in js.splitlines() if line.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:'EN'};
FUNCTIONS
const found=new Set(filtered().map(p=>p.slug));
for(const p of guide.profiles.filter(p=>p.id>='CP576'&&p.id<='CP594')){if(found.has(p.slug)!==(p.slug==='makemake-teen'))throw Error('falseEN '+p.slug);}
cs.language='ES';if(filtered().some(p=>p.slug.startsWith('star-')||p.slug==='santa-ursula-general'))throw Error('site/application notES teaching');
cs.language='';cs.child='both';if(filtered().some(p=>['makemake-teen','stemrise-winter-research'].includes(p.slug)))throw Error('later age route');
""".replace('FUNCTIONS',funcs)
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(verified=True,events=3071,dossiers=594,new_dossiers=19,deepened_dossiers=1,new_calendar_rows=34,new_family_ics=41,corrected_prior_event_ids=len(changed),family_ics=2320,source_urls=893,worldwide_complete=False)))
