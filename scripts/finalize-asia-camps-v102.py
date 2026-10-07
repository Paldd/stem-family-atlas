"""Publish selected-source receipts and preserve the expanded worldwide goal."""
import hashlib,json,subprocess
from pathlib import Path
from camp_asia_v102 import CHECKED,NEW
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v102'
BASE='54610f96af67effeba81351194db4aaa61d08fdf'
old=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old_ev={e['id']:e for e in old['events']};fresh=[e for e in d['events'] if e['id'] not in old_ev]
assert len(fresh)==19 and all(e==old_ev[e['id']] for e in d['events'] if e['id'] in old_ev)
assert c['counts']['dossiers']==730 and c['counts']['source_urls']==1132
scopes={
 'dulwich-camps':'Selected current winter LITA11–17/English/14800/12850/two6daydates, Finlandfamily6–17/3dates/40800indicativeunitunknown/flightsexcluded and ongoingOctAIfilmG4–6/EN/650010800/max30. NotwholeEIMxpartners/worldcampaudit.',
 'ycyw-primary':'Selected own2026ShanghaiEN/PBL6–14Y1–8and8–10Y4–6/10800;BeijingVEX8–13Y4–9/9500,VEXIQG4–9/13800,TongxiangG4–12/dayboardfees/externalssameprice. No2027datesorEnglishVEXteacherstatementfound.',
 'ctd-shanghai':'DirectEnglishURL404/noactualbody. Searchprimarycachedsnippetnotfullsource/current2027programmeproof; noCTDdossierinvented.',
 'korea-ltl':'Own2027headline7–17,Koreanclasses20h/KidsDay7–11/Residence11–17/Homestay12–17/HalfDay7–17,USD377fromunitpackageunknown. Englishsite/EnglishdoctorsnotEnglishinstruction/support; copiedHalfDayinclusioncontradictionretained.',
 'mandarin-inn':'Own2026bilingualENMandarin8–12/culture9–16/fees380072201026012920/noincludedlunch/ownparentdropoff/12class/outings1:6. Fourweekdescriptionvseightformweeksnotresolved; no2027copy.',
 'ltl-taiwan':'Own2027headline/Mandarintraditional20h/7–11dayparents/11–17residence/12–17homestay/class5–8max12. Noactualexact2027cohort/fullfee/Englishstaffsupportfound inselectedbody; halfdaylistcontradictsprose.',
 'ltl-japan':'OwnTokyo/OsakaJapanese20h/2027headline/day7–11/board11or12plus/max12/parentsallowed. Noexact2027dates/fullprice/ENstaffsupportfromselectedbody. TeamLabtournottechnicalteachingcamp.',
 'ltl-generic':'Ownfamilyaccompaniment/5percentsibling/classmax12/doctorEnglish/preloadedtransitlimitedfirsttrips. EnglishdoctornotENcamplife; popupprice/startbuttonsnotreadactualdatedfees.',
 'tinycode-home':'Ownarchive2026inhomeEN10h/courseagegates6–8,7–11,body8–12vsFAQ8–10,10plus;5280single3432EACHgroup2–3/laptop/software/hardwareonlyrobotlab/projectreportcertificate16classroadmapnot16paidclasses.',
 'harrow-hk-circuit':'Ownarchive2026English9–11/JuneJulydates/8980smartcar/laptopnoiPad. Notnew2027capacity/date/fee; priorwintercoursefactsfromnewactualcards.',
 'ycyw-index':'Ownnetworkopenall2–18/bilingualmarketingdoesnotoverridecoursegrade/ageorproveENVEX. Noformsubmission orpassporteligibilityapproval.',
 'ycyw-early':'SelectedownarchiveECE2–5English/880015800 andKLT4–6STEAM2400. Notnew2027agegate; notextraEOscar6–7dossierfrom2–5archive.',
 'harrow-winter':'OwnwinterSTEMcollectionwiththreeactualproductlinks,Englishmarketing. GuangzhouproductlocatedMainlandChina despiteHKcollection; geographyreadactualproductvenue.',
 'harrow-winter-japan':'OwnwinterMyokocollection/productlink; exactage10–16/fee/gearfromactualproductnotcollectionheading.',
 'tinycode-terms':'ActualApril2026selectedfullpayment/nonrefund/nofeeorstudenttransfer/7daysreschedmax1monthly/weatherT8BlackRainresched. Notlegalreview/new2027contract.',
 'tc-home':'OwnEN9–15/5days4nights/bilingual/2027prebookinglink. Coretour4languagesnot4languagecampinstruction.',
 'tc-camp':'Ownarchive2026Aug22–26/grades9–15incoming3to10/20900early18999two17500each/inclusionhostelmealsinsurance/publictransport. Own1:7guideactivityvs1:1tasknotoverallratio; no2027pricefromarchive.',
 'tc-2027':'OwnSep2026blog2027prebooking1000deposit,priceunannounced,7dayspostpricefullrefundifreject. Noactual2027dates/fullfee/fullrefundafterthatwindowinferred.',
 'jasmine':'Ownactual2027nine-sessiontable/fees13800–19800/currentgradeatregistration/optionalnightcosts/noduplicatewaterboarding/rail3nights4500;AXCENledwithChinesepeers,NOLAMandarinprimary+ENcriticalcontact/parentENsupport.',
 'kdw-home':'OwnBishanoperator/curriculaSpikePrimeScratch/BattlebotsRescueRovers/kindergartenprimarycourseheadings. Languageofactualinstruction andfulldatedpricetableunconfirmed.',
 'ctd-cn':'DirectChineseURL404/noactualbody; cachedsearchnotusedasfullcurrentprogrammeaudit.',
 'harrow-ecobot':'ActualEnglish6–8/Dec21–24/09–16/8980/materialslunchsnacks/robotmotorssensorstablet/safety/sustainability;publicproductofferInStock/variantavailabletrue ratherthanhiddengenericSoldoutlabel. Noacceptedregistrationproof.',
 'harrow-auto':'ActualGuangzhouMainlandvenue8–13/Dec21–26/12500HKDtaxinc/English/residential/kartengineeringbrandingbusiness/fullmeals/PLI. F1-inspirednotofficialF1licence/worldroboticscompetition. Rooms/ratio/foreignintakeunknown.',
 'harrow-sleigh':'ActualEnglish9–12/Dec21–24/8980/lunchsnacks/materials/basicEN/engineeringphysicsprototype/ownfinalchallenge,notguaranteedroboticssoftwareplatform.',
 'harrow-ski':'ActualMyokoJapan10–16/Dec21–26/23800English/5nights/4lessons/lift/rentalhelmetboots/airportescorts included;winterclothes/medicalwinterinsurance/flights/evacuationexcluded.1:5ownclaim/WMAassessmentcertificateconditionnotinternationalaward.',
 'jasmine-calendar':'ActualChinese2027ninecourses/currentgradeNOTrisinggrade/13800–19800/hostelbreakfastnotdinner/waterlunchdinnertransitextra/railnightnotdoublecounted,30AXC/24formingNOLA1:6–8claimed;coursecurriculumtypedseparatelynotallcoding.',
 'kdw-program':'OwnSepOct2026headline/fullhalfday/lunchsnacksfull/Bishan/20percentdeadlineAug31archive; actualparsedbodylacksdatedsessionfee/explicitENinstruction. Noportalaccount/cart/form opened.',
 'harrow-policies':'Actual2026winterpolicyselectedpayment/7daycoolingoffonlyuntilSep30/HKMainlandOct40percentminus4fee,Novnonrefundable;overseasOct1nonrefundable/nochanges;operatorgroupcancelrefund/emergencylocalphone/weatherrefundlimits. Noagreementaccepted/legaladvice.',
 'jasmine-block':'ActualJan21–22/Grade1–5/currentgrade/physicalpaperwoodworkshopNOTMinecraftcoding/EN-ledChineseTA/max30/6800early6300untilOct16/lunchinsurance/shirt300/late400firstfree,no2daywholelateplan. Discountendnotregistrationdeadline.',
 'jasmine-build':'Own2027Jul5–9Grade2–4/currentgrade/physicalpaperwoodrecycledbuildNOTcomputerMinecraftcoding/noexperience/ENledtaskswithChineseTA/30/13800/full-daystructure/gearextras.',
 'jasmine-shop':'Own2027Jul12–16Grade4–7/pricinginventorycashier/pupilcustomersNOTpublicparentcustomers;ENcounterphrasesbutChinesebusinessreasoning. Lunchmaterialsinsurance/shirt300/late1000;legacypriceOctoberwaitlisttextnotdeclaredresolved.',
 'jasmine-discovery':'Own2027Jul19–23Grade4–7/designobserveprototypeusertest/reiterate/NTUEstudioNTUfield/13800/ENtaskquestionsChinesecomplexreflection/3foreignteachersclassnotboardingratio/gear.',
 'jasmine-micro':'Own2027Aug2–6Grade2–4/oneweekonewaterresearchquestion/individualmicroscope/faircounts/testing/5perworktable/notstaffratio/13800/lunchmaterialsinsurance. ENresearchinstructionsChinesefairmethodrules;notwaterpotabilitytest.'}
r=[q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(r)==33 and {q['key'] for q in r}==set(scopes)
for q in r:
    q.update(retrieval_method='direct_http',content_scope=scopes[q['key']])
    if q.get('status')==200:
        f=PRIMARY/(q['key']+'.html');assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
        q.update(body_snapshot_retained=True,raw_filename=f.name,content_status='html_selected_programme_clauses')
    else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body')
assert sum(q.get('status')==200 for q in r)==31
offers=json.loads((PRIMARY/'public-offer-notes.json').read_text());assert len(offers)==4
before={s['url'] for p in old['camp_programmes']['profiles'] for s in p['sources']}
added=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-before);assert len(added)==21
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
cc={iso:sum(p['iso']==iso for p in c['profiles']) for iso in ['CHE','FRA','ESP','ITA','GBR','CHN','HKG','FIN','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','BRA','CHL','PHL']}
calendar=dict(events=len(d['events']),learning_records=sum(e['block']=='Лагеря' for e in d['events']),family_ics=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text().count('BEGIN:VEVENT'),exhibition_ics=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_text().count('BEGIN:VEVENT'),managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows'])
assert calendar==dict(events=3274,learning_records=1943,family_ics=2530,exhibition_ics=104,managed_dated_rows=1480,reused_legacy_events=69,season_windows=42)
checks=[
 '23newprogramme dossiers across7operatorgroups,730total/39countries/1132dossierURLs/21newURLs. NewMainlandChina8/HongKong6/Taiwan7/Japan1/Finland1;old707dossiers/3255events preserved. Countsdistinguishprogrammesfrombrandsandnotglobalranking.',
 '19newexactwindows/16familyplanningICS:2LITA11+and1Myoko10+excludedforcurrentages.5AXC/5NOLA2027dates;Englishpartial/coreChineseandcurrentgradesexplicit. Noarchival2026summer/LTLheadline/depositdateasfuturecohort.',
 'Harrowwinter21–24HK6–8EcoBot/9–12Sleigh8980each,lunchsnacks;Guangzhou21–26/8–13/kartengineering+business12500HKDfullboard. Actualownpublicvariantsavailabletrue andInStock;hiddenSoldouttemplateisnotconfirmedclosed. Fullpayment/refundpolicycriticaldatedclauses retained.',
 'Myoko10–16/23800/5nights4ski-lessonsrentalhelmetbootstransfers included,wintergear/insuranceflightsmedicalevacuationexcluded. Current2026Matveymaximum9,Oscarmaximum6,excludedfamilyICS. Own1:5notindependentinspection/certsubjectassessment.',
 'Jasmine2027AXC13800day+6000hostel=19800,breakfastnotdinner. Shirt300/late1000explicit. CoretasksENbutpricing/design/scientificfairrulesChinese,notfullEnglish. G2–4/G4–7CURRENTatregistration,notbirthyear/risinggrade. NOLAonlyENsupportfilter,Mandarincomprehensionunknown.',
 'NOLA2027Water19800already4nights,not+6000;childlunchdinnerEasyCardextra. Rail16800includes1night+3optional4500=21300.5curriculumpathsunderoneoperatortrack,noduplicated9same-weekdates. Exactdayversusovernightvariesbysession.',
 'TCcity2027onlyrefundable1000holddeposit/datespriceunknown;archive20900/17500eachandAug2026 notpromised2027. EnglishMandarinbilingual9–15/currentgradeequivalence. Finland3exactfamilydates6–17/ENmain/40800indicativeunitunknown,domesticFinlandflightsnotincluded.',
 'TinyCodearchive2026EN10h/privatehome:notfull-daycamp.Scratch6–8/robot7–11/gamesbody8–12FAQ8–10/PythonAI10+.5280single3432EACHgroup;robotkitsprovidednotgift/laptopsown/roadmapnot16classes. TermsApril2026noautomaticrefund/transfer,new2027unknown.',
 'YCYWVEXarchivalgrades4+/specificEnglishrobotteacherunknown. Ownopen-to-allnetworkdoesnotprovepassportapproval/courseeligibility. LTLthreecountry2027headlinesnotEnglishprogramme/weeklydates/fullfee;KidsDay7–11withparents,boarding11or12plus. CTDdirecttwo404,cachedsearchnotcompleteaudit.KDWBishanactualdatedfees/Englishunconfirmed.',
 '33directretrievalattempts/31actualHTML/2CTD404/0PDF/4publicofferJSONclauses;selectedprogrammeclausesnotwholewebsiteaudit. Independentoldrecords/schema/SQLforeignkeys/CSV/ICSUIDdates/idempotence/interactivefamilylanguagephasefilters/JS/staticlimit verification. Worldscopeactive,0fullyaudited;noapplications/payments/messages/accounts/consent.'
]
next_priority='Continue fullworld2026–27 general/thematic/STEM camps, day/boarding/family EN/ES/RU. Preserve CHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatAm priorities. Check eachactualcourse/foreignindividualintake/DOB-currentgrade/teaching-vs-essential-support/rooms/nightcare/fullinvoice/gear/refund/places. China/HKnowpartialcoverage;JasminecomplexChinese/legacywaitlisttext/gradeandNOLAlanguagecritical;LTLexactdates/ENsupportandCTDcurrentcanonicalmissing. All leagues/competitions/exhibitions/schools/results5–10years/familyroutes stay fullscope. No countryfullyaudited.'
audit=dict(asof=CHECKED,version=102,status='progress',scope='SelectedAsianrobotics/general/thematicEnglishprogrammes:China/HongKongwinter,Taiwan2027,JapanskiandFinlandfamilyroutewithEIMx. Country-specificLTL/KDWevidencegaps. NotcompleteAsia/world.',new_dossiers=23,new_operator_groups=7,deepened_dossiers=0,updated_dossiers=[],programme_slugs=NEW,new_calendar_rows=19,new_family_session_ics=16,new_family_ics=16,new_registration_deadline_ics=0,new_season_windows=0,corrected_existing_event_ids=[],programme_dossiers=730,countries_with_dossiers=39,official_dossier_urls=1132,country_dossier_counts=cc,findings=c['gaps'][-5:],calendar=calendar,primary_retrievals=dict(direct_attempts=33,http200=31,retrieval_errors=2,javascript_shells_without_programme_body=0,unique_actual_pdfs=0,selected_visual_page_checks=0,public_product_offer_checks=4),fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,next_priority=next_priority)
def write(stem,value):
    txt=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(txt);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(txt)
write('asia-camp-audit-v102',audit)
write('asia-camp-source-receipts-v102',dict(asof=CHECKED,version=102,scope='33selecteddirectattempts/31HTML/2CTD404/0PDF/4publicproductofferchecks,notwholewebsites/countries. RawHTMLprivate.',sources=r,public_product_offer_checks=offers,dossier_source_urls_added=added,external_actions=external,notes=['PublicofferInStocknotacceptedregistration;hiddenSoldouttemplateisnotclosedproof. ActualcourseChinese/Englishsupportseparated. CTDcachedsnippetnotdirectsourcebody.', 'Familiesbirthyearsnotgrades/DOB. Programmegroupsnotbrands/ranking;archivalfeesnot2027invoice. Noforms/accounts/messages/payments/consent.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=102:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Research/nativepublication101 succeeded;commit'+BASE+';deploymentappgdep_6ac46561fd348191bb1f47964c2c971f. Fullworldobjective unchanged.')
plan['latest_validation']=dict(version=102,asof=CHECKED,status='Independentselectedsource/preservation/calendarverification;nativepublicationreceiptseparate',events=3274,camp_learning_records=1943,programme_dossiers=730,countries_with_dossiers=39,official_dossier_urls=1132,family_ical=2530,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=cc)
plan['asia_camp_programme_audit_v102']=audit
plan['camp_catalog_integration'].update(asof=CHECKED,dossiers=730,countries=39,swiss=99,generated_calendar_entries=1480,reused_legacy_events=69)
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        q['evidence']='v102:730dossiers/39countries/1132URLs.23newAsianprogramme dossiers/19exactwindows/16familyICS,includingfirstChina/HKcoverage.Taiwanactual2027dates/currentgrade/partialENandMandarin/supportboundaries. Harrowwinter2026package/refund/gear.33directattempts31HTML2CTD404/0PDF/4publicofferchecks.Notcompleteworldwide.'
entry=dict(version=102,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=23,deepened_dossiers=0,new_calendar_rows=19,new_family_ics=16,corrected_existing_calendar_rows=0,official_primary_retrieval_attempts=33,unique_actual_pdfs=0,selected_visual_page_checks=0,not_complete_worldwide=True)
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=102]+[entry]
plan['next_research']=[next_priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED
write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=101','?v=102').replace('data-ui-version="101"','data-ui-version="102"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text();anchor='<a href="downloads/STEM_europe_camp_audit_v101.json"'
link='<a href="downloads/STEM_asia_camp_audit_v102.json" download>Азия: зимняя техника и Тайвань2027 ↓</a> · <a href="downloads/STEM_asia_camp_source_receipts_v102.json" download>Источники нового азиатского прохода ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=730,new_dossiers=23,new_calendar_rows=19,new_family_ics=16,source_urls=1132,goal='active')))
