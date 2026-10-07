"""Bounded primary research and publication material; worldwide objective stays active."""
import collections,hashlib,json,subprocess
from camp_northamerica_v114 import ROOT,BASE,CHECKED,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-northamerica-primary-v114'
d=json.loads((ROOT/'data/catalog.json').read_text());b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
cp=d['camp_programmes'];old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
changed=[k for k in old if old[k]!=now[k]];newids=sorted(now.keys()-old.keys())
assert len(newids)==57 and not changed and len(cp['profiles'])==861
assert d['camp_planning']['offers']==b['camp_planning']['offers']
sources=[]
for f in sorted(P.glob('receipt-*.json')):
 for item in json.loads(f.read_text()):
  q=dict(item,checked=CHECKED,retrieval_method='direct_http',content_scope='Selected public programme/policy or closure clauses; not an entire site/country audit.')
  if q.get('status')==200:
   ext='pdf' if (P/(q['key']+'.pdf')).exists() else 'html';raw=(P/(q['key']+'.'+ext)).read_bytes()
   assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
   scope='closure_notice_redirect_not_current_tuition_or_intake' if q['key'].startswith('lohikan') else 'old_2025_pdf_comparison_not_counted_as_read' if q['key']=='hurontario-handbook' else 'selected_2026_visual_pages_not2027contract' if ext=='pdf' else 'unsigned_public_contract_read_only_no_submission' if q['key']=='ncc-registration' else 'selected_html_clauses'
   q.update(raw_filename=q['key']+'.'+ext,body_snapshot_retained=True,content_status=scope)
  else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body_primary_reader_separate')
  sources.append(q)
assert len(sources)==36 and sum(q.get('status')==200 for q in sources)==26
reader=[]
for name in ['public-reader-snapshot.json','public-reader-comparison.json','public-reader-onondaga-dates.json']:
 raw=(P/name).read_bytes();reader.append(dict(private_filename=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),scope='Selected public-reader extracts; may be cached and do not override fresher direct closure/404 evidence. Not an HTML/PDF body or independent organizer confirmation.'))
visual=json.loads((P/'visual-review.json').read_text());assert visual['new_visual_pdf_checks']==6
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
sm=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text());jm=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT');expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert family==2707 and expo==104
blocks=collections.Counter(q['block'] for q in now.values());country_counts=dict(collections.Counter(q['iso'] for q in cp['profiles']))
urls=len({s['url'] for p in cp['profiles'] for s in p['sources']});assert urls==1338
checks=[
 '15 genuinely different programme/age/format dossiers under six provider brands, including two theCoderSchool branches. Not15 independent providers or a world ranking. All846 prior dossiers/3433 complete prior event objects unchanged.861 dossiers/39countries/1338URLs/203editorial scenarios/220gaps;3490events incl2148camp-learning.',
 'Onondaga2027 welcomes6–16;Jincis birthyears2017–2021 cover both children. Six unambiguous sessions added:Jul2–28/Aug1–27/Jul2–15/Jul15–28/Aug1–14/Aug28–Sep3. B2Aug14–27 with4550/5665 versusAug8–21 with4335/5395 on same2027page: neither ambiguous B2 entered as exact session.',
 'Onondaga domestic/international prices separated and13%HST extra. Cinternational2800perchild;two5600+728tax=6328 is conditional arithmetic,symbol$currency unknown,not fullfamilyinvoice. Internationalallinclusive composition unknown;500nonrefundableadmin inside1000deposit,Jan15wholedepositnonrefund,Feb15half/Apr1balance,no refunds for any reason afterFeb15. Nochildphones/calls exceptemergency,no1/2weekparentvisits. Own2026handbook cachedreader/direct404,not2027contract/transferquote.',
 'Hurontario current2027dates:Intro5–8 Jul11–17/Aug8–14 onlyOscar;Matvey9–10noteligible. Regular7+ andsession-specificmax13/15/16,Oscaronlyafter7birthday. Intro dates fully covered onlyby3.5weekregular,not either shorterhalf. 2027prices1990/3650/3500/5360/5150+HST. CAD explicitly in own2026handbooks;2027currency/fulltaxinvoice stillconfirm. 2026boat70perdirection/registration300/May1balance not guaranteed2027currentfees.',
 'Hurontario approximate2:1staffratio/cabins6–8/nursepractitioner/swimassessment/PFD ownclaims;nochildcalls/electronics,letters only. Intro20:30versusregular21:30nightwatch from2026handbooks,notcurrent2027contract. Six full selectedPDFpages visuallyinspected,24pages fulltext fromtwo2026documents;older2025PDFnotcountedread.',
 'MiniYoWe2027 sevenovernightweeksJul11–Aug28andsevenweekdayweeksJul12–Aug27. Junior/day5–9,Matveyonlywhile9;Boys10–15after10birthday. ChristianBible/worship daily explicit,notseculartechnicalcamp.1350+HSTovernight/875HSTexemptday;currencycodeabsent. $1depositnotfullfee;2027cancel350versusFAQ/programme300 conflict;thirdchild300discountdoesnotapplytotwo. Laundry55/bus110oneway/addons/tuckseparate;old2019occupancy/2020instructionsnotcurrentavailability.',
 'Mondamin2027 sixage+beforecampgrade-specificsessions;MiniII11–14bothlater,Oscaronly7+June/Aug/JuniorafterGrade1. Junior8dayonlyoneyearsteppingstone. Parent-and-sonsMay21–23/Aug13–15 ages5–15,oneguardian(anygender),onlyboys:900pair+300extrason=1200base,nottwoadultpackage. Meals/activities/programmetransportincluded,externaltravel/insurance/Thursdayunknown,currencycodeabsent. FriendsFamilySep3–6 priceforkids6+ambiguous,notinventedestimate.',
 'NCC2027 exactfiveUniversitycampusweeks for8–18day/board;mainlanguages9+ agegate/prerequisites retained. Oscar6–8morningScratchonly,Arduino/3D/GameDesignlab explicitly unavailable. Morning2027table400vsownmorningpage350,minuslimited50grant conflict;campuscohort dates notindependentlybound,nomorningdatedrows. Daytime21vs21:30and08:45vs09conflicts;fullentry/intake/teacherENnotconfirmed.',
 'NCCbase1450boarding/1195day,limitedgrant200notguaranteeduntilfullpayment;card35/week,Arduino65one-time,3D/game65/course/week,weekend285,change50/late40. Deposit150/week+labs,refundtransaction60daycardlimit and10daybeforestartblackout retained. Arduino kit takehome,RobotBattleonscreensimulation,3DCTonly,AIcreativecomputing1hour generativeprojects—notphysicalworldroboticsleague/universitycredit. Oldvirtualformweeks notnew2027rows.',
 'Pasadena9 ownexplicitdatedholidayworkshops2026–27 groupedfourcurricula:robotmBotNEO7+/block7–10/Python10+,3D7+,Scratch7+/Roblox9+,Python9+. Dec21–24robot560+optional145takehome=705,3D4day560/singleday130,Python/games4day520,singleday130. Lunch/waterown/aftercare30day,minimumenrollment/refund21daysfull7days50%,oldMay31summerdiscountexpired. After-school2:1notcampcoachratio;Oscar2026under7,2027one-dayonlyafter7birthday.',
 'EastCobb own6–9mBotprogramme differentfromgenericnetwork10+;nov/decdatesno year,nonewexactrows. Oct1holiday399saleexpiredatOct6,base499onlyunconfirmedcurrentinvoice. VRunderagepolicy/alternative/gearownership/localrefundunknown;Pasadena refundnotcopied.',
 'Lohikan freshownhomepage says2026finalLakeComo season,saleMorashaexpected2027. Oldtuition/internationalURLs nowredirecttoclosurenotnewrates. NoLohikan2027sessionadded;Greeley/Cayugaareseparateprospectiveproviders,notrenamedautomaticLohikaneligibility/refund.',
 '57newexactdatedcampcards;56newtentativefamilyICS becauseMondaminMiniIIbothlaterexcluded. All2651oldfamilyUID/content unchanged exceptDTSTAMP;exhibitions104 unchanged. 17existingbudgetoffers untouched,nofullcurrencyverifiednewinvoice. CompleteJSON/SQLiteZIP/rowpreservation/filecapschecked.',
 '36directHTTPattempts26HTTP200(23HTML/3PDF),10errors(406/403/404);three separateprivatepublic-reader snapshots supplementblockedpages,notclaimingliveHTTPaccess. Onondaga dates search-reader retains birthyear and both conflicting B2 rows; direct open remains unavailable. Noforms/messages/payments/accounts/consents/automations. Worldwidegoalactive,0fullyauditedcountries.'
]
priority='Continue deep Switzerland/France/Spain/Europe,Taiwan/Singapore/SouthKorea/Japan,USA/Canada,CostaRica/Mexico/LatinAmerica: all general/thematic/STEM camps2026–27,day/boarding/family and EN/ES/RU. Verify actual curriculum,teacherlanguage,foreignindividualintake,fulltwochildpricing/equipment/nightcare/insurance/refunds androutes. Preserve worldwide competitions/leagues/exhibitions/schools/results5–10years/engineeringentrepreneurjourney; full objective remains active.'
audit=dict(version=114,asof=CHECKED,status='progress',scope='Selected North American2027 general boarding/family and technical campus programmes, Pasadena2026/27holidays and important contradictory/closure evidence; not a complete country/world audit.',new_dossiers=len(NEW),new_dossier_slugs=NEW,updated_dossier_slugs=UPDATED,new_event_ids=newids,updated_event_ids=changed,events=len(now),camp_learning_records=blocks['Лагеря'],programme_dossiers=861,countries_with_dossiers=len(cp['countries']),official_dossier_urls=urls,editorial_scenarios=203,coverage_gaps=220,country_dossier_counts=country_counts,competition_records=1153,exhibition_records=189,league_profiles=len(d['league_guide']['profiles']),budget_scenarios=17,budget_providers=10,new_budget_scenarios=0,family_ical=family,exhibition_ical=expo,new_visual_pdf_checks=6,pdf_pages_text_extracted=24,external_actions=external,goal='active',worldwide_complete=False,fully_audited_countries=0,checks=checks,next_research=priority)
def write(stem,value):
 s=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('northamerica-camps-audit-v114',audit)
write('northamerica-camps-source-receipts-v114',dict(version=114,asof=CHECKED,scope=audit['scope'],sources=sources,reader_snapshots=reader,visual_review=visual,external_actions=external,primary_reader_limits='Onondaga/MiniYoWe public-reader excerpts may be cached; directrequests blocked406/403. Onondaga2026PDF direct404 despitecachedreadertext. OwnLohikanclosure direct200overridescachedtuitionresults. Hurontario2026handbooks not2027contracts. Noexternalorganizerconfirmation.'))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=114:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native113 succeeded;commit '+BASE+';deployment appgdep_6ac4aaa43e188191a50827f4fc5d1b1d. Worldwide objective remains active.')
plan['latest_validation']=dict(version=114,asof=CHECKED,status='Selected primary clauses and complete portable database checks; native publication separate',events=3490,camp_learning_records=2148,programme_dossiers=861,countries_with_dossiers=39,official_dossier_urls=1338,editorial_scenarios=203,budget_scenarios=17,budget_providers=10,family_ical=2707,exhibition_ical=104,league_profiles=audit['league_profiles'],worldwide_complete=False,fully_audited_countries=0)
plan['northamerica_camp_programme_audit_v114']=audit;plan['complete_database_download']=sm;plan['complete_json_download']=jm
for q in plan['requirements']:
 if q['id']=='unified_database':q['evidence']='v114:3490cards/861dossiers/39countries;15newprofiles/57newholiday2026–27rows. All3433prior completeeventobjects/all846priorcompleteprofiles unchanged. CompleteJSON/SQLiteZIPwithouttruncation.'
 elif q['id']=='camp_full_pricing':q['evidence']='v114:17priorfamilyestimatesunchanged. Taxes/extras/labfees/gearownership/refunds retained;OnondagaB2,MiniYoWe350/300,NCC400/350conflicts;symbolcurrency/foreignfamilyfullinvoiceunknown. No newverifiedfullfamilybudget.'
 elif q['id']=='camp_calendar_2026_2027':q['evidence']='v114:57newexact2026–27campcards,56newtentativefamilyICSwithgates. FamilyICS2707/expo104;allpriorUID/contentretained. NoinventedOnondagaB2/EastCobbyear/NCCmorningcohort/Lohikan2027.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=114]+[dict(version=114,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=15,updated_dossiers=0,new_calendar_rows=57,updated_calendar_rows=[],official_primary_retrieval_attempts=36,pdfs_downloaded=3,pdfs_read=2,new_visual_pdf_checks=6,not_complete_worldwide=True)]
plan['next_research']=[priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED;write('research-plan',plan)
p=ROOT/'dist/index.html';s=p.read_text().replace('?v=113','?v=114').replace('data-ui-version="113"','data-ui-version="114"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_northamerica_camps_audit_v114.json" download>США и Канада · смены 2027, зимняя техника и возрастные условия</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text();anchor='<a href="downloads/STEM_latam_camps_audit_v113.json"'
link='<a href="downloads/STEM_northamerica_camps_audit_v114.json" download>США и Канада: программы, цены и возрастные ограничения ↓</a> · <a href="downloads/STEM_northamerica_camps_source_receipts_v114.json" download>Первичные страницы и ограничения доказательств ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(status='progress',version=114,new_dossiers=15,new_calendar_rows=57,dossiers=861,events=3490,budget_scenarios=17,goal='active')))
