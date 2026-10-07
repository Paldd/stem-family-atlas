"""Check dated offers, unresolved conflicts and preservation of prior research."""
import json
import sqlite3
import subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
BASE='0acfd341f6a0736a713109bce094a09f89c578e9'
def oldfile(name):
    return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(oldfile('data/catalog.json'))
d=json.loads((ROOT/'data/catalog.json').read_text())
old={x['id']:x for x in b['events']}; ev={x['id']:x for x in d['events']}
assert len(old)==2447 and len(ev)==len(d['events'])==2451
assert all(ev.get(k)==v for k,v in old.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==b[key],key
c=d['camp_programmes']; p={x['slug']:x for x in c['profiles']}
op={x['slug']:x for x in b['camp_programmes']['profiles']}
assert len(op)==300 and len(p)==314 and len(set(p)-set(op))==14
assert all(p.get(k)==v for k,v in op.items())
assert c['counts']['countries']==32 and c['counts']['swiss']==49 and c['counts']['source_urls']==507
assert sum(x['iso']=='FRA' for x in p.values())==30
assert sum(x['iso']=='ESP' for x in p.values())==26
assert sum(x['block']=='Лагеря' for x in ev.values())==1120
assert len(c['generated_event_ids'])==657
assert c['integration']['reused_legacy_events']==58 and c['integration']['seasonal_windows']==18
assert len(c['shortlist'])==59 and c['shortlist'][:55]==b['camp_programmes']['shortlist']
for name,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:
    assert json.loads((ROOT/'dist/downloads'/name).read_text())==wanted
again=json.loads(json.dumps(d))
integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()))
assert again==d
new=[x for k,x in ev.items() if k not in old]
assert len(new)==4 and all(x['block']=='Лагеря' and x['checked']=='2026-10-05' for x in new)
def rows(slug):return [x for x in new if x['camp_dossier_slug']==slug]
def pairs(slug):return [(x['start'],x['end']) for x in rows(slug)]
assert pairs('seacamp-panama')==[('2027-01-07','2027-01-10'),('2027-03-25','2027-03-28')]
q=p['seacamp-panama']; text=json.dumps(q,ensure_ascii=False)
assert 'USD 650' in q['price']['label'] and 'USD 200' in q['price']['deposit'] and 'в счёт' in q['price']['deposit']
assert '19–22' in text and '11–14' in text and 'исключён' in q['timing']['label']
assert not any(x['start'].startswith('2027-02') for x in rows(q['slug']))
assert q['family_fit']['oscar']['status']=='conditional' and q['confirmed_instruction_languages']==[]
assert q['formats']==['boarding'] and 'Isla Saboga' in q['place']
assert pairs('llanada-panama-board')==[('2027-01-24','2027-01-31')]
assert pairs('llanada-panama-valle')==[('2027-01-25','2027-01-29')]
for slug in ['llanada-panama-board','llanada-panama-valle','llanada-panama-city']:
    q=p[slug]
    assert q['confirmed_instruction_languages']==['ES'] and q['language_evidence_role']=='camp_life'
    assert 'помощь' in q['language'] and 'не английская смена' in q['language']
assert '6–10' in p['llanada-panama-valle']['age'] and '6–12' in p['llanada-panama-valle']['age']
assert p['llanada-panama-valle']['family_fit']['oscar']['status']=='candidate'
assert '400' in p['llanada-panama-valle']['price']['label'] and 'City-bus' in p['llanada-panama-valle']['price']['extras']
assert rows('llanada-panama-valle')[0]['date_scope']=='day_camp_window'
assert '1 290' in p['llanada-panama-board']['price']['label'] and '1 352' in p['llanada-panama-board']['price']['label']
assert p['llanada-panama-board']['family_fit']['oscar']['status']=='conditional'
assert not rows('llanada-panama-city') and p['llanada-panama-city']['price']['year'] is None
for slug in ['sek-cr-space','tecnobotrix-summer','robotpunk-summer','wecode-pocitos-lab','wecode-pocitos-ia','wecode-pocitos-minecraft','british-chile-young-a','british-chile-young-b']:
    q=p[slug]
    assert q['price']['year']==2026 and not q['timing']['sessions'] and not rows(slug)
assert p['sek-cr-space']['family_fit']['oscar']['status']=='unknown'
assert 'IVA' in p['sek-cr-space']['price']['label'] and '51 980' in p['sek-cr-space']['price']['extras']
assert p['robotpunk-summer']['family_fit']['matvey']['status']=='unknown'
assert p['tecnobotrix-summer']['family_fit']['oscar']['status']=='conditional'
q=p['troonic-robotics-camp']
assert q['price']['year']==2027 and '700' in q['price']['label'] and q['formats']==['day']
assert not q['timing']['sessions'] and q['timing']['precision']=='season_window' and not rows(q['slug'])
assert q['related_event_ids']==['L149','L150'] and 'членам' in q['place']
for slug in ['wecode-pocitos-lab','wecode-pocitos-ia','wecode-pocitos-minecraft']:
    q=p[slug]
    assert 'Grade' in q['age'] and q['family_fit']['matvey']['status']=='conditional'
    assert 'ISO' in q['price']['label'] and 'вероятно UYU' in q['price']['label']
    assert q['confirmed_instruction_languages']==[]
assert 'Windows 8' in p['wecode-pocitos-minecraft']['price']['included']
for slug in ['british-chile-young-a','british-chile-young-b','norte-chile-summer']:
    q=p[slug]
    assert q['confirmed_instruction_languages']==['EN'] and q['language_evidence_role']=='language_lessons'
    assert not rows(slug)
q=p['norte-chile-summer']
assert q['price']['year']==2027 and q['timing']['precision']=='season_window'
assert '2024' in q['timing']['label'] and '23850' in q['price']['label'] and '29158' in q['price']['label']
assert q['family_fit']['oscar']['status']=='conditional'
assert all(x['checked']=='2026-10-05' for s,x in p.items() if s not in op)

def calendar(raw):
    t=raw.decode().replace('\r\n ','').replace('\r\n\t',''); out={}
    for ch in t.split('BEGIN:VEVENT')[1:]:
        f={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert f['UID'] not in out;out[f['UID']]=f
    return out
fn='dist/downloads/STEM_подтвержденные_даты.ics'
before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1768 and len(now)==1772 and len(set(now)-set(before))==4
for uid,prior in before.items():
    assert now[uid].get('DTSTART;VALUE=DATE')==prior.get('DTSTART;VALUE=DATE')
    assert now[uid].get('DTEND;VALUE=DATE')==prior.get('DTEND;VALUE=DATE')
for x in new:assert 'stem-'+x['id']+'@family-stem.local' in now
fn='dist/downloads/STEM_крупные_выставки.ics'
ex=calendar((ROOT/fn).read_bytes());oldex=calendar(oldfile(fn))
assert len(ex)==104 and set(ex)==set(oldex)
for uid,prior in oldex.items():
    assert {k:v for k,v in ex[uid].items() if k!='DTSTAMP'}=={k:v for k,v in prior.items() if k!='DTSTAMP'}
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2451
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==314
con.close()
plan=json.loads((ROOT/'data/research-plan.json').read_text())
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==74
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version73' in plan['previous_goal_turn_classification']['evidence']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert d['coverage_summary']['fully_audited_countries']==0
for stem in ['latam-camp-audit-v74','latam-camp-source-receipts-v74']:
    a=json.loads((ROOT/('data/'+stem+'.json')).read_text())
    assert json.loads((ROOT/('dist/downloads/STEM_'+stem.replace('-','_')+'.json')).read_text())==a
html=(ROOT/'dist/index.html').read_text()
assert 'data-ui-version="74"' in html and '?v=73' not in html
assert 'STEM_latam_camp_audit_v74.json' in (ROOT/'dist/assets/camp-programmes.js').read_text()
print(json.dumps(dict(passed=True,preserved_events=len(old),preserved_dossiers=len(op),new_dossiers=14,
    new_calendar_rows=4,new_family_ics=4,events=len(ev),dossiers=len(p),family_ics=len(now),
    exhibition_ics=len(ex),season_windows=18,worldwide_complete=False)))
