"""Independent source, classification, record, portable DB and calendar checks."""
import hashlib, io, json, re, sqlite3, subprocess, zipfile
from collections import Counter
from camp_northamerica_v131 import ROOT, BASE, NEW, EVENT_IDS, PROFILE_ID, RES
P=ROOT.parent/'stem-family-atlas-work/camp-northamerica-primary-v131'
def prior(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={p['slug']:p for p in b['camp_programmes']['profiles']};new={p['slug']:p for p in d['camp_programmes']['profiles']}
assert len(old)==1049 and len(new)==1079 and set(new)-set(old)==set(NEW)
assert all(old[s]==new[s] for s in old)
oe={e['id']:e for e in b['events']};ne={e['id']:e for e in d['events']}
assert len(oe)==3777 and len(ne)==3788 and all(oe[s]==ne[s] for s in oe)
campids={'CP1057-20270705-20270709','CP1057-20270712-20270716','CP1057-20270719-20270723','CP1057-20270726-20270730'}
assert set(ne)-set(oe)==campids|set(EVENT_IDS)
assert all(ne[i]['block']=='Лагеря' and ne[i]['priority'].startswith('P4') for i in campids)
assert all(ne[i]['block']=='События' and not ne[i].get('exhibition_tier') for i in EVENT_IDS)
assert {e['id']:e for e in d['events'] if e['block']=='Соревнования'}=={e['id']:e for e in b['events'] if e['block']=='Соревнования'}
assert Counter(e['block'] for e in d['events'])==dict(Соревнования=1153,События=196,Лагеря=2439)
assert d['camp_planning']==b['camp_planning'] and len(d['camp_planning']['offers'])==55
assert d['school_focus']==b['school_focus'] and d['school_history']==b['school_history'] and d['schools']==b['schools']
assert d['development_routes']==b['development_routes'] and d['family_strategy']==b['family_strategy']
assert d['league_guide']['profiles'][:-1]==b['league_guide']['profiles'] and len(d['league_guide']['profiles'])==142
assert d['league_guide']['profiles'][-1]['id']==PROFILE_ID and not d['league_guide']['profiles'][-1]['legacy_ids']
assert d['leagues']==b['leagues'] and len(d['leagues'])==46
assert d['league_guide']['legacy_count']==d['league_guide']['mapped_legacy_count']==46
for s in NEW:
    p=new[s];assert p['checked']=='2026-10-06' and p['id'] not in {q['id'] for q in old.values()}
    assert all(q['checked']=='2026-10-06' for q in p['sources'])
    if s!='toronto-deep-day-2027':assert p['timing']['sessions']==[] and p['calendar_links']==[]
    if s.startswith(('toronto-jr','carleton','mcmaster','stemminds')) or s=='thetech-camp-2027':assert not p['confirmed_instruction_languages']
assert new['toronto-deep-board-watch']['timing']['status']=='partial_2027'
assert new['toronto-deep-day-2027']['price']['year']==2026
for s in ['stemminds-junior-paused','stemminds-senior-paused']:
    assert new[s]['availability']['status']=='closed' and new[s]['availability']['label']=='Лагеря на паузе'
    assert all(v['status']=='not_eligible' for v in new[s]['family_fit'].values())
assert all(new[s]['confirmed_instruction_languages']==['EN'] and new[s]['price']['year'] is None for s in NEW[26:29])
assert new['id-battlebots-junior']['formats']==['day'] and new['id-battlebots-junior']['family_fit']['oscar']['status']=='conditional'
assert new['id-battlebots-junior']['family_fit']['matvey']['status']=='conditional'
assert 'VEX IQ' in new['id-battlebots-junior']['programme'] and 'VEX V5' in new['id-battlebots-vex']['programme']
assert 'Arduino IDE' in new['id-battlebots-takehome']['programme']
r=d['camp_programmes']['family_review'];assert r['coverage']==dict(candidates=57,countries=16,fully_audited_countries=0)
assert len({q['slug'] for q in r['entries']})==57 and r['entries'][:50]==b['camp_programmes']['family_review']['entries']
assert not any(q['slug'].startswith('stemminds') for q in r['entries'])
show=ne['TC2027-SHOWCASE'];assert show['date_scope']=='festival_window' and show['deadline']=='2026-12-31'
assert 'тарифа' in show['deadline_label'] and 'competition' in show['reward']
assert ne['TC2027-REGOPEN']['date_scope']=='registration_open'
assert all(ne[i]['event_kind']=='organizer_information_session' and not ne[i].get('sessions') and 'timezone' in ne[i]['note'] for i in EVENT_IDS[2:])
def clause(file,*words):
    def normal(s):return ''.join(s.lower().replace('’',"'").replace('–','-').replace('\xad','').split())
    text=normal((P/(file+'.txt')).read_text())
    for word in words:assert normal(word) in text,(file,word)
clause('toronto-jr','will not be eligible','completing Grade 2','$490/week','Robotics at Work','Mechatronics Lab','AI & Autonomous Systems')
clause('toronto-deep','July 5 – 9, 2027','July 26 – 30, 2027','these are 2026 prices','$1111/week','BOTH Grade 9 level math','first language')
clause('carleton-types','Programming Junior: Grade 3-5','a week entirely off-computers','all-girls senior camps','Sprockets: Grade JK-SK')
clause('carleton-fees','$339','$295','$50')
clause('mcmaster-camp','Fireball','Flare','entering','2026')
clause('stemminds-newcamps','Camps on Pause','Our camps are on pause for now')
clause('id-junior','VEX IQ','7-9','$1,199','March 1st','28 days','$250')
clause('id-vex','VEX V5','10-12','$1,299')
clause('id-3d','Arduino IDE','take home','$1,399')
clause('id-general','10-17','$679/week','$70/week')
clause('tech-camp','Summer 2027','entering grades 2-6','Lunch is not automatically included','Friday, July 3','30-59 days')
clause('tech-rules-pdf','NOT a competition','purchased kits','playtest')
clause('tech-faq','third-grader','2-6 students','Oct. 6th, 2026','Friday, April 30, 2027','no additional cost','spectators','Registration opens in February 2027')
clause('tech-events','October 20, 2026','November 18, 2026','December 16, 2026','January')
receipts=json.loads((ROOT/'data/northamerica-camps-source-receipts-v131.json').read_text())
assert len(receipts['sources'])==35 and not any(receipts['external_actions'].values())
assert len(receipts['web_primary_reader_sources'])==4 and any(s['url']==RES for s in receipts['web_primary_reader_sources'])
for q in receipts['sources']:
    if q['body_snapshot_retained']:
        raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
        if q['key'] in ['id-age','id-groups','id-english']:
            assert not (P/(q['key']+'.txt')).read_text().strip() and q['content_status']=='javascript_shell_not_programme_clause_evidence'
assert sum(q['body_snapshot_retained'] for q in receipts['sources'])==31
def blocks(raw):return {re.search(br'(?m)^UID:([^\r\n]+)',v).group(1):v for v in re.findall(br'BEGIN:VEVENT\r?\n.*?END:VEVENT\r?\n',raw,re.S)}
before=blocks(prior('dist/downloads/STEM_подтвержденные_даты.ics'));after=blocks((ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes())
assert len(before)==2993 and len(after)==3001 and all(before[k]==after[k] for k in before)
assert set(after)-set(before)=={('stem-'+i+'@family-stem.local').encode() for i in EVENT_IDS}|{b'stem-TC2027-SHOWCASE-deadline@family-stem.local'}
assert not any(b'CP1057' in k for k in after)
for i in EVENT_IDS[2:]:assert b'DTSTART;VALUE=DATE:' in after[('stem-'+i+'@family-stem.local').encode()]
assert (ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes()==prior('dist/downloads/STEM_крупные_выставки.ics')
def portable(meta,kind):
    m=json.loads((ROOT/'dist/downloads'/meta).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
    assert m['complete_database'] and len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256']
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        assert z.testzip() is None and z.namelist()==[m[kind+'_entry'],'README.txt'];body=z.read(m[kind+'_entry'])
    assert len(body)==m[kind+'_bytes'] and hashlib.sha256(body).hexdigest()==m[kind+'_sha256']
    assert m['raw_download_available']==(len(body)<=26214400)
    return body
assert json.loads(portable('STEM_database_json_download.json','json'))==d
sql=portable('STEM_database_download.json','sqlite');(P/'verified-v131.sqlite').write_bytes(sql)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as z:(P/'baseline-v130.sqlite').write_bytes(z.read('STEM_database.sqlite'))
c=sqlite3.connect(P/'verified-v131.sqlite');oc=sqlite3.connect(P/'baseline-v130.sqlite')
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
tables=[x[0] for x in oc.execute("SELECT name FROM sqlite_master WHERE type='table'")]
assert tables==[x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
for t in tables:
    a=oc.execute('SELECT * FROM '+t).fetchall();z=c.execute('SELECT * FROM '+t).fetchall()
    if t=='metadata':
        am=dict(a);zm=dict(z);changed={k for k in am if am[k]!=zm[k]};assert changed=={'camp_family_review','league_guide','camp_focus','completeness_audit'},changed
        assert json.loads(zm['camp_family_review'])==r and json.loads(zm['league_guide'])==d['league_guide']
    elif t in ['sources','events','event_countries','event_themes','camp_programmes','camp_programme_sources','camp_programme_events']:assert set(a)<=set(z),t
    elif t=='countries':
        assert [v for v in a if v[0] not in ['CAN','USA']]==[v for v in z if v[0] not in ['CAN','USA']]
        for iso,dc,de in [('CAN',4,0),('USA',0,7)]:
            x=next(v for v in a if v[0]==iso);y=next(v for v in z if v[0]==iso);assert x[:3]==y[:3]
            # The legacy coverage key 'exhibitions' counts the mixed Events
            # block; classification checks above exclude these from major expos.
            record=json.loads(x[3]);record['camps']+=dc;record['exhibitions']+=de;record['dated']+=dc+de;assert record==json.loads(y[3]),(iso,record,json.loads(y[3]))
    else:assert a==z,t
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']==plan['native_goal_status']=='active'
assert plan['human_scope_expansion']==json.loads(prior('data/research-plan.json'))['human_scope_expansion']
assert plan['next_research']==json.loads(prior('data/research-plan.json'))['next_research']
assert plan['current_publication']['status']=='prepared_local_not_published'
result=dict(status='passed',version=131,new_dossiers=30,new_dated_camp_rows=4,new_noncompetitive_event_rows=7,new_budget_scenarios=0,
    unchanged_dossiers=1049,unchanged_event_objects=3777,unchanged_budget_objects=55,unchanged_competition_objects=1153,
    old_guide_profiles_unchanged=141,new_profile_explicitly_noncompetitive=True,family_review_candidates=57,
    old_ics_blocks_byte_identical=2993,new_ics_entries=8,future_senior_camp_rows_excluded=True,qa_all_day_without_assumed_timezone=True,exhibition_ics_byte_identical=True,
    all_old_sqlite_entity_rows_preserved=True,derived_country_counts_updated=['CAN:+4camps/+4dated','USA:+7events/+7dated'],complete_sqlite_bytes=len(sql),complete_json_matches_catalog=True,
    retained_source_body_hashes_verified=31,empty_help_shells_not_counted_as_clause_evidence=True,source_grade_language_contract_years_pause_and_noncompetition_checked=True,
    goal='active',worldwide_complete=False,publication='prepared_local_not_published')
(P/'independent-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result))
