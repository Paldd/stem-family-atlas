"""Scoped retrieval receipts and an active, unchanged worldwide objective."""
import collections, hashlib, json, subprocess
from pathlib import Path
from camp_europe_v100 import NEW, CHECKED
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v100'
BASE='337d9550f7626b7eba3eb5251abcf7714aa78d43'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text()); c=d['camp_programmes']
old={e['id']:e for e in b['events']}; new=[e for e in d['events'] if e['id'] not in old]
assert len(new)==25 and all(e==old[e['id']] for e in d['events'] if e['id'] in old)
assert c['counts']['dossiers']==698 and c['counts']['source_urls']==1087
scopes={
 'cosmo':'Own classes8+ separate from camp age unknown; microbit/Maqueen/camp dates and format. EN website not ENteacher evidence; giftboard for yearclass not automatically camp.',
 'cosmo-camp-form':'Actual3page2027PDF: p1/3 selected visually, other text read; six morning intervals/three summer fulldays/Easter280 vs webTBC/Academy-only10percent/insurance/nonrefund/paymentfirstday/operatorcancel5days. Blankform not filled; banking data omitted from paraphrases.',
 'code-home':'Own current course-menu/season-opening notices. Winter starts Dec2026, not invented Dec2027. Voucher range not programme fee; sponsors not independent ranking.',
 'code-camps':'Own9 programme levels and agegates; Masters8–13 menu conflicts with7–12 owncourse. Spring/Summer2027registration opening notice not exactcohorts.',
 'code-faq':'Selected own language-by-cohort/dayformat/priceapprox120CHF/siblingunknown/foodBYO/device/license/rental50late/partialrefund clauses. AI9–13 programme vs demanded13+account conflict, no account created; no change of age or providerpolicy verification.',
 'code-winter':'Own exactstarts/durations/venues winter2026–27; programme/language/price bycohort not readable here. No campus-week multiplied into9 course calendars.',
 'code-spark':'Own7–12/blockgame/basiclogic/3dayexample/projectcontinuation. Genericdailyexample not confirmed2027cohort. Internalmedal not internationalaward.',
 'code-ai':'Own9–13/twodaygenerativeAI/computervision/comic; six actual intervals in sixmunicipalities2026–27 admitted with keyedvenues; teachinglanguage/price/minoraccount unresolved.',
 'code-roadmap':'Own learning progression, not internationalqualification. No rigid age-inferred mastery or guarantee of teacherEnglish.',
 'code-byod':'Own pointer to per-course device requirements; FAQ contains concrete restrictions. No external app installation/account/signup.',
 'code-terms':'Selected publicly displayed terms show Australianlaw/AUD/footer2018 vs Swissaddress; current Swisscontract applicability unknown, not legalvalidation.',
 'code-list':'Direct public listing returned JS shell, not programme/language/price body. Embedded client identifiers/keys not used or copied to public receipt. No signup opened/entered.',
 'code-ignite':'Own7–12/priorSparkorequivalent/twodgame/blocktofirstJavaScript, usually3days. Game via commonCodeCamp app not guaranteed independentstore app.',
 'code-blast-3d':'Own8–13/pureJavaScript3D/priorlearning/keyboardcomfort, variable3dayexample. Operatorfirstworldwide claim not independently verified.',
 'code-web-builders':'Own8–13/HTMLCSSJavaScript/multipageproject/layout/navigation, keyboard requirement andtypical3days. EN teaching not confirmed.',
 'code-minecraft-engineers':'Own7–12/three-dayrollercoaster/Redstone/commandblocks/MinecraftEducation license forcourse only. Exactnewcohort not proven.',
 'code-minecraft-masters':'Own7–12 conflictsmenu8–13; requiresEngineers, spyHQ/Redstone/parkour/NPC/escaperoom. GenericBlast3D/GameOver lower template not selectedMinecraftsyllabus.',
 'code-minecraft-experts':'Own8–13/atleastoneMinecraftcamp/commandblocks/MakeCode/adventuremap/Elytra/arena. Generic3D lower template not actualMinecraftdailyproof.',
 'code-animation':'Own7–10/two-daystopmotion/storyboard/pairedshooting/editing, ownclassprose used. Genericthree-day3D template not course duration.',
 'issh-techlabs':'Own archivedJul13–17 2026/9–16/CHF650 each7–10robotics and11+drones; specific robot/sensor and simulator-toautonomous missions. DE/ENenvironment only7–10; no2027cohort or schoolboarding transfer.',
 'issh-stem':'Own schoolSTEMcamp background not newdated2027camp. No form entered, schooladmission not inferred.',
 'florimont':'Own2026 four types: Albert15–18EN/Futurekids5–14halfday/TechSpark9–16; Englishinterface not allcampteacher language. ExistingTechSpark preserved, no duplicatebrandcamp.',
 'florimont-autumn':'OwnOct19–23 2026/4–9/day8–17/CHF810/multiactivity; ENteacher not established. No newconfirmedENdossier.',
 'futurekids':'Directreturned JS shell withtitle, no owncurriculum/date/fee/languagebody. Florimontclaim not provider-fullsiteaudit.',
 'techspark-zurich':'Currentown full citydate/course menu/ENinstruction/gear/fees; allalreadycovered25games+Python andLEGO unknowncohort. No duplicate datedrows or fakeLEGO availability.',
 'lacunza':'Ownseason2027Jun20–Aug8/6–13/threeformats; still no new full2027invoice/individualweeks. Existingdossier unchanged.',
 'ilc-home':'Currentown2027headline but no newlyfoundconfirmedannualdatedcourse; existingdossier not upgraded from headline.',
 'ilc-prices':'Currentown prices/dates withoutyear still; priorcarefulinvoice/transfer/laundry dossier unchanged, no new2027cohorts.',
 'fais-home':'Own generaleducation/technology/Englishofferings not proof technicalcamp EN. Archivedcamp dossier unchanged.',
 'fais-pdf':'Actual2page2026PDF bothpages viewed; phantomhiddenEnglish/grade/date text not visible andnot camp evidence. Priorcorrectdossier retained, no2027guess.',
 'stgeorge-barcelona-pdf':'Actual13page2026PDF selectedpage9 visually and robotics paragraph read;6–10/Jul6–31/3306459501240/Igniterobotics3D. Existingdossier unchanged; not whole13page seasonalprogramme audit.',
 'forest-fr':'Own2026–27 openexternal2–12/Englishcampdays/six exactweeks/450or480+40meals/40summerextendedhour/transportunpriced, nature/projects/pool; no inventedrobotics.',
 'eib-camps':'OwnMonceau twoOct19–23 2026 programmes:2.5–5castle and6–11primarysciencecoding/fullEN/8.5–17/650lunch/externalkids. Grades/DOB/internationalintake/contracts not assumed.',
 'beelingue-autumn':'OwnOct19–23Paris3–10/Oct26–30Levallois5–10/differentvenues/halfday/partnermove. EN all-neededblocks ofpartnercamp separatelyunknown.',
 'beelingue-pdf':'Actual6pagePDF selected3/4/5visual: Paris3–6and7–10timetable/495day225halfweek/25outing50two/foodBYO/10percentsecondconditional; Lev14–18/225week50day/15ludotheque, role15–17EN only directlyspecified.',
 'beelingue-terms':'OwnworkshopCGDV annual30family/48hcancellation/late-norefund/photooptout. Applicability tocamp/partnerinvoice not proven; no acceptance.',
 'ps-mediterranean':'Own2026–27 listedtwoOctoberScienceEnglish7–12 androbotics8+ separately; no detailedscience curriculum/format/fullpackage yet, gap only.',
 'ps-english1':'OwnOct19–23 title7–12/190EUR/address11rueSansPeurGrasse06130; detailedtimes/boarding/inclusions not provided. No newtopdossier from title alone.',
 'ps-english2':'OwnOct26–30 same titleage/190EUR/Grasseaddress; selecteddetails no newdetailedprogramme or2027dates.'}
receipts=[q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(receipts)==39 and {q['key'] for q in receipts}==set(scopes)
for q in receipts:
    assert q.get('status')==200
    ext='.pdf' if (PRIMARY/(q['key']+'.pdf')).exists() else '.html';f=PRIMARY/(q['key']+ext)
    assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
    q.update(retrieval_method='direct_http',content_scope=scopes[q['key']],body_snapshot_retained=True,raw_filename=f.name,
             content_status='actual_pdf_selected_pages' if ext=='.pdf' else 'javascript_shell_no_programme_body' if q['key'] in ['futurekids','code-list'] else 'html_selected_programme_clauses')
visual=json.loads((PRIMARY/'visual-source-notes.json').read_text())
assert len(visual)==4 and sum(q['pages_visual_checked'] for q in visual)==8
urls={s['url'] for p in b['camp_programmes']['profiles'] for s in p['sources']}
added=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-urls);assert len(added)==21
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
cc={iso:sum(p['iso']==iso for p in c['profiles']) for iso in ['CHE','FRA','ESP','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','BRA','CHL','PHL']}
calendar=dict(events=len(d['events']),learning_records=sum(e['block']=='Лагеря' for e in d['events']),family_ics=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text().count('BEGIN:VEVENT'),
              exhibition_ics=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_text().count('BEGIN:VEVENT'),managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows'])
assert calendar==dict(events=3230,learning_records=1899,family_ics=2491,exhibition_ics=104,managed_dated_rows=1436,reused_legacy_events=69,season_windows=42)
checks=[
 '18newprogramme/format/age/venue dossiers across6operatorgroups:13CHE/5FRA. All680priorprofiles and3205priorrecords retained byte-logically;698dossiers/37countries/1087URL/21newURL.',
 '25new exactdatedrecords and25familyplanningICS;9Cosmo formatweeks/6CodeAI venuecohorts/6Forest seasonalweeks/2EIB/2BeeLingue. Unknownadmission/language remain TENTATIVE, not confirmedparticipation. No newregistrationdeadline or seasonwindow invented.',
 'Cosmo2027 actualPDF: morning350/full500/Academyonly10percent/Pascha280vswebTBC, camp age not inheritedfrom8+yearclass, giftmicrobit notpromisedtocamp, Wednesdaypool not15automaticroboticshours/nonrefund/personalinsurance.',
 'CodeCamp9distincttechnicalprogrammes and progression; cohortlanguageunconfirmed. Masters7–12vs8–13, AI9–13 vs13+account, MinecraftEducation/templicense/foodBYO/50lateequipmentfee, Australian2018terms applicability unresolved. Generic3D copiedtemplates notsyllabus or duration.',
 'ISSH7–10robot/sensor and11+simulator-toautonomousdrones are2026archive650CHF. DE/ENenvironment onlyyounggroup; no new2027dates/teacherlanguage or schoolboarding assumption.',
 'Forest ENcampLife2–12/openexternal/six2026–27weeks:450or480+40=490or520, two980or1040. 40summerextendedday/transportunpriced. EIB650lunch primary6–11 vs preschool2.5–5 andexactbirthday unknown.',
 'BeeLingueParisage3–6and7–10/495full225halfweek/foodBYO/25eachouting;1090two beforeannual30/discount, conditional1070.50 ifsecondtuition10percentandannualfee apply. Lev differentvenue/14–18/225week,EN15–17lessonrole; generalworkshopCGDV notautomaticallycampcontract.',
 '39directHTTP200retrievals/4actualPDFs/8selectedvisualpages. Codepubliclist andFuturekids JSshell no programmefacts. FlorimontENinterface/Albertfutureage/PlaneteSciencetitle-only/Spanisharchives/ILCyearmissing are opengaps; alloldprofiles retained.',
 'IndependentJSONSQLiteCSVMDICS/bridgeidempotence/JSfilters/oldUID-dates verification; allstaticfiles below26214400byte/native limit andpage_size1024 retained. RawHTML/PDF/renders private; public factualparaphrases/sourceURLs/hash/scopedreceipts only.',
 'Fullworldscope/prioritycountries/requirements/goalactive preserved;0countriesfullyaudited. Selection is editorial familyfit, not worldranking; internal medals not international results.'
]
audit=dict(asof=CHECKED,version=100,status='progress',scope='Swiss technical programme levels/format/price and French English-family holiday options, with scoped Spain/France archive cross-checks. Not wholeEurope/world.',
           new_dossiers=18,new_operator_groups=6,deepened_dossiers=0,updated_dossiers=[],programme_slugs=NEW,new_calendar_rows=25,new_family_session_ics=25,new_family_ics=25,new_registration_deadline_ics=0,new_season_windows=0,
           corrected_existing_event_ids=[],programme_dossiers=698,countries_with_dossiers=37,official_dossier_urls=1087,country_dossier_counts=cc,findings=c['gaps'][-4:],calendar=calendar,
           primary_retrievals=dict(direct_attempts=39,http200=39,retrieval_errors=0,javascript_shells_without_programme_body=2,unique_actual_pdfs=4,selected_visual_page_checks=8),
           fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
           next_priority='Continue fullworld2026–27 general/thematic/technical camps, boarding/day/family andEN/ES/RU instruction byactualprogramme. Prioritize CHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatinAmerica; verify currentseason/foreignindividualintake/DOB-grade/language/fullinvoice/contract/gear/ratio/places. DeepSwissgeneralboarding andFrench/Spanishseasonchanges remainactive. Leagues/competitions/exhibitions/childadmission/schools/results5–10years/familyroutes remainfullscope; no countryfullyaudited.')
def write(stem,value):
    txt=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(txt)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(txt)
write('europe-camp-audit-v100',audit)
write('europe-camp-source-receipts-v100',dict(asof=CHECKED,version=100,scope='39directselectedretrievals/4PDF/8selectedvisualpages only. Notwholewebsites/countries;rawHTML/PDF/renders remainprivate.',
      sources=receipts,visual_pdf_checks=visual,dossier_source_urls_added=added,external_actions=external,
      notes=['TwoJSshells no programmebody; publicclient identifiers not used/copied. No form/signup/consent/message/payment/account.',
             'ENinterface/support/campLife/teacher language separate; typedPDFghostEnglish andgeneric3D templates not accepted asprogramme evidence.',
             'Dossier count is formats/programmes/agegroups, not uniquebrands or independentranking. Futureintake/places/all-in unknown explicit.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=100:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Researchv98/nativev99publication succeeded; commit'+BASE+'; deploymentappgdep_6ac45a8428f4819181aaed8ee03fa7a6. Fullworldwideobjective unchanged.')
plan['latest_validation']=dict(version=100,asof=CHECKED,status='Independentselectedsource/preservation/calendarverification; nativepublicationreceiptseparate',events=3230,camp_learning_records=1899,programme_dossiers=698,countries_with_dossiers=37,official_dossier_urls=1087,family_ical=2491,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=cc)
plan['europe_camp_programme_audit_v100']=audit
plan['camp_catalog_integration'].update(asof=CHECKED,dossiers=698,countries=37,swiss=99,generated_calendar_entries=1436,reused_legacy_events=69)
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        q['evidence']='v100:698programme/formatdossiers in37countries/1087dossierURLs;18new across6operatorgroups13CHE5FRA,25exactcalendarandfamilyplanningICS.39directretrievals4PDF8selectedvisualpages. Swisslevels/gear/languageandageconflicts, FrenchENfamilyweeks/fullbaseexpenses, selectedSpainarchives reconfirmed; priorcontent/worldscope retained. Notcompleteworldwide.'
entry=dict(version=100,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=18,deepened_dossiers=0,new_calendar_rows=25,new_family_ics=25,corrected_existing_calendar_rows=0,official_primary_retrieval_attempts=39,unique_actual_pdfs=4,selected_visual_page_checks=8,not_complete_worldwide=True)
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=100]+[entry]
plan['next_research']=[audit['next_priority']];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED
write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=98','?v=100').replace('data-ui-version="98"','data-ui-version="100"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_europe_camp_audit_v100.json" download>Европа: технические треки и английские каникулы ↓</a> · <a href="downloads/STEM_europe_camp_source_receipts_v100.json" download>Проверенные страницы и брошюры ↓</a> · '
anchor='<a href="downloads/STEM_asia_camp_audit_v98.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=698,new_dossiers=18,new_calendar_rows=25,new_family_ics=25,source_urls=1087,goal='active')))
