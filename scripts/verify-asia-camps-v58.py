"""Evidence and preservation checks for the Asian holiday programme pass."""
import datetime,json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
BASE='6f7a32bc471a41dc5323b2fe1031acc169afe11c'
base=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());rows={e['id']:e for e in d['events']}
assert len(rows)==len(d['events'])==1969
assert all(rows[e['id']]==e for e in base['events'])
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==base[key],key
guide=d['camp_programmes'];profiles={p['slug']:p for p in guide['profiles']}
assert guide['counts']['dossiers']==len(profiles)==78
assert guide['counts']['countries']==19 and guide['counts']['swiss']==18
assert guide['counts']['source_urls']==140 and len(guide['generated_event_ids'])==175
old={p['slug']:p for p in base['camp_programmes']['profiles']}
assert all(profiles[s]['id']==p['id'] for s,p in old.items())
assert all(profiles[s]==p for s,p in old.items() if s not in ['camp-taiwan','camp-sfs'])
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==guide
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[e for e in d['events'] if e['id'] not in {e['id'] for e in base['events']}]
assert len(new)==17 and all(e['block']=='Лагеря' for e in new)
asia=[e for e in new if e['camp_dossier_slug']=='campasia-robotics'];assert len(asia)==1
assert asia[0]['start']=='2026-10-19' and asia[0]['age']=='6–8' and 'Нет сейчас' in asia[0]['mat']
assert asia[0]['languages']==[] and asia[0]['language_mode']=='unconfirmed'
for slug in ['campasia-coding','campasia-electronics','campasia-stem','camp-taiwan-family','camping-taiwan','hakuba-summer']:
    assert profiles[slug]['timing']['sessions']==[]
for slug in ['lccl-early','lccl-fundamentals']:
    matches=[e for e in new if e['camp_dossier_slug']==slug];assert len(matches)==7
    assert all(e['date_scope']=='day_camp_window' and e['attendance_weekdays']==['MO','TU','WE','TH','FR'] for e in matches)
    assert all(datetime.date.fromisoformat(e['start']).weekday()==0 and datetime.date.fromisoformat(e['end']).weekday()==4 for e in matches)
    assert all(e['languages']==[] and e['language_mode']=='unconfirmed' for e in matches)
    assert 'портал' in profiles[slug]['age']
assert profiles['lccl-early']['family_fit']['matvey']['status']=='later'
assert 'Grade 1' in profiles['camping-taiwan']['age'] and profiles['camping-taiwan']['language_evidence_role']=='camp_life'
assert profiles['camp-taiwan-family']['formats']==['family'] and profiles['camp-taiwan-family']['confirmed_instruction_languages']==[]
assert '40' in profiles['camp-taiwan-family']['programme'] and '17–18' in profiles['camp-taiwan-family']['timing']['label']
assert 'классы 6–9' in profiles['hakuba-summer']['age'] and profiles['hakuba-summer']['price']['year']==2026
assert all(f['status']=='later' for f in profiles['hakuba-summer']['family_fit'].values())
ea=profiles['english-adventure-winter'];assert '01.04.2020' in ea['family_fit']['oscar']['detail']
assert ea['confirmed_instruction_languages']==['EN'] and ea['language_evidence_role']=='camp_life'
matches=[e for e in new if e['camp_dossier_slug']==ea['slug']];assert len(matches)==2
assert {(e['start'],e['end']) for e in matches}=={('2026-12-26','2026-12-30'),('2027-01-03','2027-01-06')}
assert all(e['participation']=='residential' and e['language_mode']=='camp_life' for e in matches)
assert profiles['camp-taiwan']['formats']==['boarding'] and 'братья' in profiles['camp-taiwan']['accommodation']
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert con.execute('PRAGMA foreign_key_check').fetchall()==[]
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==1969
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==78
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
assert len(now)==1353 and len(now)-len(oldcal)==17
fn='dist/downloads/STEM_крупные_выставки.ics'
assert cal((ROOT/fn).read_bytes())==cal(subprocess.check_output(['git','show',BASE+':'+fn],cwd=ROOT))
assert len(cal((ROOT/fn).read_bytes()))==104
audit=json.loads((ROOT/'data/asia-camp-audit-v58.json').read_text())
assert audit['worldwide_complete'] is False and audit['new_calendar_entries']==17
print(json.dumps(dict(preserved_events=len(base['events']),new_calendar_entries=17,dossiers=78,swiss=18,countries=19,source_urls=140,family_ical=len(now),sqlite='ok',bridge_idempotency='ok',worldwide_complete=False),ensure_ascii=False))
