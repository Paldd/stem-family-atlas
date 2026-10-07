"""Independent primary-evidence, age/language, preservation and payload checks."""
import collections,datetime,hashlib,json,re,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v92'
BASE='898c56aeebb81820bd3e2dda84962dff563c5fd7'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def before(file):return subprocess.check_output(['git','show',BASE+':'+file],cwd=ROOT)
def raw(key):return (PRIMARY/(key+'.txt')).read_text()
def compact(value):return re.sub(r'\s+','',value)
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
op={p['slug']:p for p in b['camp_programmes']['profiles']};p={q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3097 and len(old)==3075 and set(old)<=set(ev)
assert all(ev[k]==v for k,v in old.items()),'previous events changed'
assert len(p)==len(c['profiles'])==611 and len(op)==601
assert [q['id'] for q in c['profiles'][:601]]==[q['id'] for q in b['camp_programmes']['profiles']]
for slug,q in op.items():
 if slug!='camp-taiwan':assert p[slug]==q,slug
 else:
  for k in ['id','slug','iso','country','related_event_ids','confirmed_instruction_languages','language_evidence_role']:assert p[slug].get(k)==q.get(k),(slug,k)
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[k]==b[k],k
assert c['counts']['countries']==37 and c['counts']['swiss']==85 and c['counts']['source_urls']==941
assert len(c['shortlist'])==137 and c['shortlist'][:132]==b['camp_programmes']['shortlist']
assert c['gaps'][:-5]==b['camp_programmes']['gaps']
for q in c['shortlist'][-5:]:assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
fresh={s:q for s,q in p.items() if s not in op};new=[e for k,e in ev.items() if k not in old]
assert len(fresh)==10 and len(new)==22
assert [q['id'] for q in fresh.values()]==['CP%03d'%i for i in range(602,612)]
assert collections.Counter(q['iso'] for q in fresh.values())==dict(SGP=4,KOR=1,AUS=2,JPN=2,PHL=1)
assert collections.Counter(e['camp_dossier_slug'] for e in new)==dict([('gungho-general',4),('gungho-santa-steam',1),('gungho-treasure',1),('gungho-adventure',1),('british-council-korea-winter-kinder',1),('imagine-gold-coast-junior',1),('imagine-brisbane-junior',1),('ugaku-nasu',2),('ugaku-okinawa',2),('ugaku-cebu',2),('camp-taiwan',6)])
assert sum(e['block']=='Лагеря' for e in ev.values())==1766
assert len(c['generated_event_ids'])==1303 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==39
def rows(slug):return [e for e in new if e['camp_dossier_slug']==slug]
for e in new:
 assert e['start']>=d['asof'] and e['start']<=e['end']
 if e['deadline']:datetime.date.fromisoformat(e['deadline'])
# Independently parse the printed2027 calendar; not an implied weekly recurrence.
t=raw('camp-taiwan-summer');assert 'Camp Taiwan 2027 English Summer Camp Schedule' in t
pairs=[(f'2027-{int(m):02d}-{int(a):02d}',f'2027-{int(n):02d}-{int(z):02d}') for m,a,n,z in re.findall(r'(\d{1,2})/(\d{1,2}) to (\d{1,2})/(\d{1,2})',t)]
assert len(pairs)==6 and set(pairs)=={(e['start'],e['end']) for e in rows('camp-taiwan')}
assert t.count('Not yet open')==6 and ('2027-08-09','2027-08-14') not in pairs
assert p['camp-taiwan']['availability']['status']=='not_open_yet'
assert all(e['availability']['status']=='not_open_yet' for e in rows('camp-taiwan'))
for value in ['24 000','23 000','26 000']:assert value in p['camp-taiwan']['price']['label']
for value in ['NT$24000','NT$23000','NT$26000']:assert value in t,value
notice=raw('camp-taiwan-notice-pdf')
for text in ['English version is official','14 days','NT$1,000','credit 5%','at least one guardian will be in Taiwan','90% refund','70% refund','50% refund','30% refund']:assert text in notice,text
assert 'уже входят' in p['camp-taiwan']['price']['included'] and '5%' in p['camp-taiwan']['price']['extras']
assert '21–29 / 11–20 / 4–10' in p['camp-taiwan']['price']['deposit'] and 'опекун' in p['camp-taiwan']['accommodation']
# Own booking cards: parse selectedcurrentdates, fees and ageconflicts, not hiddenmessages.
months={'Oct':10,'Nov':11,'Dec':12}
for key,slug in [('beach','gungho-general'),('wilderness','gungho-general'),('christmas','gungho-general'),('xtra','gungho-general'),('steam','gungho-santa-steam'),('treasure','gungho-treasure'),('adventure','gungho-adventure')]:
 t=raw('gungho-register-'+key)
 dates=re.search(r'(Oct|Nov|Dec) (\d{1,2}), (2026) to (Oct|Nov|Dec) (\d{1,2}), (2026)',t)
 assert dates,key
 m,a,y,n,z,yy=dates.groups();pair=(f'{y}-{months[m]:02d}-{int(a):02d}',f'{yy}-{months[n]:02d}-{int(z):02d}')
 assert pair in {(e['start'],e['end']) for e in rows(slug)},key
 for rate in ([600,660] if key=='beach' else [408,430] if key=='xtra' else [640,690] if key=='adventure' else [620,660]):assert re.search(r'SGD\s*'+str(rate)+r'\.00',t),(key,rate)
 assert not p[slug]['confirmed_instruction_languages'] and all(e['languages']==[] for e in rows(slug))
assert 'November 23, 2011 and November 22, 2017' in raw('gungho-register-adventure')
assert '5-8' in raw('gungho-register-treasure') and '5-12' in raw('gungho-register-treasure')
assert '5-10' in raw('gungho-register-christmas') and '5-12' in raw('gungho-register-christmas')
assert p['gungho-treasure']['family_fit']['matvey']['status']=='unknown'
assert p['gungho-adventure']['family_fit']['oscar']['status']=='later'
assert all(not e['deadline'] for e in new if e['camp_dossier_slug'].startswith('gungho-') and not e['id'].endswith('-xtra'))
xtra=next(e for e in rows('gungho-general') if e['id'].endswith('-xtra'));assert xtra['deadline']=='2026-12-18'
assert 'Dec 18, 2026 @ 11:55 PM' in raw('gungho-register-xtra')
for slug in [s for s in fresh if s.startswith('gungho-')]:assert '3%' in p[slug]['price']['extras'] and '12 месяцев' in p[slug]['price']['deposit'] and '12 месяцев' in p[slug]['accommodation']
# BritishCouncil's source retrieval method and winterfee boundary.
t=json.loads((PRIMARY/'british-council-web.json').read_text())
for text in ['Jan 11 (Mon)','Jan 22 (Fri)','2020','2021','1,516,200','1,020,300']:assert text in t,text
assert 'September 2026–February 2027' in t and 'Priority for current students' in t
q=p['british-council-korea-winter-kinder'];assert q['language_evidence_role']=='language_lessons'
assert q['family_fit']['matvey']['status']=='later' and q['family_fit']['oscar']['status']=='conditional'
assert 'не цена' in q['price']['label'] and rows(q['slug'])[0]['date_scope']=='day_camp_window'
# Two flyers are2027 tuition, while actual homestay fee sheets are2026.
for key,slug in [('imagine-gc-flyer','imagine-gold-coast-junior'),('imagine-bne-flyer','imagine-brisbane-junior')]:
 t=raw(key);assert '11th January 2027 - 12th February 2027' in t
 for value in ['$250','$800','$150','6-11','12-16','Australia Day']:assert value in t,(key,value)
 for weeks,total in [(1,1200),(2,2150),(5,5000)]:assert 250+(800+150)*weeks==total and f'{total:,}'.replace(',',' ') in p[slug]['price']['label']
 assert p[slug]['language_evidence_role']=='language_lessons' and rows(slug)[0]['date_scope']=='day_camp_window'
 assert rows(slug)[0]['attendance_weekdays']==['MO','TU','WE','TH','FR'] and rows(slug)[0]['deadline']==''
 assert '8–17' in p[slug]['accommodation'] and '2026' in p[slug]['price']['extras'] and '2027' in p[slug]['price']['extras']
assert 'GOLD COAST 2026' in raw('imagine-homestay-bne') and 'BRISBANE 2026' in raw('imagine-homestay-bne-actual')
for key in ['imagine-homestay-bne','imagine-homestay-bne-actual']:
 for value in ['$660','$1310','2 parents + 2 children']:assert value in raw(key).replace(',',''),(key,value)
assert '2025' in raw('imagine-fee-2026') and '2026' in raw('imagine-homestay-gc')
# Seasonalplaces/pricesandgrades are independently anchored to the ownJapanesepages.
for slug,key,base in [('ugaku-nasu','ugaku-nasu',159800),('ugaku-okinawa','ugaku-okinawa',139800),('ugaku-cebu','ugaku-cebu',139800)]:
 t=raw(key);assert '2027年3月28日' in t or '2027.3.28' in t
 assert '199,800' in t and '30,000' in t
 for child in ['matvey','oscar']:assert p[slug]['family_fit'][child]['status']=='unknown'
 assert p[slug]['language_evidence_role']=='camp_life'
 assert {(e['start'],e['end']) for e in rows(slug)}=={('2026-12-26','2026-12-30'),('2027-03-28','2027-04-03')}
 assert f'{base+30000:,}'.replace(',',' ') in p[slug]['price']['label'] and '229 800' in p[slug]['price']['label']
 assert '4 недели' in p[slug]['price']['deposit'] and '5 или 7' in p[slug]['price']['deposit']
assert '159,800円（税込）' in raw('ugaku-own-winter-prices') and '国立那須甲子青少年自然の家' in raw('ugaku-nasu')
assert '福島県西郷村' in raw('ugaku-nasu') and ('福島' in rows('ugaku-nasu')[1]['city'] or 'Fukushima' in rows('ugaku-nasu')[1]['city'])
assert 'マンツーマンレッスン14時間' in raw('ugaku-cebu') and '空港⇔校舎の送迎込み' in raw('ugaku-cebu')
assert '4週間以上' in raw('ugaku-guarantee') and '3日以内' in raw('ugaku-guarantee')
for value in ['90','60','45','50％','70％','サービス料金及び関連費用の全額']:assert value in raw('ugaku-cancel')
# Database, exports, bridge and calendars must agree; all oldICS exceptDTSTAMP preserved.
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
for file,total in [('STEM_подтвержденные_даты.ics',2347),('STEM_крупные_выставки.ics',104)]:
 prior=calendar(before('dist/downloads/'+file));now=calendar((ROOT/'dist/downloads'/file).read_bytes());assert set(prior)<=set(now) and len(now)==total
 for uid,v in prior.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
 if total==2347:
  expected={'stem-'+e['id']+'@family-stem.local' for e in new}|{'stem-'+xtra['id']+'-deadline@family-stem.local'}
  assert set(now)-set(prior)==expected
  assert now['stem-'+xtra['id']+'-deadline@family-stem.local']['DTSTART;VALUE=DATE']=='20261218'
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==92
assert {q['id'] for q in bp['requirements']}<={q['id'] for q in plan['requirements']}
for key in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[key]==bp[key],key
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert d['coverage_summary']['fully_audited_countries']==0 and plan['camp_catalog_integration']['dossiers']==611
for stem in ['asia-camp-audit-v92','asia-camp-source-receipts-v92']:
 v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
 assert not any(v['external_actions'].values())
 if 'sources' in v:
  assert len(v['sources'])==49 and sum(q.get('status')==200 for q in v['sources'])==46 and len(v['dossier_source_urls_added'])==23
  assert sum(q.get('raw_filename','').endswith('.pdf') for q in v['sources'])==8
  for q in v['sources']+v['additional_retrieval_methods']:
   if q.get('raw_filename'):assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
  assert len(v['additional_retrieval_methods'])==1 and v['additional_retrieval_methods'][0]['retrieval_method']=='web_extract'
assert len(list(PRIMARY.glob('*page*.png')))==11
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_asia_camp_audit_v92.json' in js and 'STEM_europe_camp_audit_v91.json' in js
assert 'not_open_yet' in js and 'data-ui-version="92"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(line for line in js.splitlines() if line.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:'EN'};
FUNCTIONS
const found=new Set(filtered().map(p=>p.slug));
for(const p of guide.profiles.filter(p=>p.id>='CP602'&&p.id<='CP611')){if(found.has(p.slug)!==['british-council-korea-winter-kinder','imagine-gold-coast-junior','imagine-brisbane-junior','ugaku-nasu','ugaku-okinawa','ugaku-cebu'].includes(p.slug))throw Error('falseEN '+p.slug);}
cs.language='';cs.child='both';const both=new Set(filtered().map(p=>p.slug));
for(const slug of ['ugaku-nasu','ugaku-okinawa','ugaku-cebu','gungho-adventure','gungho-treasure','british-council-korea-winter-kinder'])if(both.has(slug))throw Error('falseBoth '+slug);
for(const slug of ['gungho-general','gungho-santa-steam','imagine-gold-coast-junior','imagine-brisbane-junior'])if(!both.has(slug))throw Error('missingBoth '+slug);
""".replace('FUNCTIONS',funcs)
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(verified=True,events=3097,dossiers=611,new_dossiers=10,deepened_dossiers=1,new_calendar_rows=22,new_family_ics=23,prior_events_unchanged=3075,family_ics=2347,source_urls=941,worldwide_complete=False)))
