"""Bounded programme audit and expanded worldwide-goal continuity."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v90'
BASE='21d9f87320b8d6b38a5724a3ce475e1c294e4c3b'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
op={q['slug']:q for q in b['camp_programmes']['profiles']};old={e['id']:e for e in b['events']}
fresh=[q for q in c['profiles'] if q['slug'] not in op]
changed=[e['id'] for e in d['events'] if e['id'] in old and e!=old[e['id']]]
new=[e for e in d['events'] if e['id'] not in old]
assert len(fresh)==19 and len(new)==34 and len(changed)==7
assert all(old[i].get('camp_dossier_slug')=='makemake' for i in changed)
assert c['counts']['dossiers']==594 and c['counts']['source_urls']==893
receipts=[v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts)==52 and sum(q.get('status')==200 for q in receipts)==45
scopes={
 'tamwood-current':'Live redirect to ILAC closure notice, despite cached Summer2027 offer; no new Tamwood/ILAC programme admitted.',
 'ilac-current':'Current own closure notice read; no printed year for FridaySeptember18 inferred.',
 'santa-international':'Relevant international/language/admission sections read; not an English bilingual curriculum or every historical cohort.',
 'santa-language':'Relevant first-residential and language/context sections read; no cohort-level EN/ES guarantee inferred.',
 'star-home':'Provider context only; no country/world ranking or grade admission inferred.',
 'star-robotics':'Operator robotics context; no independent contest achievement attributed to a camp.',
 'starcode':'Application22languages includingEN/ES/RU, not evidence of teaching language. No app/account opened.',
 'ucr-call':'October1,2026 call to2027 instructors/facilitators, not a child camp registration.',
 'real-madrid-brochure':'Observed brochure link resolves to generic operator page, not a retrieved priced PDF. Fee remains unknown.',
 'real-madrid-legal':'Relevant medical/media/cancellation clauses read; no acceptance or education-admission decision.',
 'amora-about':'Provider/community context; home waitlist is not camp enrolment.',
 'amora-events':'Index discovery, separately followed actual camp event; not an additional programme dossier.',
 'woods-cr':'Mixed Corcovado ages, three-month research and four-day family tour explicitly separated from JanuaryDominicalito camp.',
 'woods-day':'Sample educational day, not exact January2027 timetable.',
 'makemake-home':'Generic6–17 not substituted for actual ClassicGrade2–8 or TeenGrade9–11.',
 'makemake-es':'Secondary language website not used as independent teaching proof.',
}
for q in receipts:
 if q.get('status')==200:
  f=PRIMARY/(q['key']+'.html');assert hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
  q.update(raw_filename=f.name,body_snapshot_retained=True,
   content_scope=scopes.get(q['key'],'Relevant own programme body, age/date/price/curriculum/conditions read; unknown language, places and complete country coverage not inferred.'))
  if q['key'].startswith('star-') and q['key'] not in ['star-home','star-terms','star-camps','star-robotics']:
   q['content_scope']='Visible own Event body/date/ticket fees and public JSON-LD read. ShowMore not fully expanded: browser redirected to blocked-page. Hidden programme text not claimed read; date/hour conflicts preserved.'
browser=json.loads((PRIMARY/'browser-receipts.json').read_text())
assert len(browser)==1
for q in browser:assert hashlib.sha256((PRIMARY/q['raw_filename']).read_bytes()).hexdigest()==q['sha256']
oldurls={s['url'] for q in op.values() for s in q['sources']}
added=sorted({s['url'] for q in c['profiles'] for s in q['sources']}-oldurls);assert len(added)==31
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False)
isos=['CHE','FRA','ESP','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','MYS','USA','CAN','CRI','MEX','BRA','CHL']
byiso={s:sum(q['iso']==s for q in c['profiles']) for s in isos}
learning=sum(e['block']=='Лагеря' for e in d['events'])
checks=[
 '19 new programme/format/age dossiers across8 new operator groups; existing Mákemáke Classic deepened and Teen added as ninth group. All575 prior dossier IDs/order retained;574 complete profiles unchanged. All3037 previous events retained;only7 CP047 Classic rows have updated transport/cancel/context. Dates/admission identity preserved.',
 'Star Kids five themes at one Cupertino venue: Carbots15–19Feb2027 and EcoBots12–16Apr2027; Christmas21–24/28–31Dec2026. Own Grades1–2/3–6, not birth-derived admission. Four prices include ticketfees:399.75/461.25/563.75/666.25USD. StarCode22languages does not prove campEN. BattleBots23–26 versus23–27Nov excluded from exact calendar; Gaming31Dec12:00vs15:00 unresolved. ShowMore body not fully read; own terms food not served, first-day/transfer rules separate from monthly after-school fees.',
 'RoboLabs Grades1–12,max8/instructor: Thanksgiving3days417full/237half;Christmas4days556/316. Three explicitly named California camp venues produce9 venue/date rows, not3 operators. Own lunch, extended20USD/hour;2026summer695/395 and separate BattleK–7summer2025 not transferred to2027 or current Kindergarten admission. English/foreign/cancel unknown.',
 'Snapology Greensboro official page recovered in browser after directHTTP403; selected rendered excerpts retained, not full rawHTML. AttendingKindergarten/self-toileting/staffcannotmedicate and waiver gates. Winter table3days twice versusfour-dayintro,150/175full225/275extended;spring22–26Mar2027 224/249full324/349extended. Ten schoolholiday dates including2past;8future plus2winter plus1spring=11rows. Staff medication/lunch/no heating/pickup/cancel conditions read; EN unknown.',
 'STEAMUP Orlando:5–15table vs3–15body, SpringK–5/6–8 distinct projects. Thanksgiving closed26Nov=>4actualdays;Winter closed24/25/31Dec/Jan1=>6actualdays, deadline15Nov2026. Independent source-to-calendar weekday/closure enumeration prevents false visits. Spring15–19Mar2027five days. From250 only Spring explicitly perweek,84care/1.85perlate-minute, no finalinvoice/EN inferred; schoolVEXmenu notcampqualifier.',
 'STEMRise three winter tracks7–13/9–16/12–18,20Dec2026–10Jan2027 seasonalwindow only. OnsiteMarkham;NorthYork/RichmondHill/Scarborough onlineonly, no4false onsite rows. Pricesquote/9.9trialnotcampfee,ENunknown;camprefund5/20/25percent and Chineseversionprevails acknowledged. GeneralcourseFAQ flat50/100 notcamp, referral/stacking conflicts preserved. No dated familyICS from window;Researchfuture.',
 'SantaÚrsula summer7–15 not generalactivityminimum6. Actualdated2027cards10–16July/17–23July51700MXN,10–23July98500. First cardstart repeats but distinct end/variant prevents duplicate IDs. Generichome16–23/old2026hero conflicts explicit. Internationalcommunity notENimmersion. Accidentpolicy150000MXN limit through exit/illness exclusions, not invented10000deductible or allmedicalcosts. Cancel15/3day/<=3day boundary; phones/webmessages; instructor+safety/boarding read. Oscar onlyafter7thbirthday.',
 'CostaRica Avanza football11–15/18–22Jan2027 actuallyGSDGuácimaAlajuela:ownpage5–17vsFAQ6–17, feeunknown,mandatoryAdidasuniformpurchasedseparately, lunchincludedvsbring. GeneralfootballnotSTEM/scouting or guaranteedMadridroute. Spanishcoaches/ESsite notteachinglanguage. AmoraNature4Jan–6Febwindowfamily:campage/EN/fee/hoursTBA;USschool3–13 and adjacentCorcovado10–13/10–15/5–15research/tour notadmission. UCRcall is for2027 instructors.',
 'Mákemáke ClassicGrade2–8 remains higher authority than generic6–17;Englishallactivities/translationconfirmed.535000CLP VAT,roundtripSantiagobusincluded, departsDay1at13/returnsfinalday13;40/42busseatsnotguaranteed, oldFAQLaReina vsratesLasCondes stop. Directtransport20000CLP exception vsno-discountclaim preserved. Refundbefore20Dec26minus21percent,limitedseriousillness/emergencyafterminus30;exact20Decunknown. TeenGrade9–11future twoactual2027slots;notchild6/9 orJuniorCounselorFULLcohort.',
 'Tamwoodcampcurrentlink redirects to currentILAC ceasedoperations/allprogrammingcancelled notice, despite cached2027offer. No exact noticeyear inferred and no existingTamwood/ILACrows found; no new open programme admitted. Qwanoes/Kamin403,FunWithBots406/currentClosed and Amoraeducation404 are gaps, not verified wholecamp programmes.',
 '3071events/1740camp-learningrows;594dossiers/36countries/893dossierURLs;129familycomparisons.34newdatedcatalogue rows,41newfamilyICS(10actualSTEAMUPdaysreplace2broadwindows plus15Novwinterregistrationdeadline),2320familyICS/104exhibitionICS.1277manageddated/69legacyreuse/39seasonwindows. Allcountries249/82withrecords/0fullyaudited.52directattempts45HTTP200/7errors plus1browserread with selectedexcerpts;8programmegroups not52completedoperatoraudits. Worldwide expandedgoal active; no external applications/messages/payments/accounts/automations.'
]
audit=dict(asof='2026-10-05',version=90,status='progress',scope='USA/Canada real holiday and2027 curriculum; Mexico/Chile generalboarding and fullcost/contract; CostaRica localfamily/sport boundaries. Worldwide task remains active.',
 new_dossiers=19,new_operator_groups=8,operator_groups_including_existing_deepening=9,new_calendar_rows=34,new_family_ics=41,updated_dossiers=['makemake'],corrected_existing_event_ids=changed,
 programme_dossiers=594,countries_with_dossiers=36,official_dossier_urls=893,country_dossier_counts=byiso,programme_slugs=[q['slug'] for q in fresh],findings=c['gaps'][-5:],
 calendar=dict(events=3071,learning_records=1740,family_ics=2320,exhibition_ics=104,managed_dated_rows=1277,reused_legacy_events=69,season_windows=39),fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
 next_priority='Continue Switzerland/France/Spain/allEurope, Taiwan/Singapore/Korea/Japan/Asia, Americas and allworldwide2026–27 general/technical camps, exact language/foreign intake/grades/DOB/fees/contracts, schoolresults/history, competitions/leagues/exhibitions and family routes.')
def write(stem,v):
 t=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(t)
 (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(t)
write('americas-camp-audit-v90',audit)
write('americas-camp-source-receipts-v90',dict(asof='2026-10-05',version=90,scope='52 direct HTMLattempts/45HTTP200/7errors;oneprimary browserread with selected observedexcerpts, not fullHTML. No new PDFs. Relevant sections, not wholeworld/operator audits.',sources=receipts,browser_primary_reads=browser,dossier_source_urls_added=added,external_actions=external,notes=[
 'RawHTML andselectedbrowserexcerpts retained outside checkout; public export onlyparaphrases/URLs/hashes/errors. PartialStarShowMore/blockedpage openlymarked.',
 'Primary language, optional translation and application language separate; ages/grades/places/fullinvoice never inferred from marketingname. Actualdaycalendars excludeholidays. Worldwidecoverage active.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=90:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',evidence='v89nativepublication succeeded;commit21d9f87320b8d6b38a5724a3ce475e1c294e4c3b;deploymentappgdep_6ac41d83a9d08191a9ab8b75d72c45ee. Worldwide expandedscope retained.')
plan['latest_validation']=dict(version=90,asof='2026-10-05',status='Independent primary/preservation/calendar verification; nativepublication receipt separate',events=3071,camp_learning_records=1740,programme_dossiers=594,countries_with_dossiers=36,official_dossier_urls=893,family_ical=2320,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=byiso)
plan['americas_camp_programme_audit_v90']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=594,countries=36,swiss=84,generated_calendar_entries=1277,reused_legacy_events=69)
for q in plan['requirements']:
 if q['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
  q['evidence']='v90:594programme/venue/formatdossiers36countries;19new+MákemákeClassicdeepened,34newdatedcataloguerows/41familyICS,893dossierURLs. Ownholidaycurriculum/fees/contracts/age/language/operationalavailability. Worldwidecompletenessnotachieved.'
entry=dict(version=90,asof='2026-10-05',status='progress',scope=audit['scope'],new_dossiers=19,deepened_dossiers=1,new_calendar_rows=34,new_family_ics=41,official_primary_sources=31,not_complete_worldwide=True)
plan.setdefault('research_passes',[])[:]=[q for q in plan.get('research_passes',[]) if q.get('version')!=90]+[entry]
plan['next_research']=[audit['next_priority']]
plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05';write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=89','?v=90').replace('data-ui-version="89"','data-ui-version="90"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_americas_camp_audit_v90.json" download>Америка: зимние смены, пансионы и полная стоимость ↓</a> · <a href="downloads/STEM_americas_camp_source_receipts_v90.json" download>Источники и границы проверки ↓</a> · '
anchor='<a href="downloads/STEM_asia_camp_audit_v89.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=594,new_dossiers=19,deepened_dossiers=1,new_calendar_rows=34,new_family_ics=41,source_urls=893,goal='active')))
