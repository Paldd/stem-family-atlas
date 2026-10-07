"""Independent preservation, selected source clauses and complete portable data."""
import hashlib,io,json,re,sqlite3,subprocess,zipfile
from collections import Counter
from lxml import html
from camp_europe_v133 import ROOT,BASE,NEW,EVENT_ID,COOLEST

P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v133'
def prior(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(prior('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={p['slug']:p for p in b['camp_programmes']['profiles']};new={p['slug']:p for p in d['camp_programmes']['profiles']}
assert len(old)==1084 and len(new)==1098 and set(new)-set(old)==set(NEW)
assert all(old[s]==new[s] for s in old)
oe={e['id']:e for e in b['events']};ne={e['id']:e for e in d['events']}
assert len(oe)==3793 and len(ne)==3806 and all(oe[s]==ne[s] for s in oe)
added={s:ne[s] for s in set(ne)-set(oe)};camp={s:e for s,e in added.items() if e['block']=='Лагеря'}
assert len(camp)==12 and set(added)-set(camp)=={EVENT_ID}
assert Counter(e['block'] for e in d['events'])==dict(Соревнования=1157,События=197,Лагеря=2452)
assert d['camp_planning']['offers'][:-1]==b['camp_planning']['offers'] and len(d['camp_planning']['offers'])==56
q=d['camp_planning']['offers'][-1];assert q['id']=='kidsus-rueil-english-both' and q['currency']=='EUR' and q['price_year']==2026
assert sum(q['base_by_child'].values())==570 and q['unknown_required'] and not q['required'] and not q['optional']
for field in ['school_focus','school_history','schools','development_routes','leagues','family_strategy']:assert d[field]==b[field],field
gp={p['id']:p for p in d['league_guide']['profiles']};op={p['id']:p for p in b['league_guide']['profiles']}
assert len(gp)==len(op)==142 and all(gp[k]==op[k] for k in op if k!='coolest')
assert {k for k in op['coolest'] if op['coolest'][k]!=gp['coolest'][k]}=={'event_ids','categories','nuances','sources'}
for field in ['event_ids','categories','nuances','sources']:assert gp['coolest'][field][:-1]==op['coolest'][field]
e=ne[EVENT_ID];assert e['block']=='События' and e['participation']=='visitor' and not e.get('exhibition_tier') and not e['deadline']
assert e['exhibitor_deadline']=='2026-10-08' and e['start']==e['end']=='2026-10-24' and e['languages']==[] and e['source']==COOLEST
for slug in NEW[:6]:assert new[slug]['confirmed_instruction_languages']==['EN']
assert new['kidsus-rueil-english-art']['language_evidence_role']=='language_lessons' and 'не установлен' in new['kidsus-rueil-english-art']['language']
p=new['kidsus-paris11-autumn'];assert p['timing']['variant_keyed'] and len(p['calendar_links'])==3
v=next(v for v in p['timing']['session_details'] if v['variant_key']=='full-one');assert v['age']=='5–8' and 'до девятого' in v['family_fit']['matvey']['detail']
assert ne['CP1087-20261019-20261023-full-one']['age']=='5–8'
assert len(new['kidsus-angers-autumn']['calendar_links'])==3 and new['kidsus-angers-autumn']['timing']['variant_keyed']
for slug in NEW[6:9]+NEW[10:]:
    p=new[slug];assert not p['timing']['sessions'] and not p['calendar_links']
for slug in NEW[6:9]:assert new[slug]['confirmed_instruction_languages']==[]
assert 'не напечатанный возраст' in new['codelearn-sixseven']['programme']
assert 'не является курсом Python' in new['codelearn-godot']['programme']
assert new['sanpatricio-mega-day']['confirmed_instruction_languages']==['EN'] and 'Tuesday11–12' in new['sanpatricio-mega-day']['programme']
for slug in NEW[12:]:assert new[slug]['confirmed_instruction_languages']==['EN','ES'] and new[slug]['age']=='Main 10–16'
norm=new['silc-normandy-english'];assert norm['availability']['status']=='unconfirmed' and norm['price']['year']==2027
assert norm['timing']['sessions']==[['2027-07-18','2027-07-23']] and norm['family_fit']['oscar']['status']=='later'
assert ne['CP1094-20270718-20270723']['availability']['label']=='Онлайн-покупка недоступна · причину уточнить'
r=d['camp_programmes']['family_review'];assert r['coverage']==dict(candidates=62,countries=16,fully_audited_countries=0)
assert r['entries'][:-4]==b['camp_programmes']['family_review']['entries']
def clause(file,*words):
    def norm(s):return ''.join(s.lower().replace('–','-').replace('’',"'").split())
    t=norm((P/(file+'.txt')).read_text())
    for word in words:assert norm(word) in t,(file,word)
clause('kids-es-barcelona-autumn','26 al 30','2026','3','10')
clause('kids-fr-paris5','30 septembre 2026','19 au 23 octobre','26 au 30 octobre','100% en anglais','7-10 ans')
clause('kids-fr-paris11','5–8 ans','3–10 ans','9h–16h30','Swamp Life','26 au 30 octobre')
clause('kids-fr-angers','19 au 23 octobre','26 au 30 octobre','5 à 10 ans','pique-nique','14h à 16h30')
clause('kids-fr-rueil','285€/ semaine par enfant','495€/ semaine par enfant','30€','9h à 13h (en anglais)','atelier de l\'art')
clause('codelearn-sixseven','bromas internas','nombre informal','montando robots')
clause('codelearn-roboball','22, 23 y 24 de Diciembre','joystick','febrero')
clause('codelearn-godot','GDScript','Godot')
clause('silc-normandie','Du 18 au 23 juillet 2027','1150','hors frais de dossier','10/15 ans')
clause('silc-one','55','A1/A2','autonomie')
clause('silc-adolescent-terms-selected','2026','incluent les frais de dossier de 100','10%','30%','50%','75%','100%')
var=[v for attr in html.fromstring((P/'silc-normandie.html').read_bytes()).xpath('//*[@data-product_variations]/@data-product_variations') for v in json.loads(attr)]
assert len(var)==1 and var[0]['display_price']==1150 and var[0]['is_in_stock'] is False and '2027' in str(var[0]['attributes'])
clause('coolest-spain-organizer','24 OCT 2026','12 a 18','11:30—13:30','8 de octubre de 2026','asistir al evento es gratuito','Raspberry Pi Pico')
clause('sanpatricio-mega-2026-pdf','6-9 yrs','8:45','STEAM','robotics','Engineering','16:00')
clause('sanpatricio-robotics-2026-pdf','Robotics & Computing','Spanish/English','Lego robotics')
clause('sanpatricio-archive-pdf','CAMPS 2024')
receipts=json.loads((ROOT/'data/europe-camps-source-receipts-v133.json').read_text())
assert len(receipts['sources'])==25 and len(receipts['native_browser_sources'])==1 and not any(receipts['external_actions'].values())
for q in receipts['sources']:
    raw=(P/q['raw_filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
assert next(q for q in receipts['sources'] if q['key']=='sanpatricio-bundle')['content_status'].startswith('javascript_source_bundle')
def blocks(raw):return {re.search(br'(?m)^UID:([^\r\n]+)',v).group(1):v for v in re.findall(br'BEGIN:VEVENT\r?\n.*?END:VEVENT\r?\n',raw,re.S)}
before=blocks(prior('dist/downloads/STEM_подтвержденные_даты.ics'));after=blocks((ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes())
assert len(before)==3009 and len(after)==3022 and all(before[k]==after[k] for k in before)
assert set(after)-set(before)=={('stem-'+ident+'@family-stem.local').encode() for ident in added}
assert not any(b'E190-deadline' in k for k in after)
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
sql=portable('STEM_database_download.json','sqlite');(P/'verified-v133.sqlite').write_bytes(sql)
with zipfile.ZipFile(io.BytesIO(prior('dist/downloads/STEM_database.zip'))) as z:(P/'baseline-v132.sqlite').write_bytes(z.read('STEM_database.sqlite'))
c=sqlite3.connect(P/'verified-v133.sqlite');oc=sqlite3.connect(P/'baseline-v132.sqlite')
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
tables=[x[0] for x in oc.execute("SELECT name FROM sqlite_master WHERE type='table'")];assert tables==[x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
for t in tables:
    a=oc.execute('SELECT * FROM '+t).fetchall();z=c.execute('SELECT * FROM '+t).fetchall()
    if t=='metadata':
        am=dict(a);zm=dict(z);changed={k for k in am if am[k]!=zm[k]};assert changed=={'camp_family_review','league_guide','camp_focus','completeness_audit','camp_planning'},changed
    elif t in ['sources','events','event_countries','event_themes','camp_programme_sources','camp_programme_events','camp_programmes']:assert set(a)<=set(z),t
    elif t=='countries':
        assert [v for v in a if v[0] not in ['FRA','ESP']]==[v for v in z if v[0] not in ['FRA','ESP']]
        for iso,camps,expo in [('FRA',11,0),('ESP',1,1)]:
            x=next(v for v in a if v[0]==iso);y=next(v for v in z if v[0]==iso);assert x[:3]==y[:3]
            record=json.loads(x[3]);record['camps']+=camps;record['exhibitions']+=expo;record['dated']+=camps+expo;assert record==json.loads(y[3]),iso
    else:assert a==z,t
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(prior('data/research-plan.json'))
for field in ['human_scope_expansion','next_research']:assert plan[field]==bp[field],field
assert plan['status']==plan['native_goal_status']=='active' and plan['current_publication']['status']=='prepared_local_not_published'
assert plan['latest_validation']['version']==133 and plan['latest_validation']['fully_audited_countries']==0
assert (P/'native-site-check.json').exists() and json.loads((P/'native-site-check.json').read_text())['structuredContent']['error_data']['code']==404
result=dict(version=133,status='passed',baseline_commit=BASE,unchanged_event_objects=3793,unchanged_dossiers=1084,unchanged_budget_objects=55,unchanged_guide_profiles=141,
    new_dossiers=14,new_calendar_rows=13,new_budget_scenarios=1,family_review_candidates=62,old_ics_blocks_byte_identical=3009,new_ics_entries=13,exhibitor_deadline_not_family_visitor_deadline=True,
    exhibition_ics_byte_identical=True,all_old_sqlite_entity_rows_preserved=True,complete_sqlite_bytes=len(sql),complete_json_matches_catalog=True,source_bodies_hash_verified=25,
    meme_not_age_rule=True,full_day_cutoff_preserved=True,english_art_language_not_inferred=True,online_unavailable_reason_unknown=True,toledo_pdf_filename_2026_not_2027_session=True,
    general_steam_not_main_robotics_intensive=True,unknown_language_and_admission_preserved=True,no_school_or_world_prizes_inferred=True,unchanged_worldwide_goal_scope=True,goal='active',worldwide_complete=False,publication='prepared_local_not_published')
(P/'independent-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result))
