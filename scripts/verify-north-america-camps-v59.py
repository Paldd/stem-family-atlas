"""Verify family decisions and preserve prior IDs/dates in the North America pass."""
import datetime,json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
BASE='ac9334d1a065239184effbe0ae66d5686126e457'
base=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());rows={e['id']:e for e in d['events']}
assert len(rows)==len(d['events'])==1986
changed=[]
for e in base['events']:
    now=rows[e['id']]
    assert (now['start'],now['end'])==(e['start'],e['end'])
    if now!=e:
        assert now['camp_dossier_slug'] in ['space-camp','space-robotics']
        keys={k for k in set(now)|set(e) if now.get(k)!=e.get(k)}
        allowed={'language','languages','language_mode','language_certainty','references','note'}
        if now['camp_dossier_slug']=='space-robotics':allowed|={'age','gear'}
        assert keys <= allowed,keys
        assert now['languages']==['EN'] and now['language_mode']=='primary'
        assert any('weeklong' in r['url'] for r in now['references'])
        changed.append(e['id'])
assert len(changed)==27
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==base[key],key
guide=d['camp_programmes'];profiles={p['slug']:p for p in guide['profiles']}
assert guide['counts']['dossiers']==len(profiles)==88
assert guide['counts']['countries']==19 and guide['counts']['swiss']==18
assert guide['counts']['source_urls']==159 and len(guide['generated_event_ids'])==192
old={p['slug']:p for p in base['camp_programmes']['profiles']}
assert all(profiles[s]['id']==p['id'] for s,p in old.items())
assert all(profiles[s]==p for s,p in old.items() if s not in ['id-tech','space-camp','space-robotics'])
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==guide
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[e for e in d['events'] if e['id'] not in {e['id'] for e in base['events']}]
assert len(new)==17 and all(e['block']=='Лагеря' for e in new)
assert all(e['languages']==[] and e['language_mode']=='unconfirmed' for e in new)
assert len([e for e in d['events'] if e['block']=='Лагеря'])==655
for slug in ['bricklabs-robotics','bricklabs-creative']:
    p=profiles[slug];assert '01.06.2027' in p['age'] and p['family_fit']['oscar']['status']=='later'
    matches=[e for e in new if e['camp_dossier_slug']==slug];assert len(matches)==2
    assert {(e['start'],e['end']) for e in matches}=={('2027-07-25','2027-07-30'),('2027-08-15','2027-08-20')}
assert 'robotics' not in profiles['bricklabs-creative']['themes']
assert all('robotics' not in e['themes'] for e in new if e['camp_dossier_slug']=='bricklabs-creative')
nextp=profiles['next-robotics'];assert 'сентябре 2027' in nextp['age'] and '$315' in nextp['price']['label']
assert '+2%' in nextp['price']['extras'] and 'Grades 4–7' in nextp['programme']
matches=[e for e in new if e['camp_dossier_slug']=='next-robotics'];assert len(matches)==3
assert all(e['date_scope']=='day_camp_window' and e['attendance_weekdays']==['MO','TU','WE','TH','FR'] for e in matches)
assert all(datetime.date.fromisoformat(e['start']).weekday()==0 and datetime.date.fromisoformat(e['end']).weekday()==4 for e in matches)
for slug in ['yres-sports-steam','yres-ai-robotics']:
    p=profiles[slug];assert p['timing']['precision']=='season_window'
    assert p['timing']['sessions']==[['2027-07-05','2027-08-13']]
    assert not any(e['camp_dossier_slug']==slug for e in new)
    assert 'TBD' in p['place'] and '$1 399' in p['price']['label']
    assert 'Card processing' in p['price']['extras'] and '30.09' in p['price']['deposit']
mini=profiles['arowhon-mini'];assert mini['family_fit']['matvey']['status']=='conditional'
assert '6–9' in mini['age'] and 'SK–Grade 3' in mini['age'] and 'CAD100' in mini['price']['extras']
assert 'не применяется' in mini['price']['deposit']
matches=[e for e in new if e['camp_dossier_slug']=='arowhon-regular'];assert len(matches)==6
assert len([e for e in matches if e.get('date_scope')=='programme_window_with_break'])==2
assert '27–29.07' in profiles['arowhon-regular']['accommodation'] and '+HST' in profiles['arowhon-regular']['price']['label']
cata=profiles['catalina-sea-junior'];assert cata['family_fit']['oscar']['status']=='later'
assert 'Fox Landing' in cata['accommodation'] and 'Toyon Bay' in cata['accommodation']
assert len([e for e in new if e['camp_dossier_slug']==cata['slug']])==3
for slug in ['lavner-lego','lavner-vex']:
    p=profiles[slug];assert p['timing']['sessions']==[] and p['price']['year']==2026
    assert 'Kindergarten' in p['age'] and 'USD79' in p['price']['label']
idp=profiles['id-tech'];assert idp['confirmed_instruction_languages']==['EN']
assert 'до 31 декабря' in idp['age'] and 'overnight' in idp['family_fit']['matvey']['detail']
assert 'до дня рождения' in idp['family_fit']['oscar']['detail']
assert 'требуется текущий или завершённый Grade 4' in profiles['space-robotics']['age']
assert 'RealFlight' in profiles['space-robotics']['programme']
assert any(g['provider'].startswith('Tamwood') for g in guide['gaps'])
assert not any('tamwood' in p['slug'] for p in guide['profiles'])
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert con.execute('PRAGMA foreign_key_check').fetchall()==[]
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==1986
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==88
con.close()
def cal(raw):
    text=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
    for chunk in text.split('BEGIN:VEVENT')[1:]:
        f={x.split(':',1)[0]:x.split(':',1)[1] for x in chunk.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert f['UID'] not in out
        out[f['UID']]=(f.get('DTSTART;VALUE=DATE',f.get('DTSTART')),f.get('DTEND;VALUE=DATE',f.get('DTEND')))
    return out
fn='dist/downloads/STEM_подтвержденные_даты.ics'
oldcal=cal(subprocess.check_output(['git','show',BASE+':'+fn],cwd=ROOT));now=cal((ROOT/fn).read_bytes())
assert all(now[uid]==pair for uid,pair in oldcal.items())
assert len(now)==1370 and len(now)-len(oldcal)==17
fn='dist/downloads/STEM_крупные_выставки.ics'
assert cal((ROOT/fn).read_bytes())==cal(subprocess.check_output(['git','show',BASE+':'+fn],cwd=ROOT))
assert len(cal((ROOT/fn).read_bytes()))==104
audit=json.loads((ROOT/'data/north-america-camp-audit-v59.json').read_text())
assert audit['worldwide_complete'] is False and audit['new_calendar_entries']==17
print(json.dumps(dict(prior_event_ids_dates_preserved=len(base['events']),prior_event_objects_unchanged=1942,corrected_prior_entries=27,new_calendar_entries=17,dossiers=88,swiss=18,countries=19,source_urls=159,family_ical=len(now),sqlite='ok',bridge_idempotency='ok',worldwide_complete=False),ensure_ascii=False))
