"""Bounded research receipt; the worldwide objective remains active."""
import collections,hashlib,json,subprocess
from camp_americas_v110 import ROOT,BASE,CHECKED,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-americas-primary-v110'
d=json.loads((ROOT/'data/catalog.json').read_text());b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
cp=d['camp_programmes'];assert len(cp['profiles'])==815
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
assert old.keys()<=now.keys() and all(now[k]==v for k,v in old.items())
newids=sorted(now.keys()-old.keys());assert len(newids)==28
assert d['camp_planning']['offers'][:9]==b['camp_planning']['offers']
assert len(d['camp_planning']['offers'])==14
sources=[]
for n in range(1,5):
 for item in json.loads((P/f'receipt-{n}.json').read_text()):
  q=dict(item,checked=CHECKED,retrieval_method='direct_http',content_scope='Selected programme/policy clauses or comparison with existing dossiers; not a full site/country audit.')
  if q.get('status')==200:
   f=P/(q['key']+'.html');raw=f.read_bytes()
   assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
   q.update(raw_filename=f.name,body_snapshot_retained=True,content_status='html_shell_no_readable_programme_body' if q['key']=='nr-main' else 'selected_html_clauses')
  else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body')
  sources.append(q)
assert len(sources)==25 and sum(q.get('status')==200 for q in sources)==22
f=P/'web-reader-fallback.json';raw=f.read_bytes();reader=dict(retrieval_method='public_primary_web_reader',raw_filename=f.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),urls=['https://spacecenter.org/explorer-camps/','https://spacecenter.org/education-programs/explorer-camps/explorer-camps-parent-guide/'],content_scope='Selected Houston age/course/price/parent-guide clauses opened through web reader after HTTP timeouts; retained responses are not raw HTML or whole-site audit.')
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
sm=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text());jm=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
def countics(name):return (ROOT/'dist/downloads'/name).read_bytes().count(b'BEGIN:VEVENT')
family=countics('STEM_подтвержденные_даты.ics');expo=countics('STEM_крупные_выставки.ics');assert family==2616 and expo==104
blocks=collections.Counter(e['block'] for e in d['events']);countries=dict(collections.Counter(p['iso'] for p in cp['profiles']))
checks=[
 '17 new dossiers across 7 operators: Houston8 age/format profiles,Perot2 programmes,KSC1,Arca1,Cacao1,Berkana3,RF1. Not17 independent camp providers or a world quality ranking.',
 '798 old dossiers and all3348 old event records/IDs unchanged;28 new camp calendar rows. Competitions1153/exhibitions189 unchanged;camp-learning2034;3376 total cards.',
 '815 programme dossiers/39 countries/1250 dossierURLs/189 editorial scenarios/197 gaps. CHE106/FRA62/ESP67/TWN53/SGP96/JPN52/KOR17/USA96/CAN98/CRI14/MEX38/BRA4/PAN6. None fully audited.',
 'Houston2026: evenings79.95 including meal, single74.95, multi179.95 perchild. Age bands5–7/8–10 evening-single and4–5/6–7/8–9/10–11 multi. Themes differentiated; no overnight stay. English teacher/individual foreign intake not directly confirmed.',
 'Houston guide:3day meal34.50;care20/day/slot onlymulti;auto latecare30 differs from20;shirts/snack included. Agefirstday/selfcare/medical required. Refund2weeks/full vs48h/yearcredit; intermediate period unknown. FAQsummer2025 not future2027 intake.',
 'Perot2026 Nov23–25/Dec21–23/Dec28–30, strictly K–4, public275 per3-day package. Aftercare45 course vs75 generalFAQ explicit conflict. ES translation not ES teaching. Refund earlier4weeks unclear, under4weeks no refund/transfer;ProCare/immunization requirements not submitted.',
 'KSC2026 ten closed/soldout5day weeks;DOB cutoffs and ENfluency directly published.2027 dates/prices unknown;repeatedweeks repeatcurriculum;simulatorheight limits and cancellation gaps explicit. No false2027 calendar imported.',
 'Arca directHTML authoritative Oct30–Nov1,2026 vs oldSeptembersearchcache. Whole campEN,Little4–7/Junior8–11,science/art/creativebooklet;Christian content explicit. Two-siblingTOTAL497.80 food/427.80 without, not per-child or invented discount. Fullhours/address/refund/availability unresolved; no boarding proof.',
 'CacaoJan4–8,2027 published range conflicts withTue–Sat copy. Tentnight75 optional, not whole-weekboarding;PAB428+406.60=834.60 includingITBMS/lunch/snack/onsiteaccidentcover. Dec1refundgap. Range exported as schedule-to-confirm with no invented weekdays.',
 'BerkanaJotunheader2027/body2026/5daysvsDec19–22 unresolved, no session. ThorsJuly18–Aug1,2027 season window only,13200/week and noncumulative earlydiscounts;no invented weekboundaries. TyrAug5–8,2027 day/board,priceofday unknown. Deposits already partofprice;ACAsoon/RNTpending not accreditation.',
 'RFJan2026 age10–14/CRC127750 archived;generic2week127500 not samecourse. CPICprofessionalUCRworkshop no childage, gap only. MountView schoolgroup US/UK trips not independent family intake. ExistingMakeX/ScienceNorth retained without duplicate dossiers.',
 'Nine old family scenarios retained exactly;5 new estimates:Arca2,Cacao1,Houston1,Perot1. Missing travel/lodging/expenses remain unknown. Complete SQLite/JSON ZIP without record truncation;raw oversized assets removed by filecap rule. FamilyICS2616/Expo104;past-dated entries may expire at2026-10-06,all catalogue rows preserved.',
 '25 directattempts/22HTTP200 HTML includingNRshell/3HoustonHTTPtimeouts;Houston fallback selectedprimaryweb-reader responses retained separately. Zero PDFs/visualPDF checks. No external messages/forms/payments/accounts/consents/schedules.',
 'Full worldwide objective and priority countries,permanent schools/5–10year results/competitions/leagues/exhibitions/all general,thematic,STEMEN-ES-RUcamps2026–27/familyroutes retained. Goalactive/0fullyauditedcountries;native publication receipt separate.'
]
priority='Continue deep Switzerland/France/Spain/Europe,Taiwan/Singapore/SouthKorea/Japan,USA/Canada,CostaRica/Mexico/LatinAmerica: all general/thematic/STEM camps2026–27,day/boarding/family and EN/ES/RU. Own current curriculum,actual technical teacher language,individual foreign intake,full two-child pricing/gear/nightcare/insurance/refunds,quality shortlist and routes. Preserve worldwide competitions/leagues/exhibitions/permanent schools/5–10year results and all requirements;0fullyauditedcountries.'
audit=dict(version=110,asof=CHECKED,status='progress',scope='Selected own-site camp/course and policy clauses in USA/Brazil/Panama/Mexico/CostaRica;Canada and Mexico competition duplicate checks. Not a whole-country/world audit.',new_dossiers=17,new_dossier_slugs=NEW,updated_dossier_slugs=UPDATED,new_event_ids=newids,updated_event_ids=[],events=len(now),camp_learning_records=blocks['Лагеря'],programme_dossiers=815,countries_with_dossiers=39,official_dossier_urls=1250,editorial_scenarios=189,gaps=197,budget_scenarios=14,budget_providers=8,family_ics=family,exhibition_ics=expo,league_profiles=len(d['league_guide']['profiles']),worldwide_complete=False,fully_audited_countries=0,primary_retrievals=dict(direct_attempts=25,http200=22,html=22,html_shells=1,errors=3,primary_reader_fallback=True,pdfs_downloaded=0,new_visual_pdf_checks=0),external_actions=external,validation=checks,next_priority=priority,complete_database_download=sm,complete_json_download=jm)
def write(stem,value):
 s=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('americas-camps-audit-v110',audit)
write('americas-camps-source-receipts-v110',dict(version=110,asof=CHECKED,scope=audit['scope'],sources=sources,primary_reader_fallback=reader,external_actions=external))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=110:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native109 succeeded and refreshed110;commit '+BASE+';deployment appgdep_6ac48f9eff3c8191abea33019874624c. Fullworld objective remains active.')
plan['latest_validation']=dict(version=110,asof=CHECKED,status='Selected primary programme and portable database checks;native publication separate',events=len(now),camp_learning_records=blocks['Лагеря'],programme_dossiers=815,countries_with_dossiers=39,official_dossier_urls=1250,editorial_scenarios=189,budget_scenarios=14,budget_providers=8,family_ical=family,exhibition_ical=expo,league_profiles=audit['league_profiles'],worldwide_complete=False,checks=checks,country_dossier_counts=countries)
plan['americas_camp_programme_audit_v110']=audit;plan['complete_database_download']=sm;plan['complete_json_download']=jm
for q in plan['requirements']:
 if q['id']=='unified_database':q['evidence']='v110:3376cards/815dossiers/39countries;17newdossiers/28calendarrows;all prior records retained. Complete portable JSON/SQLZIP without truncation.'
 elif q['id']=='camp_full_pricing':q['evidence']='v110:14familyestimates,9old+5new. Arca497.80food/427.80without for2siblings;Cacao834.60+optionalnight150;Houston359.90+meal69/optionalcare;Perot550base/aftercareconflict. Full invoices/travel/places not yet confirmed.'
 elif q['id']=='camp_calendar_2026_2027':q['evidence']='v110:28newcampcalendarrows;Houston/Perot/Arca2026,Cacao/Tyr2027. Thorsseasononly/Jotunyearconflict/KSC-RFarchives explicit;no inventedintakes. FamilyICS2616/expo104.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=110]+[dict(version=110,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=17,new_calendar_rows=28,updated_calendar_rows=[],official_primary_retrieval_attempts=25,pdfs_downloaded=0,new_visual_pdf_checks=0,not_complete_worldwide=True)]
plan['next_research']=[priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED;write('research-plan',plan)
p=ROOT/'dist/index.html';s=p.read_text().replace('?v=109','?v=110').replace('data-ui-version="109"','data-ui-version="110"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_americas_camps_audit_v110.json" download>Америка · зимние и летние лагеря, возраст и стоимость для братьев</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(status='progress',version=110,new_dossiers=17,new_calendar_rows=28,dossiers=815,events=len(now),budget_scenarios=14,goal='active')))
