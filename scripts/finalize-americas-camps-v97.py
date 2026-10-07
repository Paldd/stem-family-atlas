"""Publish scoped retrieval receipts; preserve the full active world objective."""
import hashlib,json,subprocess
from pathlib import Path
from camp_americas_v97 import NEW
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v97'
BASE='18bf9653ad5e00376ba303b9d2994f1873cb0603'
before=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in before['events']};new=[e for e in d['events'] if e['id'] not in old]
assert len(new)==31 and all(e==old[e['id']] for e in d['events'] if e['id'] in old)
assert c['counts']['dossiers']==664 and c['counts']['source_urls']==1046
receipts=[q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(receipts)==25 and sum(q.get('status')==200 for q in receipts)==22
scopes={
 'sciencequest':'Owncompleted2026season/2027unannounced;4actualgradeprogrammes and2knownholidayweeks/fees/100deposit/cancel/lunch. Youngerphysicalalgorithmsnotcomputerprogramming; no2027cohort, teachingEN or actualfamilygradeassumed.',
 'discovere':'Direct403; no ownbody retained/read. Searchsnippetnot admittedasverifiedcurrentprogramme or fee; no newdossier.',
 'calgary-camps':'Owncatalogue/filter, not proofeachcourseofferedall2027weeks. Specificcoursebodiesreadseparately.',
 'pali-home':'Owncurrent2027context/FallPromo2750perregularsession/Oct23withoutyear; notMiniquote or automaticregistrationdeadline.',
 'pali-dates':'Own9regularcohorts2027/7days6nights/includeactivitiesfoodlodging/nospecialtyextrafee. SpecificRoboticsweekavailabilitynotestablished.',
 'pali-news':'Own2027season9regularand9Mini4days3nights. CurrentheaderFallPromo againstexpiredSep28EarlyBirdbody; themesnotroboticscourses.',
 'pali-faq':'Ownregular8–16/room10with2staff/meals/2027insurance150weekandrefundschedule. No automaticMini-contract assumption or independentlyverifiedACAqualityranking.',
 'liota-home':'HTTP200JS/hydrationshell, extractedprogrammebodyempty. Not currentprogramme/price/languagebodyproof; existingdossier unchanged.',
 'english-br-kids':'OwnOctoberJanuary2027Kids4772/4295promo matchesexistingCP101; no tariffupdate, duplicate or eventcorrection.',
 'pali-mini':'Own6–8/fourdays3nights/9intervals/3staff9children/50capacity/sampleday. Year2027explicitlycrosscheckedownnews; general2750notMiniquote or fullRoboticsaccess.',
 'pali-specialties':'Ownspecialtyregistry containsRobotics; specificsyllabusreadseparately. Not allspecialties/foreignadmission fullyaudited.',
 'wenonah-dates':'Direct406; ownsource readthroughwebtool, receiptmethodkeptseparate. No successfulHTTPbodyclaim.',
 'wenonah-home':'Direct406; currentownhome readthroughwebtool, includingbody/tableageconflicts. No successfulHTTPbodyclaim.',
 'sciencequest-faq':'RelevantownFAQ/policies supportingarchivalprogramme audit; no fullmedical/accessibilitycontract review or submittedform.',
 'sfu-summer':'Own2026Burnabygrade-themeweektable;4targettracks/8pastvariants,322fromBurnabyvs186fromSurrey/daylengthcareprices. No2027cohort or preciseprogrammeinvoice.',
 'sfu-faq':'Ownentering2026/27grade/nooldergrade/packedlunch/35adminrefund>week/noRefund<week/10transfer. Noactualfamilygrade or Englishteacherproof.',
 'calgary-early-engineering':'OwnG1–2curriculum andexplicitnoofferings; exampleactivitiesmaychange/enteringfallgrade. Not generic2027filterasexactcohort.',
 'calgary-early-technology':'OwnG1–2circuits/colour-codedrobots/noofferings; exampleactivitiesnotguaranteedfullcourse or teacherEN.',
 'calgary-engineering101':'OwnG3–9/LEGO SPIKE/3D/VR/materials/noofferings; LEGOexplicitnotendorseprogram. Noexact2027cohort/price.',
 'calgary-winter':'Own21–23Dec2026/F26YMWB301/260/Gr3–5againstsidebarentering4/5/6. 13placesretrievalsnapshotnotguarantee; AddToCart notclicked. GeneralwinternotRoboticsintensive.',
 'calgary-spring':'OwngeneralSpringMiniUcontent/noofferings/noageestablished; excludedasnewgraded/futurecohortdossier.',
 'pali-international':'Ownwelcomesforeignfamilies andlinksES/RU descriptions; translatedmaterial notteacherlanguageproof.',
 'pali-spanish':'OwnSpanishpageexplicitlystill2023/Englishpractice andairportdescription; notcurrent2027teachingSpanish/transferrate.',
 'pali-russian':'OwnRussianpageexplicitlystill2023/Englishpractice andairportdescription; notcurrent2027teachingRussian/transferrate.',
 'pali-robotics':'Own8–16curriculum/VEXcode/sensors/autonomousmaze/rescue/engineeringtasks. Noexactweeklyavailability/platform/hoursof2027; internalcontestnotinternationalmedal.'}
assert {q['key'] for q in receipts}==set(scopes)
for q in receipts:
    q.update(retrieval_method='direct_http',content_scope=scopes[q['key']],body_snapshot_retained=q.get('status')==200)
    if q.get('status')==200:
        f=PRIMARY/(q['key']+'.html');assert f.exists() and hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
        q['raw_filename']=f.name
    else:q['content_status']='http_error_no_programme_body'
    if q['key']=='liota-home':q['content_status']='http200_javascript_shell_no_readable_programme_body'
web=[
 ('wenonah-dates-web','https://campwenonah.com/2027-dates-fees/','2027specifictable12cohorts/Dec31age/Weemin5atstart/regular6350/3650/1960/1300/500/HST13%/expiredOct1priority/Wee100tablevs75policies/Apr1balance/cancelboundaryconflicts. Dollarfeecurrencynotexplicit.'),
 ('wenonah-international-web','https://campwenonah.com/welcome-international-campers/','AllteachingandcampEnglish/basicEnglish/otherlanguagesnotpromised/foreignfamilies/complimentaryPearsonarrivaltransport/earlyday/airlineUMnotpaid/weeklyphones. AirportCanadianpocketmoneynotexplicitcampfeecurrency.'),
 ('wenonah-wee-web','https://campwenonah.com/weenonah/','Specific5–7/3days2nights/outdoorartsintro; nottechnicalcamp.2027datesandDec31agefromspecifictable.'),
 ('wenonah-five-web','https://campwenonah.com/odyssey-period-five/','Specific7–12/5days4nights/generalintro; notrobotics.2027ageanddatesfromtable.'),
 ('wenonah-activities-web','https://campwenonah.com/activities/','Relevantoutdoor/water/arts/sport/PICchoice/activitylists read; no advertisedRobotics/AI/codingcourse, not fullsafetyaudit.'),
 ('wenonah-faq-web','https://campwenonah.com/faq/','Relevant5:1staff/8–10children2staff/introversuslongerPIC choices; operatorclaims notindependentranking.'),
 ('wenonah-home-web','https://campwenonah.com/','Current9–15/5–7headersagainstbody8–15/5–6. Specific2027tabletakesprecedence; operatoraccreditationclaimnotindependentverification.')]
f=PRIMARY/'wenonah-web-tool-evidence.txt'
f.write_bytes((PRIMARY/'wenonah-web-tool-return.txt').read_bytes()+b'\n'+(PRIMARY/'wenonah-web-tool-clauses-return.txt').read_bytes())
for key,url,scope in web:
    assert url in f.read_text()
    receipts.append(dict(key=key,url=url,retrieval_method='web_tool_selected_primary_clauses',content_scope=scope,
        content_status='aggregate_tool_return_not_direct_http_body',raw_filename=f.name,bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),
        body_snapshot_retained=False,tool_return_retained=True,raw_snapshot_kind='one_aggregate_of_two_tool_returns_contains_seven_sources_not_seven_http_bodies'))
assert len(receipts)==32
oldurls={s['url'] for p in before['camp_programmes']['profiles'] for s in p['sources']}
added=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls);assert len(added)==25
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False)
countrycounts={s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','BRA','CHL']}
checks=[
 '19newprogramme/formatdossiers across5operators, noexistingdossiercorrection;664total/37countries/1046ownURLs. All645priorIDs/order/dossiercontent preserved.',
 'All3153priorcalendarrecords/leagues/competitions/exhibitions/schools/results/familyroutes retainedexactly.31newfuturecohorts/ICS:18Pali/12Wenonah/1CalgaryWinter.16pastvariantsnotfutureICS.',
 'PaliGeneral8–16/9seven-daycohorts andMini6–8/9four-daycohorts separated;2027MiniyearownNews. General2750promo notMiniquote. Robotics8–16/VEXcode/sensors/autonomousmaze specificoption withoutweekavailability,not9duplicatecohorts. ES/RU2023notcurrentteacherlanguageproof.',
 'Wenonah12futurevariants withDec31 2027age;Weealso5atstart. PeriodFivefitsbothbirthyears. HST13%andregularfees calculated;expiredOct1prioritynotapplied, dollarfeecurrencyunconfirmed. Wee100/75deposit andhomebodyageconflicts explicit; siblings3yearsapartnotcabinmate≤18months.',
 'Queen’s4gradeprogrammes/archive2026fees/cancel/holidayweeks;youngeralgorithmsphysicalnotcomputer. SFUBurnaby4tracks/8pastweeks/gradegate/noolderlevel/322fromvsSurrey186 separated. Englishinterfaceandbirthyearnotteachlanguageoractualgradeproof.',
 'Calgary3engineeringprogrammes noofferings, generic2027filter not exactsessionproof. Winter21–23Dec2026/260/Gr3–5againstsidebarentering4/5/6;13placesretrievalsnapshotnotreservation.',
 '25directattempts:22HTTP200 including1JSshell,3HTTPerrors;7web-toolscopedsourceobservations inoneaggregate retainedreturn. NoPDF/visualchecks/fullsite/countryauditclaim. BrazilOctoberpricealreadyCP101/no duplicate;Liotashell/Alberta403notnewprogrammeproof.',
 'JSONSQLiteCSVJSMDICSconsistency/oldUID/date/deadline preservation/bridgeidempotence/child/language/phasefilters independentlyverified. Worldwideobjective/requirements retained,0fullyauditedcountries/nativegoalactive.'
]
audit=dict(asof='2026-10-05',version=97,status='progress',scope='Canada/USA ownprogramme/age/fee/year evidence and boundedBrazil/Argentina/Alberta rechecks; not completeAmericas/world.',
    new_dossiers=19,new_operator_groups=5,deepened_dossiers=0,updated_dossiers=[],new_calendar_rows=31,new_family_ics=31,new_registration_deadline_ics=0,corrected_existing_event_ids=[],historical_variants_not_added_as_future=16,
    programme_dossiers=664,countries_with_dossiers=37,official_dossier_urls=1046,country_dossier_counts=countrycounts,programme_slugs=NEW,findings=c['gaps'][-4:],
    calendar=dict(events=3184,learning_records=1853,family_ics=2445,exhibition_ics=104,managed_dated_rows=1390,reused_legacy_events=69,season_windows=39),
    primary_retrievals=dict(direct_attempts=25,http200=22,http_errors=3,http200_javascript_shells=1,scoped_web_tool_sources=7,aggregate_tool_return_files=1,actual_pdfs=0,visual_page_checks=0),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
    next_priority='Continue worldwide2026–27 general/thematic/robotics/AI/day/residential/familycampinventory, deepCHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatinAmerica. Verify programmecurrentseasonteachingEN/ES/RU andsupportroles, individualforeignintake/currentplaces/actualDOB-grade, detailedsyllabus/hours/levels, completeinvoice/contract/transport, campuscoordinates/map andfamilycomparisons. Keep leagues/competitions/exhibitions/admission/schools/results5–10years/familyroutes active; no country fullyaudited.')
def write(stem,value):
    txt=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(txt)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(txt)
write('americas-camp-audit-v97',audit)
write('americas-camp-source-receipts-v97',dict(asof='2026-10-05',version=97,scope='25directattempts,22HTTP200includingemptyJSshell,3errors;7scopedwebsourceobservations retainedinoneaggregate tool-return. Not fullsites/operators/country audit.',sources=receipts,dossier_source_urls_added=added,external_actions=external,
    notes=['Direct406Wenonahfollowedbyownweb-toolread,notHTTP200claim. SharedaggregatehashdoesnotmeansevenindependentHTTPbodies.',
           'Englishinterface/translatedES-RU2023pagesnotconfirmed2027teacherlanguage. Exactgradesnotinferredfrombirthyears. Dollarfeecurrencyunconfirmedwhereprimarynotexplicit.',
           'RawHTML/toolreturns remainprivateoutsidecheckout;publiconlyparaphrases/URLs/hashes/scopedreceipts. Noform/payment/booking/contact;0PDFs/visualchecks.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=97:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',evidence='v96nativepublication succeeded; commit'+BASE+'; deploymentappgdep_6ac44f2060a48191b1b0338787b6bd89. Fullworldwideobjectivepreserved.')
plan['latest_validation']=dict(version=97,asof='2026-10-05',status='Independentprimary/preservation/calendarverification; nativepublicationreceiptseparate',events=3184,camp_learning_records=1853,programme_dossiers=664,countries_with_dossiers=37,official_dossier_urls=1046,family_ical=2445,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=countrycounts)
plan['americas_camp_programme_audit_v97']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=664,countries=37,swiss=86,generated_calendar_entries=1390,reused_legacy_events=69)
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        q['evidence']='v97:664programme/venue/formatdossiers in37countries,1046dossierURLs;19new across5operators/31futurecohorts/ICS. Canada/USAcurrentage/fees/HST/2027dateand2026archive/grade/languageproof,16pastvariantsnotfutureICS. Brazilcurrentpromoalreadyentered, no duplicate. Fullworldobjectiveactive.'
entry=dict(version=97,asof='2026-10-05',status='progress',scope=audit['scope'],new_dossiers=19,deepened_dossiers=0,new_calendar_rows=31,corrected_existing_calendar_rows=0,new_family_ics=31,official_primary_sources=25,not_complete_worldwide=True)
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=97]+[entry]
plan['next_research']=[audit['next_priority']];plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05'
write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=96','?v=97').replace('data-ui-version="96"','data-ui-version="97"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_americas_camp_audit_v97.json" download>Канада и США: пансионы, STEM, классы и смета ↓</a> · <a href="downloads/STEM_americas_camp_source_receipts_v97.json" download>Проверенные страницы и ограничения источников ↓</a> · '
anchor='<a href="downloads/STEM_france_spain_camp_audit_v96.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=664,new_dossiers=19,new_calendar_rows=31,new_family_ics=31,source_urls=1046,goal='active')))
