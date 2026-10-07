"""Preserve the atlas while checking camp language, dates, price and access gates."""
import json, sqlite3, subprocess
from pathlib import Path
from camp_catalog_bridge import integrate

ROOT=Path(__file__).resolve().parents[1]
BASE='ca1ab59c19e3bfb056d1449712f64da54ce035f9'
base=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text())
rows={e['id']:e for e in d['events']}
assert len(rows)==len(d['events'])==1997
assert all(rows[e['id']]==e for e in base['events'])
for key in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[key]==base[key],key
guide=d['camp_programmes']; profiles={p['slug']:p for p in guide['profiles']}
assert len(profiles)==guide['counts']['dossiers']==102
assert guide['counts']['countries']==20 and guide['counts']['swiss']==18
assert guide['counts']['source_urls']==182 and len(guide['generated_event_ids'])==203
old={p['slug']:p for p in base['camp_programmes']['profiles']}
assert all(profiles[s]==p for s,p in old.items())
assert len(profiles.keys()-old.keys())==14
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==guide
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
again=json.loads(json.dumps(d))
integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()))
assert again==d
new=[e for e in d['events'] if e['id'] not in {e['id'] for e in base['events']}]
assert len(new)==11 and all(e['block']=='Лагеря' and e['start']>='2027-01-01' for e in new)
assert sum(e['block']=='Лагеря' for e in d['events'])==666
for slug, count in [('ojo-ciego',1),('pellines-pioneros',1),('pellines-exploradores',2),('pellines-aventureros',2),('las-mulas',4),('english-camp-brazil-kids',1)]:
    assert sum(e['camp_dossier_slug']==slug for e in new)==count
for e in new:
    if e['camp_dossier_slug'] in ['las-mulas','english-camp-brazil-kids']:
        assert e['language_mode']=='camp_life' and e['languages']
    else: assert e['languages']==[] and e['language_mode']=='unconfirmed'
    assert 'robotics' not in e['themes'] and 'ai' not in e['themes']
cenfo=profiles['cenfotec-makers']
assert all(cenfo['family_fit'][k]['status']=='later' for k in ['matvey','oscar'])
assert 'USD 183.60' in cenfo['price']['label'] and cenfo['timing']['sessions']==[['2026-12-07','2026-12-11']]
assert any(x['kind']=='existing_programme' and x['event_ids']==['L139'] for x in cenfo['calendar_links'])
assert profiles['mount-view-camps']['family_fit']['matvey']['status']=='later'
assert 'robotics' not in profiles['conversa-flex']['themes'] and 'robotics' in profiles['conversa-tech']['themes']
assert profiles['conversa-flex']['price']['year']==2026 and profiles['conversa-tech']['price']['year']==2026
assert profiles['ojo-ciego']['timing']['sessions']==[['2027-07-18','2027-07-31']]
assert '20 550' in profiles['ojo-ciego']['price']['label'] and '18 000' not in profiles['ojo-ciego']['price']['label']
assert profiles['ojo-ciego']['family_fit']['oscar']['status']=='conditional'
assert profiles['rancho-aventura']['timing']['sessions']==[] and profiles['rancho-aventura']['price']['year'] is None
assert profiles['liota-winter']['timing']['sessions']==[] and not profiles['liota-winter']['confirmed_instruction_languages']
assert all(profiles['liota-winter']['family_fit'][k]['status']=='unknown' for k in ['matvey','oscar'])
assert profiles['las-mulas']['confirmed_instruction_languages']==['EN','ES']
assert profiles['las-mulas']['price']['year'] is None and 'FAQ 2026' in profiles['las-mulas']['price']['deposit']
ec=profiles['english-camp-brazil-kids']
assert ec['price']['year']==2027 and '4 772' in ec['price']['label'] and '4 295' in ec['price']['label']
assert ec['family_fit']['oscar']['status']=='later' and '12–16' in ec['age']
assert ec['confirmed_instruction_languages']==['EN'] and ec['language_evidence_role']=='camp_life'
assert profiles['campo-aventuras']['availability']['status']=='closed'
assert profiles['campo-aventuras']['timing']['sessions']==[]
assert any(g['provider'].startswith('NR') for g in guide['gaps'])
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert con.execute('PRAGMA foreign_key_check').fetchall()==[]
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==1997
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==102
con.close()
def calendar(raw):
    text=raw.decode().replace('\r\n ','').replace('\r\n\t',''); out={}
    for chunk in text.split('BEGIN:VEVENT')[1:]:
        f={x.split(':',1)[0]:x.split(':',1)[1] for x in chunk.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert f['UID'] not in out
        out[f['UID']]=(f.get('DTSTART;VALUE=DATE',f.get('DTSTART')),f.get('DTEND;VALUE=DATE',f.get('DTEND')))
    return out
fn='dist/downloads/STEM_подтвержденные_даты.ics'
oldcal=calendar(subprocess.check_output(['git','show',BASE+':'+fn],cwd=ROOT)); now=calendar((ROOT/fn).read_bytes())
assert all(now[uid]==pair for uid,pair in oldcal.items())
assert len(now)==1381 and len(now)-len(oldcal)==11
fn='dist/downloads/STEM_крупные_выставки.ics'
assert calendar((ROOT/fn).read_bytes())==calendar(subprocess.check_output(['git','show',BASE+':'+fn],cwd=ROOT))
assert len(calendar((ROOT/fn).read_bytes()))==104
audit=json.loads((ROOT/'data/latam-camp-audit-v60.json').read_text())
assert audit['worldwide_complete'] is False and audit['new_calendar_entries']==11
print(json.dumps(dict(prior_event_objects_preserved=1986,prior_dossiers_preserved=88,new_dossiers=14,new_calendar_entries=11,dossiers=102,countries=20,swiss=18,source_urls=182,family_ical=1381,sqlite='ok',bridge='idempotent',worldwide_complete=False),ensure_ascii=False))
