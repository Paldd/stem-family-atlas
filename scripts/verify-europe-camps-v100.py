"""Independent source, preservation, export and interactive-filter checks."""
import collections,csv,datetime,hashlib,json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
from camp_europe_v100 import NEW
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v100'
BASE='337d9550f7626b7eba3eb5251abcf7714aa78d43'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def tokens(key,*values):
    t=(PRIMARY/(key+'.txt')).read_text()
    for v in values:assert v in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
op={q['slug']:q for q in b['camp_programmes']['profiles']};p={q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3230 and len(old)==3205 and set(old)<=set(ev)
assert all(ev[k]==v for k,v in old.items())
new=[e for k,e in ev.items() if k not in old]
assert collections.Counter(e['camp_dossier_slug'] for e in new)=={'cosmo-mornings':6,'cosmo-full-days':3,'codecamp-ai':6,'forest-paris-holidays':6,
    'eib-monceau-preschool':1,'eib-monceau-science':1,'beelingue-paris-autumn':1,'beelingue-levallois-autumn':1}
assert collections.Counter(e['iso'][0] for e in new)=={'CHE':15,'FRA':10}
assert all(e['end']>='2026-10-05' and e['end']>=e['start'] and not e['deadline'] for e in new)
assert len(p)==698 and set(p)-set(op)==set(NEW)
assert [q['id'] for q in c['profiles'][:680]]==[q['id'] for q in b['camp_programmes']['profiles']]
assert [p[s]['id'] for s in NEW]==['CP%03d'%i for i in range(681,699)]
assert all(p[s]==v for s,v in op.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
assert c['counts']['countries']==37 and c['counts']['swiss']==99 and c['counts']['source_urls']==1087
assert c['shortlist'][:-3]==b['camp_programmes']['shortlist'] and c['gaps'][:-4]==b['camp_programmes']['gaps']
assert len(c['shortlist'])==161
for q in c['shortlist']:assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
assert sum(e['block']=='Лагеря' for e in ev.values())==1899 and len(c['generated_event_ids'])==1436
assert c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==42

tokens('cosmo','Ages 8+ · 1 hour a week','micro:bit','Maqueen','Wednesday is a full day','price to be confirmed')
tokens('cosmo-camp-form','CHF 280.-','CHF 350','CHF 500','8–12 février','30 mars–2 avril','12–16 juillet','26–30 juillet','9–13 août','11–15 octobre',
       'ne sont pas remboursables','5 jours','assuré personnellement')
assert len(p['cosmo-mornings']['timing']['sessions'])==6 and len(p['cosmo-full-days']['timing']['sessions'])==3
assert all(q['status']=='unknown' for s in ['cosmo-mornings','cosmo-full-days'] for q in p[s]['family_fit'].values())
assert all(not p[s]['confirmed_instruction_languages'] for s in ['cosmo-mornings','cosmo-full-days']+[s for s in NEW if s.startswith('codecamp-')])
tokens('code-faq','language of instruction depends on the specific camp','about CHF 120 per day','CHF 50','less than 72 hours',
       'No. At our regular Code Camps','Minecraft Education is not the same','13 and older','Animation Camp, equipment rental is already included')
tokens('code-camps','Minecraft Masters','Ages 8–13','Spring 2027','Summer 2027','March 2027')
tokens('code-minecraft-masters','7 - 12','Only for kids who have already visited Minecraft Engineers','Blast 3D')
tokens('code-minecraft-experts','at least one Minecraft camp','MakeCode','adventure')
tokens('code-animation','Days:\n2','teams of 2','stop-motion','Day 3')
tokens('code-ai','9 - 13','February 11–12, 2027','February 16–17, 2027','February 18–19, 2027','October 5–6, 2026','October 15–16, 2026','computer vision')
tokens('code-terms','New South Wales, Australia','AUD','2018')
assert len(p['codecamp-ai']['timing']['session_details'])==6
assert {q['place'].split(' · ')[0] for q in p['codecamp-ai']['timing']['session_details']}=={'Winterthur','Zürich','Aarau','Basel','Wettingen','Steinhausen'}
# Six cohorts in six municipalities, while two share a date: do not collapse venues.
assert len({e['id'] for e in new if e['camp_dossier_slug']=='codecamp-ai'})==6
assert p['codecamp-ai']['family_fit']['oscar']['status']=='later'
assert p['codecamp-masters']['family_fit']['oscar']['status']=='unknown'
tokens('issh-techlabs','7 - 10 years','11+ years','CHF 650','Mon 13 Jul 2026','Fri 17 Jul 2026','German- and English-speaking environment','autonomous missions')
assert p['issh-techlabs-robots']['language_evidence_role']=='camp_life' and p['issh-techlabs-robots']['confirmed_instruction_languages']==['EN','DE']
assert not p['issh-techlabs-drones']['confirmed_instruction_languages']
assert not any(s['timing']['sessions'] for s in [p['issh-techlabs-robots'],p['issh-techlabs-drones']])
tokens('forest-fr','2 à 12 ans','leurs journées dehors et en anglais','19 - 23 octobre 2026','8 - 12 février 2027','5 - 9 avril 2027',
       'juillet 2027','5 - 9','12 - 16','19 - 23','450 €/semaine','480 €/semaine','40 €/semaine','40 €/jour')
assert len(p['forest-paris-holidays']['timing']['sessions'])==6 and p['forest-paris-holidays']['language_evidence_role']=='camp_life'
assert (450+40)*2==980 and (480+40)*2==1040
tokens('eib-camps','2 ans et demi à 5 ans','6 à 11','650€','Immersion totale en anglais','codage','non scolarisés')
assert p['eib-monceau-preschool']['family_fit']['matvey']['status']=='not_eligible'
assert p['eib-monceau-science']['family_fit']['oscar']['status']=='conditional'
tokens('beelingue-autumn','3 à 10 ans','5 à 10 ans','49 rue de Prony','80 rue Rivay','14h à 18h','aucune activité')
tokens('beelingue-terms','30 €','48 heures','Sauf opposition expresse')
assert p['beelingue-levallois-autumn']['language_evidence_role']=='language_lessons'
assert 495*2+25*2*2==1090 and round(495*1.9+25*2*2+30,2)==1070.5
assert not any(e['camp_dossier_slug'].startswith(('ps-','futurekids','florimont','faisl','stgeorge','lacunza','ilc','techspark')) for e in new)
visual=json.loads((PRIMARY/'visual-source-notes.json').read_text())
assert len(visual)==4 and sum(q['pages_visual_checked'] for q in visual)==8
for q in visual:
    f=PRIMARY/(q['key']+'.pdf');assert f.read_bytes().startswith(b'%PDF') and hashlib.sha256(f.read_bytes()).hexdigest()==q['pdf_sha256']
    assert len(q['selected_pages'])==q['pages_visual_checked']
    for r in q['renders']:assert hashlib.sha256((PRIMARY/r['filename']).read_bytes()).hexdigest()==r['sha256']

again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
for f,v in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/f).read_text())==v
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA page_size').fetchone()[0]==1024
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert {json.loads(v)['id']:json.loads(v) for v, in con.execute('SELECT record_json FROM events')}==ev
assert {json.loads(v)['slug']:json.loads(v) for v, in con.execute('SELECT record_json FROM camp_programmes')}==p
oldfile=PRIMARY/'baseline.sqlite';oldfile.write_bytes(prior('dist/downloads/STEM_database.sqlite'));oc=sqlite3.connect(oldfile)
schema=lambda db: sorted(db.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"))
assert schema(oc)==schema(con)
for name, in oc.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
    rows=set(oc.execute('SELECT * FROM "'+name+'"'));now=set(con.execute('SELECT * FROM "'+name+'"'))
    if name not in ['metadata','countries']:assert rows<=now,name
    elif name=='metadata':assert {r[0] for r in rows-now}=={'completeness_audit','camp_focus'}
    else:
        delta=rows-now;assert {r[0] for r in delta}=={'CHE','FRA'}
        for r in delta:
            q=con.execute('SELECT * FROM countries WHERE iso=?',(r[0],)).fetchone();assert r[:3]==q[:3]
oc.close();con.close()
assert all(f.stat().st_size<=26214400 for f in (ROOT/'dist').rglob('*') if f.is_file()),'Static hosting per-file limit'
csvpath='dist/downloads/STEM_catalog.csv'
rows=lambda raw:{r['id']:r for r in csv.DictReader(raw.decode('utf-8-sig').splitlines())}
oldcsv=rows(prior(csvpath));newcsv=rows((ROOT/csvpath).read_bytes());assert len(newcsv)==3230 and all(newcsv[k]==v for k,v in oldcsv.items())
md=(ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.md').read_text()
for s in NEW:assert p[s]['provider'] in md and p[s]['editorial_reason'] in md
def calendar(value):
    out={};t=value.decode().replace('\r\n ','').replace('\r\n\t','')
    for block in t.split('BEGIN:VEVENT')[1:]:
        f={s.split(':',1)[0]:s.split(':',1)[1] for s in block.split('END:VEVENT')[0].splitlines() if ':' in s};assert f['UID'] not in out;out[f['UID']]=f
    return out
path='dist/downloads/STEM_подтвержденные_даты.ics';oldcal=calendar(prior(path));now=calendar((ROOT/path).read_bytes())
assert len(now)==2491 and len(oldcal)==2466 and set(oldcal)<=set(now)
for uid,v in oldcal.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
assert set(now)-set(oldcal)=={'stem-'+e['id']+'@family-stem.local' for e in new}
for e in new:
    f=now['stem-'+e['id']+'@family-stem.local'];assert f['DTSTART;VALUE=DATE']==e['start'].replace('-','')
    assert f['DTEND;VALUE=DATE']==(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d') and f['STATUS']=='TENTATIVE'
expo='dist/downloads/STEM_крупные_выставки.ics';oe=calendar(prior(expo));ne=calendar((ROOT/expo).read_bytes());assert len(ne)==104 and set(oe)==set(ne)
for uid,v in oe.items():assert {k:x for k,x in ne[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==100
assert {q['id'] for q in bp['requirements']}=={q['id'] for q in plan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==bp[k],k
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['europe-camp-audit-v100','europe-camp-source-receipts-v100']:
    v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
    assert not any(v['external_actions'].values())
    if 'sources' in v:
        assert len(v['sources'])==39 and len(v['dossier_source_urls_added'])==21
        assert sum(q.get('status')==200 for q in v['sources'])==39
        assert sum(q['content_status']=='javascript_shell_no_programme_body' for q in v['sources'])==2
        for q in v['sources']:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_europe_camp_audit_v100.json' in js
assert 'data-ui-version="100"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(s for s in js.splitlines() if s.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:''};
FUNCTIONS
const fresh=new Set(NEW);const current=()=>new Set(filtered().filter(p=>fresh.has(p.slug)).map(p=>p.slug));
cs.child='both';if(current().size!==9)throw Error('both');
cs.child='oscar';if(current().size!==10)throw Error('oscar');cs.child='matvey';if(current().size!==13)throw Error('matvey');
cs.child='';cs.phase='2027';if(current().size!==4)throw Error('phase');cs.phase='';
cs.language='EN';if(current().size!==6||[...current()].some(s=>s.startsWith('codecamp')||s.startsWith('cosmo')))throw Error('falseEnglish');
cs.child='both';cs.phase='2027';if(current().size!==1||!current().has('forest-paris-holidays'))throw Error('family2027English');
cs.child='';cs.phase='';cs.language='ES';if(current().size)throw Error('falseES');cs.language='EN-support';if(current().size)throw Error('falseSupport');
cs.language='';cs.format='boarding';if(current().size)throw Error('falseBoarding');
cs.format='';cs.country='CHE';if(current().size!==13)throw Error('Switzerland');cs.country='FRA';if(current().size!==5)throw Error('France');
""".replace('FUNCTIONS',funcs).replace('NEW',json.dumps(NEW))
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(verified=True,events=3230,dossiers=698,new_dossiers=18,new_calendar_rows=25,prior_events_unchanged=3205,prior_dossiers_unchanged=680,family_ics=2491,source_urls=1087,worldwide_complete=False)))
