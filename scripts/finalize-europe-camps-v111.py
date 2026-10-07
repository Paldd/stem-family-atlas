"""Bounded primary-programme research receipt; worldwide objective stays active."""
import collections,hashlib,json,subprocess
from camp_europe_v111 import ROOT,BASE,CHECKED,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v111'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
cp=d['camp_programmes'];old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
assert old.keys()<=now.keys() and all(now[k]==v for k,v in old.items())
newids=sorted(now.keys()-old.keys());assert len(newids)==43 and len(cp['profiles'])==827
assert d['camp_planning']['offers'][:14]==b['camp_planning']['offers'] and len(d['camp_planning']['offers'])==17
sources=[]
for n in range(1,8):
 for item in json.loads((P/f'receipt-{n}.json').read_text()):
  q=dict(item,checked=CHECKED,retrieval_method='direct_http',content_scope='Selected programme/policy clauses or comparison with an existing dossier; not a whole-site or country audit.')
  if q.get('status')==200:
   ext='pdf' if q['key'] in ['eyyc-brochure','techlabs-flight-faq'] else 'html'
   f=P/(q['key']+'.'+ext);raw=f.read_bytes()
   assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
   q.update(raw_filename=f.name,body_snapshot_retained=True,content_status='html_shell_no_readable_programme_body' if q['key']=='aal-courses' else 'selected_visual_pdf_pages' if ext=='pdf' else 'selected_html_clauses')
  else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body')
  sources.append(q)
assert len(sources)==32 and sum(q.get('status')==200 for q in sources)==25
posters=json.loads((P/'posters-receipt.json').read_text())
for q in posters:
 raw=(P/q['filename']).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
f=P/'web-reader-fallback.json';raw=f.read_bytes()
reader=dict(retrieval_method='public_primary_web_reader',raw_filename=f.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),urls=['https://techlabkids.com/campamentos/dias-sin-cole/','https://techlabkids.com/campamentos/casal-de-navidad/'],content_scope='Retained selected primary-reader responses after direct DNS/certificate failures. Not raw HTML, complete whole-site audit or proof of accessible new Easter2027 intake.')
visual=json.loads((P/'visual-review.json').read_text())
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
sm=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text());jm=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT');expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert family==2643 and expo==104
blocks=collections.Counter(e['block'] for e in d['events']);countries=dict(collections.Counter(p['iso'] for p in cp['profiles']))
checks=[
 '12 new programme/age/format dossiers across5 operators in5 venue countries: Planète Sciences3/HelenDoronParis15 three/TechLabs three/TechLabKids one/EnglishYesYouCan two. Not12 independent providers or an objective world ranking.',
 'All815 prior dossier objects and3376 prior event objects/IDs unchanged.43 new datedcamp rows;3419 cards,1153 competitions/189 exhibitions/2077 camp-learning.827 dossiers/39 countries/1272 dossierURLs/193 editorial scenarios/203 gaps.',
 'Planète Sciences:3 own posters visually inspected. Robot8+/220EUR/19–23Oct2026 ThymioScratch;Science7–12/190 each/19–23 and26–30October2026,nature/science/English named but language share not established;Explor250/26–30October2026,11–13overview vs11+poster. Format/nightcare/teacher/insurance/food/refund unknown. New explicit format-unknown filter prevents false boarding/day classification.',
 'HelenDoron Paris15:8 junior sessionsOct2026/FebAprJulAug2027;half3–10PS–CM2/320EUR/09:30–12:30,full5+GS/690/09:30–17 withbadminton,mealboxown. English morning/instructors directly confirmed. Teen10–18bodyvs11–18fee345,10sessions;June21–25/28Jun–2Jul onlyteens. National2026 summer robotics activity not assumed inParis15curriculum.',
 'TechLabs Basel:LEGO overview6–8 vsbooking6–9,450–924CHF/mode breakdown unknown,currentOct5–9 fullybooked/waitlist. Controllers8–13game/micro:bit/HaloCode/ML/3D curriculum but no dates/fee. ENwebsite/bookinglanguages not teacher guarantee.',
 'TechLabs Flight:9–16,TrogenPestalozzi boarding/four6nightJuly2027blocks3–9/10–16/17–23/24–30.210CHF is approved financial-aidnet after90%subsidy,not standardquote;regularfee unknown. StaffEN/DE/FR not confirmed scheduledENstream. FAQ2027link leads to visible2026PDF with old4/11/18/25Julyarrivals: dates not imported.',
 'TechLabKids Barcelona6–14:four individualdaysDec7,2026/Feb8,May14,May18,2027 at60EUR09–16;foodown. ES/ENteacher andforeignintake unknown. Christmas still2025–26,not falsely rolled. Own cancellation-minimum clause refund confirmed, fullcontract later inaccessible.',
 'EnglishYesYouCan12–17:StirlingGBRvenue two14day2027sessions,2299EUR/599depositinside;visible2027PDF15Englishhours/week/privateownroom/3meals/laundry.2250hidden extraction absent visiblypage12 ignored. Flights/transferincluded scope andrefund30day/personalabsence contradictions unresolved. Ireland4weekhostfamily separately,feenotpublished,ScotlandtermsnotIrelandcontract;SpanishoperatordoesnotmakecampcountryESP.',
 'TechSpark LEGO-specific2027 not proved by generalcitycalendar; priorcourseprofileunchanged. HESsameNatukexistingprofile not duplicated. RobotikidsSSL mismatch/readererror,PlayCodeDNS/readererror,AAL433shell do not yield new validatedprogramme.',
 'All14old family budget offers retained exactly;three new estimates:Paris640half/1380full per5days andBarcelona120one-day. No invented siblingdiscount;missinginvoice/insurance/travel/lodging remain unknown.17 scenarios/10 providers. CompleteSQLite/JSONZIP,no recordtruncation;oversizedrawdownloads absent byfilecaprule.',
 '32HTTPattempts/25success including23HTML(oneAALshell) and2PDF;4posterdownloads/3uniquevisualposters.16selectedPDFpages reviewed across2documents. Readerfallback retained separately. Noexternal messages/forms/payments/accounts/consents/schedules.',
 'Worldwide competitions/leagues/exhibitions,allgeneral/thematic/STEMcamps2026–27 EN/ES/RU,permanentschools/5–10yearresultshistory,familyroutes andallprioritycountries preserved. Nativegoalactive,0fullyauditedcountries;nativepublication separate.'
]
priority='Continue deep Switzerland/France/Spain/Europe,Taiwan/Singapore/SouthKorea/Japan,USA/Canada,CostaRica/Mexico/LatinAmerica: all general/thematic/STEM camps2026–27,day/boarding/family and EN/ES/RU. Current primary course curriculum,actual technical teacher language,foreign individual intake,full two-child pricing/equipment/nightcare/insurance/refunds,quality shortlist and routes. Preserve worldwide competitions/leagues/exhibitions andpermanentschools/5–10yearresulthistory. No country/worldwide completion claim from a bounded pass.'
audit=dict(version=111,asof=CHECKED,status='progress',scope='Selected own-site programmes/policies/posters/PDFs in Switzerland/France/Spain andUK/Ireland venues. Other priority countries remain in the active worldwide objective; not a full country/world audit.',new_dossiers=len(NEW),new_dossier_slugs=NEW,updated_dossier_slugs=UPDATED,new_event_ids=newids,updated_event_ids=[],events=len(now),camp_learning_records=blocks['Лагеря'],programme_dossiers=len(cp['profiles']),countries_with_dossiers=len(cp['countries']),official_dossier_urls=1272,editorial_scenarios=len(cp['shortlist']),coverage_gaps=len(cp['gaps']),country_dossier_counts=countries,competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],league_profiles=len(d['league_guide']['profiles']),budget_scenarios=17,budget_providers=10,new_budget_scenarios=3,family_ical=family,exhibition_ical=expo,new_visual_pdf_checks=16,new_visual_image_checks=3,external_actions=external,goal='active',worldwide_complete=False,fully_audited_countries=0,checks=checks,next_research=priority)
def write(stem,value):
 s=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('europe-camps-audit-v111',audit)
write('europe-camps-source-receipts-v111',dict(version=111,asof=CHECKED,scope=audit['scope'],sources=sources,primary_reader_fallback=reader,posters=posters,visual_review=visual,external_actions=external))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=111:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native110 succeeded and refreshed111;commit '+BASE+';deployment appgdep_6ac4968cfde08191bec3ab27ae989aaa. Full worldwide objective remains active.')
plan['latest_validation']=dict(version=111,asof=CHECKED,status='Selected primary programme,visual sources and portable database checks;nativepublication separate',events=len(now),camp_learning_records=blocks['Лагеря'],programme_dossiers=827,countries_with_dossiers=39,official_dossier_urls=1272,editorial_scenarios=193,budget_scenarios=17,budget_providers=10,family_ical=family,exhibition_ical=expo,league_profiles=audit['league_profiles'],worldwide_complete=False,fully_audited_countries=0)
plan['europe_camp_programme_audit_v111']=audit;plan['complete_database_download']=sm;plan['complete_json_download']=jm
for q in plan['requirements']:
 if q['id']=='unified_database':q['evidence']='v111:3419cards/827dossiers/39countries;12newprogrammeprofiles/43calendarrows;all prior objects retained. Complete portable JSON/SQLZIP without truncation.'
 elif q['id']=='camp_full_pricing':q['evidence']='v111:17familyestimates,14old+3new:Paris640half/1380fullEnglish+badminton,Barcelona120one-day. Swissflight210onlyapprovedsubsidy/regularpriceunknown;UK2299/599inside,Irishfeeunknown. Full invoice,places andtravel not confirmed.'
 elif q['id']=='camp_calendar_2026_2027':q['evidence']='v111:43 new dates including16juniorParisrows,4Flight2027blocks and4Barcelonaindividualdays;teen/12+ futureage gates andfilledBasel course not familyICS. FamilyICS2643/expo104;no invented2027course from genericcalendar oroldFAQ.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=111]+[dict(version=111,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=12,new_calendar_rows=43,updated_calendar_rows=[],official_primary_retrieval_attempts=32,pdfs_downloaded=2,new_visual_pdf_checks=16,new_visual_image_checks=3,not_complete_worldwide=True)]
plan['next_research']=[priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED;write('research-plan',plan)
p=ROOT/'dist/index.html';s=p.read_text().replace('?v=110','?v=111').replace('data-ui-version="110"','data-ui-version="111"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_europe_camps_audit_v111.json" download>Европа · новые смены, языки, пансионы и стоимость для братьев</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text().replace('ПОДРОБНЫЙ ВЫБОР · 05 ОКТЯБРЯ 2026','ПОДРОБНЫЙ ВЫБОР · 06 ОКТЯБРЯ 2026')
anchor='<a href="downloads/STEM_americas_camp_audit_v106.json"'
link='<a href="downloads/STEM_europe_camps_audit_v111.json" download>Европа: новые смены, языки и семейная стоимость ↓</a> · <a href="downloads/STEM_europe_camps_source_receipts_v111.json" download>Первичные страницы, афиши и PDF Европы ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(status='progress',version=111,new_dossiers=12,new_calendar_rows=43,dossiers=827,events=len(now),budget_scenarios=17,goal='active')))
