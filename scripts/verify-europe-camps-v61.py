"""Verify preservation, concrete eligibility gates and the rolling family calendar."""
import json, sqlite3, subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
BASE='49d346c216e041d2872e952c97a1f961747c4c72'
def oldfile(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
base=json.loads(oldfile('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
rows={e['id']:e for e in d['events']};oldrows={e['id']:e for e in base['events']}
assert len(rows)==len(d['events'])==2014
assert all(rows[k]==e for k,e in oldrows.items())
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==base[key],key
g=d['camp_programmes'];p={x['slug']:x for x in g['profiles']};oldp={x['slug']:x for x in base['camp_programmes']['profiles']}
assert all(p[k]==v for k,v in oldp.items())
assert len(p)==112 and len(p.keys()-oldp.keys())==10
assert g['counts']['countries']==27 and g['counts']['swiss']==18 and g['counts']['source_urls']==203
assert len(g['generated_event_ids'])==220
assert sum(e['block']=='Лагеря' for e in d['events'])==683
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==g
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[e for e in d['events'] if e['id'] not in oldrows]
assert len(new)==17 and all(e['block']=='Лагеря' and e['checked']=='2026-10-05' for e in new)
assert all(p[k]['checked']=='2026-10-05' for k in p.keys()-oldp.keys())
nl=p['bricks-robots-nl'];assert nl['confirmed_instruction_languages']==[]
assert len(nl['timing']['session_details'])==5 and len({v['variant_key'] for v in nl['timing']['session_details']})==5
assert 'Основной язык голландский' in nl['language'] and '4 дней отдельно не подтверждена' in nl['timing']['session_details'][1]['price']
closed=next(e for e in new if e.get('availability',{}).get('status')=='closed')
assert 'rotterdam' in closed['id']
assert p['heureka-science']['timing']['sessions']==[] and p['heureka-science']['price']['year'] is None
assert p['heureka-science']['family_fit']['oscar']['status']=='unknown'
assert p['arkki-family']['family_fit']['oscar']['status']=='candidate'
assert p['arkki-huts']['family_fit']['oscar']['status']=='conditional'
assert all(p[k]['price']['year']==2026 and not p[k]['timing']['sessions'] for k in ['arkki-family','arkki-huts'])
assert p['designer-minds']['confirmed_instruction_languages']==[] and '6.5' in p['designer-minds']['age'] and '1st' in p['designer-minds']['age']
assert p['gowreads-autumn']['confirmed_instruction_languages']==['EN'] and 'VAT' in p['gowreads-autumn']['price']['label']
assert '7' in p['bels-family']['age'] and p['bels-family']['timing']['sessions']==[]
assert all(p['neuslab-solutions']['family_fit'][k]['status']=='unknown' for k in ['matvey','oscar'])
assert all(p['ranum-summer']['family_fit'][k]['status']=='later' for k in ['matvey','oscar'])
assert len(p['ranum-summer']['timing']['sessions'])==6 and all(e['priority'].startswith('P4') for e in new if e['camp_dossier_slug']=='ranum-summer')
assert all(e['language_mode']=='camp_life' and 'robotics' not in e['themes'] for e in new if e['camp_dossier_slug']=='fosc-helsinki')
march=next(e for e in new if e['start']=='2027-03-25')
assert march['end']=='2027-03-29' and march['attendance_weekdays']==['MO','TU','WE','TH','FR'] and '25, 26 и 29' in march['title']
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert con.execute('PRAGMA foreign_key_check').fetchall()==[]
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2014
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==112
con.close()
def calendar(raw):
    text=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
    for chunk in text.split('BEGIN:VEVENT')[1:]:
        f={x.split(':',1)[0]:x.split(':',1)[1] for x in chunk.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert f['UID'] not in out
        out[f['UID']]=(f.get('DTSTART;VALUE=DATE',f.get('DTSTART')),f.get('DTEND;VALUE=DATE',f.get('DTEND')))
    return out
fn='dist/downloads/STEM_подтвержденные_даты.ics'
before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
removed=set(before)-set(now);added=set(now)-set(before)
assert len(removed)==12 and all(before[k][1][:8]<=d['asof'].replace('-','') for k in removed)
assert all(now[k]==v for k,v in before.items() if k in now)
assert len(added)==10 and len(now)==1379
assert 'stem-'+closed['id']+'@family-stem.local' not in now
assert all('stem-'+e['id']+'@family-stem.local' not in now for e in new if e['camp_dossier_slug']=='ranum-summer')
assert 'stem-'+march['id']+'@family-stem.local' in now
fn='dist/downloads/STEM_крупные_выставки.ics'
assert calendar((ROOT/fn).read_bytes())==calendar(oldfile(fn)) and len(calendar(oldfile(fn)))==104
audit=json.loads((ROOT/'data/europe-camp-audit-v61.json').read_text())
assert audit['worldwide_complete'] is False and audit['country_fully_audited'] is False
print(json.dumps(dict(prior_events_preserved=1997,prior_dossiers_preserved=102,new_dossiers=10,new_catalogue_dates=17,new_family_calendar_dates=10,expired_calendar_entries=12,dossiers=112,countries=27,swiss=18,source_urls=203,family_ical=1379,exhibition_ical=104,sqlite='ok',bridge='idempotent'),ensure_ascii=False))
