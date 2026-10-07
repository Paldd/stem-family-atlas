"""Evidence receipt for bounded European progress; preserve the worldwide goal."""
import hashlib, json, subprocess
from pathlib import Path
from camp_europe_v94 import UPDATED

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT.parent/'stem-family-atlas-work/camps-primary-v94'
BASE = '186b283a2b4ca00f6161bf1457b9fc0bc8fb624b'
before = json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d = json.loads((ROOT/'data/catalog.json').read_text()); c = d['camp_programmes']
old = {e['id']:e for e in before['events']}
oldp = {p['slug']:p for p in before['camp_programmes']['profiles']}
new = [e for e in d['events'] if e['id'] not in old]
changed = [e for e in d['events'] if e['id'] in old and e != old[e['id']]]
assert len(new)==2 and len(changed)==40
assert {e['camp_dossier_slug'] for e in changed}=={'les-elfes','la-garenne','village-leysin'}
assert c['counts']['dossiers']==622 and c['counts']['source_urls']==975
receipts = [q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(receipts)==24 and all(q.get('status')==200 for q in receipts)
scopes = {
 'elfes-summer-form':'Own enrol page and its actual Summer2027 PDF link retrieved; no fields filled or submission. HTML is not final basket/availability proof.',
 'elfes-summer-pdf':'Actual own-linked two-page Summer2027 form/contract; both pages visually read. Six cohorts, compulsory150/120week, included Shelter, optional180Robotics10+, linen/clothes distinction and Summer1000 cancellation deduction read. Winter/Spring conditions not replaced by Summer terms; language fee charging period and transfer unit still unconfirmed.',
 'village-stem':'Own STEM10–17 page: only two July2027 cohorts5500, SPIKE/gears/sensors/programming/teamwork and internal RobotWars. Kits supplied/remaincamp. Leysin rooms conflict with Salzburg/Austria excursions in samepage; no Austria travel promised. English technical teaching not stated.',
 'village-junior':'Own Junior7–9 page: four2027 cohorts5200/5500/5500/5100, general outdoor/adventure, ratio1:4 and staff certification operator claims. Language of instruction not stated. Different programme from STEM10+.',
 'village-prices':'Current own2027 price table relevant Junior and STEM rows read. Not every operator programme/course independently audited.',
 'village-parent':'Own Parent Guide2027 links to travel/conditions/Leysin booklet observed; linking from2027 context does not change PDF metadata2026 into final2027 contract.',
 'village-signup':'Read-only public form retrieved; optional accident/illness140CHF perchild/session and travel form≥30days read. English proficiency field not English teacher proof. No child data/Continue/account/submission.',
 'village-loyalty':'Own household-based loyalty tiers and eligible booking months read. Counts different summers, not numberofchildren/sessions; first summer no loyalty reduction. Manual team application after booking not immediate checkout rebate.',
 'village-leysin-booklet':'Actual14-page PDF with metadata Camp Information Booklet Switzerland2026. Relevant medical/insurance/supervision clauses read; page12 visually read. Under12 accompaniment has activity-park exception; not continuous1:1. Not all14pages audited or a confirmed2027 contract.',
 'village-travel':'Actual3-page undated Travel PDF; page2 visually read to resolve columns. Geneva100/200,Lausanne55/110; Salzburg100/200 andMunich150/300EUR. ExtraCHF215childnight. May1/May15 text conflict and form30day rule retained; not registration deadlines/current2027 tariff guarantee.',
 'village-conditions':'Actual1-page own-linked PDF, metadata ParentGuide2026; page1 visually read. Swiss1000credited deposit48h/May1 balance, cancellation phases, specialistprogramme change andcardfees read. Not accepted terms or definitive2027 contract.',
 'village-overview':'Own current Leysin overview: three-hour morning mainprogramme, age tracks, rooms/meals/activities and admissionfees on excursions read. Does not guarantee30hours STEM or English technical teaching.',
 'garenne-summer':'Own current2027 menu includes Robotics in5–9 and10–12, resolving old menu10+ conflict. Explicit form/contract8–12 still applies; menu group5–9 does not admit Oscar6–7 to Robotics.',
 'garenne-form':'Read-only own form: Robotics8–12/500/3sessions and insurance/pocket context. No fields/consent/signature/submission. A displayed option not confirmed available place.',
 'garenne-conditions':'Actual9-page Summer2027 contract. Relevant age/fee/inclusions and clauses read; pages4/8/9 visually read for500/3/8–12, medical10day, siblings10percent sameformat/session,65-day cancellation and28-day extras. Not all9pages independently audited/accepted; insurance charging-day count still unknown.',
 'garenne-workshop':'Actual4-page workshop PDF. Relevant8–12/possibleVEXIQV5/Python/Tinkercad/Fusion360/3D/speaker read. Page4 visually read: ThreeSessions heading vs twoSessions finalphrase on samepage. Possible projects not all guaranteed completed; no definite technical hours/English instructor/year-specific kit.',
 'ilc-prices':'Own undated pricepage itemised FUN/Adrenaline1/2weeks day/board, registration200stay, mandatory70weeklaundry for2weekstay, group350transfer1–2people and options. Two-child formula explicitly conditional; no2027 dated sessions or quote admitted.',
 'ilc-fun':'Own FUN6–9/15hweek EN/FR lessons and conversational camp practice, general alpine activities read. Embedded emptycalculator applicationfee0 not final invoice. Technical course not claimed.',
 'ilc-terms':'Own undated terms:1000CHF cancellation retention plus separately listed5/25/100percent, interaction unclear; not automatically summed or calleddeposit. Earlydeparture no refund, operatorcancelrefund stated; actual2027 applicability unresolved.',
 'ilc-faq':'Own FAQ relevant unaccompanied-minor travel context read; not all airline policy/insurance/availability verified.',
 'tecs-kids':'Own PuertoKids7–13, progressive English immersion/PBL, upto14dorm, bodydates withoutyear and1730button. Header2027 insufficient to assign year todates/price; no dated2027 rows admitted.',
 'tecs-catalogs':'Own current catalog page describes TECS2026 and lead-email/account access to brochure; no public2027 brochure obtained. No form/account/subscription.',
 'tecs-discounts':'Own discounts: early40until30Apr2026 expired; siblings25each/twochildren and combination mechanics. No automatic2027 applicability, new registrationdeadline or current discount deduction.',
 'tecs-consumer':'Own general consumerinformation identifies TheEnglishCentreSuppliersSL/nonofficialeducation; not a complete camprefundcontract or actual2027 quote.'}
for q in receipts:
 f=PRIMARY/(q['key']+'.pdf')
 if not f.exists(): f=PRIMARY/(q['key']+'.html')
 assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
 q.update(retrieval_method='direct_http',raw_filename=f.name,body_snapshot_retained=True,content_scope=scopes[q['key']])
 if f.suffix=='.pdf':
  info=subprocess.check_output(['/opt/homebrew/bin/pdfinfo',str(f)],text=True)
  q['pdf_metadata']={line.split(':',1)[0]:line.split(':',1)[1].strip() for line in info.splitlines() if line.startswith(('Title:','Pages:','CreationDate:','ModDate:'))}
oldurls={s['url'] for p in oldp.values() for s in p['sources']}
added=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls)
assert len(added)==10
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False)
countrycounts={s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','MYS','PHL','AUS','USA','CAN','CRI','MEX','BRA','CHL']}
checks=[
 'One new separate Village STEM10–17 dossier with only two July2027 cohorts; CP051/four old IDs retained and narrowed to Junior7–9. Six prior dossiers deepened;621 prior IDs/order and615 unrelated dossiers unchanged.',
 'Forty existing calendar rows explicitly corrected:26LesElfes season-aware references/fees,10LaGarenne resolved8–9 menu conflict,4Village Junior-only. All3081 other old rows, leagues/competitions/exhibitions/schools/history/familyroutes preserved. Two new familyICS; olddate/deadlineUIDs retained andno guessed dates/deadlines.',
 'LesElfes Summer2027 registration150+medical120/week mandatory, included Shelter6+ satisfies compulsory workshop.5140each/10280two at4750base excludesroad/options;1000crediteddeposit not addedtwice. Summer cancellationpolicy retains1000; Winter text/fees preserved pervariant. AXAliability1000deductible not mandatorysecondcharge.',
 'Village optional medical140/session and travel100/200/55/110 recorded withPDFyearlimits. Conditions andbooklet metadata2026 despite current2027 parentlink;May1/May15/30day travel conflict not registrationdeadline. Firstsummerfamily2children not loyaltytier. EN Junior/STEM not inferred; Austrianexcursioncopyconflict preserved.',
 'LaGarenne currentmenu includes5–9 Robotics, resolvingold10+ conflict. Concrete form/contract8–12/500/3 still excludesOscar6–7. PDFThreeSessions vs finaltwo on samepage4 retained. Insurance10/daycount unconfirmed, sibling10percent onlysameformat/session; shortoption not wholecamptechnicalintensive.',
 'ILC actual group350transfer1–2people, reg200stay andmandatorylaundry70week for2weekstay yield conditional17360twoFUNboard/17560withoneAdrenaline. Priceyearunknown; language-only700 not fullcampprice.1000cancelfee/percentinteraction unresolved, not crediteddeposit orautomaticsum.',
 'TECS7+ bodydates/yearprice notpromoted fromheader2027. Catalog2026/emailgate andexpiredApr30,2026discount recorded. Generalconsumerinfo notcamprefundcontract; nochild/contact/account/subscription supplied.',
 '24directprimaryretrievals/24HTTP200/0errors,6actualPDFs/relevantclauses and9visualpagechecks/renders. Rawretainedoutsidecheckout; publicexports paraphrases/URL/hash/errors only. Noform/message/payment/account/subscription/automation.',
 '622dossiers/37countries/975distinctdossierURLs/142familycomparisons;3123events/1792learningrows/2384familyICS/104exhibitICS.1329manageddated/69legacyreuse/39seasonwindows;249countries/82withrecords/0fullyaudited. Expandedworldwidegoal remainsactive.']
audit=dict(asof='2026-10-05',version=94,status='progress',scope='Deeper Switzerland/France/Spain programme contracts and family costs; one separated Swiss STEM track, not a complete Europe/world audit.',new_dossiers=1,new_operator_groups=0,deepened_dossiers=6,updated_dossiers=UPDATED,new_calendar_rows=2,new_family_ics=2,new_registration_deadline_ics=0,corrected_existing_event_ids=[e['id'] for e in changed],programme_dossiers=622,countries_with_dossiers=37,official_dossier_urls=975,country_dossier_counts=countrycounts,programme_slugs=['village-leysin-stem'],findings=c['gaps'][-3:],calendar=dict(events=3123,learning_records=1792,family_ics=2384,exhibition_ics=104,managed_dated_rows=1329,reused_legacy_events=69,season_windows=39),primary_retrievals=dict(direct_attempts=24,http200=24,errors=0,actual_pdfs=6,visual_page_checks=9,retained_page_renders=9),fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,next_priority='Continue all Switzerland/France/Spain/Europe andTaiwan/Singapore/Korea/Japan/Asia, USA/Canada/CostaRica/Mexico/LatinAmerica andotherworldcountries2026–27 general/thematic/boarding/day/familyprogrammes: datedowncohorts, seasoncontract, fullinvoice, exactDOB/actualschoolgrade, technicalhours/level, EN/ES/RUteaching, foreignintake andcurrentplaces. Preserve leagues/competitions/exhibitions/admission/schools/results5–10years/familyroutes;0countriesfullyaudited.')
def write(stem,value):
 text=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
 (ROOT/'data'/f'{stem}.json').write_text(text)
 (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(text)
write('europe-camp-audit-v94',audit)
write('europe-camp-source-receipts-v94',dict(asof='2026-10-05',version=94,scope='24 own direct pages/documents; relevant clauses/6PDFs/9visualpages, not every operator/country fully reviewed.',sources=receipts,dossier_source_urls_added=added,external_actions=external,notes=['RawHTML/PDF/renders outsidecheckout; publicexports paraphrases/URLs/hashes only.','PDFmetadata2026 and current2027link context retained independently. No datedcamp/deadline fromundatedbody or payment/travel/discount deadline.','Programme, availability, instructionlanguage, agefit andorganiseracceptance are distinct. No allcountry/worldwidecompletion claim.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=94:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',evidence='v93nativepublication succeeded;commit186b283a2b4ca00f6161bf1457b9fc0bc8fb624b;deploymentappgdep_6ac439a7c988819184bc9d88ee79166a. Expandedworldwideobjective preserved.')
plan['latest_validation']=dict(version=94,asof='2026-10-05',status='Independent primary/preservation/calendar verification; nativepublicationreceiptseparate',events=3123,camp_learning_records=1792,programme_dossiers=622,countries_with_dossiers=37,official_dossier_urls=975,family_ical=2384,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=countrycounts)
plan['europe_camp_programme_audit_v94']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=622,countries=37,swiss=86,generated_calendar_entries=1329,reused_legacy_events=69)
for q in plan['requirements']:
 if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:q['evidence']='v94:622programme/venue/formatdossiers37countries;one separatedSTEM+six deepened,2newcohorts/ICS,40explicitlycorrectedoldrows,975dossierURLs. Seasonfees/mandatoryversusoptional/agefit/PDFmetadata/units/conflicts retained; allcountry/worldwidecomplete notachieved.'
entry=dict(version=94,asof='2026-10-05',status='progress',scope=audit['scope'],new_dossiers=1,deepened_dossiers=6,new_calendar_rows=2,corrected_existing_calendar_rows=40,new_family_ics=2,official_primary_sources=10,not_complete_worldwide=True)
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=94]+[entry]
plan['next_research']=[audit['next_priority']];plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05';write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=93','?v=94').replace('data-ui-version="93"','data-ui-version="94"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_europe_camp_audit_v94.json" download>Европа: возраст, договор и семейная смета ↓</a> · <a href="downloads/STEM_europe_camp_source_receipts_v94.json" download>Первичные источники и годы PDF ↓</a> · '
anchor='<a href="downloads/STEM_americas_camp_audit_v93.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=622,new_dossiers=1,deepened_dossiers=6,corrected_rows=40,new_calendar_rows=2,new_family_ics=2,source_urls=975,goal='active')))
