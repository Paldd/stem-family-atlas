"""Bounded European source audit; archive and native publishing are separate receipts."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v88'
BASE='2d76829dc5390385a77c0192084e000c482b9082'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
oldp={q['slug']:q for q in b['camp_programmes']['profiles']};old={e['id']:e for e in b['events']}
fresh=[q for q in c['profiles'] if q['slug'] not in oldp]
changedp=[q['slug'] for q in c['profiles'] if q['slug'] in oldp and q!=oldp[q['slug']]]
new=[e for e in d['events'] if e['id'] not in old];changed=[e['id'] for e in d['events'] if e['id'] in old and e!=old[e['id']]]
assert len(fresh)==18 and len(new)==22 and len(changed)==35 and set(changedp)=={'le-rosey','les-elfes','tasis'}
assert c['counts']['dossiers']==547 and c['counts']['source_urls']==829
receipts=[v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts)==39 and sum(v.get('status')==200 for v in receipts)==37
for v in receipts:
    if v.get('status')==200:
        f=next(PRIMARY/(v['key']+ext) for ext in ['.html','.pdf'] if (PRIMARY/(v['key']+ext)).exists())
        assert hashlib.sha256(f.read_bytes()).hexdigest()==v['sha256']
        v.update(raw_filename=f.name,body_snapshot_retained=True,content_scope=(
            'Campus map downloaded; not used as verified programme/coordinate evidence' if v['key'] in ['rosey-plan-rolle','rosey-plan-gstaad'] else
            'Website-use/privacy terms, not camp cancellation contract' if v['key']=='rosey-terms' else
            'Linked HPAIR file identifies JBCN host and conflicting3/5-day duration; not admitted as exact Paris cohort' if v['key']=='ics-hpair-public-file' else
            'Primary body retained; programme facts, read depth and boundaries described in dossiers/audit'))
webfile=PRIMARY/'robbo-web-primary.txt'
webread=dict(url='https://robboclub.es/barcelona/campverano26',method='web tool full primary page read; direct HTTP403 retained separately',
    raw_filename=webfile.name,sha256=hashlib.sha256(webfile.read_bytes()).hexdigest(),bytes=webfile.stat().st_size,read_scope='Own summer2026 curriculum, ages, dates, fees. Teaching language unconfirmed; weekday typo retained. Not a direct HTTP200 receipt.')
visual=[]
for f,key,page,note in [
    ('leselfes-winter-pdf-p1.png','leselfes-winter-pdf',1,'WINTER2026–27 tariff matrix inclAprilI2300;registration150/medical120/helmet15,languageperiod50min and optionalfees.'),
    ('leselfes-winter-pdf-p2.png','leselfes-winter-pdf',2,'Boarding cancellation CHF500/week deduction with policy;medical120/week;visa-denial clause separate, not day terms.'),
    ('leselfes-day-pdf-p1.png','leselfes-day-pdf',1,'DAY2026–27 350/450,medical25/day,helmet3,deposit200,EN/FR50min/noSaturday.'),
    ('leselfes-day-pdf-p2.png','leselfes-day-pdf',2,'Day specific60/30/29-day cancellation thresholds;paragraph2 differs, not winterboarding policy.'),
    ('rosey-financial-p1.png','rosey-financial',1,'Title explicitly SUMMER2026;deposit1000/selectiveadmission, not2027contract.'),
    ('rosey-financial-p3.png','rosey-financial',3,'Cancellation before1May2026 returns70percent;not copied to2027.'),
    ('rosey-atglance-p2.png','rosey-atglance',2,'Multi-column camp/academy matrix:Tech11–15,Excellence13–16,MyFamily13200;2027 cover checked separately.'),
    ('ics-ai-pdf-p1.png','ics-ai-pdf',1,'HWCS CertificateofParticipation,Grades6–12,730EUR,29Jun–3Jul2026,Paris host;no degree/award claim.'),
    ('ics-camp-pdf-p1.png','ics-camp-pdf',1,'BackToSchool3–16,100percentEnglish,24–28Aug2026,studentsentering/returningICS;pricing continues secondpage.'),
    ('ics-yira-p3.png','ics-yira-public-file',3,'YIRA Paris dates/Grades6–12/studentassociationcertificate;20April2026deadline conflicts15JuneHTML.')]:
    bb=(PRIMARY/f).read_bytes();r=next(v for v in receipts if v['key']==key)
    visual.append(dict(url=r['url'],page=page,method=note,render_sha256=hashlib.sha256(bb).hexdigest(),render_bytes=len(bb)))
oldurls={s['url'] for q in oldp.values() for s in q['sources']}
added=sorted({s['url'] for q in c['profiles'] for s in q['sources']}-oldurls);assert len(added)==25
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False)
learning=sum(e['block']=='Лагеря' for e in d['events'])
byiso={s:sum(q['iso']==s for q in c['profiles']) for s in ['CHE','FRA','ESP','KEN','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','MYS','USA','CAN','CRI','MEX','BRA']}
checks=[
    '18new programme/format dossiers across7operatorgroups;3existingdossiersdeepened,not18independentworld-topcamps. All529priorIDs/order retained,526completepreviousdossiersunchanged. OnlyLeRosey/LesElfes/TASIS and their35cataloguerowscorrected;allother2940oldrows unchanged;alloldUID/datepairs retained.',
    'LeRoseyClassic oneacademy2x75min/day;Tech11–15 max20,science/lifeskills8–12. Matvey9–10 in2027 belowTech11; afternoonRoboticsagehoursunknown. FLLmention not officialqualifier/award. MountainnoformalENlessons;MyFamilythirdweeknoENlessonsandnoparents. EN/FRdailycamp_lifeproved, technicalinstructionnotautomaticallyEN.',
    'Roseysevenexisting2027cohorts retained withoutduplicates;FAQdoubleensuite/agegenderroommate,limitedGVAtransfer/1000depositread. LinkedfinancialcontractSUMMER2026not2027,May1yearnotshifted. MyFamily13200/13500 and Excellence13–16/12–16 discrepancies preserved. Excellence4–19July2027Alps/Svalbard16300age13–16;future,notfamilyICS.',
    'TASIS2027MSP11–13/HSP14–17 day5100/board9200 per3weeks27Jun–17Jul/19Jul–8Aug. Onecoursechoice,STEMdistinctfromStartup/Finance/writing,ownlaptop/DSLRwhereexplicit,requiredFrenchColmar/ArchitectureBaseltripextra. EALENlanguage_lessons proofnottechnicalEN. Day2027excludesweekenddaytripsdespitegenericFAQ7days;attendanceweekdaysnotguessed. Daysinsuranceoptionalextra,nonSwissboardinsured;brothers/friendsnotroommates;deposit1500/May15/exceptionpolicyyearconfirm.',
    'LesElfesexisting19winterweeks/sixsummer/spring retained;winter2026–27mandatoryregistration150/medical120perweek/helmet15,optionalgear140/clothes120/languages6x50min180 or12x50min340replaceski/apresski,GVA190. WinterAprilI2300inPDFagreesexistingdossier,noinvented2200conflict. SeparateDay8–17,350/450+25medical+3helmet=378/478beforeothers,deposit200,60/30/29dayrefunddiffersboard. ES/DE/2hwebvsEN/FR/50minPDFconflict,dayindividualdatesnotguessed.',
    'ChyuluactualKenya13–17,max30,tentedlodge2–4,5500block2027vsFAQ5300;Nairobi-campairtransfer/fullboardincluded,homeflightsexcluded.17–24/23–30Julyoverlapretained;7dayundatedsample not8day2027curriculum. Maasai/conservation/scienceprojectsnotrobotics;EnglishnotinferredfromSwissFAQ;noimmigration/medicalclaimsadopted.',
    'FranceICSownfullpage+PDF:generalEN/FR3–12andBackToSchool100percentEN3–16archive2026;595/695,optional9lunch,465GBPtypo preserved,new2027notguessed. AI730 andYIRA630 G6–12actualgradesunknown;HWCS/YIRAstudentorganizationparticipationcertificate notHarvard/YaleUniversitydegree/admission/leagueaward. FullYIRAPDFstudent-run/timetable/20Aprilvs15Junedeadline read;HPAIRJBCNidentity/3vs5daynotusedasexactParisnewcohort.',
    'ALCNYupcoming19–23/26–30Oct2026generalEN3–9 atLennen/Concordia/Chardin,ASPonlyweek1;7venue-weekvariantsnot4operators,695/720plus9lunch,agegroups3–5/6–7/8–9birthdayunknownOscar5–6. Teens10–16media/artfourvenue-weekvariantswithheadingalternatives/pricemissing,not6independentprogrammes.4teensrows excludedfamilyICS,bothcurrentchildrenbelow10. ASPholiday2024–25primary725/695/secondary610/580/45lunch archived,noinvented2027.',
    'SpainAgoraGranadaSummerFun5–14ENlessons,RoboticsVR9–14unknowninstructionEN,Creative6–14EN+ESbilingual23–26Junno yearorprice. BoardingAndorramenunotGranadanightstay;brochurerequestnotreadPDF. ROBBOprimarywebreadretainsdirect403;owntermsMay2026direct200,48hrefund;archiveages6–8/9–13,curricula/feesread,24Junweekdaytypo/yearnotfixed,languageunconfirmed.',
    '2997events/1666camp-learningrecords;547dossiers/36countries/829dossierURLs;119familycomparisons.22newdatedcataloguerows,butonly7familyICSadditions;2256familyICS/104exhibitionICS. OldcalendarUID/datepairs preserved;35correcteddescriptions/costs onlyauthorisedprofiles;allothercontentstable,SQLite/publicJSON/bridgeidempotenceverified.',
    'Worldwidegeneral+technicalcamps2026–27,allpriorityregions,schools/leagues/results/exhibitions/familyroutesremainactive;0fullyauditedcountries. Noforms/messages/payments/accounts/subscriptions/automations.39directattempts/37HTTP200 plusoneprimarywebsnapshot and10visualPDFreads,not39fullyauditedcampoperators.'
]
audit=dict(asof='2026-10-05',version=88,status='progress',scope='Switzerland season-specific contracts/curriculum/formats;France actualautumn and academicbrand boundaries;Spain language/age/theme;Kenya futureRoseyextension. Worldwideworkactive.',
    new_dossiers=len(fresh),operators_covered=7,new_calendar_rows=len(new),new_family_ics=7,updated_dossiers=changedp,corrected_existing_event_ids=changed,
    programme_dossiers=len(c['profiles']),countries_with_dossiers=c['counts']['countries'],official_dossier_urls=c['counts']['source_urls'],country_dossier_counts=byiso,programme_slugs=[q['slug'] for q in fresh],findings=c['gaps'][-4:],
    calendar=dict(events=len(d['events']),learning_records=learning,family_ics=2256,exhibition_ics=104,managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows']),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
    next_priority='All authorised worldwidegeneral/technical26–27camps and seasonalboarding/day/family,especiallyTaiwan/Singapore/Korea/Japan,USA/Canada/CRI/MEX/LatAm and Europe;realgrades/DOB,EN/ES/RU/secondarylanguageproof,foreignadmission,fees/places. Schools/historicalresults/leagues/exhibitions/familyroutes remainactive.')
def write(stem,v):
    text=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(text)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(text)
write('europe-camp-audit-v88',audit)
write('europe-camp-source-receipts-v88',dict(asof='2026-10-05',version=88,
    scope='39 direct HTML/PDF attempts,37HTTP200;directROBBO403 andoldALCNY404 retained.12PDFdownloaded,read/use boundaries separate. Oneprimarywebsnapshot,10materialPDFvisualreads;not39completeprogrammea audits.',
    sources=receipts,web_primary_reads=[webread],visual_primary_reads=visual,dossier_source_urls_added=added,external_actions=external,
    notes=['SourceHTML/PDF/websnapshots/renders retained outsidepubliccheckout. Onlyparaphrasedfacts,sourceURLs,hashes/errors published;nosourcephotos/fullPDFscopied.',
        'DirectHTTPstatusandwebtoolreadaredifferentreceipts. Campusmaps/websiteprivacytermsnotacceptedascurriculum/campcontract.',
        'Announceddateandprice do not establish places,admission,finalinvoice,worldranking or Englishtechnicalinstruction. Archivedcohorts/contractyears not shifted. Worldwidegoalactive.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=88:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',evidence='Version87nativepublication succeeded:commit2d76829dc5390385a77c0192084e000c482b9082;deployment appgdep_6ac40d98a7048191a11c2a0d1f8388d0.24newdossiers/9datedrows/9familyICS.Worldwidegoalactive.')
plan['latest_validation']=dict(version=88,asof='2026-10-05',status='Independent source,preservation,correction/calendar verification;nativepublicationreceipt separate',events=len(d['events']),camp_learning_records=learning,programme_dossiers=len(c['profiles']),countries_with_dossiers=c['counts']['countries'],official_dossier_urls=c['counts']['source_urls'],family_ical=2256,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=byiso)
plan['europe_camp_programme_audit_v88']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=len(c['profiles']),countries=c['counts']['countries'],swiss=c['counts']['swiss'],generated_calendar_entries=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'])
for req in plan['requirements']:
    if req['id'] in ['camps','family_top_picks','camp_switzerland_full','camp_calendar_2026_2027','camp_full_pricing']:
        req['evidence']='v88:547 programme/venue/format dossiers in36countries;18new and3deepened,22newdatedrows/7familyICS,829officialdossierURLs. Swisscurriculum/age/seasoncontracts andmandatoryfees,FranceactualOctober/ENandstudentorganizationboundaries,Spainundated/archivalthemes/languages,Kenyaactualroute verified with unresolvedconflicts retained. Worldwide26–27scope/allpriorityregions active;0fullyauditedcountries.'
plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05';write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=87','?v=88').replace('data-ui-version="87"','data-ui-version="88"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_europe_camp_audit_v88.json" download>Швейцария / Франция / Испания: программы и условия ↓</a> · <a href="downloads/STEM_europe_camp_source_receipts_v88.json" download>Источники нового прохода ↓</a> · '
anchor='<a href="downloads/STEM_americas_camp_audit_v87.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=547,new_dossiers=18,updated_dossiers=3,new_calendar_rows=22,new_family_ics=7,source_urls=829,goal='active')))
