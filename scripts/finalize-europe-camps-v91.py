"""Record the bounded European pass without declaring a worldwide audit complete."""
import hashlib,json,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v91'
BASE='0465a462d6a769284b883c05d4e8552c9e345da9'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
op={q['slug']:q for q in b['camp_programmes']['profiles']};old={e['id']:e for e in b['events']}
fresh=[q for q in c['profiles'] if q['slug'] not in op]
changed=[e['id'] for e in d['events'] if e['id'] in old and e!=old[e['id']]]
assert len(fresh)==7 and len(changed)==2
assert all(old[i].get('camp_dossier_slug')=='las' for i in changed)
assert c['counts']['dossiers']==601 and c['counts']['source_urls']==918
receipts=[v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts)==43 and sum(q.get('status')==200 for q in receipts)==42
scopes={
 'las-families':'Guessed path returned404; not evidence of a parent-family camp. Actual residential page distinguishes counselor-led child Families.',
 'action-program-pdf':'HTML iframe wrapper, not a PDF. Its observed source was followed separately; wrapper not counted as a read programme PDF.',
 'action-program-body-pdf':'One-page programme PDF read and visually checked: actual October2025, age8–14. Not dates for live2026 table.',
 'hes-catalog-pdf':'Relevant catalogue2026 pages3,6,25 read/visually checked: venue/ages, sample daily schedule, robotics content.29-page catalogue not declared fully read.',
 'hes-guide-pdf':'Single-page practical guide read/visually checked: minimum group4, laundry5EUR, staff medication, visits/phone rules. Not a price2027 contract.',
 'faisl-brochure':'Two-page visible2026 brochure checked against extracted text. Hidden older English/grade/date lines not evidence of current language/admission/calendar.',
 'faisl-form-pdf':'Programme2026 dates/fees/payment/media/park sections and page1 visually read; blank SEPA payment form not completed or accepted.',
 'las-flyer-pdf':'Both pages visually read; flyer cover2027 and page2 Junior9–12/Senior13–16 and daily schedule. Not course-level prerequisites or instruction language.',
 'las-terms-pdf':'Payment/refund/inclusions and page1 visually read, supporting clauses read: actualGeneralBookingConditions2026, not contract2027. Remaining behaviour text not claimed a full legal audit.',
 'action-cgv-pdf':'Relevant page1 payment/cancellation/insurance clauses visually read: printed economic baseline8April2019. Not current2026 contract confirmation; flexibleweb conflict preserved.',
 'ischool-terms':'Annual after-school terms2026–27, not summer-camp cancellation. Course tuition/membership/media terms not imported as camp fee/refund.',
 'ischool-faq':'Provider/programme context; Spanish page/WRO collaboration not proof of teaching language or independently verified camp competition wins.',
 'faisl-terms':'Website terms, not summer-camp refund; distinct from actualblank programme form.',
 'action-map':'Discovery index only; not all1500 listed offers audited.',
 'action-home':'Marketing minimum6 cannot substitute actualprogramme7–14/table8–14.',
 'action-bretagne':'Actual Santec/BonVent programme read:16hoursENteaching vs2hoursMon–Fri/lengthunspecified. Page says nocurrentstay; no open2027 programme admitted.',
 'action-winter':'Actual WinterAuvergne English/ski description read, but page says nocurrentstay; dates/price/age not inferred.',
 'action-roches':'Title Roches de Scoeux but body VillageEspaceNatureChamberet; nocurrentstay. Not a confirmedfuturevenue/dates.',
 'prefleuri-summer':'Relevant Summer2026 age/language/content read; previous separatelychecked schoolcalendar2027 retained. Not proof of new summer2027 fee.',
 'hes-price-detail':'Actualredirect /catalogos-0 own2026 numeric fee/formula read; old transport dates conflict with2026 catalogue. Not all-in2027 price.',
 'technomatic-camps':'ActualEnglishcreative/robotics programme2026 read; captionregionalVEX result lacks event/year/team verification. Not a top-ranked school.',
}
for q in receipts:
 if q.get('status')==200:
  files=[PRIMARY/(q['key']+suffix) for suffix in ['.pdf','.html']]
  f=next(f for f in files if f.exists())
  assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
  q.update(raw_filename=f.name,body_snapshot_retained=True,content_scope=scopes.get(q['key'],'Relevant ownprogramme/age/date/price/content sections read; language, foreign admission, completeoperator/country coverage and2027 availability not inferred.'))
oldurls={s['url'] for q in op.values() for s in q['sources']}
added=sorted({s['url'] for q in c['profiles'] for s in q['sources']}-oldurls);assert len(added)==25
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False)
isos=['CHE','FRA','ESP','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','MYS','USA','CAN','CRI','MEX','BRA','CHL']
byiso={s:sum(q['iso']==s for q in c['profiles']) for s in isos}
checks=[
 '7 new programme/track dossiers across4 newoperators (iSchool,Technomatic,FAI,Action) plus existingLAStrack;3 existingdossiers deepened (LAS,Préfleuri,NATUK). All594priorIDs/order and591completeprofiles unchanged. All3071prior events retained;only2LASrows updated in age/language/course/contract. Existing dates/IDs preserved.',
 'LAS own2027 flyer visiblyJunior9–12/Senior13–16; morning09–12 is a dailyblock, not15hoursPython/AI perweek. CurrentAI&Python track builds owninteractivePythonapp/sourcecode, prerequisite/junioravailability/technicalENunknown. ResidentialFamilies are childgroups, not a parentcamp. RegisterComingSoon, ownprice9500CHF3weeks/16750two sessions, Leadership+500, optionalEurope+1500, offdateGeneva+350. Linkedterms are2026/non-refundable/2000deposit/15May2026balance/UM150 perflight, not confirmed2027 contract. Mainstay andAItrack alternatives, not2operators/trips.',
 'Préfleuri current fees still2026:5–14board5550/8150/9990/12235/14400 for2–6weeks, day3250/4770/6240/7650/9000. 10percent4weeks included vs secondchild10percent, onlyone reduction. EN/FRlessons from6, not fullcampEnglish. Terms1000deposit vsfullreservationpayment conflict; summer60–45fee1000/<45full, winter>60fee1000/<60full; exactboundaries and summer>60unknown. Medicaltravel/death creditfuture notcashrefund; daymeal/insurance separate.',
 'NATUK/HES existingoperator, actuallocationTraineraEsterriLleidaSpain from2026ownlocation/catalogue, oldEuroSki notseparateAndorra. Robotics6–16, afternoon16–19sample; minimum4 orreplacement, not17robots perchild/week. HES2026formula150registration+base655/1195/1750+robotics50/week+morning:oneweek855Englishclasses/905Discovery/980ActiveAdventure. Not2027 orall-in. Airport70/140minimum4, laundryincludedvs5/load, hotelroom2–4vs3–6, transport29–19vsbrochure28–18 conflicts preserved;dayresidentsonly.',
 'iSchool Constructores6–8/12capacity, Creadores9+/recommended9–12/10capacity, Minecraft8+intermediate/16capacity are distinctage/content programmes, not3operators. 25hours/09–14/free08–15care; numericpopupgeneral139/239/335 vsaffiliate125/225/320. Annual405/423terms notsummerfee/refund. Internalcombatrobotleague andWROcollaboration notworldmedals. OwnpageSpanish notteachingES/EN; no2027 dates.',
 'TechnomaticMálaga own2026creativecamp6–17 explicitallENincludingrobotics, alllevels withoptionalB1/B2/C1 examgroups;27–31July/3–7Aug archival. Half95/170one/twoweeks, full125/215;second50/70perweek =>145/195twochildrenoneweek, two-weekstackingunknown. Extraafternoon10/day; lunch/VAT/refund/hardwaregiftunknown. CaptionregionalVEX1st not independentlyverifiedresult/qualifier.',
 'FAI/RockboticSalamanca ownvisible2026PDF/form:40EUR2days/70EURweek, sixpastblocks25June–31July,08–15PDFvs08–14web. PDF hiddenolderEnglish/Primaria1–3/July–August lines absentvisually, notcampteaching/admission/date evidence. Webstrict>6, mininclusive6/upperageunknown; Spanishsite/OxfordexamcentrenotEnglishcamp. WeeklySEPA/media/parkconsent read butnotaccepted; futuredateprice/refundunknown. All8pastTechnomatic/FAI intervalsexcludedfromfuturecatalogue/ICS.',
 'ActionSaintPardoux live18–24/25–31Oct2026 table8–10/11–14 vscard7–14;Matveyconditional/Oscarlater. FullEnglishcreativeimmersionwithouttraditionalclasses; Wizard5halfdaysoption noteveryone. Ownpricequote, aggregatorMissionRobotique740EURexcluded. Chabannes59beds/3–4rooms/4meals/staff24h, possibleMeymac. LinkedPDF2025, CGVeconomicbaseline2019 versuscurrentflexibleweb1month/noairtransport/freecancellation/balance1month; currentcohortcontractunknown. Bretagne/WinterAuvergne/Roches saynocurrentstay; notopen2027.',
 '601dossiers/36countries/918unique dossierURLs,85Swiss/49French/52Spanish;132familycomparisons.4newfuturecataloguerows/4familyICS;3075events/1744camp-learningrows/2324familyICS/104exhibitionICS.1281manageddated/69legacyreuse/39windows.43directattempts42HTTP200/1error,8actualPDFs (relevantscopes and12visualpagechecks, not8wholecontracts).249worldcountries/82withrecords/0fullyaudited. Worldwideexpandedgoal active; noexternalmessages/forms/accounts/payments/automations.'
]
audit=dict(asof='2026-10-05',version=91,status='progress',scope='Switzerland/France/Spain deeper programme/contract/age/language evidence, including visible PDF versus stale textlayer. Worldwide task remains active.',new_dossiers=7,new_operator_groups=4,operator_groups_including_existing_deepening=7,new_calendar_rows=4,new_family_ics=4,updated_dossiers=['las','prefleuri','natuk-robotics'],corrected_existing_event_ids=changed,programme_dossiers=601,countries_with_dossiers=36,official_dossier_urls=918,country_dossier_counts=byiso,programme_slugs=[q['slug'] for q in fresh],findings=c['gaps'][-3:],calendar=dict(events=3075,learning_records=1744,family_ics=2324,exhibition_ics=104,managed_dated_rows=1281,reused_legacy_events=69,season_windows=39),fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,next_priority='Continue allEurope/Switzerland/France/Spain, Taiwan/Singapore/Korea/Japan/Asia, USA/Canada/CostaRica/Mexico/LatinAmerica and allworld2026–27 general/technical camps; actualDOB/grades/language/foreignintake/availability/fullinvoice/contracts, schools/results/history, competitions/leagues/exhibitions and familyroutes.')
def write(stem,v):
 t=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(t)
 (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(t)
write('europe-camp-audit-v91',audit)
write('europe-camp-source-receipts-v91',dict(asof='2026-10-05',version=91,scope='43 directattempts/42HTTP200/1error;8actualPDFs with relevantsection scopes and12visualpagechecks. OneHTMLiframewrapper separately followed; not a completedPDFread or wholecountry/operator audit.',sources=receipts,dossier_source_urls_added=added,external_actions=external,notes=['RawHTML/PDF/renders retained outsidecheckout; publicexports onlyparaphrases/URLs/hashes/errors. Nooriginalcampphotos reused.','VisiblePDFversusextractedstaletext separated, dates/fees/English website/actualcourse language/annualterms/operatingavailability notinferred. Worldcoverage stillactive.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=91:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',evidence='v90nativepublication succeeded;commit0465a462d6a769284b883c05d4e8552c9e345da9;deploymentappgdep_6ac4252e814c8191b300b3460d7df144. Worldwide expanded scope retained.')
plan['latest_validation']=dict(version=91,asof='2026-10-05',status='Independent primary/preservation/calendar verification; nativepublication receipt separate',events=3075,camp_learning_records=1744,programme_dossiers=601,countries_with_dossiers=36,official_dossier_urls=918,family_ical=2324,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=byiso)
plan['europe_camp_programme_audit_v91']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=601,countries=36,swiss=85,generated_calendar_entries=1281,reused_legacy_events=69)
for q in plan['requirements']:
 if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:q['evidence']='v91:601programme/venue/formatdossiers36countries;7new+3deepened,4newfuturecalendarrows/4familyICS,918dossierURLs. Ownage/language/fees/contracts/visiblePDF/programmeavailability; worldwidecomplete notachieved.'
entry=dict(version=91,asof='2026-10-05',status='progress',scope=audit['scope'],new_dossiers=7,deepened_dossiers=3,new_calendar_rows=4,new_family_ics=4,official_primary_sources=25,not_complete_worldwide=True)
plan.setdefault('research_passes',[])[:]=[q for q in plan.get('research_passes',[]) if q.get('version')!=91]+[entry]
plan['next_research']=[audit['next_priority']];plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05';write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=90','?v=91').replace('data-ui-version="90"','data-ui-version="91"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_europe_camp_audit_v91.json" download>Европа: программы, младшие группы и полный счёт ↓</a> · <a href="downloads/STEM_europe_camp_source_receipts_v91.json" download>Источники и границы проверки ↓</a> · '
anchor='<a href="downloads/STEM_americas_camp_audit_v90.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=601,new_dossiers=7,deepened_dossiers=3,new_calendar_rows=4,new_family_ics=4,source_urls=918,goal='active')))
