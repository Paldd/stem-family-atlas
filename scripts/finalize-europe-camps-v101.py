"""Publish scoped retrieval evidence and preserve the active worldwide research plan."""
import hashlib,json,subprocess
from pathlib import Path
from camp_europe_v101 import NEW,CHECKED
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v101'
BASE='5237c21f57c3666461a906e9f3686cb0937b4c86'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};fresh=[e for e in d['events'] if e['id'] not in old]
assert len(fresh)==25 and all(e==old[e['id']] for e in d['events'] if e['id'] in old)
assert c['counts']['dossiers']==707 and c['counts']['source_urls']==1111
scopes={
 'bede-home':'Own2027 headline alongside old2026 fields; currentprogramme facts grounded in neweractual2027 summary/terms, notheadline alone.',
 'bede-fees':'InitialHTTPattempt DNSfailure/no body; later sameURL succeeded. No fee fact inferred fromfailedresponse.',
 'bede-brochure-index':'Actual72page2026 prospectus, notHTML. Selectedp19/25 visual plus relevantEnglishhours/age/room text. Notcomplete72pageaudit; archivalrooms/fees/venue notpromised for2027.',
 'sancelso-home':'OwnEnglishoperator overview/age/seasoncontext, notfullcurrent2027contract.',
 'sancelso-summer':'Own6–17/allnationalities/ENcommonstafflanguage/residential/generalartsciencecooking nature programme;2026 nextseasonnotinvented.',
 'italy-sport-info':'Own2027dates/age10–14Cavalese12–16Oclini/680780340fullboardorday/fullpackage/24hcare/medicaldocuments/50interveningnight. First27–02luglio startmonthnotexplicit, excludedfromexactcalendar.',
 'socks-camp':'Own7–10Children10–14Tweens/residential/musicmovement/mother-tongueEnglishweek; nofee/calendar/robotics frombranddescription.',
 'aosr-camp':'OwnEnglishday3–15/openexternaltemporaryvisitor/makerspacecodingrockets/2026fees250450650bus175.2027inprogress/March/closedintake isnotprovensoldout; no2027cohortcreated.',
 'village-home':'Owncurrent2027 destinationsAustriaPortugalSwitzerland, priorprofiles preserved. SearchfoundFranceonlyhistoricalarchives; noFrancecampaddedfrom2013/2015/2019guide.',
 'xuk-residential':'OwnActivityresidential8–17/internationalgroups/generalprogramme. Day3–6/7–12London differentcamp notyoungerboardingexception.',
 'sancelso-dates':'Own2026 exactarchive7951550/mandatory60or120/sibling7551490/bus4590/insurance/300deposit. All-intotals beforeoptionaltravel/pocketmoney calculated, notnew2027invoice.',
 'sancelso-faq':'OwnEnglishstaff/camp-life but externalinstructorsItalianwithENtranslation;agegroups1:10plusyoungintern/rooms/nightstaff/Italyhealthcover/vaccinations/equipment/pocketmoney. Bankingdetails notcopied; noformsentered.',
 'sancelso-day':'Ownweeklystructure/generalactivities/tent-orhutnight/fullboard/4bedrooms/privatebath, nottechnicalintensive.',
 'sancelso-sport':'Ownmandatoryexternalactivities/60or120/Sailing100/agegates;Sailing>8 card vsFAQ8+ remainsunknownexactthreshold.',
 'socks-dates':'Actualbody2027registrationopensJan15 despite2026menulabel; noexactcohort,feeorregistrationdeadlineinferred.',
 'sport-programmes':'Ownlinks totypicalweeklyplans; links notalone proofnewdated2027syllabus.',
 'xuk-dates':'Actual5weekly2027arrivaldepartures butPrices/Packages2026 still1160/2695/3835;2027earlydiscountseparate. Costs notlabelledfinal2027fees.',
 'xuk-faq':'OwnENstaffallcampLife/ActivityvsExcelvsEnglish/foreign40countries2026/1–6dorm/6laundry/three meals/separateinsurance/age8–17. Operatorclaims notindependentinspection.',
 'xuk-venue':'OwnDauntseySchoolWiltshireaddress. Excel venue/activities text notautomaticallyActivityelectivesyllabus.',
 'xuk-activities':'OwnExcelmorningelectivesdistinctfromActivity/English; noExcelcurriculumduplicatedasActivity.',
 'xuk-terms':'Actual8pagePDF selectedp3visual, relevantcontract/insurance/photo/transporttextread. TableMay–July2026 anddepositforfeit notcarriedto2027.',
 'bede-dates':'Actual2027annualwindowsbelow2026heading;LittleJul4–Aug14/FutureBurgessJul11–Aug7. FuturePDFweek6 discrepancy explicit, noAug8–14FutureICS.',
 'bede-faq':'Ownnationality/native-languagecap20percent/transfers/rooms/agedexception;FAQcancel29–41 outdatedcomparedactual2027terms29–55. Noexceptionorlanguagecapavailabilitypromised.',
 'lacunza-2027':'Own2027seasonJun20–Aug8/3formats/activities butfeeplaceholders dashEUR/week remain. Priorprofile unchanged; no2027all-inorindividualweekinvented.',
 'canopee':'Own6exact2026–27periods/5155days2062days/9–17lunch/allEnglishschoolteachers/externalchildren/age3–5,6–11overviewvs6–10themes. Specificthemesnotrobotics.',
 'chester-2027':'Own2027headline8–17butboardingsection8–18/datescomingsoon/feesPDF2026. Priorprofile unchanged; headline notagediscrepancyresolution.',
 'sport-multi-pdf':'Actual1pagePDF visuallyreadtypicalCavaleseclasses/sports/ENgames;ENGLANDSCOTLANDaregroupcolumnsnotcountries. Noownyear/fullcampENstatement.',
 'sport-intensive-pdf':'Actual1pagePDF visuallyreadtypicalIntensivehours/sports/fullENallactivitiesclause. Noownyearprinted, notexact2027dailyplan.',
 'socks-location':'OwnCaDiGianni/BagnoDiRomagna/pooladventureparkMagicalRoom/woods; no2027roomoccupancy/ratio orfee inferred.',
 'bede-eastbourne':'Current2027Little6weeks/1775board1125day/17.5ENhours/class14/dayhours/snacklunch/1:3typical/excursions. Age5dayvs6board groundednewPDFfootnote, notgeneral5headline.',
 'bede-windlesham':'Old2026Future8–13/18.5h/1595/roomsratio nottransferred to2027Burgess. New2027programme groundedsummaryp2.',
 'bede-fees-retry':'SameURLsecondretrievalHTTP200/current2027feesinclusions andownlinks to2027summary/terms; initialDNSfailure resolved withoutinventingbody.',
 'bede-summary-2027':'Actual2page2027PDFbothvisual:footnote5–11day/6–11board,Little2–5rooms/Future1–4,1775/1125,class14,A0,weekgrid/academyfees/Burgessnewprogramme. Futureweek6PDFvswebdiscrepancy excludesuncertainlastweek.',
 'bede-terms-2027':'Actual4page2027PDFselectedp2visual,relevantp1deposit/textclausesread:800board400day,balance56days,cancel29–55deposit/8–28oneweek/0–7full,extra23516095295100/insurance/nightcare. Notfulllegalrevieworconsent.'}
r=[q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(r)==34 and {q['key'] for q in r}==set(scopes)
for q in r:
    q.update(retrieval_method='direct_http',content_scope=scopes[q['key']])
    if q.get('status')==200:
        ext='.pdf' if (PRIMARY/(q['key']+'.pdf')).exists() else '.html';f=PRIMARY/(q['key']+ext)
        assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
        q.update(body_snapshot_retained=True,raw_filename=f.name,content_status='actual_pdf_selected_pages' if ext=='.pdf' else 'html_selected_programme_clauses')
    else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body')
assert sum(q.get('status')==200 for q in r)==33
visual=json.loads((PRIMARY/'visual-source-notes.json').read_text());assert len(visual)==6 and sum(q['pages_visual_checked'] for q in visual)==8
urls={s['url'] for p in b['camp_programmes']['profiles'] for s in p['sources']}
added=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-urls);assert len(added)==24
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
cc={iso:sum(p['iso']==iso for p in c['profiles']) for iso in ['CHE','FRA','ESP','ITA','GBR','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','BRA','CHL','PHL']}
calendar=dict(events=len(d['events']),learning_records=sum(e['block']=='Лагеря' for e in d['events']),family_ics=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text().count('BEGIN:VEVENT'),exhibition_ics=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_text().count('BEGIN:VEVENT'),managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows'])
assert calendar==dict(events=3255,learning_records=1924,family_ics=2514,exhibition_ics=104,managed_dated_rows=1461,reused_legacy_events=69,season_windows=42)
checks=[
 '9newprogramme dossiers/6operatorgroups:5Italy,3UK,1France. Prior698profiles/3230events retained unchanged;707dossiers/37countries/1111dossierURLs/24newURLs. Counts areprogrammes, notindependentworldranking.',
 '25newexactdate windows:2Cavalese,2Oclini,5XUK,6BedeLittle,4BedeFuture,6Canopée.23newfamilyplanningICS:2Oclini12+excludedforbothcurrentages. NoSocksregistrationdateasdeadline/cohort; noSancelsoorAOSRarchived2026futurecohort.',
 'Bedeactual2027PDF5day6board/1775board1125day/Little2–5rooms/FuturenewBurgess1–4rooms/class14.800/400depositinprice,balance56days,cancel29–55vsFAQ29–41. FutureAug8–14PDFvswebendingAug7 excluded; oldWindlesham1595/ratio/roomsnotpromised.',
 'Sancelso6–17ENcamplife withItalianexternalinstructors/ENtranslation,1:10plusyoungintern,4beds/sleepingbag/healthdocuments.2026mandatorysportbase855/1670;withsiblings1670/3280familybeforetravel/pocketmoney. New2027invoice/contractunknown.',
 'Socks7–10/10–14/musiccreativeENresidential,Jan15registration2027butnosessions/fees. AOSR3–15ENday/openvisitingforeignfamilies/codingrocketsmaker/250450650+175busarchive2026;2027Marchdetailsandclosedintake notsoldout.',
 'Cavalese10–14/680board340day/2exact2027dates;first27–02luglioambiguousstartmonthexcluded. Oclini12–16/780/2exactdates/fullENtypicalPDF. EnglandScotlandtimetablecolumnsnotcountries;typicalPDFyearunknownnotexact2027syllabus.',
 'XUK8–17five2027dates/ENstaffcampLife;2026price1160andtermscalendarretainedasarchive. Insuranceextra/laundry6/bag/transfer99way/options separate. Activity/Excel/English andyoungerLondonDay differentprogrammes.',
 'Canopéesix2026–27daywindows09–17/Englishownteachers/openexternal/lunch5155days2062days;1030or412two. Overview6–11vsthemes6–10 remainsupperagegap. Noinventedrobotics/boarding.',
 '34directattempts/33HTTP200/oneDNSfailurelaterresolved,6actualPDFs/8selectedvisualpages. Lacunza2027feeplaceholders/Chester8–17vs8–18+2026feePDF unchanged; VillageFranceonlyarchive notnewcamp.',
 'Independentold-recordpreservation/JSONSQLiteCSVMDICS/bridgeidempotence/interactivefilters/staticfilelimit/JSsyntax checks. RawHTML/PDF/rendersprivate; selectedclauseparaphrases/hashreceipts public. Fullworldscope/prioritycountries active,0fullyaudited; noapplication/consent/booking/payment/message/account.'
]
next_priority='Continue fullworld2026–27 general/thematic/STEM camps and boarding/day/family EN/ES/RU. Prioritize CHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatinAmerica with foreignindividualintake/DOB-grade/languageofactualteaching/fullinvoice/contract/gear/ratio/places. NewItalianseasons, Burgess2027lastweek/XUK2027contracts remainunresolved. All leagues/competitions/exhibitions/familyadmission/schools/results5–10years/familyroutes stay fullscope; no countryfullyaudited.'
audit=dict(asof=CHECKED,version=101,status='progress',scope='Selected international family boarding/general English camps Italy/UK and French all-English holiday weeks; repeated Spain annualfee/date gaps. NotwholeEurope/world.',new_dossiers=9,new_operator_groups=6,deepened_dossiers=0,updated_dossiers=[],programme_slugs=NEW,new_calendar_rows=25,new_family_session_ics=23,new_family_ics=23,new_registration_deadline_ics=0,new_season_windows=0,corrected_existing_event_ids=[],programme_dossiers=707,countries_with_dossiers=37,official_dossier_urls=1111,country_dossier_counts=cc,findings=c['gaps'][-5:],calendar=calendar,primary_retrievals=dict(direct_attempts=34,http200=33,retrieval_errors=1,javascript_shells_without_programme_body=0,unique_actual_pdfs=6,selected_visual_page_checks=8),fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,next_priority=next_priority)
def write(stem,value):
    txt=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(txt);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(txt)
write('europe-camp-audit-v101',audit)
write('europe-camp-source-receipts-v101',dict(asof=CHECKED,version=101,scope='34directselectedretrievals/6PDF/8selectedvisualpages; notwholewebsites/countries. RawHTML/PDF/rendersprivate.',sources=r,visual_pdf_checks=visual,dossier_source_urls_added=added,external_actions=external,notes=['OnefailedDNSbodyretrieval resolvedonsameURLlater;failedresponse notsourceproof. No forms/signup/consent/message/payment/account.', 'Programme/age/formatgroups notuniquebrands. ENcamplife/lesson/supportdifferent;current2027terms notinheritedfrom2026. Editorialfamilyfit notindependentworldranking.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=101:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Research/nativepublication100 succeeded; commit'+BASE+'; deploymentappgdep_6ac4606756188191b060f15f64a7e56f. Fullworldobjective unchanged.')
plan['latest_validation']=dict(version=101,asof=CHECKED,status='Independentselectedsource/preservation/calendarverification; nativepublicationreceiptseparate',events=3255,camp_learning_records=1924,programme_dossiers=707,countries_with_dossiers=37,official_dossier_urls=1111,family_ical=2514,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=cc)
plan['europe_camp_programme_audit_v101']=audit
plan['camp_catalog_integration'].update(asof=CHECKED,dossiers=707,countries=37,swiss=99,generated_calendar_entries=1461,reused_legacy_events=69)
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        q['evidence']='v101:707programme dossiers/37countries/1111URLs.9new across6operatorsItalyUKFrance;25exactdatewindows/23familyICS.34directattempts6PDF8selectedvisualpages; Bedeactual2027prices/contracts, youngerboarding andlanguageboundaries, winter/summerFrenchdates, Spainfees/agegaps preserved. Notcompleteworldwide.'
entry=dict(version=101,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=9,deepened_dossiers=0,new_calendar_rows=25,new_family_ics=23,corrected_existing_calendar_rows=0,official_primary_retrieval_attempts=34,unique_actual_pdfs=6,selected_visual_page_checks=8,not_complete_worldwide=True)
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=101]+[entry]
plan['next_research']=[next_priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED
write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=100','?v=101').replace('data-ui-version="100"','data-ui-version="101"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text();anchor='<a href="downloads/STEM_europe_camp_audit_v100.json"'
link='<a href="downloads/STEM_europe_camp_audit_v101.json" download>Европа: пансионы, английские каникулы и цены 2027 ↓</a> · <a href="downloads/STEM_europe_camp_source_receipts_v101.json" download>Источники нового европейского прохода ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=707,new_dossiers=9,new_calendar_rows=25,new_family_ics=23,source_urls=1111,goal='active')))
