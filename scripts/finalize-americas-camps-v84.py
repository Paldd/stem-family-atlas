"""Retain primary receipts and report bounded Americas progress against published v83."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v84'
BASE='3587a9bd56dbfbe98d584fb1bd2d8bf2c32eb4d8'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
oldslugs={p['slug'] for p in b['camp_programmes']['profiles']};oldids={e['id'] for e in b['events']}
slugs=[p['slug'] for p in c['profiles'] if p['slug'] not in oldslugs]
new=[e for e in d['events'] if e['id'] not in oldids]
assert len(slugs)==16 and len(new)==26 and len(c['profiles'])==464
receipts=[v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts)==31 and sum(v.get('status')==200 for v in receipts)==29
for v in receipts:
    if v.get('status')==200:
        f=next(PRIMARY/(v['key']+ext) for ext in ['.html','.pdf'] if (PRIMARY/(v['key']+ext)).exists())
        assert hashlib.sha256(f.read_bytes()).hexdigest()==v['sha256']
        v.update(body_snapshot_retained=True,raw_filename=f.name)
web=[]
for file,urls,note in [
    ('walden-rates-web.txt',['https://www.campwalden.ca/rates-and-dates/'],'Own reader: complete rates/grade/availability/terms. Direct403 retained as error.'),
    ('extra-primary-web.txt',['https://timbalaia.com.br/','https://www.campwalden.ca/rates-and-dates/','https://www.icomexico.com/faq'],
     'Own reader response retained. Timbalaia primary dates/fee/age read; direct403 remains an error. ICO FAQ independently read by retained direct200 redirect body.')]:
    bb=(PRIMARY/file).read_bytes();web.append(dict(urls=urls,method=note,snapshot_sha256=hashlib.sha256(bb).hexdigest(),snapshot_bytes=len(bb)))
png=PRIMARY/'intercultura-2027-price-view.png'
visual=[dict(url='https://interculturacostarica.com/wp-content/uploads/2026/06/2027-Price-List-Intercultura-Costa-Rica.pdf',page=1,
    method='Poppler rendered and visually read header, campus columns, kid/adult/teen/lodging/transfer/discount units.',
    render_sha256=hashlib.sha256(png.read_bytes()).hexdigest(),render_bytes=png.stat().st_size)]
oldurls={s['url'] for p in b['camp_programmes']['profiles'] for s in p['sources']}
newurls=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls)
assert len(newurls)==24 and c['counts']['source_urls']==727
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,subscriptions_created=False)
checks=[
    'All 2797 previous event IDs/content and 448 programme dossiers preserved.16 new programme/grade/format dossiers cover6 operators, not16 independent camps; 26 explicitly dated rows,21 familyICS additions.',
    'Whitman Pioneer2027 July25–31/$2000: finishingGrade1/2 only. Matvey age9–10 is not proof of grade1/2 admission. Regular Full/First/Second source prices17600/12150/9400; short-session grades2/3 and limited4–7 preserved, Second dates not stretched to four weeks.',
    'Whitman Family Aug16–20 2027: adult1000,child4–17 500,<=3free;2adults+2children>=4 arithmetic3000 before unknown food/fees. Own English webpage not a whole-course language guarantee; no EN-confirmed flag.',
    'Champions 2027 HTML rates parsed independently:5 one-week terms,5 two-week,4 four-week,TriplePlay3-week and Combo5-week. One-week maxGrade3/8 differs; lower one-week bound not copied from K–11 two/four-week. Longer3/5/6 weeks Grade2–11. Six-week combine-any-three rule not expanded into guessed calendar dates.',
    'Champions tuition/deposit:2450/400,4750/800,7250/800,6350/800,8995/800,10500/800. No double-counted deposit. Current-families heading2027/text2026 and automatic Campanion opt-out conflict with rates optional; unconfirmed2026 transport amounts not promoted to2027.',
    'Champions Family Sep25–27 2026 archive only, not2027. Family rates differ by attendance/age; own linen, whole-cabin only6+ group/499.50 deposit; family of4 not assumed to receive private cabin. No family2027ICS.',
    'Walden Ontario Summer2027 RegistrationClosed/waitlist:5 dated catalogue rows all closed and excluded from familyICS. Grade2–10 regular/2–5 six-week,Grade2-onlyExplorer,Grade1-onlyLongWeekend; finishingSK explicitly not thisyear. DAY1 decoration not day-camp mode.',
    'Walden foreign rates outsideCanada/US mayvary, fees payableCAN/USD,13%HST/3%card. General2000deposit but explicitFAQLongWeekend full-payment exception retained. Rates3days vsjourney4days label; actualJul30–Aug2 unchanged. Tiered refund vs blanket non-refundable paragraph conflict retained, not free-cancellation promise.',
    'Nominingue camp operates inEnglish directly stated inFAQ; French exposure not mandatory bilingual instruction. Boys7+ and age/grade-specific durations, junior rates7–10 vsFAQ7–9 upper bound conflict; Oscar only after7birthday. Calendar explicitly2026/PDF2026 agrees; unlabelled rates not proof of2027 or future vacancies/currency/tax.',
    'Nominingue Family Aug19–23 2026 tents/meals,adult150/day520/full,child100/day350/full,<=3free; unit currency/tax unknown. General boys EN proof not automatically wholefamilyEN. No invented2027 dates or medical insurance2018 fee reused ascurrent.',
    'ICO Oaxaca Kids5–12,groups5/6–8/9–12,max6,100%Spanish,June1–Aug21 2026,20hoursMonFri9–13. Price300/560/780/960USD1–4weeks;5thweek gap retained. Deposit55/14day generalFAQ credit rules scoped toKids confirmation. No copied52Monday camp sessions or2027 dates.',
    'Intercultura own2027PDF visuallyread: kids365Heredia/380Samara perweek,adult345/3651–4weeks separately;teen3650two-week all-inclusive. Family page older345/365not treated2027. Ages8–12,Oscar below8;private hourly rate not proof ofunder8camp admission. Heredia schoolapartments forbidunder8;family housingquote separate.',
    'Intercultura Heredia fixedAM/PM vsSamara alternatingAM/PM,parents priority notguaranteed;20hours includesbreaks. Standard150/250nonrefundabledeposit vsgroup/teen20% and cancellation schedules retained. Teen13–17 futuretrack only;price2027 notdate2027, no rolling-session calendar invention.',
    'Brazil Timbalaia ownreader Jan2027 6–17/BRL2940,2450,5130;HTTP403 retained. Acampark direct2027 age5–16/date/package/cancel read,English/Spanish programme and price notknown: no fakeENshortlist. ExistingWildRoots/Makemake bodyrevalidated withoutduplicate dossiers.',
    'SQLite/publicJSON agree, calendar bridge idempotent,104exhibitionICS and all previous2128familyUID/datepairs preserved.102family scenarios,34dossiercountries,0fullyauditedcountries; complete authorised worldwide goal remains active.'
]
byiso={s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','PHL','USA','CAN','CRI','MEX','COL']}
learning=sum(e['block']=='Лагеря' for e in d['events'])
audit=dict(asof='2026-10-05',version=84,status='progress',scope='USA/Canada/CostaRica/Mexico programme-specific general/family/boarding/Spanish camps; all priority regions and full worldwide goal remain active',
    new_dossiers=16,operators_covered=6,updated_dossiers=[],new_calendar_rows=26,new_family_ics=21,reused_existing_calendar_rows=0,
    programme_dossiers=464,countries_with_dossiers=34,official_dossier_urls=727,country_dossier_counts=byiso,programme_slugs=slugs,findings=c['gaps'][-4:],
    calendar=dict(events=len(d['events']),learning_records=learning,family_ics=2149,exhibition_ics=104,managed_dated_rows=len(c['generated_event_ids']),
        reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows']),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
    next_priority='Continue Swiss/French/Spanish/Europe,USA/Canada/CostaRica/Mexico/LatinAmerica,Taiwan/Singapore/Japan/Korea junior/general/technical2026–27 day/boarding/family programmes with full prices/languages/grade/admission/availability; schools/results/routes and worldwide leagues/exhibitions remain in scope')
def write(stem,v):
    t=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(t)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(t)
write('americas-camp-audit-v84',audit)
write('americas-camp-source-receipts-v84',dict(asof='2026-10-05',version=84,
    scope='31 directHTML/PDF attempts:29successful bodies retained/2HTTP403errors. Two own-reader snapshots retained; one2027Intercultura pricePDF visuallyread.403s not relabelled successful programme reads.',
    sources=receipts,web_reader_sources=web,visual_primary_reads=visual,dossier_source_urls_added=newurls,external_actions=external,
    notes=['RawHTML/PDF/provider photographs/web bodies/rendered source images remain outside public repository; public facts/provenance/errors only.',
        'Published dates/grades/fees are not admissions, confirmed places, bookings or full family invoices.',
        'No applications, bookings, payments, organizer messages, subscriptions or new automations.',
        'Full worldwide authorised scope remains active;0fullyauditedcountries.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=84:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',
    evidence='Version83 native publication succeeded: commit3587a9bd56dbfbe98d584fb1bd2d8bf2c32eb4d8; deployment appgdep_6ac3f400b56c819188caf7e8d753028e.16new dossiers/17calendar rows/16familyICS. Goal active; worldwide coverage incomplete.')
plan['latest_validation']=dict(version=84,asof='2026-10-05',status='Independent source/preservation/calendar verification; native publication tracked separately',
    events=len(d['events']),camp_learning_records=learning,programme_dossiers=464,countries_with_dossiers=34,official_dossier_urls=727,
    family_ical=2149,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=byiso)
plan['americas_camp_programme_audit_v84']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=464,countries=34,swiss=69,
    generated_calendar_entries=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'])
for req in plan['requirements']:
    if req['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        req['evidence']='v84:464 programme/grade/format dossiers in34countries;16new dossiers/26dated rows/21familyICS,727dossierURLs. Primary2027 dates/prices vs2026archives,closedwaitlist/currency/foreign/grade/English scope retained; all priority regions and worldwide blocks remain active,0fullyauditedcountries.'
plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05';write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=83','?v=84').replace('data-ui-version="83"','data-ui-version="84"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_americas_camp_audit_v84.json" download>Америка: классы, пансионы и семейные программы ↓</a> · <a href="downloads/STEM_americas_camp_source_receipts_v84.json" download>Источники проверки программ Америки ↓</a> · '
anchor='<a href="downloads/STEM_asia_camp_audit_v83.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=464,new_dossiers=16,new_calendar_rows=26,new_family_ics=21,source_urls=727,goal='active')))
