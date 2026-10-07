"""Independent source clauses and old-object preservation, with date/venue/price gates."""
import collections,csv,hashlib,io,json,re,sqlite3,subprocess,zipfile
from camp_europe_v127 import ROOT,BASE,NEW,NEW_IDS
P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v127'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={q['slug']:q for q in b['camp_programmes']['profiles']};z={q['slug']:q for q in d['camp_programmes']['profiles']}
assert len(a)==999 and len(z)==1015 and z.keys()-a.keys()==set(NEW) and all(z[k]==v for k,v in a.items())
assert d['camp_programmes']['shortlist'][:236]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==239
assert d['camp_programmes']['gaps'][:289]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==296
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']};expected={}
for slug in NEW:
    p=z[slug]
    if p['timing'].get('precision')=='season_window':continue
    for v in p['timing'].get('session_details',[]):
        key=p['id']+'-'+v['start'].replace('-','')+'-'+v['end'].replace('-','')
        if p['timing'].get('variant_keyed'):key+='-'+v['variant_key']
        expected[key]=(slug,v)
assert len(expected)==28 and len(now)==3769 and now.keys()-old.keys()==expected.keys() and all(now[k]==v for k,v in old.items())
assert collections.Counter(q['block'] for q in now.values())=={'Соревнования':1153,'События':189,'Лагеря':2427}
for key,(slug,v) in expected.items():
    e=now[key];assert (e['start'],e['end'],e['camp_dossier_slug'])==(v['start'],v['end'],slug) and e['date_precision']=='published_session'
    assert e['languages']==['EN'] and e['language_mode']==('bilingual' if slug.startswith('hopla-') else 'language_lessons' if slug.startswith('littlebritish-') else 'camp_life')
    if slug.startswith('littlebritish-'):
        assert e['date_scope']=='day_camp_window' and e['city']==v['place'] and e['attendance_weekdays']==['MO','TU','WE','TH','FR']
    elif slug=='hopla-outdoors':
        assert e['date_scope']=='session_days' and [x['date'] for x in e['sessions']]==['2027-07-12','2027-07-13','2027-07-15','2027-07-16']
        assert all(x['start_time']=='09:00' and x['end_time']=='16:30' and x['timezone']=='Europe/Paris' for x in e['sessions'])
    elif slug=='hif-winter-2027':assert e['date_scope']=='camp_session'
    else:assert e['date_scope']=='day_camp_window'
for slug in NEW:
    p=z[slug];assert p['checked']=='2026-10-06' and all(s['checked']=='2026-10-06' for s in p['sources'])
    assert p['confirmed_instruction_languages']==([] if slug=='ciencia-sorolla-camp' else ['EN'])
for slug in ['village-kids','village-teens','ciencia-sorolla-camp']:assert z[slug]['timing']['sessions']==[]
assert z['french-colo-summer']['timing']['precision']=='season_window' and all(x['kind']=='season_window' and not x['event_ids'] for x in z['french-colo-summer']['calendar_links'])
assert z['french-colo-summer']['family_fit']['matvey']['status']=='unknown'
for slug in ['littlebritish-winter-fairy','littlebritish-spring-london']:assert z[slug]['family_fit']['matvey']['status']=='not_eligible' and z[slug]['family_fit']['oscar']['status']=='conditional'
for slug in ['littlebritish-winter-boost','littlebritish-spring-boost']:assert all(q['status']=='unknown' for q in z[slug]['family_fit'].values())
assert z['hif-winter-2027']['family_fit']['matvey']['status']=='conditional' and z['hif-winter-2027']['family_fit']['oscar']['status']=='later'
o={q['id']:q for q in d['camp_planning']['offers']};assert len(o)==50 and o.keys()-{q['id'] for q in b['camp_planning']['offers']}==set(NEW_IDS)
assert all(o[q['id']]==q for q in b['camp_planning']['offers'])
assert o[NEW_IDS[0]]['base_by_child']=={'matvey':290,'oscar':290} and o[NEW_IDS[0]]['optional'][0]['amount']==100 and o[NEW_IDS[0]]['unknown_required']
assert o[NEW_IDS[1]]['children']==['matvey'] and o[NEW_IDS[1]]['base_by_child']=={'matvey':300}
brand=lambda n:'Enforex' if n.startswith('Enforex') else 'La Garenne' if n.startswith('La Garenne') else n.split(' · ')[0]
assert len({brand(z[q['slug']]['provider']) for q in o.values()})==26
osrc={q['url']:q for q in b['sources']};nsrc={q['url']:q for q in d['sources']};assert all(nsrc[k]==v for k,v in osrc.items())
fail=[]
def clause(key,*values):
    norm=lambda t:re.sub(r'\s+','',t).casefold().replace('–','-').replace('—','-')
    t=norm((P/(key+'.txt')).read_text())
    for v in values:
        if norm(v) not in t:fail.append((key,v))
clause('hopla-form','19 au 23 octobre 2026','15 au 19 février 2027','12 au 16 avril 2027','5 au 9 juillet 2027','12 au 16 juillet 2027','19 au 23 juillet 2027','23 au 27 août 2027','290 €','2,50 €','12 enfants maximum','au moins 6 enfants','15 jours','14 et 7 jours','50 %','français-anglais','Repas et goûters fournis par les familles')
clause('hopla-camp','14 juillet','All About Games')
for key,date in [('little-fairy','08 AU 12 février 2027'),('little-winter-boost','08 AU 12 février 2027'),('little-london','05 AU 09 avril 2027'),('little-spring-boost','05 AU 09 avril 2027')]:clause(key,date,'300 €','Paris 6','Paris 7','Paris 16','Paris 17','Meudon','2h30/ jour')
clause('little-fairy','3 - 6 ans','entièrement en anglais','expériences scientifiques')
clause('little-london','3 - 6 ans','100% anglais','activités de construction')
clause('little-winter-boost','CE1 au CM2','14h00 - 16h30');clause('little-spring-boost','CE1 au CM2','14h00 - 16h30')
clause('village-brochure','FECHAS VERANO 2026','8-12','13-17','Media','URH Zen Balagares')
clause('village-kids','2,290','4.460','2026','Spanish');clause('village-faq','85%','every 4 days','will not be washed','Family Day','7 days','General Terms and Conditions')
clause('hif-winter','10-20 February 2027','10–16','English','4,586','300','500','1,000','rented locally','11 days/10 nights','Phones')
clause('french-colo','2027','4 juillet au 27 août','10 à 16','11 à 16','galop 3','10h')
clause('french-colo-prices','765 €','910 €','25€','50€','10 h','6 jours')
clause('french-colo-cgv','33%','30 jours','35 €','60 jours','50 %','75 %','90 %','100 %','2024')
clause('science-robotics-pdf','VERANO 2026','234,00','439,00','614,00','789,00','170','2017 y 2016','2019 y 2018','2023','Inteligencia Artificial','ESO','equipo de robótica','por alumno')
clause('science-robotics-camp','6 y los 18','2026','Bularas, 2')
assert not fail,fail
r=json.loads((ROOT/'data/europe-camps-source-receipts-v127.json').read_text());assert len(r['sources'])==30 and sum(q.get('status')==200 for q in r['sources'])==28 and not any(r['external_actions'].values())
for q in r['sources']:
    if q['body_snapshot_retained']:
        raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert next(q for q in r['sources'] if q['key']=='space-os-trust-home')['content_status']=='client_rendered_landing_not_programme_evidence'
def portable(name,ext):
    m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
    assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
    with zipfile.ZipFile(io.BytesIO(raw)) as q:
        assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry'])
    assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
    assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
    return body
sql=portable('STEM_database_download.json','sqlite');assert json.loads(portable('STEM_database_json_download.json','json'))==d
f=P/'verified-v127.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v126.sqlite';f.write_bytes(oldsql);oc=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(oc)
changes={}
for name, in oc.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
    aa=set(oc.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'));removed={q[0] for q in aa-zz}
    allowed={'metadata':{'camp_focus','camp_planning','completeness_audit'},'countries':{'FRA','ESP','CHE'}}.get(name,set())
    assert removed<=allowed,(name,removed);assert {q[0] for q in aa}<={q[0] for q in zz},name
    if removed:changes[name]=sorted(removed)
assert c.execute('SELECT count(*) FROM events').fetchone()[0]==3769 and c.execute('SELECT count(*) FROM camp_programmes').fetchone()[0]==1015
c.close();oc.close()
def calendar(raw):
    t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
    for s in t.split('BEGIN:VEVENT')[1:]:
        f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None);assert f['UID'] not in out;out[f['UID']]=f
    return out
for name,count in [('STEM_подтвержденные_даты.ics',2974),('STEM_крупные_выставки.ics',104)]:
    aa=calendar(prior('dist/downloads/'+name));zz=calendar((ROOT/'dist/downloads'/name).read_bytes());assert len(zz)==count and all(zz[k]==v for k,v in aa.items())
    extra={k:v for k,v in zz.items() if k not in aa};assert len(extra)==(31 if count==2974 else 0)
    if extra:
        outdoor=[v for k,v in extra.items() if z['hopla-outdoors']['id'] in k];assert len(outdoor)==4
        assert sorted(v.get('DTSTART',v.get('DTSTART;TZID=Europe/Paris',''))[:8] for v in outdoor)==['20270712','20270713','20270715','20270716']
        assert all(v['DTSTART'].endswith('T070000Z') and v['DTEND'].endswith('T143000Z') for v in outdoor)
        assert all(any(e in uid for e in expected) for uid in extra)
for name in ['STEM_catalog.csv','STEM_country_coverage.csv']:
    rows=lambda raw:list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))));key='id' if name=='STEM_catalog.csv' else 'iso'
    x={q[key]:q for q in rows(prior('dist/downloads/'+name))};y={q[key]:q for q in rows((ROOT/'dist/downloads'/name).read_bytes())}
    assert all(y[k]==v for k,v in x.items() if key=='id' or k not in ['FRA','ESP','CHE']) and y.keys()-x.keys()==(expected.keys() if key=='id' else set())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for key in ['events','camp_programmes','camp_planning','league_guide','family_strategy']:assert web[key]==d[key]
plan=json.loads((ROOT/'data/research-plan.json').read_text());prev=json.loads(prior('data/research-plan.json'))
assert plan['status']=='active' and plan['native_goal_status']=='active' and plan['next_research']==prev['next_research']
assert [q['id'] for q in plan['requirements']]==[q['id'] for q in prev['requirements']]
assert plan['latest_validation']['fully_audited_countries']==0 and plan['latest_validation']['worldwide_complete'] is False
assert plan['current_publication']['status']=='prepared_local_not_published' and plan['current_publication']['last_confirmed_published_version']==125
for stem in ['research-plan','europe-camps-audit-v127','europe-camps-source-receipts-v127']:assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
assert 'data-ui-version="127"' in (ROOT/'dist/index.html').read_text()
for f in (ROOT/'dist').rglob('*'):
    if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['camp-planning.js','camp-programmes.js','data.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['nearby-participation.js','nearby-participation.css','experience.js','camp-planning.js','app.js']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=127,all_prior_events_preserved=3741,all_prior_dossiers_preserved=999,all_prior_budget_objects_preserved=48,new_dossiers=16,new_calendar_rows=28,new_budget_scenarios=2,venue_variants_distinct=True,holiday_july14_excluded=True,archived_prices_not_2027=True,age_grade_language_gates_checked=True,complete_sqlite=True,complete_json=True,sqlite_allowed_updated_keys=changes,family_ical=2974,exhibition_ical=104,worldwide_scope_preserved=True,goal='active',publication='prepared_local_not_published')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
