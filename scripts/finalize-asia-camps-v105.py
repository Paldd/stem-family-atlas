"""Record selected primary evidence and continuity; publication receipt stays private."""
import hashlib,json,subprocess
from pathlib import Path
from camp_asia_v105 import CHECKED,NEW
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v105'
BASE='17bed4437b7ae7b932ee0f1f67245116c80d960e'
old=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
before={e['id']:e for e in old['events']};fresh=[e for e in d['events'] if e['id'] not in before]
assert len(fresh)==14 and all(e==before[e['id']] for e in d['events'] if e['id'] in before)
assert c['counts']['dossiers']==769 and c['counts']['source_urls']==1203
scopes={
 'hcc-winter':'Actual Korean local winterDec21 2026–Jan2 2027/grade4–9/KRW3000000/twoweeks/editormentors1:1/Englishwritingdiscussion;dailyhoursandnumericrefundnotpublic. Localgradecontradictsprimarypublisher9–12. No form or optional essay sent.',
 'ulearn-korea':'Actual university deliveredKoreanlanguage/culture/AIrobotmuseumvisit/JuniorParentandteen/halls/supervisionclaim1:10;actualdynamicdatesandfullfeesnotretainedasprogrammebody. EnglishsiteandcontactnotEnglishteacherproof;publicGoogleDriveviewlinksnotopened/submitted.',
 'bc-sg-holiday':'Readtimeout35s;no body. DoesnotinvalidatepriorpublishedBritishCouncilSingapore2026winterPDF evidence. No duplicatecamp created.',
 'steam-squad':'Actualown2027tenweekdaymissions/Jan21–Feb3/27000standard24000paidbyDec5 2026/materialsentriesmealinsurance/ownEasyCard/refund/min8Jan5;previousdossieralreadycontainsfactsandunchanged.',
 'edventure-winter':'ActualtwooperatingwindowsDec12 2026–Jan9 2027/Feb1–17 2027/day3–12/fullday5–12/multiday3consecutive/rentliftincludedonlymultiday. Pricebanddatesstill2025–26/duplicatefrompricesnotcurrent2027invoice.',
 'edventure-summer':'ActualthankyouSummer2026/Summer2027notopen/Familyparent/Moiwaovernight/Yotei9plus/Rishiri13plus;contradictorylegacyprices/agesandweekcalendars. No2027datedsummercohort inferred.',
 'nbs-price':'Actualown16page26/27PDF/creationJune2026. Selectedpage7visuallyread:5–7ski24000/8–14skiandsnowboard23000/EN/Dec14–Feb28/min5peak/7rentalpackagefees. GeneralAprilendnotKidsClubdate;notwhole16pageaudit.',
 'kidsstop-holiday':'HTTP200actualgenericScienceCentre/KidsStopnavigation;no usablecurrentNov2026specificprogrammeclauses. Cached/secondarydatesnotnewconfirmedcamp.',
 'nac-day':'Actualown2026day6–12/min4/5day75000/3day40000/taxaccidentinsurancegear/lunch/exampleactivities;lastweekwebAug17–19contradictsPDF17–21. Englishteacherunestablished/2027notannounced.',
 'imagine-hokkaido':'ActualSummer2026/6.5–13/intermediateENorJP/primaryEnglishadaptedbilingual/oneovernightThursFri/150000/ownlunchdays1–4/specificdinnerbreakfastlunch/discountrequiresconditionsnotautomaticsiblings. No2027dates.',
 'edventure-winter-faq':'ActualEnglishinstructionanswer/allguestservicesEnglish/bilingualhelp/max5/3–4onlyhalfday/localNisekoUnitedpickup/lunch/allgearonly3day/noovernight.',
 'edventure-winter-packing':'Actualwinterownclothingpackinglist;notcampgearownershiportakehomeincluded.',
 'edventure-terms':'Actualseason-specificcancellationWinter>15full/14–7minus20/≤7none;Summer≥15minus10000/14–7half/≤7none. Exact7overlap/winterexact15gap;amend5000/14days/fullpay7daysor24h/fees/medicaldiscretion. No consent.',
 'edventure-summer-faq':'ActualEnglishfamily/Moiwa/child/meal/oneovernight/selftransport/tent/bagmat4900/newweeksrotated;not2027datesorfullinvoice.',
 'edventure-residential':'ActualYotei9plusvslegacy10–12/6nights7days/allmeals/lodge4children/staffonsite/devicefreeactivities/arrivalSun≤13departSatdomestic≥12intl≥14;19900/11–15comparisoncontradictsFAQ;pricesandlegacycalendarconflictsvisible.',
 'nac-programme':'Actualbilingual2026PDFselecteddatesage6–12school/75000/40000/programme09–16/raftingraftbuildtest/navigation/skate/guideplansmin4max20. Internal7000supplierlessonnotextrafamilyfee/overnightstaffnotboardingoffer. Selectedpage1visuallychecked.',
 'imagine-terms':'Actuallinked2023PDFselectedcancellation≥48hcredit/12–48halfcredit/<12none/cashonlyoperatorcancels/liability/photosoptout;selectedpage1visuallychecked. Notnew2027contract;no consent.',
 'traidhos-winter':'Actualfive2027weekly7dayresidential9–14/33000THB/ESLandoutdoor/mealsaccommodationaccidentinsurance/nosiblingdiscount/medicalonlyrefund;copydaycampfeecontradictionnotdayformat.',
 'traidhos-faq':'ActualcampussharedPrem/ESLteachersEnglish/rooms/nightcounsellors/nurse24claim1:10/accidentnotillness/parentstayseparate/generalforceMajeurevsordinarycancel. EnglishCampstaffnotJuniorNatureEnglishproof.',
 'fcis-winter':'Actualschoolown2027campJan9–Feb4/two2wkboarding/daydatesJan10/22vsboardJan9/23;day7–15birth2020board10–15birth2017ageconflicts. FourRMpackageprices/Dec12earlyfeeconditionnotregistrationdeadline/EnglishdailycurriculumSTEMPBL/3levels/native/admissions/PrimeCampoperator;refund/minimumunknown/selfranknotindependentworldtop.',
 'campasia-book':'ActualOct19–23Robotics6–8/725SGD;noactualChristmas2026offeredtechnicalcohort/unchangedpublisheddossiers. Availabilitysnapshotnotapprovedbooking.',
 'campasia-robotics':'Actualgeneralrobotprogramme/725five-day/menu/samplecurriculum;notnewdatedwinter2026offerorENteacherproof.',
 'campasia-coding':'Actualgeneralcodingprogramme/725five-day/campdevice;noactualdatednewwinter2026offer.',
 'campasia-electronics':'Actualgeneralhardwareprogramme/samplecurriculum;noactualdatednewwinter2026offer.',
 'campasia-dec3':'Actual13pagePDFfilenameDec26-3/TitleDec26-2/creationDec26 2018,notDecember2026camp. Selectedpage2WeDoWedThuFrithree-daycurriculumvisuallyread;archiveexampleonly.',
 'nbs-kids':'ActualEnglishinstructors/5–7ski/8–14skiorsnowboard/day0930–1530/soft4soft6/dateDec14–Feb28/basicvsrentalpackage/noforcedyearwindowMarchApril.',
 'nbs-terms':'Actualtoilettrained/age5skigroup8snowboard/liftseparate/softgroupsnotguaranteed/printwebdiscrepancywebwins/cancel0till15/14–7half/≤7all/medicalonlyinjuredperson/weather/photoprioroptout;not accepted.',
 'edventure-family':'ActualFamilyparentperchild/selftransport/MoiwachildMonWedparentovernightmandatoryvsoptionalcopy/onecampingnight/EN/mealexceptions/bagmat4900;multiplepriceandageblockswithout2027fullinvoice.',
 'traidhos-nature-wonder':'ActualownFeb15–19 2027titlevsold2026bodycopy/4–8/12000THB/day/2snackslunchmaterialsinsurance/ordinarymedicalrefundonly. Englishinstructionnotexplicit.',
 'traidhos-nature-everywhere':'ActualownFeb22–26 2027titlevsold2026copy/4–8/12000THB/day;samematerialsinsurancepolicynotsecondduplicateprovider.',
 'crimson-partners':'ActualpublisherprimarylistconfirmsKoreaco-hostPrincetonReviewWritingLeadershipCamp/DecandSummer2026/Seoul9–12gradescontradictlocal4–9. StudentnewspaperpartnershipnotHarvardUniversitycredit.',
 'crimson-local-partner':'ActuallocalPrincetonReviewKoreacampindex;partneridentitynotresolutionofgradeconflict/foreignadmission.'
}
r=[q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(r)==32 and sum(q.get('status')==200 for q in r)==31 and set(scopes)=={q['key'] for q in r}
for q in r:
    q.update(retrieval_method='direct_http',content_scope=scopes[q['key']],checked=CHECKED)
    if q.get('status')==200:
        pdf=q['key'] in ['nbs-price','nac-programme','imagine-terms','campasia-dec3'];f=PRIMARY/(q['key']+('.pdf' if pdf else '.html'))
        assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
        q.update(body_snapshot_retained=True,raw_filename=f.name,content_status='selected_pdf_clauses' if pdf else 'no_usable_specific_programme_body' if q['key']=='kidsstop-holiday' else 'selected_html_clauses')
    else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body')
urls={s['url'] for p in old['camp_programmes']['profiles'] for s in p['sources']}
added=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-urls);assert len(added)==23
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
cc={iso:sum(p['iso']==iso for p in c['profiles']) for iso in ['CHE','FRA','ESP','ITA','GBR','CHN','HKG','FIN','TWN','SGP','JPN','KOR','THA','MYS','USA','CAN','CRI','MEX','BRA','CHL','PHL']}
cal=dict(events=len(d['events']),learning_records=sum(e['block']=='Лагеря' for e in d['events']),family_ics=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text().count('BEGIN:VEVENT'),exhibition_ics=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_text().count('BEGIN:VEVENT'),managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows'])
assert cal==dict(events=3323,learning_records=1992,family_ics=2577,exhibition_ics=104,managed_dated_rows=1529,reused_legacy_events=69,season_windows=49)
checks=[
 '11newdossiers/7operatorgroups/14exactcalendarrows/13familyplanningICS/3seasonwindows/0newdeadlines;old758dossiers/3309eventsunchanged.769total/39countries/1203URLs/23newURLs;notworldrankingorwholecountryaudit.',
 'HCCactualDec21–Jan2/3000000KRW/localgrade4–9vspublisher9–12/noapprovedcurrentfamilyintake;futureP4/excludedfamilyICS. OwnnewspaperpartnershipnotHarvardUniversitycredit.',
 'EdVenturewinteractualtwooperatingwindows/EN/day3–12fullday5–12/gearandliftonly3consecutive;prices2025–26conflicts. Summer2027notopen/familyparentperchild/oneovernight/Yotei9vs10–12/sixnights/wholepriceandmeal/flightconflictsvisible. Noinventedfutureweeks.',
 'NBSown26/27PDFpage7/EN5–7ski/8–14skiandsnowboard/Dec14–Feb28only/softgroupnotguaranteed/liftextra/basicvsrentalpackage. Operatingwindownotseason-longsession;nosportsrecordlabelledroboticsleague.',
 'NACday2026/6–12andschool/75000or40000/gearmealinsurance/rafttestactualcurriculum/lastweek3vs5days/overnightstaffnotenotboardingoffer;noENteacherproof. Imagine6.5–13/ENJPpartialbilingual/1500002026/oneovernight/ownlunch/discountnotautomatic/creditnotcashrefund;no2027dates.',
 'TraidhosEnglish9–14/5weekly2027residential33000THB;JuniorNature4–8/2dateddayweeks12000/ENunconfirmed/MatnoteligibleOscarconditional. Accidentnotillness;ordinarynomedicalcancelnonevsFAQforceMajeureseparate.',
 'FCISreal2027separateboardandday/age10–15birth2017vsday7–15birth2020DOBconflicts/2or4weekfee/Dec12earlypricingnotregistrationdeadline/ELAdebateSTEMPBL/hostschoolvsPrimeCamp. DayJan22vsboardJan23/weekendextras/Singaporeborder/refundminimumunknown;selfranknotworldbest.',
 '32directattempts/31HTTP200/26selectedHTMLclausebodies1genericnavigation/4actualPDFs/1timeout/4selectedvisualpages. CampAsiaDec26-3PDFcreatedDec2018notDec2026booking;KidsStopnavigationnotnewprogram. SteamSquadunchangedexistingTWNfactsnotduplicate.'
]
next_priority='Continue worldwide2026–27 general/thematic/STEM camps/day/boarding/family EN/ES/RU, especially CHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatAm. Officialfullinvoices/ageDOBgrades/foreignindividualintake/teacherlanguagevslessons/life/support/gear/nightcare/refunds/currentplaces. Schools/results5–10years/leagues/competitions/exhibitions/familyroutes remain active;0fullyauditedcountries. Researchscope mustnot be reduced by staticdownloadlimits;preservecompleteDBwithverifiedportablepackagingwhenneeded.'
audit=dict(asof=CHECKED,version=105,status='progress',scope='SelectedJapan/Korea/Thailand/Malaysia2026–27winter/summer/day/boardingprogrammeandcontractclauses;Singapore/Taiwanduplicateandarchivechecks. NotcompleteAsia/world.',new_dossiers=11,new_operator_groups=7,deepened_dossiers=0,updated_dossiers=[],programme_slugs=NEW,new_calendar_rows=14,new_family_session_ics=13,new_family_ics=13,new_registration_deadline_ics=0,new_season_windows=3,corrected_existing_event_ids=[],programme_dossiers=769,countries_with_dossiers=39,official_dossier_urls=1203,country_dossier_counts=cc,findings=c['gaps'][-6:],calendar=cal,primary_retrievals=dict(direct_attempts=32,http200=31,selected_html_bodies=26,unusable_specific_programme_bodies=1,retrieval_errors=1,unique_actual_pdfs=4,selected_visual_page_checks=4,primary_web_reader_fallbacks=0),fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,next_priority=next_priority)
def write(stem,value):
    txt=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(txt);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(txt)
write('asia-camp-audit-v105',audit)
write('asia-camp-source-receipts-v105',dict(asof=CHECKED,version=105,scope='Selected32directattempts/26HTMLclausebodies1genericnavigation/4PDFselectedclauses1error. Rawbodyprivate;notwholewebsites/countries.',sources=r,dossier_source_urls_added=added,external_actions=external))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=105:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Research/nativepublication104 succeeded;commit '+BASE+';deployment appgdep_6ac47462f73081919bd1d3d6e3fcd092. Fullworldobjective unchanged.')
plan['latest_validation']=dict(version=105,asof=CHECKED,status='Independent selected-source/preservation/calendar verification; nativepublication receipt separate',events=3323,camp_learning_records=1992,programme_dossiers=769,countries_with_dossiers=39,official_dossier_urls=1203,family_ical=2577,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=cc)
plan['asia_camp_programme_audit_v105']=audit
plan['camp_catalog_integration'].update(asof=CHECKED,dossiers=769,countries=39,swiss=106,generated_calendar_entries=1529,reused_legacy_events=69)
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:q['evidence']='v105:769dossiers/39countries/1203URLs.11newAsianprogrammecards/14calendarrows/13familyICS/3seasonwindows.32directattempts26selectedHTMLclauses1genericnavigation4PDFs1timeout/4selectedvisualpages. Source/pricing/age/language/contractconflictsvisible;notcompleteworldwide.'
entry=dict(version=105,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=11,deepened_dossiers=0,new_calendar_rows=14,new_family_ics=13,new_season_windows=3,corrected_existing_calendar_rows=0,official_primary_retrieval_attempts=32,unique_actual_pdfs=4,selected_visual_page_checks=4,not_complete_worldwide=True)
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=105]+[entry]
plan['next_research']=[next_priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED
write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=104','?v=105').replace('data-ui-version="104"','data-ui-version="105"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text();anchor='<a href="downloads/STEM_europe_camp_audit_v104.json"'
link='<a href="downloads/STEM_asia_camp_audit_v105.json" download>Азия: новые подробные программы и условия ↓</a> · <a href="downloads/STEM_asia_camp_source_receipts_v105.json" download>Проверенные источники Азии ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=769,new_dossiers=11,new_calendar_rows=14,new_family_ics=13,source_urls=1203,goal='active')))
