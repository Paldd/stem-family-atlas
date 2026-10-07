"""Verify preserved history, age gates, tariff conflicts and seasonal precision."""
import json
import sqlite3
import subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT = Path(__file__).resolve().parents[1]
BASE = 'df8870a07dd8e7f2cd3ff7b7f62543e06216312d'

def oldfile(name):
    return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)

b = json.loads(oldfile('data/catalog.json'))
d = json.loads((ROOT/'data/catalog.json').read_text())
old = {x['id']:x for x in b['events']}
ev = {x['id']:x for x in d['events']}
assert len(old) == 2321 and len(ev) == len(d['events']) == 2338
assert all(ev.get(k) == v for k,v in old.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key] == b[key],key
c = d['camp_programmes']
p = {x['slug']:x for x in c['profiles']}
op = {x['slug']:x for x in b['camp_programmes']['profiles']}
assert len(p) == 258 and len(set(p)-set(op)) == 16
assert all(p.get(k) == v for k,v in op.items())
assert c['counts']['countries'] == 30 and c['counts']['swiss'] == 49 and c['counts']['source_urls'] == 426
assert sum(x['iso']=='FRA' for x in p.values()) == 23
assert sum(x['iso']=='ESP' for x in p.values()) == 19
assert sum(x['block']=='Лагеря' for x in ev.values()) == 1007
assert len(c['generated_event_ids']) == 544
assert c['integration']['reused_legacy_events'] == 58 and c['integration']['seasonal_windows'] == 17
assert len(c['shortlist']) == 43 and c['shortlist'][:39] == b['camp_programmes']['shortlist']
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text()) == d
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text()) == c
again = json.loads(json.dumps(d))
integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()))
assert again == d
new = [x for k,x in ev.items() if k not in old]
assert len(new) == 17 and all(x['block']=='Лагеря' and x['checked']=='2026-10-05' for x in new)
windows = ['haut-lac-day-junior','haut-lac-day-multi','haut-lac-day-teen','lemania-fun-science','lemania-science-prep']
for slug in windows:
    q = p[slug]
    assert q['timing']['precision']=='season_window'
    assert all(x['kind']=='season_window' and not x['event_ids'] for x in q['calendar_links'])
    assert not any(x.get('camp_dossier_slug')==slug for x in new)
for slug in ['haut-lac-day-junior','haut-lac-day-multi','haut-lac-day-teen']:
    assert p[slug]['timing']['sessions']==[['2027-06-28','2027-07-30']]
    assert p[slug]['price']['year']==2026 and p[slug]['price']['season']=='2025–26'
    assert '2027 ещё не подтверждён' in p[slug]['price']['label']
q = p['hif-summer-2027']
assert q['timing']['sessions']==[['2027-07-03','2027-07-16'],['2027-07-17','2027-07-30']]
assert q['family_fit']['matvey']['status']=='conditional' and q['family_fit']['oscar']['status']=='later'
assert q['confirmed_instruction_languages']==['EN'] and 'D4' in q['programme'] and 'D9' in q['programme']
assert 'pick-up' in q['price']['extras'] and 'не подтверждённый тариф туда-обратно' in q['price']['extras']
assert 'собственную travel/medical insurance' in q['price']['extras']
q = p['haut-lac-boarding']
assert q['age']=='8–15' and q['family_fit']['oscar']['status']=='later'
assert len(q['timing']['sessions'])==5 and q['timing']['sessions'][-1]==['2027-07-25','2027-07-31']
assert '2 000' in q['price']['label'] and 1650+350==2000
assert p['haut-lac-storybook']['family_fit']['matvey']['status']=='not_eligible'
assert 'послеобеденных' in p['haut-lac-storybook']['price']['label']
q = p['haut-lac-winter-ski']
assert q['timing']['sessions']==[['2026-12-14','2026-12-18']]
assert not q['confirmed_instruction_languages'] and q['family_fit']['matvey']['status']=='conditional'
assert all(s in q['price']['label'] for s in ['850','780','750','665'])
assert 'lower-intermediate' in q['age'] and q['family_fit']['oscar']['status']=='later'
for slug in ['junior','multi','teen']:
    q = p['haut-lac-easter-'+slug]
    assert q['timing']['sessions']==[['2027-03-30','2027-04-02'],['2027-04-05','2027-04-09']]
    assert 'четырёхдневной' in q['price']['label']
assert p['haut-lac-easter-teen']['family_fit']['matvey']['status']=='later'
assert '12–19' in p['lemania-fun-science']['age'] and '15–19' in p['lemania-fun-science']['age']
assert p['lemania-science-prep']['age']=='16–19'
for slug in ['lemania-fun-science','lemania-science-prep']:
    assert 'только девочкам' in p[slug]['price']['label']
    assert all(v['status']=='later' for v in p[slug]['family_fit'].values())
assert p['cll-isb-discoverers']['age']=='6–9' and p['cll-isb-explorers']['age']=='10–12'
for slug in ['cll-isb-discoverers','cll-isb-explorers']:
    q = p[slug]
    assert q['confirmed_instruction_languages']==['EN'] and not q['timing']['sessions']
    assert q['price']['year'] is None and q['timing']['status']=='next_unannounced'

def calendar(raw):
    t = raw.decode().replace('\r\n ','').replace('\r\n\t','')
    out = {}
    for ch in t.split('BEGIN:VEVENT')[1:]:
        fields = {x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert fields['UID'] not in out
        out[fields['UID']] = fields
    return out

fn = 'dist/downloads/STEM_подтвержденные_даты.ics'
before = calendar(oldfile(fn)); now = calendar((ROOT/fn).read_bytes())
assert len(before)==1645 and len(now)==1660 and len(set(now)-set(before))==15
for uid,prior in before.items():
    assert now[uid].get('DTSTART;VALUE=DATE')==prior.get('DTSTART;VALUE=DATE')
    assert now[uid].get('DTEND;VALUE=DATE')==prior.get('DTEND;VALUE=DATE')
for x in new:
    assert ('stem-'+x['id']+'@family-stem.local' in now)==(x['camp_dossier_slug']!='haut-lac-easter-teen')
fn = 'dist/downloads/STEM_крупные_выставки.ics'
exhibitions = calendar((ROOT/fn).read_bytes()); oldex = calendar(oldfile(fn))
assert len(exhibitions)==104 and set(exhibitions)==set(oldex)
for uid,prior in oldex.items():
    assert exhibitions[uid].get('DTSTART;VALUE=DATE')==prior.get('DTSTART;VALUE=DATE')
    assert exhibitions[uid].get('DTEND;VALUE=DATE')==prior.get('DTEND;VALUE=DATE')
con = sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2338
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==258
con.close()
plan = json.loads((ROOT/'data/research-plan.json').read_text())
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==70
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version69' in plan['previous_goal_turn_classification']['evidence']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert d['coverage_summary']['fully_audited_countries']==0
for stem in ['swiss-europe-camp-audit-v70','swiss-europe-camp-source-receipts-v70']:
    source = json.loads((ROOT/('data/'+stem+'.json')).read_text())
    assert json.loads((ROOT/('dist/downloads/STEM_'+stem.replace('-','_')+'.json')).read_text())==source
assert 'Haut-Lac: свежие сезоны' in (ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.md').read_text()
print(json.dumps(dict(prior_events_unchanged=2321,prior_dossiers_unchanged=242,new_dossiers=16,new_calendar_rows=17,new_family_ical=15,new_season_windows=5,events=2338,dossiers=258,countries=30,official_urls=426,family_ical=1660,exhibition_ical=104,sqlite='ok',bridge='idempotent',worldwide_goal='active'),ensure_ascii=False))
