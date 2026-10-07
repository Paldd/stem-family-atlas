"""Record selected primary clauses and continued worldwide scope; receipts remain scoped."""
import hashlib,json,subprocess
from pathlib import Path
from camp_americas_v106 import CHECKED,NEW
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v106'
BASE='ed1911191baa568d0082d2212685482e5e0946b3'
old=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
before={e['id']:e for e in old['events']};fresh=[e for e in d['events'] if e['id'] not in before]
assert len(fresh)==14 and all(e==before[e['id']] for e in d['events'] if e['id'] in before)
assert c['counts']['dossiers']==778 and c['counts']['source_urls']==1215
scopes={
 'steamup-winter':'ActualownDec21 2026–Jan1 2027/closed24,25,31,Jan1/MonFri/6attendance days/Nov15registrationdeadline/from250unitunknown/5–15vsbody3–15/care84week/1.85min/sibling10oldest. ExistingCP586unchanged/no duplicatecalendar.',
 'journey-winter':'ActualWinter2026fourcourses/FirstenburgVancouverWAandBeavertonOR/Dec21–23and28–31/7–11,6–10,7–12,6–10/219,289,289,249USD/early20lessbyNov2/max20/agegroups/showcase. WinterexactcheckoutcontradictsFAQservicefee;earlypriceconditionnotregistrationdeadline.',
 'robothink-nexus':'HTTP200only2167byteJSshell/no readableprogrammeclauses. CachedsearchsnippetnotactualverifiednewWinter2026camp;no new dossier.',
 'kidnetix-winter':'ActualDec21–31 2026/0830–1630/4–12/175CAD2weeksEARLYBIRD/mayLEGOrobotics/generalactivities. Dailyholidayattendance/regularprice/earlydeadline/teacherlanguage/refundunknown;notguaranteedrobotintensive.',
 'nova-mex-itcamp':'ActualownSpanish8–12/12–15/LEGOEducationPrime/Roblox/Minecraft/3D/PixelArt/allmaterials/ownlunch. MainVerano2025July21fiveweeks09–13or14–18,cardInvierno/EstadoMexicoand1000noexplicitcurrency/yearcontradictCDMXaddress. No2026–27datesinvented.',
 'pyrox-home':'ActualFRC10225secondary/highschool/outreachAstroCampPapaloteMonterrey/TecmilenioGuadalupe/ownimpactclaims. Noage6/9open2027campdates/price/intake;notproofwinningrankingoruniversalfreefamilyadmission.',
 'fod-oferta':'Actualownfourformativepillars/no newdated2027campfee/age/EnglishSpanishprogrammeintake. Regularprogrammesnotconvertedintofutureholidaycohorts;no new dossier.',
 'envision-winter':'ActualownindexWinter2026Dec21–24/28–31andMarch15–19 2027/5–13. ExistingCP299unchanged;actualproductsstillconflictdates/year.',
 'journey-faq':'ActualallLEGOrobotsChromebookmaterialsprovided/noowngear/beginner/groups/authorizedpickup/backgroundchecks. enropsservicefeeatcheckout/refund>15minus35vsownpolicyupto15/operatorcancelsfull/weatheroneunrefunded;Englishteacherunknown.',
 'journey-refund':'ActualupdatedSept20 2026/upto15daysminus35USD/nonattendanceandlatecancelnone/medicalcasebycase/transfer≥7dayspossiblefees. Exact15boundarywithFAQunresolved;no consent.',
 'steamup-thanks':'ActualNov23–27 2026/Nov26closed/fourattendance days/09–17/care08–18/from250unitunknown/5–15vs3–15/siblingcarefees. ExistingCP585unchanged.',
 'steamup-spring':'ActualMar15–19 2027/fivedays/09–17/starting250perweekexplicit/codingengineering/5–15vs3–15/care84week/late1.85min. ExistingCP587unchanged/no duplicatecalendar.',
 'steamup-home':'ActualoperatorK8/afterschool/camps/VEXIQoffering;schoolteamsnotproofcampinternationalwins/Englishteacher/fullinvoice.',
 'envision-winter-product':'ActualproductDec22–24/Dec29–30withoutyear/two5–8and9–13curricula/no experience. Productdatesnotcurrentindex21–24/28–31;no duplicateornewconfirmedcohort.',
 'envision-march-product':'ActualproductMar16–20 2026/5–8SearchRescue/9–13AIandYouTube/oldfees/care/norefundmedicalcreditdiscretion. IndexMar15–19 2027notthisoldproduct;no2027datesinvented.',
 'explorations-home':'HTTP406/directno body;actualownlinkedprogrammeclausesreadthroughprimarywebreaderelsewhere,notwholehomeaudit.',
 'explorations-break':'HTTP406/directno body;fallbackprimarySchoolBreakactual7–15/winterroboticsgames/spring3Dgames/485CAD/week/6591Somerled/dropoffconflict/care60week.',
 'explorations-policies':'HTTP406/directno body;fallbackprimaryactualwritten10daysminus10%admin/latecare25day/late5min/nutfreefood/threewarningsdischargewithoutrefund. No submission/consent.',
 'explorations-rates':'HTTP406/directno body;fallbackactualheading2026/priorJuly785/JuneAug445/care60or120/two+sessions10%;notnew2027price,age9Aug23–27actual545.',
 'explorations-age6':'ActualownlinkedpublicZeffyage6Kindergarten2027/Jul5–16and19–30/785CADeach/2290Cavendish6645deMaisonneuve/dropoff08–0845/pickup1530–16/care16–18. No Add/Continue/donation/consent.',
 'explorations-age9':'ActualownlinkedpublicZeffyage9Summer2027/fiveTechweeks/June28–July2games3D/July2twoweek785/Aug2–6games445/Aug9–13games445/Aug16–20RobotsEngineering445/Aug23–27PrintingEngineering545. Actualage10/7feesunknown/no Add/Continue.'
}
r=[q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(r)==21 and sum(q.get('status')==200 for q in r)==17 and set(scopes)=={q['key'] for q in r}
for q in r:
    q.update(retrieval_method='direct_http',content_scope=scopes[q['key']],checked=CHECKED)
    if q.get('status')==200:
        f=PRIMARY/(q['key']+'.html');assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
        q.update(body_snapshot_retained=True,raw_filename=f.name,content_status='javascript_shell_no_specific_programme_body' if q['key']=='robothink-nexus' else 'selected_html_clauses')
    else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body')
for filename,urls,scope in [
 ('explorations-primary-web.json',[E for E in ['https://explorationslearning.com/school-break-camps/','https://explorationslearning.com/our-policies/','https://explorationslearning.com/rates/']], '3actualprimarypages/selectedSchoolBreakcurriculum485/datesage7–15/LearningLab/contract10daysminus10/carefood/2026ratesnot2027invoice.'),
 ('explorations-registration-primary-web.json',['https://explorationslearning.com/registration/','https://www.zeffy.com/en-CA/ticketing/age-9-summer-camp-2027-next-year','https://explorationslearning.com/explorer-program-ages-6-7/'], '3actualprimarypages/current2027datesagefirstday/6gradefork/age9new445vs545/Explorerold2026curriculumexamples. Separateage6webreadererrorcontenttoo large;directHTTPage6bodylaterretained.')
]:
    body=(PRIMARY/filename).read_bytes();r.append(dict(key=filename.removesuffix('.json'),urls=urls,retrieval_method='primary_web_reader',checked=CHECKED,raw_filename=filename,bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),body_snapshot_retained=True,content_status='selected_primary_web_reader_clauses',content_scope=scope))
urls={s['url'] for p in old['camp_programmes']['profiles'] for s in p['sources']}
added=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-urls);assert len(added)==12
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
cc={iso:sum(p['iso']==iso for p in c['profiles']) for iso in ['CHE','FRA','ESP','ITA','GBR','CHN','HKG','FIN','TWN','SGP','JPN','KOR','THA','MYS','USA','CAN','CRI','MEX','BRA','CHL','PHL']}
cal=dict(events=len(d['events']),learning_records=sum(e['block']=='Лагеря' for e in d['events']),family_ics=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text().count('BEGIN:VEVENT'),exhibition_ics=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_text().count('BEGIN:VEVENT'),managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows'])
assert cal==dict(events=3337,learning_records=2006,family_ics=2591,exhibition_ics=104,managed_dated_rows=1543,reused_legacy_events=69,season_windows=49)
download=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text())
checks=[
 '9newdossiers/4operatorgroups/14exactcalendarrows/14familyplanningICS/0newdeadlines/0newseasonwindows. Allold769dossiers/3323events unchanged;778total/39countries/1215URLs/12newURLs. Notworldrankingorwholecountryaudit.',
 'JourneyfourWinter2026technicalcourses/age6or7gate/219,289,249USD/early20lessbyNov2/allmaterialsChromebooksprovided/max20. VancouverWashingtonUSAnotCanada; ENteacherunknown, checkoutservicefeeand15dayrefundconflictsvisible;earlypriceconditionnotregistrationdeadline.',
 'STEAMUPexistingCP585–587freshprimaryreread/no duplicatecard/day/ICS/deadline. Thanksgivingfour/wintersixactualdays/Nov15deadlinepreviouslypresent/closed24,25,31DecandJan1 preserved;from250winterunitunknown/spring250perweek/5–15vs3–15/care84/late1.85min. OwnschoolVEXnotcampwin.',
 'Explorationscurrentregistration2027/actualage6kindergartenandage9publicZeffy785Julytwo-week/5technicalweeksage9prices445,445,445,445,545/RobotsAug16–20. Previous2026Explorer/ratesdatesnotnew2027syllabus/fees;ENteacherunknown/6gradefork/7min/DOB/age10tariffnotapproved. KellsJulyvsSomerledTech/location/holidaydropoffconflicts visible.',
 'Kidnetixgeneral4–12/175CAD2weeksEARLYBIRD/mayroboticsnotguaranteedintensive/Christmasattendanceunknown. NOVAexplicitEspañol8+LEGOPrime/Roblox/3D/allmaterialsownlunchbutarchive2025/wintertitlecurrencyconflicts/no invented2026–27dates. OscarNOVAcurrentlytoo young.',
 '21directattempts/17HTTP200/16HTMLclausebodies/1JSshell/4HTTP406errors.2retainedprimarywebreaderresponseswith6actualselectedprimarypagebodies(5ownsiteand1ownlinkedage9)+1age6readererror later recovered direct. No entirewebsite/country audit.',
 'FullSQLite ZIP verified byte-for-byte before removing oversize rawdownload; allschemas/oldrelationalrows retained/newJSONSQLCSVICS equal. HumanUI download nowZIPwithREADMEandsha256manifest; no records cut for hosting size.'
]
next_priority='Continue fullworld2026–27 general/thematic/STEM camps/day/boarding/family EN/ES/RU, especially CHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatAm. Actualfullinvoices/ageDOBgrades/foreignindividualintake/teacherlanguagevslessons/life/support/gear/nightcare/refunds/currentplaces. Schools/results5–10years/leagues/competitions/exhibitions/familyroutes remain active;0fullyauditedcountries. VerifiedcompleteSQLiteZIP preservesworldscope as databasegrows;neverreducecountry/programme coverage tofitstaticlimits.'
audit=dict(asof=CHECKED,version=106,status='progress',scope='SelectedUSA/CanadaWinter2026–27andSummer2027/curricula/dayfees/contracts;MexicoSpanisharchiveandCostaRica/Mexiconon-specificintakegaps. NotcompleteAmericas/world.',new_dossiers=9,new_operator_groups=4,deepened_dossiers=0,updated_dossiers=[],programme_slugs=NEW,new_calendar_rows=14,new_family_session_ics=14,new_family_ics=14,new_registration_deadline_ics=0,new_season_windows=0,corrected_existing_event_ids=[],programme_dossiers=778,countries_with_dossiers=39,official_dossier_urls=1215,country_dossier_counts=cc,findings=c['gaps'][-6:],calendar=cal,primary_retrievals=dict(direct_attempts=21,http200=17,selected_html_bodies=16,javascript_shell_no_programme_bodies=1,retrieval_errors=4,unique_actual_pdfs=0,selected_visual_page_checks=0,primary_web_reader_response_files=2,primary_web_reader_selected_page_bodies=6,primary_web_reader_errors=1),fully_audited_countries=0,worldwide_complete=False,complete_database_download=download,external_actions=external,validation=checks,next_priority=next_priority)
def write(stem,value):
    txt=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(txt);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(txt)
write('americas-camp-audit-v106',audit)
write('americas-camp-source-receipts-v106',dict(asof=CHECKED,version=106,scope='Selected21directattempts/17success including1unusableJSshell/4errors and2retainedprimarywebreaderresponses. Rawbodyprivate;notwholewebsites/countries.',sources=r,dossier_source_urls_added=added,external_actions=external))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=106:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Research/nativepublication105 succeeded;commit '+BASE+';deployment appgdep_6ac47995cf708191a627b13e6bd9bee4. Fullworldobjective unchanged.')
plan['latest_validation']=dict(version=106,asof=CHECKED,status='Independent selected-source/preservation/calendar/completeDBZIP verification; nativepublication receipt separate',events=3337,camp_learning_records=2006,programme_dossiers=778,countries_with_dossiers=39,official_dossier_urls=1215,family_ical=2591,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=cc)
plan['americas_camp_programme_audit_v106']=audit
plan['complete_database_download']=download
plan['camp_catalog_integration'].update(asof=CHECKED,dossiers=778,countries=39,swiss=106,generated_calendar_entries=1543,reused_legacy_events=69)
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:q['evidence']='v106:778dossiers/39countries/1215URLs;9newprogramme cards/14exactcalendarrows/14familyICS. Actualprimaryprogrammes/pricing/age/teacherlanguage/contractconflicts visible;alloldrecords retainedinverifiedcompleteSQLiteZIP. Notcompleteworldwide.'
entry=dict(version=106,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=9,deepened_dossiers=0,new_calendar_rows=14,new_family_ics=14,new_season_windows=0,corrected_existing_calendar_rows=0,official_primary_retrieval_attempts=21,unique_actual_pdfs=0,selected_visual_page_checks=0,not_complete_worldwide=True)
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=106]+[entry]
plan['next_research']=[next_priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED
write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=105','?v=106').replace('data-ui-version="105"','data-ui-version="106"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text();anchor='<a href="downloads/STEM_asia_camp_audit_v105.json"'
link='<a href="downloads/STEM_americas_camp_audit_v106.json" download>Америка: ближайшие технические и общие программы ↓</a> · <a href="downloads/STEM_americas_camp_source_receipts_v106.json" download>Проверенные источники Америки ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=778,new_dossiers=9,new_calendar_rows=14,new_family_ics=14,source_urls=1215,complete_database_zip_bytes=download['archive_bytes'],goal='active')))
