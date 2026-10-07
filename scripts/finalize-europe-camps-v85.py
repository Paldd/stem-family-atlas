"""Retain source receipts and report bounded European progress against published v84."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v85'
BASE='220b513e9720864862294c47f9d633897c8a995a'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
oldslugs={p['slug'] for p in b['camp_programmes']['profiles']};oldids={e['id'] for e in b['events']}
slugs=[p['slug'] for p in c['profiles'] if p['slug'] not in oldslugs]
new=[e for e in d['events'] if e['id'] not in oldids]
assert len(slugs)==23 and len(new)==136 and len(c['profiles'])==487
receipts=[v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts)==32 and sum(v.get('status')==200 for v in receipts)==31
for v in receipts:
    if v.get('status')==200:
        f=next(PRIMARY/(v['key']+ext) for ext in ['.html','.pdf'] if (PRIMARY/(v['key']+ext)).exists())
        assert hashlib.sha256(f.read_bytes()).hexdigest()==v['sha256']
        v.update(body_snapshot_retained=True,raw_filename=f.name,
                 content_scope='JavaScript shell only, not a current camp programme read' if v['key']=='stgeorge-summer' else 'primary HTML/PDF body retained')
images=json.loads((PRIMARY/'image-receipts.json').read_text())
js=json.loads((PRIMARY/'js-receipts.json').read_text())
for v in images:assert hashlib.sha256((PRIMARY/v['file']).read_bytes()).hexdigest()==v['sha256']
for v in js:assert hashlib.sha256((PRIMARY/v['raw_filename']).read_bytes()).hexdigest()==v['sha256']
visual=[]
for file,url,page,note in [
    ('chantemerle-2027-cover.png','https://chantemerle.ch/documents/summer-camp-2027-brochure.pdf',1,
     '2027 cover visually read: 6–11 juniors / 12–16 teens, opening window, 2–5-week tariff and inclusions.'),
    ('enforex-2027-prices.png','https://download.enforex.com/pdf/enforex-summercamps.pdf',33,
     'Visually read nine campus columns, age categories, exact session dots, weekly/fortnight prices, formats and supplemental fees.'),
    ('englishcamp-price-table.png','https://english-camp.ch/images/Screenshot_2024-09-28_at_154805.png',None,
     'Own price image visually read. Current parent price page explicitly labels 2026 & 2027; image filename 2024 retained, no inferred season from filename.')]:
    bb=(PRIMARY/file).read_bytes();visual.append(dict(url=url,page=page,method=note,
        render_sha256=hashlib.sha256(bb).hexdigest(),render_bytes=len(bb)))
oldurls={s['url'] for p in b['camp_programmes']['profiles'] for s in p['sources']}
newurls=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls)
assert len(newurls)==22 and c['counts']['source_urls']==749
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,subscriptions_created=False,automations_created=False)
checks=[
    'All 2823 previous event IDs/content preserved. All 464 dossier IDs retained; 463 dossiers unchanged. CP018 Barcelona Beach refreshed from the official 2027 PDF, with its previous 2026 facts retained. 23 new programme/format/venue dossiers cover four operators, not 23 independent camps.',
    'Enforex 2027 page33 independently parsed from retained PDF: nine campus dot columns and all 1/2-week dates. Madrid/Elviria/Salamanca junior 5–18, Beach5–16; Centro14–18 and Alicante/Malaga/Valencia12–18 kept as future tracks. A destination heading up to21 combines a different Young Adults product.',
    'Enforex one-week tuition:1195 Elviria/Salamanca/Valencia,1395 others; fortnight2095/2495. Day600/week, course-only300/week, application35/person. Two children fortnight boarding4260/5060, day2470, language-only1270 before extras; deposit not double counted. 20 lessons×45min =15hours, not20hours.',
    'Enforex exact campus date differences retained: Barcelona Centro and Valencia have no July one-week cohorts; Beach has Aug15–21 one-week but no Aug15–28 fortnight. Published 3/4-week prices do not create guessed cohorts. Day attendance MO/TU/WE/TH/FR, no character-list weekday bug or weekend attendance promise.',
    'Enforex Elviria junior dorms6–12 / older4–6, no single option; Madrid/Beach double private-bath rooms, Salamanca singles without surcharge/shared bath. Four meals vs three varies by destination. Homestay14+ not applied to children6–10. Specific camp cancellation850 last4weeks / no refund<=2weeks retained separately from generic250deposit and optional300/week guarantee.',
    'Enforex Leadership Jul4–17 2027,14–21,3950+35,English entrepreneurship OR Spanish language choice; its Francisco de Vitoria campus not the junior Wynwood residence. Single room/three meals/24h care not Young Adults50% supervision. Not eligible for current children and excluded from familyICS.',
    'Alpadia Leysin springMar29–Apr16 and summerJun21–Aug6,EngelbergJun28–Jul30,PassyJun28–Aug6 are 2027 opening windows. No fake every-Monday/cohort calendar. Leysin8+,Engelberg10+conditional on birthday,Passy13+;Igny13+ still2026. English lessons confirmed, whole camp English not assumed. Nice/Biarritz own French pages read but not EN-supported family recommendations.',
    'Alpadia standard20/45minutes=15hours, intensive25=18h45m. English pages2027 vsFrenchLeysin2026 and brochure/Terms priceyear2026 retained. Base price not rendered, option/transfer amounts not a full price. Enrolment in package not double counted using older125/90 fees; exactly21-day cancellation gap retained.',
    'Chantemerle own2027PDF juniors6–11,teens12–16,Jun27–Aug1 and2–5week tariffs4950/6250/7500/8900. Fee-page1week2800 vsbrochure min2 conflict, day1600/week/halfday1100(noactivities), insurance8/day, EuropaPark included only residential. CHF800 nonrefundable initial inclusion unresolved, not silently credited or doubled.',
    'Chantemerle MakeItCount English Jul18–Aug1,teen future track, not an official TEDx competition. MathsPhysics14–17 vsbrochure12–16 upper-age issue retained; two weeks insideJun27–Jul18 is a window, not a21-day stay. EPFL connection attributed to operator and3D-printing activity not a full robotics course.',
    'EnglishCamp Switzerland 2027 independently read: Apr18–24/Apr25–May1 Uerikon andJul11–17/Jul18–24 Rotberg,age9–15. Price page explicitly2026&2027 with older image filename; regular1380/2430+50perinvoice, early/sibling conditions not assumed. Oscar below9 cannot use sibling tuition to bypass admission. No3/4-week dates inferred from their price columns.',
    'StGeorge Summer HTTP200 only JS shell; public bundle contains2026 defaults/alternative camp cards, not verified current2027 displayed programme. One parents URL404 retained as an error. Raw bodies/provider photos/rendered pages remain outside public checkout; no failed/challenge/shell read presented as a complete programme audit.',
    '2959 total events/1628 camp-learning records,487 dossiers in34countries/749 dossierURLs,106 family scenarios.136 dated additions:84 familyICS additions and52 future-age rows excluded;8 new season windows do not createICS. All2149 prior familyUID/date pairs and104 exhibitionICS preserved. SQLite/publicJSON agree and bridge idempotent.0 fully audited countries; full worldwide authorised goal active.'
]
byiso={s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','COL']}
learning=sum(e['block']=='Лагеря' for e in d['events'])
audit=dict(asof='2026-10-05',version=85,status='progress',
    scope='Switzerland/France/Spain programme-specific primary 2027 dates/prices/languages/boarding/day/future tracks; all priority regions and full worldwide goal remain active',
    new_dossiers=23,operators_covered=4,updated_dossiers=['enforex-barcelona'],new_calendar_rows=136,new_family_ics=84,future_age_rows_excluded_from_family_ics=52,reused_existing_calendar_rows=0,
    programme_dossiers=487,countries_with_dossiers=34,official_dossier_urls=749,country_dossier_counts=byiso,programme_slugs=slugs,findings=c['gaps'][-4:],
    calendar=dict(events=len(d['events']),learning_records=learning,family_ics=2233,exhibition_ics=104,managed_dated_rows=len(c['generated_event_ids']),
        reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows']),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
    next_priority='Continue Taiwan/Singapore/Japan/Korea,USA/Canada/CostaRica/Mexico/LatinAmerica and Europe junior/general/technical2026–27 day/boarding/family programmes with full prices/languages/grades/admission/availability; schools/results/routes and worldwide leagues/exhibitions remain in scope')
def write(stem,v):
    t=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(t)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(t)
write('europe-camp-audit-v85',audit)
write('europe-camp-source-receipts-v85',dict(asof='2026-10-05',version=85,
    scope='32 direct HTML/PDF attempts:31 HTTP200 bodies, of which one JS-only shell; one404 error retained. One separately retained publicJS bundle and own price image; three primary visual reads. HTTP200 is not a full programme/admission confirmation.',
    sources=receipts,image_sources=images,public_bundle_sources=js,visual_primary_reads=visual,dossier_source_urls_added=newurls,external_actions=external,
    notes=['Raw HTML/PDF/provider photographs/source images remain outside public repository; public paraphrased facts/provenance/errors only.',
        'Published dates/ages/fees are not admissions, confirmed places, bookings or full family invoices.',
        'No applications, bookings, payments, organizer messages, subscriptions or new automations.',
        'Full worldwide authorised scope remains active;0 fully audited countries.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=85:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',
    evidence='Version84 native publication succeeded: commit220b513e9720864862294c47f9d633897c8a995a; deployment appgdep_6ac3f9e5b9288191a5ea27e00986166e.16new dossiers/26calendar rows/21familyICS. Goal active; worldwide coverage incomplete.')
plan['latest_validation']=dict(version=85,asof='2026-10-05',status='Independent source/preservation/calendar verification; native publication tracked separately',
    events=len(d['events']),camp_learning_records=learning,programme_dossiers=487,countries_with_dossiers=34,official_dossier_urls=749,
    family_ical=2233,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=byiso)
plan['europe_camp_programme_audit_v85']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=487,countries=34,swiss=78,
    generated_calendar_entries=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'])
for req in plan['requirements']:
    if req['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        req['evidence']='v85:487 programme/venue/format dossiers in34countries;23new across4operators,CP0182027refresh,136dated rows/84familyICS,749dossierURLs. Camp-specific primary2027PDFdates/ages/prices vs2026web/unknowncohorts/languages retained; full worldwide and all priority regions active,0fullyauditedcountries.'
plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05';write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=84','?v=85').replace('data-ui-version="84"','data-ui-version="85"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_europe_camp_audit_v85.json" download>Европа: смены, цены и пансионы 2027 ↓</a> · <a href="downloads/STEM_europe_camp_source_receipts_v85.json" download>Источники проверки Европы ↓</a> · '
anchor='<a href="downloads/STEM_americas_camp_audit_v84.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=487,new_dossiers=23,updated_dossiers=1,new_calendar_rows=136,new_family_ics=84,source_urls=749,goal='active')))
