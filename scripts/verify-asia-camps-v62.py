"""Guard catalogue preservation, age/price evidence and exact calendar reuse."""
import json,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
BASE='5637ec4aa5d307cf8f42b739a81c0c78e830984c'
def oldfile(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
b=json.loads(oldfile('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};rows={e['id']:e for e in d['events']}
assert len(rows)==len(d['events'])==2041
assert all(rows[k]==v for k,v in old.items())
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[k]==b[k],k
g=d['camp_programmes'];p={x['slug']:x for x in g['profiles']};oldp={x['slug']:x for x in b['camp_programmes']['profiles']}
assert all(p[k]==v for k,v in oldp.items())
assert len(p)==125 and len(p.keys()-oldp.keys())==13
assert g['counts']['countries']==28 and g['counts']['swiss']==18 and g['counts']['source_urls']==231
assert len(g['generated_event_ids'])==247 and g['integration']['reused_legacy_events']==28
assert sum(e['block']=='Лагеря' for e in rows.values())==710
assert json.loads((ROOT/'dist/downloads/STEM_database.json').read_text())==d
assert json.loads((ROOT/'dist/downloads/STEM_camp_programmes_deep_2026_2027.json').read_text())==g
again=json.loads(json.dumps(d));integrate(again,json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text()));assert again==d
new=[e for e in rows.values() if e['id'] not in old]
assert len(new)==27 and all(e['checked']=='2026-10-05' and e['block']=='Лагеря' for e in new)
for key in ['apprentice','junior','senior','spike','ai']:
    q=p['worklab-'+key];assert q['confirmed_instruction_languages']==['EN']
    assert len(q['calendar_links'])==4 and all(x['kind']=='existing_programme' for x in q['calendar_links'])
    assert len(q['related_event_ids'])==4 and q['price']['year']==2026
    assert not any(e.get('camp_dossier_slug')==q['slug'] for e in new)
assert p['worklab-apprentice']['family_fit']['matvey']['status']=='not_eligible'
assert '7.5' in p['worklab-ai']['age'] and p['worklab-ai']['family_fit']['oscar']['status']=='later'
assert '9–13' in p['worklab-senior']['age'] and '9+' in p['worklab-senior']['age']
assert 'Shaw Centre' not in p['worklab-spike']['place']
assert len(p['lighthouse-winter']['timing']['sessions'])==4
assert len([e for e in new if e['camp_dossier_slug']=='lighthouse-winter'])==4
assert 'VEX IQ' in p['lighthouse-winter']['programme'] and 'не указан' in p['lighthouse-winter']['programme']
assert '10–14' in p['lighthouse-vexiq']['age'] and p['lighthouse-vexiq']['timing']['sessions']==[]
assert p['lighthouse-junior']['timing']['sessions']==p['lighthouse-vexgo']['timing']['sessions']==[]
assert 'возвратный залог' in p['lighthouse-winter']['price']['extras']
assert '22 500' in p['lighthouse-winter']['price']['label'] and '16 000' in p['lighthouse-winter']['price']['label']
el=p['elev8-tokyo'];assert len(el['timing']['sessions'])==23 and el['confirmed_instruction_languages']==['EN']
assert el['timing']['sessions'][-1]==['2027-05-03','2027-05-07']
assert round(109250*1.1)==120175 and round(23000*1.1)==25300 and round(23000*4*1.1)==101200
assert '120 175' in el['price']['label'] and 'Билеты общественного транспорта' in el['price']['extras']
assert '24 часа' in el['price']['deposit'] and '21+' in el['price']['deposit']
assert all(e['attendance_weekdays']==['MO','TU','WE','TH','FR'] for e in new)
dw=p['dwight-seoul-junior'];assert dw['price']['year']==2025 and dw['timing']['sessions']==[] and dw['confirmed_instruction_languages']==[]
assert 'Робототехнические и AI-модули' in dw['programme'] and '2024' in dw['price']['deposit']
for k in ['bisp-main','bisp-lower']:
    assert p[k]['confirmed_instruction_languages']==['EN'] and p[k]['price']['year']==2026 and not p[k]['timing']['sessions']
assert p['bisp-lower']['formats']==['day'] and p['bisp-lower']['family_fit']['matvey']['status']=='not_eligible'
assert p['bisp-main']['formats']==['day','boarding'] and 'older than 9' in p['bisp-main']['age']
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2041
assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==125
con.close()
def calendar(raw):
    t=raw.decode().replace('\r\n ','').replace('\r\n\t','');out={}
    for ch in t.split('BEGIN:VEVENT')[1:]:
        f={x.split(':',1)[0]:x.split(':',1)[1] for x in ch.split('END:VEVENT')[0].splitlines() if ':' in x}
        assert f['UID'] not in out
        out[f['UID']]=(f.get('DTSTART;VALUE=DATE',f.get('DTSTART')),f.get('DTEND;VALUE=DATE',f.get('DTEND')))
    return out
fn='dist/downloads/STEM_подтвержденные_даты.ics';before=calendar(oldfile(fn));now=calendar((ROOT/fn).read_bytes())
assert all(now.get(k)==v for k,v in before.items()) and len(now)==1406 and len(set(now)-set(before))==27
assert all('stem-'+e['id']+'@family-stem.local' in now for e in new)
fn='dist/downloads/STEM_крупные_выставки.ics';assert calendar((ROOT/fn).read_bytes())==calendar(oldfile(fn))
assert len(calendar(oldfile(fn)))==104
print(json.dumps(dict(prior_events_preserved=2014,prior_dossiers_preserved=112,new_dossiers=13,new_catalogue_dates=27,reused_worklab_dates=20,dossiers=125,countries=28,swiss=18,source_urls=231,family_ical=1406,exhibition_ical=104,sqlite='ok',bridge='idempotent'),ensure_ascii=False))
