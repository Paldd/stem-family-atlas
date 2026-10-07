"""Scoped, reproducible source receipts and the preserved worldwide work plan."""
import collections,hashlib,json,subprocess
from pathlib import Path
from camp_asia_v98 import NEW,CHECKED
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v98'
BASE='c4a58064e7408f84e367bc4e427b77f653f2d024'
before=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in before['events']};new=[e for e in d['events'] if e['id'] not in old]
assert len(new)==21 and all(e==old[e['id']] for e in d['events'] if e['id'] in old)
assert c['counts']['dossiers']==680 and c['counts']['source_urls']==1066
receipts=[q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(receipts)==27 and sum(q.get('status')==200 for q in receipts)==24
scopes={
 'laurus-index':'Own2026 three age formats/dates/nonLaurus weeklyfees/6000siblingsrules/externalforeignintake/basicEN/insurance; Primary syllabus/address/fullpackage unresolved. Secondary upperage11–16 vs11–15 conflict. No forms entered.',
 'laurus-prek':'Japanese ownWinter2026 page/seven activecampus addresses/MusashiShinjo unavailable; programme/fee/terms sections only, not wholecampusschool audit.',
 'laurus-prek-en':'SpecificEnglish2026 PreK/daywindows/Englishinstruction/scientistthemes/13000or17000from/6000entry/5000internationaltransfer/lunchmaterialsinsurance/740buslimits/Dec14deadline/Dec15nonrefund/1000admin. Oldsummer sentence conflict retained.',
 'bc-taiwan-zh':'Directtimeout; no ownbody retained/read through this attempt, no newcurrentfee/date claim. Existing dossier unchanged.',
 'bc-taiwan-en':'Directtimeout; no ownbody retained/read through this attempt, no newcurrentfee/date claim. Existing dossier unchanged.',
 'branksome-gamejam':'Currentown junior-school enrichment GameJam, not externalholidaycamp/date/price/admissionproof. Existing school/camps not replaced.',
 'branksome-robotics':'Currentown juniorcurriculum BeeBot/Dash/VEXGO/Arduino, not openexternalholidaycamp proof. No newcampcohort.',
 'tenten':'Currentown2027 specific4 programmes/gradegates/5datedvariants/regularvsconditionalearlyfees; ClarkEnglish1:1 andcampLifeclaimvsKoreanstylegrammarmaths, domesticENlessons. SSP/insurance/extras excluded, grade/foreignintake/contracts unresolved.',
 'ltl-japan':'Own2027 TokyoOsakaJapaneselanguage/kidsday7–11/residence11–17/20hJapanese/456USDfrom without chosenformat. No exactcohort/teacherEN/fullinvoice; not newconfirmedENcamp.',
 'taas-summer-home':'Owncompleted2026 programmes; currentopening/waitlist UI not2027intake guarantee. Dailylanguage/class curriculum separatelyread.',
 'taas-lv1':'Own2026 Grade1–2 Augustgate/July6–31/NT41500/Englishclasses/art/scoutthemes; no2027coursefee or inferredfamilygrade.',
 'taas-lv2':'Own2026 Grade3–4/41500/language/buildfly/technology/rocket andwater activities; nextyearcourse not announced.',
 'taas-lv3':'Own2026 Grade5–6/41500/modelrockets/bridges/photography/art; notRoboticsintensive or2027fee.',
 'taas-schedule':'Own09–1530/chapel/PE/music/swim/Fridaytrips timetable; not allsubjectsEnglishguarantee.',
 'taas-faq':'Wholemonthonly, textbooks/lunchandbusseparate, packedlunch/typhoonnoMakeup/absence. Not current2027contract or foreignpassportcampintake.',
 'taas-policy':'Refund90/70/0 footer explicitlyMarch1–July31 2020; stale not2027contract. Behaviourdismissal/noRefund separate. No consent entered.',
 'taas-calendar':'Actualonepage school2026–27PDF, selectedfooterreadvisually:2027SummerSchoolJuly5–30 only seasonwindow, not threeconfirmedgradedcohorts.',
 'smis-jeju':'Directown2027 currentwinter20days19nights/2intervals/Grade3–Middle2/3900000KRW completebasepackage/100000pocketmoney/rooms2–4/EnglishESL/AI-STEAMday/humanities; technicalteaching/campLifeEN/foreignintake/refund unresolved.',
 'kidscamp-home':'Owncurrent2027 fourTaiwanvenues andManila PDFlinks/tuition9800+meal500/Oct20early8折for1–2. Discountiscalculated80percent tuition only, finalinvoice/intakeunconfirmed.',
 'alv-taipei':'Own2027image-only5pagebrochure all5pagesviewed;Jan25–29/Grade1–3and4–6/NT9800+500/feecomponents/EnglishOnly/timetable/address. Generaltheatre/science, notroboticsintensive.',
 'alv-shilin':'FirstattemptIncompleteRead/noPDFsaved; retryHTTP200 image-only5pagebrochure p1/2/4/5viewed: exactvenue/date/grade/fee/English/timetable, p3notviewed.',
 'alv-banqiao':'Own2027image-only5pagebrochure p1/2/4/5viewed: exactvenue/date/grade/fee/English/timetable, p3notviewed.',
 'alv-kaohsiung':'Own2027image-only5pagebrochure p1/2/4/5viewed: exactvenue/date/grade/fee/English/timetable, p3notviewed.',
 'alv-manila':'Own2027image-only6pagebrochure all6viewed:Jan23–Feb1/10days7nights conflict/58800yuancurrencyunexplicit/ENcampandbuddy NOTteacher1:1. Age/foreignintakeunknown, fullincluded/extras paraphrased.',
 'alv-policy':'OwnTaiwanandabroad refundclauses includingoverlapping7dayboundary/500fee/mealonlyabsence/typhoonSaturdaymakeup andphoto-rightclause. No contractual acceptance or legalvalidation.',
 'alv-english':'OwnEnglishsite/generalimmersiondescription; newprogrammeEN proof taken from each2027PDF, not siteinterface.'}
assert {q['key'] for q in receipts}==set(scopes)
for i,q in enumerate(receipts):
    q.update(retrieval_method='direct_http',content_scope=scopes[q['key']],body_snapshot_retained=q.get('status')==200)
    if q.get('status')==200:
        ext='.pdf' if (PRIMARY/(q['key']+'.pdf')).exists() else '.html'
        f=PRIMARY/(q['key']+ext);assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
        q['raw_filename']=f.name;q['content_status']='actual_pdf' if ext=='.pdf' else 'html_selected_programme_clauses'
    else:q['content_status']='retrieval_error_no_complete_body'
visual=json.loads((PRIMARY/'visual-source-notes.json').read_text())
assert len(visual)==6 and sum(q['pages_visual_checked'] for q in visual)==24
oldurls={s['url'] for p in before['camp_programmes']['profiles'] for s in p['sources']}
added=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls);assert len(added)==20
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
countrycounts={s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','BRA','CHL','PHL']}
calendar=dict(events=len(d['events']),learning_records=sum(e['block']=='Лагеря' for e in d['events']),
              family_ics=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text().count('BEGIN:VEVENT'),
              exhibition_ics=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_text().count('BEGIN:VEVENT'),
              managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows'])
assert calendar==dict(events=3205,learning_records=1874,family_ics=2466,exhibition_ics=104,managed_dated_rows=1411,reused_legacy_events=69,season_windows=42)
checks=[
 '16newprogramme/venue/formatdossiers across5operators;all664priorIDs/order/content and3184priorrecords unchanged.680dossiers/37countries/1066dossierURLs;20newURLs.',
 '21newcalendarrecords:9Laurusvenue/formats,4ALVTaiwan,1ALVManila,2SMIS,5Tenten. FamilyICS gains20sessions and1deduplicatedLaurusdeadline; Secondaryfutureage excluded.3TAASseasonwindows not cohortICS.',
 'Laurus7activePreKcampuses/notMusashiShinjo;nonLaurus13/17kfrom vsweeklyPrimary85/100k andSecondary104k,6000entryrules. PreKDec14deadline/5000transfer/1000canceladmin/740busrestrictions. Weeklyspecificsyllabus/inclusions unresolved; older summer copy not programme proof.',
 'ALV four2027imagebrochures: exactJan25–29/Grade1–6/ENclasses/timetable/address/9800+500. Registration500alreadyincluded,2Minsurancecoverage notfee.80%tuition early1–2tillOct20 gives8340/16680 conditional; promo deadline not registrationdeadline.',
 'TAAS2027schoolwindowJul5–30 not weeklycohort or tuition2027. Three gradecourses/41500/currentUI are2026archive; refunddated2020 notcurrentcontract. Chapel and ENlanguage-lessonsrole visible; foreigngrade/intake not inferred.',
 'SMIS current2027winter againststalecachedsummer:390만원=3900000KRW/Grade3+/19nights/2cohorts/completebasepackage;technicalEN/intake/refund unknown. TentenGrade4+/29calendardatesClark/secondspeech20days, Koreanstylemath unknownlanguage/foreignfit; earlyfeeconditions unresolved.',
 'ALVManilaall6PDFpages: Jan23–Feb1,10days7nights conflict;currency/gradeunpublished. FullENandpeerbuddy notteacher1:1; flights/visasexcluded/internalcertificate notinternationalmedal.',
 '27directattempts24HTTP200/3errors;6actualPDFs and24selectedvisualpagechecks, notfullsites/countryaudit. LTL Japanese/Englishunconfirmed andBranksomeschoolGameJam notnewENcamp. BCtimeoutsdidnotreplaceexistingdossiers.',
 'IndependentJSONSQLiteCSVMDJSICS checks, stableoldUID/dates/deadlines, bridgeidempotence andfamily/language/phasefilters. Fullworldobjective/requirements preserved,0countriesfullyaudited/nativegoalactive.'
]
checks.append('SQLite storage layout compacted after native per-file size rejection; complete logical SQL dump equals originally pushed v98 export, schema/alltables/allrows retained. Every static file checked against26214400byte limit; new native publication receipt separate.')
audit=dict(asof=CHECKED,version=98,status='progress',scope='Japan/Taiwan/Korea programme, price, school-category and language evidence; Philippines linked winter boarding. Bounded additions, not complete Asia/world.',
           new_dossiers=16,new_operator_groups=5,deepened_dossiers=0,updated_dossiers=[],programme_slugs=NEW,new_calendar_rows=21,new_family_session_ics=20,new_family_ics=21,new_registration_deadline_ics=1,new_season_windows=3,
           corrected_existing_event_ids=[],programme_dossiers=680,countries_with_dossiers=37,official_dossier_urls=1066,country_dossier_counts=countrycounts,
           findings=c['gaps'][-4:],calendar=calendar,primary_retrievals=dict(direct_attempts=27,http200=24,retrieval_errors=3,unique_actual_pdfs=6,selected_visual_page_checks=24),
           fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
           next_priority='Continue deepCHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatinAmerica within fullworld2026–27 general/thematic/robotics/coding/AI/day/residential/family inventory. VerifycurrentseasonteachingEN/ES/RU/campLife/supportroles, individualforeignintake/places/actualDOB-grade, syllabus/hours/levels/kit, fullinvoice/contract/transport, exactcampusmap andfamilycomparisons. Leagues/competitions/exhibitions/childadmission/schools/results5–10years/familyroutes remainactive; no countryfullyaudited.')
def write(stem,value):
    txt=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(txt)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(txt)
write('asia-camp-audit-v98',audit)
write('asia-camp-source-receipts-v98',dict(asof=CHECKED,version=98,scope='27directretrievalattempts only;6uniquePDFs/24selectedvisualpages. Notfullsite/countryaudit. RawHTML/PDF/renders/privateparaphrase-notes stayoutsidecheckout.',
      sources=receipts,visual_pdf_checks=visual,dossier_source_urls_added=added,external_actions=external,
      notes=['ShilinfirstIncompleteRead andretrysuccesskeptseparate;BCEN/ZHtimeouts notbodyproof.',
             'Image-onlyALVPDFtext extraction empty;selectedprogramme/fee/language/timetable pages readvisually, notallpagesofeachPDF.',
             'EN rolecampLife/language_lessons/primary separated; schoolgrade notinferredfrombirthyear. TAAS2020refund/2026fees not2027contracts.',
             'Programme/venue/formatdossiercount not uniquebrands or independentworldranking; foreignacceptance/places not guaranteed.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=98:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='v97nativepublication succeeded; commit'+BASE+'; deploymentappgdep_6ac453fc91008191ab66dbab81d7348b. Fullworldwideobjectivepreserved.')
plan['latest_validation']=dict(version=98,asof=CHECKED,status='Independentprimary/preservation/calendarverification; nativepublicationreceiptseparate',events=3205,camp_learning_records=1874,programme_dossiers=680,countries_with_dossiers=37,official_dossier_urls=1066,family_ical=2466,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=countrycounts)
plan['asia_camp_programme_audit_v98']=audit
plan['camp_catalog_integration'].update(asof=CHECKED,dossiers=680,countries=37,swiss=86,generated_calendar_entries=1411,reused_legacy_events=69)
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        q['evidence']='v98:680programme/venue/formatdossiers in37countries/1066dossierURLs;16new across5operators/21newcalendarrecords,20familyshiftICS+1deadline/3seasonwindows. CurrentJapan/Taiwan/Koreawinter andlinkedPhilippinesboarding,24selectedPDFvisualpages/27directattempts. Grade/language/invoice/foreignintake unknowns andstaleTAAS2020refund/2026prices explicit. Allpriorcontent/fullworldscopepreserved.'
entry=dict(version=98,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=16,deepened_dossiers=0,new_calendar_rows=21,new_family_ics=21,corrected_existing_calendar_rows=0,official_primary_retrieval_attempts=27,unique_actual_pdfs=6,selected_visual_page_checks=24,not_complete_worldwide=True)
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=98]+[entry]
plan['next_research']=[audit['next_priority']];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED
write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=97','?v=98').replace('data-ui-version="97"','data-ui-version="98"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_asia_camp_audit_v98.json" download>Азия: зимние программы, классы, языки и полная смета ↓</a> · <a href="downloads/STEM_asia_camp_source_receipts_v98.json" download>Проверенные страницы и брошюры ↓</a> · '
anchor='<a href="downloads/STEM_americas_camp_audit_v97.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=680,new_dossiers=16,new_calendar_rows=21,new_family_ics=21,source_urls=1066,goal='active')))
