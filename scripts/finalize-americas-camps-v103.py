"""Selected-source receipts and native-goal continuity, publication is a separate receipt."""
import hashlib,json,subprocess
from pathlib import Path
from camp_americas_v103 import CHECKED,NEW
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v103'
BASE='2ea55367db46f906261caeba97825a2a13d2b93d'
old=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
before={e['id']:e for e in old['events']};fresh=[e for e in d['events'] if e['id'] not in before]
assert len(fresh)==13 and all(e==before[e['id']] for e in d['events'] if e['id'] in before)
assert c['counts']['dossiers']==745 and c['counts']['source_urls']==1158
scopes={
 'kupugani':'Actual operator permanently-closed banner; old fees not available camp. Referenced Swift links checked separately.',
 'bc-mexico':'Actual 2026 Young Innovators6–11/100percentEnglish/STEM/general/Jul20–Aug21/09:15–13:30/5096–20384MXN and archival discounts. No2027 dates.',
 'science-world-winter':'Actual returning Fall2026 notice without dated session, ages or new price; historical themes not current curriculum.',
 'science-world-camps':'Actual operator programme index and source links; Summer2026 and future winter/spring notice not2027 sessions.',
 'techknow-home':'Old .com body December2025/Summer2026, not actual2026 winter authority. Its linked kids-domain programme checked separately.',
 'holland-winter':'Actual Winter2027 body behind old2026 slug: ScienceClub6–14/Junior6–10/Scratch9–14/Intermediate10–14 weekly evenings, conditional snowmakeup and erroneous2026 snowmakeup. Not six-week full-day camp.',
 'holland-march':'Actual Mar15–19 2027/475+HST9–14 headline versus8–14 eligibility; safe structured group,20minute sitting/3step instructions, intake and45min meet, confirmationDec18. Formaldiagnosis condition checked in general description. Not generic familycamp.',
 'rooted-cr':'Actual2027 girl-only14–18/June28–Aug1/15000USD/5week therapeutic route, internationalflights+insurance excluded,3stafffor10 ownclaim. Both children ineligible.',
 'swift-home':'Own current homepage6–15/generalnature/science/boarding, contradictory referencedKupugani6–17; own rates/firsttimercamp/internationalFAQ URLs404. No2027 new dossier.',
 'science-world-knowledge':'Actual admission by birthyear, not inferred familygrades;2026 2020Little/2016–17Curious; English basic mandatory; samecamp repeat prohibited; >14/>7/within7days refund and adminfees; meal own; two-part registration not submitted.',
 'science-world-summer':'Actual archive2026 AmazingHumans/agegroups/inventions/body/STEMtools, 549.95/474.95five and439.95/384.95four, aftercare25/20,oneweek pertheme. Grade and birthyear conditions; no2027 guarantee.',
 'science-world-field':'Actual archiveJul6–Aug28 2026/field2–3and4–5/halfdayoutdoor/8:30–15/range369.95–524.95; weatherbackup/noearlypickupguarantee/oneweek, not roboticsintensive or new2027 date.',
 'holland-description':'Actual formaldiagnosis required; appropriateageasDec31/6–14/possibly family1:1 support and assistivecommunicationdevice. Conflicts softer March page. Not assumption of family medicalneeds.',
 'pipiol-one':'Actual 2027 Jul4–17/6–16/MXN84000/three venues/owninternalMundialito; concretecourseminimum differs homepage.',
 'pipiol-two':'Actual 2027 Jul19–31/6–16/MXN78400/calls2weeks but13calendardays; exactarrival/nightcount unresolved.',
 'pipiol-home':'Actual Hacienda/Guerrilleros/Kanoas/nature/noelectronics/roomsbyage/ownmedicalstaffclaims; conflicting4–17 and7–15; MiniKids mention not dated2027 cohort; Spanishsite not confirmed teachinglanguage.',
 'pipiol-contract':'Actual linked PDF selected clauses: three meals/lodging/transportonlyifstipulated/accidentpolicylimits; cancellation>=30daysnocharge,20days30percent,<20daysnone;21–29unresolved;20businessdaysrefund; publicityphoto/video clause not accepted; yearunmarked. Visualpages4/5.',
 'techknow-winter':'Actual Winter2026 heading; Pokémon5–8motorizedLEGOCodeyRocky/Minecraft6–9; two campuses3vs4days. .com old2025 not used.',
 'techknow-faq':'Old .com FAQ includes2020online assumptions/10:1; not used as newwintercontract, current kids-domain9:1 checked separately.',
 'techknow-modern-faq':'Actual max20/2–3teachers/max9:1 ownclaim, computerkit suppliednotgift, ownmeals, standardextendedcare; Englishteacher not explicit.',
 'techknow-pokemon':'Actual5–8motor/gears/battery/CodeyRocky/digitalmazes/Pokemon, weekDec21Glen465andDec28Sunset355. NotMinecraftgamecourse.',
 'techknow-minecraft':'Actual6–9motorizedLEGOandMinecraftprojects/noexperienceneeded, Dec21Sunset355andDec28Glen465, 3vs4days.',
 'techknow-glen':'Actual395AddisonStreet/Dec21–24Pokemon/Dec28–31Minecraft/09–15:30/465/ext105.',
 'techknow-sunset':'Actual999BrotherhoodWay/Dec21–23Minecraft/Dec28–30Pokemon/355/ext80; mistakenGlenParkheadline kept explicit, address not conflated.',
 'techknow-pricing':'Actual Winter2026 25percentdeposit/autobalanceDec4; cancellationbeforeDec1refundminus25,afterDec1>=1weekcreditthroughSep2027minus25,within1weeknone; healthordermandate90refund10credit,otheroperatorcancel100choice;10sibling/secondweek not guaranteedstack.',
 'roboiq':'Actual general4–14/VEXpathway/oldplannedRichmondHill; not specificcampageorEnglishroboticsteacher.',
 'roboiq-camp':'Actualcamps SummerWinterMarchPDWeekend withEnglishlessons/MathRobotics/art; actualMarkham/RichmondHilladdresses,NewMarketOpeningInProgress; exactdatedfee absent.',
 'laurus':'Actual2027planning/bilingualENFR/FrenchImmersion/ownparentpollclaims/7STAheading; no fullprice or actual datedcohorts. Ownranking not independentworldrank.',
 'laurus-faq':'Actual FAQ headings, answerbody not available in selected directtext; no invented answers/fees.',
 'laurus-summer':'ActualYouth5–11/75minuteSTAs/11categories vs7home/TorontoRosedale131Bloorvenueconfirmed2027,othercitiesplanned/schedulespricingcomingsoon/earlycareinc,extendedoptional.',
 'eli-montreal':'Actual Junior12–13/Senior14–17/ENorFR/15vs20lessons/Jul4–Aug1/1–4weeks/dayboard/McGill; genericinclusion20lessons correctedbyown2027brochure15Junior.',
 'eli-brochure':'Actual two-page Montreal2027 brochure confirms Junior15/Senior20/ENFR/Jul4–Aug1/daylunch/insurance/boardairport/onewashdry/meals/24:7; not Toronto7+rules. Visualpage2.',
 'eli-handbook':'Actual Toronto2027 handbook7–17/Primary7–11/Jun27–Aug15/1–7weeks/45min15lessons/firstdayorientation/July1Aug2activities/rooms/nightcare/laundryextra/250depositinprice/balance21days/flight14days. DespitelinkedfromMontreal appliesToronto, homestay14–17 conflictsweb15+. Visualpage1.',
 'eli-programs':'Actual operator programme index linksToronto/Montreal/family; universitycampus not universityacademiccourse.',
 'eli-toronto':'Actual Primary7–11/EN15lessons/dayboardallages7+/June27–Aug15 2027/1–7weeks/home15+senior only; actuallinkedhandbookmorecurrentdetails,homestaycontradictionretained.',
 'eli-family':'Actual familyprogramme7+same2027season/parentsoptionalEN/childlunch/optionalhousing/Niagara and parent3hpackage contradiction; under7customdiscussionnotacceptedregistration.',
}
r=[q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(r)==44
for q in r:
    q.update(retrieval_method='direct_http',content_scope=scopes.get(q['key'],'Public linked URL retrieval failed; no programme body or 2027 fee inferred.'))
    if q.get('status')==200:
        f=PRIMARY/(q['key']+('.pdf' if (PRIMARY/(q['key']+'.pdf')).exists() else '.html'))
        assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
        q.update(body_snapshot_retained=True,raw_filename=f.name,content_status='selected_pdf_clauses' if f.suffix=='.pdf' else 'selected_html_programme_clauses')
    else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body')
assert sum(q.get('status')==200 for q in r)==36
web=PRIMARY/'langmobile-web-fresh.json'
web_receipt=dict(url='https://langmobile.com/en/summer-camps/plateau/#faq',retrieval_method='web_reader_open_primary',checked=CHECKED,body_snapshot_retained=True,raw_filename=web.name,bytes=web.stat().st_size,sha256=hashlib.sha256(web.read_bytes()).hexdigest(),content_scope='Fresh actual EN page2027/5–6sevenweeks/7–12specialtyTBA/100percentEnglish/from305currencyunmarked/Janregistration/mealcareextra/headerendAug14vsweeklyendAug13. EarliercachedEN/FRreturned2026specialties and FR subsequenttimeout, not current2027specialtyproof. DirectHTTP403 recordedseparately.')
before_urls={s['url'] for p in old['camp_programmes']['profiles'] for s in p['sources']}
added=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-before_urls);assert len(added)==26
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
cc={iso:sum(p['iso']==iso for p in c['profiles']) for iso in ['CHE','FRA','ESP','ITA','GBR','CHN','HKG','FIN','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','BRA','CHL','PHL']}
cal=dict(events=len(d['events']),learning_records=sum(e['block']=='Лагеря' for e in d['events']),family_ics=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text().count('BEGIN:VEVENT'),exhibition_ics=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_text().count('BEGIN:VEVENT'),managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows'])
assert cal==dict(events=3287,learning_records=1956,family_ics=2543,exhibition_ics=104,managed_dated_rows=1493,reused_legacy_events=69,season_windows=46)
checks=[
 '15 new programme dossiers across 8 operator groups; old730dossiers/3274events unchanged. 745total/39countries/1158dossierURLs/26newURLs. Not a global ranking or fully audited country.',
 '13exactnewdates:2PipiolJuly2027/4TechKnowDecember2026/7Langmobile5–6weeks2027.13familyplanningICS,4newflexibleseasonwindowsnotmadeintoevents. Archive2026ScienceWorld/BCMexico not rolledinto2027.',
 'Pipiol actual84000/78400MXN,6–16coursebuthomepage7–15and4–17; Spanishsite not explicitteacherlanguage. Meals/accommodation/accidentpolicy included,transportconditional; cancellation21–29daygap retained. MiniKids mentionnotnew2027cohort.',
 'TechKnowHow newWinter2026currentcampus/pricing overold.com2025and2020FAQ;CodeyRocky5–8/Minecraft6–9,separateaddresses/3vs4days/355or465,aftercare80or105/ownmeals/kitsnotgift;teacherENstillunconfirmed. 25percentdepositinprice/Dec4balance,Dec1refundcreditchange not registrationdeadline.',
 'ScienceWorld actualbirthyearadmission2026:Oscar2020Little/Mat2017Curious; schoolgradeguideline not inferredfamilygrade. Englishmandatory; oneweekeachtype,Fielddifferentcurriculum. 2027dates/groupsunknown/WinterreturningFallheadline not datedcamp.',
 'Eli Toronto7+and Montreal12+ separated; TorontoPrimary15lessons45min,firstdayorientation/holidayactivities,250depositinprice/21daybalance; handbooklinkedfromMontrealactuallyToronto. Montrealownbrochure15Juniorcorrects20genericwebinclusions,onewashdryincvsTorontolaundryextra. Familyunder7discussionnotacceptance.',
 'Langmobile direct403, primarywebreaderfreshbody2027actualweeks;earliercachedbody2026notfuturecurriculum. HeaderAug14versuslastweekAug13;7–12specialtyTBAandJanuaryregistration;from305currencyunmarked. Laurus5–11bilingual75minSTAs butnewpricingdatesunannounced;ROBOIQEnglishlessonnotEnglishrobotics.',
 'Kupuganiownpermanentlyclosed,Swiftownlinks404; noavailabilityfromoldsearch. HollandBloorviewformaldiagnosis/1:1/intakeconditionsandcourseageconflicts;weeklyeveningsnotholidaycamp, no genericfamily recommendation. Rootedgirls14–18notourboys.',
 '44directattempts36actualbodies(33HTML/3PDF)8failures;1freshprimarywebreaderfallbackafter403;4selectedvisualPDFpages. Selectedclausesnotwholewebsiteaudit. Preservation/SQLschema/SQLrecords/CSV/ICS/filter/JS/maxfileindependentverification. Goal active0fullyaudited.'
]
next_priority='Continue all worldwide 2026–27 general/thematic/STEM camps, day/boarding/family EN/ES/RU; deepen CHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatAm and all remaining countries. Real programme dates/fullinvoices/age-currentgrade/foreignindividualadmission/teaching-vs-language-lessons-support/gear/nightcare/refunds/availability. All schools/results5–10years/leagues/competitions/exhibitions/familyroutes retained. No country fully audited.'
audit=dict(asof=CHECKED,version=103,status='progress',scope='SelectedUSA/Canada/Mexico2026winterand2027general/thematic/STEM programmes;CostaRicaandclosed/specialintakegaps. NotcompleteAmericas/world.',new_dossiers=15,new_operator_groups=8,deepened_dossiers=0,updated_dossiers=[],programme_slugs=NEW,new_calendar_rows=13,new_family_session_ics=13,new_family_ics=13,new_registration_deadline_ics=0,new_season_windows=4,corrected_existing_event_ids=[],programme_dossiers=745,countries_with_dossiers=39,official_dossier_urls=1158,country_dossier_counts=cc,findings=c['gaps'][-4:],calendar=cal,primary_retrievals=dict(direct_attempts=44,http200=36,retrieval_errors=8,unique_actual_pdfs=3,selected_visual_page_checks=4,primary_web_reader_fallbacks=1),fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,next_priority=next_priority)
def write(stem,value):
    txt=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(txt);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(txt)
write('americas-camp-audit-v103',audit)
write('americas-camp-source-receipts-v103',dict(asof=CHECKED,version=103,scope='44selecteddirectattempts/33HTML/3PDF/8errors,primarywebreaderLangmobilefallbackand4visualpages. Rawsourcebodiesprivate;notwholewebsites/countries.',sources=r,web_reader_fallbacks=[web_receipt],dossier_source_urls_added=added,external_actions=external))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=103:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Research/nativepublication102 succeeded;commit '+BASE+';deployment appgdep_6ac46bd14a0c8191a1ec70211d81b051. Fullworldobjective unchanged.')
plan['latest_validation']=dict(version=103,asof=CHECKED,status='Independent selected-source/preservation/calendar verification; nativepublication receipt separate',events=3287,camp_learning_records=1956,programme_dossiers=745,countries_with_dossiers=39,official_dossier_urls=1158,family_ical=2543,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=cc)
plan['americas_camp_programme_audit_v103']=audit
plan['camp_catalog_integration'].update(asof=CHECKED,dossiers=745,countries=39,swiss=99,generated_calendar_entries=1493,reused_legacy_events=69)
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:q['evidence']='v103:745dossiers/39countries/1158URLs.15newAmericanprogrammecards/13exactdates/13familyICS/4seasonwindows; USAactualWinter2026/Mexico2027/Pipiolcontract/CanadianbirthyearandEnglish2027routes.44direct36bodies3PDF8errors/1webreaderfallback/4visualpages. Notcompleteworldwide.'
entry=dict(version=103,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=15,deepened_dossiers=0,new_calendar_rows=13,new_family_ics=13,corrected_existing_calendar_rows=0,official_primary_retrieval_attempts=44,unique_actual_pdfs=3,selected_visual_page_checks=4,not_complete_worldwide=True)
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=103]+[entry]
plan['next_research']=[next_priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED
write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=102','?v=103').replace('data-ui-version="102"','data-ui-version="103"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text();anchor='<a href="downloads/STEM_asia_camp_audit_v102.json"'
link='<a href="downloads/STEM_americas_camp_audit_v103.json" download>Америка: зима2026 и лето2027 ↓</a> · <a href="downloads/STEM_americas_camp_source_receipts_v103.json" download>Проверенные источники Америки ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=745,new_dossiers=15,new_calendar_rows=13,new_family_ics=13,source_urls=1158,goal='active')))
