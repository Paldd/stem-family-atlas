"""Publish selected-source audit without claiming worldwide completion."""
import collections,hashlib,json,subprocess
from camp_asia_v121 import ROOT,BASE,CHECKED,NEW,ROBOTO
P=ROOT.parent/'stem-family-atlas-work/camp-asia-primary-v121'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
newids=sorted(now.keys()-old.keys());cp=d['camp_programmes'];offers=d['camp_planning']['offers']
assert len(newids)==40 and all(now[k]==q for k,q in old.items())
assert len(cp['profiles'])==915 and [q['slug'] for q in cp['profiles'][897:]]==NEW
assert cp['profiles'][:897]==b['camp_programmes']['profiles'] and d['camp_planning']==b['camp_planning']
sources=[]
for f in sorted(P.glob('receipt-*.json')):
 for item in json.loads(f.read_text()):
  q=dict(item,checked=CHECKED,retrieval_method='direct_public_http',content_scope='Selected programme, age, language, price and policy clauses or discovery links. Not a whole-site/country or accepted intake audit.')
  if q.get('status')==200:
   ext='pdf' if (P/(q['key']+'.pdf')).exists() else 'html';name=q['key']+'.'+ext;raw=(P/name).read_bytes()
   assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
   q.update(raw_filename=name,body_snapshot_retained=True,content_status='selected_pdf_clauses_or_title' if ext=='pdf' else 'selected_html_clauses_or_discovery')
  else:q.update(body_snapshot_retained=False,content_status='retrieval_error_not_content_evidence')
  sources.append(q)
assert len(sources)==45 and sum(q.get('status')==200 for q in sources)==31
pdfs=json.loads((P/'pdf-extraction-index.json').read_text())
visual={'malvern-bc-pdf':[1,2,6,7],'csa-dec-pdf':[1],'malvern-arts-current-pdf':[8,9],'malvern-orchestra-current-pdf':[8,9],'malvern-musical-current-pdf':[8,9]}
visual_files=[]
for key,pages in visual.items():
 for page in pages:
  name=f'{key}-{page:02}.jpg' if 'current-pdf' in key else f'{key}-visual-{page}.png'
  assert (P/name).stat().st_size>0;visual_files.append(name)
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
blocks=collections.Counter(q['block'] for q in now.values())
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT')
expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert (family,expo)==(2814,104)
audit=dict(version=121,asof=CHECKED,status='progress',scope='Selected new Taiwan, Singapore, Japan and South Korea programme dossiers. Forty Nov/Dec2026 Roboto course-week records; archival or incomplete programmes do not create new2027 dates. Not all Asian/worldwide camps or a world-ranking claim.',
 events=len(now),competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],camp_learning_records=blocks['Лагеря'],programme_dossiers=915,countries_with_dossiers=39,official_dossier_urls=1437,editorial_scenarios=221,coverage_gaps=250,league_profiles=len(d['league_guide']['profiles']),
 budget_scenarios=43,budget_providers=21,budget_programme_dossiers=len({q['slug'] for q in offers}),new_budget_scenarios=0,new_dossiers=18,new_dossier_slugs=NEW,
 new_programme_brands=['Roboto Coding Academy','Taipei Kids Academy','One Step Initiative','Malvern College Tokyo / British Council','Cognitive Systems Academy','Connected Jeju Global IT'],updated_dossier_slugs=[],new_event_ids=newids,updated_event_ids=[],unchanged_dossier_objects=897,unchanged_event_objects=3559,unchanged_prior_budget_objects=43,
 source_retrieval_attempts=45,direct_successful_bodies=31,retrieval_errors=14,pdf_download_files=14,unique_pdf_sha256=13,pdf_downloaded_page_instances=132,pdf_embedded_text_page_instances=80,pdf_ocr_page_instances=40,new_visual_pdf_checks=len(visual_files),family_ical=family,exhibition_ical=expo,goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,
 ui_fix='Archive status no longer hardcodes2026 when a dossier is2025; partial_2026 now has a visible status, filter option and shareable URL parser. All existing43budgetoffer objects and budget interactions unchanged.',checks=[
  'Roboto ten tracks are one operator, not ten independent top camps. Four dates per track, with one record per course-week and two venue choices; no doubled campus capacity. Ages7–8 vs9–12 separate: Matvey8–9 requires exact age on start, Oscar5–6 below7 for all current2026 dates. General FAQ5+ is not holiday acceptance.2/3/5 full days vs5 half days, lunch only explicitly for full days. Creator programmes do not claim physical robotics. JuniorCoder structured day plan does not allocate a separate AI lesson despite general promotional AI wording.',
  'Roboto current November/December own-course reader bodies establish dates, normal/early prices and selected curriculum; directHTTP406 retained as failure, not direct content success. JuniorInventor first cached June body superseded by fresh own-course November/December clauses. Dollar currencycode, English teaching, discount expiry, holiday-specific laptop/rental/refund, foreign intake and seat not established. Weekly FAQratio1:3 and laptop rules not automatically transferred to camp ratio1:4–6.',
  'TaipeiKids own current ZH theme-camps body confirms3–12, max16, coreEN and20%Chinese specialistart, day08–16:30 with pickupuntil18, halfday08–12:30. OldENsummer2026 URL404 with primaryreaderbody remains archival discovery. Jan/Feb2026 and Jul/Aug2026 all past; no2027dates. Basefee not established, thirdparty5100–13800 not imported; NT1000admin/NT1200withinmonthsession cancellation deductions are not a base tuition.',
  'OneStep bilingualmaker12–16 is future-age pathway for both. Free pilotJuly2026 only: models/electronics,3Dgame andpaperLEDcircuits with takehomecraft; no invented2027freeplaces or currentchild recommendation. Learning-needs/photo-consent questionnaires not submitted or accepted.',
  'MalvernTokyo school + ownlinkedPDFs separate Arts5–11/Prep1–6, Orchestra8–12/Prep4–FY1, Musical10–18/Prep6+, BC6–9. Firstthree summer2026closedFull; no2027seats. Arts/orchestra88000JPY/5days, musical176000/2weeks, extra12100externalregistration whosefamily/childunit remainsunknown, lunch5500/week. Refund7May2026cutoff archived. Englishcommunicationaim is not every-classEnglishpromise and UKMalvern robotics syllabus not applied to Tokyo.',
  'BCownTokyoPDF21–24Jul2026fourdays and27–31Julfive: nonMCT75600/92000JPY, optionallunch4400/5500; MCTdiscountnotexternalfamilyprice. ENmorning/Clubs explicit, min12/max16, reading/writinglevels separate. Matvey2027onlywhile9 ifmax9remains;Oscar6–7 provisionalfuture. OwnPDF dates override weekdaytypos in familydirectory. Historicalcancel0/30/70/100% not2027contract.',
  'CSADecember2026ownHTML7–12 vs linkedSpacePDFMayJune2026/7–18; eightotherworkshopPDFs7–14/1–2hrs do not broaden December.2day240min/3day360min/5day600min not full childcare days. Dollar299/416/554first20/715normal currency/availability unknown; noexactdates/venue, no dated calendar rows. InternalCSAmedals/FLLtrainers/DSA/MIT/NASA references not independently verifiedworldleaguewins/admission/partnership. Digitalrefundpolicy not physicalcampcontract.',
  'ConnectedJeju ownRUprogramme andENseminar5–12, parentrequired, EnglishSTEAM/coding/3D, familyresort; onlyJul13–Aug2,2025. Russianpage notRussianclass. No2026–27newseason/price/cancellation established. Distinct from existingSMIS/Gamjawinterprogrammes. HappyKidsregularDay/ASLA andSpanishClubtestimonial not seasonal camp evidence, retainedgapwithoutnewflimsydossier.',
  'All3559prior event,897prior programme,43prior budget objects preserved. Worldwidecompetitions/exhibitions/leagues/permanentschools/results/routes remain. FullportableJSON/SQLite preserved; unknown mandatory amounts remain unknown.0fullyauditedcountries, goalactive.'
 ])
def write(stem,v):
 s=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('asia-camps-audit-v121',audit)
reader=[dict(url='https://roboto.sg/holiday-camp-'+q[0],checked=CHECKED,status='selected_current_primary_reader_clauses',direct_http_error='406; no direct body snapshot') for q in ROBOTO]
reader += [dict(url='https://roboto.sg/holiday-camp',status='selected_current_primary_reader_clauses',direct_http_error='406'),dict(url='https://roboto.sg/faq',status='selected_primary_reader_weekly_clauses_not_holiday_terms',direct_http_error='406'),dict(url='https://tka.com.tw/en/summer-camp-2026/',status='selected_primary_reader_archive2026',direct_http_error='404; current own ZHpage directly captured')]
write('asia-camps-source-receipts-v121',dict(version=121,asof=CHECKED,scope=audit['scope'],sources=sources,web_reader=reader,private_reader_files=['web-reader-1.json','web-reader-2.json','web-reader-3.json'],pdf_extraction=pdfs,visual_pdf_pages=visual,visual_pdf_files=visual_files,new_visual_pdf_checks=len(visual_files),external_actions=external,
 primary_reader_limits='Selected clauses, titles and linked brochures; raw pages/reader captures/OCR/rendered PDF pages retained outside source. Eight CSA workshop PDF titles are discovery, not a new fullcamp audit. Malvern three image PDFs have40 OCR pages but only selected age/price pages visually checked. No whole website/country, accepted foreign intake, reserved seat or fullinvoice confirmation.'))
sm=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text());jm=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=121:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native120 succeeded2026-10-06T11:29:58.262814Z; commit '+BASE+'; deployment appgdep_6ac4db99640881918b714a2e246f67ea. Worldwide objective active.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','budget_providers','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected Asian primary clauses and complete portable database checked; native publication separate.'
plan['asia_camp_programme_audit_v121']=audit;plan['complete_database_download']=sm;plan['complete_json_download']=jm
for q in plan['requirements']:
 if q['id']=='unified_database':q['evidence']='v121:3599 events/915 programme dossiers/39 countries/1437 URLs;18 new Asian dossiers and40 RobotoNovDec2026course-week rows;every3559prior event/897priorprofile preserved,fullJSON/SQLiteZIP.'
 elif q['id'] in ['camps','family_top_picks']:q['evidence']='v121:915 dossiers/39 countries/221 editorial scenarios;TWNEN+ZH,SGPcurrentagegroups,JPNartsandEN,KORfamilyarchive. No independentworldranking or all-countrycompletion claim. Worldwidefocus includes allgeneral/thematic/STEMday/boarding/family2026–27 EN/ES/RU.'
 elif q['id']=='camp_full_pricing':q['evidence']='v121:43 existingpartialscenarios/21brands/33dossiers preserved. NewTokyo2026 archivedfees includeexternalregistration/lunch. Roboto/CSA dollars lackconfirmedcurrency/contract, notnew2027familybudget. Unknownmandatoryexpenses remainunknown.'
 elif q['id']=='camp_calendar_2026_2027':q['evidence']='v121:40 preciseRobotoNovemberDecember2026course-week rows,centrechoice notdoublecount;familyICS2814/expo104. No invented2027TKA/Malvern/OneStep/Connecteddates or CSAmonthasday. PriorUID/content preserved.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=121]+[dict(version=121,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=18,updated_dossiers=0,new_calendar_rows=40,new_budget_scenarios=0,official_primary_retrieval_attempts=45,pdf_download_files=14,unique_pdf_sha256=13,new_visual_pdf_checks=len(visual_files),not_complete_worldwide=True)]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=120','?v=121').replace('data-ui-version="120"','data-ui-version="121"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_asia_camps_audit_v121.json" download>Азия · ближайшие треки и новые досье</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text();anchor='<a href="downloads/STEM_europe_camps_audit_v120.json"'
link='<a href="downloads/STEM_asia_camps_audit_v121.json" download>Азия: 18 новых досье и 40 датированных вариантов ↓</a> · <a href="downloads/STEM_asia_camps_source_receipts_v121.json" download>Программы и границы проверки ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps(dict(version=121,status='progress',new_dossiers=18,new_calendar_records=40,events=len(now),dossiers=915,budgets=43,goal='active')))
