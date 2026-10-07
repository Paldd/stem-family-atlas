"""Publishable selected-source audit; broad worldwide research remains active."""
import collections,hashlib,json,subprocess
from camp_europe_v120 import ROOT,BASE,CHECKED,NEW,NEW_IDS
P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v120'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
newids=sorted(now.keys()-old.keys());assert len(newids)==4 and all(now[k]==q for k,q in old.items())
cp=d['camp_programmes'];offers=d['camp_planning']['offers'];new=offers[35:]
assert len(cp['profiles'])==897 and [q['slug'] for q in cp['profiles'][890:]]==NEW
assert cp['profiles'][:890]==b['camp_programmes']['profiles']
assert offers[:35]==b['camp_planning']['offers'] and [q['id'] for q in new]==NEW_IDS
sources=[]
for f in sorted(P.glob('receipt-*.json')):
 for item in json.loads(f.read_text()):
  q=dict(item,checked=CHECKED,retrieval_method='direct_public_http',content_scope='Selected public programme, price, age and policy clauses. Not an entire site, country or accepted intake audit.')
  if q.get('status')==200:
   ext='pdf' if (P/(q['key']+'.pdf')).exists() else 'html';name=q['key']+'.'+ext;raw=(P/name).read_bytes()
   assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
   q.update(raw_filename=name,body_snapshot_retained=True,content_status='selected_pdf_clauses' if ext=='pdf' else 'selected_html_clauses')
  else:q.update(body_snapshot_retained=False,content_status='retrieval_error_not_content_evidence')
  sources.append(q)
assert len(sources)==27 and sum(q.get('status')==200 for q in sources)==24
visual={'pari-ranelagh-autumn-pdf':[1,3,4],'pari-convention-autumn-pdf':[1,2,3],'pari-convention-fee-pdf':[7],'enforex-2027-pdf':[11,33,35]}
for key,pages in visual.items():
 for page in pages:assert (P/f'{key}-visual-{page}.png').stat().st_size>0
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
blocks=collections.Counter(q['block'] for q in now.values())
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT')
expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert (family,expo)==(2774,104)
audit=dict(version=120,asof=CHECKED,status='progress',scope='Selected new France/Spain family, bilingual day and technical programme dossiers; Enforex2027 partial two-child prices and Pari2026–27 venue-specific prices. Not all European camps or a worldwide completion claim.',
 events=len(now),competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],camp_learning_records=blocks['Лагеря'],programme_dossiers=897,countries_with_dossiers=39,official_dossier_urls=1412,editorial_scenarios=217,coverage_gaps=244,league_profiles=len(d['league_guide']['profiles']),
 budget_scenarios=43,budget_providers=21,budget_programme_dossiers=len({q['slug'] for q in offers}),new_budget_scenarios=8,new_budget_ids=NEW_IDS,new_budget_brands=['Enforex','Pari-Grandir'],
 published_budget_components=[dict(id=q['id'],currency=q['currency'],amount=sum(q['base_by_child'].values())+sum(x['amount'] for x in q['required']),children=q['children'],complete=False) for q in new],
 new_dossiers=7,new_dossier_slugs=NEW,new_programme_brands=['Country Kids','Pari-Grandir','Etopia Kids / Fundación Hiberus','PlayCode Academy'],updated_dossier_slugs=[],new_event_ids=newids,updated_event_ids=[],unchanged_dossier_objects=890,unchanged_event_objects=3555,unchanged_prior_budget_objects=35,
 source_retrieval_attempts=27,direct_successful_bodies=24,retrieval_errors=3,pdfs_downloaded=5,pdf_pages_text_extracted=57,new_visual_pdf_checks=10,family_ical=family,exhibition_ical=expo,goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,
 ui_fix='Offer switching after editing a focused expense field can synchronously dispatch the old field change during DOM replacement. Ignore these previous-offer events while replacing the form; new fields and options reset before recalculation.',
 checks=[
  'CountryKids is a parent-accompanied family resort, not child-only boarding. English-speaking childcare team and up-to12 club explicit. From7490EUR/family4/week has no established2027priceyear or exactsessions. Sat–Sat only. FAQ excludes Saturdaylunch and parentsTue/Thu restaurantdinners. Mandatoryholidayinsurance outsideprice; current2024contract30%advance/eightweekbalance/nineweekresale-onlyrefund/300fee explicit.',
  'PariConvention venue3–10 includeslunch:450first/337second/fullweek,787both printedtable, not450*.75rounding. Ranelagh venue3–6 takesOscaronly395/fullweek andownlunchbox. Generic3–10widgetdoesnotexpandRanelagh. Own centrePDFs exactly19–23/26–30Oct2026 bilingualdailyplans, fournewfuturecalendarrows. Network2027winter/spring/summerwindowsnotcopied to everyvenue; AtMontessori pupilprice notforeign-familyprice. Taxcreditnotapplied andannualafterschooltermsnotcampcontract.',
  'Etopia2026 completed: three dossiers for6–8junior,8–11game/space/science,10–13robotics/cyber/AI, not threeoperators. Ten realitineraries include12–15oldertracks. JuniorOscaronly2027; middleMatvey; advancedonlyafter10. Week130,early5/week,lunch27/week archived. Early10%deadlineexpired; siblingcodeafterfirstpurchase notautomaticbothorders. Sameitineraryrepeatdiscouraged; no inventedEnglishteacher/2027dates/newinvoice.',
  'ULPGC ownJune2026 announcement6–16 andLEGO/Arduino/Microbit/Edison/drone/3D explicitlyread. Firstweek22/23/25/26June onlyfourdays; all2026sessionspast.135external/115ULPGC andunspecifiedsiblingdiscount notnew2027quote orfull-three-sessioncost. OperatorbothdirectURLsDNSerror; universitybodyfullselectedprogrammevalid. Campusvenue notacademiccredit, language/kitownership/newseason/cancellationunknown.',
  'EnforexPDF page33 matrix visuallychecked: Madrid3two-weekblocksJul/Aug1; Elviria4includingAug15; Salamanca2Julyonly. Board2495Madrid/2095others perchild2wk plus35/childapplication=5060/4260both. Day1200/child2wk plus35each=2470both, actualMo–Frboundaries separatefromboardSun–Sat. Feevalid12months; firstfamilyregistrationassumed, notlifetimesurcharge. Alljunior5–18, homestay14+ excluded.20*45minlanguage=15h/week, camp-lifeEnglishnotpromised; certificate notworldwin.',
  'Enforex local95/person/oneway is localstation/airport in samecity, notMadridairporttoSalamanca. SalamancaMadrid↔camp220/personshuttle separatelymodeled440both, localoptionnotduplicated. Daybus250/2wk/child onlypublishedcities, noSalamancabuspromise. Optionalguarantee300/week/person=1200both2wk withcontractlimits; fulltripcostnotrefundpromise. Junior100%supervision distinctfromYoungAdults50%; genericdeposit250 andcamp850/4wk/2wkrefundclauses notsummed asnewcharges; actualcontract/coverage/invoiceconditional.',
  'Everyprior3555event,890dossier,35budgetoffer object preserved; onlyfourPari futurecalendarrows added. Entireworldwidecompetition/exhibition/league/school-history/routes remain. No independent topcamp ranking manufactured. Unknownmandatoryamounts notzero, onechildOscarprice notfreeMatvey. Worldwidegoalactive,zerofullyauditedcountries.'
 ])
def write(stem,v):
 s=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('europe-camps-audit-v120',audit)
write('europe-camps-source-receipts-v120',dict(version=120,asof=CHECKED,scope=audit['scope'],sources=sources,visual_pdf_pages=visual,new_visual_pdf_checks=10,pdf_pages_text_extracted=57,
 web_reader=[dict(url='https://playcodeacademy.com/campus-tecnologico-de-verano/',status='selected_primary_reader_body_2026_and_stale2024_cards',direct_http_error='DNS; no direct body snapshot'),dict(url='https://www.zaragoza.es/sede/servicio/tramite/33960',status='selected_primary_reader_body_2026',direct_http_error='Timeout; no direct body snapshot')],external_actions=external,
 primary_reader_limits='Selected public pages and PDF clauses; raw bodies and selected rendered pages retained outside website source. No entire-site/country audit, foreign accepted intake, reserved seat or full invoice confirmation.'))
sm=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text());jm=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=120:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native119 succeeded2026-10-06T10:57:31.176286Z; commit '+BASE+'; deployment appgdep_6ac4d409eff48191a01453d0133b02cc. Worldwide objective active.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','budget_providers','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected France/Spain primary clauses and complete portable database verified; native publication separate.'
plan['europe_camp_programme_audit_v120']=audit;plan['complete_database_download']=sm;plan['complete_json_download']=jm
for q in plan['requirements']:
 if q['id']=='unified_database':q['evidence']='v120:3559events/897dossiers/39countries;7newFrance/Spainprogramme dossiers,4PariOctcalendarrows,fullJSON/SQLiteZIP;every3555prior event and890priorprofileobject preserved.'
 elif q['id']=='camp_full_pricing':q['evidence']='v120:43 partial scenarios/21brands/33dossiers. SixEnforex2027two-childday/board andtwoPari2026centre-specificoffers; 35oldoffers unchanged. CountryKidsfrom7490family4 withoutyear notchildcalculatorbase. Fullinvoiceunknown.'
 elif q['id']=='camp_calendar_2026_2027':q['evidence']='v120:Fourcentre-specificPariOctober2026rows; noCountryKids2027/Etopia2027/PlayCode2027 made-up dates or network2027windows turnedintocentreappointments. FamilyICS2774/expo104 withpriorUID/content preserved.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=120]+[dict(version=120,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=7,updated_dossiers=0,new_calendar_rows=4,new_budget_scenarios=8,official_primary_retrieval_attempts=27,pdfs_downloaded=5,new_visual_pdf_checks=10,not_complete_worldwide=True)]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=119','?v=120').replace('data-ui-version="119"','data-ui-version="120"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_europe_camps_audit_v120.json" download>Франция и Испания · семейные программы и сметы</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text();anchor='<a href="downloads/STEM_swiss_camp_budgets_audit_v119.json"'
link='<a href="downloads/STEM_europe_camps_audit_v120.json" download>Франция / Испания: 7 новых досье и 8 смет ↓</a> · <a href="downloads/STEM_europe_camps_source_receipts_v120.json" download>Программы, тарифы и границы проверки ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps(dict(version=120,status='progress',new_dossiers=7,new_calendar_records=4,new_partial_budgets=8,events=len(now),dossiers=897,budgets=43,goal='active')))
