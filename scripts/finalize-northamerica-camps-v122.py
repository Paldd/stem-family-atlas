"""Selected public evidence and portable-database manifest; no full-world claim."""
import collections,hashlib,json,subprocess
from camp_northamerica_v122 import ROOT,BASE,CHECKED,NEW
P=ROOT.parent/'stem-family-atlas-work/camp-americas-primary-v122'
d=json.loads((ROOT/'data/catalog.json').read_text());b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']};cp=d['camp_programmes'];offers=d['camp_planning']['offers']
newids=sorted(now.keys()-old.keys());assert len(newids)==58 and all(now[k]==v for k,v in old.items())
assert len(cp['profiles'])==932 and [q['slug'] for q in cp['profiles'][915:]]==NEW and cp['profiles'][:915]==b['camp_programmes']['profiles']
assert d['camp_planning']==b['camp_planning'] and len(offers)==43
sources=[]
for f in sorted(P.glob('receipt-*.json')):
 for item in json.loads(f.read_text()):
  q=dict(item,checked=CHECKED,retrieval_method='direct_public_http',content_scope='Selected age, programme, dated session, price and policy clauses or discovery; not entire websites/countries.')
  if q.get('status')==200:
   name=q['key']+'.html';raw=(P/name).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
   q.update(raw_filename=name,body_snapshot_retained=True,content_status='selected_html_clauses_or_discovery')
  else:q.update(body_snapshot_retained=False,content_status='retrieval_error_not_content_evidence')
  sources.append(q)
assert len(sources)==35 and sum(q.get('status')==200 for q in sources)==29
raw=(P/'web-reader-kandalore.txt').read_bytes();assert b'2017-2021' in raw and b'5,830' in raw and b'2027' in raw
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
blocks=collections.Counter(q['block'] for q in now.values());family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT');expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert (family,expo)==(2872,104)
urls=len({s['url'] for p in cp['profiles'] for s in p['sources']})
audit=dict(version=122,asof=CHECKED,status='progress',scope='Selected Canada/USA general, family, arts and film programme clauses, 2027 dated variants. Seventeen programme dossiers across five operators are not seventeen independent top-ranked camps. Prior worldwide technical leagues/camps remain; no all-country or accepted-intake claim.',events=len(now),competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],camp_learning_records=blocks['Лагеря'],programme_dossiers=932,countries_with_dossiers=39,official_dossier_urls=urls,editorial_scenarios=len(cp['shortlist']),coverage_gaps=len(cp['gaps']),league_profiles=len(d['league_guide']['profiles']),budget_scenarios=43,budget_providers=21,budget_programme_dossiers=len({q['slug'] for q in offers}),new_budget_scenarios=0,new_dossiers=17,new_dossier_slugs=NEW,new_programme_brands=['Camp Can-Aqua / Northern Ontario Film Academy','Kandalore','Interlochen','Camp Cayuga','Camp Watitoh'],updated_dossier_slugs=[],new_event_ids=newids,updated_event_ids=[],unchanged_dossier_objects=915,unchanged_event_objects=3599,unchanged_prior_budget_objects=43,source_retrieval_attempts=35,direct_successful_bodies=29,retrieval_errors=6,pdf_download_files=0,new_visual_pdf_checks=0,family_ical=family,exhibition_ical=expo,goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,checks=[
 'Can-Aqua ShortStay1A5–15 and eight5–11 table rows; Intro8–15 overrides conflicting general5–15, Oscar6–7 excluded. TwoWeek6–14 vs heading6–15, FourWeek9–14 vs9–15: specific matrix controls. Day4/5days09–16:30 lunchincluded, no siblingdiscount, no copiedboardingdeposit. Film9–15 Matveycandidate/Oscarlater,3productionperiods/day+elective, no coding/robotics claim.',
 'Can-Aqua family895June/1195September is up-to-five same-household unit. Pair395 means oneparent/onechild in offgridSummit, not wholefamily. PairthirdJune18–Sept20 sourceconflict omitted fromprecisecalendar. Familycancel explicitly excluded from general May1refund rule. Includedmembership200 not twice, deposits650/900/1250 inbase,card2%deposit-only, tax/codecurrency unknown. Siblingsdifferentage notsamecabinguarantee.',
 'Kandalore own2027reader table born2017–2021 oneweek,PrepJunior2016–2020 longer, not old age6–9/headbooks. International2390/week,5830/twoweeks,8650/four vsDomestic2200/4225/7150 whosepricingCanadaUSA. CostaRicaresidentfamily notautomaticallyDomestic. CurrentdirectHTTP406 distinguished from primarysearchreader selected clauses crawled2weeksago. Summerfamily410adult/330child+HST domestic only; winterski passes1/2 for3/5days,rentalextra,TBAprice. SchoolgroupOECwindows/old2020skiPDF not openchild2027programme.',
 'Interlochen Junior3–6 currentgradeBEFOREsummer notrisingfall. Exploration andVisualArt separate curricula,5300/twoweeks+65applicationfee;VisualArtnoportfolio,4studioh/day. Priority15Jan2027,tuitionMay1,scholarshipnotguaranteed. OwnintFAQstudentstatus/I20 andB1B2restriction notpersonallegaldecisionforfamilyE2. AcademyESL/annualfees/privatehighschoolranking/collegecertificatebanner notJuniorcampEN/credit/robotics. TVConlyairportpickup notChicago/Detroit;Juniorlaptopsnotgeneraltechcampgear.',
 'ArtsDiscovery2027snapshot7–12/currentgrade1–6,sevenMonFriweeksJun21–Aug6: datescalculatedfrompublishedrule, themes2027TBA, old2026themesnotrelabelled.425/week100deposit snapshot mixed2026/27;price/contract2027confirm,notnewfullfamilybudget. Matveygradecheck,Oscaronlyafter7andgrade1–6.',
 'CayugaJuniorCampus≤13/entering1–8 separate JuniorDivision≤9/entering1–4. Fourmini2027sessions precise;first6weekSundayJune26contradiction omitted. Normal4200+mandatorycanteen120;displayeddiscounteligibility notguaranteed. Canteencoverslaundry/snacks/Tshirt,linen35/2weekoptional;NYbus140oneway/AVP70/EWR140/JFK180extra. Firsttimeproratedguarantee tuitiononly afterordinarycharges,notcanteenfullrefund/certaintyofcontract.',
 'Watitoh2027Full14950Jun26Aug13/FirstMonth11500Jun26Jul25;enteringgrade≤5fallAFTERcamp,minimumageunknown,notbothcandidate. EarlycreditOct1expiredatOct6,noaddeddiscount. Gearinternetdevicesprohibited:notcoding. Internationalcommunitynotacceptedseat/ENpromise. Deposit/cancel/currencyunknown.',
 'Tamarackcamptamarack.com ownbodycentralOregonUSA,notOntarioCanada orMichiganJewishtamarackcamps.com. GreeleyDNSfailure and InterlochenhypothesizedJuniorWritingURL404 are gaps/discovery,nofakeCanadian/writingprogramme. NonewconfirmedEN/ES/RUfor17dossiers: Englishpage alone not instruction.',
 'All3599old events/915oldprofiles/43oldbudgetobjects preserved;58new2027course/sessionvariants. Familyovernight eventvariants residential withparentrequired, notdaychildcare. FullportableJSON/SQLite retained. Worldwide objective active;0fullyauditedcountries.'
 ])
def write(stem,v):
 s=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('northamerica-camps-audit-v122',audit)
write('northamerica-camps-source-receipts-v122',dict(version=122,asof=CHECKED,scope=audit['scope'],sources=sources,web_reader=[dict(url='https://www.kandalore.com/'+tail,status='selected_2027_own_search_reader_clauses',direct_http_error='406',crawl_age='about2weeks according to reader',checked=CHECKED) for tail in ['rates-and-dates/','outside-programs/']],private_reader_files=['web-reader-kandalore.txt'],reader_snapshot_sha256=hashlib.sha256(raw).hexdigest(),pdf_download_files=0,external_actions=external,primary_reader_limits='Selected programme/fee/policy clauses and discovery, not whole-site/fullcountry/accepted-intake. Directrawbodies and primaryreader snapshots outside repository. Englishteaching/currency unknown for all new candidates.'))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=122:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native121 succeeded2026-10-06T12:00:50.428790Z; commit '+BASE+'; deployment appgdep_6ac4e2d6512c8191b82ee05aa77b22c2. Worldwide objective active.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','budget_providers','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected North America programme/policy clauses and complete portable database checked; native publication separate.'
plan['northamerica_camp_programme_audit_v122']=audit
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for q in plan['requirements']:
 if q['id']=='unified_database':q['evidence']='v122:3657 events/932 programme dossiers/39 countries/1460 URLs;17 newNA dossiers/58future2027variants. Every3599old event/915profile/43budgetoffer preserved; fullJSON/SQLiteZIP.'
 elif q['id'] in ['camps','family_top_picks']:q['evidence']='v122:932 dossiers/39 countries/224editorialscenarios. General/day/boarding/family/film/arts2027NA with birthyear,current-vs-risinggrade andparticularsessionagegates. AllpriorCHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/CRI/MEX/LatAmwork retained;EN/ES/RUglobalfocusactive. Notcompleteworldwide.'
 elif q['id']=='camp_full_pricing':q['evidence']='v122:43oldpartialfamilybudgets unchanged. NewNApublishedbaseprices separatemandatoryfees,depositincluded,domestic/international/family/pairunits. Unknowncurrency/tax/EN/foreigncontract anddatesconflict preventnewconfirmedfullbudget.'
 elif q['id']=='camp_calendar_2026_2027':q['evidence']='v122:58newprecise2027variants,including7ArtsDiscoverycalculatedMonFrivariantslabelledpublishedrule/themesTBA;familyICS2872/expo104. OldUID/contentpreserved;CanAquapair3/Cayugafirst6wkconflictsnotexactdates.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=122]+[dict(version=122,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=17,updated_dossiers=0,new_calendar_rows=58,new_budget_scenarios=0,official_primary_retrieval_attempts=35,pdf_download_files=0,not_complete_worldwide=True)]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=121','?v=122').replace('data-ui-version="121"','data-ui-version="122"');anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_northamerica_camps_audit_v122.json" download>США и Канада · новые программы 2027</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text();anchor='<a href="downloads/STEM_asia_camps_audit_v121.json"';link='<a href="downloads/STEM_northamerica_camps_audit_v122.json" download>США и Канада: 17 досье и 58 вариантов 2027 ↓</a> · <a href="downloads/STEM_northamerica_camps_source_receipts_v122.json" download>Источники и ограничения проверки ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps({k:audit[k] for k in ['version','status','events','programme_dossiers','new_dossiers','family_ical','official_dossier_urls','worldwide_complete']}))
