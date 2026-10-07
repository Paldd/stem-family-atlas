"""Bounded research receipt; preserve the active worldwide family objective."""
import collections,hashlib,json,subprocess
from camp_asia_v112 import ROOT,BASE,CHECKED,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-asia-primary-v112'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
cp=d['camp_programmes'];old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
changed=[k for k in old if old[k]!=now[k]];newids=sorted(now.keys()-old.keys())
assert len(newids)==2 and set(changed)=={'CP676-20270105-20270124','CP676-20270127-20270215'}
assert len(cp['profiles'])==839 and d['camp_planning']['offers']==b['camp_planning']['offers']
sources=[]
for f in sorted(P.glob('receipt-*.json')):
 for item in json.loads(f.read_text()):
  q=dict(item,checked=CHECKED,retrieval_method='direct_http',content_scope='Selected primary programme/policy clauses or comparison with an existing dossier; not a whole-site or country audit.')
  if q.get('status') in [200,202]:
   ext='pdf' if (P/(q['key']+'.pdf')).exists() else 'html';raw=(P/(q['key']+'.'+ext)).read_bytes()
   assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
   q.update(raw_filename=q['key']+'.'+ext,body_snapshot_retained=True,content_status='empty_http202_body' if not raw else 'selected_visual_pdf_pages' if ext=='pdf' else 'html_notice_shell_zero_posts' if q['key']=='hafs-notice' else 'selected_html_clauses')
  else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body')
  sources.append(q)
assert len(sources)==39 and sum(q.get('status')==200 for q in sources)==35
reader=P/'web-reader-comparison.json';raw=reader.read_bytes()
reader_receipt=dict(retrieval_method='public_primary_web_reader',raw_filename=reader.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),content_scope='BC Taiwan fresh EN/ZH2027 comparison and WINNING family2027 article; separately retained reader output, not raw HTML.')
visual=json.loads((P/'visual-review.json').read_text());assert visual['new_visual_pdf_checks']==20
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
sm=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text());jm=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT');expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert family==2644 and expo==104
blocks=collections.Counter(q['block'] for q in now.values());country_counts=dict(collections.Counter(q['iso'] for q in cp['profiles']))
urls=len({s['url'] for p in cp['profiles'] for s in p['sources']})
checks=[
 '12 new programme/format dossiers across6 operators in5 venue countries:WINNING3 including2 Philippines venues, Kidchen2, YoungEngineers3, Sunshine1, Kspace2, HAFS1. One existing SMISJeju dossier materially deepened. Not12 independent providers or an objective world ranking.',
 'All3419 prior event IDs retained;3417 event objects exactly unchanged. Only two existing SMISJeju generated rows updated for new primary curriculum/room evidence. All827 prior dossier IDs retained;826 old dossier objects exactly unchanged.839 total dossiers/39 countries/1297 dossierURLs/197 editorial scenarios/208 gaps.',
 'WINNING Singapore Jan23–Feb1,2027,11–18,AIGC inEnglish,boardingfour/room.3900USD early quote with no expiry/baseprice,1000depositinside,group3people5%not2siblings. Both family children later. Universityvisit/certificateclaim not universitycredit or competitionmedal.',
 'WINNING Cebu STEAM Jan22–Feb3,2027,10–17,EnglishCLIL/maker3D/basiccircuits/ecology/prototype/presentation.1900early/2200regular;−100promo conditions unknown,not deducted. Twelve nights/3meals/activities/localstudenttransport/laundry/video included;airfare/personal excluded,insurance/equipmentownership/refundunknown. Adult1200/1300/1400 separate noSTEAM activities;familyemptybed175/week rounding unknown. Matvey conditional10byJan22,Oscar later.',
 'WINNING generalWinter2027 6–10DannyKids/10–18Cambridge plusadultlanguage/familyrooms is separate. No exactdates/fees,STEAMcalendar/1900/adultfees not copied. Foreignpassportintake unconfirmed despite internationalstudentdescription.',
 'Kidchen Taipei4–10:autumnOct19–23/26–30 without year;copyright2026 not campdateproof. No datedcalendarrows. Half1900/full3400daily,8500/13800week,5%twofullweek gives26220TWD;half17000withoutdiscount. Halfcookingmorning versusSTEAMafternoon/full split;ENinteractions not entireEnglish-onlyguarantee. Camp cancellation4day boundary conflict retained,partytermsnotcopied.',
 'Young Engineers:AlgoPlay5–9/Bricks6–12/Robobricks8–12,two lessons/3hours,LEGOkitnotforhome. Englishsoftwareterminology not fullEnglishteacher. Date/year/fee unknown;5 actualholidaycentres not7 genericbranches. Weekly curriculum/marketingendorsement not currentdatedcamp/independentqualityproof.',
 'Sunshine Japan general6months–12/English/foreignfamilies,Tokyo andChiba one providerdossier. ActualSummer2026EarthtoUniverse6months–3 unsuitable both;infantcare/lunch/bus/options not copiedtooldercohorts. Winter2026–27/Summer2027 date/fee unknown.',
 'Kspace Summer2026 only18Jul–22Aug/26Aug–5Sep,14months–10,Englishonly/overseas screening.13000/18000daily plusnew25000reg/8000materials/15000Zoom,tax10%/mandatoryuniform/meals. OldAug31,2025cutoff evenin2026brochure retained. Winterwrapper2026→PDF2025/26 seven selecteddays,notcontinuousnorDec2026/Jan2027. No futurecalendar ornewpriceestimate fromarchives. Cancellation/noentry/anaphylaxis restrictions recorded as datedcontractfacts.',
 'HAFS Grade4–6/Middle1–2 Englishdebate/essay/ARC boarding. OwnFAQ explicitly100%Englishonlyimpossible. Curriculum electivesmedicalAI areexamples not promisedrobotics2027course.4190000KRW actualSummer2026 quote not winter2027. Publicnotice0posts:cached32Winter2027searchsnippet not exactcampdateproof. Samplelatehomework/nightregime distinguished from chosenclassguarantee;overseasemailnot passportadmission.',
 'SMIS ownSep/Oct2026 winter2027FutureLab:8periodsabout40min inrotationday,not8dailyentirecamp;AI/vibecoding/emotion/fairness/architecture/body/sportscience;ENESL onlyconfirmed. Ownfour/room vsMGGlobal2–4 retained;mentor~10/nightchecks3/phone3calls operatorclaims,notindependentaudit. Bothclass/foreignintake stillunknown.',
 'BC Taiwan fresh EN/ZH both2027;prior2026searchcache not liveconflict. Existing2BCprofiles/Computhink/STEAMSQUAD unchanged,no duplicatefreshsamefacts. NKJune2026 expired,Sep8–12MonFri2025residue,NovDecyearless not newdates. KID.FUN.FITHTTP202empty andKidchenlegacy404/timeouts not validatedprogramme.',
 'All17 prior two-child budget estimates exactly retained;newprices do not produceeligibleconfirmed-datebothchildscenarios. FamilyICS2644:+oneCebuMatveyconditionalcalendar;Singaporebothlater excluded. CompleteSQLite/JSONZIP without truncation and filecaps checked.',
 '39directHTTPattempts/35HTTP200:31HTML and4PDF;oneHTTP202empty/threeerrors.20 full selectedPDFpages visually inspected. No externalmessages/forms/payments/accounts/consents/schedules. Worldwide goal remains active;0 fullyauditedcountries.'
]
priority='Continue deep Switzerland/France/Spain/Europe,Taiwan/Singapore/SouthKorea/Japan,USA/Canada,CostaRica/Mexico/LatinAmerica: all general/thematic/STEM camps2026–27,day/boarding/family and EN/ES/RU. Verify course curriculum,actual teacher language,foreign individual intake,full two-child pricing/equipment/nightcare/insurance/refunds,quality shortlist and routes. Preserve worldwide competitions/leagues/exhibitions and permanent schools/5–10yearresults. No country/worldwide completion claim from a bounded pass.'
audit=dict(version=112,asof=CHECKED,status='progress',scope='Selected own-site Asian programmes and policies in Taiwan/Singapore/Japan/SouthKorea plus Taiwan-organized Philippines venues; not a complete country/world audit.',new_dossiers=len(NEW),new_dossier_slugs=NEW,updated_dossier_slugs=UPDATED,new_event_ids=newids,updated_event_ids=changed,events=len(now),camp_learning_records=blocks['Лагеря'],programme_dossiers=len(cp['profiles']),countries_with_dossiers=len(cp['countries']),official_dossier_urls=urls,editorial_scenarios=len(cp['shortlist']),coverage_gaps=len(cp['gaps']),country_dossier_counts=country_counts,competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],league_profiles=len(d['league_guide']['profiles']),budget_scenarios=17,budget_providers=10,new_budget_scenarios=0,family_ical=family,exhibition_ical=expo,new_visual_pdf_checks=20,external_actions=external,goal='active',worldwide_complete=False,fully_audited_countries=0,checks=checks,next_research=priority)
def write(stem,value):
 s=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('asia-camps-audit-v112',audit)
write('asia-camps-source-receipts-v112',dict(version=112,asof=CHECKED,scope=audit['scope'],sources=sources,primary_reader_comparison=reader_receipt,visual_review=visual,external_actions=external))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=112:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native111 succeeded and refreshed112;commit '+BASE+';deployment appgdep_6ac49e75df2881919aaa2b6b0c50035d. Full worldwide objective remains active.')
plan['latest_validation']=dict(version=112,asof=CHECKED,status='Selected primary programme,visual sources and portable database checks;nativepublication separate',events=len(now),camp_learning_records=blocks['Лагеря'],programme_dossiers=839,countries_with_dossiers=39,official_dossier_urls=urls,editorial_scenarios=197,budget_scenarios=17,budget_providers=10,family_ical=family,exhibition_ical=expo,league_profiles=audit['league_profiles'],worldwide_complete=False,fully_audited_countries=0)
plan['asia_camp_programme_audit_v112']=audit;plan['complete_database_download']=sm;plan['complete_json_download']=jm
for q in plan['requirements']:
 if q['id']=='unified_database':q['evidence']='v112:3421cards/839dossiers/39countries;12newprofiles/twonew2027calendarrows,oneSMISdossier/tworowsdeepened;all prior IDs retained. CompleteJSON/SQLiteZIP withouttruncation.'
 elif q['id']=='camp_full_pricing':q['evidence']='v112:17priorfamilyestimatesexactlyretained. NewCebu1900early/2200regularand1200–1400adult separate;Singapore3900early/1000inside;Kidchenyearunknown,Japanarchivefees+mandatoryextras. Newfamilyfullinvoice/places notconfirmed.'
 elif q['id']=='camp_calendar_2026_2027':q['evidence']='v112:twoexactnew2027boardingrows(Cebu10+,Singapore11+),twoSMISrowsdeepened. FamilyICS2644/expo104. No inventeddatefromyearlessKidchen/oldKspacePDF/infantSunshine/currentHAFSshell.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=112]+[dict(version=112,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=12,updated_dossiers=1,new_calendar_rows=2,updated_calendar_rows=changed,official_primary_retrieval_attempts=39,pdfs_downloaded=4,new_visual_pdf_checks=20,not_complete_worldwide=True)]
plan['next_research']=[priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED;write('research-plan',plan)
p=ROOT/'dist/index.html';s=p.read_text().replace('?v=111','?v=112').replace('data-ui-version="111"','data-ui-version="112"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_asia_camps_audit_v112.json" download>Азия · возраст, язык, новые зимние смены и полный состав цены</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text();anchor='<a href="downloads/STEM_europe_camps_audit_v111.json"'
link='<a href="downloads/STEM_asia_camps_audit_v112.json" download>Азия: новые смены, возраст и состав цены ↓</a> · <a href="downloads/STEM_asia_camps_source_receipts_v112.json" download>Первичные страницы и проверенные PDF Азии ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(status='progress',version=112,new_dossiers=12,updated_dossiers=1,new_calendar_rows=2,updated_calendar_rows=changed,dossiers=839,events=len(now),budget_scenarios=17,goal='active')))
