"""Independent source clauses, family gates, mandatory costs and exact old-object preservation."""
import collections,csv,hashlib,io,json,re,sqlite3,subprocess,zipfile
from camp_asia_v128 import ROOT,BASE,NEW,NEW_IDS,COBO_DATED
P=ROOT.parent/'stem-family-atlas-work/camp-asia-primary-v128'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
mutable={'events','source_count','sources','coverage','completeness_audit','camp_focus','camp_programmes','camp_planning'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
a={q['slug']:q for q in b['camp_programmes']['profiles']};z={q['slug']:q for q in d['camp_programmes']['profiles']}
assert len(a)==1015 and len(z)==1034 and z.keys()-a.keys()==set(NEW) and all(z[k]==v for k,v in a.items())
assert d['camp_programmes']['shortlist'][:239]==b['camp_programmes']['shortlist'] and len(d['camp_programmes']['shortlist'])==242
assert d['camp_programmes']['gaps'][:296]==b['camp_programmes']['gaps'] and len(d['camp_programmes']['gaps'])==303
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']};expected={}
for slug in NEW:
    p=z[slug]
    for v in p['timing'].get('session_details',[]):
        key=p['id']+'-'+v['start'].replace('-','')+'-'+v['end'].replace('-','');expected[key]=(slug,v)
assert len(expected)==6 and len(now)==3775 and now.keys()-old.keys()==expected.keys() and all(now[k]==v for k,v in old.items())
assert collections.Counter(q['block'] for q in now.values())=={'Соревнования':1153,'События':189,'Лагеря':2433}
for key,(slug,v) in expected.items():
    e=now[key];assert (e['start'],e['end'],e['camp_dossier_slug'])==(v['start'],v['end'],slug)
    assert e['languages']==['EN'] and e['date_precision']=='published_session'
    if slug.startswith('cobo-'):
        assert e['date_scope']=='session_days' and e['sessions']==v['sessions'] and e['language_mode']=='primary'
        assert [q['date'] for q in e['sessions']]==['2026-10-20','2026-10-21','2026-10-22','2026-10-23']
        i=NEW.index(slug);times=COBO_DATED[i];assert all(q['start_time']==times[0] and q['end_time']==times[1] and q['timezone']=='Asia/Hong_Kong' and q['ical_timed'] for q in e['sessions'])
    else:assert e['date_scope']=='day_camp_window' and e['language_mode']=='camp_life' and e['attendance_weekdays']==['MO','TU','WE','TH','FR']
for slug in NEW:
    p=z[slug];assert p['checked']=='2026-10-06' and all(s['checked']=='2026-10-06' for s in p['sources'])
    assert p['confirmed_instruction_languages']==([] if slug.startswith('kas-') else ['EN'])
for i in [0,4,5,7]+list(range(10,19)):assert not z[NEW[i]]['timing']['sessions']
assert z['cobo-arcade-junior']['family_fit']['oscar']['status']=='unknown'
assert all(q['status']=='later' for q in z['cobo-hackathon-principal']['family_fit'].values())
assert all(q['status']=='unknown' for q in z['kas-future-city']['family_fit'].values())
assert z['headstart-activity']['family_fit']['oscar']['status']=='not_eligible'
assert all(z[slug]['language_evidence_role']=='language_lessons' for slug in ['brighton-vibha-ai','brighton-vibha-general'])
o={q['id']:q for q in d['camp_planning']['offers']};assert len(o)==53 and o.keys()-{q['id'] for q in b['camp_planning']['offers']}==set(NEW_IDS)
assert all(o[q['id']]==q for q in b['camp_planning']['offers'])
q=o[NEW_IDS[0]];assert q['base_by_child']=={'matvey':70000,'oscar':70000} and [x['amount'] for x in q['required']]==[10000,30000,18000]
assert sum(q['base_by_child'].values())+sum(x['amount'] for x in q['required'])==198000 and q['unknown_required'] and q['price_year']==2026
assert o[NEW_IDS[1]]['children']==['matvey'] and o[NEW_IDS[1]]['base_by_child']=={'matvey':3600}
assert o[NEW_IDS[2]]['children']==['oscar'] and o[NEW_IDS[2]]['base_by_child']=={'oscar':3600}
osrc={q['url']:q for q in b['sources']};nsrc={q['url']:q for q in d['sources']};assert all(nsrc[k]==v for k,v in osrc.items())
fail=[]
def clause(key,*values):
    norm=lambda t:re.sub(r'\s+','',t).casefold().replace('–','-').replace('—','-')
    t=norm((P/(key+'.txt')).read_text())
    for v in values:
        if norm(v) not in t:fail.append((key,v))
for key in ['cobo-wedo','cobo-spike-junior','cobo-spike-senior','cobo-vex','cobo-arcade-junior','cobo-arcade-senior','cobo-ai-junior','cobo-ai-senior','cobo-hackathon']:clause(key,'Medium of Instruction: English','Each daily lesson is 2 hours','4-8 students')
for key,slot in [('cobo-spike-junior','10:00 - 12:00'),('cobo-spike-senior','14:00 - 16:00'),('cobo-vex','14:00 - 16:00'),('cobo-ai-junior','10:00 - 12:00'),('cobo-hackathon','10:00 - 12:00')]:clause(key,'20-10-2026','23-10-2026','TUE, WED, THU, FRI',slot,'8 hrs','3,600')
for key in ['cobo-wedo','cobo-arcade-junior','cobo-arcade-senior','cobo-ai-senior']:assert 'Period:' not in (P/(key+'.txt')).read_text()
clause('cobo-spike-junior','LEGO WeDo 2.0','Scratch','Laptop');clause('cobo-vex','15+','hardware','Blocks, C++ and Python','VEX IQ kit')
clause('cobo-ai-junior','Previous experience with programming is essential','Teachable Machine');clause('cobo-arcade-junior','Ages 6-8','aged 8+','HKD 400 (inclusive)','take home','USB-C')
clause('cobo-hackathon','12-14','Figma','Base44','certificates and awards','No prior coding experience required')
clause('cobo-terms','at least 3 weeks','non-refundable after registration','NOT applicable to Holiday Camps','Typhoon signal 8','without refund or make-up','before and after class')
clause('cobo-camps','before Sep 30','extra 10% discount','Oct 20 - 23')
clause('owis-winter','14th–Friday 18th December 2026','Children aged 4–16','Open to OWIS and external students','Registrations are not yet open','¥70,000','¥5,000','¥15,000','10%','No school bus','No overnight accommodation','previous programme','Immersive English','8:30–8:45','3:30 pm–4:00 pm')
clause('owis-act','One World Tsukuba','Consumption tax (included in the product price)','School Management approval');clause('owis-service','website','Singapore')
clause('kas-reader','PK–G5','English-based schools','3D models','registration is closed')
clause('kas-schedule','July 13 - 17','July 20 - 24','draft','Parents Invited');clause('kas-terms','7/13–7/20','16,500','15,500','March 19, 2026','two (2) weeks','15 working days','50%','10 campers','2 educators : 9 children','lunch is provided daily')
clause('headstart-mirror','All lessons, instructions and camp activities are conducted in English','Weekly Fee: 18,000','Weekly Fee: 20,000','maximum of 24','age after 1 July','40,000 THB','groups of 4','2,000 THB','80% Refund','more than 14 days','less than 14 days','3,000 THB','do not provide or arrange accommodation','Chaofah City','3x per week')
clause('headstart-options-mirror','Weeks 3–5','Weeks 3–6','VEX robots','CYBERone','Roblox','personalised game link','three times per week')
clause('brighton-july','29 June – 17 July 2026','3–12 years','18,000','32,000','45,000','21,000','40,000','55,000','Morning: English','Afternoon: AI, Robotics & Coding')
clause('brighton-brochure','9.00-12.00','13.00-15.00','Face and object detection','Speech recognition','Teddy Tower','Machine learning concepts','Online safety and privacy')
clause('brighton-activity-description','Egg Drop Challenge','Bridge Building','polymers','Kite');clause('brighton-activity-schedule','6-12YO','sample schedule')
assert not fail,fail
r=json.loads((ROOT/'data/asia-camps-source-receipts-v128.json').read_text());assert len(r['sources'])==30 and sum(q.get('status')==200 for q in r['sources'])==27 and not any(r['external_actions'].values())
for q in r['sources']:
    if q['body_snapshot_retained']:
        raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert r['pdf_text_pages_extracted']==27 and r['visual_source_images_checked']==['brighton-ai-schedule.jpg']
def portable(name,ext):
    m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
    assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
    with zipfile.ZipFile(io.BytesIO(raw)) as q:assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry'])
    assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
    assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
    return body
sql=portable('STEM_database_download.json','sqlite');assert json.loads(portable('STEM_database_json_download.json','json'))==d
f=P/'verified-v128.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:oldsql=q.read('STEM_database.sqlite')
f=P/'baseline-v127.sqlite';f.write_bytes(oldsql);oc=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(oc)
changes={}
for name, in oc.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
    aa=set(oc.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'));removed={q[0] for q in aa-zz}
    allowed={'metadata':{'camp_focus','camp_planning','completeness_audit'},'countries':{'HKG','JPN','TWN','THA'}}.get(name,set())
    assert removed<=allowed,(name,removed);assert {q[0] for q in aa}<={q[0] for q in zz},name
    if removed:changes[name]=sorted(removed)
assert c.execute('SELECT count(*) FROM events').fetchone()[0]==3775 and c.execute('SELECT count(*) FROM camp_programmes').fetchone()[0]==1034
c.close();oc.close()
def calendar(raw):
    t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
    for s in t.split('BEGIN:VEVENT')[1:]:
        f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None);assert f['UID'] not in out;out[f['UID']]=f
    return out
for name,count in [('STEM_подтвержденные_даты.ics',2991),('STEM_крупные_выставки.ics',104)]:
    aa=calendar(prior('dist/downloads/'+name));zz=calendar((ROOT/'dist/downloads'/name).read_bytes());assert len(zz)==count and all(zz[k]==v for k,v in aa.items())
    extra={k:v for k,v in zz.items() if k not in aa};assert len(extra)==(17 if count==2991 else 0)
    if extra:
        assert not any(z['cobo-hackathon-principal']['id'] in uid for uid in extra)
        for slug in [NEW[i] for i in COBO_DATED if i!=8]:
            rows=[v for k,v in extra.items() if z[slug]['id'] in k];assert len(rows)==4
            assert sorted(v['DTSTART'][:8] for v in rows)==['20261020','20261021','20261022','20261023']
            time=COBO_DATED[NEW.index(slug)][0];hour='02' if time=='10:00' else '06'
            assert all(v['DTSTART'].endswith('T'+hour+'0000Z') and v['DTEND'].endswith('T'+('04' if hour=='02' else '08')+'0000Z') for v in rows)
for name in ['STEM_catalog.csv','STEM_country_coverage.csv']:
    rows=lambda raw:list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))));key='id' if name=='STEM_catalog.csv' else 'iso'
    x={q[key]:q for q in rows(prior('dist/downloads/'+name))};y={q[key]:q for q in rows((ROOT/'dist/downloads'/name).read_bytes())}
    assert all(y[k]==v for k,v in x.items() if key=='id' or k not in ['HKG','JPN','TWN','THA']) and y.keys()-x.keys()==(expected.keys() if key=='id' else set())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for key in ['events','camp_programmes','camp_planning','league_guide','family_strategy']:assert web[key]==d[key]
plan=json.loads((ROOT/'data/research-plan.json').read_text());prev=json.loads(prior('data/research-plan.json'))
assert plan['status']=='active' and plan['native_goal_status']=='active' and plan['next_research']==prev['next_research']
assert [q['id'] for q in plan['requirements']]==[q['id'] for q in prev['requirements']]
assert plan['latest_validation']['fully_audited_countries']==0 and plan['latest_validation']['worldwide_complete'] is False
assert plan['current_publication']['status']=='prepared_local_not_published' and plan['current_publication']['last_confirmed_published_version']==125
for stem in ['research-plan','asia-camps-audit-v128','asia-camps-source-receipts-v128']:assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
assert 'data-ui-version="128"' in (ROOT/'dist/index.html').read_text()
for f in (ROOT/'dist').rglob('*'):
    if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['camp-planning.js','camp-programmes.js','data.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['nearby-participation.js','nearby-participation.css','experience.js','camp-planning.js','app.js']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=128,all_prior_events_preserved=3769,all_prior_dossiers_preserved=1015,all_prior_budget_objects_preserved=50,new_dossiers=19,new_calendar_rows=6,new_budget_scenarios=3,course_specific_dates_only=True,timed_cobo_lessons=16,hackathon_12plus_excluded_from_family_ical=True,owis_two_new_external_mandatory_total=198000,unknown_lunch_not_zero=True,archived_prices_not_2027=True,age_grade_language_gates_checked=True,complete_sqlite=True,complete_json=True,sqlite_allowed_updated_keys=changes,family_ical=2991,exhibition_ical=104,worldwide_scope_preserved=True,goal='active',publication='prepared_local_not_published')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
