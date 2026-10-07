"""Independent source gates, old-row continuity and full portable-export checks."""
import collections,csv,datetime,hashlib,io,json,sqlite3,subprocess,zipfile
from pathlib import Path
from opportunities_v107 import ROOT,BASE,NEW_IDS,UPDATED,enrich
from database_download import package_json
P=ROOT.parent/'stem-family-atlas-work/opportunities-primary-v107'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clauses(key,*values):
    t=' '.join((P/(key+'.txt')).read_text().split())
    for v in values:assert ' '.join(v.split()) in t,(key,v)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};ev={e['id']:e for e in d['events']}
assert len(ev)==len(d['events'])==3348 and len(old)==3337
assert set(ev)-set(old)==set(NEW_IDS)
assert {k for k,v in old.items() if ev[k]!=v}==set(UPDATED)
assert collections.Counter(e['block'] for e in d['events'])=={'Соревнования':1153,'События':189,'Лагеря':2006}
for k in ['leagues','development_routes','schools','school_history','family_context','family_strategy','top_picks','camp_programmes','camp_focus','school_focus','project_focus','kazakhstan_focus','europe_focus','east_asia_focus']:
    assert d[k]==b[k],k
before={p['id']:p for p in b['league_guide']['profiles']};now={p['id']:p for p in d['league_guide']['profiles']}
assert len(now)==141 and set(now)-set(before)=={'world-robot-league'}
assert {k for k,v in before.items() if now[k]!=v}=={'waicy'}
for p in now.values():assert set(p['event_ids'])<=set(ev)
x=json.loads(json.dumps(d));enrich(x);assert x==d,'Data transformation must be idempotent'
clauses('roborave-amaze','2-4 students','8–15 years','Elementary School · 8–11')
clauses('roborave-houston','November 5, 2027','November 7, 2027','Por confirmar')
clauses('roborave-guanajuato','May 21, 2027','May 22, 2027')
assert 'tentativ' in (P/'roborave-guanajuato.txt').read_text().lower()
assert not ev['C083']['start'] and ev['C083']['scope']=='national'
assert '2020' in ev['C087']['osc'] and 'максимум 7' in ev['C087']['osc'] and ev['C087']['osc'].startswith('Нет')
for day in [datetime.date(2027,1,1),datetime.date(2027,12,31)]:assert day.year-2020<8
clauses('worldrobotleague-home','February 2027','TBA','9 Events · 29 Divisions','Online registration for domestic and international teams','fees and payment methods')
clauses('wrl-othello-rules','12 years old or under','Planned (TBA)','≤ 500g','11.7V or less')
clauses('wrl-soccer-rules','Junior (ages 5–13)','2–3 players with 2–4 robots','All-LEGO hardware exclusively','at least 50 days')
clauses('mrc-lego','Junior','5 ปี จนถึง 13 ปี','All Lego Hardware','13-02-2026')
clauses('wrl-humanoid-relay','no restriction on age or nationality','Robot specifications, team composition, mission details and scoring are being finalised')
clauses('wrl-roborave-rules','800 mm','100 cm','LEGO/VEX IQ 1 kg (ES)','800 g class','ES 75–125')
assert all(not ev[k]['start'] and not ev[k]['deadline'] and ev[k]['languages']==[] for k in NEW_IDS[:7])
assert ev['C1151']['osc'].startswith('Нет')
clauses('waicy-2026','ages 6–18','including remote participation','Be the first to know')
clauses('waicy-guide-curl','Submission Deadline: November 29, 2026, 5:00 PM ET','Competition date: December 4th-6th, 2025','scheduled for December 5th - 7th','November 29, 2025','December 4th-6th, 2026','The Future We Choose','This track is open to all grades','1–2 minute','English or subtitled in English','upper-middle and high school','no separate categories for different age groups')
assert all(ev[k]['deadline_utc']=='2026-11-29T22:00:00Z' and not ev[k]['start'] for k in ['C1152','C1153','C1154'])
assert not ev['C037']['deadline'] and 'Showcase' in ev['C037']['period']
clauses('robofest-general','TENTATIVE May 28, 29, 30, & 31','School Grade in spring 2027','Jr. (5~8)')
clauses('robofest-host','공식 확정했다')
assert not ev['C053']['start'] and 'Конфликт' in ev['C053']['note']
clauses('beijing-robot-marathon','2027年4月18日','全球机器人创新团队')
assert ev['E189']['start']==ev['E189']['end']=='2027-04-18' and not ev['E189'].get('exhibition_tier')
assert ev['E189']['visitor_policy']=='confirm_children' and ev['E189']['participation']=='visitor'
r=json.loads((ROOT/'data/opportunities-source-receipts-v107.json').read_text())
assert len(r['sources'])==28 and sum(q.get('status')==200 for q in r['sources'])==25
assert not any(r['external_actions'].values())
for q in r['sources']:
    if q['body_snapshot_retained']:
        body=(P/q['raw_filename']).read_bytes();assert len(body)==q['bytes'] and hashlib.sha256(body).hexdigest()==q['sha256']
for name,pages in [('waicy-guide-curl',[3,9,14,20,29]),('robofest-general',[11,24])]:
    assert all((P/(name+'-page-'+str(i)+'.png')).stat().st_size>1000 for i in pages)

def portable(stem,extension):
    m=json.loads((ROOT/'dist/downloads'/stem).read_text());zbody=(ROOT/'dist/downloads'/m['download']).read_bytes()
    assert len(zbody)==m['archive_bytes'] and hashlib.sha256(zbody).hexdigest()==m['archive_sha256'] and m['complete_database']
    with zipfile.ZipFile(io.BytesIO(zbody)) as z:
        assert z.testzip() is None and z.namelist()==[m[extension+'_entry'],'README.txt']
        body=z.read(m[extension+'_entry']);assert m[extension+'_sha256'] in z.read('README.txt').decode()
    assert len(body)==m[extension+'_bytes'] and hashlib.sha256(body).hexdigest()==m[extension+'_sha256']
    raw=ROOT/'dist/downloads'/m[extension+'_entry'];assert raw.exists()==m['raw_download_available']
    if raw.exists():assert raw.read_bytes()==body
    return body,m
body,sqlmanifest=portable('STEM_database_download.json','sqlite')
jbody,jsonmanifest=portable('STEM_database_json_download.json','json')
assert json.loads(jbody)==d
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==d['camp_programmes']
current=P/'checked.sqlite';current.write_bytes(body);con=sqlite3.connect(current)
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert {json.loads(r)['id']:json.loads(r) for r, in con.execute('SELECT record_json FROM events')}==ev
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as z:oldbody=z.read('STEM_database.sqlite')
f=P/'baseline-v106.sqlite';f.write_bytes(oldbody);oc=sqlite3.connect(f)
schema=lambda c:sorted(c.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"))
assert schema(oc)==schema(con)
for name, in oc.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
    rows=set(oc.execute('SELECT * FROM "'+name+'"'));curr=set(con.execute('SELECT * FROM "'+name+'"'));delta=rows-curr
    if name=='events':assert {r[0] for r in delta}==set(UPDATED)
    elif name=='metadata':assert {r[0] for r in delta}=={'league_guide','coverage_summary','completeness_audit'}
    elif name=='countries':
        assert {r[0] for r in delta}=={'KOR','CHN'}
        for r in delta:assert con.execute('SELECT iso,country,region FROM countries WHERE iso=?',(r[0],)).fetchone()==r[:3]
    else:assert not delta,name
oc.close();con.close()
# Exercise removal and retention with the actual complete JSON, without shrinking its records.
for name,limit,available in [('json-remove',1,False),('json-retain',len(jbody),True)]:
    folder=P/name;folder.mkdir(exist_ok=True);raw=folder/'STEM_database.json';raw.write_bytes(jbody)
    m=package_json(raw,limit);assert raw.exists()==available and m['raw_download_available']==available
    assert m['archive_sha256']==jsonmanifest['archive_sha256'] and m['json_sha256']==jsonmanifest['json_sha256']
assert all(f.stat().st_size<=26214400 for f in (ROOT/'dist').rglob('*') if f.is_file())
rows=lambda raw:{r['id']:r for r in csv.DictReader(raw.decode('utf-8-sig').splitlines())}
oldcsv=rows(prior('dist/downloads/STEM_catalog.csv'));csvrows=rows((ROOT/'dist/downloads/STEM_catalog.csv').read_bytes())
assert set(csvrows)-set(oldcsv)==set(NEW_IDS) and {k for k,v in oldcsv.items() if csvrows[k]!=v}==set(UPDATED)
def calendar(raw):
    out={};t=raw.decode().replace('\r\n ','').replace('\r\n\t','')
    for s in t.split('BEGIN:VEVENT')[1:]:
        f={x.split(':',1)[0]:x.split(':',1)[1] for x in s.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert f['UID'] not in out;out[f['UID']]=f
    return out
path='dist/downloads/STEM_подтвержденные_даты.ics';before=calendar(prior(path));now=calendar((ROOT/path).read_bytes())
assert len(before)==2591 and len(now)==2593 and set(before)<=set(now)
assert set(now)-set(before)=={'stem-C1152-deadline@family-stem.local','stem-E189@family-stem.local'}
changed=set()
for uid,v in before.items():
    a={k:x for k,x in v.items() if k!='DTSTAMP'};z={k:x for k,x in now[uid].items() if k!='DTSTAMP'}
    if a!=z:changed.add(uid)
assert changed=={'stem-C082@family-stem.local','stem-C087@family-stem.local'}
deadline=now['stem-C1152-deadline@family-stem.local'];assert deadline['DTSTART']=='20261129T220000Z' and deadline['DTEND']=='20261129T220100Z'
assert now['stem-E189@family-stem.local']['DTEND;VALUE=DATE']=='20270419'
path='dist/downloads/STEM_крупные_выставки.ics';before=calendar(prior(path));now=calendar((ROOT/path).read_bytes())
assert len(now)==104 and set(before)==set(now)
for uid,v in before.items():assert {k:x for k,x in v.items() if k!='DTSTAMP'}=={k:x for k,x in now[uid].items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==107
assert {q['id'] for q in plan['requirements']}=={q['id'] for q in bp['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==bp[k],k
assert d['coverage_summary']['fully_audited_countries']==0 and not plan['latest_validation']['worldwide_complete']
assert plan['complete_database_download']==sqlmanifest and plan['complete_json_download']==jsonmanifest
for stem in ['research-plan','opportunities-audit-v107','opportunities-source-receipts-v107']:
    assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
html=(ROOT/'dist/index.html').read_text();assert 'data-ui-version="107"' in html
assert 'href="downloads/STEM_database_json.zip"' in html and 'href="downloads/STEM_database.json"' not in html
assert 'STEM_opportunities_audit_v107.json' in html
web=(ROOT/'dist/assets/data.js').read_text();v=json.loads(web.removeprefix('window.STEM_DATA=').removesuffix(';\n'));assert v['events']==d['events'] and v['league_guide']==d['league_guide'] and v['camp_programmes']==d['camp_programmes']
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/data.js')],check=True)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
print(json.dumps(dict(status='passed',version=107,events=3348,camp_dossiers=778,new_competitions=10,new_visitor_events=1,corrected_oldcards=5,league_profiles=141,family_ics=2593,exhibition_ics=104,goal='active')))
