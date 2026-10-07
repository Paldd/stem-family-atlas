"""Independent preservation, primary-clause, age, time and portable-data checks."""
import collections,csv,datetime,hashlib,io,json,re,sqlite3,subprocess,zipfile
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
P=ROOT.parent/'stem-family-atlas-work/nearby-primary-v118'
BASE='861a8690dfe23a3c029a5e90e17bce23bf91b595'
ALLOW={'C001','C020','C078','C082','C180','C608','C609','C614','C615','C662','C805','C806','C1124','C1125','C1126'}
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def prior(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def clause(key,*needles,compact=False):
    t=(P/(key+'.txt')).read_text();norm=(lambda s:re.sub(r'\s+','',s)) if compact else (lambda s:' '.join(s.split()))
    for needle in needles:assert norm(needle) in norm(t),(key,needle)
d=json.loads((ROOT/'data/catalog.json').read_text());b=json.loads(prior('data/catalog.json'))
mutable={'events','source_count','sources','family_strategy','completeness_audit'}
assert set(d)==set(b) and {k:v for k,v in d.items() if k not in mutable}=={k:v for k,v in b.items() if k not in mutable}
old={e['id']:e for e in b['events']};new={e['id']:e for e in d['events']}
assert len(new)==3555 and old.keys()==new.keys() and {k for k in old if old[k]!=new[k]}==ALLOW
assert collections.Counter(e['block'] for e in new.values())=={'Соревнования':1153,'События':189,'Лагеря':2213}
assert d['camp_programmes']==b['camp_programmes'] and len(d['camp_programmes']['profiles'])==890
assert d['camp_planning']==b['camp_planning'] and len(d['camp_planning']['offers'])==27
fs=d['family_strategy'];assert {k:v for k,v in fs.items() if k!='nearby_participation_v118'}==b['family_strategy']
route=fs['nearby_participation_v118'];assert route['version']==118 and len(route['items'])==14
assert len(route['prices'])==7 and len(route['budget_scenarios'])==3
assert set(route['closed_ids'])=={'C1124','C1125','C1126'}
assert all(new[k]['priority'].startswith('P2') for k in route['closed_ids'])
assert new['C662']['priority'].startswith('P4') and new['C180']['deadline']=='2026-10-23'
instant=datetime.datetime.fromisoformat(new['C180']['deadline_utc'].replace('Z','+00:00'))
assert instant.astimezone(ZoneInfo('America/Costa_Rica')).isoformat()=='2026-10-23T22:00:00-06:00'
assert instant.astimezone(ZoneInfo('America/New_York')).isoformat()=='2026-10-24T00:00:00-04:00'
def age(dob,day):return day.year-dob.year-((day.month,day.day)<(dob.month,dob.day))
day=datetime.date(2026,1,1);start=datetime.date(2020,1,1)
dob=[start+datetime.timedelta(days=n) for n in range(366)]
assert all(4<=age(q,day)<=6 for q in dob)
assert [q for q in dob if 6<=age(q,day)<=9]==[start]
assert all(6<=age(datetime.date(2017,1,1)+datetime.timedelta(days=n),day)<=9 for n in range(365))
assert age(datetime.date(2020,1,1),datetime.date(2027,12,31))==7
ri={q['id']:q for q in route['items']}
assert ri['C608']['children']==['oscar'] and ri['C609']['children']==['matvey'] and ri['C082']['children']==['matvey']
assert ri['C615']['children']==['matvey','oscar'] and ri['C662']['mode']=='visitor'
clause('tecpro-rules','mínimo dos','máximo cuatro','mentor adulto responsable','representante autorizado','Hasta un día antes del evento',compact=True)
clause('tecpro','28/09/2026','28/09/2026 al 04/10/2026','08 de Oct. / 2026')
clause('mtiny-rules','4 y 6 años','al 1 de enero del año en curso','6 minutos',compact=True)
clause('codey-rules','6 y 9 años','al 1 de enero del año en curso',compact=True)
clause('inspire-rules-linked','January 2nd, 2013','December 31, 2020','the number of contestants is 1',compact=True)
clause('starter-rules-linked','January 2, 2012','December 31, 2020','1-2 for each team',compact=True)
clause('lati','5 días antes del evento','PRIMERA FECHA EL VIERNES 9 DE OCTUBRE','Primaria y Secundaria')
raw=(P/'luva-bundle.html').read_text();assert all(t in raw for t in ['Inscripciones Cerradas','10 Octubre','Sumo LEGO','Secundaria'])
clause('roborave-amaze','8–15 years','2-4 students')
clause('fll-mx','equipos independientes','medalla a cada participante','eventos demostrativos')
keys={'mtiny-registration':'mtiny-price','codey-registration':'codey-price','mtiny-robot':'mtiny-robot','mtiny-arena':'mtiny-arena','mtiny-bundle':'mtiny-kit','codey-robot':'codey-robot','codey-arena':'codey-arena'}
prices={q['id']:q for q in route['prices']}
for key,source in keys.items():
    raw=(P/(source+'.html')).read_text()
    assert re.search(r'<meta itemprop="priceCurrency" content="MXN"',raw)
    amount=re.search(r'<meta itemprop="price" content="([^"]+)"',raw).group(1)
    assert float(amount.replace(',',''))==prices[key]['amount'] and prices[key]['invoice_confirmed'] is False
for q in route['budget_scenarios']:
    assert round(sum(prices[k]['amount'] for k in q['items']),2)==q['amount'] and not q['complete']
assert 'mtiny-registration' not in route['budget_scenarios'][1]['items']
clause('mtiny-arena','1 inscripción al torneo MakeX México')
clause('mtiny-kit','2 inscripciones','XI Edición')
clause('codey-arena','No incluye inscripción a la competencia ni robot')
receipt=json.loads((ROOT/'data/nearby-participation-source-receipts-v118.json').read_text())
assert len(receipt['sources'])==30 and sum(q.get('status')==200 for q in receipt['sources'])==25
assert not any(receipt['external_actions'].values()) and receipt['new_visual_pdf_checks']==8
for q in receipt['sources']:
    if q['body_snapshot_retained']:
        raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
image_files=['tecpro-teams-05.png','tecpro-category-08.png','tecpro-delivery-09.png','mtiny-age-02.png','codey-age-02.png','inspire-age-07.png','starter-age-06.png','lati-deadline-2.png']
assert all((P/n).stat().st_size>0 for n in image_files)
assert receipt['web_reader'][0]['direct_http_status']==403 and receipt['web_reader'][0]['observed_open_spots']==24
oldsrc={q['url']:q for q in b['sources']};newsrc={q['url']:q for q in d['sources']}
assert all(newsrc[u]==q for u,q in oldsrc.items()) and len(newsrc)-len(oldsrc)==8
def portable(name,ext):
    m=json.loads((ROOT/'dist/downloads'/name).read_text());raw=(ROOT/'dist/downloads'/m['download']).read_bytes()
    assert len(raw)==m['archive_bytes'] and hashlib.sha256(raw).hexdigest()==m['archive_sha256'] and m['complete_database']
    with zipfile.ZipFile(io.BytesIO(raw)) as q:
        assert q.testzip() is None and q.namelist()==[m[ext+'_entry'],'README.txt'];body=q.read(m[ext+'_entry'])
        assert m[ext+'_sha256'] in q.read('README.txt').decode()
    assert len(body)==m[ext+'_bytes'] and hashlib.sha256(body).hexdigest()==m[ext+'_sha256']
    assert (ROOT/'dist/downloads'/m[ext+'_entry']).exists()==m['raw_download_available']==(len(body)<=26214400)
    return body,m
sql,sm=portable('STEM_database_download.json','sqlite');js,jm=portable('STEM_database_json_download.json','json')
assert json.loads(js)==d
f=P/'verified-v118.sqlite';f.write_bytes(sql);c=sqlite3.connect(f)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as q:raw=q.read('STEM_database.sqlite')
f=P/'baseline-v117.sqlite';f.write_bytes(raw);o=sqlite3.connect(f)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
schema=lambda q:sorted(q.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"));assert schema(c)==schema(o)
allowed={'events':ALLOW,'metadata':{'family_strategy'}}
for name, in o.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
    aa=set(o.execute('SELECT * FROM "'+name+'"'));zz=set(c.execute('SELECT * FROM "'+name+'"'))
    assert {r[0] for r in aa-zz}==allowed.get(name,set()),(name,{r[0] for r in aa-zz})
    assert {r[0] for r in aa}<={r[0] for r in zz},name
assert new=={k:json.loads(v) for k,v in c.execute('SELECT id,record_json FROM events')}
assert {p['slug']:p for p in d['camp_programmes']['profiles']}=={k:json.loads(v) for k,v in c.execute('SELECT slug,record_json FROM camp_programmes')}
assert json.loads(c.execute("SELECT value FROM metadata WHERE key='family_strategy'").fetchone()[0])==fs
c.close();o.close()
def calendar(raw):
    t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
    for s in t.split('BEGIN:VEVENT')[1:]:
        f={v.split(':',1)[0]:v.split(':',1)[1] for v in s.split('END:VEVENT')[0].splitlines() if ':' in v};f.pop('DTSTAMP',None)
        assert f['UID'] not in out;out[f['UID']]=f
    return out
p='dist/downloads/STEM_подтвержденные_даты.ics';oa=calendar(prior(p));na=calendar((ROOT/p).read_bytes())
assert oa.keys()==na.keys() and len(na)==2770
changes={u for u in oa if oa[u]!=na[u]};assert len(changes)==16
assert all(re.search(r'stem-(C\d+)',u).group(1) in ALLOW for u in changes)
assert na['stem-C180-deadline@family-stem.local']['DTSTART']=='20261024T040000Z'
assert 'stem-C662@family-stem.local' not in na
p='dist/downloads/STEM_крупные_выставки.ics';assert calendar(prior(p))==calendar((ROOT/p).read_bytes()) and len(calendar(prior(p)))==104
for name in ['STEM_catalog.csv','STEM_календарь_2026_2027.csv','STEM_крупные_выставки.csv']:
    f=ROOT/'dist/downloads'/name
    if f.exists():
        aa=list(csv.DictReader(io.StringIO(prior('dist/downloads/'+name).decode('utf-8-sig'))));zz=list(csv.DictReader(io.StringIO(f.read_text(encoding='utf-8-sig'))))
        assert len(aa)==len(zz)
        assert all(x==y or any(y.get(k) in ALLOW for k in ['id','ID']) for x,y in zip(aa,zz)),name
plan=json.loads((ROOT/'data/research-plan.json').read_text());oldplan=json.loads(prior('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==118
assert {q['id'] for q in plan['requirements']}=={q['id'] for q in oldplan['requirements']}
for k in ['objective','completion_rule','camp_priority_countries_current_request','family_context','schools_success_criteria']:assert plan[k]==oldplan[k],k
assert plan['complete_database_download']==sm and plan['complete_json_download']==jm
assert d['coverage_summary']['fully_audited_countries']==0 and not plan['latest_validation']['worldwide_complete']
for stem in ['research-plan','nearby-participation-audit-v118','nearby-participation-source-receipts-v118']:
    assert json.loads((ROOT/'data'/f'{stem}.json').read_text())==json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())
web=json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').removesuffix(';\n'))
for k in ['events','camp_programmes','camp_planning','league_guide','family_strategy']:assert web[k]==d[k]
assert 'data-ui-version="118"' in (ROOT/'dist/index.html').read_text()
for f in ROOT.joinpath('dist').rglob('*'):
    if f.is_file():assert f.stat().st_size<=26214400,(f,f.stat().st_size)
for name in ['data.js','nearby-participation.js','experience.js']:subprocess.run([NODE,'--check',str(ROOT/'dist/assets'/name)],check=True)
for name in ['camp-planning.js','camp-programmes.js','camp-programmes.css']:assert (ROOT/'dist/assets'/name).read_bytes()==prior('dist/assets/'+name)
subprocess.run(['git','diff','--check','--','.',':!dist/downloads/*.ics',':!dist/downloads/*.csv'],cwd=ROOT,check=True)
result=dict(status='passed',version=118,unchanged_event_objects=3540,updated_competitions=15,unchanged_camp_dossiers=890,unchanged_camp_budget_offers=27,
    complete_sqlite=True,complete_json=True,age_control_dates_verified=True,deadline_timezones_verified=True,price_and_arena_double_count_checked=True,
    family_ics=2770,exhibition_ics=104,worldwide_scope_preserved=True,goal='active')
(P/'independent-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
