"""Prevent false holiday attendance, archived-year promotion and lost earlier research."""
import json
import sqlite3
import subprocess
from datetime import date, timedelta
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT = Path(__file__).resolve().parents[1]
BASE = 'b04a347f78171d44c50976ce11a21c353860f3f2'
def oldfile(name):
    return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)

b = json.loads(oldfile('data/catalog.json'))
d = json.loads((ROOT/'data/catalog.json').read_text())
old = {x['id']:x for x in b['events']}
ev = {x['id']:x for x in d['events']}
assert len(old)==2338 and len(ev)==len(d['events'])==2355
assert all(ev.get(k)==v for k,v in old.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==b[key],key
c = d['camp_programmes']; p = {x['slug']:x for x in c['profiles']}
op = {x['slug']:x for x in b['camp_programmes']['profiles']}
assert len(p)==273 and len(set(p)-set(op))==15
assert all(p.get(k)==v for k,v in op.items())
assert c['counts']['countries']==30 and c['counts']['swiss']==49 and c['counts']['source_urls']==441
assert sum(x['iso']=='FRA' for x in p.values())==30
assert sum(x['iso']=='ESP' for x in p.values())==26
assert sum(x['block']=='Лагеря' for x in ev.values())==1024
assert len(c['generated_event_ids'])==561
assert c['integration']['reused_legacy_events']==58 and c['integration']['seasonal_windows']==18
assert len(c['shortlist'])==47 and c['shortlist'][:43]==b['camp_programmes']['shortlist']
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==c
again=json.loads(json.dumps(d))
integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()))
assert again==d
new=[x for k,x in ev.items() if k not in old]
assert len(new)==17 and all(x['block']=='Лагеря' and x['checked']=='2026-10-05' for x in new)

def dates_for(slug):
    return [(x['start'],x['end']) for x in new if x['camp_dossier_slug']==slug]

attendance=set()
for a,z in dates_for('casita-christmas'):
    a,z=date.fromisoformat(a),date.fromisoformat(z)
    while a<=z:
        attendance.add(a.isoformat()); a+=timedelta(days=1)
assert attendance=={'2026-12-23','2026-12-24','2026-12-28','2026-12-29','2026-12-30','2026-12-31','2027-01-04','2027-01-05','2027-01-07','2027-01-08'}
q=p['keiko-christmas']
assert q['timing']['precision']=='season_window' and not dates_for('keiko-christmas')
assert all(x['kind']=='season_window' and not x['event_ids'] for x in q['calendar_links'])
assert all(v['status']=='unknown' for v in q['family_fit'].values())
assert '5/день' in q['price']['extras'] and '130' in q['price']['label'] and '150' in q['price']['label']
for slug in ['tecnoeduka-christmas','av-cour-buis-summer','unicaja-tech','unicaja-english','funtech-christmas']:
    assert not dates_for(slug) and not p[slug]['timing']['sessions']
assert p['tecnoeduka-christmas']['price']['year']==2025
assert p['av-cour-buis-summer']['price']['year']==2026
assert p['funtech-christmas']['confirmed_instruction_languages']==[]
assert dates_for('av-cour-buis-spring')==[('2027-04-11','2027-04-16')]
assert dates_for('av-cour-buis-autumn')==[('2026-10-18','2026-10-23'),('2026-10-25','2026-10-30')]
assert dates_for('kaleidoscope-drama')==[('2026-10-19','2026-10-23')]
assert all(v['status']=='later' for v in p['kaleidoscope-drama']['family_fit'].values())
assert p['kaleidoscope-little']['family_fit']['matvey']['status']=='not_eligible'
assert p['kaleidoscope-multi']['family_fit']['oscar']['status']=='later'
assert dates_for('cimes-kids-english')==[('2027-07-22','2027-07-28')]
assert 'христианской' in p['cimes-kids-english']['programme']
assert p['cimes-kids-english']['family_fit']['oscar']['status']=='conditional'
for slug in ['native-goirle','native-salamanca']:
    q=p[slug]
    assert q['family_fit']['matvey']['status']=='conditional' and q['family_fit']['oscar']['status']=='later'
    assert 'EUR 200' in q['price']['deposit'] and '2021' in q['price']['deposit']
    assert q['language_evidence_role']=='camp_life' and q['confirmed_instruction_languages']==['EN']
for slug in ['unicaja-tech','unicaja-english']:
    q=p[slug]
    assert q['price']['year']==2026 and q['formats']==['boarding']
    assert all(v['status']=='conditional' for v in q['family_fit'].values())
    assert 'клиентом Unicaja' in q['family_fit']['matvey']['detail']
    assert 'DNI' in q['questions'][0]

def calendar(raw):
    t=raw.decode().replace('\r\n ','').replace('\r\n\t',''); out={}
    for ch in t.split('BEGIN:VEVENT')[1:]:
        fields={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert fields['UID'] not in out
        out[fields['UID']]=fields
    return out

fn='dist/downloads/STEM_подтвержденные_даты.ics'
before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1660 and len(now)==1676 and len(set(now)-set(before))==16
for uid,prior in before.items():
    assert now[uid].get('DTSTART;VALUE=DATE')==prior.get('DTSTART;VALUE=DATE')
    assert now[uid].get('DTEND;VALUE=DATE')==prior.get('DTEND;VALUE=DATE')
for x in new:
    assert ('stem-'+x['id']+'@family-stem.local' in now)==(x['camp_dossier_slug']!='kaleidoscope-drama')
fn='dist/downloads/STEM_крупные_выставки.ics'
ex=calendar((ROOT/fn).read_bytes());oldex=calendar(oldfile(fn))
assert len(ex)==104 and set(ex)==set(oldex)
for uid, prior in oldex.items():
    assert {k:v for k,v in ex[uid].items() if k!='DTSTAMP'}=={k:v for k,v in prior.items() if k!='DTSTAMP'}
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2355
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==273
con.close()
plan=json.loads((ROOT/'data/research-plan.json').read_text())
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==71
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version70' in plan['previous_goal_turn_classification']['evidence']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert d['coverage_summary']['fully_audited_countries']==0
for stem in ['france-spain-europe-camp-audit-v71','france-spain-europe-camp-source-receipts-v71']:
    a=json.loads((ROOT/('data/'+stem+'.json')).read_text())
    assert json.loads((ROOT/('dist/downloads/STEM_'+stem.replace('-','_')+'.json')).read_text())==a
print(json.dumps(dict(passed=True,preserved_events=len(old),preserved_dossiers=len(op),new_dossiers=15,new_calendar_rows=17,new_family_ics=16,events=len(ev),dossiers=len(p),family_ics=len(now),exhibition_ics=len(ex),season_windows=18,worldwide_complete=False)))
