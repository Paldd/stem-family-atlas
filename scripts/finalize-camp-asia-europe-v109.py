"""Record a bounded research pass without shrinking the worldwide goal."""
import collections,hashlib,json,subprocess
from camp_asia_europe_v109 import ROOT,BASE,CHECKED,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-asia-europe-primary-v109'
d=json.loads((ROOT/'data/catalog.json').read_text());b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
cp=d['camp_programmes'];assert len(cp['profiles'])==798
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
assert old.keys()==now.keys() and {k for k in old if old[k]!=now[k]}=={'L183'}
assert d['camp_planning']==b['camp_planning']
sources=[]
for n in [1,2,3]:
 for q in json.loads((P/f'receipt-{n}.json').read_text()):
  q.update(checked=CHECKED,retrieval_method='direct_http',content_scope='Selected own-site clauses or duplicate comparison; not a whole-site/country audit.')
  if q.get('status')==200:
   f=P/(q['key']+('.pdf' if q['key']=='faisl-brochure' else '.html'));body=f.read_bytes()
   assert len(body)==q['bytes'] and hashlib.sha256(body).hexdigest()==q['sha256']
   q.update(raw_filename=f.name,body_snapshot_retained=True,content_status='download_only_existing_pdf_not_newly_visually_reviewed' if f.suffix=='.pdf' else 'selected_html_clauses')
  else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body')
  sources.append(q)
assert len(sources)==27 and sum(q.get('status')==200 for q in sources)==26
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
sm=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text());jm=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
checks=[
 '20 new programme dossiers:18 distinct XCL courses inSingapore and2 specific French boarding programmes. Dossiers are not a count of independent providers or a world quality ranking.',
 '778 old dossiers/IDs retained; only xcl and american-village evidence updated. 3348 old event IDs retained; only L183 corrected: unconfirmed technical language no longer appears as EN; age-after7 and contract clauses explicit. No new event/session/deadline.',
 '798dossiers/39countries/1233dossierURLs/185editorialscenarios/190gaps. CHE106/FRA62/ESP67/TWN53/SGP96/JPN52/KOR17/USA85/CAN98/CRI13/MEX35; none fully audited.',
 'FutureEngineerscourse10–15 versus calendar7–15 and generalCodeAcademy6–14; STEAMJune22 vsJune29; Science7–11vs7–12. Exact programme restrictions not replaced by general headers.',
 'XCL2026 tariffs are archive only; TBC/undated price years stay unknown. Earlybird15May2026 expired; no2027 intake or price invented. EN-level FAQ is not an EN-technical instructor; EAL is only an English course.',
 'XCL no-refund-after-payment terms conflict with FAQ discretionary illness refund; payment3workingdays/changes10days/sameseason/ownmedical-accident/120bus≥6riders/conditional3percentStripe visible. No full travel invoice claimed.',
 'MangaJF2 July12–17 2026 from779EUR/6days/10–14; Damian six closed2026 intakes from749/6days or1469/13days/11–15. Packinsurance60extra; station transfer reservation required; provincial route can be unaccompanied. Reviews not dates or independent ranking.',
 'Oscar2020max7in2027: no8plus boarding admission. MatveyMangaafter10; Damianafter11in2028. General7–17header/CE2schoolgroup do not prove family admission.',
 'Respira group minimum50 and generic one-week78/90/102EUR for4/5/6h are not a two-child invoice. Christmas2026–27 window is not exact open family intake. Existing EnglishSummer/Keiko/FAISL/Taiwan programmes retained without duplicate dossiers.',
 '27directattempts/26HTTP200:25HTML and1PDF download only; guessed old XCLterms404 retained, observed correctedterms200 used. Zero fresh visual PDF checks. Complete portable SQL/JSON ZIP/hash/README and2593family/104expo ICS preserved. Nine family budget scenarios unchanged.',
 'Worldwide goal/requirements/permanent schools/5–10year results/competitions/leagues/exhibitions/EN-ES-RU camps2026–27/routes retained;0fullyauditedcountries. Native publication receipt is separate.'
]
priority='Continue full deep CHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatAm general/thematic/STEM camps2026–27/day/boarding/family EN/ES/RU: own current programme, technical instructor, individual foreign intake, full price/travel/gear/insurance/nightcare/refunds and child-specific quality shortlist. Preserve world competitions/leagues/exhibitions/permanent schools/5–10year results/family routes and all requirements. No world or country completeness claim.'
audit=dict(version=109,asof=CHECKED,status='progress',scope='Selected Singapore programme/contract and French boarding-intake clauses; Spanish duplicate and group-intake checks. Not a whole-country/world audit.',new_dossiers=len(NEW),new_dossier_slugs=NEW,updated_dossier_slugs=UPDATED,new_event_ids=[],updated_event_ids=['L183'],events=3348,camp_learning_records=2006,programme_dossiers=798,countries_with_dossiers=39,official_dossier_urls=1233,editorial_scenarios=185,gaps=190,budget_scenarios=9,family_ics=2593,exhibition_ics=104,league_profiles=141,worldwide_complete=False,fully_audited_countries=0,primary_retrievals=dict(direct_attempts=27,http200=26,html=25,pdfs_downloaded=1,errors=1,new_visual_pdf_checks=0),external_actions=external,validation=checks,next_priority=priority,complete_database_download=sm,complete_json_download=jm)
def write(stem,value):
 s=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('camp-asia-europe-audit-v109',audit)
write('camp-asia-europe-source-receipts-v109',dict(version=109,asof=CHECKED,scope=audit['scope'],sources=sources,external_actions=external))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=109:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native108 succeeded;commit '+BASE+';deployment appgdep_6ac4899a501c819190f87c91d5335763. Fullworld objective remains active.')
plan['latest_validation']=dict(version=109,asof=CHECKED,status='Selected primary research, archive-language correction and portable database checks; native publication separately',events=3348,camp_learning_records=2006,programme_dossiers=798,countries_with_dossiers=39,official_dossier_urls=1233,editorial_scenarios=185,budget_scenarios=9,budget_providers=4,family_ical=2593,exhibition_ical=104,league_profiles=141,worldwide_complete=False,checks=checks,country_dossier_counts=dict(collections.Counter(p['iso'] for p in cp['profiles'])))
plan['asia_europe_camp_programme_audit_v109']=audit;plan['complete_database_download']=sm;plan['complete_json_download']=jm
for q in plan['requirements']:
 if q['id']=='unified_database':q['evidence']='v109:3348cards/798dossiers/39countries, full JSON/SQL ZIP without truncation;20newprogrammes/2updates/L183language corrected.'
 elif q['id']=='camp_full_pricing':q['evidence']='v109:XCL archived2026/unknownyear fees,120bus/conditional3percent/owninsurance and refund conflict; French closed2026price/60insurance. Nine prior family scenarios retained; not fullworld pricing.'
 elif q['id']=='camp_calendar_2026_2027':q['evidence']='v109:unannounced2027 and archive2026 separated;no new exactdates/deadlines. 2593familyICS/104expo retained.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=109]+[dict(version=109,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=20,new_calendar_rows=0,updated_calendar_rows=['L183'],official_primary_retrieval_attempts=27,pdfs_downloaded=1,new_visual_pdf_checks=0,not_complete_worldwide=True)]
plan['next_research']=[priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED;write('research-plan',plan)
p=ROOT/'dist/index.html';s=p.read_text().replace('?v=108','?v=109').replace('data-ui-version="108"','data-ui-version="109"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_camp_asia_europe_audit_v109.json" download>Сингапур и французские пансионы · проверка программ и условий</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(status='progress',version=109,new_dossiers=20,dossiers=798,events=3348,goal='active')))
