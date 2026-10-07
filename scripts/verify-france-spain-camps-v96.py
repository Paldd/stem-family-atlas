"""Independent preservation, primary-evidence and cross-export checks."""
import collections, datetime, hashlib, json, re, sqlite3, subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
from camp_france_spain_v96 import NEW, UPDATED
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v96'
BASE='0efdae1af263aba021ffdcfbbf3240049eb952ef'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def before(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def raw(key):return (PRIMARY/(key+'.txt')).read_text()
def tokens(key,*values):
    text=raw(key)
    for v in values:assert v in text,(key,v)
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
op={q['slug']:q for q in b['camp_programmes']['profiles']};p={q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3153 and len(old)==3140 and set(old)<=set(ev)
assert all(ev[k]==v for k,v in old.items())
new=[e for k,e in ev.items() if k not in old]
assert len(new)==13 and collections.Counter(e['camp_dossier_slug'] for e in new)=={'sswp-jardins':5,'sswp-pcc-primary':4,'sswp-racing-primary':2,'olocau-english-summer':1,'olocau-fluent':1}
assert all(e['start']>='2026-10-05' and not e['deadline'] for e in new)
assert len(p)==645 and set(p)-set(op)==set(NEW)
assert [q['id'] for q in c['profiles'][:631]]==[q['id'] for q in b['camp_programmes']['profiles']]
assert [p[s]['id'] for s in NEW]==['CP%03d'%i for i in range(632,646)]
for slug,q in op.items():
    if slug not in UPDATED:assert p[slug]==q,slug
    else:
        for key in ['id','slug','iso','country','related_event_ids','calendar_links','confirmed_instruction_languages']:assert p[slug].get(key)==q.get(key),(slug,key)
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
assert c['counts']['countries']==37 and c['counts']['swiss']==86 and c['counts']['source_urls']==1021
assert c['shortlist'][:-4]==b['camp_programmes']['shortlist'] and c['gaps'][:-4]==b['camp_programmes']['gaps']
assert len(c['shortlist'])==150
for q in c['shortlist']:assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
assert sum(e['block']=='Лагеря' for e in ev.values())==1822 and len(c['generated_event_ids'])==1359
assert c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==39

# Source bodies independently establish year, track and price; archived/uncertain dates cannot become future cohorts.
autumn={('2026-10-19','2026-10-23'),('2026-10-26','2026-10-30')}
winter={('2027-02-08','2027-02-12'),('2027-02-15','2027-02-19')}
for slug,key,dates in [('sswp-jardins','sswp-jardins',autumn|winter|{('2026-12-21','2026-12-23')}),('sswp-pcc-primary','sswp-pcc',autumn|winter),('sswp-racing-primary','sswp-racing',autumn)]:
    assert set(map(tuple,p[slug]['timing']['sessions']))==dates
    tokens(key,'19-23','26-30','2026')
for key in ['sswp-jardins','sswp-pcc']:tokens(key,'8-12 février 2027','15-19 février 2027')
tokens('sswp-jardins-pdf','550€/5 jours','330€/3 jours','2027','2026','pique-nique')
tokens('sswp-jardins-pdf-observed','25EURdaylate','45EURannualparkpass insidefee','minimum10/day')
tokens('sswp-pcc-pdf','130€/SEMAINE','90€/SEMAINE')
tokens('sswp-racing','110€ par jour')
tokens('sswp-racing-pdf','120€/jour','80€/semaine','90€/semaine','Golf')
assert p['sswp-racing-primary']['language_evidence_role']=='language_lessons'
assert 'не установлен' in p['sswp-racing-primary']['language']
tokens('sswp-marymount-pdf','575 € par semaine','120 € par semaine','2026')
assert not p['sswp-marymount-primary']['calendar_links']

tokens('olocau-english','31 jul','6 agosto 2027','De 6 a 14','250 plazas','7 de enero','2 de noviembre de 2026')
for slug in ['olocau-english-summer','olocau-fluent']:
    assert p[slug]['timing']['sessions']==[['2027-07-31','2027-08-06']] and p[slug]['price']['year']==2027
    assert 'не опубликована' in p[slug]['price']['label']
tokens('olocau-facilities','no incluyen ropa de cama','ni toallas')
tokens('pueblo-kids','€890.00','300€','2027')
tokens('pueblo-kids-faq','7 y 12','8 participantes','ida/vuelta')
assert not p['pueblo-kids']['calendar_links'] and p['pueblo-kids']['price']['year'] is None
tokens('pueblo-ai','13 de octubre','245 €','420 €','210 €','100% en inglés')
assert p['pueblo-eduplai-online']['formats']==['online'] and p['pueblo-eduplai-online']['programme_category']=='school_year_online_supplement'
assert not p['pueblo-eduplai-online']['timing']['sessions'] and not p['pueblo-eduplai-online']['calendar_links']
assert p['pueblo-eduplai-online']['family_fit']['oscar']['status']=='later'

tokens('vaughan-catalogue','2026','1.590 €','880 €','1.685 €','930 €','1.760 €','6 a 15','5 horas')
for s,n in [('vaughan-bravo',10),('vaughan-mazo',2),('vaughan-kiriko',2)]:
    assert len(p[s]['timing']['sessions'])==n and not p[s]['calendar_links'] and p[s]['price']['year']==2026
tokens('ymca-priego','2010 y 2015','1.340€')
tokens('ymca-salduero','2013 y 2019','810€','560€')
tokens('ymca-terms','100 €','incluida en el precio','Campamentos Nacionales de YMCA 2026','500€')
assert all(v['status']=='later' for v in p['ymca-priego']['family_fit'].values())
assert p['ymca-salduero']['family_fit']['matvey']['status']=='candidate' and p['ymca-salduero']['family_fit']['oscar']['status']=='later'
past=[v for s in NEW for v in p[s]['timing']['sessions'] if v[1]<'2026-10-05'];assert len(past)==24
tokens('chester-mini','2019 al 2023','FECHAS 2027','1 de diciembre de 2026')
tokens('chester-mini-fees-observed','2018–2022','1230EUR','770EUR','reserve250insidefee','5%youngercorefee')
tokens('chester-board-fees-es-observed','500insidefee','50EURoneway','balanceJun1')
tokens('chester-board-fees-en-observed','750insidefee','60oneway')
tokens('chester-day-fees-en-observed','balanceMay1','1150half/1950full')
tokens('chester-day-fees-observed','title2025','1855EURfull/1095half')
assert p['chester-mini']['family_fit']['matvey']['status']=='not_eligible' and p['chester-mini']['family_fit']['oscar']['status']=='candidate'
assert not p['chester-mini']['calendar_links']
assert all(v in p['chester-english']['price']['deposit'] for v in ['€750','€500','€60','€50','1 мая','1 июня'])

again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
for f,v in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/f).read_text())==v
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert {json.loads(v)['id']:json.loads(v) for v, in con.execute('SELECT record_json FROM events')}==ev
assert {json.loads(v)['slug']:json.loads(v) for v, in con.execute('SELECT record_json FROM camp_programmes')}==p;con.close()
def calendar(value):
    out={};text=value.decode().replace('\r\n ','').replace('\r\n\t','')
    for block in text.split('BEGIN:VEVENT')[1:]:
        f={s.split(':',1)[0]:s.split(':',1)[1] for s in block.split('END:VEVENT')[0].splitlines() if ':' in s};assert f['UID'] not in out;out[f['UID']]=f
    return out
for file,total in [('STEM_подтвержденные_даты.ics',2414),('STEM_крупные_выставки.ics',104)]:
    prior=calendar(before('dist/downloads/'+file));now=calendar((ROOT/'dist/downloads'/file).read_bytes())
    assert set(prior)<=set(now) and len(now)==total
    for uid,v in prior.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
    if total==2414:
        assert set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in new}
        for e in new:
            f=now['stem-'+e['id']+'@family-stem.local'];assert f['DTSTART;VALUE=DATE']==e['start'].replace('-','')
            assert f['DTEND;VALUE=DATE']==(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d')
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==96
assert {q['id'] for q in bp['requirements']}=={q['id'] for q in plan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==bp[k],k
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['france-spain-camp-audit-v96','france-spain-camp-source-receipts-v96']:
    v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
    assert not any(v['external_actions'].values())
    if 'sources' in v:
        assert len(v['sources'])==45 and len(v['dossier_source_urls_added'])==29
        assert sum(q['retrieval_method']=='direct_http' for q in v['sources'])==37
        assert sum(q.get('content_status')=='redirect_general_course_not_camp' for q in v['sources'])==2
        assert sum(bool(q.get('pdf_metadata')) for q in v['sources'])==12
        assert sum(q['retrieval_method']=='pdf_visual_selected_clauses' for q in v['sources'])==8
        for q in v['sources']:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
        assert next(q for q in v['sources'] if q['key']=='sswp-marymount-pdf')['pdf_metadata']['Pages']=='7'
js=(ROOT/'dist/assets/camp-programmes.js').read_text()
assert 'STEM_france_spain_camp_audit_v96.json' in js and "online:'Онлайн · учебная программа'" in js
assert 'data-ui-version="96"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(s for s in js.splitlines() if s.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'online',child:'',phase:'',language:''};
FUNCTIONS
let found=new Set(filtered().map(p=>p.slug));if(found.size!==1||!found.has('pueblo-eduplai-online'))throw Error('online filter');
cs.format='boarding';found=new Set(filtered().map(p=>p.slug));if(found.has('pueblo-eduplai-online')||!found.has('olocau-fluent'))throw Error('boarding');
cs.format='';cs.phase='2027';found=new Set(filtered().map(p=>p.slug));for(const s of ['sswp-jardins','sswp-pcc-primary','olocau-fluent'])if(!found.has(s))throw Error('2027 missing '+s);
for(const s of ['pueblo-eduplai-online','vaughan-bravo','ymca-priego','sswp-marymount-primary'])if(found.has(s))throw Error('false2027 '+s);
cs.phase='archive_next_unannounced';found=new Set(filtered().map(p=>p.slug));if(found.size!==10)throw Error('archive');
cs.phase='';cs.child='both';found=new Set(filtered().map(p=>p.slug));for(const s of ['chester-mini','ymca-priego','ymca-salduero','pueblo-eduplai-online'])if(found.has(s))throw Error('falseBoth '+s);
for(const s of ['sswp-jardins','sswp-pcc-primary','olocau-fluent'])if(!found.has(s))throw Error('both missing '+s);
cs.child='';cs.language='EN';found=new Set(filtered().map(p=>p.slug));for(const s of ['sswp-jardins','chester-mini','pueblo-eduplai-online'])if(!found.has(s))throw Error('missingEN '+s);
""".replace('FUNCTIONS',funcs)
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(verified=True,events=3153,dossiers=645,new_dossiers=14,deepened_dossiers=1,new_calendar_rows=13,prior_events_unchanged=3140,prior_dossiers_unchanged=630,family_ics=2414,source_urls=1021,worldwide_complete=False)))
