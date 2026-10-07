"""Check primary contradictions, old records and unchanged calendar subscriptions."""
import ast, hashlib, io, json, re, sqlite3, subprocess, zipfile
from camp_europe_canada_v130 import ROOT, BASE, NEW, NEW_OFFERS
P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v130'
def prior(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={p['slug']:p for p in b['camp_programmes']['profiles']};new={p['slug']:p for p in d['camp_programmes']['profiles']}
assert len(old)==1034 and len(new)==1049 and set(new)-set(old)==set(NEW)
assert all(old[s]==new[s] for s in old)
oe={e['id']:e for e in b['events']};ne={e['id']:e for e in d['events']}
assert len(oe)==3775 and len(ne)==3777 and all(oe[s]==ne[s] for s in oe)
assert set(ne)-set(oe)=={'CP1035-20261019-20261024','CP1038-20270823-20270827'}
assert d['camp_planning']['offers'][:-2]==b['camp_planning']['offers'] and len(d['camp_planning']['offers'])==55
assert [o['id'] for o in d['camp_planning']['offers'][-2:]]==NEW_OFFERS
assert d['league_guide']==b['league_guide'] and d['school_focus']==b['school_focus'] and d['school_history']==b['school_history']
for s in ['enjoy-winter-junior','enjoy-spring-junior']:
    assert new[s]['timing']['status']=='partial_2027' and new[s]['timing']['sessions']==[] and new[s]['calendar_links']==[]
for s in NEW[6:]:assert new[s]['timing']['sessions']==[] and new[s]['timing']['status']=='archive_next_unannounced'
assert new['littlebritish-best']['family_fit']['matvey']['status']=='not_eligible'
assert new['agora-lledo-super']['family_fit']['oscar']['status']=='not_eligible'
assert new['agora-lledo-tech-young']['family_fit']['matvey']['status']=='not_eligible'
assert new['agora-lledo-tech']['confirmed_instruction_languages']==['EN']
assert all(not new[s]['confirmed_instruction_languages'] for s in NEW[10:])
r=d['camp_programmes']['family_review'];assert r['coverage']==dict(candidates=50,countries=16,fully_audited_countries=0)
assert len({q['slug'] for q in r['entries']})==50 and r['entries'][:41]==b['camp_programmes']['family_review']['entries']
def clause(file,*words):
    def normal(s):return ''.join(s.lower().replace('’',"'").replace('–','-').replace('\xad','').split())
    text=normal((P/(file+'.txt')).read_text())
    for word in words:assert normal(word) in text,(file,word)
clause('enjoy-october','19-24octobre2026','lundi10h30','samedi16h30','820€TTC','6-10ans')
clause('enjoy-faq','Leprojet6-10ansestbilingue','Il n’inclut pas le transport')
clause('enjoy-march','FÉVRIER2027','820€')
clause('enjoy-upcoming','1-6mars','2027')
clause('enjoy-april','19-24AVRIL2027','dudimanchematinauvendredi','750€')
clause('enjoy-tariff','820€TTC')
clause('littlebritish-best','23AU27août2027','3-6ans','300€','entièrementenanglais')
clause('littlebritish-grammar-current','24AU28août2026','Collège','250€','Complet')
clause('agora-lledo-brochure','2026','100%English+Technology','From2022al2020','From2019to2014','notapplicabletotheTechnologyCampus','385€','452€','non-refundable')
clause('ridley-intermediate','ages7to10','DotandDash','LegoSpikePrime','$450')
clause('ridley-senior','Robotics:LegoSpikePrime','2026')
clause('ridley-boarding','Ages10to16','CanadianandInternationalstudents','$3995','taxincluded','May1st,2026')
clause('masthau-price','5285€perweekforafamilyof4','2026','Hal fboard'.replace(' ',''))
clause('suisse-faq','English-speakingenvironment','CHF500','non-refundable')
receipts=json.loads((ROOT/'data/europe-canada-camps-source-receipts-v130.json').read_text())
assert len(receipts['sources'])==37 and not any(receipts['external_actions'].values())
for q in receipts['sources']:
    if q['body_snapshot_retained']:
        raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert sum(q['body_snapshot_retained'] for q in receipts['sources'])==32
def blocks(raw):return {re.search(br'(?m)^UID:([^\r\n]+)',v).group(1):v for v in re.findall(br'BEGIN:VEVENT\r?\n.*?END:VEVENT\r?\n',raw,re.S)}
before=blocks(prior('dist/downloads/STEM_подтвержденные_даты.ics'));after=blocks((ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes())
assert len(before)==2991 and len(after)==2993 and all(before[k]==after[k] for k in before)
assert (ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes()==prior('dist/downloads/STEM_крупные_выставки.ics')
# Changed event content must still replace the old event; only unchanged UIDs are retained.
tree=ast.parse((ROOT/'scripts/build-database.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='write_ical')
ns={'re':re};exec(compile(ast.Module(body=[fn],type_ignores=[]),'calendar-helper','exec'),ns)
test=P/'calendar-change-check.ics'
old_cal=b'BEGIN:VCALENDAR\r\nBEGIN:VEVENT\r\nUID:old\r\nDTSTAMP:20261001T000000Z\r\nDTSTART:20261010\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n';test.write_bytes(old_cal)
changed=old_cal.replace(b'20261001T000000Z',b'20261006T000000Z').replace(b'DTSTART:20261010',b'DTSTART:20261011')
ns['write_ical'](test,changed);assert test.read_bytes()==changed
ns['write_ical'](test,changed.replace(b'20261006T000000Z',b'20261007T000000Z'));assert test.read_bytes()==changed
def portable(meta,kind):
    m=json.loads((ROOT/'dist/downloads'/meta).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
    assert m['complete_database'] and len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256']
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        assert z.testzip() is None and z.namelist()==[m[kind+'_entry'],'README.txt'];body=z.read(m[kind+'_entry'])
    assert len(body)==m[kind+'_bytes'] and hashlib.sha256(body).hexdigest()==m[kind+'_sha256']
    assert m['raw_download_available']==(len(body)<=26214400)
    return body
assert json.loads(portable('STEM_database_json_download.json','json'))==d
sql=portable('STEM_database_download.json','sqlite');(P/'verified-v130.sqlite').write_bytes(sql)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as z:(P/'baseline-v129.sqlite').write_bytes(z.read('STEM_database.sqlite'))
c=sqlite3.connect(P/'verified-v130.sqlite');oc=sqlite3.connect(P/'baseline-v129.sqlite')
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
tables=[x[0] for x in oc.execute("SELECT name FROM sqlite_master WHERE type='table'")]
assert tables==[x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
for t in tables:
    a=oc.execute('SELECT * FROM '+t).fetchall();z=c.execute('SELECT * FROM '+t).fetchall()
    if t=='metadata':
        am=dict(a);zm=dict(z);changed={k for k in am if am[k]!=zm[k]};assert changed=={'camp_family_review','camp_planning','camp_focus','completeness_audit'}
        assert json.loads(zm['camp_family_review'])==r and json.loads(zm['camp_planning'])==d['camp_planning']
    elif t in ['sources','events','event_countries','event_themes','camp_programmes','camp_programme_sources','camp_programme_events']:
        assert set(a)<=set(z),t
    elif t=='countries':
        assert [v for v in a if v[0]!='FRA']==[v for v in z if v[0]!='FRA']
        x=next(v for v in a if v[0]=='FRA');y=next(v for v in z if v[0]=='FRA');assert x[:3]==y[:3]
        record=json.loads(x[3]);record['camps']+=2;record['dated']+=2;assert record==json.loads(y[3])
    else:assert a==z,t
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']==plan['native_goal_status']=='active'
assert plan['human_scope_expansion']==json.loads(prior('data/research-plan.json'))['human_scope_expansion']
assert plan['next_research']==json.loads(prior('data/research-plan.json'))['next_research']
assert plan['current_publication']['status']=='prepared_local_not_published'
result=dict(status='passed',version=130,new_dossiers=15,new_calendar_rows=2,new_budget_scenarios=2,unchanged_dossiers=1034,unchanged_event_objects=3775,unchanged_budget_objects=53,
    family_review_candidates=50,priority_selection_countries=16,old_ics_blocks_byte_identical=2991,exhibition_ics_byte_identical=True,changed_event_still_updates=True,
    all_old_sqlite_entity_rows_preserved=True,derived_country_counts_updated=['FRA:+2camps/+2dated'],complete_sqlite_bytes=len(sql),complete_json_matches_catalog=True,raw_source_receipt_hashes_verified=32,
    source_contract_years_age_language_and_session_conflicts_checked=True,goal='active',worldwide_complete=False,publication='prepared_local_not_published')
(P/'independent-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result))
