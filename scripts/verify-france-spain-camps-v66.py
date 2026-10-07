"""Verify programme-specific eligibility, calendar exclusions and preserved history."""
import datetime,json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
BASE='656e5cfca8c44d485819118f9d5e4db5ba5073c0'
def oldfile(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(oldfile('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};rows={e['id']:e for e in d['events']}
assert len(rows)==len(d['events'])==2218
corrected={e['id'] for e in b['events'] if e.get('camp_dossier_slug')=='la-garenne'}
assert len(corrected)==3
allow={'action','cost','format','gear','language','language_certainty','language_mode','languages','note','participation','period','proof','references','source','title'}
for k,v in old.items():
 if k in corrected:
  changed={key for key in set(v)|set(rows[k]) if v.get(key)!=rows[k].get(key)}
  assert changed==allow,(k,changed)
  assert rows[k]['start']==v['start'] and rows[k]['end']==v['end'] and rows[k]['participation']=='residential'
 else:assert rows[k]==v,k
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[k]==b[k],k
p={x['slug']:x for x in d['camp_programmes']['profiles']};oldp={x['slug']:x for x in b['camp_programmes']['profiles']}
assert len(p)==179 and len(set(p)-set(oldp))==17
for k,v in oldp.items():
 if k not in ['la-garenne','garenne-robotics-workshop']:assert p[k]==v,k
 else:assert p[k]['id']==v['id'] and p[k]['formats']==v['formats'] and p[k]['family_fit']==v['family_fit']
c=d['camp_programmes']['counts']
assert c==dict(dossiers=179,countries=28,swiss=35,by_status={'published_2026_27':15,'published_2027':54,'partial_2027':21,'published_2026':31,'next_unannounced':51,'partial_2026_27':7},source_urls=334)
assert sum(e['block']=='Лагеря' for e in rows.values())==887
assert len(d['camp_programmes']['generated_event_ids'])==424
assert d['camp_programmes']['integration']['reused_legacy_events']==58 and d['camp_programmes']['integration']['seasonal_windows']==12
assert len(d['camp_programmes']['shortlist'])==28
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==d['camp_programmes']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==json.loads((ROOT/'data/research-plan.json').read_text())
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[e for k,e in rows.items() if k not in old];assert len(new)==52
for slug in set(p)-set(oldp):
 q=p[slug];assert q['checked']=='2026-10-05' and q['iso'] in ['FRA','ESP']
 assert all(s['checked']=='2026-10-05' and s['url'].startswith('https://') for s in q['sources'])
 assert set(q['themes'])<={'general','art','robotics','coding','science','languages','sport'}
assert all(e['checked']=='2026-10-05' and e['block']=='Лагеря' for e in new)
closed=[e for e in new if e.get('availability',{}).get('status')=='closed'];assert len(closed)==3
assert {e['camp_dossier_slug'] for e in closed}=={'kidsrobots-kids','kidsrobots-mini','activebrain-little-holiday'}
assert all(e['start']=='2026-10-26' and e['end']=='2026-10-30' for e in closed)
assert len(p['kidsrobots-mini']['timing']['sessions'])==9
assert {x['event_ids'][0] for x in p['kidsrobots-mini']['calendar_links'] if x['kind']=='existing_programme'}=={'L%03d'%i for i in range(339,347)}
assert not any(e['camp_dossier_slug']=='kidsrobots-mini' and e['start']!='2026-10-26' for e in new)
for slug in ['kidsrobots-kids','kidsrobots-mini','madrid-chess-robotics','logiscool-spain-wedo']:
 assert not p[slug]['confirmed_instruction_languages']
for slug in ['activebrain-holiday','activebrain-little-holiday','activebrain-monthly']:
 assert p[slug]['confirmed_instruction_languages']==['EN'] and p[slug]['timing']['status']=='published_2026'
assert p['activebrain-little-holiday']['availability']['status']=='closed'
assert len(p['activebrain-monthly']['timing']['sessions'])==3
assert all(e['date_scope']=='workshop_window' and '10:00–12:00' in e['title'] for e in new if e['camp_dossier_slug']=='activebrain-monthly')
for slug in ['ibs-mini','ibs-kids','ibs-general','natuk-robotics','costablanca-robotics','ausias-summer','logiscool-spain-wedo']:
 assert not p[slug]['timing']['sessions']
assert p['ibs-mini']['price']['year'] is None and p['ibs-kids']['price']['year']==p['ibs-general']['price']['year']==2026
assert p['ibs-mini']['formats']==p['ibs-kids']['formats']==['day']
assert p['ibs-kids']['family_fit']['matvey']['status']=='not_eligible' and p['ibs-general']['family_fit']['oscar']['status']=='later'
assert p['natuk-robotics']['confirmed_instruction_languages']==['EN'] and p['natuk-robotics']['price']['year'] is None
assert p['costablanca-robotics']['family_fit']['matvey']['status']==p['costablanca-robotics']['family_fit']['oscar']['status']=='unknown'
assert p['costablanca-robotics']['language_evidence_role']=='language_lessons'
assert p['ausias-summer']['price']['year']==2026 and '377' in p['ausias-summer']['price']['extras']
for slug in ['lacunza-general','madrid-chess-robotics']:
 assert p[slug]['timing']['precision']=='season_window' and not any(x['event_ids'] for x in p[slug]['calendar_links'])
assert p['lacunza-general']['price']['year']==2026
future=[e for e in new if e['camp_dossier_slug']=='cmef-junior'];assert len(future)==18
assert all(e['priority'].startswith('P4') and e['date_precision']=='published_rule' and e['date_rule'] for e in future)
assert not p['cmef-junior']['confirmed_instruction_languages']
for slug in ['cervantes-beach-board','cervantes-beach-day']:
 q=p[slug];assert q['price']['year']==2027 and q['booking_channel']=='Cervantes EI' and q['operator_identity_status']=='unconfirmed'
 assert q['possible_same_operator_as']=='enforex-barcelona' and not q['related_event_ids']
 assert len(q['timing']['sessions'])==6 and q['language_evidence_role']=='language_lessons'
 for e in new:
  if e['camp_dossier_slug']!=slug:continue
  assert e['date_precision']=='published_rule' and e['date_rule']
  if slug.endswith('day'):assert datetime.date.fromisoformat(e['start']).weekday()==0 and datetime.date.fromisoformat(e['end']).weekday()==4
g=p['la-garenne'];assert len(g['timing']['sessions'])==10
assert g['language_evidence_role']=='language_lessons' and g['confirmed_instruction_languages']==['EN','FR']
ge=[e for e in rows.values() if e.get('camp_dossier_slug')=='la-garenne'];assert len(ge)==10
assert sum(e['participation']=='day_camp' for e in ge)==5
assert all(not e.get('attendance_weekdays') and e['date_scope']=='camp_session' for e in ge)
assert 'Пн–Сб' in g['accommodation'] and '10%' in g['price']['deposit'] and '65' in g['price']['deposit']
r=p['garenne-robotics-workshop'];assert r['price']['year']==2027 and '500' in r['price']['label']
assert not r['timing']['sessions'] and not r['confirmed_instruction_languages']
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2218
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==179;con.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
  assert f['UID'] not in out
  out[f['UID']]=(f.get('DTSTART;VALUE=DATE',f.get('DTSTART')),f.get('DTEND;VALUE=DATE',f.get('DTEND')))
 return out
fn='dist/downloads/STEM_подтвержденные_даты.ics';before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1519 and len(now)==1550 and all(now.get(k)==v for k,v in before.items()) and len(set(now)-set(before))==31
for e in new:assert ('stem-'+e['id']+'@family-stem.local' in now)==(e not in closed and e not in future)
assert not any('CP179-' in uid or 'CP174-' in uid or 'CP162-' in uid for uid in now)
fn='dist/downloads/STEM_крупные_выставки.ics';assert calendar((ROOT/fn).read_bytes())==calendar(oldfile(fn)) and len(calendar(oldfile(fn)))==104
assert d['coverage_summary']['fully_audited_countries']==0
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']=='active' and plan['previous_goal_turn_classification']['classification']=='progress'
assert 'Version65' in plan['previous_goal_turn_classification']['evidence']
print(json.dumps(dict(prior_events_unchanged=2163,corrected_events=3,prior_dossiers_unchanged=160,corrected_dossiers=2,new_dossiers=17,new_catalogue_dates=52,new_family_ical=31,dossiers=179,countries=28,swiss=35,french=23,spanish=19,official_urls=334,family_ical=1550,exhibition_ical=104,closed_new_rows=3,future_age_rows=18,mini_dates_reused=8,season_windows=12,sqlite='ok',bridge='idempotent'),ensure_ascii=False))
