"""Publish bounded research receipts and preserve the expanded active objective."""
import hashlib, json, subprocess
from pathlib import Path
from camp_france_spain_v96 import NEW, UPDATED
ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT.parent/'stem-family-atlas-work/camps-primary-v96'
BASE = '0efdae1af263aba021ffdcfbbf3240049eb952ef'
before = json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d = json.loads((ROOT/'data/catalog.json').read_text());c = d['camp_programmes']
old = {e['id']:e for e in before['events']}
new = [e for e in d['events'] if e['id'] not in old]
assert len(new)==13 and all(e==old[e['id']] for e in d['events'] if e['id'] in old)
assert c['counts']['dossiers']==645 and c['counts']['source_urls']==1021
receipts = [q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(receipts)==37 and all(q.get('status')==200 for q in receipts)
scopes = {
 'pueblo-kids':'Own Kids8days/7nights/7–12/July2027comingsoon;890EURwithoutyear,300reserveinsidefee. Not dated2027cohort or confirmedseasoninvoice.',
 'pueblo-kids-faq':'Relevant language, leveltest, 1:8staff, meals/boarding/Madridreturnbus/insurance/devices/medicaldocument clauses read. Fullrefundpolicy and passportalternative not established; no formsubmission.',
 'pueblo-ai':'Own school-yearonline supplement8–18/English10lessons/245group420individual210recorded;13Octoberwithoutyear or timezone. Not physicalholidaycamp or exactdated2026cohort.',
 'pueblo-ai-demo':'Actual2pageown demo, English/Spanish prompts and codecomments, target12–14 despitecourse8+. SnakeHTML/CSS/JS/Gemini sample not fullsyllabus. Embedded instructions not executed.',
 'pueblo-kids-venue':'OwnElFresnoÁvila facility/accommodation/activity descriptions; not proof2027places/foreignindividualadmission.',
 'ymca-priego':'Ownteaser2027 but actual2026dates/2010–2015campers/1340regular andexpired1200early.940LIT2009notyoungCamperfee; includedbus/food/materials/insurance read.',
 'ymca-salduero':'Ownteaser2027 but actual2026dates/2013–2019/810ten-day560seven-day, expired730/500early. Matveybirth2017candidatearchive, Oscar2020excluded. No automatic2027gate.',
 'ymca-terms':'Relevant NationalCamps2026 management100insidefee/balanceJun1/cancel/minparticipation clauses read. Separateinternational500management not applied to Spanishnationalcamps. No paymentinstructions followed.',
 'ymca-priego-family':'Actual25page2026familymanual retained/extracted as supportingarchive. Not claimed fullmanual or medicalpolicy audit; specificdated/fee/agefacts taken fromownprogramme andNationalterms.',
 'olocau-english':'Own31Jul–6Aug2027/6–14/twotracks/same250capacity/Englishstaff/group10; Fluentnotbeginnercourse. Fee/invoice unknown; January7generalopeningyearnotprinted, not exactdeadline.',
 'olocau-form':'Ownblank registrationnotice: returningNov2 2026/generalJan7withoutyear. No personalfields/Next/submission or placesconfirmation.',
 'olocau-facilities':'Ownconnectedmonitorrooms/shower/heating/fencedgrounds/outdoors/observatory; studentroomlinen/towelsnotincludedfacilitystatement, campcontract inclusionstillunknown. Facilitynotguaranteedastronomylesson.',
 'olocau-location':'Ownlocation description, not independentlyverifiedtravel-time or exactcampuscoordinates.',
 'olocau-staff':'Ownstaff/supervision statements, not independentbackgroundcheck, accreditation or qualityranking.',
 'vaughan-plain':'HTTP200redirects togeneralchildrenlanguagecourse. No currentcampbody/placesdates admitted fromredirect or cachedsearchclaim.',
 'vaughan-summer':'HTTP200redirects togeneralchildrenlanguagecourse. Queryvariant not secondcamp or currentcampavailabilityevidence.',
 'vaughan-catalogue':'Actual31page2026PDF; relevantpages1/2/8/9/15–21/29/30read. Page8visuallychecked; locationprices16/18/20textread:Bravo880/1590,Mazo1685,Kiriko930/1760. Housing,5hEnglish,Nationalcancel clauses read; not all31pages audit or2027rates.',
 'chester-general':'OwnESresidential2027age8–17 butdayblock2026; dates2027unannounced. ExistingENprofiledeepened, not replaced by staleattachedfeePDF.',
 'chester-mini':'Owncurrent2027birth2019–2023/3–7/8/up-to2Primary/English/12group/pool2–5/openDec1 2026. Datesprices2027unknown, linkedfeePDF2026.',
 'chester-mini-fees':'Actualimage-only1page2026PDF, page1visuallyread selectedfees/250reserve/siblings/earlylate clauses. Not2027price, fullcontract or OCRbody.',
 'chester-board-fees-es':'Actualimage-only1page2026PDF, selectedvisualfees/500reserve/50airport/Jun1balance. ConflictswithEN750/60, not treated ascorrectreplacement or2027contract.',
 'chester-day-fees':'Actualimage-only1page2025PDFlinkedfromESdaypage; selectedvisualtitle/fees read. Not2026/27rate.',
 'chester-board-fees-en':'Actualimage-only1page2026PDF, selectedvisual2225/3865/750reserve/60airport/30train/dates read. Not2027rate or supersededbyES.',
 'chester-day-fees-en':'Actualimage-only1page2026PDF, selectedvisual1150/1950/750reserve/May1balance/bus70/140/early50/100 read. No payment/form.',
 'kidooland-camps':'Currentownlevels/Englishteaching/Frenchfreeplay/visitorfamilies rechecked; existing3dossiers unchanged, not duplicated.',
 'kidooland-brochure':'Own2027brochurecomingsoon; not proofnewdates/fees. Existingdossiers preserved.',
 'ermitage-camps':'OwnexistingOctober2026/FebruaryAprilSummer2027calendar rechecked; existingdossier/calendar unchanged, not countedasnewresearchcohort.',
 'ermitage-form':'Ownlinkedpublicblankform GET selectedage/languageleader/2026feeclauses rechecked. No fields/consent/submission; Englishleaderpreference notguarantee. Existingdossier preserved.',
 'marymount-provider':'Own2026archive3–16general/primary3–11/English/575/120day/110late, distinctPDF120late preserved; no2027cohort.',
 'sswp-index':'OwnnativeEnglish/wholeactivitylanguage/externalstudent clauses; operatorCambridgeEnglishProgram not independentlyvalidatedaccreditation.',
 'sswp-jardins':'Ownfuture5cohorts/3–11/550/120/30late/150week/picnic; Feb2027site againstPDFform2026typo. Parkpass45insidefee notdoublecharge.',
 'sswp-pcc':'Ownfuture4cohorts/primary3–11 vssecondary/sports;575/120day/110late/90bus. PDF130late andprimary15:30vs16 conflict retained.',
 'sswp-racing':'OwnOct2cohorts/primary3–11/550/110day/80late90bus; EnglishprimaryagainstFrenchgolfstaff andprimaryPDFgolfafternoons. CompleteEnglishimmersion not established.',
 'sswp-marymount-pdf':'Actual7page2026brochure: primaryprogramme andspecificfees575/120day/120late read; notall7pagesfullaudit. General3–15/16notoverridemainprimary3–11.',
 'sswp-jardins-pdf':'Actual4pages; relevantprogramme/sampleday/fees read, page4visuallychecked.330Dec/25late/park45insidefee; Feb2026form conflictscover2027. No consent/paymentfields.',
 'sswp-pcc-pdf':'Actual8pages; relevantprimarysample/fees read, page7visuallychecked.130latevs110HTML;275halfdaynotappliedtoprimary. No personaldata/formsubmission.',
 'sswp-racing-pdf':'Actual6pages; relevantprimarysample/Frenchgolf/550/120day/80late/90bus textread. Page3rendered but not countedvisuallyread. NotfullENmoduleproof; formnotfilled.'}
assert {q['key'] for q in receipts}==set(scopes)
for q in receipts:
    f = PRIMARY/(q['key']+'.pdf')
    if not f.exists(): f = PRIMARY/(q['key']+'.html')
    assert f.exists() and hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
    q.update(retrieval_method='direct_http',content_scope=scopes[q['key']],raw_filename=f.name,body_snapshot_retained=True)
    if q['key'] in ['vaughan-plain','vaughan-summer']: q['content_status']='redirect_general_course_not_camp'
    if f.suffix=='.pdf':
        info = subprocess.check_output(['/opt/homebrew/bin/pdfinfo',str(f)],text=True)
        q['pdf_metadata'] = {line.split(':',1)[0]:line.split(':',1)[1].strip() for line in info.splitlines() if line.startswith(('Title:','Pages:','CreationDate:','ModDate:'))}
bykey = {q['key']:q for q in receipts}
for f in sorted(PRIMARY.glob('*-observed.txt')):
    key = f.name.removesuffix('-observed.txt');q = bykey[key]
    receipts.append(dict(key=key+'-observed',url=q['url'],retrieval_method='pdf_visual_selected_clauses',content_status='selected_observation_not_ocr_or_full_pdf',
        content_scope=q['content_scope'],raw_filename=f.name,bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),body_snapshot_retained=True))
assert len(receipts)==45
oldurls = {s['url'] for p in before['camp_programmes']['profiles'] for s in p['sources']}
added = sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls);assert len(added)==29
external = dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False)
countrycounts = {s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','BRA','CHL']}
checks = [
 '14newdossiers across6operatorgroups, 1Chesterexistingdossierdeepened.645total/37countries/1021ownURLs, 631priorIDs/order and630unrelateddossiers preserved.',
 'All3140priorcalendarrecords/leagues/competitions/exhibitions/schools/results/familyroutes retainedexactly.13newfuturecohorts/ICS, 24pastvariantsnotcopiedinto2027. Onlineyearlessstartnotcalendarcohort.',
 'SSWP11futurecohorts:5Jardins/4PCC/2Racing. JardinsFeb2027cover/HTMLvsform2026 retained;330Dec andpark45insidefee. Late25/30Jardins,110/130PCC,110/120Marymount/day110/120Racing conflicts explicit. GolfFrenchstaffandprimaryafternoonsnotfalsefullEN.',
 'Olocau6–14/twotracksonecamp31Jul–6Aug2027/250sharedcapacity;FluentforEnglishfluentnotbeginner. Price/contractunknown. GeneralJan7withoutyearnotdeadline. Linenfacilitystatementnotcampinvoiceguarantee.',
 'PuebloKids7–12/8days7nights/July2027undated/890withoutyear/300insidefee. EduplAI8–18Englishonline10lessons245/420/210, demo12–14bilingualmaterial,13Octwithoutyear/timezone. Distinctonlinefilter; notphysicalcamp/roboticsmedal.',
 'Vaughanactual31page2026catalogue locationprices880/1590Bravo,1685Mazo,930/1760Kiriko;relevanthousing/cancelclauses. CurrentcampURLsredirectgeneralcourse. YMCA2026birthgates/regularprices/expiredpromos/100nationaladmininsidefeevs500international separated.',
 'ChesterMINIcurrent2027birth2019–2023 fitsOscar,notMatvey; 2026PDFbirth2018–2022notnewgate. GeneralES2027age8–17vsENarchive8–18. Fiveimage-onlyfeePDFpagesselectedvisually; 750/500reserve,60/50airport andMay/Junbalancesnotaveraged. ESdayPDF2025excludedascurrentprice.',
 '37directretrievalsHTTP200 include2generalcourseredirects,12actualPDFs withscopedpagechecks and8selectedvisualobservations. No fullPDF/site/countryauditclaim. RawHTML/PDF/forms/renders privateoutsidecheckout;publiconlyparaphrases/URLs/hashes.',
 'JSONSQLiteCSVJSMDICSconsistency/oldUID/date/deadline preservation/bridgeidempotence/language-child-phase-onlinefilters independentlychecked. Worldwideobjective/requirements retained,0fullyauditedcountries/nativegoalactive.'
]
audit = dict(asof='2026-10-05',version=96,status='progress',scope='France/Spain own2026–27general/boarding/dayprogrammes and school-yearonlinesupplement; boundedprogrammeaudit, not completeEurope/world.',
    new_dossiers=14,new_operator_groups=6,deepened_dossiers=1,updated_dossiers=UPDATED,new_calendar_rows=13,new_family_ics=13,new_registration_deadline_ics=0,corrected_existing_event_ids=[],
    historical_variants_not_added_as_future=24,programme_dossiers=645,countries_with_dossiers=37,official_dossier_urls=1021,country_dossier_counts=countrycounts,programme_slugs=NEW,findings=c['gaps'][-4:],
    calendar=dict(events=3153,learning_records=1822,family_ics=2414,exhibition_ics=104,managed_dated_rows=1359,reused_legacy_events=69,season_windows=39),
    primary_retrievals=dict(direct_attempts=37,http200=37,general_course_redirects=2,actual_pdfs=12,selective_visual_observations=8,visual_page_checks=8),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
    next_priority='Continue worldwide2026–27 general/thematic/robotics/AI camp/boarding/day/familyprogrammeinventory, deepCHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatinAmerica. Verify programme-specificteachingEN/ES/RU andsupportroles, foreignindividualintake/currentplaces, actualDOB/grade, syllabus/hours/level, completecurrentseasoninvoice/contract, campuscoordinates/map andfamilycomparisons. Keep leagues/competitions/exhibitions/ageadmission/schools/results5–10years/familyroutes active; no country fullyaudited.')
def write(stem,value):
    txt = json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'data'/f'{stem}.json').write_text(txt)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(txt)
write('france-spain-camp-audit-v96',audit)
write('france-spain-camp-source-receipts-v96',dict(asof='2026-10-05',version=96,scope='37directHTTP200attempts incl2generalcourseredirects;12actualPDFs withrelevantselectedclauses,8visualpagereadobservations. Notfullsites/PDFs/operators/countriesaudit.',sources=receipts,dossier_source_urls_added=added,external_actions=external,
    notes=['Archiveprices/terms/birthgates2026 anddayPDF2025notcurrent2027quotes; uncertainyears not inferredintoICS.',
           'Visualobservations selectedclauses, notOCR/fulltranscripts; instructionsinsideforms/demo PDFs not followed. Rawpayment/bank/form/sourcecontentremainsprivate.',
           'ConfirmedEnglishteaching distinguishedfrommodulelanguage/Englishinterface/Spanishsupportmaterial. Operatorsqualityclaimsnotindependentworldranking.']))
plan = json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=96:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification'] = dict(classification='progress',asof='2026-10-05',evidence='v95nativepublication succeeded; commit'+BASE+'; deploymentappgdep_6ac4493bd79c819193849cbcfcdf8150. Expandedworldwideobjectivepreserved.')
plan['latest_validation'] = dict(version=96,asof='2026-10-05',status='Independentprimary/preservation/calendarverification; nativepublicationreceiptseparate',events=3153,camp_learning_records=1822,programme_dossiers=645,countries_with_dossiers=37,official_dossier_urls=1021,family_ical=2414,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=countrycounts)
plan['france_spain_camp_programme_audit_v96']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=645,countries=37,swiss=86,generated_calendar_entries=1359,reused_legacy_events=69)
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        q['evidence']='v96:645programme/venue/formatdossiers in37countries,1021dossierURLs;14new across6operatorgroups+1Chesterdeepened;13newfuturecohorts/ICS. France/Spainprimary2026–27programme/fee/language/age conflicts,24archivalvariantsnotfutureICS. Onlinelearningdistinctfromphysicalcamps. Fullworldobjectiveactive.'
entry=dict(version=96,asof='2026-10-05',status='progress',scope=audit['scope'],new_dossiers=14,deepened_dossiers=1,new_calendar_rows=13,corrected_existing_calendar_rows=0,new_family_ics=13,official_primary_sources=29,not_complete_worldwide=True)
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=96]+[entry]
plan['next_research']=[audit['next_priority']];plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05'
write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=95','?v=96').replace('data-ui-version="95"','data-ui-version="96"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_france_spain_camp_audit_v96.json" download>Франция и Испания: программы, языки и полная смета ↓</a> · <a href="downloads/STEM_france_spain_camp_source_receipts_v96.json" download>Страницы и сезонные брошюры ↓</a> · '
anchor='<a href="downloads/STEM_asia_camp_audit_v95.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
s=s.replace("family:'С родителями'","family:'С родителями',online:'Онлайн · учебная программа'")
s=s.replace('День, пансион и семья</option>','День, пансион, семья и онлайн</option>')
p.write_text(s)
print(json.dumps(dict(dossiers=645,new_dossiers=14,deepened_dossiers=1,new_calendar_rows=13,new_family_ics=13,source_urls=1021,goal='active')))
