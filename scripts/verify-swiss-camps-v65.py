"""Verify winter availability, calculated weekdays and narrowly corrected history."""
import json,sqlite3,subprocess,datetime
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
BASE='5822e8c2c183947f8695071409173f2c2218fc1d'
def oldfile(name): return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(oldfile('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};rows={e['id']:e for e in d['events']}
assert len(rows)==len(d['events'])==2166
corrected={e['id'] for e in b['events'] if e.get('camp_dossier_slug')=='la-garenne'}
assert len(corrected)==3
for k,v in old.items():
 if k in corrected:
  changed={key for key in set(v)|set(rows[k]) if v.get(key)!=rows[k].get(key)}
  assert changed=={'gear','action','references','checked'},(k,changed)
 else: assert rows[k]==v,k
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[k]==b[k],k
p={x['slug']:x for x in d['camp_programmes']['profiles']};oldp={x['slug']:x for x in b['camp_programmes']['profiles']}
assert len(p)==162 and len(set(p)-set(oldp))==10
for k,v in oldp.items():
 if k=='la-garenne':
  assert {key for key in v if v[key]!=p[k].get(key)}=={'programme','questions','sources','checked'}
 else: assert p[k]==v,k
counts=d['camp_programmes']['counts'];assert counts==dict(dossiers=162,countries=28,swiss=35,by_status={'published_2026_27':13,'published_2027':51,'partial_2027':19,'published_2026':28,'next_unannounced':44,'partial_2026_27':7},source_urls=305)
assert len(d['camp_programmes']['generated_event_ids'])==372
assert d['camp_programmes']['integration']['reused_legacy_events']==50 and d['camp_programmes']['integration']['seasonal_windows']==10
assert sum(e['block']=='Лагеря' for e in rows.values())==835 and len(d['camp_programmes']['shortlist'])==25
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==d['camp_programmes']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==json.loads((ROOT/'data/research-plan.json').read_text())
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[e for k,e in rows.items() if k not in old];assert len(new)==55
for slug in set(p)-set(oldp):
 q=p[slug];assert q['checked']=='2026-10-05' and q['iso']=='CHE' and not q['related_event_ids']
 assert all(s['checked']=='2026-10-05' and s['url'].startswith('https://') for s in q['sources'])
 assert set(q['themes'])<={'general','art','robotics','coding','science','languages','sport'}
 assert q['timing']['status'] in ['published_2027','published_2026_27','partial_2027']
assert all(e['checked']=='2026-10-05' and e['block']=='Лагеря' for e in new)
nano=p['cdl-nano'];assert len(nano['timing']['sessions'])==5 and nano['language_evidence_role']=='bilingual'
assert nano['family_fit']['matvey']['status']=='not_eligible' and nano['family_fit']['oscar']['status']=='candidate'
assert all(e['language_mode']=='bilingual' for e in new if e['camp_dossier_slug']=='cdl-nano')
assert '965' in nano['price']['extras'] and 'CDL Family' in nano['price']['label']
assert len(p['lovell-summer']['timing']['sessions'])==2 and p['lovell-summer']['confirmed_instruction_languages']==['EN']
assert p['lovell-summer']['language_evidence_role']=='camp_life' and '7 000' in p['lovell-summer']['price']['extras']
closed=[e for e in new if e.get('availability',{}).get('status')=='closed']
assert len(closed)==3 and [e['start'] for e in closed]==['2027-01-10','2027-01-17','2027-01-24']
assert all(e['camp_dossier_slug']=='lovell-winter-board' for e in closed)
day=[e for e in new if e['camp_dossier_slug']=='lovell-winter-day'];assert len(day)==14
for e in day:
 assert datetime.date.fromisoformat(e['start']).weekday()==0 and datetime.date.fromisoformat(e['end']).weekday()==4
 assert e['date_scope']=='day_camp_window' and e['attendance_weekdays']==['MO','TU','WE','TH','FR']
 assert e['date_precision']=='published_rule' and e['date_rule'] and e['language_mode']=='language_lessons'
assert day[0]['start']=='2026-12-14' and day[-1]['end']=='2027-03-19'
assert all(e['language_mode']=='language_lessons' for e in new if e['camp_dossier_slug'] in ['lovell-winter-board','garenne-english-ski'])
assert p['camp-suisse-day']['timing']['precision']=='season_window' and not any(x['event_ids'] for x in p['camp-suisse-day']['calendar_links'])
assert p['camp-suisse-day']['formats']==['day'] and p['camp-suisse-day']['family_fit']['oscar']['status']=='candidate'
assert len(p['camp-suisse-board']['timing']['sessions'])==4 and p['camp-suisse-board']['family_fit']['oscar']['status']=='conditional'
ski=p['garenne-super-ski'];assert len(ski['timing']['sessions'])==6 and not ski['confirmed_instruction_languages']
assert not any(s[0] in ['2026-01-31','2027-01-31','2026-02-28','2027-02-28'] for s in ski['timing']['sessions'])
assert ski['family_fit']['matvey']['status']=='conditional' and ski['family_fit']['oscar']['status']=='later'
for slug in ['garenne-english-ski','garenne-integration']:
 assert len(p[slug]['timing']['sessions'])==5 and p[slug]['timing']['session_details'][-1]['end']=='2027-03-19'
 assert 'без ski' in p[slug]['timing']['session_details'][-1]['label']
r=p['garenne-robotics-workshop'];assert not r['timing']['sessions'] and not r['confirmed_instruction_languages'] and r['price']['year'] is None
assert '8–12' in r['age'] and '10–12' in r['age'] and '3sessions' in r['programme'] and '2' in r['programme']
assert r['family_fit']['matvey']['status']=='conditional' and r['family_fit']['oscar']['status']=='later'
assert '8–9' in p['la-garenne']['programme'] and 'подтверждения' in p['la-garenne']['programme']
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2166
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==162;con.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
  assert f['UID'] not in out
  out[f['UID']]=(f.get('DTSTART;VALUE=DATE',f.get('DTSTART')),f.get('DTEND;VALUE=DATE',f.get('DTEND')))
 return out
fn='dist/downloads/STEM_подтвержденные_даты.ics';before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1467 and len(now)==1519 and all(now.get(k)==v for k,v in before.items()) and len(set(now)-set(before))==52
for e in new:assert ('stem-'+e['id']+'@family-stem.local' in now)==(e not in closed)
assert not any('CP158-' in uid or 'CP162-' in uid for uid in now)
fn='dist/downloads/STEM_крупные_выставки.ics';assert calendar((ROOT/fn).read_bytes())==calendar(oldfile(fn)) and len(calendar(oldfile(fn)))==104
assert not any(c['research_status']=='fully_audited' for c in d['countries'] if 'research_status' in c)
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']=='active' and plan['previous_goal_turn_classification']['classification']=='progress'
print(json.dumps(dict(prior_events_unchanged=2108,corrected_events=3,prior_dossiers_unchanged=151,corrected_dossiers=1,new_dossiers=10,new_catalogue_dates=55,dossiers=162,countries=28,swiss=35,official_urls=305,family_ical=1519,exhibition_ical=104,closed_boarding=3,calculated_day_windows=14,sqlite='ok',bridge='idempotent'),ensure_ascii=False))
