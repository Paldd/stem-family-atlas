"""Public audit receipt; raw primary snapshots stay outside the repository."""
import collections,hashlib,json,subprocess
from camp_europe_v124 import ROOT,BASE,CHECKED,NEW,NEW_IDS
P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v124'
d=json.loads((ROOT/'data/catalog.json').read_text());b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
cp=d['camp_programmes'];old={x['id']:x for x in b['events']};now={x['id']:x for x in d['events']}
assert len(now)==3667 and len(cp['profiles'])==966 and cp['profiles'][:950]==b['camp_programmes']['profiles']
assert {x['slug'] for x in cp['profiles'][950:]}==set(NEW) and all(now[k]==v for k,v in old.items())
assert d['camp_planning']['offers'][:43]==b['camp_planning']['offers'] and len(d['camp_planning']['offers'])==46
sources=[]
for f in sorted(P.glob('receipt-*.json')):
 for x in json.loads(f.read_text()):
  q=dict(x,checked=CHECKED,retrieval_method='direct_public_http',content_scope='Selected primary programme, age, teaching-language, housing, fee, timetable and cancellation clauses; not entire sites or countries.')
  if q.get('status')==200:
   name=q['key']+('.pdf' if (P/(q['key']+'.pdf')).exists() else '.html');raw=(P/name).read_bytes()
   assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
   q.update(raw_filename=name,body_snapshot_retained=True,content_status='selected_pdf_clauses' if name.endswith('.pdf') else 'selected_html_clauses_or_discovery')
  else:q.update(body_snapshot_retained=False,content_status='retrieval_error_not_content_evidence',resolution='Mistyped EIB PDF path corrected with exact primary search URL; corrected retrieval succeeded200.')
  sources.append(q)
assert len(sources)==28 and sum(q.get('status')==200 for q in sources)==27
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
blocks=collections.Counter(x['block'] for x in d['events'])
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT');expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert (family,expo)==(2882,104)
checks=[
 'IIL fresh direct October2026 catalogue supersedes cached summer reader. Six curricula of one operator; seven precise October intervals. AI8–13 five mornings350CHF; Junior3–6 week550 not checkout0; days125, fullweekcare625, two separate days250/290withcare. LEGO5–7 two afternoons110, chemistry8–13 two afternoons120, dance6–9 five mornings300, pBuzz6–9 afternoons275. AM-only no on-site lunch;105/week only with separate PMcamp. Specific two-day latecare30 differs from general20/day. EN/FR camp_life kept separate from guaranteed EN subject instructor. Foreign health/accident/liability cover required. French CGC binding; refund thresholds and medical cancellations explicit.',
 'Simply holiday camps explicitly taught EN. Thriller7–11 five days09–16,595CHF; ZürichOct12–16 and VersoixOct19–23. Year2026 comes from own linked current2026–27 portal, labelled published_rule rather than an unqualified printed-year session. Mini4–6 halfday, old cutoff1Sep2025 not2027; separate HalloweenStudio45CHF/two hours not a week camp and no exact calendar date. Annualtuition and25%WestEndTripdeposit not campfees. Own summer cancellation clauses not automatically an autumn-specific contract.',
 'LNE Paris camp3–7 versus generalactivity2–8/school2–6. Archived2025–26 standard500/300EURfull/half, Aprilfourdays400/250; lunchbox. Geneva own6pagePDF external4+preschool/primary versus website3–7, Matveyage unknown until reconciled. External630 not school600; lunch+AMsnack, ownPMsnack, no prorata for3–4days. EN/FR teaching explicit, archived dates never imported as future2027.',
 'MUNCYT15page official2026PDF text extracted; selected three-group curricula and contract clauses read, Electrones and Protones timetable pages visually checked.34total divided three completed2025–26gradegroups. InfantilmobileLEGOvehicle is mechanics; primary1–3general science;4–6RoboMakers introduction is part of DescubreII, not a full robotics-intensive week. Own announcement170EUR/week and conditional20%nonstackable discount. Spanish document not an explicit instructor-language guarantee; free Coruña workshops not paid Alcobendas camp. Reservation/payment/document instructions recorded, not executed.',
 'OSI Swiss drone course explicitly offers English/French, age7–12, KuspoLenk2/4/8bed rooms, piloting/nature field projects; no public2027date/fullfee in selected course. Oscaronlyafter7. ProvenceJunior specifically Français; EN/RU navigation not teaching evidence.7–10title versus7–9/10–13/families body retained; old2019kitlists/2022scenario not current2027syllabus. Public user comments/spam ignored as quality evidence. No account created.',
 'SwissTecLadies own camp: girls12–15 AND schooledSwitzerland, French;Oct19–23Avenches,100CHFday/250boarding with listedmeals/activity,50%CarteCultureconditional. Both boys noteligible. Old31Aug partnerdeadline versus booking links retained as gap, not a new family-accessible recommendation.',
 'EIBLaJonchère own onepagePDF visually checked: science/media/baking3–11 bilingualFR/EN,July6–10,2026archive.595+60lunch+220coach+100care=975EUR/child, not Monceau650; next2027notannounced.',
 'All950 prior dossiers,3658 events and43 offer objects preserved. Sixteen curricular/place-specific dossiers across six operators, nine new future October2026 intervals and three single-child partial budgets. Prior worldwide competitions, exhibitions, camps, schools,5–10year results, priorities and family routes preserved;0 fullyauditedcountries, goalactive.'
]
audit=dict(version=124,asof=CHECKED,status='progress',scope='Selected Switzerland/France/Spain junior curricula, autumn2026 intakes, archived museum/school programmes and explicit language/grade gates. Sixteen dossiers across six operators; neither sixteen separate world-ranked camps nor a complete world inventory.',events=len(d['events']),competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],camp_learning_records=blocks['Лагеря'],programme_dossiers=len(cp['profiles']),countries_with_dossiers=39,official_dossier_urls=len({s['url'] for x in cp['profiles'] for s in x['sources']}),editorial_scenarios=len(cp['shortlist']),coverage_gaps=len(cp['gaps']),league_profiles=len(d['league_guide']['profiles']),budget_scenarios=46,budget_providers=23,budget_programme_dossiers=len({x['slug'] for x in d['camp_planning']['offers']}),new_budget_scenarios=3,new_budget_ids=NEW_IDS,new_dossiers=16,new_dossier_slugs=NEW,new_programme_operators=['IILCamps','SimplyTheatre','LaNouvelleEcole','MUNCYT/FECYT','ObjectifSciencesInternational','EIBLaJonchère'],updated_dossier_slugs=[],new_event_ids=sorted(now.keys()-old.keys()),updated_event_ids=[],unchanged_dossier_objects=950,unchanged_event_objects=3658,unchanged_prior_budget_objects=43,source_retrieval_attempts=28,direct_successful_bodies=27,retrieval_errors=1,pdf_download_files=4,pdf_text_pages_extracted=23,new_visual_pdf_checks=4,family_ical=family,exhibition_ical=expo,goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,checks=checks,verification={})
for name in ['independent-check.json','functional-check.json']:
 f=P/name
 if f.exists():
  q=json.loads(f.read_text());assert q['status']=='passed' and q['version']==124;audit['verification'][name.removesuffix('.json')]=q
def write(stem,v):
 text=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(text);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(text)
write('europe-camps-audit-v124',audit)
write('europe-camps-source-receipts-v124',dict(version=124,asof=CHECKED,scope=audit['scope'],sources=sources,pdf_download_files=4,pdf_text_pages_extracted=23,visual_pdf_pages_checked=[dict(filename='muncyt-summer-pdf.pdf',page=4),dict(filename='muncyt-summer-pdf.pdf',page=10),dict(filename='lne-geneva-pdf.pdf',page=2),dict(filename='eib-jonchere-correct-pdf.pdf',page=1)],external_actions=external,primary_reader_limits='Selected primary clauses and public schedules; not all sites, global rankings or every2027intake. Four selected PDF pages visually checked; others text extracted. Raw snapshots and PDF images private outside repository. No forms, checkout, login or consent actions.'))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=124:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native123 succeeded2026-10-06T12:50:47.532257Z; deployment appgdep_6ac4ee8884308191974373c3de0022a7; commit '+BASE+'. Worldwide goal active.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','budget_providers','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected European junior curricula, actual autumn sessions and partial budgets checked; native publication separate.'
plan['europe_camp_programme_audit_v124']=audit
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for x in plan['requirements']:
 if x['id']=='unified_database':x['evidence']='v124:3667 events/966 programme dossiers/39 countries/1498 URLs;16 newEurope dossiers,9 futureOctoberintervals,3 partialsinglechildbudgets. Every3658oldevent/950profile/43offer preserved; completeportableJSON/SQLite.'
 elif x['id'] in ['camps','family_top_picks','camp_switzerland_full']:x['evidence']='v124:966 dossiers/39countries/230editorialscenarios. SwissIIL3–6/5–7/6–9/8–13,SimplyEN4–6/7–11, SwissOSI7–12ENoffered; FranceLNE/EIBbilingualandFR-onlyOSI; SpainMUNCYTcompletedgradecurricula. AllpriorEurope/Asia/Americas/globalgeneral/thematic/day/boarding/familyENESRUscopepreserved; notcompleteworldwide.'
 elif x['id']=='camp_full_pricing':x['evidence']='v124:46partialbudgets/23brands;43oldoffers unchanged. IILAI350MatveyAM-noonsitelunch,Junior550Oscarfullweek+75latecare; Simply595MatveyENweek+lunchbox. Insurance/travel/housingunknown, no fake0. ArchivedLNE/EIB/MUNCYTfeesyear/unitlabelled. Depositnotdoublecounted.'
 elif x['id']=='camp_calendar_2026_2027':x['evidence']='v124:9newOctober2026intervals,7IILexact+2Simplyyearfromown2026–27contextlabelledpublished_rule. MultiOct19–23and26–27notcontinuousweekendcamp. Archived2026notexportedas2027. FamilyICS2882/exhibition104; oldUID/contentpreserved.'
plan['research_passes']=[x for x in plan.get('research_passes',[]) if x.get('version')!=124]+[dict(version=124,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=16,updated_dossiers=0,new_calendar_rows=9,new_budget_scenarios=3,official_primary_retrieval_attempts=28,pdf_download_files=4,not_complete_worldwide=True)]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=123','?v=124').replace('data-ui-version="123"','data-ui-version="124"');anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_europe_camps_audit_v124.json" download>Европа · младшие программы и языки</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text();anchor='<a href="downloads/STEM_latam_camps_audit_v123.json"';link='<a href="downloads/STEM_europe_camps_audit_v124.json" download>Европа: младшие группы, ближайшие смены и смета ↓</a> · <a href="downloads/STEM_europe_camps_source_receipts_v124.json" download>Источники и ограничения ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps({k:audit[k] for k in ['version','events','programme_dossiers','new_dossiers','budget_scenarios','family_ical','worldwide_complete']}))
