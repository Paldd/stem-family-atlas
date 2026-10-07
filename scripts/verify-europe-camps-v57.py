"""Regression/evidence checks for France/Spain expansion, preserving v56."""
import json,sqlite3,subprocess,datetime
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
BASE='d38c12e0925184c321fad139d1e2e1aaa2133eeb'
base=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());rows={e['id']:e for e in d['events']}
assert len(rows)==len(d['events'])==1952
assert all(rows[e['id']]==e for e in base['events'])
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==base[key],key
guide=d['camp_programmes'];profiles={p['slug']:p for p in guide['profiles']}
assert guide['counts']['dossiers']==len(profiles)==68
assert guide['counts']['countries']==19 and guide['counts']['swiss']==18
assert guide['counts']['source_urls']==122 and len(guide['generated_event_ids'])==158
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==guide
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[e for e in d['events'] if e['id'] not in {e['id'] for e in base['events']}]
assert len(new)==21
assert all(e['block']=='Лагеря' and e['iso']==['FRA'] and e['date_scope']=='day_camp_window' for e in new)
assert all(e['date_precision']=='published_session' and e['attendance_weekdays']==['MO','TU','WE','TH','FR'] for e in new)
assert all(datetime.date.fromisoformat(e['start']).weekday()==0 and datetime.date.fromisoformat(e['end']).weekday()==4 for e in new)
assert sum(e['camp_dossier_slug']=='ermitage-holiday' for e in new)==5
assert sum(e['camp_dossier_slug']=='wander-nature' for e in new)==7
ih=[e for e in new if e['camp_dossier_slug']=='ih-holiday'];assert len(ih)==9
same=[e for e in ih if e['start']=='2026-10-19'];assert {e['city'] for e in same}=={'Париж','Ницца','Биарриц'}
assert len({e['id'] for e in same})==3 and len({e['title'] for e in same})==3
assert all('€360' in e['cost'] if e['city']=='Биарриц' else '€340' in e['cost'] for e in ih)
assert not any(e['start'].startswith('2027-07') for e in ih) # live summer row still2026
assert not any(e['start'].startswith('2027-04') for e in new if e['camp_dossier_slug']=='wander-nature') # typo2017 rejected
assert all('Тариф 2027 ещё не опубликован' in e['cost'] for e in new if e['camp_dossier_slug']=='ermitage-holiday' and e['start'].startswith('2027'))
for slug in ['sotogrande-camps','kings-soto-camps','american-wizard','rockbotic-arganzuela']:
    assert profiles[slug]['price']['year']==2026 and profiles[slug]['timing']['sessions']==[]
for slug in ['tecs-puerto-kids','ilc']:
    assert profiles[slug]['price']['year'] is None and profiles[slug]['timing']['sessions']==[]
for slug in ['petits-atomes-tech','rockbotic-chamberi','rockbotic-arganzuela','kings-soto-camps']:
    assert profiles[slug]['confirmed_instruction_languages']==[]
assert profiles['american-wizard']['family_fit']['oscar']['status']=='later'
assert profiles['ih-holiday']['family_fit']['oscar']['status']=='later'
assert profiles['sotogrande-camps']['language_evidence_role']=='camp_life'
assert '4–5' in profiles['kings-soto-camps']['age'] and 'пансион с 8' in profiles['kings-soto-camps']['age']
assert 'не считаем эту cancellation fee авансом' in profiles['ilc']['price']['deposit']
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert con.execute('PRAGMA foreign_key_check').fetchall()==[]
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==1952
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==68
con.close()
def cal(raw):
    text=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
    for chunk in text.split('BEGIN:VEVENT')[1:]:
        f={x.split(':',1)[0]:x.split(':',1)[1] for x in chunk.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert f['UID'] not in out
        out[f['UID']]=(f.get('DTSTART;VALUE=DATE',f.get('DTSTART')),f.get('DTEND;VALUE=DATE',f.get('DTEND')))
    return out
fn='dist/downloads/STEM_подтвержденные_даты.ics'
old=cal(subprocess.check_output(['git','show',BASE+':'+fn],cwd=ROOT));now=cal((ROOT/fn).read_bytes())
assert all(now[uid]==pair for uid,pair in old.items())
assert len(now)==1336 and len(now)-len(old)==21
exhibitions='dist/downloads/STEM_крупные_выставки.ics'
assert cal((ROOT/exhibitions).read_bytes())==cal(subprocess.check_output(['git','show',BASE+':'+exhibitions],cwd=ROOT))
assert len(cal((ROOT/exhibitions).read_bytes()))==104
audit=json.loads((ROOT/'data/europe-camp-audit-v57.json').read_text())
assert audit['worldwide_complete'] is False and audit['new_calendar_entries']==21
print(json.dumps(dict(preserved_events=len(base['events']),new_calendar_entries=21,dossiers=68,swiss=18,countries=19,source_urls=122,multi_campus_ih=9,family_ical=len(now),sqlite='ok',bridge_idempotency='ok',worldwide_complete=False),ensure_ascii=False))
