"""Publish selected source receipts; raw pages, PDFs and images remain private."""
import collections,hashlib,json,subprocess
from camp_asia_v125 import ROOT,BASE,CHECKED,NEW,NEW_IDS
P=ROOT.parent/'stem-family-atlas-work/camp-asia-primary-v125'
d=json.loads((ROOT/'data/catalog.json').read_text());b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
cp=d['camp_programmes'];old={x['id']:x for x in b['events']};now={x['id']:x for x in d['events']}
assert len(now)==3695 and len(cp['profiles'])==980 and cp['profiles'][:966]==b['camp_programmes']['profiles']
assert [x['slug'] for x in cp['profiles'][966:]]==NEW and all(now[k]==v for k,v in old.items())
assert d['camp_planning']['offers'][:46]==b['camp_planning']['offers'] and len(d['camp_planning']['offers'])==48
sources=[]
for f in sorted(P.glob('receipt-*.json')):
 for x in json.loads(f.read_text()):
  q=dict(x,checked=CHECKED,retrieval_method='direct_public_http',content_scope='Selected syllabus, language, age/grade, dates, pricing, accommodation and contract clauses; not entire sites or countries.')
  if q.get('status')==200:
   name=q['key']+('.pdf' if (P/(q['key']+'.pdf')).exists() else '.html');raw=(P/name).read_bytes()
   assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
   q.update(raw_filename=name,body_snapshot_retained=True,content_status='selected_pdf_clauses' if name.endswith('.pdf') else 'selected_html_clauses_or_discovery')
  else:
   error=q.get('error','')
   resolution=('Non-ASCII URL was not dispatched; encoded URL retried, application PDF succeeded, Canadian406 remained.' if 'ascii' in error else
               'Guessed route not found; replaced by own linked neuroscience/root-English route. No operator-unavailability conclusion.' if '404' in error else
               'Direct access403/406; KidsSpace cached primary FAQ/terms separately read, Canadian new /enrichment/ still unreadable. No login, consent or form action.')
   q.update(body_snapshot_retained=False,content_status='retrieval_error_not_content_evidence',resolution=resolution)
  sources.append(q)
assert len(sources)==30 and sum(q.get('status')==200 for q in sources)==18
reader=P/'web-reader-kids-clauses.json';raw=reader.read_bytes()
sources.append(dict(key='kids-faq-and-terms-reader',checked=CHECKED,retrieval_method='primary_web_reader_cached_content',
 urls=['https://www.kidsspace.sg/frequently-asked-question/','https://www.kidsspace.sg/terms-of-use/'],raw_filename=reader.name,
 bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),body_snapshot_retained=True,content_status='selected_cached_primary_clauses',
 content_scope='Camp4–8/nonmembership and conflicting cancellation terms only. Reader crawl3weeks/1month, direct403; not live contractual confirmation. Canadian redirect error in same capture is not programme evidence.'))
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
blocks=collections.Counter(x['block'] for x in d['events'])
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT');expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert (family,expo)==(2897,104)
checks=[
 'STARK Tinker grade1–6, five consecutive daysJan30–Feb3 including both weekend days;12500元 inclmeal/materials/takehome. Specific09–16 versus catalogue09–17 retained. Real mechanical/electrical device disassembly, not guaranteed programmable-robot course; concept images and syllabus substitutions disclosed. EN navigation not an English instructor. Weekday-only free shuttle not extended to weekend.',
 'STARK StudyTools specificapproxG3–6 versus winter age-selectionG4–6;9900元,09–17,Jan30–Feb3 includingweekend.68page workbook, methods and parental report; not robotics/clinical efficacy. SimultaneousTinker not a sequential two-camp itinerary.',
 'STARK science inquiry G4–G12 AND regularstudent/previousResearchTalent/VSTC.2–3 same-schoolstage students, crossschool permitted.42classhours sevenintensive daysJan21–22/25–29;22000/25000/30000元 coverswholeDecember–Juneseason,10k equipmentdeposit separate/unituncertain. No storedvalue discount; transferonly/noabsence refund. OldApril/Juneseasonrhythm not2027contestdeadline; awards notindependentlyverified.',
 'KTI/GMI own linked operatorcamp physicallyMalaysia with Taiwanese organizers.10–15/basicEnglish,technicalENexplicit; Jan21–29,courseJan22–26 includesweekend.99000元packageairfare/hotel/meals/localtransport/materials; currencyanddeparturepointnotassumedCostaRica. Hotel/two perroom/teacherassist≥1:4;industrialCNC/KUKAtouronly. Severalownnotices報名額滿: admissionclosed, notopen application or guaranteedwaitlist. Matveyonlyif10already; Oscarbelow10. No closedcamp familyICSexport.',
 'HWA13page ownwinter2027brochure/4page refund/3pagegenericform readselectedclauses. PYP6–12ANDG1–6, middle13–17ANDG7–8,upperG9–11DP-inspiredseparatefromschoolIBDiploma. ExplicitEnglishANDChinese timetable, noEnglish-only sciencepromise.1490/2850,1590/3100,1890/3680SGDweek/twoweeks. PDF packageinclusions versus siteearlydiscountexclusionsneedcomponentquote;20%first50deadlineOct15notappliedwholeprice. Refund≥30daysminus200,48hgraceforerror,nonrefundableGST/registration,credits12monthfamilyonly—notacademiccredit. Optionalgenericlodgingfielddoesnotprovesupervisedboarding.',
 'HWA sixagreedwinterintervals for3curricula=18calendarrows. Feb1–4 fourdays/Feb4halfday,shortweekfeeunknown. SiteFeb15–16 versusPDFFeb15–19 conflict excludedcalendar.3selectedbrochurepages visuallychecked:EN/ZHschedule,dateconflict,fee/inclusions; primarypricevariables notfakezero.',
 'KidsSpace own8page2026PDF detailedp7–8: fivefuturethemesOct12–16/Oct19–23/Nov23–27/Nov30–Dec4/Dec7–11. OverviewDec6–10CreativeGlobe conflictsdetailedLitLinesDec7–11; ambiguousoverviewnotadded. LittleElfalreadySRT×KidsSpacenotduplicated. OwncachedFAQ4–8/nonmembers,noENteacherstatement.150touristdaypass/45guest/tuitionnotcampprice. MedicalrefundFAQversuscredit/50%adminTerms disclosed;direct403andreaderageexplicit,notlivecontractconfirmation.',
 'ULC junior5–12+,3–10students/3agegroups/leveltest,Englishlanguagelearningexplicit; nojuniorpricefromteen580/980summer2026. Teen13–18winterDatesTBC notexactshift/currentkidsaccess. Osaka/SiliconValleyJuly2026outbound notnew2027programme. CanadianownoldURLredirect→/enrichment/,direct406/readerfailure: oldsearchsnippetnotnewverifiedcamp.',
 'SJAJeju ownGrade3/4 schoolhandbooks2025–26 VEXGOMars/VEXcodeGO/BumperSwitch/teams;Grade3schoolovernightcamping andGrade4multidaytripsnotpublicwinter2027holidayadmission. SelectedGrade3roboticsp8visuallychecked. FreshHarrowAppi ownschool/winterpage rechecks existingdossier, noELTduplicate, no2022fees/currentregularschoolageconflation.',
 'All966 prior dossier/3667 event/46 budget objects preserved.14newcurricular dossiers across5programmeoperators,28datedcalendarrows,15additionalfamilyICS dates and2partialHWA tuitionbudgets.0countriesfullyaudited, worldwide competitions/exhibitions/camps/schools5–10year results/routes and allprioritycountries preserved;goalactive.'
]
audit=dict(version=125,asof=CHECKED,status='progress',scope='Selected Asian winter2026–27 curricula, junior general themes and school-versus-camp gates;14dossiers across5operators, not a complete world ranking or camp census.',
 events=len(d['events']),competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],camp_learning_records=blocks['Лагеря'],programme_dossiers=len(cp['profiles']),countries_with_dossiers=39,
 official_dossier_urls=len({s['url'] for x in cp['profiles'] for s in x['sources']}),editorial_scenarios=len(cp['shortlist']),coverage_gaps=len(cp['gaps']),league_profiles=len(d['league_guide']['profiles']),
 budget_scenarios=48,budget_providers=24,budget_programme_dossiers=37,new_budget_scenarios=2,new_budget_ids=NEW_IDS,new_dossiers=14,new_dossier_slugs=NEW,
 new_programme_operators=['STARKLab','KTI/GMI','HWAInternationalSchool','KidsSpace','UnitedLanguageCentre'],updated_dossier_slugs=[],new_event_ids=sorted(now.keys()-old.keys()),updated_event_ids=[],
 unchanged_dossier_objects=966,unchanged_event_objects=3667,unchanged_prior_budget_objects=46,source_retrieval_attempts=30,direct_successful_bodies=18,retrieval_errors=12,primary_reader_captures=1,
 pdf_download_files=6,pdf_text_pages_extracted=48,new_visual_pdf_checks=6,family_ical=family,exhibition_ical=expo,goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,checks=checks,verification={})
for name in ['independent-check.json','functional-check.json']:
 f=P/name
 if f.exists():
  q=json.loads(f.read_text());assert q['status']=='passed' and q['version']==125;audit['verification'][name.removesuffix('.json')]=q
def write(stem,v):
 text=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(text);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(text)
write('asia-camps-audit-v125',audit)
write('asia-camps-source-receipts-v125',dict(version=125,asof=CHECKED,scope=audit['scope'],sources=sources,pdf_download_files=6,pdf_text_pages_extracted=48,
 visual_pdf_pages_checked=[dict(filename='hwa-brochure.pdf',page=i) for i in [7,11,12]]+[dict(filename='kids-calendar.pdf',page=i) for i in [7,8]]+[dict(filename='sja-grade3.pdf',page=8)],
 external_actions=external,primary_reader_limits='Selected clauses/schedules;48pages text extracted does not mean48pages visuallyread. Sixselectedpages visuallychecked. Raw snapshots/cachedreader/images private outside repository.30directattempts include guessed404,URLencoding errors,403/406; these are not evidence of absent camps. No external forms/login/checkout/consent.'))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=125:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native124 succeeded2026-10-06T13:26:33.305071Z; deployment appgdep_6ac4f6e72d208191877156dffb45fa1f; commit '+BASE+'. Worldwide goal active.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','budget_providers','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected Asiawinter/junior curricula, source conflicts and partialtuition budgets checked; nativepublication separate.'
plan['asia_camp_programme_audit_v125']=audit
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for x in plan['requirements']:
 if x['id']=='unified_database':x['evidence']='v125:3695events/980programme dossiers/39countries/1511primary dossierURLs;14newAsia curricula/28dated rows/2partialHWA familybudgets. All3667events/966dossiers/46budgets preserved;completeportableSQLite/JSON.'
 elif x['id'] in ['camps','family_top_picks','camp_asia_deep']:x['evidence']='v125:980dossiers/233editorialscenarios;STARKgradegates/realmechanics,closedEnglishGMI10–15,HWAENandZHcurricula,KidSpace4–8futuregeneralthemes,ULCjunior/teen distinctions. KoreaSJAregularVEXGOcurriculumnotopenholidaycamp;JapanHarrowrecheckedwithoutduplicate. AllpriorEurope/Asia/Americas/general/thematic/day/boarding/familyENESRUscopepreserved;notcompleteworldwide.'
 elif x['id']=='camp_full_pricing':x['evidence']='v125:48partialbudgets/24brands/37dossiers;46oldoffersunchanged. HWA1490/2850perchild→2980/5700familypublishedbase,packagecomponents/shortweekfeeunknown;20%notappliedwholeprice. STARKseasonfeeandrefundableequipmentdepositdifferent;KidsSpaceclubpassnotcampfee. NofakezeroorclosedGMIfamilyquote.'
 elif x['id']=='camp_calendar_2026_2027':x['evidence']='v125:28datedrows/15familyICSadditions;weekendskeptSTARK/GMI,sixagreedHWAintervals×3tracks,shortFeb4halfdaylabelled. ConflictingFeb15andKidsSpaceoverviewexcluded,ULCTBCnotdated. ClosedGMIandolderHWAtracksnotfamilyICS.2897familyICS/104exhibition,alloldUID/contentpreserved.'
plan['research_passes']=[x for x in plan.get('research_passes',[]) if x.get('version')!=125]+[dict(version=125,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=14,updated_dossiers=0,new_calendar_rows=28,new_budget_scenarios=2,official_primary_retrieval_attempts=30,pdf_download_files=6,not_complete_worldwide=True)]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=124','?v=125').replace('data-ui-version="124"','data-ui-version="125"');anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_asia_camps_audit_v125.json" download>Азия · зима, младшие группы и условия</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text();anchor='<a href="downloads/STEM_europe_camps_audit_v124.json"';link='<a href="downloads/STEM_asia_camps_audit_v125.json" download>Азия: зимние программы, классы и цены ↓</a> · <a href="downloads/STEM_asia_camps_source_receipts_v125.json" download>Источники и расхождения ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps({k:audit[k] for k in ['version','events','programme_dossiers','new_dossiers','budget_scenarios','family_ical','worldwide_complete']}))
