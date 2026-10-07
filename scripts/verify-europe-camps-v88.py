"""Independent source, season boundaries and authorised correction/preservation checks."""
import hashlib,json,re,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v88'
BASE='2d76829dc5390385a77c0192084e000c482b9082'
NODE='/Users/pal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
def before(file):return subprocess.check_output(['git','show',BASE+':'+file],cwd=ROOT)
def raw(k):return (PRIMARY/(k+'.txt')).read_text()
def compact(s):return re.sub(r'\s+','',s)
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};events={e['id']:e for e in d['events']}
assert len(old)==2975 and len(events)==len(d['events'])==2997 and set(old)<=set(events)
changed={k for k,v in old.items() if events[k]!=v};assert len(changed)==35
updated={'le-rosey','les-elfes','tasis'}
assert {events[k].get('camp_dossier_slug') for k in changed}==updated
for k,v in old.items():
    if k in changed:
        assert events[k]['start']==v['start'] and events[k]['end']==v['end']
        assert events[k]['title']==v['title'] and events[k]['country']==v['country']
    else:assert events[k]==v
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:assert d[k]==b[k],k
c=d['camp_programmes'];p={q['slug']:q for q in c['profiles']};op={q['slug']:q for q in b['camp_programmes']['profiles']}
assert len(op)==529 and len(p)==547 and len(p)==len(c['profiles'])
assert [q['id'] for q in c['profiles'][:529]]==[q['id'] for q in b['camp_programmes']['profiles']]
for slug,q in op.items():
    if slug not in updated:assert p[slug]==q,slug
    else:
        assert p[slug]['id']==q['id'] and p[slug]['timing']['sessions']==q['timing']['sessions']
        assert p[slug]['related_event_ids']==q['related_event_ids'] and p[slug]['calendar_links']==q['calendar_links']
assert c['counts']['countries']==36 and c['counts']['source_urls']==829 and c['counts']['swiss']==84
assert len(c['shortlist'])==119 and c['shortlist'][:115]==b['camp_programmes']['shortlist']
assert c['gaps'][:-4]==b['camp_programmes']['gaps']
assert all(len(s['slugs'])==len(set(s['slugs'])) and all(k in p for k in s['slugs']) for s in c['shortlist'][-4:])
new=[e for k,e in events.items() if k not in old]
assert len(new)==22 and sum(e['block']=='Лагеря' for e in events.values())==1666
assert len(c['generated_event_ids'])==1203 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==35
fresh={k:q for k,q in p.items() if k not in op}
assert len(fresh)==18 and [q['id'] for q in fresh.values()]==['CP%03d'%i for i in range(530,548)]
assert {k:sum(q['iso']==k for q in fresh.values()) for k in ['CHE','FRA','ESP','KEN']}==dict(CHE=6,FRA=7,ESP=4,KEN=1)
# Le Rosey curriculum, precise age and contract year, rather than brand guesses.
t=raw('rosey-classic');assert 'From 11 to 15 years old\nTECH & ROBOTICS' in t
assert '75' in t and 'Maximum 20 students' in t and 'LEGO League' in t
assert 'Both English and French are used daily' in raw('rosey-faq')
assert 'no English lessons' in compact(raw('rosey-mountain')).replace('noEnglishlessons','no English lessons')
financial=raw('rosey-financial-layout');assert 'SUMMER 2026' in financial and 'May, 2026' in financial and '70%' in financial
assert p['le-rosey']['confirmed_instruction_languages']==['EN','FR'] and p['le-rosey']['language_evidence_role']=='camp_life'
assert '11–15' in p['le-rosey']['programme'] and '1 мая 2027' in p['le-rosey']['price']['deposit']
assert p['le-rosey']['family_fit']['matvey']['status']=='conditional' and p['le-rosey']['family_fit']['oscar']['status']=='later'
assert len(p['le-rosey']['timing']['sessions'])==7
assert all(x in p['le-rosey']['price']['label'] for x in ['13 200','13 500'])
assert '2,5' in p['le-rosey']['programme'] and '2, 5' not in p['le-rosey']['programme']
# Parse future TASIS dates independently from the primary fee page.
t=raw('rosey-cde-check');assert 'Sunday, June 27–Saturday, July 17, 2027' in t and 'Monday, July 19–Sunday,\xa0August 8, 2027' in t
assert t.count('CHF 9,200')==3 and t.count('CHF 5,100')==2
assert t.count('weekend day trips are no longer offered for Day students')==2
faq=raw('tasis-faq');assert 'do not allow siblings or friends to room together' in faq
assert 'Day students\nmust provide their own health' in faq and 'CHF 1500' in faq and 'May 15' in faq
assert 'not refundable at any time' in faq
for slug in ['tasis-msp-day','tasis-msp-board','tasis-hsp-day','tasis-hsp-board']:
    q=p[slug];assert q['confirmed_instruction_languages']==['EN'] and q['language_evidence_role']=='language_lessons'
    assert all(v['status']=='later' for v in q['family_fit'].values())
    rows=[e for e in new if e['camp_dossier_slug']==slug]
    assert {(e['start'],e['end']) for e in rows}=={('2027-06-27','2027-07-17'),('2027-07-19','2027-08-08')}
    assert all(e['language_mode']=='language_lessons' for e in rows)
    assert all('attendance_weekdays' not in e for e in rows)
assert 'one primary academic course' in raw('tasis-msp') and 'Students must bring a laptop' in raw('tasis-hsp') and 'Tableau' in raw('tasis-hsp')
# Winter day and boarding have different ages, insurance/deposit/fee and refund clauses.
wd=raw('leselfes-day-pdf-layout');wb=raw('leselfes-winter-pdf-layout')
assert 'WINTER DAY CAMP 2026-2027' in wd and 'CHF 200' in wd and 'CHF 25.- per day' in wd and '60 days' in wd and 'From 29 days' in wd
assert '8 to 17' in raw('leselfes-day') and 'Saturdays' in wd
assert 'English is the main language' in raw('leselfes-faq')
assert all(x in compact(wb) for x in ['2\'300.-','150.-','120.-','15.-','CHF500perweek','CHF1,000'])
assert 'ES' not in p['les-elfes-winter-day']['confirmed_instruction_languages']
assert p['les-elfes-winter-day']['family_fit']['oscar']['status']=='later' and not p['les-elfes-winter-day']['timing']['sessions']
assert 350+25+3==378 and 450+25+3==478
assert '378/478' in compact(p['les-elfes-winter-day']['price']['label'])
april=next(v for v in p['les-elfes']['timing']['session_details'] if v['start']=='2027-04-10')
assert april['price']==next(v for v in op['les-elfes']['timing']['session_details'] if v['start']=='2027-04-10')['price']
assert 'AprilI2300' not in json.dumps(c['gaps'][-4:])
# Kenya is the actual destination; no inferred teaching language or month/year repairs.
ch=raw('rosey-chyulu');assert 'CHF 5300' in ch and 'CHF 5,500' in ch and 'July 17 – July 24 2027' in ch and 'July 23 – July 30 2027' in ch
assert 'DAY SEVEN' in raw('rosey-chyulu-sample-layout') and 'DAY EIGHT' not in raw('rosey-chyulu-sample-layout')
assert p['rosey-chyulu-kenya']['iso']=='KEN' and p['rosey-chyulu-kenya']['confirmed_instruction_languages']==[]
assert all(v['status']=='later' for v in p['rosey-chyulu-kenya']['family_fit'].values())
assert {(e['start'],e['end']) for e in new if e['camp_dossier_slug']=='rosey-chyulu-kenya'}=={('2027-07-17','2027-07-24'),('2027-07-23','2027-07-30')}
# Full YIRA PDF independently proves student-run association and conflicting prior deadline.
y=raw('ics-yira-public-file-layout');assert 'student-run' in y and '20th April 2026' in y and 'Grades 6–12' in y
assert '15th June\xa02026' in raw('ics-paris')
assert 'CertificateofParticipation' in compact(raw('ics-ai-pdf-layout'))
assert '100% English' in raw('ics-camp-pdf-layout')
for slug in ['ics-paris-ai-startup','ics-paris-yira-leaders']:
    assert all(v['status']=='unknown' for v in p[slug]['family_fit'].values()) and p[slug]['confirmed_instruction_languages']==[]
    assert not p[slug]['timing']['sessions']
assert '£465' in raw('ics-paris') and '€465' in raw('ics-paris')
# Upcoming ALCNY campus/weekday matrix: ASP only first week, siblings' exact birthday unknown.
t=raw('alcny-camps-2026');assert 'October 19–30' in t and 'AVAILABLE WEEK 1 ONLY' in t and 'full English immersion' in t
assert '€695 per child' in t and '€720 per child' in t and '€9 per day' in t
junior=[e for e in new if e['camp_dossier_slug']=='alcny-paris-autumn-junior'];teen=[e for e in new if e['camp_dossier_slug']=='alcny-paris-autumn-teens']
assert len(junior)==7 and len(teen)==4
assert {(v['variant_key'],v['start'],v['end']) for v in p['alcny-paris-autumn-junior']['timing']['session_details']}=={
    (camp+'-week'+str(i),a,z) for camp in ['lennen','concordia','chardin','asp'] for i,a,z in [(1,'2026-10-19','2026-10-23'),(2,'2026-10-26','2026-10-30')] if not(camp=='asp' and i==2)}
assert all(e['languages']==['EN'] and e['attendance_weekdays']==['MO','TU','WE','TH','FR'] and e['date_scope']=='day_camp_window' for e in junior+teen)
assert all(v['status']=='later' for v in p['alcny-paris-autumn-teens']['family_fit'].values())
assert '695' not in p['alcny-paris-autumn-teens']['price']['label'].split('Младшая')[0] and 'не раскрыт' in p['alcny-paris-autumn-teens']['price']['label']
assert '2024–25 holiday camp fee schedule' in raw('asp-holiday') and '€725' in raw('asp-holiday') and not p['asp-paris-holiday-english']['timing']['sessions']
# Language/camp-year evidence is explicit, never promoted from an English website.
t=raw('agora-granada');assert 'English part and a Spanish part' in t and 'from 9 to 14 years' in t
assert p['agora-granada-creative-immersion']['confirmed_instruction_languages']==['EN','ES']
assert p['agora-granada-robotics-vr']['confirmed_instruction_languages']==[]
assert all(not p[s]['timing']['sessions'] and p[s]['price']['year'] is None for s in fresh if s.startswith('agora-granada-'))
rob=raw('robbo-web-primary');assert '6 a 8 y 9 a 13' in rob and 'martes 24 de junio' in rob and '185€' in rob
assert p['robbo-barcelona-summer']['confirmed_instruction_languages']==[] and not p['robbo-barcelona-summer']['timing']['sessions']
assert 'Mayo de 2026' in raw('robbo-current-terms') and '48 horas' in raw('robbo-current-terms')
assert p['robbo-barcelona-summer']['timing']['status']=='published_2026'
# Public data and independent database/calendar preservation.
report=json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text());again=json.loads(json.dumps(d));integrate(again,report);assert again==d
for file,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:assert json.loads((ROOT/'dist/downloads'/file).read_text())==wanted
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite');assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2997 and con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==547;con.close()
def calendar(v):
    out={};t=v.decode().replace('\r\n ','').replace('\r\n\t','')
    for ch in t.split('BEGIN:VEVENT')[1:]:
        f={l.split(':',1)[0]:l.split(':',1)[1] for l in ch.split('END:VEVENT')[0].splitlines() if ':' in l};assert f['UID'] not in out;out[f['UID']]=f
    return out
for file,total,previous in [('STEM_подтвержденные_даты.ics',2256,2249),('STEM_крупные_выставки.ics',104,104)]:
    f='dist/downloads/'+file;prior=calendar(before(f));now=calendar((ROOT/f).read_bytes());assert len(prior)==previous and len(now)==total and set(prior)<=set(now)
    for uid,v in prior.items():
        olddates={k:x for k,x in v.items() if k.startswith('DTSTART') or k.startswith('DTEND')}
        newdates={k:x for k,x in now[uid].items() if k.startswith('DTSTART') or k.startswith('DTEND')}
        assert olddates and newdates==olddates
        eid=uid.removeprefix('stem-').removesuffix('@family-stem.local')
        if eid not in changed:assert {k:x for k,x in now[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'},uid
    if total==2256:
        assert set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in junior}
        assert all('stem-'+e['id']+'@family-stem.local' not in now for e in teen+[e for e in new if e['start'].startswith('2027')])
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==88
assert {q['id'] for q in bp['requirements']}<={q['id'] for q in plan['requirements']}
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert plan['camp_catalog_integration']['dossiers']==547 and d['coverage_summary']['fully_audited_countries']==0
for stem in ['europe-camp-audit-v88','europe-camp-source-receipts-v88']:
    v=json.loads((ROOT/'data'/f'{stem}.json').read_text());assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==v
    assert not any(v['external_actions'].values())
    if 'sources' in v:
        assert len(v['sources'])==39 and sum(q.get('status')==200 for q in v['sources'])==37
        assert len(v['visual_primary_reads'])==10 and len(v['web_primary_reads'])==1 and len(v['dossier_source_urls_added'])==25
        for q in v['sources']:
            if q.get('status')==200:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
        for q in v['web_primary_reads']:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
        assert any(q['key']=='robbo-barcelona' and '403' in q['error'] for q in v['sources'])
js=(ROOT/'dist/assets/camp-programmes.js').read_text();assert 'STEM_europe_camp_audit_v88.json' in js and 'STEM_americas_camp_audit_v87.json' in js
assert 'data-ui-version="88"' in (ROOT/'dist/index.html').read_text()
subprocess.run([NODE,'--check',str(ROOT/'dist/assets/camp-programmes.js')],check=True)
print(json.dumps(dict(verified=True,events=2997,dossiers=547,new_dossiers=18,deepened_dossiers=3,corrected_old_rows=35,new_dated_rows=22,new_family_ics=7,family_ics=2256,source_urls=829,worldwide_complete=False)))
