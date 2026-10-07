"""Publish selected source receipts in the local build; keep raw bodies private."""
import collections,hashlib,json,subprocess
from camp_americas_v126 import ROOT,BASE,CHECKED,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-americas-primary-v126'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
cp=d['camp_programmes'];old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
assert len(cp['profiles'])==999 and len(now)==3741 and all(now[k]==v for k,v in old.items())
before={p['slug']:p for p in b['camp_programmes']['profiles']};after={p['slug']:p for p in cp['profiles']}
assert after.keys()-before.keys()==set(NEW)
assert [k for k,v in before.items() if after[k]!=v]==UPDATED
assert d['camp_planning']==b['camp_planning'] and len(d['camp_planning']['offers'])==48
sources=[]
for f in sorted(P.glob('receipt-*.json')):
 for x in json.loads(f.read_text()):
  q=dict(x,checked=CHECKED,retrieval_method='direct_public_http',content_scope='Selected programmes, ages/classes, dates, price components, room and equipment details, and contractual admission/cancellation clauses. Not whole websites or countries.')
  if q.get('status') in [200,202]:
   name=q['key']+('.pdf' if (P/(q['key']+'.pdf')).exists() else '.html')
   raw=(P/name).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
   q.update(raw_filename=name,body_snapshot_retained=True)
   if q.get('status')==202:q.update(content_status='challenge_not_programme_evidence',resolution='HTTPS handbook returned a 254-byte HTML challenge; own HTTP PDF fetched separately. No PDF text claimed from challenge.')
   elif 'page-not-found' in q.get('final_url',''):q.update(content_status='soft_404_not_programme_evidence',resolution='HTTP200 redirected to own page-not-found. Not a school-break syllabus or proof of operator closure.')
   elif q['key'] in ['explora-extremo','explora-summer-2027']:q.update(content_status='homepage_fallback_not_specific_programme',resolution='Guessed route returns general home. Correct own linked hyphen Kids/Xtreme/family pages read separately; no new dates inferred.')
   elif q['key'] in ['museo-api','museo-root-api']:q.update(content_status='selected_public_search_empty',resolution='Public own search returned []; limited endpoint/search, not proof that no camps exist.')
   else:q['content_status']='selected_pdf_clauses' if name.endswith('.pdf') else 'selected_html_clauses_or_discovery'
  else:q.update(body_snapshot_retained=False,content_status='retrieval_error_not_content_evidence',resolution='Guessed route404 or temporary DNS failure; own linked routes/retries used where available. No conclusion that operator/country has no camp; no login or form action.')
  sources.append(q)
assert len(sources)==64 and sum(q.get('status')==200 for q in sources)==56
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
blocks=collections.Counter(e['block'] for e in d['events'])
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT')
expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert (family,expo)==(2943,104)
checks=[
 'InnEd own Winter2026:5–12 AND JK–G6, open nonstudents/beginners, Dec21–23/28–30 Mon–Wed09–16. $240 per three-day block,450 both for onechild, not dayprice/siblingdiscount. Math/play/YoungEngineers motorized models; build changes byblock/age. Enrollment Agreement overrides general monthlyclass makeup/termination; separate LOL waiver. EN teaching/currency code and full lunch/material package not established.',
 'Envision existingCP299 refreshed: own WinterDecember2026landing21–24/28–31Dec against product22–24/29–30 withoutyear and pickeronlyDec30. Age5–8/9–13/ramprobotics/Roblox/Flowlab/3D retained but dated admissions not inferred. Campno-refund/discretioncredit12months differs fromweeklyclasses; summerfrom200notwinterprice. One existingdossier updated, no duplicate or new conflictingevent.',
 'Frost2027two-week WawayandaenteringG2–7/FarmenteringG2–10/DurangoboysG3–8AND≥8: four own dates Jun27–Jul9/Jul11–23/Jul25–Aug6/Aug8–20. Generalcamp not guaranteed robotics. TierA/B/C sameexperience/subsidyvoluntary, not automaticcheapquote;5%registration and250deposit separated. OvernightMarch1/June1 rules not copied to day/family. SugarloafG2–3 and SeedlingsG2–4 haveonlysessioncodes, not inventedweeklydates;Seedlings1B/4B boys versus1A/4A girls.',
 'Frosthousing: mainheated/electriccabins vsfarmyurtsnoheat/electric/water/communalbathhouse. Specificratios differ across ownFAQ, notuniversal1:4promise. Own28page2026handbook selecteddevices/communication/nightcare clauses:electronics/Yondr,notunlimitedchildphones; archive2026notbinding2027. Staff/medicalandfacilityclaims source-attributed, not independent inspection.',
 'Frostday2027nineownweeks butPathfindersG1–5onlyweeks1–8,8datedrows. LEGOweek1G2–3 versusweek3G3–5,notSPIKE/leaguepreparation. InventorWorkshopweek2G4–5 slime/eggdrop/MakerLab;Garageweek8G2–3 prototypes/test/pitch. Allclassgates keptunknown frombirthyear. Dayfees/FAQstill2026:basic485/400/315,specialty495/410/325,TierD250/260 onlyfive localschooldistricts,bus125/deposit50/May1not2027quote. Baglunch and pickup/allergen differences needcurrent agreement.',
 'Frost17futuremainfamilyintervals Oct2026–Jun2027, threefarmfamilyintervals: parentaccompanied residential, notdropoffchildboarding. Specialveteran/cancer/autism/adoptivefreeconditions not generalfamilyquote. SpringFarmMay21–23 atRanch whileotherfarmyurts;Oct285two/380threenightppallinclusive,May2027unknown. OldSeptemberonechildfree/adult not extended. Mother/Father conditionalfreeparent promotion notedwithout automaticfamilydiscount.',
 'Frostown2026–27GFRonepage table:225participanttwo/300threenightsplusseparateroom/cabin;≤5participantfree not wholelodging. Two=4mealsSatbreakfast–Sunbreakfast,three=7Sat–Mon,notallFridayarrivalfood. Room/fulllodge rates distinguished;hostelsharedlimiteddates,occupancyunknown.17familyweekends publishedperiods,notacceptedbookings;longweekendtwo/three-nightchoices disclosed.',
 'FrostWinterFamilyownonepage Dec27,2026–Jan2,2027:select2–6nights,minimum2,arrivalsSun–Thu14–20/out12:30. Participant225/300/385/465/545;Lakeview407/611/712/814/930,Castle353/530/618/706/815,cabin173/259/302/345/395 and4roomlodge per-room same.14linenoptionalcampstyle,13checkoutlunchover5exceptJan2,checkin dinner included. DistinctwintervsGFRrates. Seasonwindow not fixedseven-dayevent, no artificialfamilycalendarrow. Two selected ratePDFpages visually checked.',
 'Explora correctlylinkedKids6–12/Xtreme13–17/parent-childageunknown, ownMorelosElFuerteBambu/QuintaMargarita not CDMXoffice. Nature/sustainability/generaladventure not robotcourse; guide≤8/facility/menu/certification claims are ownmarketing. Onepagepacking excludes electronics; nightcount/rooms/foreignintake/rates/cancellation/explicitESteacherunknown. Ownverano2026headingwait2027 vsJul13–18/20–25withoutyear; guessed2027/underscore routeshome not newdatedprogrammes.',
 'CodeREVowncoursesexplicit2024archive,threehistoricalcurricula: Minecraft detailed6–10 vsMicroheading6–9/G1–2/G3–5;Roblox8–10G3–5assets/Lua/level2priorcode;REVRobots8–10 Arduino/motors/sensors/blockcode withsimulatorORphysical,optionalCreatorBot$50discountnotkitprice,140hcurriculumaccessnotweekcontacthours. AnotherRevEngineeringmissingAges/Grades5–8notages5–8forOscar. MainwinterweekdayWedDec25 versusDec22 table/SantaMonicaDec22–24/29–Jan2withoutyear excluded2026–27calendar. Undated125day/369.99three/492.99four not futurequote. Credit≥week validonecalendaryear,cashdiscretion≥3weeksnotautomaticrefund. No guaranteedphysicalkit/VR/Englishteacher/currentcampus/new2027curriculum.',
 'CISVMexicosendingchapter routeVillageexact11/28days,2boys2girls+21adultleader,selectedinternationalinvitation,Englishcamp-life explicit notrobotlesson. Receivingcountry notallMexico; citizenship/CRresidency not automaticchapteradmission. Matvey11in2028/Oscar11in2031 withcutoffstillneeded. Fees/camp2027allocationunknown; not currentkidsfreebookableworldcamp.',
 'HollandBloorviewownWinter2027futurejunior6–10/Jan20–Feb24 butownformaldiagnosis/possiblefamily1:1support/ageasofDec31: specialisedadmission, not genericopenholidaycamp. Codinggeneric8–14 vswinter9–14 retainedgap. No healthassumptions orapplication. CostaRicaownMuseoselectednews/search[]/guessed404andCISVDNS are limitations,not countryabsence; existingUCR2025/Amora2027 notduplicated. DigitalDragonold2025/2021 notnew2027camp.',
 'All3695prior event and979unchanged programmeobjects/48completepriorbudgetobjects preserved; onlyEnvisionCP299 refreshed.19newcurricular/seasonal/route dossiers across5operators,46datedrows and46familyICS additions. Dollarcurrencycode/currentfees notproved: zero newcalculatoroffers ratherthaninventedfullquote. Worldcompetitions/exhibitions/camps/schools/history/routes scope keptactive;0countriesfullyaudited.'
]
publication=dict(status='prepared_local_not_published',project_id='appgprj_6abd44bca1348191809b7260dcb46d87',
    reason='Fresh native get_site returned SitesConnectorError: Sites project not found on the initial two calls and final retry; list_sites returned no visible projects. No source credential, save or deploy attempt for v126.',
    last_confirmed_published_version=125,last_confirmed_deployment_id='appgdep_6ac4ff3f3c7481918fe3d668d24574b0',
    last_confirmed_success_at='2026-10-06T14:02:09.803197+00:00',production_browser_qa=False)
audit=dict(version=126,asof=CHECKED,status='progress',scope='Selected Americas general/technical day, residential and accompanied family programmes, plus later CISV sending-chapter route. Not a world camp census or independent world ranking.',
    events=len(now),competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],camp_learning_records=blocks['Лагеря'],programme_dossiers=len(cp['profiles']),countries_with_dossiers=39,
    official_dossier_urls=len({s['url'] for p in cp['profiles'] for s in p['sources']}),editorial_scenarios=len(cp['shortlist']),coverage_gaps=len(cp['gaps']),league_profiles=len(d['league_guide']['profiles']),
    budget_scenarios=48,budget_providers=24,budget_programme_dossiers=37,new_budget_scenarios=0,new_dossiers=19,new_dossier_slugs=NEW,
    new_programme_operators=['InnEdAcademy','FrostValleyYMCA','ExploraCampamento','CodeREVKids','CISVMexico'],updated_dossier_slugs=UPDATED,new_event_ids=sorted(now.keys()-old.keys()),updated_event_ids=[],
    unchanged_dossier_objects=979,updated_dossier_objects=1,unchanged_event_objects=3695,unchanged_prior_budget_objects=48,source_retrieval_attempts=64,direct_successful_bodies=56,
    retrieval_errors=7,challenge_responses=1,pdf_download_files=5,pdf_text_pages_extracted=32,new_visual_pdf_checks=2,family_ical=family,exhibition_ical=expo,
    goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,publication=publication,checks=checks,verification={})
for name in ['independent-check.json','functional-check.json']:
 f=P/name
 if f.exists():
  q=json.loads(f.read_text());assert q['status']=='passed' and q['version']==126;audit['verification'][name.removesuffix('.json')]=q
def write(stem,v):
 text=json.dumps(v,ensure_ascii=False,indent=2)+'\n'
 (ROOT/'data'/f'{stem}.json').write_text(text)
 (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(text)
write('americas-camps-audit-v126',audit)
write('americas-camps-source-receipts-v126',dict(version=126,asof=CHECKED,scope=audit['scope'],sources=sources,pdf_download_files=5,pdf_text_pages_extracted=32,
    visual_pdf_pages_checked=[dict(filename='frost-lodging-prices.pdf',page=1),dict(filename='frost-family-prices.pdf',page=1)],external_actions=external,
    primary_reader_limits='64direct attempts/56HTTP200bodies includes home fallback, soft404 and public search, not56campwebsites fullyread. FivePDF32pages text-extracted, only two selected tables visuallyread;28pagehandbookyear2026reference. All raw bodies/images private outside repo. No accounts/consent/forms/messages/applications/booking/payments.'))
lines=['# Лагеря: подробное дополнение по Америке, версия126',
       'Подготовлено локально 6 октября2026. Обновление ещё не опубликовано: Sites возвращает «Sites project not found». Последняя подтверждённая публикация — версия125.',
       'Добавлены19 досье программ/сезонов/маршрутов у пяти операторов,46 датированных карточек; одно существующее Envision обновлено. Это не19 независимых лагерных организаций и не полный мировой рейтинг.',
       '## Весь реестр и приоритетные направления',
       'Локальная база:999 досье в39 странах. Досье включают разные программы одного оператора, архивы и будущие возрастные маршруты. Дата проверки указана в каждой карточке; весь реестр не перепроверен сегодня.']
table=['| Страна | Досье |','|---|---:|']
counts=collections.Counter(p['iso'] for p in cp['profiles'])
for iso in ['CHE','FRA','ESP','TWN','SGP','KOR','JPN','USA','CAN','CRI','MEX','BRA','PAN']:
 table.append('| '+next(p['country'] for p in cp['profiles'] if p['iso']==iso)+' | '+str(counts[iso])+' |')
lines.append('\n'.join(table))
lines += ['## Что рассматривать для семьи',
          '- Ближайшая точная техническая проба: InnEd,21–23 или28–30 декабря2026,5–12,по3дня. Язык ведущего и полный состав счёта пока подтвердить.',
          '- Общее семейное знакомство с США: Frost тематические выходные или WinterFamily с родителями. Зимой выбирают2–6ночей; деньги за участников и комнату считают отдельно.',
          '- Maker и первый самостоятельный пансион: Frost дневные Inventor/LEGO и младшие Wawayanda/Sugarloaf. Важен реальный школьный класс; LEGO Masters не обещает программируемых роботов.',
          '- Мексика: Explora Kids6–12 или проба Padres e Hijos; новые точные даты2027 и прайс ещё нужны. Xtreme13–17 пока старший маршрут.',
          '- CISV Village — будущая международная самостоятельность через national chapter и делегацию: ровно11лет,28дней,английская среда. Для Матвея возраст наступит2028,дляОскара2031,но cutoff/отбор проверяются отдельно.',
          '- Envision расходится по датам; CodeREV подробный syllabus2024. Ни один не представлен как гарантированная новая зимняя смена.',
          '## Новые подробные досье']
for slug in NEW:
 p=after[slug]
 lines += ['### '+p['provider'],p['country']+' · '+p['place'],'**Возраст/класс:** '+p['age'],
           '**Формат:** '+', '.join({'day':'дневной','boarding':'детский пансион','family':'с родителями','online':'онлайн'}.get(k,k) for k in p['formats']),
           '**Программа:** '+p['programme'],'**Когда:** '+p['timing']['label'],
           '**Цена:** '+p['price']['label'],'**Включено:** '+p['price']['included'],'**Доплаты:** '+p['price']['extras'],
           '**Оплата и отмена:** '+p['price']['deposit'],'**Проживание:** '+p['accommodation'],'**Язык:** '+p['language'],
           '**Матвей:** '+p['family_fit']['matvey']['detail'],'**Оскар:** '+p['family_fit']['oscar']['detail'],
           'Источники: '+', '.join('['+s['title']+']('+s['url']+')' for s in p['sources'])]
lines += ['## Состояние работы','Прежние3695 карточек соревнований, выставок и обучения сохранены без изменений; все48 семейных частичных смет сохранены. Только EnvisionCP299 уточнён среди прежних досье.',
          'Проверка нового блока:64 прямых обращения к первичным сайтам/PDF,56 ответовHTTP200,пятьPDF. Ошибки/домашние страницы вместо нужного курса/старые документы явно отделены от новых подтверждённых смен.',
          'Мировой аудит остаётся активным. Полностью изученных стран пока нет. Заявки, сообщения, согласия, бронирования и оплаты не выполнялись.']
(ROOT/'dist/downloads/STEM_америка_лагеря_v126.md').write_text('\n\n'.join(lines)+'\n')
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=126:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native125 success2026-10-06T14:02:09.803197Z; deployment appgdep_6ac4ff3f3c7481918fe3d668d24574b0; base '+BASE+'. Native126connection now project_not_found, local research progress. Worldwide goal active.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','budget_providers','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected Americas clauses and complete local build checked; v126 not published, fresh nativeprojectaccess unavailable.'
plan['americas_camp_programme_audit_v126']=audit
plan['current_publication']=publication
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for x in plan['requirements']:
 if x['id']=='unified_database':x['evidence']='v126 local:3741events/999programme dossiers/39countries/1541primary dossierURLs.19newAmericasprogramme dossiers/46datedrows;3695oldevents/979dossiers/48offers unchanged,EnvisionexistingCP299refreshed. CompleteSQLite/JSON;nativepublicationunavailable.'
 elif x['id'] in ['camps','family_top_picks']:x['evidence']='v126 local:999dossiers/236editorialscenarios. InnEdDecember2026, Frost2027schoolgates/panсион/day/maker/17familyweekends/winter2–6nights,ExploraMorelosKids/family,CodeREVactualcourseswithnewdatesTBC,CISVMexicofuture11yearroute. AllpriorSwiss/France/Spain/Europe/Taiwan/Singapore/Korea/Japan/Canada/LatAm/generalENESRUscope intact;notcompleteworldwide.'
 elif x['id']=='camp_full_pricing':x['evidence']='v126:48existingpartialbudgets preserved,noneinvented. InnEd240three-day/450both;Frost2027tiers+5%,separatefamilyparticipant/lodging/nights,andarchiveday2026;CodeREVundatedprices not2027,Exploraquoteunknown. Dollarcontextnotconfirmedcurrencycode,availableplace/class/teacherlanguage/fullinvoice gates explicit.'
 elif x['id']=='camp_calendar_2026_2027':x['evidence']='v126:46newexactdatedrows and46familyICS additions:InnEd2,Frost12overnight/12day/20accompaniedfamily. Sugarloaf/Seedlingssessioncodes notinventedweeklydates;WinterFamilychoose2–6nightseasonwindow notfixedseven-daycamp;Envision/CodeREV/Exploraconflicts excluded.2943familyICS/104exhibition,alloldUID/contentpreserved.'
plan['research_passes']=[x for x in plan.get('research_passes',[]) if x.get('version')!=126]+[dict(version=126,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=19,updated_dossiers=1,new_calendar_rows=46,new_budget_scenarios=0,official_primary_retrieval_attempts=64,pdf_download_files=5,not_complete_worldwide=True,publication='prepared_local_not_published')]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=125','?v=126').replace('data-ui-version="125"','data-ui-version="126"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"'
link='<a class="button secondary" href="downloads/STEM_americas_camps_audit_v126.json" download>Америка · программы, пансионы и семейные заезды</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text();anchor='<a href="downloads/STEM_asia_camps_audit_v125.json"'
link='<a href="downloads/STEM_americas_camps_audit_v126.json" download>Америка: смены, классы и семейные цены ↓</a> · <a href="downloads/STEM_americas_camps_source_receipts_v126.json" download>Источники и ограничения ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps({k:audit[k] for k in ['version','events','programme_dossiers','new_dossiers','budget_scenarios','family_ical','worldwide_complete','publication']}))
