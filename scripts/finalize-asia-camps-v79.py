"""Record the bounded primary-source pass and maintain the full active scope."""
import json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent / 'stem-family-atlas-work'
PRIMARY = WORK / 'camps-primary-v79'
BASE = '041a7a448142dbfc71a58a19e6640fd7c2cda419'
b = json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d = json.loads((ROOT/'data/catalog.json').read_text())
c = d['camp_programmes']
oldids = {v['id'] for v in b['events']}
oldslugs = {p['slug'] for p in b['camp_programmes']['profiles']}
newslugs = [p['slug'] for p in c['profiles'] if p['slug'] not in oldslugs]
new = [e for e in d['events'] if e['id'] not in oldids]
assert len(newslugs) == 13 and len(new) == 17 and len(c['profiles']) == 389
receipts = [v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts) == 24 and sum(v.get('status') == 200 for v in receipts) == 18
oldurls = {s['url'] for p in b['camp_programmes']['profiles'] for s in p['sources']}
newurls = sorted({s['url'] for p in c['profiles'] for s in p['sources']} - oldurls)
assert len(newurls) == 17 and c['counts']['source_urls'] == 604
external = dict(messages_sent=False, applications_submitted=False, payments_made=False,
                subscriptions_created=False, age_verification_submitted=False)

checks = [
    'All 2604 previous events preserved; all 376 dossier IDs stable. Only Nullspace and Camp SFS dossiers deepened; 13 new programme/age/format dossiers, not 13 independent operators.',
    'S.E.E. 25–29 January 2027: Future Dreamers 3 venues / senior kindergarten–G4; Engineering only Fu Jen / G3–6, G1–2 only after English evaluation. Primary English declaration and fee/insurance/refund rules read; university independently confirms Taipei 321 Jinan Road.',
    'S.E.E. individual/group discount through 11 October 2026 is not an application closing date. Partner-school pricing and foreign admission remain unknown; no purchase/form submission.',
    'Nullspace EV3 5 venue/theme variants on 21–24 / 28–31 December; 4 actual attendance weekdays. AI 6 October12–13 venue/topic workshops; October2 already past and excluded.',
    'Nullspace English and currency ISO remain unconfirmed. EV3 age9–12 vs9–13, 3D9–12 vs9–16, STEM5days vs FAQ4 preserved. MinecraftJune2026 and3DSeptember2026 archives generate no future calendar dates.',
    'FLL Novice30hours/12sessions/no experience distinguished from Main45hours/18sessions/SPIKE Advanced. Explore15 vs20 sessions retained; club listed2027 tournament dates are not training sessions or proof of international eligibility.',
    'OYIS Winter14–18 /21–25 December2026, PreK–G6, full English and Japan/abroad children. Registration opens20October; winter fees/flyer unknown; old winter PDF not reused as current.',
    'English Adventure Summer2026 archive split Grades1–2/3–6; no2027 dates invented. Immersion fluency/English-only policy, lodging correction, baggage extras and cancellation separated from winter birthday cutoff.',
    'Camp SFS class is registered September2026 grade, not recalculated birthdate.75/25 school category does not establish this family admission. SailingG2–5 partner English/fees uncertain; all2026 dates archive.',
    '17 new calendar rows/17 familyICS; prior1939 UID/date pairs preserved;104 exhibitionICS unchanged. SQLite/public JSON agree, bridge idempotent,82 scenarios and0 fullyaudited countries.'
]
byiso = {iso:sum(p['iso'] == iso for p in c['profiles']) for iso in
         ['CHE','FRA','ESP','GBR','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX']}
learning = sum(e['block'] == 'Лагеря' for e in d['events'])
audit = dict(asof='2026-10-05',version=79,status='progress',
    scope='Taiwan/Singapore/Japan/Korea programme-level primary pass; full worldwide competition/exhibition/school/camp objective remains active',
    new_dossiers=13, updated_dossiers=['nullspace','camp-sfs'],new_calendar_rows=17,new_family_ics=17,
    programme_dossiers=389,countries_with_dossiers=c['counts']['countries'],official_dossier_urls=604,
    country_dossier_counts=byiso,programme_slugs=newslugs,findings=c['gaps'][-4:],
    calendar=dict(events=len(d['events']),learning_records=learning,family_ics=1956,exhibition_ics=104,
        managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],
        season_windows=c['integration']['seasonal_windows']),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,
    next_priority='Continue primary programme/price/language audits in all requested countries; dynamic Singapore outdoor and new Korea/Jeju/Busan programmes; USA/Canada/LATAM plus full league and exhibition coverage',
    validation=checks)

def write(stem, value):
    body = json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'data'/f'{stem}.json').write_text(body)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(body)

write('asia-camp-audit-v79',audit)
write('asia-camp-source-receipts-v79',dict(asof='2026-10-05',version=79,
    scope='24 direct HTTP attempts /18 successful HTML bodies; failed HTTP preserved. Own operator pages with raw403 additionally read using web reader; no inferred successful raw fetch.',
    sources=receipts,verified_new_dossier_urls=newurls,
    web_reader_reads=[
        dict(url='https://seecamp.com.tw/product/2027see-winter-future-dreamers-5d/',method='Official product read: grades, three variants, English, price and dated discount'),
        dict(url='https://seecamp.com.tw/product/2027see-winter-esl-engineering-5d/',method='Official product read: G3–6/G1–2 exception, Fu Jen, curriculum, price and English'),
        dict(url='https://seecamp.com.tw/precautions/',method='Own registration/refund/day-insurance terms read; no payment/account/form action'),
        dict(url='https://sg.nullspace.co/contact-us/',method='Own centre addresses read; rawHTTP403 retained'),
        dict(url='https://www.ntucfirstcampus.com/outdoorschool/holiday-camps/',method='Own landing read; dynamic detailed camp list not returned, no programme or date fabricated')],
    external_actions=external,notes=[
        'Successful fetch alone is not full programme audit; claims use actual read primary content, including course duration, venue, year and admission contradictions.',
        'Raw HTML stays outside the public repository; public exports contain fact summaries/source links/error receipts, not provider images or personal child media.',
        '18 successful HTTP bodies plus web reader reads do not establish complete coverage of any country. Editorial selections are family candidates, not external world rankings.',
        'No future sessions from old2026 brochures; no live vacancy, registration acceptance, foreign eligibility or full invoice claimed.'
    ]))

plan = json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version') != 79:
    plan['latest_validation_previous'] = plan['latest_validation']
plan['previous_goal_turn_classification'] = dict(classification='progress',asof='2026-10-05',
    evidence='Version78 native publication succeeded: commit041a7a448142dbfc71a58a19e6640fd7c2cda419; deploymentappgdep_6ac3d2e2cee48191b11306993920ba83.13newdossiers/2deepened/15calendarrows. Goal active; worldwide coverage incomplete.')
plan['latest_validation'] = dict(version=79,asof='2026-10-05',status='preservation/source/calendar verifier passed; native publication follows',
    events=len(d['events']),camp_learning_records=learning,programme_dossiers=389,countries_with_dossiers=33,
    swiss_dossiers=59,french_dossiers=35,spanish_dossiers=28,uk_dossiers=5,
    taiwan_dossiers=23,singapore_dossiers=52,japan_dossiers=17,korea_dossiers=8,
    official_dossier_urls=604,family_ical=1956,exhibition_ical=104,worldwide_complete=False,checks=checks)
plan['asian_camp_programme_audit_v79'] = audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=389,countries=33,swiss=59,
    generated_calendar_entries=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'])
for req in plan['requirements']:
    if req['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        req['evidence'] = 'v79:389 programme/age/format dossiers in33countries;17new dated Asia variants;604official URLs. Programme-specific grades/language/price/year/foreign entry documented. All worldwide blocks retained; country/global completeness unproven.'
plan['status'] = plan['native_goal_status'] = 'active'
plan['updated'] = '2026-10-05'
body = json.dumps(plan,ensure_ascii=False,indent=2)+'\n'
(ROOT/'data/research-plan.json').write_text(body)
(ROOT/'dist/downloads/STEM_research_plan.json').write_text(body)
p = ROOT/'dist/index.html'
p.write_text(p.read_text().replace('?v=78','?v=79').replace('data-ui-version="78"','data-ui-version="79"'))
p = ROOT/'dist/assets/camp-programmes.js'
s = p.read_text()
link = '<a href="downloads/STEM_asia_camp_audit_v79.json" download>Азия: подробные программы и допуск ↓</a> · <a href="downloads/STEM_asia_camp_source_receipts_v79.json" download>Источники проверки Азии ↓</a> · '
anchor = '<a href="downloads/STEM_europe_camp_audit_v78.json"'
if link not in s:
    assert anchor in s
    s = s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=389,new_dossiers=13,new_calendar_rows=17,new_family_ics=17,source_urls=604,goal='active')))
