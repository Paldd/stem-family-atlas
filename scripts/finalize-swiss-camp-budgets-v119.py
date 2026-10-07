"""Publishable evidence for selected Swiss budgets; the worldwide audit stays active."""
import collections,hashlib,json,subprocess
from camp_swiss_v119 import ROOT,BASE,CHECKED,NEW_IDS
P=ROOT.parent/'stem-family-atlas-work/camp-swiss-primary-v119'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
assert {k:v for k,v in d.items() if k!='camp_planning'}=={k:v for k,v in b.items() if k!='camp_planning'}
assert d['camp_planning']['offers'][:27]==b['camp_planning']['offers']
new=d['camp_planning']['offers'][27:];assert [q['id'] for q in new]==NEW_IDS
receipts=[q for f in sorted(P.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(receipts)==20 and sum(q.get('status')==200 for q in receipts)==19
sources=[]
for item in receipts:
 q=dict(item,checked=CHECKED,retrieval_method='direct_public_http',content_scope='Selected public programme, price and policy clauses. No whole-site, country or current intake audit.')
 if q.get('status')==200:
  ext='pdf' if (P/(q['key']+'.pdf')).exists() else 'html';name=q['key']+'.'+ext;raw=(P/name).read_bytes()
  assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
  q.update(raw_filename=name,body_snapshot_retained=True,content_status='selected_pdf_clauses' if ext=='pdf' else 'selected_html_clauses')
  if q['key']=='altitude-booking-day':q['content_scope']='Own readonly HTML calendar starts June2027; six-to-fourteen label and selected extras. Calendar classes are not accepted intake or reserved places; fee table elsewhere has no year.'
  if q['key']=='suisse-terms-pdf':q['content_scope']='Own currently linked six-page 2018 terms: selected payment, cancellation, insurance and confirmation clauses; not asserted to be the2027contract.'
  if q['key']=='suisse-policy-pdf':q['content_scope']='Own linked two-page IPID in2025folder, version1.0_11.23: selected insured-events, home-country GP registration and policy-scope clauses. Not full2027insurance documentation.'
 else:q.update(body_snapshot_retained=False,content_status='retrieval_error_not_content_evidence')
 sources.append(q)
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
cp=d['camp_programmes'];blocks=collections.Counter(q['block'] for q in d['events'])
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT')
expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert family==2770 and expo==104
audit=dict(version=119,asof=CHECKED,status='progress',scope='Selected Swiss day/boarding winter2026–27 and summer2027 family-budget scenarios. Existing programme dossier and calendar objects unchanged. Not a complete Switzerland or worldwide audit.',
 events=len(d['events']),competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],camp_learning_records=blocks['Лагеря'],
 programme_dossiers=len(cp['profiles']),countries_with_dossiers=39,official_dossier_urls=1398,editorial_scenarios=215,coverage_gaps=240,league_profiles=len(d['league_guide']['profiles']),
 budget_scenarios=35,budget_providers=19,budget_programme_dossiers=25,new_budget_scenarios=8,new_budget_ids=NEW_IDS,new_budget_brands=['Camp Suisse','Lovell','Lyceum Alpinum'],
 published_budget_components=[dict(id=q['id'],currency=q['currency'],amount=sum(q['base_by_child'].values())+sum(c['amount'] for c in q['required']),children=q['children'],lower_bound=q.get('price_basis')=='from',complete=False) for q in new],
 new_dossiers=0,updated_dossier_slugs=[],new_event_ids=[],updated_event_ids=[],unchanged_dossier_objects=890,unchanged_event_objects=3555,unchanged_prior_budget_objects=27,
 source_retrieval_attempts=20,direct_successful_bodies=19,retrieval_errors=1,pdfs_downloaded=4,pdf_pages_text_extracted=13,new_visual_pdf_checks=5,
 family_ical=family,exhibition_ical=expo,goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,
 checks=[
  'Camp Suisse day2027:5–17;200/day or1000/five weekdays;21Jun–13Aug seasonwindow notonepackage. Returnminibus20/day/child:2000bothbase or2200includingfive-daybothbus. Lunchactivitiesexcursions included; full languagecourse notinferred. Overnight120 notofferedwithoutyoungchildsleepovereligibility.',
  'Camp Suisse board2027:7–17,4400/two weeks. Matvey-only4400 excludesOscarcare; both8800 conditionalOscaralready7. FourSaturday-to-Saturdaysessions,15inclusivecalendardates not14nightsasserted. Childtransferonlyofficialhours/days. Parent100/adultGeneva→camp→Aigle notairportreturn.',
  'Camp Suisse500depositinbase notaddedagain,4weekbalance. Insuranceincludedclaim notaccepted2027coverage; currentlylinkedIPIDin2025folder requireshome-country GP registration andcoversspecifiedinsured-events, not everycancellation. Fullpolicyafterregistration,2018termsstilllinked; CostaRicaresidence/MexRFcitizenshipapplicabilityunknown. NoinventedUK-onlyexclusion.',
  'Lovell2026/27 PDF5–16/allnationalities,websiteboard5–15 upperconflictdoesnotchangecurrentchildrenlowergate. Day1900+50registration=3900both;board2600+100=5400bothperweek. 1000advanceperchildinsidebase,notextra. Medicalcertificateandbalance30days;registrationnonrefund;written30daycancellationdepositrule, withdrawalnoratediscount.',
  'Lovellboardweeks5–7(10–30Jan)explicitnoboarding:excludedfrom11boardperiods;day14MoFrweeksseparate. IncludedlessonsskipassENorFR/supply/excursiontransport; personalgearinsuranceairportsdoorbusnotincluded. Languageversusafternoonchoice, PDFTshirtexcludedvswebincluded,dayendtimeconflictretained. Nofulldualprogramme/gearpriceorSTEMintensiveinvented.',
  'LyceumJunior6–9 only:Oscar6–7candidate,Matvey9–10conditionalwhile9. FourJuly2027MoFrweeks,1000perweek/child=2000both;16EN/DElessons,lunch/materials08:30–16. Localpick-upserviceclaimedincludedbutroute/withwithoutconfirm; noairporttransferorDigitalSkillsboardinginferred. Parentsprovidehealthaccidentliabilityinsurance;30/29–15/14dayrefundrules.',
  'LaGarenneWinterIntegration5–14:from7500day/7950board minimum2weeks =>from15000/15900both. Fivepublishedblocks;dayonlyMoFr,last7–19Marshorterthan14calendardaysandnosecondweekski. Ordinaryschoolintegrationandminimum2ski/week,notEnglish+Ski8+/SuperSki8+. Winterextrasfulltermsnightcarelanguageplacementunknown;nosummer10%siblingdiscountor500depositreused.',
  'Altitude own serverdaybookingJune2027withstartable28Jun and6–14label,daypageyearless28Jun–13Aug975/950; residentialyearless2950/5550/etc. Calendar notproof of seats or year-boundprice. No new2027budget or datedeventcreated from ambiguous association. Termsinsuranceabsent,20%deposit/May31balance/cancellation30/14 boundaries stayconditional.',
  'All3555events890profiles27priorbudgetobjects,leagues/exhibitions/schools/history/routes preserved. Eightpartialscenariosfourbrands(three newlybudgetedbrands),nooverallcampqualityranking. Structured unknowns empty≠zero; depositsnotdoubled; frompricesvisiblymarked;seasonwindowdistinguished. Worldwideobjectiveactive;0fullyauditedcountries.'
 ])
def write(stem,value):
 s=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('swiss-camp-budgets-audit-v119',audit)
write('swiss-camp-budget-source-receipts-v119',dict(version=119,asof=CHECKED,scope=audit['scope'],sources=sources,
 visual_pdf_pages={'lovell-pdf':[1,2],'lyceum-pdf':[1],'suisse-policy-pdf':[1],'suisse-terms-pdf':[2]},new_visual_pdf_checks=5,
 external_actions=external,primary_reader_limits='Selected public pages and PDF clauses only. Raw bodies/rendered pages retained outside website source. No full2027intake/insurance/invoice confirmation.'))
sm=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text());jm=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=119:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native118 succeeded2026-10-06T10:29:54.360855Z; commit '+BASE+'; deployment appgdep_6ac4cd8fbe8c8191b50e96f98e6055d5. Worldwide objective active.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','budget_providers','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected Swiss price/policy clauses and portable database verified; native publication separate.'
plan['swiss_camp_budget_audit_v119']=audit;plan['complete_database_download']=sm;plan['complete_json_download']=jm
for q in plan['requirements']:
 if q['id']=='camp_full_pricing':q['evidence']='v119:35 partial scenarios/19brands/25dossiers, including8newSwissday/boardingbudgets. Sixexistingdossiersnewlypriced. 27priorofferobjectsunchanged; fromprices,weeklygates,gearinsurance/travelseparate,fullorganizerinvoiceunknown.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=119]+[dict(version=119,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=0,updated_dossiers=0,new_calendar_rows=0,new_budget_scenarios=8,official_primary_retrieval_attempts=20,pdfs_downloaded=4,new_visual_pdf_checks=5,not_complete_worldwide=True)]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=118','?v=119').replace('data-ui-version="118"','data-ui-version="119"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_swiss_camp_budgets_audit_v119.json" download>Швейцария · летние и зимние семейные сметы</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text();anchor='<a href="downloads/STEM_latam_camps_audit_v117.json"'
link='<a href="downloads/STEM_swiss_camp_budgets_audit_v119.json" download>Швейцария: 8 новых летних и зимних смет ↓</a> · <a href="downloads/STEM_swiss_camp_budget_source_receipts_v119.json" download>Тарифы, договоры и границы проверки ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps(dict(version=119,status='progress',new_partial_budgets=8,total_partial_budgets=35,all_events_unchanged=3555,all_dossiers_unchanged=890,goal='active')))
