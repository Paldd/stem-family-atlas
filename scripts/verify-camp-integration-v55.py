"""Verify canonical records, relational exports and stable existing calendar IDs."""
import datetime, json, sqlite3, subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'data/catalog.json').read_text())
baseline=json.loads(subprocess.check_output(['git','show','70a55ab2df74813d1cc95df53accac06fcacf9d3:data/catalog.json'],cwd=ROOT))
rows={e['id']:e for e in catalog['events']}
assert len(rows)==len(catalog['events'])
assert all(rows[e['id']]==e for e in baseline['events'])
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert catalog[key]==baseline[key],key
programmes=catalog['camp_programmes']
assert len(programmes['profiles'])>=54
assert len({p['iso'] for p in programmes['profiles']})>=19
assert sum(p['iso']=='CHE' for p in programmes['profiles'])>=14
assert len(programmes['generated_event_ids'])>=97
assert sum(rows[i]['camp_dossier_slug']=='les-elfes' for i in programmes['generated_event_ids'])==26
assert sum(rows[i]['camp_dossier_slug']=='le-rosey' for i in programmes['generated_event_ids'])==7
assert rows['CP001-20261212-20261219']['cost'].startswith('2026/27 · CHF 2,600')
assert rows['CP001-20270516-20270529']['city']=='Zermatt / Verbier'
assert rows['CP001-20261212-20261219']['osc'].startswith('Условно')
assert rows['CP001-20261212-20261219']['mat'].startswith('Да')
assert rows['CP001-20261212-20261219']['language_mode']=='camp_life'
assert '13,200' in rows['CP009-20270704-20270723']['cost']
assert len({(x['programme_id'],x['event_id']) for x in programmes['event_links']})==len(programmes['event_links'])
public=json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())
assert public==programmes
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==catalog
again=json.loads(json.dumps(catalog))
integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()))
assert again==catalog,'Bridge must be idempotent'
for e in catalog['events']:
    if e.get('camp_dossier_slug') in {'les-elfes','la-garenne','tasis','le-rosey','village-leysin'}:
        assert not {'robotics','coding','ai'}&set(e['themes']),'Optional workshops must not tag the general stay'
assert all(rows[i]['participation']=='residential' for i in programmes['generated_event_ids'] if rows[i]['camp_dossier_slug']=='family-aviation')
assert not any(e.get('camp_dossier_slug') in {'prefleuri','montana-zug','aiglon','rosenberg','newtonshow','ilsc-ubc'} for e in catalog['events'])
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert con.execute('PRAGMA foreign_key_check').fetchall()==[]
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==len(catalog['events'])
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==len(programmes['profiles'])
assert con.execute('SELECT COUNT(*) FROM camp_programme_events').fetchone()[0]==len(programmes['event_links'])
for pid,payload in con.execute('SELECT id,record_json FROM camp_programmes'):
    assert json.loads(payload)==next(p for p in programmes['profiles'] if p['id']==pid)
con.close()

def calendar(raw):
    text=raw.decode().replace('\r\n ','').replace('\r\n\t','')
    result={}
    for chunk in text.split('BEGIN:VEVENT')[1:]:
        fields={line.split(':',1)[0]:line.split(':',1)[1] for line in chunk.split('END:VEVENT')[0].strip().splitlines() if ':' in line}
        uid=fields['UID'];assert uid not in result
        result[uid]=(fields.get('DTSTART;VALUE=DATE',fields.get('DTSTART')),fields.get('DTEND;VALUE=DATE',fields.get('DTEND')))
    return result
fn='dist/downloads/STEM_подтвержденные_даты.ics'
oldcal=calendar(subprocess.check_output(['git','show','70a55ab2df74813d1cc95df53accac06fcacf9d3:'+fn],cwd=ROOT))
newcal=calendar((ROOT/fn).read_bytes())
for uid,dates in oldcal.items():
    if dates[1][:8]>catalog['asof'].replace('-',''):
        assert newcal.get(uid)==dates,(uid,dates,newcal.get(uid))
for eid in programmes['generated_event_ids']:
    e=rows[eid];uid='stem-'+eid+'@family-stem.local'
    excluded=e['priority'].startswith('P4') or (e['mat'].startswith('Нет') and e['osc'].startswith('Нет'))
    if excluded:assert uid not in newcal
    else:
        assert newcal[uid]==(e['start'].replace('-',''),(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d'))
print(json.dumps(dict(original_events_preserved=len(baseline['events']),dossiers=len(programmes['profiles']),countries=len({p['iso'] for p in programmes['profiles']}),new_sessions=len(programmes['generated_event_ids']),sqlite_foreign_keys='ok',bridge_idempotency='ok',family_calendar_entries=len(newcal),new_family_entries=sum('stem-'+i+'@family-stem.local' in newcal for i in programmes['generated_event_ids'])),ensure_ascii=False))
