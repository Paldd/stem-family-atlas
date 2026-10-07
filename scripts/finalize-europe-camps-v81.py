"""Public provenance and bounded-progress receipt for programme-specific Europe pass."""
import json, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parent/'stem-family-atlas-work'
PRIMARY=WORK/'camps-primary-v81'
BASE='1c1ed0c5c34aac0a6c247fa885b16104ac40c4e7'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
oldids={e['id'] for e in b['events']};oldslugs={p['slug'] for p in b['camp_programmes']['profiles']}
newslugs=[p['slug'] for p in c['profiles'] if p['slug'] not in oldslugs]
new=[e for e in d['events'] if e['id'] not in oldids]
assert len(newslugs)==13 and len(new)==10 and len(c['profiles'])==415
receipts=[v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts)==27 and sum(v.get('status')==200 for v in receipts)==23
oldurls={s['url'] for p in b['camp_programmes']['profiles'] for s in p['sources']}
newurls=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls)
assert len(newurls)==19 and c['counts']['source_urls']==653
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,subscriptions_created=False)
checks=[
    'All2731previous events and402dossier IDs/content preserved.13new programme/age/format dossiers, not13independentoperators.10new exactcalendarrows;7familyICS additions. ClosedAutumn and bothchildren-ineligibleoldertracks are excluded from familyICS.',
    'YoYo own embeddedBookacamp cards independently read: FEZJuly6–12 vsAugust8–13, Steglitz8–12, Spanish12–14. General6–14/11–15 pages do not override datedcohorts. Bald buchbar and displayed10+/4female/4male counts are not openbookings or confirmedvacancies.',
    'YoYoAutumn18–24Oct2026 Ausgebucht; Saturdaydeparture specificcamp vs generalFAQFriday. Pricefrom699 retained and closedflag reaches calendar. AGBJan2026 EUR25day/EUR50boarddeposit and cancellation/optionalguarantee recorded; fifteen-dayboundary ambiguous. Soli±15/25 means pricesfrom are not final ordinaryfamilyinvoice.',
    'SalemKids2027 own9–11 cohort/EUR3650/24July–7August/1Novemberopening. BasicEnglish instruction is not EnglishMiniUni or wholecamp. No guaranteedrobotics course claimed.',
    'Landheimform2027 visually read pages2–3: internationalstudentsGermanrule, LEGOrobotics and AIagents optionalactivities, feeEUR2750 inclMunichtransfer, signedcontract+fullpaymentneeded. Mainpage2027/9–14 vs linkedbrochure2026/9–13. Generalcamp calendar retainsgeneral themes despite optionaltechnicalchoices.',
    'LandheimAI14–17 separatefuturetrack: August2027 announcement and promised1October documents stilllinked2026. No inventedexactsession/price/ICS, no inference thatEnglishmodule provesEnglishAImodule.',
    'StGIS own2027 pages: general10–15 vsRobotics12–15/B2. CampI languages/sustainability;CampIIarts;CampIIIrobotics. EUR4180base+400robotics=4580, optionalGolf500/Horse900 extra. Application2027HTTP404 retained;2026terms not transplanted. Staffworkvisa conditions are not camperadmissionconditions.',
    'NewTechKids3own8–12 bilingualNL/ENbootcamps link existingL132/L133/L134 without duplicatedcalendar/ICS. Three actualshortlinks returned403; prices/hours/foreignadmission remainunknown. SubsidizedStadspas is not a generalforeignfamilyprice.',
    'Allprevious2066familyICS UID/datepairs and104exhibitionICS preserved. SQLite/publicJSON agree; bridge idempotent,90family scenarios,0fullyauditedcountries; full worldwidegoal remainsactive.'
]
byiso={s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','COL']}
learning=sum(e['block']=='Лагеря' for e in d['events'])
audit=dict(asof='2026-10-05',version=81,status='progress',
    scope='European programme-specific general/technical boarding/day camps; full worldwide leagues/competitions/exhibitions/schools/familyroutes remain active',
    new_dossiers=13,updated_dossiers=[],new_calendar_rows=10,new_family_ics=7,reused_existing_calendar_rows=3,
    programme_dossiers=415,countries_with_dossiers=33,official_dossier_urls=653,country_dossier_counts=byiso,
    programme_slugs=newslugs,findings=c['gaps'][-4:],
    calendar=dict(events=len(d['events']),learning_records=learning,family_ics=2073,exhibition_ics=104,
        managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows']),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
    next_priority='Continue full Swiss/French/Spanish operators and priority Asian/American junior programmes, allcountry general2026–27 camps, schoolresults and league/exhibitioncoverage; confirm exactforeign/ENgates and fullfamilyinvoices')

def write(stem,val):
    body=json.dumps(val,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'data'/f'{stem}.json').write_text(body)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(body)

write('europe-camp-audit-v81',audit)
write('europe-camp-source-receipts-v81',dict(asof='2026-10-05',version=81,
    scope='27read-only directHTTP attempts;23successfulHTML/PDF,4errors retained. Source summaries derive from read primary programme tables/terms/PDF and preserve archive/current conflicts.',
    sources=receipts,dossier_source_urls_added=newurls,
    visual_primary_reads=[dict(url='https://www.landheim-ammersee.de/sites/default/files/media/downloads/Anmeldung_Summer%20Camp_2027_EN_Formular_0.pdf',
        pages=[2,3],method='Poppler rendered and visually read: internationalGermanrule, optionalLEGO/AI, excursions, EUR2750 andMunichtransfer')],
    embedded_operator_tables=[dict(url=BAC,url_source=src) for BAC,src in [
        ('https://bookacamp.de/de/booking/form/view-by-date/162c63b16e6cec45f83ae6ac3227808f/7','https://www.yoyocamps.de/camps/fun-action-camp-fez-berlin'),
        ('https://bookacamp.de/de/booking/form/view-by-date/162c63b16e6cec45f83ae6ac3227808f/86','https://www.yoyocamps.de/camps/fun-action-camp-berlin-steglitz'),
        ('https://bookacamp.de/de/booking/form/view-by-date/162c63b16e6cec45f83ae6ac3227808f/82','https://www.yoyocamps.de/camps/herbst-camp-im-jugenddorf-am-ruppiner-see'),
        ('https://bookacamp.de/de/booking/form/view-by-date/162c63b16e6cec45f83ae6ac3227808f/78','https://www.yoyocamps.de/camps/spanisch-camp-im-jugenddorf-am-ruppiner-see')]],
    excluded_candidates=[dict(url='https://www.gls-berlin.de/2048.html',reason='Read current2027rate table: EnglishMunichAdventure12–16/EnglishBerlinCollege16–18. HistoricalYoung&Fun7–14 searchPDF2024 is not2027offer to thesechildren.'),
        dict(url='https://newtechkids.com/15454-2/',reason='LinkedAIeducationevent19October2026 addressed teachers/policy/research, not juniorcamp; detailedpage not audited')],
    external_actions=external,notes=[
        'Raw providerHTML/PDF/child photos and renderedimages remain outsidepublicrepo; facts/provenance/errors onlypublic.',
        'SourceURL withexplicit404 documents failure, not a verifiednewadmissionform. Search cache can differ from currentcanonicalownpage.',
        'No place confirmed, no externallyvalidatedworldranking, no comprehensivecountryaudit. Differentage/course/formatdossiers are not differentoperators.',
        'Full authorizedworldwidegoal, allpriorityregions and general/thematic2026–27 seasons preserved.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=81:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',
    evidence='Version80 nativepublication succeeded: commit1c1ed0c5c34aac0a6c247fa885b16104ac40c4e7; deploymentappgdep_6ac3e0b044788191858fddf110b38487.13newdossiers/110calendarrows. Goalactive; worldwidecoverageincomplete.')
plan['latest_validation']=dict(version=81,asof='2026-10-05',status='preservation/source/calendar verifier passed; native publication follows',
    events=len(d['events']),camp_learning_records=learning,programme_dossiers=415,countries_with_dossiers=33,
    official_dossier_urls=653,family_ical=2073,exhibition_ical=104,worldwide_complete=False,checks=checks,
    country_dossier_counts=byiso)
plan['europe_camp_programme_audit_v81']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=415,countries=33,swiss=59,
    generated_calendar_entries=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'])
for req in plan['requirements']:
    if req['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        req['evidence']='v81:415programme/age/formatdossiers in33countries;10newEuropean calendarrows/7familyICS/3reusedlegacyrows;653sourceURLs. Actualage/language/foreign/price/yearconflicts andclosedcamp retained. Worldwideblocks/prioritycountries remainactive; no globalcompletenessclaim.'
plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05'
write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=80','?v=81').replace('data-ui-version="80"','data-ui-version="81"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_europe_camp_audit_v81.json" download>Европа: группы, язык и пансионы2027 ↓</a> · <a href="downloads/STEM_europe_camp_source_receipts_v81.json" download>Источники европейской проверки ↓</a> · '
anchor='<a href="downloads/STEM_americas_camp_audit_v80.json"'
if link not in s:
    assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=415,new_dossiers=13,new_calendar_rows=10,new_family_ics=7,reused_calendar=3,source_urls=653,goal='active')))
