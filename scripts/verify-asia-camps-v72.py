"""Check exact session alternatives, holiday gaps and actual admission evidence."""
import json
import sqlite3
import subprocess
from datetime import date, timedelta
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT = Path(__file__).resolve().parents[1]
BASE = 'ccdfeb900f9950bfefb5d3e37bad14ad5f666e44'
def oldfile(name):
    return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)

b=json.loads(oldfile('data/catalog.json'))
d=json.loads((ROOT/'data/catalog.json').read_text())
old={x['id']:x for x in b['events']}
ev={x['id']:x for x in d['events']}
assert len(old)==2355 and len(ev)==len(d['events'])==2392
assert all(ev.get(k)==v for k,v in old.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==b[key],key
c=d['camp_programmes'];p={x['slug']:x for x in c['profiles']}
op={x['slug']:x for x in b['camp_programmes']['profiles']}
assert len(p)==286 and len(set(p)-set(op))==13
assert all(p.get(k)==v for k,v in op.items())
assert c['counts']['countries']==30 and c['counts']['swiss']==49 and c['counts']['source_urls']==457
assert sum(x['iso']=='FRA' for x in p.values())==30
assert sum(x['iso']=='ESP' for x in p.values())==26
assert sum(x['block']=='Лагеря' for x in ev.values())==1061
assert len(c['generated_event_ids'])==598
assert c['integration']['reused_legacy_events']==58 and c['integration']['seasonal_windows']==18
assert len(c['shortlist'])==51 and c['shortlist'][:47]==b['camp_programmes']['shortlist']
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==c
again=json.loads(json.dumps(d))
integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()))
assert again==d
new=[x for k,x in ev.items() if k not in old]
assert len(new)==37 and all(x['block']=='Лагеря' and x['checked']=='2026-10-05' for x in new)
def rows(slug):
    return [x for x in new if x['camp_dossier_slug']==slug]
def pairs(slug):
    return [(x['start'],x['end']) for x in rows(slug)]

for slug,n in [('computhink-lego',4),('computhink-scratch',2),('computhink-agent',8),('computhink-redstone',8)]:
    q=p[slug]
    assert len(rows(slug))==n
    assert q['timing']['variant_keyed'] and q['confirmed_instruction_languages']==[]
    assert q['family_fit']['matvey']['status']=='conditional' and q['family_fit']['oscar']['status']=='later'
    assert q['price']['year']==2026 and '367' in q['price']['label']
    assert len({x['id'] for x in rows(slug)})==n
    for x in rows(slug):
        assert (date.fromisoformat(x['end'])-date.fromisoformat(x['start'])).days==2
        assert '367' in x['cost'] and ('09:30' in x['title'] or '14:00' in x['title'])
for slug in ['computhink-agent','computhink-redstone']:
    assert len(set(pairs(slug)))==4
    for a,z in set(pairs(slug)):
        choices=[x['title'] for x in rows(slug) if (x['start'],x['end'])==(a,z)]
        assert len(choices)==2 and any('09:30' in x for x in choices) and any('14:00' in x for x in choices)
assert pairs('bc-sg-early')==[('2026-12-14','2026-12-18')]
assert 'Napier' in p['bc-sg-early']['place'] and 'Toa Payoh' not in p['bc-sg-early']['place']
assert p['bc-sg-early']['family_fit']['matvey']['status']=='not_eligible'
for slug in ['bc-sg-p12','bc-sg-p34']:
    assert len(rows(slug))==4 and p[slug]['confirmed_instruction_languages']==['EN']
    assert 'класс' in p[slug]['family_fit']['matvey']['detail']
assert p['bc-sg-p34']['family_fit']['oscar']['status']=='later'
expected=[('2027-01-18','2027-01-22'),('2027-01-25','2027-01-29'),
          ('2027-02-01','2027-02-04'),('2027-02-09','2027-02-12'),('2027-02-15','2027-02-19')]
assert pairs('bc-sg-winter-primary')==expected
q=p['bc-sg-winter-primary']
assert 'диагностики' in q['language'] and 'не пересчитываем' in q['price']['label']
assert '7-летия' in q['family_fit']['oscar']['detail']
for x in rows('bc-sg-winter-primary'):
    assert x['date_scope']=='day_camp_window'
    assert x['attendance_weekdays']==['MO','TU','WE','TH','FR']
    assert not any(x['start']<=z<=x['end'] for z in ['2027-02-05','2027-02-08'])
for slug in ['bc-sg-early','bc-sg-p12','bc-sg-p34','bc-sg-winter-primary']:
    assert '§5.2' in p[slug]['price']['deposit'] and '§5.6' in p[slug]['price']['deposit']
for slug in ['bc-tw-early','bc-tw-primary']:
    assert p[slug]['timing']['status']=='partial_2027' and not pairs(slug)
    assert p[slug]['price']['year'] is None and not p[slug]['timing']['sessions']
assert 'Grade 1' in p['bc-tw-primary']['age']
assert p['bc-tw-early']['family_fit']['matvey']['status']=='not_eligible'
assert pairs('steamsquad-expedition')==[('2027-01-21','2027-02-03')]
q=p['steamsquad-expedition'];x=rows(q['slug'])[0]
days=[];start=date.fromisoformat(x['start']);end=date.fromisoformat(x['end'])
while start<=end:
    if start.weekday()<5:days.append(start)
    start+=timedelta(days=1)
assert len(days)==10 and x['attendance_weekdays']==['MO','TU','WE','TH','FR']
assert 'полный курс' in x['cost'] and '27 000' in x['cost']
assert 'отдельно' in q['price']['extras'] and q['family_fit']['oscar']['status']=='later'
for slug in ['codinglab-japan','lfs-seoul']:
    assert not pairs(slug) and not p[slug]['timing']['sessions']
assert p['codinglab-japan']['confirmed_instruction_languages']==['EN']
assert 'одинаковую' in p['codinglab-japan']['programme']
assert p['lfs-seoul']['price']['year']==2026 and p['lfs-seoul']['language_evidence_role']=='language_lessons'
assert 'Alien Registration Card' in p['lfs-seoul']['editorial_reason']

def calendar(raw):
    t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
    for ch in t.split('BEGIN:VEVENT')[1:]:
        fields={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert fields['UID'] not in out
        out[fields['UID']]=fields
    return out
fn='dist/downloads/STEM_подтвержденные_даты.ics'
before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1676 and len(now)==1713 and len(set(now)-set(before))==37
for uid,prior in before.items():
    assert now[uid].get('DTSTART;VALUE=DATE')==prior.get('DTSTART;VALUE=DATE')
    assert now[uid].get('DTEND;VALUE=DATE')==prior.get('DTEND;VALUE=DATE')
for x in new:
    assert 'stem-'+x['id']+'@family-stem.local' in now
fn='dist/downloads/STEM_крупные_выставки.ics'
ex=calendar((ROOT/fn).read_bytes());oldex=calendar(oldfile(fn))
assert len(ex)==104 and set(ex)==set(oldex)
for uid,prior in oldex.items():
    assert {k:v for k,v in ex[uid].items() if k!='DTSTAMP'}=={k:v for k,v in prior.items() if k!='DTSTAMP'}
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2392
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==286
con.close()
plan=json.loads((ROOT/'data/research-plan.json').read_text())
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==72
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version71' in plan['previous_goal_turn_classification']['evidence']
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert d['coverage_summary']['fully_audited_countries']==0
for stem in ['asia-camp-audit-v72','asia-camp-source-receipts-v72']:
    a=json.loads((ROOT/('data/'+stem+'.json')).read_text())
    assert json.loads((ROOT/('dist/downloads/STEM_'+stem.replace('-','_')+'.json')).read_text())==a
html=(ROOT/'dist/index.html').read_text()
assert 'data-ui-version="72"' in html and '?v=71' not in html
print(json.dumps(dict(passed=True,preserved_events=len(old),preserved_dossiers=len(op),new_dossiers=13,
    new_calendar_rows=37,new_family_ics=37,events=len(ev),dossiers=len(p),family_ics=len(now),
    exhibition_ics=len(ex),season_windows=18,worldwide_complete=False)))
