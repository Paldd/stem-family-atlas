"""Publishable evidence receipt for a bounded primary-source Americas pass."""
import json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent / 'stem-family-atlas-work'
PRIMARY = WORK / 'camps-primary-v80'
BASE = '404545dbb212a3d6b841a25ee4531b825aaa1af3'
b = json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d = json.loads((ROOT/'data/catalog.json').read_text())
c = d['camp_programmes']
oldids = {e['id'] for e in b['events']}
oldslugs = {p['slug'] for p in b['camp_programmes']['profiles']}
newslugs = [p['slug'] for p in c['profiles'] if p['slug'] not in oldslugs]
new = [e for e in d['events'] if e['id'] not in oldids]
assert len(newslugs) == 13 and len(new) == 110 and len(c['profiles']) == 402
receipts = [v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts) == 36 and sum(v.get('status') == 200 for v in receipts) == 30
oldurls = {s['url'] for p in b['camp_programmes']['profiles'] for s in p['sources']}
newurls = sorted({s['url'] for p in c['profiles'] for s in p['sources']} - oldurls)
assert len(newurls) == 30 and c['counts']['source_urls'] == 634
external = dict(messages_sent=False,applications_submitted=False,payments_made=False,
                subscriptions_created=False,age_verification_submitted=False)
checks = [
    'All 2621 previous events and all 389 dossier IDs/content preserved; 13 new programme/age/season/format dossiers, not 13 independent operators.',
    'Camp Muskoka is separate from Muskoka Woods. Its eight weeklong2027 sessions/CAD1695/tax/cancellation are primary; language and foreign eligibility remain unknown.',
    'Muskoka Woods2027 WILD2019–2021 / Venture2017–2018 match the children by explicit cohorts. Eight weeks each with different prices; Christian Cabin Chat, insurance and mandatory adult pickup within six hours documented. ISO currency and 14-vs15-day transport cancellation conflict retained.',
    'Robin Hood Canada2027 own price image visually read: four sessions, third nine attendance days; early new-family1855/1680 through31October. Current bus280/190 differs from stale search265/180. Home&Away separate completedGrades2–4/three-night programme; neither school grade inferred from birthyear.',
    'VGC PDF filename2026 contains real Summer/Winter2027 tables on pages8–9, both rendered/read. Junior individual rates, adult rates and unknown Family bundle separated. Junior9–12 must travel with adult despite generic unaccompanied-minorfee. Two season windows produce no exact-session ICS.',
    'STEM4Kids78 course/campus/date variants:21Builders and19each other. Actual product table dates independently parsed from primary cachedHTML; spring4courses12–16April onlyCupertino. Nov1/Open labels are not live vacancies; English/ISO/taxes not inferred. Robotkits stay atcamp.',
    'STEM4Kids OscarGO only afterseventh birthday; MatveyBuilders/Rookies only while9. SPIKEEssential/Prime,GO/IQ course-specific gates and actual cancellation/full-payment rules retained.',
    'RobotAcademy2027 Westerville andLewis-area dates tied to detailed own full-day programme pages. Age4–7/8–13,optionalTakeHomeRobot,bringlunch,unknownfullprice/English. Four-week refund counts from registration, not start; internalmedals not worldchampionships.',
    'YMCA Colombia29November–4December2026 atBochica/Santandercito,COP1950000,100%English,YCAMP8–13. EarliergenericLaVega/undatedmini variants not newvenue/date evidence;2027 notification form not bookeddate. Oscarbelow8.',
    'LincolnEPICGrades8–12/EN&ESJanuary2026 archive,notJunior2027. LiotaWinter19days-vs4weeks/summer-only ageFAQ remains unresolved. CampHopevolunteerteam andHerediaJanuary2026 workshops excluded as ordinary future familycamps.',
    '110 new calendar rows/familyICS; prior1956 UID/datepairs preserved;104 exhibitionICS unchanged. SQLite/publicJSON agree,bridge idempotent,86family scenarios and0fullyauditedcountries.'
]
byiso = {s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','GBR','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','COL']}
learning = sum(e['block']=='Лагеря' for e in d['events'])
audit = dict(asof='2026-10-05',version=80,status='progress',
    scope='USA/Canada/Latin America programme, admission, price and calendar primary pass; full worldwide competition/exhibition/school/camp objective remains active',
    new_dossiers=13,updated_dossiers=[],new_calendar_rows=110,new_family_ics=110,
    programme_dossiers=402,countries_with_dossiers=33,official_dossier_urls=634,country_dossier_counts=byiso,
    programme_slugs=newslugs,findings=c['gaps'][-4:],
    calendar=dict(events=len(d['events']),learning_records=learning,family_ics=2066,exhibition_ics=104,
        managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows']),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
    next_priority='Continue requested European/Asian/American countries and full league/exhibition/school scope; primary2027 junior CRI/MEX winter programmes, English course proof, complete contracts and family invoices remain open')

def write(stem,value):
    body=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'data'/f'{stem}.json').write_text(body)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(body)

write('americas-camp-audit-v80',audit)
write('americas-camp-source-receipts-v80',dict(asof='2026-10-05',version=80,
    scope='36 direct HTTP attempts:30successful including one operator rate image and one PDF;6failedHTTP kept. Own VGC/RobotAcademy pages additionally read via web reader; own Liota/STEM4Kids read in browser without forms.',
    sources=receipts,verified_new_dossier_urls=newurls,
    visual_primary_reads=[dict(url='https://www.camprobinhood.ca/wp-content/uploads/2027-REG-RATES-Oct-1-819x1024.png',method='Own2027 price image read visually: sessions, early deadline, shortened session and bus charges'),
        dict(url='https://vgc.ca/wp-content/uploads/2026-General-Price-Book-FINAL.pdf',pages=[8,9],method='Own PDF rendered with Poppler and visually read: both2027 price titles, individual packages and mandatory accompanying adult')],
    browser_reads=[dict(url='https://liotacamps.com/',method='Dynamicwintersection and expandedage/refundFAQs read; summer-only age rule/19day-vs4weeks conflict corroborated, no application'),
        dict(url='https://www.stem4kids.co/camps/lego-robotics-builders',method='Public table10summerweeks/twocampuses/springCupertino/date/price/platforms inspected; Open+OpensNov1 ambiguous, no live vacancy')],
    web_reader_reads=[dict(url=u,method='Own primary programme page read; rawHTTP403 retained') for u in [
        'https://vgc.ca/english-programs-and-schedule/family-program/',
        'https://vgc.ca/english-programs-and-schedule/the-camps-junior-program/',
        'https://vgc.ca/price-list/',
        'https://robot-academy.com/summer-camps-columbus/',
        'https://robot-academy.com/westerville-summer-robotics-camp-page/',
        'https://robot-academy.com/lewis-center-delaware-camp-page/']],
    excluded_candidates=[dict(url='https://www.camphopeworldwide.org/costaricafaq',reason='Staff/volunteer mission trip, not ordinary juniorcamp offer'),
        dict(url='https://agenda.mcj.go.cr/evento/taller-de-programacion-y-robotica-desde-el-juego-biblioteca-publica-de-heredia',reason='January2026 archivedworkshop, no2027dates'),
        dict(url='https://www.aiandbeyondacademy.com/index.php/dates-and-rates-2027',reason='Earlyprices explicitly closed14August2026; platform-specific age/venue/ordinarycurrentprice not yet read. Not claimed as ready foreign familycourse')],
    external_actions=external,notes=[
        'All source summaries use read content, including year/programme/admission conflicts. Search snippets and successfulHTTP alone do not establish complete audits.',
        'Provider raw HTML/PDF/image and child photos remain outside public repository; only fact summaries and provenance/error receipts are published.',
        'Different course/age/campus/format dossiers are not independent campoperators; editorial candidates are not an external worldranking.',
        'Published price/session does not establish live vacancy, international acceptance, English teaching, final tax/insurance invoice or legal admission. Full worldwide goal remains active.']))

plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=80:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',
    evidence='Version79 native publication succeeded: commit404545dbb212a3d6b841a25ee4531b825aaa1af3; deploymentappgdep_6ac3d8f39cf8819184372798693e8d73.13newdossiers/2deepened/17calendarrows. Goal active; worldwide coverage incomplete.')
plan['latest_validation']=dict(version=80,asof='2026-10-05',status='preservation/source/calendar verifier passed; native publication follows',
    events=len(d['events']),camp_learning_records=learning,programme_dossiers=402,countries_with_dossiers=33,
    swiss_dossiers=59,french_dossiers=35,spanish_dossiers=28,uk_dossiers=5,taiwan_dossiers=23,
    singapore_dossiers=52,japan_dossiers=17,korea_dossiers=8,usa_dossiers=38,canada_dossiers=51,costa_rica_dossiers=7,mexico_dossiers=24,
    official_dossier_urls=634,family_ical=2066,exhibition_ical=104,worldwide_complete=False,checks=checks)
plan['americas_camp_programme_audit_v80']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=402,countries=33,swiss=59,
    generated_calendar_entries=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'])
for req in plan['requirements']:
    if req['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        req['evidence']='v80:402 programme/age/format dossiers in33countries;110new dated Americasvariants;634official URLs. Explicit language/age/year/foreignentry and priceconflicts retained. All worldwideblocks retained; no country/globalcompleteness claim.'
plan['status']=plan['native_goal_status']='active'
plan['updated']='2026-10-05'
write('research-plan',plan)
p=ROOT/'dist/index.html'
p.write_text(p.read_text().replace('?v=79','?v=80').replace('data-ui-version="79"','data-ui-version="80"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_americas_camp_audit_v80.json" download>Америка: программы, пансионы и цены ↓</a> · <a href="downloads/STEM_americas_camp_source_receipts_v80.json" download>Источники проверки Америки ↓</a> · '
anchor='<a href="downloads/STEM_asia_camp_audit_v79.json"'
if link not in s:
    assert anchor in s
    s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=402,new_dossiers=13,new_calendar_rows=110,new_family_ics=110,source_urls=634,goal='active')))
