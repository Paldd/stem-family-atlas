"""Publish bounded progress evidence without treating the world inventory as complete."""
import hashlib, json, subprocess
from pathlib import Path
from camp_asia_v95 import NEW, UPDATED, W

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT.parent/'stem-family-atlas-work/camps-primary-v95'
BASE = 'dfc36a921a2030d2d0090c77314d256b100b2cd7'
before = json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d = json.loads((ROOT/'data/catalog.json').read_text()); c = d['camp_programmes']
old = {e['id']:e for e in before['events']}
new = [e for e in d['events'] if e['id'] not in old]
assert len(new)==17 and all(e==old[e['id']] for e in d['events'] if e['id'] in old)
assert c['counts']['dossiers']==631 and c['counts']['source_urls']==992
receipts = [q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(receipts)==30 and sum(q.get('status')==200 for q in receipts)==21
scopes = {
 'whizz-home':'Direct406, not a successful HTTP body. Own visible homepage and actual product links observed separately in browser.',
 'mind-guide':'Own year-end2026 reference/2027 unannounced context read; comparisons of other operators are secondary and not adopted as primary facts.',
 'mind-courses':'Guessed noncanonical path redirects to PageNotFound with HTTP200; soft404, not a programme or admitted source.',
 'tcs-steam':'Own actual2–6Feb2026 archive: English-based/G5–7/Microbit/science/19000 includes2000 materials/lunch, min10/max15/no transport. Relevant refund/payment clauses read; not2027 dates, places or admission.',
 'science-camps':'HTTP200 but extracted own page contains generic navigation/footer, not a camp schedule. Not evidence of a dated holiday camp.',
 'harrow-winter':'Own13–19Dec2026 exact daily timetable/5mornings/6nights/9–13/440k public tax included/352k currentstudents.13h45 morning and13h20 snow windows include groups/tests/races, not measured purecoding hours. Parent bus/device rules read; insurance/cancel not established. Prior calendar row retained.',
 'mind-home':'Own year-end2026 season establishes year of detailed Nov/Dec tables; March/June2027 posted around6weeks before breaks is not actual future dates.',
 'mind-sprint':'Own dated Nov/Dec syllabus with old June title/FAQ retained as context. Creative generativeAI/Roblox/vibecoding/video, not modeltraining or externalinternationalleague.4-day price and28Dec hour contradiction retained.',
 'mind-story':'Own course exact5-day680/4-day600 table10–13 versus generic14–17/afterearly800. Broad system2025–2030 range not continuously opencamp. No formfields/consent/Pay used.',
 'mind-story-guide':'Own day-by-day creative syllabus, approx3–7 students/80page manual, basiccomputer requirements. Operatorquality claims not independentratings;4-day syllabus/Englishteacher stillunknown.',
 'mind-courses-canonical':'Actual own courseindex/course_group links, distinctAI/Sprint/Story/adult/school courses. Adult courses not childcamp; no booking/application.',
 'mind-faq':'Relevant own desktop/transfer/emergencycredit/makeup/nonrefund/similar-age siblings clauses read; not fullcampcontract or admissionapproval.',
 'whizz-2027':'Direct406, not a successful HTTP fetch. Own browser upperblock22–26Feb/1–5Mar2027 and oldSummer2026 Description inspected separately; age selector7–12 then CampDatesempty, no AddToCart.',
 'whizz-2026':'Direct406, browser currentOct19–23/26–30 and oldSummer2026 Description separatelyobserved. No AddToCart.',
 'whizz-programmes':'Direct406, own correct separate programmeURLs observed in browser, not inferred from brokenhomepage links.',
 'science-kidsstop':'HTTP200 generic navigation/footer, no workshop body in direct extraction. Web search ownsnapshot mentions pastMay/June short1–1.5h parent-child workshops, not admitted as new future multi-day camps.',
 'ilri-home':'OwnLEGO TeachingEnglishandChinese explicit; Englishprogramminginterface ofgamecourses distinguished. InstituteNASA/exclusivehost/awardmarketing not independentlyvalidated or adopted as rankings.',
 'curious-winter':'Direct406 and no programmebody inspected. Candidate not admitted; not counted as successfullyaudited programme/country.',
 'iamfuture-about':'Own2024 charitycamp/outreach fornewresident/disadvantagedchildren. Not an advertised open2026/27internationaltouristcamp, volunteer intake not child admission.',
 'lighthouse-current':'Own currentprogramme/menu andwinter26–27 title observed; four previouslypublishedLighthouse dossiers unchanged, no automaticnewcohort or duplicateoperator.',
 'whizz-nlcs':'Direct406; own browser currentOct12–16/4–6Crafty/7–12Medley/450$/09–12/currentstudentdiscount observed separately. Productimageactivityposters not read; not language/availability/completeinvoice proof.',
 'whizz-smash':'Direct406; own browser Sep/Octselector7–12/340–400$/50$familytotal observed separately. Public+Oct12selection did not resolve individualprice. ThirdpartyNov–Dec not admitted.',
 'whizz-holiday':'Direct406; own browser generalSTEAM/customforeignschoolgroup page read separately. Groupadmission not individualforeignchildacceptance; Englishwebsite notEnglishteaching.',
 'whizz-about':'DirectTLS timeout; no body inspected. Not used as programme/teachingevidence.',
 'ilri-donghu-form':'Actualownlinkedpublic2026form GET: specific10track/campus options,7four-dayweeks/incomingG1–9/RobloxG4+,13200regular/9500expiredJuneearly/1000admininsidefee/device-rental/paidrobotgift/pickupfees. No personaldata/Next/consent/payment.',
 'ilri-keelung-form':'Actualownlinkedpublic2026form GET:7specificcampus/track options, differentthemeorder fromDonghu. Genericagechoices4–18 do not overridegradegates. No personaldata/Next/submission.',
 'mind-sprint-course':'Guessed aisprint path soft404 with HTTP200, not admitted as owncamp source. Actualcourse found viaown courseindex separately.',
 'mind-sprint-actual-course':'Actualown index-linked course4935 Nov/Dec2026 tables andSGD6005×2h. Template2025–2028 not futurecontinuouscamp.4-day exactprices unconfirmed,28Dec14–16vs3h conflict. No formfields/consent/Pay.',
 'branksome-admissions':'Own current2026–27 regularschoolage/educationalhistory information read; not a campgate or assignment of actualfamilygrades frombirthyears.',
 'branksome-camp-pdf':'Actual6-pagePDF createdApr2016, body2016SummerSeries/2016–17. RelevantEnglishintro/Prep read andpage2 visuallychecked; otherpages not claimedfullyaudited. ExistingBranksomegirls/PYP/MYP prep, not new2026/27camp.'
}
for q in receipts:
    q.update(retrieval_method='direct_http',content_scope=scopes[q['key']])
    f = PRIMARY/(q['key']+'.pdf')
    if not f.exists(): f = PRIMARY/(q['key']+'.html')
    q['body_snapshot_retained'] = f.exists()
    if f.exists():
        assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
        q['raw_filename'] = f.name
    if q['key'] in ['mind-courses','mind-sprint-course']:
        q['content_status'] = 'soft_404_not_programme'
    if q['key'] in ['science-camps','science-kidsstop']:
        q['content_status'] = 'navigation_only_not_programme'
    if f.suffix=='.pdf' and f.exists():
        info = subprocess.check_output(['/opt/homebrew/bin/pdfinfo',str(f)],text=True)
        q['pdf_metadata'] = {line.split(':',1)[0]:line.split(':',1)[1].strip() for line in info.splitlines() if line.startswith(('Title:','Pages:','CreationDate:','ModDate:'))}
urls = {q['key']:q['url'] for q in receipts}
for key in ['whizz-home','whizz-programmes','whizz-2027','whizz-2026','whizz-nlcs','whizz-smash','whizz-holiday']:
    f = PRIMARY/(key+'-observed.txt')
    receipts.append(dict(key=key+'-observed',url=urls[key],retrieval_method='browser_visible_dom_selected_clauses',
        content_status='selected_observation_not_http_body',raw_filename=f.name,bytes=f.stat().st_size,
        sha256=hashlib.sha256(f.read_bytes()).hexdigest(),body_snapshot_retained=True,
        content_scope=scopes[key]+' Retained file transcribes selected visible clauses/dropdown observations, not a complete rawHTML/AX dump or a complete policy review.'))
oldurls = {s['url'] for p in before['camp_programmes']['profiles'] for s in p['sources']}
added = sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls)
assert len(added)==17
external = dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False)
countrycounts = {s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','BRA','CHL']}
checks = [
 'Nine new programme dossiers across4operatorgroups, not9independent top-ranked operators.631total/37countries/992own-dossierURLs.622priorIDs/order and621unrelated dossiers retained; onlyHarrowAppi existingprofile deepened.',
 'All3123prior events/leagues/competitions/exhibitions/schools/results/familyroutes preserved exactly.17newfuturecalendarrows/ICS only;19actualpastcampvariants retained in dossiers, not copiedinto2027 or addedasfuturecalendar.',
 'LPE own2026/27upperdates vs oldsummerDescription/4–6/7–12 conflict preserved;2027selectorempty notplacesproof. WhizzEN/GST/currency unknown. Smash ownOctdates override no secondaryNov/Dec claim; member/public price not invented and family50discount totalnotperchild.',
 'MindSprint/Story separateage9+/8+ courses;10own2026futurecohorts. StoryAMtable/genericPM and680/600/800 conflicts, Sprint28Dec8or12h conflict andunknown4-dayfee retained. CreativeAI/noexternalinternationalmedal. ENwebsite/prompt not humanEnglishteacher.',
 'ILRI actual17specificcampus/track variants split8LEGO/5Minecraft/4Roblox; allarchive2026. Grade1gate/Roblox4+ not inferredfrombirthyear or genericage4–18. ConfirmedbilingualENonlyLEGO, gameEnglishinterface notteacher.13200/9500expired/1000insidefee andpaidkit preserved.',
 'TCS actualFeb2026English-based/G5–7/19000includes2000materials/lunch archive, no new2027date. Actualfamilygrades unknown; no false childeligibility fromDOB. BranksomePDF6pages metadata/body2016/page2visual not2026camp; currentregularschoolgradechart notcampgate.',
 'Harrow5mornings13h45 includegrouping/tests/races, snow13h20,6nights/7calendar dates,440000JPYpublictaxincluded/352000onlycurrentstudents. No purecodinghour/parentboarding/registrationacceptance claim.',
 'Allprimaryretrievalmethods/errors/soft404/navigation-only responses and7selectivebrowserobservations recorded honestly. RawHTML/PDF/form/render text outsidecheckout; publicexports only paraphrases/URLs/hashes. No personaldata/formsubmission/cart/payment.',
 'CanonicalJSON/SQLite/CSV/JS/MD/ICS consistency, stableoldUID/date/deadline, bridgeidempotence andlanguage/age/phase filters independently checked. Allworld requirements/priorities retained,0fullyauditedcountries/nativegoalactive.'
]
audit = dict(asof='2026-10-05',version=95,status='progress',
    scope='Own Singapore/Taiwan programme cohorts/contracts, deeper Japan winter timetable, Korea archive exclusion; bounded progress, not complete Asia/world.',
    new_dossiers=9,new_operator_groups=4,deepened_dossiers=1,updated_dossiers=UPDATED,
    new_calendar_rows=17,new_family_ics=17,new_registration_deadline_ics=0,corrected_existing_event_ids=[],
    historical_variants_not_added_as_future=19,programme_dossiers=631,countries_with_dossiers=37,official_dossier_urls=992,
    country_dossier_counts=countrycounts,programme_slugs=NEW,findings=c['gaps'][-4:],
    calendar=dict(events=3140,learning_records=1809,family_ics=2401,exhibition_ics=104,managed_dated_rows=1346,reused_legacy_events=69,season_windows=39),
    primary_retrievals=dict(direct_attempts=30,http200=21,direct_errors=9,soft404=2,navigation_only=2,selective_browser_observations=7,actual_pdfs=1,visual_page_checks=1),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
    next_priority='Continue full Switzerland/France/Spain/Europe, Taiwan/Singapore/Korea/Japan/Asia, USA/Canada/CostaRica/Mexico/LatinAmerica and allworldcountry2026–27 general/thematic/boarding/day/family camp inventory. Verify freshowncohorts, actualDOB/grade, EN/ES/RU teaching/support roles, foreignintake, currentplaces, specificsyllabus/technicallevel,fullseasoninvoice/contract, campusmap andfamilycomparisons. Keep leagues/competitions/exhibitions/admission/schools/results5–10years/familyroutes active; no country fullyaudited.')

def write(stem,value):
    text = json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'data'/f'{stem}.json').write_text(text)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(text)

write('asia-camp-audit-v95',audit)
write('asia-camp-source-receipts-v95',dict(asof='2026-10-05',version=95,
    scope='30directattempts including9errors/2soft404/2navigation-only, plus7selectivevisible-browserobservations.1actual2016PDF/relevantpage2visual; not allprogrammes/operators/countries reviewed.',
    sources=receipts,dossier_source_urls_added=added,external_actions=external,
    notes=['HTTP200 alone is not a valid programme body; failures/navigation-only/soft404 explicit.',
        'Visible-browser observations transcribe selected clauses, not fullHTTP/AX/screenshot evidence or certifiedavailableplaces.',
        'Archive2026 dates/rates/discounts are not automatically2027 and gradecharts are not actualchildgrades.',
        'Rawsource/bank/payment/formtext remains private scratch; publicexports only scope/paraphrases/URLs/hashes. No contact/form/cart/booking/payment.']))
plan = json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=95:
    plan['latest_validation_previous'] = plan['latest_validation']
plan['previous_goal_turn_classification'] = dict(classification='progress',asof='2026-10-05',
    evidence='v94 native publication succeeded; commitdfc36a921a2030d2d0090c77314d256b100b2cd7; deploymentappgdep_6ac440a31bac819182be24cd1e097c51. Expanded worldwide objective preserved.')
plan['latest_validation'] = dict(version=95,asof='2026-10-05',status='Independentprimary/preservation/calendarverification; nativepublicationreceiptseparate',
    events=3140,camp_learning_records=1809,programme_dossiers=631,countries_with_dossiers=37,official_dossier_urls=992,
    family_ical=2401,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=countrycounts)
plan['asia_camp_programme_audit_v95'] = audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=631,countries=37,swiss=86,generated_calendar_entries=1346,reused_legacy_events=69)
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        q['evidence'] = 'v95:631 programme/venue/format dossiers in37countries;9new across4operatorgroups+1deepenedJapan,17newfuturecohorts/ICS,992dossierURLs. Singapore/Taiwan primaryprogramme/fees/grades/language conflicts and Korea2016archive exclusion.19pastvariants not copiedinto2027; fullworld objective stillactive.'
entry = dict(version=95,asof='2026-10-05',status='progress',scope=audit['scope'],new_dossiers=9,deepened_dossiers=1,
    new_calendar_rows=17,corrected_existing_calendar_rows=0,new_family_ics=17,official_primary_sources=17,not_complete_worldwide=True)
plan['research_passes'] = [q for q in plan.get('research_passes',[]) if q.get('version')!=95]+[entry]
plan['next_research'] = [audit['next_priority']]
plan['status'] = plan['native_goal_status'] = 'active';plan['updated'] = '2026-10-05'
write('research-plan',plan)
p = ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=94','?v=95').replace('data-ui-version="94"','data-ui-version="95"'))
p = ROOT/'dist/assets/camp-programmes.js';s = p.read_text()
link = '<a href="downloads/STEM_asia_camp_audit_v95.json" download>Азия: новые программы, цены и возрастные уровни ↓</a> · <a href="downloads/STEM_asia_camp_source_receipts_v95.json" download>Первичные страницы, формы и архивы ↓</a> · '
anchor = '<a href="downloads/STEM_europe_camp_audit_v94.json"'
if link not in s:
    assert anchor in s;s = s.replace(anchor,link+anchor,1)
if "archive_next_unannounced:'" not in s:
    s = s.replace("next_unannounced:'Следующий набор уточнить'", "next_unannounced:'Следующий набор уточнить',archive_next_unannounced:'Архив2026 · новый набор не объявлен'")
if '<option value="archive_next_unannounced">' not in s:
    s = s.replace('<option value="next_unannounced">Следующая смена не объявлена</option>', '<option value="next_unannounced">Следующая смена не объявлена</option><option value="archive_next_unannounced">Архив2026 · новый набор не объявлен</option>')
if "engineering:'" not in s:
    s = s.replace("entrepreneurship:'Предпринимательство'", "entrepreneurship:'Предпринимательство',engineering:'Инженерия',stem:'STEAM / STEM',games:'Игры / геймдизайн'")
p.write_text(s)
print(json.dumps(dict(dossiers=631,new_dossiers=9,new_operator_groups=4,deepened_dossiers=1,new_calendar_rows=17,new_family_ics=17,source_urls=992,goal='active')))
