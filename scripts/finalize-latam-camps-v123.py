"""Public research receipt without raw bodies, credentials or complete-world claims."""
import collections,hashlib,json,subprocess
from camp_latam_v123 import ROOT,BASE,CHECKED,NEW,MAN,PER
P=ROOT.parent/'stem-family-atlas-work/camp-latam-primary-v123'
d=json.loads((ROOT/'data/catalog.json').read_text());b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']};cp=d['camp_programmes'];offers=d['camp_planning']['offers']
newids=sorted(now.keys()-old.keys());assert len(newids)==1 and all(now[k]==v for k,v in old.items())
assert len(cp['profiles'])==950 and [q['slug'] for q in cp['profiles'][932:]]==NEW and cp['profiles'][:932]==b['camp_programmes']['profiles']
assert d['camp_planning']==b['camp_planning'] and len(offers)==43
sources=[]
for f in sorted(P.glob('receipt-*.json')):
 for item in json.loads(f.read_text()):
  q=dict(item,checked=CHECKED,retrieval_method='direct_public_http',content_scope='Selected programme, age, format, fee, timetable and contract clauses or discovery; not entire websites/countries.')
  if q.get('status')==200:
   suffix='.pdf' if (P/(q['key']+'.pdf')).exists() else '.html';name=q['key']+suffix;raw=(P/name).read_bytes()
   assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
   q.update(raw_filename=name,body_snapshot_retained=True,content_status='selected_pdf_clauses' if suffix=='.pdf' else 'selected_html_clauses_or_discovery')
  else:q.update(body_snapshot_retained=False,content_status='retrieval_error_not_content_evidence')
  sources.append(q)
assert len(sources)==29 and sum(q.get('status')==200 for q in sources)==23
readerfiles=['primary-reader-1.txt','v123reader2.json','v123reader3.json','v123reader4.json','v123reader5.json']
readers=[dict(filename=name,bytes=(P/name).stat().st_size,sha256=hashlib.sha256((P/name).read_bytes()).hexdigest()) for name in readerfiles]
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
blocks=collections.Counter(q['block'] for q in now.values());family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT');expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert (family,expo)==(2873,104)
audit=dict(version=123,asof=CHECKED,status='progress',scope='Selected Mexico/CostaRica/Peru technical curricula, Expanish2027 general language packages and ManqueChile2027 organization admission. Eighteen dossiers across nine programme operators, not eighteen independent top-ranked camps. Previous worldwide competitions, exhibitions, schools, routes and camp work preserved.',events=len(now),competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],camp_learning_records=blocks['Лагеря'],programme_dossiers=len(cp['profiles']),countries_with_dossiers=39,official_dossier_urls=len({s['url'] for p in cp['profiles'] for s in p['sources']}),editorial_scenarios=len(cp['shortlist']),coverage_gaps=len(cp['gaps']),league_profiles=len(d['league_guide']['profiles']),budget_scenarios=43,budget_providers=21,budget_programme_dossiers=len({q['slug'] for q in offers}),new_budget_scenarios=0,new_dossiers=18,new_dossier_slugs=NEW,new_programme_operators=['LogiscoolMexico','PuenteDigitalMexico','UTN-IAC','UCR-CIMM','ParqueLaLibertad/ColibrIA','ExpanishCostaRica','INICTEL-UNI','IESVonBraun','MovimientoManqueChile'],updated_dossier_slugs=[],new_event_ids=newids,updated_event_ids=[],unchanged_dossier_objects=932,unchanged_event_objects=3657,unchanged_prior_budget_objects=43,source_retrieval_attempts=29,direct_successful_bodies=23,retrieval_errors=6,pdf_download_files=2,new_visual_pdf_checks=1,family_ical=family,exhibition_ical=expo,goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,checks=[
 'Logiscool nine separate curricula under one network: WeDo6–9 inpersononly; Minecraft7–14 PC/Mac licence, not Android/Xbox/PS4; RobloxMultiverse9–12 ownaccount/classroomclosedproject; CreatorLab10+ five days; generative9–12 five days; illustration8–10 online6 vs generic8;3D12–15 not printedartifact guarantee. No new dated intake/price/ENESRU teaching promise.',
 'Logiscool Interlomas no open coming-weekcamps;1500MXNhalfday/800deposit and credit deadline31Dec2023 are archival, not2027. GenericCGC≤30%advance/rest8days vs oldlocal800/5days; cancellation11/22% ten-dayboundary ambiguity, medicalproportionate refund. No acceptedcontract, no bookedseat.',
 'PuenteDigital CórdobaVeracruz not CostaRicaSanJosé. Jul13–Aug7,2026 past;1499MXN/week20h vs3990MXN/full4week80h, takehomeArduino onlyfullpackage;999advance withinbase. Eightmax, ownsnack,15% siblingonrequest, seven-daymarketingguarantee, contradictoryBellaVista/PlazaSanJosé. Stale3/8availability not current.',
 'UTN IAC Scratch firstlocalpublicschoolgroup2025, sixlessons/twelveparticipants/freehistorical. July/December2025 futureplan not2026–27 dates or foreignintake. UCR CIMM9–12 ANDgrade4–6; Jan27–30,2026 archive08–11:30 maths/science/art, notrobotics. PLLAI12–15 Jul7/8/10/14/17,2026 five3hmornings15h not elevenfulldays; oldregistrationtext conflictsheader.',
 'Expanish currently suspended/resumeSummer2027 withoutexactdates/price;12–17 too oldforboth2027. ExplicitSpanishlessons only language_lessons.15/20 lessons conflict; DayrequirementparentMadrid contradictsCostaRicacampus;LaFortunaHotelFaroArenal notSamarafooter. Fourstudentcabin/fullboard vsdaylunch distinct, weekendexcursionsonly2+weeks; generic15%discount notapplied.',
 'INICTEL own2026PDF selectedreader curriculum/timetablecost:4×12h=48h,Feb2–27 MonWedFri09–13:15 withbreak;650PEN wholebundle not4×650. mBotbasic vsadvancedpriorrobotics, introductoryChatGPT/MakeCode;under13teachercontrolled AI questionkept. DirectPDF403/readerselectedclausenotlocal3pagevisualproof. VonBraun onepage localPDF andimage checked,1or2days/week/8–11/SPIKE Essential/Surco;year2026URLnotprinteddate,fee/time2027unknown.',
 'ManqueChile2027 IllapelJan4–10 exact butorganizationrouteManqueChile/IFM-SEI. Age/fee/language/nightfamilyformatunknown;bilanguageannouncementnotinstruction. Newcalendaradmission organization_route replacesdefaultopen_application onlyexplicitnewvariant;allpriorcalendarobjects preserved. Direct403 distinguished primaryreaderbody.',
 'MINERD original/wwwTLSwronghostname, reader502: TLS notdisabled, fullpublicschoolbases not obtained, no fake openforeignfreecamp. CampHopevolunteerfee/oldyoungestchild notchildholidayfee;UWCselectioncamp notpublicvacationcamp. No newDOMprofile or count inflation.',
 'All932 priorprofiles/3657events/43budgetobjects preserved; eighteen new programme dossiers, one future precise2027 calendarrow, nine curricularLogiscoolprofiles not nineproviders. New2026/2025 archives kept outsidefuturecalendars. PriorCHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN and all worldwide blocks remain;goalactive/0fullyauditedcountries.'
 ])
# There are nine named operators; their curricula/packages account for eighteen dossiers.
audit['verification']={}
for name in ['independent-check.json','functional-check.json']:
 f=P/name
 if f.exists():
  q=json.loads(f.read_text());assert q['status']=='passed' and q['version']==123
  audit['verification'][name.removesuffix('.json')]=q
def write(stem,v):
 s=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('latam-camps-audit-v123',audit)
write('latam-camps-source-receipts-v123',dict(version=123,asof=CHECKED,scope=audit['scope'],sources=sources,web_reader=[dict(url=MAN,status='selected_own2027_announcement_body',direct_http_error='403',checked=CHECKED),dict(url=PER,status='selected_own2026_pdf_curriculum_timetable_fee_clauses',direct_http_error='403',checked=CHECKED)],private_reader_files=readers,pdf_download_files=2,visual_pdf_pages_checked=[dict(filename='peru-vonbraun-junior.pdf',page=1,scope='Age8–11,1or2days/week,SPIKE Essential,Surco address;noexactprice/date.')],external_actions=external,primary_reader_limits='Selected own programme/contract clauses and discovery, not all websites/allcountries/all2027intakes. One localPDFpage visually checked; INICTELprimarysearchreader clauses, not three-page localvisualverification. Rawbodies/PDF/reader captures private outside repository.'))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=123:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native122 succeeded2026-10-06T12:22:39.644543Z; commit '+BASE+'; deployment appgdep_6ac4e7f8a8708191959dbd8df78bd8a8. Worldwide objective active.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','budget_providers','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected LatAm curriculum, contract and admission gates checked; native publication separate.'
plan['latam_camp_programme_audit_v123']=audit
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for q in plan['requirements']:
 if q['id']=='unified_database':q['evidence']='v123:3658 events/950 programme dossiers/39 countries/1479 URLs;18 newLatAmdossiers/1future2027variant. Every3657oldevent/932profile/43budgetoffer preserved;fullportableJSON/SQLite.'
 elif q['id'] in ['camps','family_top_picks']:q['evidence']='v123:950 dossiers/39 countries/227editorialscenarios. LocalMexico6+WeDo,7+Minecraft,9+Roblox/AI,10+CreatorLab,12+3D;CRIuniversity/AIgradegates;Peru48htechnicalpackage/LEGO;Chileorg2027date/Expanish12–17later. Allpriorpriorityregionsandgeneral/day/boarding/familyENESRUscopepreserved. Notcompleteworldwide.'
 elif q['id']=='camp_full_pricing':q['evidence']='v123:43priorpartialfamilybudgets unchanged. ArchivedMex1500/8002023,Puente1499/weekvs3990/4wk2026,Peru650whole48h2026bundle retainedwithyear/unit;nonewfutureconfirmedfullbudget. Depositnotaddedtwice;fullcontractandlanguagesunknown.'
 elif q['id']=='camp_calendar_2026_2027':q['evidence']='v123:onefutureManqueJan4–10,2027withorganization_route/unknownage/night/language. Archived2025/2026notfuturecalendars;Expanishsummer2027noexactdates. FamilyICS2873/exhibition104;oldUID/contentpreserved.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=123]+[dict(version=123,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=18,updated_dossiers=0,new_calendar_rows=1,new_budget_scenarios=0,official_primary_retrieval_attempts=29,pdf_download_files=2,not_complete_worldwide=True)]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=122','?v=123').replace('data-ui-version="122"','data-ui-version="123"');anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_latam_camps_audit_v123.json" download>Латинская Америка · программы и допуск</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text();anchor='<a href="downloads/STEM_northamerica_camps_audit_v122.json"';link='<a href="downloads/STEM_latam_camps_audit_v123.json" download>Латинская Америка: 18 новых досье и условия участия ↓</a> · <a href="downloads/STEM_latam_camps_source_receipts_v123.json" download>Источники и ограничения ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps({k:audit[k] for k in ['version','status','events','programme_dossiers','new_dossiers','official_dossier_urls','family_ical','worldwide_complete']}))
