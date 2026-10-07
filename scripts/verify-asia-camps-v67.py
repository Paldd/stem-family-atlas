"""Verify current intake, exact attendance and additive database preservation."""
import datetime,json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
BASE='7ca9d22b2e353ba6248dacd6976b393dd7835eab'
def oldfile(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(oldfile('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};rows={e['id']:e for e in d['events']}
assert len(rows)==len(d['events'])==2254
assert all(rows.get(k)==v for k,v in old.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[key]==b[key],key
p={x['slug']:x for x in d['camp_programmes']['profiles']};op={x['slug']:x for x in b['camp_programmes']['profiles']}
assert len(p)==198 and len(set(p)-set(op))==19
assert all(p[k]==v for k,v in op.items())
c=d['camp_programmes']['counts']
assert c==dict(dossiers=198,countries=28,swiss=35,by_status={'published_2026_27':19,'published_2027':54,'partial_2027':22,'published_2026':35,'next_unannounced':61,'partial_2026_27':7},source_urls=351)
assert sum(e['block']=='Лагеря' for e in rows.values())==923
assert len(d['camp_programmes']['generated_event_ids'])==460
assert d['camp_programmes']['integration']['reused_legacy_events']==58
assert d['camp_programmes']['integration']['seasonal_windows']==12
assert len(d['camp_programmes']['shortlist'])==31
assert d['camp_programmes']['shortlist'][:28]==b['camp_programmes']['shortlist']
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==d['camp_programmes']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==json.loads((ROOT/'data/research-plan.json').read_text())
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[e for k,e in rows.items() if k not in old];assert len(new)==36
assert all(e['checked']=='2026-10-05' and e['block']=='Лагеря' for e in new)
for slug in set(p)-set(op):
 q=p[slug];assert q['checked']=='2026-10-05' and q['iso'] in ['SGP','JPN','TWN','KOR']
 assert all(s['checked']=='2026-10-05' and s['url'].startswith('https://') for s in q['sources'])
 assert not q['related_event_ids']
for slug,amount,role in [('koa-classic',98000,'camp_life'),('koa-aire',117000,'camp_life'),('koa-english-ski',125000,'primary')]:
 q=p[slug];assert q['language_evidence_role']==role and q['confirmed_instruction_languages']==['EN']
 assert q['formats']==['boarding'] and len(q['timing']['sessions'])==2
 assert q['price']['season']=='2026/27' and f'{amount:,}' in q['price']['label']
 assert 'Grade 1' in q['family_fit']['oscar']['detail'] and '6' in q['family_fit']['oscar']['detail']
 assert '21' in q['price']['deposit'] and '17:00' in q['price']['deposit']
a=p['ayla-tokyo'];assert len(a['timing']['sessions'])==24
assert not a['confirmed_instruction_languages'] and a['price']['season']=='2026/27'
assert a['family_fit']['matvey']['status']=='conditional' and a['family_fit']['oscar']['status']=='candidate'
assert '10%' in a['price']['label'] and 'non-refundable' in a['price']['deposit']
for e in new:
 if e['camp_dossier_slug']!='ayla-tokyo':continue
 assert not(e['start']<='2027-08-11'<=e['end'])
 assert e['date_scope']=='day_camp_window' and e['attendance_weekdays']==['MO','TU','WE','TH','FR']
 if e['start'] in ['2027-08-09','2027-08-12']:assert e['date_precision']=='published_rule' and 'no school' in e['date_rule'] and '22,000' in e['cost']
 assert '20267' not in e['start'] and '20267' not in e['end']
assert ['2027-07-20','2027-07-23'] in a['timing']['sessions'] and ['2027-03-23','2027-03-26'] in a['timing']['sessions']
u=[x for x in p.values() if x['slug'].startswith('uwc-dover-')];assert len(u)==9
assert not any(x['confirmed_instruction_languages'] for x in u)
active={x['slug'] for x in u if x['intake_evidence']=='offered_in_current_schedule'}
assert active=={'uwc-dover-sciencecraft','uwc-dover-python-ml','uwc-dover-minecraft'}
assert sum(len(x['timing']['sessions']) for x in u)==4
for q in u:
 if q['slug'] not in active:assert not q['timing']['sessions'] and q['price']['year'] is None
 else:assert q['price']['year']==2026 and '434.50' in q['price']['label'] and '71.50' in q['price']['extras']
assert p['uwc-dover-python-ml']['family_fit']['matvey']['status']==p['uwc-dover-python-ml']['family_fit']['oscar']['status']=='later'
sh=p['shhk-spike-claw'];assert len(sh['timing']['sessions'])==2 and sh['price']['year']==2026
assert not sh['confirmed_instruction_languages'] and sh['family_fit']['oscar']['status']=='later'
assert len({x['place'] for x in sh['timing']['session_details']})==2
for slug in ['citop-day','citop-uch','citop-eda']:
 q=p[slug];assert not q['timing']['sessions'] and q['price']['year'] is None and q['confirmed_instruction_languages']==['EN']
assert '1 500' in p['citop-uch']['price']['extras'] and '1 000' in p['citop-eda']['price']['extras']
assert not p['ishou-international']['timing']['sessions'] and p['ishou-international']['timing']['status']=='partial_2027'
assert p['ishou-international']['language_evidence_role']=='camp_life' and p['ishou-international']['price']['year'] is None
kr=p['cistudy-jeju-seoul'];assert not kr['timing']['sessions'] and kr['price']['year']==2026
assert kr['booking_channel']=='CiStudy' and kr['operator_identity_status']=='unconfirmed' and kr['language_evidence_role']=='language_lessons'
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2254
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==198;con.close()
def calendar(raw):
 t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
 for ch in t.split('BEGIN:VEVENT')[1:]:
  f={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
  assert f['UID'] not in out
  out[f['UID']]=(f.get('DTSTART;VALUE=DATE',f.get('DTSTART')),f.get('DTEND;VALUE=DATE',f.get('DTEND')))
 return out
fn='dist/downloads/STEM_подтвержденные_даты.ics';before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1550 and len(now)==1585 and all(now.get(k)==v for k,v in before.items()) and len(set(now)-set(before))==35
for e in new:assert ('stem-'+e['id']+'@family-stem.local' in now)==(e['camp_dossier_slug']!='uwc-dover-python-ml')
fn='dist/downloads/STEM_крупные_выставки.ics';assert calendar((ROOT/fn).read_bytes())==calendar(oldfile(fn)) and len(calendar(oldfile(fn)))==104
assert d['coverage_summary']['fully_audited_countries']==0
plan=json.loads((ROOT/'data/research-plan.json').read_text());assert plan['status']=='active' and plan['previous_goal_turn_classification']['classification']=='progress'
assert 'Version66' in plan['previous_goal_turn_classification']['evidence']
print(json.dumps(dict(prior_events_unchanged=2218,prior_dossiers_unchanged=179,new_dossiers=19,new_catalogue_dates=36,new_family_ical=35,dossiers=198,countries=28,swiss=35,official_urls=351,family_ical=1585,exhibition_ical=104,uwc_description_only=6,uwc_offered_profiles=3,uwc_future_ics_excluded=1,ayla_calendar_parts=24,ayla_closed_wednesday_excluded=True,season_windows=12,sqlite='ok',bridge='idempotent'),ensure_ascii=False))
