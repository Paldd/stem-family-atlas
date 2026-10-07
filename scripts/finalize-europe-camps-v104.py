"""Source receipts and scoped research continuity; publication has its own receipt."""
import hashlib,json,subprocess
from pathlib import Path
from camp_europe_v104 import CHECKED,NEW
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v104'
BASE='22b81c011ffbf31d33a1b6c1f5f428d44b1c4eef'
old=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
before={e['id']:e for e in old['events']};fresh=[e for e in d['events'] if e['id'] not in before]
assert len(fresh)==22 and all(e==before[e['id']] for e in d['events'] if e['id'] in before)
assert c['counts']['dossiers']==758 and c['counts']['source_urls']==1180
scopes={
 'ensr-holiday':'Actual autumn2026 and spring/summer2027 day dates; agegroups2.5–6/6–10, outside school admission, from135/95/60CHF. EntirelyEnglish appliesonlyAI13–18 FutureMakers1250/max12/min6; not generalcamp language. No2027generaltheme yet.',
 'ensr-form-young':'Actual public unsubmitted autumn2026 form;135/95/60CHF, outside pupils,36monthminimumcontradiction, earlierstart/julycopyerrors,insurance/absence/cancellation/publicityimageclause; no2027contract.',
 'ensr-form-older':'Actual public unsubmitted autumn2026 form;140CHF/day not135, outsidepupils,Octoberdates/JulcopyandWednesday21error; paymentbeforefirstday,absence/cancellation/ownmedicalaccidentliabilityinsurance/publicityclause. Not2027newcontract.',
 'tandem-holiday':'Actual ownschoolpupilsonly,4–10/ENDEFRteam,2027Feb15–19/22–26/Apr26–30/May3–5/Jul19–23; oldflyerexamples not2027admission. Gap not openfamilycamp.',
 'eisb-index':'ActualJuly2027 fourcoursebirthcohorts;Babyonlyschoolpupils. Linkedpricecalendar2026 not2027datedsession.',
 'eisb-chess':'ActualJuly2027/2019–2012/chessintrobuildingcoding/specialweeks/pool/freecare/outerfamilies. Noexplicitrobotlanguage or2027specificweeks; earlybird2026andimage2026 not2027fee.',
 'eisb-science':'ActualJuly2027/2019–2012/experimentsandprojects/directEnglishteachers/freecare/outerfamilies; samepriceanddatesgaps.',
 'eisb-english':'ActualJuly2027/2022–2012/Englishimmersion/outerfamilies/freecare/halfvsfullday; outdated2026earlybird and no2027fullfee.',
 'eisb-spanish':'ActualJuly2027/2020–2014/activitiesentirelySpanish/outerfamilies/freecare; age bybirthyear not inferredgrades; no2027exactweeksorfullfee.',
 'ecolem-summer':'Actual3–7/100percentENincludinglunch/nativeleaders/1:8ownclaim/outsidepupils/Jul5–9/12–16 2027second4dayswithoutmissingday. Prices395/335external345/280ownstillJul6–10/13–17 oldcalendar;care90/16vs16:30/ownlunch, no guaranteed2027invoice.',
 'techspark-robotics':'ActualLEGO6+English/Arduino12+hardware100CHFtakehome/PrimarilyEnglish; generic2027locationdatepicker not actualnewdatedLEGOspecificcohort. Existingdossier unchanged.',
 'numerique-camps':'ActualCampus26LePuy2026–27robot8–14threeafternoons60EUR/CodeGaming11+singlefullday60;ENESRUteacherunestablished, not eligiblefamilylanguagecalendar.',
 'sanpatricio-home':'Actualschoolhomepage observedownsummercamplink; no2027specificcampprice or cohort inferred.',
 'sanpatricio-camps':'HTTP200 title-only2114byte InspiredSummerCamps shell afterredirect, no usable programmeclauses; old2022PDF not new2027evidence.',
 'spark-index':'Actual5–11/2027DeepFreeze750Feb15–19/ScienceSport795Apr26–30;HogwartsOct2026fullybooked;SuperheroesApril2026. OwnFAQEnglish/basicrequired/meal/snack/trips/1:8/max20, softerrefundpolicy contradictsnewterms.',
 'spark-deep-freeze':'ActualFeb15–19 2027/5–11/09–16:30/Zürich; programmeoutline expresslybasedonlastyear; ice/crystals/chemistry/iceskating/glass factoryHergiswil vsbookingLuzern. No allcurriculumguarantee.',
 'spark-sport':'Ownlinkedcourse redirectstooldJul13–17 2026/Rotkreuz09–16:30/5–11/science sportandmuseum; programmeexamplelastyear. Newindex2027date not detail2026date.',
 'spark-hero':'ActualApril5–9 2026 only, outlinepastyear; newbooklistApril5 2027 onlystart, not independently readfulldated2027cohort; no invented5dayfuturecalendar.',
 'spark-book-freeze':'Actual750CHF/startFeb15 2027/24spots/max20FAQcontradiction/electronicAuroraart/glassLuzern;strict30plusminus100/15–29half/14orlessnone;manualhold48h vs general72h. No booking submitted.',
 'spark-sport-book':'Actual ownbookinglist index containsApril5 2027Superheroesstart795, not completedatedcoursebody. Schoolafterclass/partyservices not falselycampdossiers.',
 'spark-terms':'Actual strictercampcancellation100CHF/50percent/no14days,24haccidentalminususually25/manual72h,20CHFhourcare/15min;ENorDEonrequest/publicliabilityinsurance. Supersedes softFAQonlysubjectcontractconfirmation; no terms accepted.',
 'xlabs-index':'ActualGeneva8–12/bilingualFREN/Oct19–23 2026SuperEngineers/Feb15–19 2027Forensic;375half/595full5days/ownlunch/25hourcare/PPEjournalcert/snack,fullticketscards. NoZurichLausannedate copied.',
 'hif-spring':'Actual12–17/ENApr10–30 2027/6985CHF/flightsandtransferambiguity/optional300pickup500or1000single/21days20nightsvs14+7/24hsupervision/outdoorscience/datatoEurope/owninsurance. No currentfamilyICS.',
 'hif-spring-de':'ActualGermanMar30–Apr10 2027 contradictsENApr10–30 and21dayduration; same6985/nightcount. No chooseoneunconfirmeddate.',
 'iab-short':'Actual2027indexJun28–Jul30/fiveweeks6–17/ENallclasses/09:30–13:30/familyshow;210feeheadingstillSummer2026. Ownweeklydates2027, not olderlandingdates.',
 'iab-camp':'ActualdetailstillSummer2026 Jun22–Jul24/210/sibling10or15percent/EN/mostteachersES/noexperience/afternoon12plus95three days. Oldterms not guaranteed2027discount oroption;universitySeptemberadmissionsnotcampdeadline.',
}
r=[q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(r)==29 and sum(q.get('status')==200 for q in r)==26
for q in r:
    q.update(retrieval_method='direct_http',content_scope=scopes.get(q['key'],'HTTP403 no body; actual primary web-reader programme/terms retained separately.'))
    if q.get('status')==200:
        f=PRIMARY/(q['key']+'.html');assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
        q.update(body_snapshot_retained=True,raw_filename=f.name,content_status='no_usable_programme_body' if q['key']=='sanpatricio-camps' else 'selected_html_clauses')
    else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body')
web=PRIMARY/'xlabs-web-reader.json'
wr=[dict(url=XL,retrieval_method='web_reader_open_primary',checked=CHECKED,body_snapshot_retained=True,raw_filename=web.name,bytes=web.stat().st_size,sha256=hashlib.sha256(web.read_bytes()).hexdigest(),content_scope=scope) for XL,scope in [
 ('https://xlabs.ch/en/camps/super-engineers','Actual five-day engineering plan: circuits/fan/solarboat/bridges/waterrocket/takehomemodels, not leaguewin.'),
 ('https://xlabs.ch/en/camps/forensic-sciences','Actual five-day detectivework: fingerprints/cryptography/invisibleink/microscopy/simulatedbloodtypes, not roboticsleague.'),
 ('https://xlabs.ch/en/terms','Actual2019effective linkedterms section5b CAMP cancellation >30days50CHF/30–10half/10–0all/medicalcertificateexception/admin50ambiguity and exact10overlap;ageerrorcouldcancelwithoutrefund. Not workshopvoucher14dayrule.')]]
before_urls={s['url'] for p in old['camp_programmes']['profiles'] for s in p['sources']}
added=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-before_urls);assert len(added)==22
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
cc={iso:sum(p['iso']==iso for p in c['profiles']) for iso in ['CHE','FRA','ESP','ITA','GBR','CHN','HKG','FIN','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','BRA','CHL','PHL']}
cal=dict(events=len(d['events']),learning_records=sum(e['block']=='Лагеря' for e in d['events']),family_ics=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text().count('BEGIN:VEVENT'),exhibition_ics=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_text().count('BEGIN:VEVENT'),managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows'])
assert cal==dict(events=3309,learning_records=1978,family_ics=2564,exhibition_ics=104,managed_dated_rows=1515,reused_legacy_events=69,season_windows=46)
checks=[
 '13 new dossiers across7operatorgroups/22exactcalendarrows/21familyplanningICS/0newdeadline/0newseasonwindow; old745dossiers/3287events preserved.758total/39countries/1180URLs/22newURLs;not globalranking orcompletecountry.',
 'ENSRonefamilygeneralcampwithtwoagegroups/10datesnotduplicated;formsautumn135young140older/95morning60afternoon,insuranceandcancellation2026not2027.EntirelyEnglishonlyFutureMakers13–18/1250max12min6;excludedfamilyICS. GenericFrench/EnglishformnotteacherEN.',
 'SparkEnglish5–11/Feb15–19 2027CHF750/Apr26–30CHF795;oneprogramme2026detailcontradiction. Strictterms/bookingcancel100CHF/50percent/no14dvssoftFAQ;hold48vs72h/max20vs24spots. Availabilitysnapshotnotconfirmedbooking. Superheroes2027startalone not future5dayevent.',
 'XLabsGeneva8–12/bilingualFREN/375half595full/ownlunch25care/PPEcert;actual5dayengineeringordetectivecurriculum. NotEnglishonly guarantee. Camp5b2019refund differsworkshoprule/admin50andexact10ambiguous;foreignadmissionnotassumed.',
 'EISBEnglish/Spanishbothbirth2017and2020;robotics/science2012–2019onlyMatvey. ScienceENexplicitdoesnotproveroboticsEN. July2027only/no inventedweeks;2026priceimageandearlybirdnotcurrentfee. Acampadaoneactivitynotfullresidentialcamp.',
 'ÉcoleM3–7/EN100percent/openexternal/2027weeks5–9/12–16second4daysunknownexcludedday;price395335stillJul6–10/13–17/care90hourmismatch/ownlunch. IAB2027index5weeks/EN/6–17but210Summer2026/detail2026siblingsafternoonnotcurrent2027promise.',
 'HIF12–17/6985/20nightsvs14+7/ENApr10–30vsDEMar30–Apr10/flightsincludedscopeand300pickupextra: no exactICS. Tandemonlyschoolpupils not opencamp;Campus26roboticsFrenchpage no ENESRUteacher;SanPatricioredirectshelland2022PDFnot2027programme.',
 '29directattempts/26HTTP200(25selectedHTMLclauses+1titleonlyshell)/3errors/3primarywebreaderfallbackpages retainedoneprivate response. NoPDFthispass. AlloldJSON/SQLschemaandrelationalrows/CSV/ICS/JSfilters/staticlimit independently checked. Allworldobjectiveactive0fullyaudited.'
]
next_priority='Continue worldwide2026–27 general/thematic/STEM camps,day/boarding/family EN/ES/RU, especially CHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatAm. Realfullinvoices/ageDOBandgrades/foreignindividualadmission/teacherlanguagevslessons/life/support/gear/nightcare/refunds/currentplaces. Schools/results5–10years/leagues/competitions/exhibitions/familyroutes remain active;no country fully audited.'
audit=dict(asof=CHECKED,version=104,status='progress',scope='SelectedCHE/FRA/ESP2026autumnand2027winter/spring/summer programmes; programme/contract/date/language conflicts. NotcompleteEurope/world.',new_dossiers=13,new_operator_groups=7,deepened_dossiers=0,updated_dossiers=[],programme_slugs=NEW,new_calendar_rows=22,new_family_session_ics=21,new_family_ics=21,new_registration_deadline_ics=0,new_season_windows=0,corrected_existing_event_ids=[],programme_dossiers=758,countries_with_dossiers=39,official_dossier_urls=1180,country_dossier_counts=cc,findings=c['gaps'][-5:],calendar=cal,primary_retrievals=dict(direct_attempts=29,http200=26,selected_html_bodies=25,unusable_programme_shells=1,retrieval_errors=3,unique_actual_pdfs=0,selected_visual_page_checks=0,primary_web_reader_fallbacks=3),fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,next_priority=next_priority)
def write(stem,value):
    txt=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(txt);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(txt)
write('europe-camp-audit-v104',audit)
write('europe-camp-source-receipts-v104',dict(asof=CHECKED,version=104,scope='29selecteddirectattempts/25HTMLclausebodies/1shell/3errors;3primarywebreaderfallbackpages. Rawbodyprivate;not wholewebsiteorcountryaudit.',sources=r,web_reader_fallbacks=wr,dossier_source_urls_added=added,external_actions=external))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=104:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Research/nativepublication103 succeeded;commit '+BASE+';deployment appgdep_6ac4702ccc7c8191a4724bba7b246a29. Fullworldobjective unchanged.')
plan['latest_validation']=dict(version=104,asof=CHECKED,status='Independent selected-source/preservation/calendar verification; nativepublication receipt separate',events=3309,camp_learning_records=1978,programme_dossiers=758,countries_with_dossiers=39,official_dossier_urls=1180,family_ical=2564,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=cc)
plan['europe_camp_programme_audit_v104']=audit
plan['camp_catalog_integration'].update(asof=CHECKED,dossiers=758,countries=39,swiss=106,generated_calendar_entries=1515,reused_legacy_events=69)
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:q['evidence']='v104:758dossiers/39countries/1180URLs.13newEuropeanprogrammecards/22calendarrows/21familyICS.29directattempts25selectedHTMLclauses1shell3errors/3primaryreaderfallbacks. Programme/pricing/language/age/contractconflicts visible;notcompleteworldwide.'
entry=dict(version=104,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=13,deepened_dossiers=0,new_calendar_rows=22,new_family_ics=21,corrected_existing_calendar_rows=0,official_primary_retrieval_attempts=29,unique_actual_pdfs=0,selected_visual_page_checks=0,not_complete_worldwide=True)
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=104]+[entry]
plan['next_research']=[next_priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED
write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=103','?v=104').replace('data-ui-version="103"','data-ui-version="104"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text();anchor='<a href="downloads/STEM_americas_camp_audit_v103.json"'
link='<a href="downloads/STEM_europe_camp_audit_v104.json" download>Европа: подробные программы и условия ↓</a> · <a href="downloads/STEM_europe_camp_source_receipts_v104.json" download>Проверенные источники Европы ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=758,new_dossiers=13,new_calendar_rows=22,new_family_ics=21,source_urls=1180,goal='active')))
