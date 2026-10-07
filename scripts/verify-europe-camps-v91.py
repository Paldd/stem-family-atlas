"""Independently check source dates/fees/age gates, preservation and published payloads."""
import collections,hashlib,json,re,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v91'
BASE='0465a462d6a769284b883c05d4e8552c9e345da9'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def before(f):return subprocess.check_output(['git','show',BASE+':'+f],cwd=ROOT)
def raw(k):return (PRIMARY/(k+'.txt')).read_text()
def compact(s):return re.sub(r'\s+','',s)
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
p={q['slug']:q for q in c['profiles']};op={q['slug']:q for q in b['camp_programmes']['profiles']}
assert len(ev)==len(d['events'])==3075 and len(old)==3071 and set(old)<=set(ev)
assert len(p)==len(c['profiles'])==601 and len(op)==594
assert [q['id'] for q in c['profiles'][:594]]==[q['id'] for q in b['camp_programmes']['profiles']]
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[k]==b[k],k
deepened={'las','prefleuri','natuk-robotics'}
for slug,q in op.items():
 if slug not in deepened:assert p[slug]==q,slug
 else:
  for field in ['id','slug','iso','country','timing','calendar_links','related_event_ids']:assert p[slug][field]==q[field],(slug,field)
changed=[k for k,v in old.items() if v!=ev[k]]
assert len(changed)==2 and all(old[k].get('camp_dossier_slug')=='las' for k in changed)
for k in changed:
 for field in ['id','start','end','themes','participation','source','camp_dossier_slug']:assert ev[k][field]==old[k][field],(k,field)
 assert ev[k]['osc']=='Нет сейчас; будущая возрастная ступень' and ev[k]['languages']==['EN'] and ev[k]['language_mode']=='camp_life'
assert c['counts']['countries']==36 and c['counts']['swiss']==85 and c['counts']['source_urls']==918
assert len(c['shortlist'])==132 and c['shortlist'][:129]==b['camp_programmes']['shortlist']
assert c['gaps'][:-3]==b['camp_programmes']['gaps']
for s in c['shortlist'][-3:]:assert len(s['slugs'])==len(set(s['slugs'])) and all(k in p for k in s['slugs'])
fresh={k:q for k,q in p.items() if k not in op};new=[e for k,e in ev.items() if k not in old]
assert len(fresh)==7 and len(new)==4
assert [q['id'] for q in fresh.values()]==['CP%03d'%i for i in range(595,602)]
assert collections.Counter(q['iso'] for q in fresh.values())==dict(CHE=1,ESP=5,FRA=1)
assert sum(e['block']=='Лагеря' for e in ev.values())==1744
assert len(c['generated_event_ids'])==1281 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==39
def rows(slug):return [e for e in new if e['camp_dossier_slug']==slug]
# Parse the operator's printed2027 schedule separately from authored dates.
t=raw('las-fees');assert 'LAS Summer 2027' in t
months={'June':6,'July':7,'August':8}
pairs=[(f'2027-{months[m]:02d}-{int(a):02d}',f'2027-{months[n]:02d}-{int(z):02d}') for m,a,n,z in re.findall(r'(June|July|August)\s+(\d{1,2})\s*-\s*(June|July|August)\s+(\d{1,2})',t)]
assert len(pairs)==2 and set(pairs)=={(e['start'],e['end']) for e in rows('las-ai-python')}
assert 'Junior Program: Ages 9-12' in raw('las-residential') and 'SENIOR PROGRAM + AGES 13-16' in raw('las-flyer-pdf')
assert '09:00 - 12:00' in raw('las-flyer-pdf') and 'General Booking Conditions 2026' in raw('las-terms-pdf')
assert 'May 15, 2026' in raw('las-terms-pdf') and 'non-refundable' in raw('las-terms-pdf')
assert 'Coming Soon' in raw('las-register') and 'original, fully functional Python application' in raw('las-morning')
assert 'Family' in raw('las-residential') and 'two or three counselors' in raw('las-residential')
assert p['las']['family_fit']['oscar']['status']==p['las-ai-python']['family_fit']['oscar']['status']=='later'
assert p['las-ai-python']['language_evidence_role']=='camp_life' and p['las-ai-python']['themes']==['coding','ai','engineering']
assert 'prerequisite' in p['las']['questions'][0] and '2026' in p['las-ai-python']['price']['deposit']
# Full older fee table and cancellation boundaries remain distinct from the new season.
t=raw('prefleuri-fees');assert 'Summer 2026' in t and 'Only one reduction possible' in t
for value in ["5'550","8'150","9'990","12'235","14'400","3'250","4'770","6'240","7'650","9'000"]:assert value in t,value
assert 'No visits are permitted without prior request' in raw('prefleuri-terms')
assert 'Cancellation 60 to 45 days before arrival' in raw('prefleuri-terms') and 'More than 60 days before arrival' in raw('prefleuri-terms')
assert p['prefleuri']['price']['year']==2026 and not p['prefleuri']['confirmed_instruction_languages']
assert p['prefleuri']['timing']['precision']=='season_window'
# Numeric HES price actually found, but archived dates/transport conflicts not repaired by guess.
t=raw('hes-price-detail');base=[int(x) for x in re.search(r'Precio base\s+(\d+)\s+(\d+)\s+(\d+)',t).groups()]
registration=int(re.search(r'Inscripción\s+(\d+)',t).group(1));robot=int(re.search(r'DISCOVERY - ROBOTICS - CRAFTS\s*\+(\d+)',t).group(1))
assert base==[655,1195,1750] and registration+base[0]+robot==855
assert '+125' in t and registration+base[0]+robot+robot==905 and registration+base[0]+robot+125==980
assert 'Hotel Trainera' in raw('hes-location') and 'Esterri' in raw('hes-catalog-pdf') and 'Euro Ski' in raw('hes-robotics')
assert '16:00-19:00' in raw('hes-catalog-pdf') and 'Camp de 6 a 16 años' in raw('hes-catalog-pdf')
assert '4 participantes' in raw('hes-guide-pdf') and '5€' in compact(raw('hes-guide-pdf'))
assert p['natuk-robotics']['iso']=='ESP' and p['natuk-robotics']['price']['year']==2026 and not p['natuk-robotics']['timing']['sessions']
# Course-level age/price tiers are not copied from after-school tuition or Spanish-site language.
for slug,key,age,capacity in [('ischool-constructors','ischool-constructors','De 6 a 8 años','12 plazas/turno'),('ischool-creators','ischool-creators','A partir de los 9 años','10 plazas/turno'),('ischool-minecraft','ischool-minecraft','Desde los 8 años','16 plazas/turno')]:
 t=raw(key);assert age in t and capacity in t and '25 horas' in t and '¡gratis!' in t
 assert not p[slug]['confirmed_instruction_languages'] and p[slug]['price']['year']==2026 and not rows(slug)
 for val in ['139 euros','239 euros','335 euros','125 euros','225 euros','320 euros']:assert val in t
assert '9 a 12 años' in raw('ischool-creators') and 'Intermedio' in raw('ischool-minecraft')
assert p['ischool-constructors']['family_fit']['matvey']['status']=='later' and p['ischool-creators']['family_fit']['oscar']['status']=='later'
assert '405 euros' in raw('ischool-terms') and '423 euros' in raw('ischool-terms') and 'annual' in p['ischool-creators']['sources'][2]['title']
# Visually inspected obsolete hidden PDF lines never become English/grade/calendar evidence.
assert 'INTENSIVOS100%INGLÉS' in compact(raw('faisl-brochure')) and 'Primaria' in raw('faisl-brochure')
assert 'Verano 2026' in raw('faisl-form-pdf') and '70 €' in raw('faisl-form-pdf') and '40 €' in raw('faisl-form-pdf')
assert 'mayor de 6 años' in raw('faisl-school')
assert not p['faisl-salamanca-summer']['confirmed_instruction_languages'] and 'не доказательство' in p['faisl-salamanca-summer']['language']
assert not rows('faisl-salamanca-summer') and all(z<'2026-10-05' for a,z in p['faisl-salamanca-summer']['timing']['sessions'])
assert 'Robótica en Inglés' in raw('technomatic-camps') and 'Verano 2026' in raw('technomatic-camps')
assert all(x in raw('technomatic-camps') for x in ['95€','170€','125€','215€','50€/sem','70€/sem'])
assert p['technomatic-english-tech']['confirmed_instruction_languages']==['EN'] and not rows('technomatic-english-tech')
# Actual future boarding table, not old PDF/programme header or aggregator prices.
t=raw('action-saint-pardoux');dates=re.findall(r'\b(\d{2})/(\d{2})/(2026)\b',t)
dates=sorted({f'{y}-{m}-{a}' for a,m,y in dates});assert len(dates)==4
assert [(e['start'],e['end']) for e in rows('action-american-saint-pardoux')]==list(zip(dates[::2],dates[1::2]))
assert '8 - 10' in t and '11 - 14' in t and '7 à 14 ans' in t
assert 'DATES DES SÉJOURS 2025' in raw('action-program-body-pdf') and '8 avril 2019' in raw('action-cgv-pdf')
assert 'un mois avant le départ' in raw('action-conditions') and 'sans transport aérien' in raw('action-conditions')
assert p['action-american-saint-pardoux']['family_fit']['oscar']['status']=='later' and 'personalized quote' in p['action-american-saint-pardoux']['price']['label']
for key in ['action-bretagne','action-winter','action-roches']:assert 'Ce centre n’a pas de séjour en ce moment' in raw(key)
assert not any(k in p for k in ['action-american-bretagne','action-american-winter-auvergne','action-american-roches'])
# All datasets agree; integration remains idempotent, all existing calendars retained.
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
for f,w in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/f).read_text())==w
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert {json.loads(v)['id']:json.loads(v) for v, in con.execute('SELECT record_json FROM events')}==ev
assert {json.loads(v)['slug']:json.loads(v) for v, in con.execute('SELECT record_json FROM camp_programmes')}==p;con.close()
def calendar(v):
 out={};t=v.decode().replace('\r\n ','').replace('\r\n\t','')
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={line.split(':',1)[0]:line.split(':',1)[1] for line in ch.split('END:VEVENT')[0].splitlines() if ':' in line}
  assert f['UID'] not in out;out[f['UID']]=f
 return out
for f,total in [('STEM_подтвержденные_даты.ics',2324),('STEM_крупные_выставки.ics',104)]:
 prior=calendar(before('dist/downloads/'+f));now=calendar((ROOT/'dist/downloads'/f).read_bytes());assert set(prior)<=set(now) and len(now)==total
 for uid,v in prior.items():
  if any('stem-'+k+'@' in uid for k in changed):assert now[uid]['DTSTART;VALUE=DATE']==v['DTSTART;VALUE=DATE'];continue
  assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
 if total==2324:assert set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in new}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==91
assert {q['id'] for q in bp['requirements']}<={q['id'] for q in plan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==bp[k],k
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert d['coverage_summary']['fully_audited_countries']==0 and plan['camp_catalog_integration']['dossiers']==601
for stem in ['europe-camp-audit-v91','europe-camp-source-receipts-v91']:
 v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
 assert not any(v['external_actions'].values())
 if 'sources' in v:
  assert len(v['sources'])==43 and sum(q.get('status')==200 for q in v['sources'])==42 and len(v['dossier_source_urls_added'])==25
  assert sum(q.get('raw_filename','').endswith('.pdf') for q in v['sources'])==8
  for q in v['sources']:
   if q.get('raw_filename'):assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
assert len(list(PRIMARY.glob('*page*.png')))==12
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_europe_camp_audit_v91.json' in js and 'STEM_americas_camp_audit_v90.json' in js
assert 'data-ui-version="91"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(line for line in js.splitlines() if line.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:'EN'};
FUNCTIONS
const found=new Set(filtered().map(p=>p.slug));
for(const p of guide.profiles.filter(p=>p.id>='CP595'&&p.id<='CP601')){if(found.has(p.slug)!==['las-ai-python','technomatic-english-tech','action-american-saint-pardoux'].includes(p.slug))throw Error('falseEN '+p.slug);}
cs.language='ES';if(filtered().some(p=>['ischool-creators','faisl-salamanca-summer'].includes(p.slug)))throw Error('Spanish website not teaching');
cs.language='';cs.child='both';if(filtered().some(p=>['las-ai-python','las','ischool-constructors','ischool-creators','ischool-minecraft','action-american-saint-pardoux'].includes(p.slug)))throw Error('both age mismatch');
""".replace('FUNCTIONS',funcs)
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(verified=True,events=3075,dossiers=601,new_dossiers=7,deepened_dossiers=3,new_calendar_rows=4,new_family_ics=4,corrected_prior_event_ids=len(changed),family_ics=2324,source_urls=918,worldwide_complete=False)))
