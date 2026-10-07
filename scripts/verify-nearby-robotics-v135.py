"""Independent preservation, source, calendar and complete-export checks."""
import hashlib,io,json,re,sqlite3,subprocess,zipfile
from collections import Counter
from nearby_robotics_v135 import ROOT,BASE,NEW_IDS,RL_IDS,GUIDES

P=ROOT.parent/'stem-family-atlas-work/robotics-nearby-primary-v135'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
oe={e['id']:e for e in b['events']};ne={e['id']:e for e in d['events']}
assert len(oe)==3808 and len(ne)==3829 and set(ne)-set(oe)==set(NEW_IDS)
assert {k for k in oe if oe[k]!=ne[k]}=={'C043','C064'}
assert Counter(e['block'] for e in d['events'])==dict(Соревнования=1168,События=207,Лагеря=2454)
assert ne['C043']['start']=='2027-03-03' and ne['C043']['end']=='2027-03-06'
assert ne['C043']['date_status']=='Подтверждено' and not ne['C043']['deadline']
assert ne['C064']['start']==oe['C064']['start'] and ne['C064']['deadline']=='2026-10-16'
assert {k for k in oe['C064'] if oe['C064'][k]!=ne['C064'].get(k)}=={'checked','proof'}
assert '2.º' in ne['C064']['proof'] and '3–6' in ne['C064']['proof']
assert ne['C064']['note']==oe['C064']['note'] and all('https: //' not in str(e) for e in ne.values())
for key in ['camp_programmes','camp_planning','camp_focus','schools','school_focus','school_history','development_routes','leagues','family_context','top_picks']:
    assert d[key]==b[key],key
assert d['family_strategy'].keys()==b['family_strategy'].keys()|{'nearby_participation_v135'}
assert all(d['family_strategy'][k]==b['family_strategy'][k] for k in b['family_strategy'])
op={p['id']:p for p in b['league_guide']['profiles']};np={p['id']:p for p in d['league_guide']['profiles']}
assert len(op)==142 and len(np)==144 and set(np)-set(op)==set(GUIDES)
assert {k for k in op if op[k]!=np[k]}=={'tmr','robofest'}
assert np['robofest']['categories']==op['robofest']['categories']
assert np['robofest']['sources']==op['robofest']['sources']
assert np['robofest']['nuances'][:-1]==op['robofest']['nuances']
assert np['tmr']['sources'][:len(op['tmr']['sources'])]==op['tmr']['sources']
assert np['tmr']['nuances'][:-1]==op['tmr']['nuances']
assert np['tmr']['categories'][0]['source']==ne['C043']['source']
for id in RL_IDS+['E191','C1169','E200']:
    assert not ne[id]['start'] and not ne[id]['end'] and not ne[id]['deadline'],id
for id in NEW_IDS:
    assert not ne[id]['languages'] and ne[id]['language_mode']=='unconfirmed'
    assert re.match(r'^P[0-4]\b',ne[id]['priority']),id
assert ne['E191']['block']=='События' and ne['E191']['team_min']==2 and ne['E191']['team_max']==3
assert 'противоречие' in ne['E191']['note'] or 'расхождение' in ne['E191']['note']
assert ne['C1169']['team_min']==2 and ne['C1169']['team_max']==3 and '4–6' in ne['C1169']['age']
assert ne['C1165']['team_min']==1 and ne['C1165']['team_max']==5
assert '10%' in ne['C1165']['note'] and '1/2' in ne['C1165']['note'] or '1–2' in ne['C1165']['note']
assert '9–14' in ne['C1166']['age'] and '10–12' in ne['C1166']['age']
assert ne['C1167']['osc'].startswith('Нет') and '800' in ne['C1167']['gear']
assert ne['E199']['mat'].startswith('Нет') and ne['E199']['osc'].startswith('Нет')
assert all(ne[id]['date_scope']=='workshop_window' and ne[id]['parent_event_id']=='E001' for id in ['E'+str(i) for i in range(192,201)])
assert ne['E197']['cost'].startswith('0') and ne['E193']['cost'].startswith('70') and 'валюта' in ne['E193']['cost']

def text(file):return (P/(file+'.txt')).read_text()
def clause(file,*needles):
    n=lambda s:''.join(s.lower().replace('–','-').replace('’',"'").split())
    body=n(text(file))
    for q in needles:assert n(q) in body,(file,q)
clause('rl-general-pdf','20 Y 21 de MARZO','PACHUCA','(6 a menos','5-49','80%','100 USD','10 USD','No se darán reembolsos')
clause('rl-parade-pptx','6','14','1','5','7','16')
clause('rl-parade-rubric-pdf','Team Independence','10%','Math Test','3%','one member','1 or 2')
clause('rl-drones','10-12','13-18')
clause('rl-drones-pdf','9','14','15','20','75%')
clause('rl-football-pdf','8','14','800','W193','Julio','2 equipos')
clause('baja-general-pdf','17 de mayo de 2026','8 de mayo de 2026','No se considera una competencia con premiación','diploma de participación')
clause('baja-armado-manual','mínimo de 2, máximo 3','proporcionando por el museo','sólo como participación','se evaluará y premiará')
clause('baja-minisumo-manual','cuarto','sexto','mínimo 2 máximo 3','2 kg','USB','5 segundos','77 cm')
agenda=json.loads((P/'bebras-agenda-public-api.html').read_text())['data'];assert agenda['events'][0]['date']=='28/09/2026 al 16/10/2026'
assert 'tercero a sexto' in json.loads((P/'bebras-rules-public-api.html').read_text())['data']['sections'][1]['body_html']
maker={r['id']:r for r in json.loads((P/'maker-workshops-public-json.html').read_text())}
assert len(maker)==28 and maker['4']['fecha']=='' and maker['23']['precio']==70 and maker['31']['precio']==0
assert '5 años' in maker['23']['requisitos'] and '12 años' in maker['10']['requisitos']
assert maker['24']['fecha']=='Sábado 17 de octubre' and maker['28']['fecha']=='Domingo 18 de octubre'
receipts=json.loads((ROOT/'data/nearby-robotics-source-receipts-v135.json').read_text())
assert len(receipts['sources'])==30 and sum(r.get('status')==200 for r in receipts['sources'])==27
assert sum(r.get('pdf_pages',0) for r in receipts['sources'])==80 and not any(receipts['external_actions'].values())
for r in receipts['sources']:
    if r.get('raw_filename'):
        raw=(P/r['raw_filename']).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
assert not receipts['primary_reader_observations']['tmr_government']['full_raw_body_retained']
assert not receipts['primary_reader_observations']['bebras_rendered_pages']['conflict_resolved']

def blocks(raw):
    out={}
    for m in re.finditer(br'BEGIN:VEVENT\r\n.*?END:VEVENT\r\n',raw,re.S):
        uid=re.search(br'(?m)^UID:([^\r\n]+)',m.group()).group(1);assert uid not in out;out[uid]=m.group()
    return out
raw=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes()
assert not re.search(br'(?<!\r)\n',raw) and all(len(l)<=75 for l in raw.split(b'\r\n'))
for l in raw.split(b'\r\n'):l.decode('utf-8')
before=blocks(prior('dist/downloads/STEM_подтвержденные_даты.ics'));after=blocks(raw)
assert len(before)==3025 and len(after)==3033
updates={b'stem-C064@family-stem.local',b'stem-C064-deadline@family-stem.local'}
assert {k for k in before if before[k]!=after[k]}==updates
for k in updates:
    for field in [b'UID',b'DTSTART;VALUE=DATE',b'DTEND;VALUE=DATE']:
        expr=br'(?m)^'+re.escape(field)+br':[^\r\n]+';assert re.findall(expr,before[k])==re.findall(expr,after[k])
expected={('stem-'+k+'@family-stem.local').encode() for k in ['C043']+['E'+str(i) for i in range(192,199)]}
assert set(after)-set(before)==expected
assert (ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes()==prior('dist/downloads/STEM_крупные_выставки.ics')

def portable(meta,kind):
    m=json.loads((ROOT/'dist/downloads'/meta).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
    assert m['complete_database'] and len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256']
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        assert z.testzip() is None and z.namelist()==[m[kind+'_entry'],'README.txt'];body=z.read(m[kind+'_entry'])
    assert len(body)==m[kind+'_bytes'] and hashlib.sha256(body).hexdigest()==m[kind+'_sha256']
    assert m['raw_download_available']==(len(body)<=26214400);return body
assert json.loads(portable('STEM_database_json_download.json','json'))==d
sql=portable('STEM_database_download.json','sqlite');(P/'verified-v135.sqlite').write_bytes(sql)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as z:(P/'baseline-v134.sqlite').write_bytes(z.read('STEM_database.sqlite'))
c,oc=sqlite3.connect(P/'verified-v135.sqlite'),sqlite3.connect(P/'baseline-v134.sqlite')
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
tables=[r[0] for r in oc.execute("SELECT name FROM sqlite_master WHERE type='table'")];assert tables==[r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
for t in tables:
    x,y=oc.execute('SELECT * FROM '+t).fetchall(),c.execute('SELECT * FROM '+t).fetchall()
    if t=='metadata':
        xm,ym=dict(x),dict(y);assert {k for k in xm if xm[k]!=ym[k]}=={'league_guide','family_strategy','completeness_audit'}
    elif t=='events':
        ym={r[0]:r for r in y};assert all(r==ym[r[0]] for r in x if r[0] not in ['C043','C064'])
        assert c.execute('SELECT COUNT(*) FROM events').fetchone()[0]==3829
    elif t=='countries':
        assert [r for r in x if r[0]!='MEX']==[r for r in y if r[0]!='MEX']
        a,z=next(r for r in x if r[0]=='MEX'),next(r for r in y if r[0]=='MEX');assert a[:3]==z[:3]
        q=json.loads(a[3]);q['competitions']+=11;q['exhibitions']+=10;q['dated']+=9;assert q==json.loads(z[3])
    elif t in ['sources','event_countries','event_themes']:assert set(x)<=set(y),t
    else:assert x==y,t
c.close();oc.close()
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(prior('data/research-plan.json'))
for k in ['human_scope_expansion','next_research']:assert plan[k]==bp[k],k
assert plan['status']==plan['native_goal_status']=='active'
assert plan['latest_validation']['version']==135 and plan['latest_validation']['fully_audited_countries']==0
assert plan['current_publication']['status']=='prepared_local_not_published'
assert json.loads((P/'native-site-check.json').read_text())['structuredContent']['error_data']['code']==404
result=dict(version=135,status='passed',baseline_commit=BASE,unchanged_event_objects=3806,updated_event_ids=['C043','C064'],new_rows=21,
    unchanged_dossiers=1102,unchanged_budget_objects=57,unchanged_school_history_routes=True,unchanged_guide_profiles=140,new_guide_ids=GUIDES,
    source_receipts=30,retained_body_hashes_verified=28,pdf_pages_retained=80,old_ics_blocks_byte_identical=3023,old_bebras_dates_and_uids_preserved=2,new_ics_entries=8,
    complete_json_verified=True,complete_sqlite_verified=True,sqlite_integrity='ok',exhibition_ics_byte_identical=True,unannounced_seasons_undated=True,
    no_duplicate_category_id=True,no_external_actions=True,worldwide_complete=False,fully_audited_countries=0)
(P/'independent-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
