"""Public source receipts and bounded progress for the Swiss/French/Spanish pass."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v82'
BASE='8bac850381d6661e830b6f030e23f7490d970ac2'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
oldslugs={p['slug'] for p in b['camp_programmes']['profiles']};oldids={e['id'] for e in b['events']}
slugs=[p['slug'] for p in c['profiles'] if p['slug'] not in oldslugs]
new=[e for e in d['events'] if e['id'] not in oldids]
assert len(slugs)==17 and len(new)==39 and len(c['profiles'])==432
receipts=[v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts)==36 and sum(v.get('status')==200 for v in receipts)==33
for v in receipts:
    if v.get('status')==200:
        f=next(PRIMARY/(v['key']+ext) for ext in ['.html','.pdf'] if (PRIMARY/(v['key']+ext)).exists())
        v['body_snapshot_retained']=hashlib.sha256(f.read_bytes()).hexdigest()==v['sha256']
        v['raw_filename']=f.name if v['body_snapshot_retained'] else None
        if not v['body_snapshot_retained']:
            v['snapshot_note']='Earlier kidooland-holidays key body overwritten by later /holidays read; original HTTP/hash receipt retained, but original bytes unavailable. French page also independently read under kidooland key; not a byte-equivalence claim.'
assert sum(v.get('body_snapshot_retained') is True for v in receipts)==32
assert sum(v.get('body_snapshot_retained') is False for v in receipts)==1
oldurls={s['url'] for p in b['camp_programmes']['profiles'] for s in p['sources']}
newurls=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls)
assert len(newurls)==28 and c['counts']['source_urls']==681
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,subscriptions_created=False)
checks=[
    'All2741previous events and415dossier IDs/content preserved.17new programme/age/format dossiers for8operators, not17independentcamps.39new calendarrows/39familyICS additions; coding workshop has no second weeklyICS.',
    'ENSR own2027 dates/prices/Junior8–11 read; linkedPDF visually verified2026. Insurancecurrent EU/EEA/Switzerland vs archivedalloutsideSwitzerland retained. Transferunit ambiguous,22periods/week vs88examlessons not a promisedcertificate. GeneralMultisportEnglish unknown.',
    'CJSA own language9–17 andJunior8–10 override network8–17. Six2027weeks only, Aug1–7 gap preserved. Board/day prices differ, junior3weekday1500 verified. Dailyattendanceweekdays not invented, FAQ08:30–18 and two-building allocation retained. Cancellationboundaries incomplete, healthcredit notcashrefund.',
    'Braunwald7starts +publishedSunday/Saturdayrule generate14one-week variants forJunior andFamily; airportSundayreturn notsilentextension. Junior8–17 vsFamily6–17 retained:under8course/supervision/childfee unconfirmed. Adult500workation lacksactivities and is notwholefamilyprice;800/1400/1800packages differ; malformedmultiweektable notinterpreted.',
    'Braunwald optionalcoding English/minimum3/ownlaptop,3MonWedFribeginnerwebsiteworkshops/+150. Technicaldossier linked tobaseprogramme without duplicateICS. ENcoding does not prove ENallcamp activities orchild6codingadmission.',
    'Altitude day6–14 vsresidential7–14; own dates/prices lackyear, booking©2025/birthdatewindows do notprove2027. Noinferred2027ICS; insurance notprovided. Day975/950 andboard2950/5550/7750/9950 retained asyearunknown.',
    'Bell3exactExplorer4–10dates2026/27,half415/full725,lunch stated;Winter/Springhours09–12:30/09–17 butAutumnhours unknown. Webterms are notcampcancellationcontract. BCParis4PrimarydatesCE1–CM2/799, notsecondary8weeks/3–18brochure;birthyear notgrade. ColdlunchBYO,currentloyalty50 vsbroadPDF80 retained.',
    'KidooLand3tracks4–6/6–8/8–14 vsEnglishordinary4–12/fewleaders12–16; Englishwholeteaching andinternationalholidaymakers confirmed. Newcampbrochurecomingsoon,fees/medicalrequirements retained;weeklyvs3day/Christmasclosures notfilledwithschoolholidaydates.',
    'EnglishSummerTECH8–15/min10,15hEN+15hrobotics,WeDo8–11/Mindstorms12–15;FAQ905/8days hasnoyear. Multiactivity5–15,Alive6–14vs5–14;paymentpage2025 not2027terms. RelatedL006 unchanged, nonewICS; technicalinstructionEN/ESunknown.',
    'Fullprevious2073familyICS UID/datepairs and104exhibitionICS preserved. SQLite/publicJSON agree;bridgeidempotent,94familyscenarios,0fullyauditedcountries. Fullworldwidegoal/prioritycountries/all2026–27generalthematicseasons remainactive.'
]
byiso={s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','COL']}
learning=sum(e['block']=='Лагеря' for e in d['events'])
audit=dict(asof='2026-10-05',version=82,status='progress',
    scope='Swiss/French/Spanish general, boarding, family and optional technical programmes; all worldwide blocks and priority countries remain active',
    new_dossiers=17,new_operators=8,updated_dossiers=[],new_calendar_rows=39,new_family_ics=39,reused_existing_calendar_rows=0,
    programme_dossiers=432,countries_with_dossiers=33,official_dossier_urls=681,country_dossier_counts=byiso,
    programme_slugs=slugs,findings=c['gaps'][-4:],
    calendar=dict(events=len(d['events']),learning_records=learning,family_ics=2112,exhibition_ics=104,
        managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows']),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
    next_priority='Continue Swiss/French/Spanish unresolved operators/new2027catalogues and full Taiwan/Singapore/Korea/Japan/USA/Canada/CostaRica/Mexico/LatinAmerica/Europe programmes, allgeneral/thematicday/boarding/familyseasons, schools/results and leagues/exhibitions')
def write(stem,v):
    t=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(t)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(t)
write('europe-camp-audit-v82',audit)
write('europe-camp-source-receipts-v82',dict(asof='2026-10-05',version=82,
    scope='36directHTTPattempts,33successfulHTML/PDF,3timeoutsretained;32successfulrawbodiesretained,oneearlierbodyoverwrittenbyreusedresearchkeywithoriginalmetadataonly. Separateownpagewebreader succeeded forBCPrimary andcached2pagePDF, PDFscreenshotfailedcachemiss',
    sources=receipts,dossier_source_urls_added=newurls,
    web_reader_sources=[dict(url='https://www.britishcouncil.fr/anglais/enfants/primaire-stages',method='Ownprogramme webreader text cached outsidepublicrepo; directHTTPtimeout notconvertedto200'),
        dict(url='https://www.britishcouncil.fr/sites/default/files/stages_anglais_2026_2027_web.pdf',method='Linkedown2pagePDF cachedreader;directPDFopenfailed,clickreaderworked;tablescreenshotcachemiss, no visualtableclaim')],
    visual_primary_reads=[dict(url='https://cdn.prod.website-files.com/6964c7b4ab6723b37f5f5366/69a572f1eb362d7af8bf982f_summer_camp_application_form_2026.pdf',pages=[1],method='Poppler renderedandread:body2026dates,notnew2027contract')],
    external_actions=external,notes=[
        'Raw providerHTML/PDF/childphotos andrenderedimages stayoutsidepublicrepo;onlyfacts/provenance/errors public.',
        '17dossiers cover8operators andmultipleage/format/coursechoices;noexternalworldranking/comprehensivecountryclaim.',
        'Noassignedcourse,confirmedvacancy,application,booking/payment ororganizercommunication.',
        'Family6–17providerstatementisconditionalchildprogrammeeligibility;schoolgradeandexactbirthdateunknown. Optionalcoding isnotwholecamprobotics.',
        'Fullauthorizedworldwidegoalpreserved;0fullyauditedcountries.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=82:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',
    evidence='Version81 nativepublication succeeded: commit8bac850381d6661e830b6f030e23f7490d970ac2; deploymentappgdep_6ac3e57da5988191b3b15508be0b3d85.13newdossiers/10calendarrows/7familyICS. Goalactive; worldwidecoverageincomplete.')
plan['latest_validation']=dict(version=82,asof='2026-10-05',status='preservation/source/calendar verifier passed; native publication tracked separately',
    events=len(d['events']),camp_learning_records=learning,programme_dossiers=432,countries_with_dossiers=33,official_dossier_urls=681,
    family_ical=2112,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=byiso)
plan['europe_camp_programme_audit_v82']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=432,countries=33,swiss=69,
    generated_calendar_entries=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'])
for req in plan['requirements']:
    if req['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        req['evidence']='v82:432programme/age/formatdossiers in33countries;17newdossiers/8operators,39newcalendar/familyICS,681dossierURLs. Exactage/grade/language/foreign/year/feeconflicts retained;allpriorityregions/worldwideblocks remainactive,0fullyauditedcountries.'
plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05';write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=81','?v=82').replace('data-ui-version="81"','data-ui-version="82"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_europe_camp_audit_v82.json" download>Швейцария, Франция, Испания: программы и условия ↓</a> · <a href="downloads/STEM_europe_camp_source_receipts_v82.json" download>Источники проверки этих программ ↓</a> · '
anchor='<a href="downloads/STEM_europe_camp_audit_v81.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=432,new_dossiers=17,new_calendar_rows=39,new_family_ics=39,source_urls=681,goal='active')))
