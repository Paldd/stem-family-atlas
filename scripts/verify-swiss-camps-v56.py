"""Verify new source-derived Swiss options and preservation of the prior release."""
import datetime,json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
base=json.loads(subprocess.check_output(['git','show','551caa626ae2a36f30e0b71c7d48358ba4e626be:data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());rows={e['id']:e for e in d['events']}
assert len(rows)==len(d['events'])==1931
assert all(rows[e['id']]==e for e in base['events'])
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==base[key],key
p=d['camp_programmes'];assert len(p['profiles'])==58 and p['counts']['swiss']==18
assert len(p['generated_event_ids'])==137 and p['counts']['source_urls']==96
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==p
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[e for e in d['events'] if e['id'] not in {e['id'] for e in base['events']}]
assert len(new)==40
jfk=[e for e in new if e['camp_dossier_slug']=='jfk-outdoor']
assert len(jfk)==31
assert sum(e['date_scope']=='day_camp_window' for e in jfk)==15
assert sum(e['date_scope']=='camp_session' for e in jfk)==15
opened=[e for e in jfk if e['date_scope']=='registration_open'];assert len(opened)==1 and opened[0]['start']==opened[0]['end']=='2026-11-02'
for e in jfk:
    if e['date_scope']=='registration_open':continue
    start=datetime.date.fromisoformat(e['start']);end=datetime.date.fromisoformat(e['end'])
    assert e['date_precision']=='published_rule' and e['date_rule']
    if e['date_scope']=='day_camp_window':
        assert start.weekday()==0 and end.weekday()==4
        assert e['attendance_weekdays']==['MO','TU','WE','TH','FR']
        assert e['participation']=='day_camp'
    else:assert start.weekday()==end.weekday()==6 and e['participation']=='residential'
assert 'CHF 5,400' in rows['CP058-20270705-20270716']['cost']
assert 'CHF 8,100' in rows['CP058-20270712-20270730']['cost']
assert 'CHF 6,600' in rows['CP058-20270704-20270718']['cost']
assert 'CHF 9,900' in rows['CP058-20270704-20270725']['cost']
assert all(not e['languages'] and e['language_mode']=='unconfirmed' for e in jfk)
labs=[e for e in new if e['camp_dossier_slug']=='regent-labs'];assert len(labs)==3
assert all(e['age'].startswith('8–14') and e['mat'].startswith('Да') and e['osc'].startswith('Нет') and e['language_mode']=='camp_life' for e in labs)
assert sum(e['priority'].startswith('P4') for e in new)==6
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert con.execute('PRAGMA foreign_key_check').fetchall()==[]
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==1931
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==58
con.close()
def cal(raw):
    text=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
    for chunk in text.split('BEGIN:VEVENT')[1:]:
        f={x.split(':',1)[0]:x.split(':',1)[1] for x in chunk.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert f['UID'] not in out
        out[f['UID']]=(f.get('DTSTART;VALUE=DATE',f.get('DTSTART')),f.get('DTEND;VALUE=DATE',f.get('DTEND')))
    return out
fn='dist/downloads/STEM_подтвержденные_даты.ics'
old=cal(subprocess.check_output(['git','show','551caa626ae2a36f30e0b71c7d48358ba4e626be:'+fn],cwd=ROOT));now=cal((ROOT/fn).read_bytes())
assert all(now[uid]==pair for uid,pair in old.items())
assert len(now)==1315 and len(now)-len(old)==34
raw=(ROOT/fn).read_text().replace('\n ','')
assert '[Окно дневного лагеря · Пн–Пт]' in raw
print(json.dumps(dict(preserved_events=len(base['events']),new_events=40,dossiers=58,swiss_programmes=18,jfk_variants=30,registration_open=opened[0]['start'],family_calendar_entries=len(now),new_family_entries=34,sqlite='ok',bridge_idempotency='ok'),ensure_ascii=False))
