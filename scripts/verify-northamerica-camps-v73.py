"""Verify new programme gates, price conflicts and preserved family calendars."""
import json
import sqlite3
import subprocess
from datetime import date
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
BASE='36f5491728afdfb6d69f5bbf517f4a0f822f0cb4'
def oldfile(name):
    return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(oldfile('data/catalog.json'))
d=json.loads((ROOT/'data/catalog.json').read_text())
old={x['id']:x for x in b['events']};ev={x['id']:x for x in d['events']}
assert len(old)==2392 and len(ev)==len(d['events'])==2447
assert all(ev.get(k)==v for k,v in old.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==b[key],key
c=d['camp_programmes'];p={x['slug']:x for x in c['profiles']}
op={x['slug']:x for x in b['camp_programmes']['profiles']}
assert len(p)==300 and len(set(p)-set(op))==14
assert all(p.get(k)==v for k,v in op.items())
assert c['counts']['countries']==30 and c['counts']['swiss']==49 and c['counts']['source_urls']==487
assert sum(x['iso']=='FRA' for x in p.values())==30
assert sum(x['iso']=='ESP' for x in p.values())==26
assert sum(x['block']=='Лагеря' for x in ev.values())==1116
assert len(c['generated_event_ids'])==653
assert c['integration']['reused_legacy_events']==58 and c['integration']['seasonal_windows']==18
assert len(c['shortlist'])==55 and c['shortlist'][:51]==b['camp_programmes']['shortlist']
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==c
again=json.loads(json.dumps(d))
integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()))
assert again==d
new=[x for k,x in ev.items() if k not in old]
assert len(new)==55 and all(x['block']=='Лагеря' and x['checked']=='2026-10-05' for x in new)
def rows(slug):return [x for x in new if x['camp_dossier_slug']==slug]
def pairs(slug):return [(x['start'],x['end']) for x in rows(slug)]
for slug in set(p)-set(op):
    assert p[slug]['confirmed_instruction_languages']==[],slug
    assert p[slug]['checked']=='2026-10-05'
for x in new:
    assert x['languages']==[] and x['language_mode']=='unconfirmed'

assert pairs('emerson-two-weeks')==[('2027-06-27','2027-07-10'),('2027-07-11','2027-07-24'),('2027-07-25','2027-08-07')]
assert pairs('emerson-awesome-week')==[('2027-08-08','2027-08-14')]
for slug in ['emerson-two-weeks','emerson-awesome-week']:
    q=p[slug]
    assert q['price']['year']==2027 and q['formats']==['boarding']
    assert '7-летия' in q['family_fit']['oscar']['detail']
    assert '200' in q['price']['extras'] and 'stay-over' in q['price']['extras']
    assert 'робототехника' in q['programme'] or 'интенсив' in q['programme']
assert '15 700/16 100' in p['emerson-two-weeks']['price']['label']
q=p['summertech-python']
assert not rows(q['slug']) and q['price']['year']==2026 and not q['timing']['sessions']
assert 'Grade 4' in q['family_fit']['matvey']['detail'] and q['family_fit']['oscar']['status']=='later'
assert '1 650' in q['price']['label'] and '2 300' in q['price']['label']
assert '+650' in q['price']['label'] and '50%' in q['price']['deposit']

expected=[('2027-06-28','2027-07-02'),('2027-07-05','2027-07-09'),('2027-07-12','2027-07-16'),
    ('2027-07-19','2027-07-23'),('2027-07-26','2027-07-30'),('2027-08-02','2027-08-06'),('2027-08-09','2027-08-13')]
for slug,cost in [('inventor-laval-junior',389),('inventor-laval-mechanics',409),('inventor-laval-middle',429),
    ('inventor-laval-middle-plus',439),('inventor-laval-senior',449)]:
    q=p[slug]
    wanted=expected[:1]+expected[2:] if slug=='inventor-laval-mechanics' else expected
    assert pairs(slug)==wanted and str(cost) in q['price']['label']
    assert 'Laval' in q['place'] and '950' in q['place'] and 'Dollard' not in q['place']
    assert 'повторяются' in q['programme'] and 'две недели' in q['programme']
    assert 'обед и два перекуса' in q['price']['extras'] and '3%' in q['price']['deposit']
    for x in rows(slug):
        assert x['date_scope']=='day_camp_window' and date.fromisoformat(x['start']).weekday()==0
        assert date.fromisoformat(x['end']).weekday()==4
assert p['inventor-laval-mechanics']['timing']['unresolved_sessions'][0]['start']=='2027-07-06'
assert '4.5–7' in p['inventor-laval-junior']['age']
assert p['inventor-laval-junior']['family_fit']['oscar']['status']=='conditional'
assert 'Essential' in p['inventor-laval-middle-plus']['programme']
assert 'Prime' in p['inventor-laval-senior']['programme']
assert '11–12' in p['inventor-laval-senior']['age'] and '9–12' in p['inventor-laval-senior']['age']
assert p['inventor-laval-senior']['family_fit']['matvey']['status']=='conditional'
q=p['canadventure-general']
assert len(rows(q['slug']))==9 and q['price']['year']==2027
assert 'Adventure Island' in q['place'] and 'офис' in q['place']
assert '895' in q['price']['extras'] and 'Tuck CAD150' in q['price']['extras'] and 'Налог сверх' in q['price']['label']
assert 'Размер аванса' in q['price']['deposit'] and '7-летия' in q['family_fit']['oscar']['detail']
assert all(x['date_scope']=='camp_session' and 'tax' in x['cost'] for x in rows(q['slug']))
for slug in ['brainstem-winter-little','brainstem-winter-specialists']:
    q=p[slug]
    assert len(rows(slug))==3 and set(pairs(slug))=={('2026-12-28','2026-12-31')}
    assert q['timing']['variant_keyed'] and 'суммарно' in q['age']
    assert '240' in q['price']['label'] and '528' in q['price']['label']
    assert 'CAD48' in q['price']['extras'] and '90' in q['price']['deposit']
    assert any('528' in x['cost'] for x in rows(slug)) and sum('240' in x['cost'] for x in rows(slug))==2
assert p['brainstem-winter-little']['family_fit']['matvey']['status']=='not_eligible'
assert p['brainstem-winter-specialists']['family_fit']['oscar']['status']=='later'
assert any('09:30' in x['title'] for x in rows('brainstem-winter-little'))
assert all('09:30' not in x['title'] for x in rows('brainstem-winter-specialists'))
assert pairs('stemotics-winter')==[('2026-12-21','2026-12-24'),('2026-12-28','2026-12-31')]
q=p['stemotics-winter']
assert '239.99' in q['price']['label'] and '199.99' in q['price']['label'] and '3днями' in q['price']['label']
assert 'ещё вычитает35' in q['price']['deposit'] and 'остаются' in q['price']['included']
assert not any(x['start']<=z<=x['end'] for x in rows(q['slug']) for z in ['2026-12-25','2027-01-01'])
for slug in ['envision-winter-audit','galileo-irvine']:
    assert not rows(slug) and not p[slug]['timing']['sessions']
assert p['envision-winter-audit']['price']['year'] is None and 'no-refund' in p['envision-winter-audit']['price']['deposit']
assert '30декабря' in p['envision-winter-audit']['timing']['label']
assert p['galileo-irvine']['price']['year']==2026 and 'CLOSED' in p['galileo-irvine']['timing']['label']

def calendar(raw):
    t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
    for ch in t.split('BEGIN:VEVENT')[1:]:
        f={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert f['UID'] not in out;out[f['UID']]=f
    return out
fn='dist/downloads/STEM_подтвержденные_даты.ics'
before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1713 and len(now)==1768 and len(set(now)-set(before))==55
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
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2447
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==300
con.close()
plan=json.loads((ROOT/'data/research-plan.json').read_text())
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==73
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version72' in plan['previous_goal_turn_classification']['evidence']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert d['coverage_summary']['fully_audited_countries']==0
for stem in ['northamerica-camp-audit-v73','northamerica-camp-source-receipts-v73']:
    a=json.loads((ROOT/('data/'+stem+'.json')).read_text())
    assert json.loads((ROOT/('dist/downloads/STEM_'+stem.replace('-','_')+'.json')).read_text())==a
html=(ROOT/'dist/index.html').read_text()
assert 'data-ui-version="73"' in html and '?v=72' not in html
print(json.dumps(dict(passed=True,preserved_events=len(old),preserved_dossiers=len(op),new_dossiers=14,
    new_calendar_rows=55,new_family_ics=55,events=len(ev),dossiers=len(p),family_ics=len(now),
    exhibition_ics=len(ex),season_windows=18,worldwide_complete=False)))
