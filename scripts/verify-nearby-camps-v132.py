"""Independent source, preservation, category, portable database and ICS checks."""
import hashlib,io,json,re,sqlite3,subprocess,zipfile
from collections import Counter
from camp_nearby_v132 import ROOT,BASE,NEW,EVENT_IDS,TERMS,REFUND,POLICY

P=ROOT.parent/'stem-family-atlas-work/nearby-latam-primary-v132'
def prior(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={p['slug']:p for p in b['camp_programmes']['profiles']};new={p['slug']:p for p in d['camp_programmes']['profiles']}
assert len(old)==1079 and len(new)==1084 and set(new)-set(old)==set(NEW)
assert all(old[s]==new[s] for s in old if s!='cenfotec-makers')
assert {k for k in old['cenfotec-makers'] if old['cenfotec-makers'][k]!=new['cenfotec-makers'][k]}=={'checked','sources','price','questions'}
assert new['cenfotec-makers']['calendar_links']==old['cenfotec-makers']['calendar_links']
assert new['cenfotec-makers']['price']['deposit']==REFUND and any(s['url']==TERMS for s in new['cenfotec-makers']['sources'])
oe={e['id']:e for e in b['events']};ne={e['id']:e for e in d['events']}
campid='CP1080-20261207-20261211'
assert len(oe)==3788 and len(ne)==3793 and all(oe[s]==ne[s] for s in oe)
assert set(ne)-set(oe)==set(EVENT_IDS)|{campid}
assert Counter(e['block'] for e in d['events'])==dict(Соревнования=1157,События=196,Лагеря=2440)
assert ne[campid]['block']=='Лагеря' and ne[campid]['priority'].startswith('P4')
assert d['camp_planning']==b['camp_planning'] and len(d['camp_planning']['offers'])==55
for key in ['school_focus','school_history','schools','development_routes','leagues']:assert d[key]==b[key],key
fs=dict(d['family_strategy']);assert fs.pop('nearby_participation_v132')['version']==132 and fs==b['family_strategy']
gp={p['id']:p for p in d['league_guide']['profiles']};op={p['id']:p for p in b['league_guide']['profiles']}
assert len(gp)==len(op)==142 and all(gp[k]==op[k] for k in op if k!='vex')
assert {k for k in op['vex'] if op['vex'][k]!=gp['vex'][k]}=={'event_ids','nuances','sources'}
assert gp['vex']['event_ids']==op['vex']['event_ids']+EVENT_IDS
assert gp['vex']['nuances'][:-1]==op['vex']['nuances'] and gp['vex']['sources'][:-4]==op['vex']['sources']
assert len({e['event_code'] for e in d['events'] if e.get('event_code')})==len([e for e in d['events'] if e.get('event_code')])
for i in EVENT_IDS:
    e=ne[i];assert e['block']=='Соревнования' and e['languages']==[] and not e.get('exhibition_tier')
    assert e['deadline_utc']==e['start']+'T17:00:00Z' and not e['priority'].startswith('P4')
    assert 'Условно' in e['mat'] and 'Условно' in e['osc'] and 'местный' in e['mat']
assert ne['C1156']['admission_kind']=='invitation' and '2026' in ne['C1156']['note']
assert 'USD 0' in ne['C1155']['cost'] and 'не установлена' in ne['C1155']['cost']
for s in NEW:
    p=new[s];assert p['checked']=='2026-10-06' and not p['confirmed_instruction_languages']
    if s!='cenfotec-ai-teen':assert not p['timing']['sessions'] and not p['calendar_links']
assert new['cenfotec-cyber-teen']['price']['year'] is None and 'без года' in new['cenfotec-cyber-teen']['timing']['label']
assert new['curious-heredia-regular']['programme_type']=='regular_learning'
assert all(q['status']=='conditional' for q in new['curious-heredia-regular']['family_fit'].values())
assert all(q['status']=='unknown' for q in new['rocket-babies-workshop']['family_fit'].values())
r=d['camp_programmes']['family_review'];assert r['coverage']==dict(candidates=58,countries=16,fully_audited_countries=0)
assert r['entries'][:-1]==b['camp_programmes']['family_review']['entries'] and r['entries'][-1]['slug']=='curious-heredia-regular'
def clause(file,*words):
    def norm(s):return ''.join(s.lower().replace('–','-').replace('’',"'").split())
    txt=norm((P/(file+'.txt')).read_text())
    for word in words:assert norm(word) in txt,(file,word)
clause('cenfotec-makers','10 a 12','7 de diciembre de 2026','11 de diciembre de 2026','180','2% IVA')
clause('cenfotec-ai-kids','14 a 16','7 de diciembre de 2026','11 de diciembre de 2026','120','prompts')
clause('cenfotec-cyberheroes','13 a 15','Lunes 7 de diciembre','phishing')
assert 'diciembre de 2026' not in (P/'cenfotec-cyberheroes.txt').read_text()
clause('cenfotec-terms','Cobramos el importe del pedido en US$','un día hábil','80%','07','antes de la fecha en que inicia el curso')
clause('curious-home','a partir de los 3 años','Lego Education','Heredia Centro','Local #2')
clause('cerebritos-home','Semana Santa','diciembre','verano','4PM A 5:30','6PM A 7:30')
clause('rocket-babies','niñas de entre 6 y 13','niñas y niños','3 horas','33.000','IVA incluido','CETAV')
receipts=json.loads((ROOT/'data/nearby-camps-source-receipts-v132.json').read_text())
assert len(receipts['sources'])==22 and len(receipts['web_primary_reader_sources'])==5 and not any(receipts['external_actions'].values())
for q in receipts['sources']:
    if q['body_snapshot_retained']:
        raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
        if q['key']=='liota-home':assert q['content_status']=='javascript_shell_not_programme_clause_evidence' and len((P/'liota-home.txt').read_text().strip())<50
assert sum(q['body_snapshot_retained'] for q in receipts['sources'])==14
def blocks(raw):return {re.search(br'(?m)^UID:([^\r\n]+)',v).group(1):v for v in re.findall(br'BEGIN:VEVENT\r?\n.*?END:VEVENT\r?\n',raw,re.S)}
before=blocks(prior('dist/downloads/STEM_подтвержденные_даты.ics'));after=blocks((ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes())
assert len(before)==3001 and len(after)==3009 and all(before[k]==after[k] for k in before)
assert set(after)-set(before)=={('stem-'+i+suffix+'@family-stem.local').encode() for i in EVENT_IDS for suffix in ['','-deadline']}
assert not any(b'CP1080' in k for k in after)
for i in EVENT_IDS:assert b'DTSTART:'+ne[i]['deadline_utc'].replace('-','').replace(':','').encode() in after[('stem-'+i+'-deadline@family-stem.local').encode()]
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
sql=portable('STEM_database_download.json','sqlite');(P/'verified-v132.sqlite').write_bytes(sql)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as z:(P/'baseline-v131.sqlite').write_bytes(z.read('STEM_database.sqlite'))
c=sqlite3.connect(P/'verified-v132.sqlite');oc=sqlite3.connect(P/'baseline-v131.sqlite')
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
tables=[x[0] for x in oc.execute("SELECT name FROM sqlite_master WHERE type='table'")]
assert tables==[x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
for t in tables:
    a=oc.execute('SELECT * FROM '+t).fetchall();z=c.execute('SELECT * FROM '+t).fetchall()
    if t=='metadata':
        am=dict(a);zm=dict(z);changed={k for k in am if am[k]!=zm[k]}
        assert changed=={'camp_family_review','league_guide','camp_focus','completeness_audit','family_strategy'},changed
    elif t=='camp_programmes':assert {x for x in a if x[0]!='CP090'}<=set(z)
    elif t in ['sources','events','event_countries','event_themes','camp_programme_sources','camp_programme_events']:assert set(a)<=set(z),t
    elif t=='countries':
        assert [v for v in a if v[0] not in ['CRI','MEX']]==[v for v in z if v[0] not in ['CRI','MEX']]
        for iso,camps,comps in [('CRI',1,0),('MEX',0,4)]:
            x=next(v for v in a if v[0]==iso);y=next(v for v in z if v[0]==iso);assert x[:3]==y[:3]
            record=json.loads(x[3]);record['camps']+=camps;record['competitions']+=comps;record['dated']+=camps+comps
            assert record==json.loads(y[3]),(iso,record,json.loads(y[3]))
    else:assert a==z,t
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==132
assert plan['human_scope_expansion']==bp['human_scope_expansion'] and plan['next_research']==bp['next_research']
assert plan['current_publication']['status']=='prepared_local_not_published'
result=dict(status='passed',version=132,new_dossiers=5,updated_existing_dossiers=['CP090'],new_competition_categories=4,new_dated_camp_rows=1,
    unchanged_event_objects=3788,unchanged_dossiers=1078,unchanged_budget_objects=55,unchanged_guide_profiles=141,updated_guide_profiles=['vex'],
    family_review_candidates=58,old_ics_blocks_byte_identical=3001,new_ics_entries=8,deadline_utc_17_correct=True,senior_course_excluded_from_young_family_ical=True,
    exhibition_ics_byte_identical=True,old_sqlite_entity_rows_preserved_except_owned_CP090=True,complete_sqlite_bytes=len(sql),complete_json_matches_catalog=True,
    source_bodies_hash_verified=14,empty_shell_not_clause_evidence=True,unknown_language_and_admission_preserved=True,no_school_prizes_inferred=True,
    unchanged_worldwide_goal_scope=True,goal='active',worldwide_complete=False,publication='prepared_local_not_published')
(P/'independent-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result))
