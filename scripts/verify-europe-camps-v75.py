"""Validate age/year conflicts, calendar reuse and preservation of worldwide work."""
import json
import sqlite3
import subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
BASE='d7461e46b45468fec5bb26f3558bcfece2e87fa5'
def oldfile(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(oldfile('data/catalog.json'))
d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']}; ev={e['id']:e for e in d['events']}
assert len(old)==2451 and len(ev)==len(d['events'])==2483
assert all(ev.get(k)==v for k,v in old.items() if k!='L222')
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==b[key],key

# One documented correction, without permitting unrelated edits to its fields.
r=ev['L222'];prior=old['L222']
allowed={'title','start','end','source','checked','period','date_status','age','cost','gear','proof','note','references','date_scope','date_precision','attendance_weekdays'}
assert {k for k in set(r)|set(prior) if r.get(k)!=prior.get(k)}==allowed
assert (r['start'],r['end'])==('2027-07-12','2027-07-16') and r['date_status']=='Подтверждено'
assert r['source']=='https://www.helveticinstitute.ch/summer-robotics-camp-zug/'
assert not r['languages'] and 'обед' in r['note'] and '13–16' in r['note']
assert r['date_scope']=='day_camp_window' and r['attendance_weekdays']==['MO','TU','WE','TH','FR']

c=d['camp_programmes']; p={x['slug']:x for x in c['profiles']}
op={x['slug']:x for x in b['camp_programmes']['profiles']}
assert len(op)==314 and len(p)==322 and len(set(p)-set(op))==8
updated={
    'aiglon':{'price','age','checked','sources','editorial_reason','programme','family_fit','questions'},
    'rosenberg':{'age','checked','sources','programme','family_fit'},
    'cdl':{'price','age','calendar_links','accommodation','checked','sources','editorial_reason','programme','timing','family_fit','questions'}
}
assert all(p.get(k)==v for k,v in op.items() if k not in updated)
for slug,fields in updated.items():
    assert p[slug]['id']==op[slug]['id']
    assert {k for k in set(p[slug])|set(op[slug]) if p[slug].get(k)!=op[slug].get(k)}==fields
assert c['counts']['countries']==32 and c['counts']['swiss']==53 and c['counts']['source_urls']==516
assert sum(x['iso']=='FRA' for x in p.values())==33 and sum(x['iso']=='ESP' for x in p.values())==27
assert sum(x['block']=='Лагеря' for x in ev.values())==1152
assert len(c['generated_event_ids'])==689
assert c['integration']['reused_legacy_events']==64 and c['integration']['seasonal_windows']==18
assert len(c['shortlist'])==63 and c['shortlist'][:59]==b['camp_programmes']['shortlist']
for name,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:
    assert json.loads((ROOT/'dist/downloads'/name).read_text())==wanted
again=json.loads(json.dumps(d))
integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()))
assert again==d
new=[x for k,x in ev.items() if k not in old]
assert len(new)==32 and all(x['block']=='Лагеря' and x['checked']=='2026-10-05' for x in new)
def rows(slug):return [x for x in new if x['camp_dossier_slug']==slug]
def pairs(slug):return [(x['start'],x['end']) for x in rows(slug)]

assert len(rows('aiglon-classic-board'))==6 and len(rows('aiglon-classic-day'))==5
assert len(rows('cdl'))==3
q=p['aiglon-classic-board']
assert q['family_fit']['oscar']['status']=='later' and q['formats']==['boarding']
assert [x['price'] for x in q['timing']['session_details']]==['CHF 4 600','CHF 8 200','CHF 12 000','CHF 8 200','CHF 8 200','CHF 4 600']
assert 'несколько программ' in q['programme'] and 'одну неделю' in q['programme'] and not q['confirmed_instruction_languages']
q=p['aiglon-classic-day']
assert q['family_fit']['oscar']['status']=='conditional'
assert '7–16' in q['age'] and '8–16' in q['age'] and 'конфликт' in q['age']
assert all('2 500' in x['price'] for x in q['timing']['session_details']) and '500' in q['price']['extras']
assert not q['confirmed_instruction_languages']
assert all(x['date_scope']=='day_camp_window' and x['attendance_weekdays']==['MO','TU','WE','TH','FR'] for x in rows(q['slug']))
q=p['rosenberg']; assert '6–18' in q['age'] and 'неизвестен' in q['age']
assert all(q['family_fit'][child]['status']=='conditional' for child in ['matvey','oscar'])
q=p['cdl']; assert q['price']['year']==2026 and '12+' in q['age'] and '12' in q['family_fit']['matvey']['detail']
assert 'ноябре' in q['timing']['label'] and all('не опубликован' in x['cost'] for x in rows('cdl'))
assert pairs('cdl')==[('2027-06-27','2027-07-10'),('2027-07-11','2027-07-24'),('2027-07-25','2027-08-07')]

assert pairs('helvetic-zug-summer')==[('2027-07-05','2027-07-16')]
assert pairs('helvetic-zurich-summer')==[('2027-07-19','2027-07-30')]
assert set(x['event_ids'][0] for x in p['helvetic-zug-summer']['calendar_links'] if x['kind']=='existing_programme')=={'L221','L222','L223'}
assert set(x['event_ids'][0] for x in p['helvetic-zurich-summer']['calendar_links'] if x['kind']=='existing_programme')=={'L224','L225','L226'}
for s in ['helvetic-zug-summer','helvetic-zurich-summer']:
    assert p[s]['confirmed_instruction_languages']==[] and p[s]['family_fit']['oscar']['status']=='conditional'
assert '6–11' in p['helvetic-zug-summer']['age'] and 'Обед' in p['helvetic-zug-summer']['price']['extras']
assert not any(x['start']=='2027-07-13' for x in rows('helvetic-zug-summer'))

q=p['babel-holiday-english']; assert q['language_evidence_role']=='camp_life' and q['confirmed_instruction_languages']==['EN']
assert 'PS–CM2' in q['age'] and '3–8 детей' in q['age']
assert len(rows(q['slug']))==6 and not any(x['start'].startswith('2027-07') for x in rows(q['slug']))
assert {v['price'] for v in q['timing']['session_details']}=={'EUR 350','EUR 160'}
assert q['price']['season']=='2026/27' and 'не подтверждает' in q['price']['extras']
assert '10%' in q['price']['deposit'] and 'spring' in q['price']['deposit']
for slug,a,bday in [('littlebritish-boost','2027-07-05','2027-07-09'),('littlebritish-zoo','2027-07-12','2027-07-16')]:
    q=p[slug]
    assert q['language_evidence_role']=='language_lessons' and q['confirmed_instruction_languages']==['EN']
    assert len(rows(slug))==5 and len({x['city'] for x in rows(slug)})==5
    assert all(x['start']==a and x['end']==bday for x in rows(slug))
    assert all('12,5' in x['cost'] for x in rows(slug))
assert 'Primaire' in p['littlebritish-boost']['age']
assert p['littlebritish-boost']['family_fit']['oscar']['status']=='conditional'
assert '3–6' in p['littlebritish-zoo']['age'] and p['littlebritish-zoo']['family_fit']['matvey']['status']=='not_eligible'
assert p['littlebritish-zoo']['family_fit']['oscar']['status']=='conditional'
q=p['navatormes-english']; assert not rows(q['slug']) and not q['timing']['sessions']
assert q['price']['year']==2026 and q['confirmed_instruction_languages']==['EN']
assert 'PDF 2026' in q['language'] and 'tipis' in q['accommodation'] and 'albergue' in q['accommodation']
assert q['family_fit']['oscar']['status']=='conditional' and q['language_evidence_role']=='camp_life'
assert all(x['checked']=='2026-10-05' for s,x in p.items() if s not in op)

def calendar(raw):
    t=raw.decode().replace('\r\n ','').replace('\r\n\t',''); out={}
    for ch in t.split('BEGIN:VEVENT')[1:]:
        f={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert f['UID'] not in out;out[f['UID']]=f
    return out
fn='dist/downloads/STEM_подтвержденные_даты.ics'
before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert len(before)==1772 and len(now)==1805 and len(set(now)-set(before))==33
for uid,prior in before.items():
    assert now[uid].get('DTSTART;VALUE=DATE')==prior.get('DTSTART;VALUE=DATE')
    assert now[uid].get('DTEND;VALUE=DATE')==prior.get('DTEND;VALUE=DATE')
for x in new+[r]:assert 'stem-'+x['id']+'@family-stem.local' in now
assert now['stem-L222@family-stem.local']['DTSTART;VALUE=DATE']=='20270712'
fn='dist/downloads/STEM_крупные_выставки.ics'
ex=calendar((ROOT/fn).read_bytes());oldex=calendar(oldfile(fn))
assert len(ex)==104 and set(ex)==set(oldex)
for uid,prior in oldex.items():
    assert {k:v for k,v in ex[uid].items() if k!='DTSTAMP'}=={k:v for k,v in prior.items() if k!='DTSTAMP'}
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2483
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==322
con.close()
plan=json.loads((ROOT/'data/research-plan.json').read_text())
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==75
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version74' in plan['previous_goal_turn_classification']['evidence']
assert plan['camp_catalog_integration']['dossiers']==322 and plan['camp_catalog_integration']['generated_calendar_entries']==689
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert d['coverage_summary']['fully_audited_countries']==0
for stem in ['europe-camp-audit-v75','europe-camp-source-receipts-v75']:
    a=json.loads((ROOT/('data/'+stem+'.json')).read_text())
    assert json.loads((ROOT/('dist/downloads/STEM_'+stem.replace('-','_')+'.json')).read_text())==a
assert len(a['verified_new_dossier_urls'])==9
assert all(value is False for value in a['external_actions'].values())
html=(ROOT/'dist/index.html').read_text()
assert 'data-ui-version="75"' in html and '?v=74' not in html
assert 'STEM_europe_camp_audit_v75.json' in (ROOT/'dist/assets/camp-programmes.js').read_text()
print(json.dumps(dict(passed=True,preserved_events=2450,corrected_legacy_rows=1,preserved_dossier_ids=314,updated_dossiers=3,new_dossiers=8,
    new_calendar_rows=32,new_family_ics=33,events=len(ev),dossiers=len(p),family_ics=len(now),exhibition_ics=len(ex),worldwide_complete=False)))
