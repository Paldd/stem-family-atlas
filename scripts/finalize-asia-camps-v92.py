"""Record the bounded Asia/Australia pass; preserve the unfinished global goal."""
import hashlib,json,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v92'
BASE='898c56aeebb81820bd3e2dda84962dff563c5fd7'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old={e['id']:e for e in b['events']};op={p['slug']:p for p in b['camp_programmes']['profiles']}
fresh=[p for p in c['profiles'] if p['slug'] not in op]
new=[e for e in d['events'] if e['id'] not in old]
assert len(fresh)==10 and len(new)==22 and all(e==old[e['id']] for e in d['events'] if e['id'] in old)
assert c['counts']['dossiers']==611 and c['counts']['source_urls']==941
receipts=[q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(receipts)==49 and sum(q.get('status')==200 for q in receipts)==46
scopes={
 'british-council-kinder':'Direct HTTP timed out. Not a successful page fetch; official web extraction and rendered expanded timetable recorded separately.',
 'british-council-kinder-retry':'Second direct HTTP timeout. Not counted as successful; no separate application or submission.',
 'computhink-lego-draft':'Guessed draft path returned404; not a future programme or an admitted source. Canonical own page fetched separately.',
 'computhink-lego-canonical':'Canonical own LEGO programme retained unchanged: four previously recorded Nov/Dec2026 cohorts,7–12,SGD367,9hours,pairs share one kit. EN teaching unconfirmed. Not a new operator/dossier.',
 'campasia-book':'Own current booking/programme context read. Earlier confirmed October cohort retained; not evidence of new2027 date or available place.',
 'campasia-faq':'Relevant meals/support/age/booking clauses read; not a complete operator or country audit.',
 'campasia-terms':'Relevant cancellation/payment clauses read; not a whole legal audit or acceptance of conditions.',
 'camp-taiwan-family':'Own family schedule and programme read. October prose16–18 versus table17–18 unresolved; private groups versus special individual-family events distinct. Summer English not transferred to family camp.',
 'camp-taiwan-summer':'Own2027 calendar with six dated cohorts all Not yet open. CurrentYouth24k/group23k/Teen26k price not individually year-stamped: final2027 invoice unknown. No9–14August invented cohort.',
 'camp-taiwan-faq':'Relevant own summer age/language/meals/bus clauses read; not foreign admission approval or final2027 contract.',
 'camp-taiwan-handbook':'Own summer parent handbook bus/meals/communication and foreigncamper handling read; separate linkednotice inspected. Not confirmed2027 child admission.',
 'camp-taiwan-notice-viewer':'Own-linked Drive viewer only; actual public PDF download followed separately, not counted as PDF body itself.',
 'camp-taiwan-notice-pdf':'Actual undated CAMP TAIWAN NOTICE. English refund/payment/guardian sections pages3–4 and Chinese precedence/transport table page1 read and visually checked. English has printed official precedence; transport refund differences retained. Page2 render retained but not counted as a visual reading. Not confirmed2027 contract.',
 'ici-korea':'Own Winter2026–27 programme read: middle/high/university categories, not a6/9 camp. English/Korean usage not proof of all-English teaching; no new dossier admitted.',
 'imagine-junior':'Own2027 Junior/Senior/family programme, English policy,30hoursExplore and schoolingweek condition read.30hours not30hoursEnglish/robotics.',
 'imagine-gc-flyer':'Both pages visually read: actualGoldCoast2027,11Jan–12Feb,6–11/12–16,250enrol+800tuition+150materials/week.26Jan no lessons;Saturday optional. Schoolingweek condition not a guaranteedschool internship.',
 'imagine-bne-flyer':'Both pages visually read: actualBrisbane2027,11Jan–12Feb,ages/fees/sample timetable. Campus distinct fromGoldCoast, sameoperator. Not a housing2027 quotation.',
 'imagine-fee-2026':'Despite local discovery filename, actualdocument International2025 fee list. Year/header scope checked; not current2027 camp or housing price.',
 'imagine-homestay-gc':'Despite local discovery filename, actualdocument International2026 fee list, notGoldCoasthomestay brochure. Not used as2027 camp/housing quotation.',
 'imagine-homestay-bne':'Despite local discovery filename, actualGoldCoastHomestay2026 one-page fee sheet visually read. Familyplacement660+1310/week andtransport100/week; notBrisbane or2027 housing price.',
 'imagine-homestay-bne-actual':'ActualBrisbaneHomestay2026 one-page fee sheet visually read. Familyplacement660+1310/week,schooltransport120/week. Fullservicesolo8–17 notOscar6–7; not a2027quote.',
 'imagine-refund':'Generalrefundpolicy v4.9 relevantpage2 visually read and tuition/homestay cancellation sections read. Not all policy pages/clauses audited; applicability to1–5weekcamp and materials refund unknown.',
 'imagine-fees':'Ownfeeindex observed old2025/2026 general and2026homestay files separately; new2027 campflyers used for2027 tuition only.',
 'imagine-policies':'Ownpolicyindex and observed relevantrefund link followed; not alllinkedpolicies reviewed.',
 'gungho-register-steam':'Actualreadonlybookingcard dates/620early660regular/age gate read and renderedstep1 inspected. Generic hiddenRestricted/Waitlist templates not availabilityproof. NoContinue/forminput/payment.',
 'gungho-register-treasure':'Actualreadonlycard renderedstep1: selectedtitle5–8 versusbody5–12 andDOB21Nov2013–20Nov2021. Conflict preserved, not solved bywideDOB gate. No formsubmitted.',
 'gungho-register-adventure':'Actualowncard23–27Nov2026,640early690regular,DOB23Nov2011–22Nov2017. ExactDOB needed forMatvey. Prices do not prove places.',
 'gungho-register-beach':'Own12–16Oct2026card600earlyexpired27Sep/660regular. Expiredearlydiscount not a registrationdeadline orcurrentprice.',
 'gungho-register-wilderness':'Own30Nov–4Dec2026card620earlyuntil8Nov/660regular. Earlydiscountdeadline not imported asregistrationdeadline.',
 'gungho-register-christmas':'Own14–18Dec2026card620earlyuntil22Nov/660regular. Selectedheading5–10 versusbody5–12/widebirthrange conflict retained.',
 'gungho-register-xtra':'Own21–23Dec2026three-daycard408earlyuntil29Nov/430regular; actualregularregistrationends18Dec23:55local. This is the single new registrationdeadlineICS.',
 'gungho-camps':'Ownprogramme explicitlyresidentsandvisitors, agegroups/activities read. Englishpage and formUI languages not EN teaching proof.',
 'gungho-faq':'Relevant ownfoodpaidadd-on/siblinggroupsDOB≤12months/ratio/discount/cancellation clauses read. No automaticgroupmates forbrothers2017/2020 or unknownsiblingsdiscountsum.',
 'gungho-terms':'Relevantownpayment/cancel/photo/livestream clauses read. Parentcancel usuallynonrefund; exceptionsdocumented; COVIDcredit12months notcashrefund. Termsnotaccepted.',
 'gungho-safety':'Relevantownkayaking10+/swimming/parenthandling read. Height/swimming eligibilitynotapproved; safetyclaims notindependentlycertified.',
 'ugaku-own-winter-prices':'Only ownoperator NasuWinter159800JPYtaxincluded+firstcontract30000 used. Otheroperator comparison/rank/prices inarticle not adopted asprimaryproof.',
 'ugaku-nasu':'OwnWinter26–30Dec2026 andspring28Mar–3Apr2027. WinterTochigi versus springNationalNasuKashiCentreFukushima; spring199800+30000contract. STEAM/teamprojects read, no gradeinferred frombirthyear.',
 'ugaku-spring-nasu':'SecondsameURL observation ofupdatedNasu programme. Duplicate URL not anotheroperator, independentprogramme orsecondsourceURL.',
 'ugaku-okinawa':'OwnWinterChatan139800 versusSpringOnna199800, firstcontract30000. Springbusiness/OISTcampustour notinternship; capacity10top versus20detailedconflict andintermediateEnglishqualification retained.',
 'ugaku-cebu':'OwnWinter139800/spring199800+firstcontract30000; spring14hoursone-to-one nottransferred towinter. Returnairporttransferincluded. Roomnamed butcompleteinclusion needscheck. Foreignunder15entryrules not verified oradvice.',
 'ugaku-winter-release':'OwnWinter2026officialrelease precise dates/venues; notNasupriceproof orspringcontract.',
 'ugaku-minor':'Ownminorpolicy read relevantguardian/responsibility clauses; exactforeigngradeequivalence/ENadmin/medical support unknown. Noconsentaccepted.',
 'ugaku-cancel':'Own90/60/45day50/70/100percentservice+relatedcosts andfirst5days>90daycancel clauses read; exact90dayoverlap unresolved. Not automaticallyoverride a specificcampcontract.',
 'ugaku-guarantee':'Ownrefundguarantee requires≥4weeks andwithin3days plusattendance. Not automaticrefund for5/7daycamps.',
 'ugaku-safety':'Ownparentsafetycontext read; not independentlyauditedcertification or overseaschildentryapproval.',
 'ugaku-tokushoho':'Ownseller/payment/cancellationidentification read relevantsections; notfulllegal/visa audit.',
}
for q in receipts:
 q['retrieval_method']='direct_http'
 q['content_scope']=scopes.get(q['key'],'Relevant ownprogramme/operatorcontext read; dates/age/language/price/foreignintake/availability not inferred. Not a completeoperator/country audit.')
 if q.get('status')==200:
  f=next(f for f in [PRIMARY/(q['key']+'.pdf'),PRIMARY/(q['key']+'.html')] if f.exists())
  assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
  q.update(raw_filename=f.name,body_snapshot_retained=True)
web=PRIMARY/'british-council-web.json'
additional=[dict(key='british-council-official-web-extraction',url='https://www.britishcouncil.kr/en/kinder-plus-all-day-programme-aged-6%E2%80%937',retrieval_method='web_extract',raw_filename=web.name,sha256=hashlib.sha256(web.read_bytes()).hexdigest(),bytes=web.stat().st_size,body_snapshot_retained=False,content_scope='Primary official page webextraction stored as toolresponse, not HTTPHTMLbody. Relevant WinterCamp11–22Jan2027 and2020/2021intake/monthlycoursefees read. Renderedcalendar expanded separately; prioritycurrentstudents. Unknowncampfee/foreignexternalintake/full-daylanguage.')]
oldurls={s['url'] for p in op.values() for s in p['sources']}
added=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls)
assert len(added)==23
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False)
byiso={s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','MYS','PHL','AUS','USA','CAN','CRI','MEX','BRA','CHL']}
checks=[
 '10newdossiers across4newoperatorgroups: GungHo4/BritishCouncilKorea1/Imagine2/U-GAKU3.1priorCampTaiwandossierdeepened;all601priorIDs/order/all600otherprofiles/all3075prioreventsunchanged.22newfutureprogrammerows plus1actualregistrationdeadline produce23newfamilyICS; exhibition104unchanged.',
 'CampTaiwan own2027schedule has6cohorts allNotyetopen. Youth24k/group23kTWD/Teen26k currentfeeon2027page notfinalinvoice. No9–14Auginvented. Undatednotice: registration1000+mandatorybus1000 alreadypartsoftotal;internationalcard5percentnonrefundable;guardianmustremainTaiwan. Englishrefundpriority andChinese transportdifferences retained, notconfirmed2027contract.',
 'GungHoownvisitorsaccepted,day09–16.7cohortdates/actual620660/640690/408430;earlyBeach600expired. Treasureheader5–8/body5–12,Christmas5–10/body5–12 andDOBgatespreserved. ExactMatveyDOBAdventure≤22Nov2017. ENteachingunknown despiteEnglishsite/translatedform. Lunchpaidunknown+card3percent,brotherssamegroupnotpromised. GenericHTMLwaitlist/restrictedtemplates notvisibleavailabilityproof.',
 'BritishCouncilKorea Winter11–22Jan2027 andcourseintake2020/2021,currentstudentspriority. Oscarconditional/Matveylater. Monthly1516200/1020300KRW notcampfee; generalIEYC/phonics/dailyhours notimportedascampsyllabus. TwoHTTPtimeouts keptaserrors, officialwebextract andrenderedexpandedtimetable usedseparately. ENrolelanguage_lessons notfull-dayteaching.',
 'ImagineGoldCoast/Brisbane own2027flyers6–11/12–16/11Jan–12Feb1–5weeks. AUD250+800/week+150/week=1200/2150/5000one/two/fiveweeks. 50percentsiblingsregistrationonly;parentsnoenrolmentfee notfreecourse. Homestay/transportactual2026 only;wrongdiscoveryfilenamesdocumented. No2026housing+2027tuition presentedascurrentinvoice. Solo8–17excludesOscar6–7. OptionalSaturday/26Janholiday/30hExplore notmandatoryEnglish/robotics; ENrolelanguage_lessons.',
 'U-GAKUWinter26–30Dec2026/Spring28Mar–3Apr2027. NasuWinter159800taxincl/Spring199800, Okinawa/CebuWinter139800/Spring199800;firstcontract30000 gives189800/169800/229800. Seasonalplacesdifferent;NasuSpringFukushima notWinterTochigi;OkinawaSpringOnna notChatan. Cebu14hone-to-oneonlySpring,airportreturnincluded;OISTtour notinternship. Gradeequivalence/foreignintake/ENadmin unknown. Cancellation90/60/45tiers notsimplified;≥4weekrefundguarantee not5/7daypromise.',
 '49directattempts/46HTTP200/3errors,1additionalprimarywebextraction withmethodexplicit.8actualPDFs relevantsections checked/10visualpagechecks/11rendersretained. RawHTML/PDF/renders outsidecheckout;publicexports containparaphrases/URLs/hashes/errors. Twoactualreadonlycards andexpandedofficialBCtimetablerendered; noforminputorContinue.',
 '611dossiers/37countries/941distinctdossierURLs,137familycomparisons;3097events/1766camp-learningrows/2347familyICS/104exhibitionICS.1303manageddated/69legacyreuse/39seasonwindows.249worldcountries/82withrecords/0fullyaudited. Expandedworldwidegoal active; competitions/leagues/exhibitions/schools/history/familyroutes preserved.'
]
audit=dict(asof='2026-10-05',version=92,status='progress',scope='Deeper Taiwan/Singapore/Korea/Japan/Philippines seasonal programmes and family-oriented Australia2027 option. Prior Europe/Americas/global work retained; worldwide goal unfinished.',new_dossiers=10,new_operator_groups=4,operator_groups_including_existing_deepening=5,new_calendar_rows=22,new_family_ics=23,new_registration_deadline_ics=1,updated_dossiers=['camp-taiwan'],corrected_existing_event_ids=[],programme_dossiers=611,countries_with_dossiers=37,official_dossier_urls=941,country_dossier_counts=byiso,programme_slugs=[p['slug'] for p in fresh],findings=c['gaps'][-5:],calendar=dict(events=3097,learning_records=1766,family_ics=2347,exhibition_ics=104,managed_dated_rows=1303,reused_legacy_events=69,season_windows=39),primary_retrievals=dict(direct_attempts=49,http200=46,errors=3,additional_web_extractions=1,actual_pdfs=8,visual_page_checks=10,retained_page_renders=11),fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,next_priority='Continue deep programme/contract audit in Switzerland/France/Spain/Europe and USA/Canada/CostaRica/Mexico/LatinAmerica; continue Taiwan/Singapore/Korea/Japan/Asia/allworld2026–27 general/technical/boarding/day/family camps. ExactDOB/actualgrade/foreignintake/teachinglanguage/availableplace/currentall-ininvoice/seasoncontract, schools/results/history, competitions/leagues/exhibitions and familyroutes remain partofgoal.')
def write(stem,value):
 t=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(t)
 (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(t)
write('asia-camp-audit-v92',audit)
write('asia-camp-source-receipts-v92',dict(asof='2026-10-05',version=92,scope='49directHTTPattempts/46HTTP200/3errors; separateprimarywebextraction,8actualPDFs relevantsections and10visualpagechecks. Noalloperator/countrycompletion claim.',sources=receipts,additional_retrieval_methods=additional,dossier_source_urls_added=added,external_actions=external,notes=['RawHTML/PDF/renders retained outsidecheckout. Publicexports onlyparaphrases/URLs/hashes/errors; nooriginalcampphotographs/PDFbundles.','Sourceyear/currentprice/registrationopen/teachinglanguage/foreignadmission/actualplace distinguished. Hiddenformtemplates notwaitlistproof; schoolgrades notinferred frombirthyears.','ActualPDFtitles/scopes govern evidence, not discoveryfilename. Retainedpage2Taiwanrender notcounted asvisuallyread. Worldwidecoverage remainsactive.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=92:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',evidence='v91nativepublication succeeded;commit898c56aeebb81820bd3e2dda84962dff563c5fd7;deploymentappgdep_6ac42b1a975481918bf23b6838177e84. Worldwide expanded scope retained.')
plan['latest_validation']=dict(version=92,asof='2026-10-05',status='Independent primary/preservation/calendar verification; nativepublication receipt separate',events=3097,camp_learning_records=1766,programme_dossiers=611,countries_with_dossiers=37,official_dossier_urls=941,family_ical=2347,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=byiso)
plan['asia_camp_programme_audit_v92']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=611,countries=37,swiss=85,generated_calendar_entries=1303,reused_legacy_events=69)
for q in plan['requirements']:
 if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:q['evidence']='v92:611programme/venue/formatdossiers37countries;10new+1deepened,22newfutureprogrammerows+1deadline/23familyICS,941dossierURLs. Ownage/language/fees/seasoncontracts/visiblePDF/programmeavailability; allcountry/worldwidecompletion notachieved.'
entry=dict(version=92,asof='2026-10-05',status='progress',scope=audit['scope'],new_dossiers=10,deepened_dossiers=1,new_calendar_rows=22,new_family_ics=23,official_primary_sources=23,not_complete_worldwide=True)
plan.setdefault('research_passes',[])[:]=[q for q in plan.get('research_passes',[]) if q.get('version')!=92]+[entry]
plan['next_research']=[audit['next_priority']];plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05';write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=91','?v=92').replace('data-ui-version="91"','data-ui-version="92"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_asia_camp_audit_v92.json" download>Азия и Австралия: новые сезоны и семейные условия ↓</a> · <a href="downloads/STEM_asia_camp_source_receipts_v92.json" download>Источники и границы проверки ↓</a> · '
anchor='<a href="downloads/STEM_europe_camp_audit_v91.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=611,new_dossiers=10,deepened_dossiers=1,new_calendar_rows=22,new_family_ics=23,source_urls=941,goal='active')))
