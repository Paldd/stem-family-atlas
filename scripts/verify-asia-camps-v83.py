"""Independent primary/grade/language/price checks and full published-v82 preservation."""
import hashlib,json,re,sqlite3,subprocess
from pathlib import Path
from camp_catalog_bridge import integrate
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v83'
BASE='94063c00ad38953ac234e75f35ddb0d17654c176'
def before(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def raw(key):return (PRIMARY/(key+'.txt')).read_text()
b=json.loads(before('data/catalog.json'));d=json.loads((ROOT/'data/catalog.json').read_text())
old={e['id']:e for e in b['events']};events={e['id']:e for e in d['events']}
assert len(old)==2780 and len(events)==len(d['events'])==2797
assert all(events.get(k)==v for k,v in old.items())
for k in ['league_guide','development_routes','schools','school_history','family_context','family_strategy','top_picks']:
    assert d[k]==b[k],k
c=d['camp_programmes'];p={q['slug']:q for q in c['profiles']};op={q['slug']:q for q in b['camp_programmes']['profiles']}
assert len(op)==432 and len(p)==448 and all(p[k]==v for k,v in op.items())
assert c['profiles'][:432]==b['camp_programmes']['profiles']
assert c['counts']['countries']==34 and c['counts']['source_urls']==703 and c['counts']['swiss']==69
for iso,n in [('CHE',69),('FRA',39),('ESP',31),('TWN',25),('SGP',56),('JPN',23),('KOR',10),('PHL',2),('USA',38),('CAN',51),('CRI',7),('MEX',24)]:
    assert sum(q['iso']==iso for q in p.values())==n
assert sum(e['block']=='Лагеря' for e in events.values())==1466
assert len(c['generated_event_ids'])==1003 and c['integration']['reused_legacy_events']==69 and c['integration']['seasonal_windows']==27
assert len(c['shortlist'])==98 and c['shortlist'][:94]==b['camp_programmes']['shortlist']
assert c['gaps'][:-4]==b['camp_programmes']['gaps']
assert all(len(s['slugs'])==len(set(s['slugs'])) and all(k in p for k in s['slugs']) for s in c['shortlist'][-4:])
new=[e for k,e in events.items() if k not in old]
assert len(new)==17 and all(e['block']=='Лагеря' and e['checked']=='2026-10-05' for e in new)
def rows(slug):return [e for e in new if e['camp_dossier_slug']==slug]
def pairs(slug):return {(e['start'],e['end']) for e in rows(slug)}
expected={'ugaku-nasu-winter':1,'ugaku-nasukashi-spring':1,'ugaku-chatan-winter':1,'ugaku-onna-spring':1,
          'ugaku-wakayama-spring':1,'ugaku-cebu-winter':1,'ugaku-cebu-spring':1,
          'see-discover-japan':2,'see-world-games':2,'srt-little-elf':1,'srt-stage-younger':1,'srt-stage-older':1,
          'voca-power-popstars':2,'embassy-korea-spring':1}
assert {s:len(rows(s)) for s in expected}==expected and {e['camp_dossier_slug'] for e in new}==set(expected)

# Parse calendar header dates from independently retained Japanese campus pages.
for source,slugs in [('ugaku-nasu',['ugaku-nasu-winter','ugaku-nasukashi-spring']),
                     ('ugaku-okinawa',['ugaku-chatan-winter','ugaku-onna-spring']),
                     ('ugaku-cebu',['ugaku-cebu-winter','ugaku-cebu-spring'])]:
    t=re.sub(r'\s+','',raw(source))
    found={('-'.join(v[:3]),'-'.join(v[3:])) for v in re.findall(r'(202[67])\.(\d{2})\.(\d{2})-(202[67])\.(\d{2})\.(\d{2})',t)}
    jt=re.sub(r'[（(][日月火水木金土][）)]','',t)
    for y,m,a,zy,zm,z in re.findall(r'(202[67])年(\d{1,2})月(\d{1,2})日[〜～-](?:(202[67])年)?(?:(\d{1,2})月)?(\d{1,2})日',jt):
        found.add((f'{y}-{int(m):02d}-{int(a):02d}',f'{zy or y}-{int(zm or m):02d}-{int(z):02d}'))
    assert {pair for s in slugs for pair in pairs(s)}==found
    assert '契約料30,000円' in t and '小学生・中学生' in t
for slug in expected:
    if slug.startswith('ugaku'):
        assert p[slug]['confirmed_instruction_languages']==['EN'] and p[slug]['language_evidence_role']=='camp_life'
        assert p[slug]['family_fit']['oscar']['status']=='conditional' and 'class' not in p[slug].get('admission_kind','')
        assert '4+ недели' in p[slug]['price']['deposit']
assert '4週間以上' in raw('ugaku-refund') and '90日目' in raw('ugaku-cancel') and '45日目' in raw('ugaku-cancel')
assert '那須甲子' in raw('ugaku-nasu') and '福島県西郷村' in raw('ugaku-nasu')
assert 'Nishigo, Fukushima' in rows('ugaku-nasukashi-spring')[0]['city'] and 'Tochigi' in rows('ugaku-nasu-winter')[0]['city']
assert '北谷ではなく恩納村' in raw('ugaku-okinawa') and 'Onna' in rows('ugaku-onna-spring')[0]['city']
assert '139,800' in p['ugaku-chatan-winter']['price']['label'] and '169,800' in p['ugaku-chatan-winter']['price']['label']
assert '159,800' in p['ugaku-nasu-winter']['price']['label'] and '189,800' in p['ugaku-nasu-winter']['price']['label']
assert 'JPY 199,800' in p['ugaku-wakayama-spring']['price']['label'] and '229,800' in p['ugaku-wakayama-spring']['price']['label']
assert '該当する記事は見つかりませんでした' in raw('ugaku-wakayama')
t=raw('ugaku-kansai');assert '2027年 春休み限定' in t and '3月28日（日）〜4月3日（土）' in t and '英語グループワーク22時間' in re.sub(r'\s+','',t)
assert pairs('ugaku-wakayama-spring')=={('2027-03-28','2027-04-03')}
assert 'マンツーマンレッスン14時間' in raw('ugaku-cebu') and '空港⇔校舎の送迎込み' in raw('ugaku-cebu')
t=raw('myoko-pdf');assert '6 - 15 years old' in t and 'advanced to native' in t and '¥130,000' in t and '¥20,000' in t
assert not p['myoko-adventure-culture']['timing']['sessions'] and p['myoko-adventure-culture']['price']['year']==2026

tj=(PRIMARY/'see-japan-web.txt').read_text();tw=(PRIMARY/'see-products-web.txt').read_text()
for text,slug,duration,pair in [(tj,'see-discover-japan',2,('2027-01-21','2027-01-22')),(tw,'see-world-games',5,('2027-01-25','2027-01-29'))]:
    assert '幼兒園大班' in text and '國小4年級' in text and '外師全程英文授課' in text
    assert '台北商業大學' in text and 'SEE英文學院' in text and pairs(slug)=={pair}
    assert len({e['city'] for e in rows(slug)})==2 and all(e['iso']==['TWN'] for e in rows(slug))
    assert all(e['date_scope']=='day_camp_window' for e in rows(slug))
    assert 'group' not in p[slug]['family_fit']['matvey']['detail']
assert '$ 5,600' in tj and '$1,100' in tj and '5,860' in tj and '5,300' in tj
assert '13,800' in tw and '11,730' in tw and '10,350' in tw
assert rows('see-discover-japan')[0]['attendance_weekdays']==['TH','FR']

t=raw('srt-dec');assert '14 –' in t and '16 Dec 2026' in t and 'Monday to Wednesday' in t and '4 to 7' in t and 'Language:\nEnglish' in t
assert 'Non-members:\n$160' in t and 'inclusive of lunch' in t and 'from 1-3 days' in t
assert '14TH - 18TH' in raw('kidsspace-pdf') and '14–18Dec' in p['srt-little-elf']['timing']['label']
assert pairs('srt-little-elf')=={('2026-12-14','2026-12-16')} and rows('srt-little-elf')[0]['attendance_weekdays']==['MO','TU','WE']
t=raw('srt-stage2');assert 'Week 2: 30' in t and '(Mandarin)' in t and '(English)' in t and 'Sold out for 4 –' in t
assert '$400' in t and '$6 booking fee' in t and 'strict age policy' in t
assert rows('srt-stage-younger')[0]['availability']['status']=='closed' and rows('srt-stage-older')[0]['availability']['status']=='limited'
for s in ['srt-stage-younger','srt-stage-older']:assert pairs(s)=={('2026-12-07','2026-12-11')}
t=raw('voca-camp');assert '7-9' in t and '14-16' in t and 'December 2026' in t and '$450/3-day' in t and '$50 Registration' in t
assert 'strictly no refunds' in t and 'not stackable' in t and '6 to 12' in t
assert not p['voca-power-popstars']['confirmed_instruction_languages'] and all(not e['languages'] for e in rows('voca-power-popstars'))
assert '450/3дня +50' in p['voca-power-popstars']['price']['label'] and '455' in p['voca-power-popstars']['price']['label']
assert pairs('voca-power-popstars')=={('2026-12-07','2026-12-09'),('2026-12-14','2026-12-16')}
t=raw('kisas-main');assert 'Grades 4 – 9 (ages 10 – 15)' in t and 'Length to be announced' in t and 'Venue to be announced' in t
assert 'pre-registration is not an application' in t.lower() and 'based on Cohort 1' in t
assert 'Native teachers: lead' in raw('kisas-program') and 'co-teach bilingually' in raw('kisas-program')
assert not p['kisas-ai-music']['timing']['sessions'] and p['kisas-ai-music']['language_evidence_role']=='language_lessons'
t=raw('embassy-korea');assert 'March 21, 2027 – March 30, 2027' in t and '10 - 19 Years' in t and '2,780.00' in t
assert '1 Meal (breakfast)' in t and 'English Speaking Club' in t and 'Programs for Parents' in t
assert pairs('embassy-korea-spring')=={('2027-03-21','2027-03-30')}
assert '200 USD' in raw('embassy-terms') and '100 USD' in raw('embassy-terms')
assert not any('ntue' in s or 'palau' in s for s in set(p)-set(op))

report=json.loads((ROOT/'data/camp-programmes-deep-2026-2027.json').read_text())
again=json.loads(json.dumps(d));integrate(again,report);assert again==d
for file,wanted in [('STEM_database.json',d),('STEM_camp_programmes_deep_2026_2027.json',c)]:
    assert json.loads((ROOT/'dist/downloads'/file).read_text())==wanted
con=sqlite3.connect(ROOT/'dist/downloads/STEM_database.sqlite')
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==2797 and con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==448
con.close()
def calendar(v):
    out={};t=v.decode().replace('\r\n ','').replace('\r\n\t','')
    for ch in t.split('BEGIN:VEVENT')[1:]:
        f={line.split(':',1)[0]:line.split(':',1)[1] for line in ch.split('END:VEVENT')[0].splitlines() if ':' in line}
        assert f['UID'] not in out;out[f['UID']]=f
    return out
file='dist/downloads/STEM_подтвержденные_даты.ics';prior=calendar(before(file));now=calendar((ROOT/file).read_bytes())
assert len(prior)==2112 and len(now)==2128 and set(prior)<=set(now)
for uid,v in prior.items():assert all(now[uid].get(k)==v.get(k) for k in ['DTSTART;VALUE=DATE','DTEND;VALUE=DATE'])
eligible=[e for e in new if e.get('availability',{}).get('status')!='closed']
assert len(eligible)==16 and set(now)-set(prior)=={'stem-'+e['id']+'@family-stem.local' for e in eligible}
file='dist/downloads/STEM_крупные_выставки.ics';expo=calendar((ROOT/file).read_bytes());oe=calendar(before(file))
assert len(expo)==104 and set(expo)==set(oe)
for uid,v in oe.items():assert {k:x for k,x in expo[uid].items() if k!='DTSTAMP'}=={k:x for k,x in v.items() if k!='DTSTAMP'}
plan=json.loads((ROOT/'data/research-plan.json').read_text());bp=json.loads(before('data/research-plan.json'))
assert plan['status']==plan['native_goal_status']=='active' and plan['latest_validation']['version']==83
assert plan['previous_goal_turn_classification']['classification']=='progress' and 'Version82' in plan['previous_goal_turn_classification']['evidence']
assert {q['id'] for q in bp['requirements']}<={q['id'] for q in plan['requirements']}
assert json.loads((ROOT/'dist/downloads/STEM_research_plan.json').read_text())==plan
assert plan['camp_catalog_integration']['dossiers']==448 and d['coverage_summary']['fully_audited_countries']==0
for stem in ['asia-camp-audit-v83','asia-camp-source-receipts-v83']:
    val=json.loads((ROOT/'data'/f'{stem}.json').read_text())
    assert json.loads((ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).read_text())==val
    assert not any(val['external_actions'].values())
assert len(val['sources'])==31 and sum(v.get('status')==200 for v in val['sources'])==22
assert len(val['dossier_source_urls_added'])==22 and len(val['visual_primary_reads'])==3
for v in val['sources']:
    if v.get('status')==200:assert v['body_snapshot_retained'] and hashlib.sha256((PRIMARY/v['raw_filename']).read_bytes()).hexdigest()==v['sha256']
for v in val['image_sources']:assert hashlib.sha256((PRIMARY/v['file']).read_bytes()).hexdigest()==v['sha256']
assert 'data-ui-version="83"' in (ROOT/'dist/index.html').read_text()
assert 'STEM_asia_camp_audit_v83.json' in (ROOT/'dist/assets/camp-programmes.js').read_text()
print(json.dumps(dict(passed=True,preserved_events=2780,preserved_dossier_ids=432,new_dossiers=16,new_calendar_rows=17,new_family_ics=16,
    events=2797,dossiers=448,family_ics=2128,exhibition_ics=104,worldwide_complete=False)))
