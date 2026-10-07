"""Verify primary clauses, preservation, relational exports and family filters."""
import collections,csv,datetime,hashlib,json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
from camp_europe_v101 import NEW
ROOT=Path(__file__).resolve().parents[1];PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v101'
BASE='5237c21f57c3666461a906e9f3686cb0937b4c86'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def tokens(key,*values):
    t=' '.join((PRIMARY/(key+'.txt')).read_text().split())
    for v in values:assert ' '.join(v.split()) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
op={q['slug']:q for q in b['camp_programmes']['profiles']};p={q['slug']:q for q in c['profiles']}
assert len(ev)==len(d['events'])==3255 and len(old)==3230 and set(old)<=set(ev)
assert all(ev[k]==v for k,v in old.items())
new=[e for k,e in ev.items() if k not in old]
assert collections.Counter(e['camp_dossier_slug'] for e in new)=={'englishsport-cavalese':2,'englishsport-oclini':2,'xuk-activity':5,'bede-little':6,'bede-future':4,'canopee-holidays':6}
assert collections.Counter(e['iso'][0] for e in new)=={'ITA':4,'GBR':15,'FRA':6}
assert all(e['end']>='2026-10-05' and e['end']>=e['start'] and not e['deadline'] for e in new)
assert len(p)==707 and set(p)-set(op)==set(NEW)
assert all(p[s]==v for s,v in op.items())
assert [q['id'] for q in c['profiles'][:698]]==[q['id'] for q in b['camp_programmes']['profiles']]
assert [p[s]['id'] for s in NEW]==['CP%03d'%i for i in range(699,708)]
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
assert c['counts']['countries']==37 and c['counts']['swiss']==99 and c['counts']['source_urls']==1111
assert c['shortlist'][:-3]==b['camp_programmes']['shortlist'] and c['gaps'][:-5]==b['camp_programmes']['gaps']
assert len(c['shortlist'])==164
for q in c['shortlist']:assert len(q['slugs'])==len(set(q['slugs'])) and all(s in p for s in q['slugs'])
assert sum(e['block']=='Лагеря' for e in ev.values())==1924 and len(c['generated_event_ids'])==1461
assert c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==42
tokens('sancelso-summer','ages 6 to 17','of any nationality','English-speaking')
tokens('sancelso-faq','explanations are provided in Italian','translate to foreign participants','ratio of about 1:10','Vaccination Certificate','sleeping bag','€ 50 per week')
tokens('sancelso-dates','2026','795 €','1550 €','€ 755','€ 1,490','€ 60','€ 120','90 round trip','initial deposit of € 300')
assert 795+60==855 and 1550+120==1670 and 795+755+120==1670 and 1550+1490+240==3280
assert p['sancelso-general']['price']['year']==2026 and not p['sancelso-general']['timing']['sessions']
assert p['sancelso-general']['language_evidence_role']=='camp_life'
tokens('socks-camp','children ages 7–10','Tweens ages 10-14','residential camp','mother-tongue English teaching')
tokens('socks-dates','English Summer Camp 2027','January 15th 2027')
assert not p['socks-general']['timing']['sessions'] and p['socks-general']['family_fit']['oscar']['status']=='conditional'
tokens('italy-sport-info','04 -','09 luglio 2027','22 -','27 agosto 2027','18 -','24 luglio 2027','25 -','31 luglio 2027','€ 680,00','€ 780,00','€ 340,00','dagli 10 ai 14','dai 12 ai 16','€50 a notte')
tokens('sport-multi-pdf','ENGLAND','SCOTLAND','ALBERGO PANORAMA','CORSO INGLESE','GIOCHI IN INGLESE')
tokens('sport-intensive-pdf','tutte le attività giornaliere','lingua inglese')
assert p['englishsport-cavalese']['language_evidence_role']=='language_lessons'
assert p['englishsport-oclini']['language_evidence_role']=='camp_life'
assert not any(e['start']=='2027-06-27' for e in new if e['camp_dossier_slug']=='englishsport-cavalese')
tokens('aosr-camp','details will be made available in March 2027','Registrations for Summer Camp 2027 are closed','temporary visitors to Rome','rocket building','€250','€450','€650','€175')
assert not p['aosr-general']['timing']['sessions'] and p['aosr-general']['formats']==['day']
tokens('xuk-faq','between 8 and 17','English is used by staff during activities','£6 per bag','Insurance is not included','three meals a day')
tokens('xuk-dates','Dates 2027','Sunday 04 July to Sunday 11 July','Sunday 01 August to Sunday 08 August','Prices 2026','£1,160','Packages 2026','Discounts 2027')
tokens('xuk-terms','Before 1 May 2026','On or after 1 July 2026','Deposit will be forfeited')
assert p['xuk-activity']['price']['year']==2026 and len(p['xuk-activity']['timing']['sessions'])==5 and p['xuk-activity']['family_fit']['oscar']['status']=='later'
tokens('bede-summary-2027','Course Summary 2027','BURGESS','HILL','£1,775','£1,125','Day students 5-11. Residential students 6-11.','We are delighted to welcome Burgess Hill School','Mission Possible')
tokens('bede-terms-2027','£800 for Residential courses','£400','56 days','29 to 55 days','Deposit retained','£235','£160','£95','£295')
tokens('bede-faq','29 to 41 days','20% of any spoken native language')
tokens('bede-dates','Burgess Hill (8-13yrs)','11 July - 07 August 2027')
assert len(p['bede-little']['timing']['sessions'])==6 and len(p['bede-future']['timing']['sessions'])==4
assert p['bede-future']['place'].startswith('Burgess Hill')
assert not any(e['start']=='2027-08-08' for e in new if e['camp_dossier_slug']=='bede-future')
assert 1775*2==3550 and 1125*2==2250 and 1775*4==7100
tokens('canopee','week entirely in English','9 am to 5 pm, with lunch included','whether or not they attend','6–11','Ages 6–10','19–23 October 2026','8–12 February 2027','5–9 April 2027','1–2 July 2027','5–9 July 2027','12–13 July 2027','€515','€206')
assert len(p['canopee-holidays']['timing']['sessions'])==6 and 515*2==1030 and 206*2==412
assert all(e['date_scope']=='day_camp_window' for e in new if e['camp_dossier_slug']=='canopee-holidays')
tokens('lacunza-2027','2027','20','08','- €/semana')
tokens('chester-2027','ages 8 to 17','Campers aged 8-18','2027 dates will be published very shortly')
assert p['lacunza-general']==op['lacunza-general'] and p['chester-english']==op['chester-english']
visual=json.loads((PRIMARY/'visual-source-notes.json').read_text());assert len(visual)==6 and sum(q['pages_visual_checked'] for q in visual)==8
for q in visual:
    f=PRIMARY/(q['key']+'.pdf');assert f.read_bytes().startswith(b'%PDF') and hashlib.sha256(f.read_bytes()).hexdigest()==q['pdf_sha256']
    assert len(q['selected_pages'])==q['pages_visual_checked']
    for r in q['renders']:assert hashlib.sha256((PRIMARY/r['filename']).read_bytes()).hexdigest()==r['sha256']
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
for f,v in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/f).read_text())==v
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite');assert con.execute('PRAGMA page_size').fetchone()[0]==1024
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert {json.loads(v)['id']:json.loads(v) for v, in con.execute('SELECT record_json FROM events')}==ev
assert {json.loads(v)['slug']:json.loads(v) for v, in con.execute('SELECT record_json FROM camp_programmes')}==p
oldfile=PRIMARY/'baseline.sqlite';oldfile.write_bytes(prior('dist/downloads/STEM_database.sqlite'));oc=sqlite3.connect(oldfile)
schema=lambda db:sorted(db.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"))
assert schema(oc)==schema(con)
for name, in oc.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
    rows=set(oc.execute('SELECT * FROM "'+name+'"'));now=set(con.execute('SELECT * FROM "'+name+'"'))
    if name not in ['metadata','countries']:assert rows<=now,name
    elif name=='metadata':assert {r[0] for r in rows-now}=={'completeness_audit','camp_focus'}
    else:
        delta=rows-now;assert {r[0] for r in delta}=={'ITA','GBR','FRA'}
        for r in delta:
            q=con.execute('SELECT * FROM countries WHERE iso=?',(r[0],)).fetchone();assert r[:3]==q[:3]
oc.close();con.close()
assert all(f.stat().st_size<=26214400 for f in (ROOT/'dist').rglob('*') if f.is_file()),'Static per-file limit'
rows=lambda raw:{r['id']:r for r in csv.DictReader(raw.decode('utf-8-sig').splitlines())}
path='dist/downloads/STEM_catalog.csv';oldcsv=rows(prior(path));newcsv=rows((ROOT/path).read_bytes());assert len(newcsv)==3255 and all(newcsv[k]==v for k,v in oldcsv.items())
md=(ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.md').read_text()
for s in NEW:assert p[s]['provider'] in md and p[s]['editorial_reason'] in md
def calendar(value):
    out={};t=value.decode().replace('\r\n ','').replace('\r\n\t','')
    for block in t.split('BEGIN:VEVENT')[1:]:
        f={s.split(':',1)[0]:s.split(':',1)[1] for s in block.split('END:VEVENT')[0].splitlines() if ':' in s};assert f['UID'] not in out;out[f['UID']]=f
    return out
path='dist/downloads/STEM_подтвержденные_даты.ics';oldcal=calendar(prior(path));now=calendar((ROOT/path).read_bytes())
assert len(now)==2514 and len(oldcal)==2491 and set(oldcal)<=set(now)
for uid,v in oldcal.items():assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
family=[e for e in new if e['camp_dossier_slug']!='englishsport-oclini']
assert set(now)-set(oldcal)=={'stem-'+e['id']+'@family-stem.local' for e in family}
for e in family:
    f=now['stem-'+e['id']+'@family-stem.local'];assert f['DTSTART;VALUE=DATE']==e['start'].replace('-','')
    assert f['DTEND;VALUE=DATE']==(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d') and f['STATUS']=='TENTATIVE'
expo='dist/downloads/STEM_крупные_выставки.ics';oe=calendar(prior(expo));ne=calendar((ROOT/expo).read_bytes());assert len(ne)==104 and set(oe)==set(ne)
for uid,v in oe.items():assert {k:x for k,x in ne[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==101
assert {q['id'] for q in bp['requirements']}=={q['id'] for q in plan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==bp[k],k
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan and d['coverage_summary']['fully_audited_countries']==0
for stem in ['europe-camp-audit-v101','europe-camp-source-receipts-v101']:
    v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
    assert not any(v['external_actions'].values())
    if 'sources' in v:
        assert len(v['sources'])==34 and len(v['dossier_source_urls_added'])==24
        assert sum(q.get('status')==200 for q in v['sources'])==33
        for q in v['sources']:
            if q.get('status')==200:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_europe_camp_audit_v101.json' in js
assert 'data-ui-version="101"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
funcs='\n'.join(s for s in js.splitlines() if s.lstrip().startswith(('function matchesLanguage(', 'function filtered(')))
test="""const fs=require('fs');const guide=JSON.parse(fs.readFileSync(0,'utf8'));const cs={query:'',country:'',theme:'',format:'',child:'',phase:'',language:''};
FUNCTIONS
const fresh=new Set(NEW);const current=()=>new Set(filtered().filter(p=>fresh.has(p.slug)).map(p=>p.slug));
const expect=(n,label)=>{if(current().size!==n)throw Error(label+':'+[...current()]);};
cs.child='both';expect(5,'both');cs.child='oscar';expect(5,'oscar');cs.child='matvey';expect(8,'matvey');cs.child='';
cs.phase='2027';expect(8,'phase');cs.phase='';cs.language='EN';expect(9,'EN');cs.child='both';cs.phase='2027';expect(4,'family2027');
cs.child='';cs.phase='';cs.language='ES';expect(0,'noES');cs.language='EN-support';expect(0,'noSupport');cs.language='';
cs.format='boarding';expect(7,'boarding');cs.format='day';expect(5,'day');cs.format='';
cs.country='CHE';expect(0,'noSwissduplicate');cs.country='ITA';expect(5,'Italy');cs.country='GBR';expect(3,'UK');cs.country='FRA';expect(1,'France');
""".replace('FUNCTIONS',funcs).replace('NEW',json.dumps(NEW))
subprocess.run([NODE,'-e',test],input=json.dumps(c).encode(),check=True)
print(json.dumps(dict(verified=True,events=3255,dossiers=707,new_dossiers=9,new_calendar_rows=25,prior_events_unchanged=3230,prior_dossiers_unchanged=698,family_ics=2514,new_family_ics=23,source_urls=1111,worldwide_complete=False)))
