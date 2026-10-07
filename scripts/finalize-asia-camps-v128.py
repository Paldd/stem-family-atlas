"""Asian primary-source supplement and truthful local-only publication receipt."""
import collections,hashlib,json,subprocess
from pypdf import PdfReader
from camp_asia_v128 import ROOT,BASE,CHECKED,NEW,NEW_IDS
P=ROOT.parent/'stem-family-atlas-work/camp-asia-primary-v128'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
cp=d['camp_programmes'];before={q['slug']:q for q in b['camp_programmes']['profiles']};after={q['slug']:q for q in cp['profiles']}
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
offers={q['id']:q for q in d['camp_planning']['offers']}
assert len(after)==1034 and after.keys()-before.keys()==set(NEW) and all(after[k]==v for k,v in before.items())
assert len(now)==3775 and all(now[k]==v for k,v in old.items())
assert len(offers)==53 and all(offers[q['id']]==q for q in b['camp_planning']['offers'])
assert offers.keys()-{q['id'] for q in b['camp_planning']['offers']}==set(NEW_IDS)
sources=[]
for f in sorted(P.glob('receipt-*.json')):
    for x in json.loads(f.read_text()):
        q=dict(x,checked=CHECKED,retrieval_method='direct_public_http',content_scope='Selected camp syllabus, course-specific dates, age/language/admission, equipment, pricing and terms; not a whole-country or whole-site audit.')
        if q.get('status')==200:
            filename=q.get('raw_filename') or q['key']+('.pdf' if (P/(q['key']+'.pdf')).exists() else '.html')
            raw=(P/filename).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
            q.update(raw_filename=filename,body_snapshot_retained=True,content_status='selected_image_read' if filename.endswith('.jpg') else 'selected_pdf_clauses' if filename.endswith('.pdf') else 'selected_html_clauses_or_discovery')
        else:q.update(body_snapshot_retained=False,content_status='HTTP403_not_content_evidence',resolution='KAS primary web reader exposed selected public clauses and linked contract; HeadStart own images subdomain returned programme and full options PDF. No challenge bypass or account creation.')
        sources.append(q)
assert len(sources)==30 and sum(q.get('status')==200 for q in sources)==27
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT')
expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert (family,expo)==(2991,104)
publication=dict(status='prepared_local_not_published',project_id='appgprj_6abd44bca1348191809b7260dcb46d87',reason='Two fresh native get_site calls in v128 returned SitesConnectorError: Sites project not found. Versions126–128 have no push/save/deploy receipt. No older credential reused.',last_confirmed_published_version=125,last_confirmed_deployment_id='appgdep_6ac4ff3f3c7481918fe3d668d24574b0',last_confirmed_success_at='2026-10-06T14:02:09.803197+00:00',production_browser_qa=False)
brand=lambda n:'Enforex' if n.startswith('Enforex') else 'La Garenne' if n.startswith('La Garenne') else n.split(' · ')[0]
providers=len({brand(after[q['slug']]['provider']) for q in offers.values()})
budget_dossiers=len({q['slug'] for q in offers.values()})
assert providers==28 and budget_dossiers==42
pages=sum(len(PdfReader(f).pages) for f in P.glob('*.pdf'));assert pages==27
audit=dict(version=128,asof=CHECKED,status='progress',scope='Selected Asian camp curricula: Hong Kong exact English technical courses; Osaka English winter; Taiwan and Thailand detailed summer2026 archives; Korean local-admission gaps. Not a worldwide census or independent global ranking.',
    events=len(now),competition_records=1153,exhibition_records=189,camp_learning_records=2433,programme_dossiers=len(after),countries_with_dossiers=39,
    official_dossier_urls=len({s['url'] for p in cp['profiles'] for s in p['sources']}),editorial_scenarios=len(cp['shortlist']),coverage_gaps=len(cp['gaps']),league_profiles=len(d['league_guide']['profiles']),
    budget_scenarios=len(offers),budget_providers=providers,budget_programme_dossiers=budget_dossiers,new_budget_scenarios=3,new_dossiers=19,new_dossier_slugs=NEW,
    new_programme_operators=['CoboAcademyHongKong','OWISOsaka','KaohsiungAmericanSchool','HeadStartPhuket','BrightonCollegeBangkokVibhavadi'],updated_dossier_slugs=[],new_event_ids=sorted(now.keys()-old.keys()),
    unchanged_dossier_objects=1015,unchanged_event_objects=3769,unchanged_prior_budget_objects=50,source_retrieval_attempts=30,direct_successful_bodies=27,retrieval_errors=3,
    pdf_download_files=6,pdf_text_pages_extracted=pages,new_visual_pdf_checks=1,new_visual_source_image_checks=1,primary_web_reader_selected_clause_checks=1,
    family_ical=family,exhibition_ical=expo,goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,publication=publication,
    checks=[
      'Cobo nine age-specific course dossiers, not nine unrelated operators. Only five ownSchedule tables support Oct20–23Tue–Fri4lessons/8hours:JuniorSPIKEmorningWanChai,SeniorSPIKE/VEXafternoonWanChai,JuniorAIKowloonTongmorning,PrincipalHackathonWanChaimorning. Four emptySchedules do not inherit all four genericOctoberweeks. Five datedcatalogue rows;16 timed familyICS for four junior/senior courses, no12–14Hackathon in currentfamilycalendar.',
      'Cobo explicit English eachcourse,typical4–8sourceclaim. Junior6–8/Matvey8–9/Oscar5–6 needsbirthdayondate;Senior9–11Matveyonlyafter9;Hackathon12–14bothlater. SPIKEWeDo2.0+ScratchandJuniorAIcodingprerequisites retained. VEXhardwareprovided/laptopself;Blocks/C++/Pythonplatformpossibilitiesnotalladvancedcurriculaguaranteed. Arcadehandheldtakehome and400inclusiveambiguous,Juniorheading6–8vsbody8+. Generalpayment3weeks/nonrefund/weather/noholidaymakeupnottermcreditpromise. EarlySep30expired, buddy10notapplied. Course-specific3600budgetonlyoneeligiblechild each, notfull-daycare.',
      'OWISOsaka Dec14–18,2026 4–16externalday,Englishcamp-life. Tax10%added to70kexternal+5kmaterials+15kfirsttime=99kperchild;both198k. Oldseasonalparticipant82.5kdifferentpackage,school60knotassignedfamily. Noovernight/bus. Bannerregistrationsnotyetopen/checkOctober despitegenericregistertext. Schedulebuttonnohref. Previousactivities/cateredlunch/SnowParknotpromised2026. FootercommercialActTsukubataxincludedcontrastsOsakaWinterexplicitexcludes10%;SingaporewebsiteTermsnotwintercamprefund. Lunch/insurance/currentcontractunknown.',
      'KAS two2026themesfoodandFutureCity,primaryreaderPK–G5English-basedschooladmission. Gradeunknown;Englishwebsite/schoolcategorynotexplicitwholecampEnglish. FullschedulePDF2pages plusownlinkedcontract3pages:GlobalPlateJul13–17vsTermsSession1Jul13–20conflict;secondJul20–24. Archive16500regular15500early/lunch/9–15/refund beforeMay25fullafterhalfwithin15workingdaysnoneexcepthospitalinjuryillness,typhoon50%dailyratepartialno. Min10classvsPK2educators9childtable unresolved. 2026closed not2027closed;nofuture2027datedrows/quotes.',
      'HeadStart ownimagesprogrammeandfull8pageOptionsPDF confirmalllessons/instructions/activitiesEnglish/alllevels. Fivecoreagegroups4–5,6–7,8–9,10–14withjunior/senior,8–14EnglishFocus. ChaofahCity actualcamp notautomaticCherngtalay. Six2026weeksarchive,2027none. VEXoptionweeks3–5 andCYBERonecoding3–6threeblocks/weekincludein20000notpaidextension;6–7nocodinglisted. Food2snacks/tshirt/materials/basicaccident40kcamp-hoursincluded. Bus2000child requires≥4sameroute,twosiblingsnotguarantee. Late3000/week3–6,refund>14days80/<14none/exact14unresolved,school25notassignedfamily. Noaccount/passportupload/payment.',
      'BrightonVibhavadi ninepagebrochure,onepagesampleSTEMschedule,fourpageactivitydescriptions andvisuallyreadownBposter. BothA/BJune29–July17,2026day9–15archive. Bposterage3–12notinvented6–12fromA. A18/32/45kversusB21/40/55k;morningEN09–12,afternoon13–15generalorAI/robotics/coding. AIhands-onrecognition/ML/digitalcitizenship,manualbridges/towers/logicrealcurriculum;notdedicatedrobotkitproof. MorningEnglishlessonsnotalltechnicalteacherlanguage. Externaladmission/food/equipment/tax/refundunknown;differentKrungthepKreethacampnotmerged.',
      'YoungHoonGangbuk ownJuly27–31EnglishcooperationG1–6requiresGangbukarea;foreignvisitoradmissionnotproved. BranksomeCanadaToronto notJejuAsia camp. NTNUMandarinwinterJan4–15,2027/37000+1000notconfirmedEnglishSTEM, gaponly. ExistingHarrowAppi/Expedition27/SMIS/SFS/Laurus/LFS/Elev8 selectedrechecksnotduplicated asnewoperators.',
      'All3769 prior eventobjects,1015dossiers,50offers preserved. Nineteennewcurriculumdossiers overfiveoperators;6newdatedrows and17familyICS;3partialfeeoffers. Worldwide competitions, exhibitions, schools, history, familyroutes,allprioritycountries,fullSQLite/JSON retained;0countriesfullyaudited,goalactive.'
    ],verification={})
for name in ['independent-check.json','functional-check.json']:
    f=P/name
    if f.exists():
        q=json.loads(f.read_text());assert q['status']=='passed' and q['version']==128;audit['verification'][name.removesuffix('.json')]=q
def write(stem,v):
    t=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(t);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(t)
write('asia-camps-audit-v128',audit)
reader=(P/'kas-reader.txt').read_bytes()
write('asia-camps-source-receipts-v128',dict(version=128,asof=CHECKED,scope=audit['scope'],sources=sources,pdf_download_files=6,pdf_text_pages_extracted=pages,
    primary_reader_excerpts=[dict(url='https://www.kas.tw/dragoncamp/',filename='kas-reader.txt',sha256=hashlib.sha256(reader).hexdigest(),scope='Selected admission/theme clauses; not whole HTML. Direct HTTP403 retained separately.')],
    visual_pdf_pages_checked=[dict(filename='brighton-brochure.pdf',page=7)],visual_source_images_checked=['brighton-ai-schedule.jpg'],external_actions=external,
    primary_reader_limits='30 direct retrieval attempts,27HTTP200 including discovery/rechecks,not27wholecampwebsites. SixPDF27pages textextracted,onefeePDFpage/oneageposter visuallyread. RawHTML/PDF/text/imagesprivate. No forms/accounts/consent/messages/booking/payment.'))
lines=['# Азия: подробные лагерные программы, версия 128','Подготовлено локально 6 октября 2026. Версии 126–128 ещё не опубликованы: Sites возвращает «Sites project not found». Последняя подтверждённая публикация — 125.',
    'Добавлены 19 возрастных и учебных досье у пяти операторов, шесть датированных карточек и 17 записей семейного календаря. Это не 19 независимых лагерей и не полный мировой рейтинг.',
    f'Локальная база: 1034 досье в 39 странах; 53 частичные сметы. Все 3769 прежние карточки и 1015 досье сохранены. Весь реестр не перепроверен сегодня.',
    '## Практический выбор',
    '- Ближайшая техника: Cobo Hong Kong, 20–23 октября 2026. Junior 6–8, Senior 9–11; свой ноутбук и требования WeDo/Scratch. Четыре занятия по два часа, HKD 3600 за ребёнка. Подходящий день рождения, поздний приём и места ещё подтвердить.',
    '- Общая английская зима для обоих: OWIS Osaka, 14–18 декабря 2026, 4–16, внешние ученики. Двое впервые: JPY 198 000 с материалами, регистрацией и налогом. Пансиона и автобуса нет; питание, договор и открытие регистрации ещё уточнить.',
    '- Будущее лето в Таиланде: HeadStart — английский для всех занятий, VEX/coding только три выбранных блока в неделю. Brighton — английское утро и общий либо AI/robotics день; язык технических ведущих пока отдельно не доказан. Тарифы и смены в этих страницах пока архив 2026.',
    '- Тайвань: KAS Future City Builders — архитектура и объёмные модели, допуск PK–G5 из школ с английским обучением. Английский всей программы, новый набор и конфликт дат договора ещё требуют подтверждения.',
    '## Новые подробные досье']
for slug in NEW:
    p=after[slug];lines += ['### '+p['provider'],p['country']+' · '+p['place'],'**Возраст:** '+p['age'],'**Программа:** '+p['programme'],'**Когда:** '+p['timing']['label'],'**Язык:** '+p['language'],
        '**Цена:** '+p['price']['label'],'**Включено:** '+p['price']['included'],'**Доплаты:** '+p['price']['extras'],'**Оплата и отмена:** '+p['price']['deposit'],'**Проживание:** '+p['accommodation'],
        '**Матвей:** '+p['family_fit']['matvey']['detail'],'**Оскар:** '+p['family_fit']['oscar']['detail'],'Источники: '+', '.join('['+s['title']+']('+s['url']+')' for s in p['sources'])]
lines += ['## Оставшаяся работа','Мировая цель активна: соревнования, выставки, общие и технические лагеря, школы, история результатов и семейные маршруты. Приоритетные Европа, Швейцария, Франция, Испания, Тайвань, США/Канада, Сингапур, Корея, Япония, Коста-Рика, Мексика и LATAM сохранены. Ни одна страна не признана полностью изученной.']
(ROOT/'dist/downloads/STEM_азия_лагеря_v128.md').write_text('\n\n'.join(lines)+'\n')
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=128:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='v127 local research, independent/UI checks, committed '+BASE+';publication unavailable but meaningful research continues.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','budget_providers','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected Asian primary clauses and local build checked; v128 publication unavailable.'
plan['asia_camp_programme_audit_v128']=audit;plan['current_publication']=publication
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for q in plan['requirements']:
    if q['id']=='unified_database':q['evidence']='v128 local:3775events/1034dossiers/39countries/1582primarydossierURLs;19newAsianprogrammevariants/6datedrows;3769oldevents/1015dossiers/50offerspreserved.FullSQLite/JSON;publicationunavailable.'
    elif q['id'] in ['camps','family_top_picks']:q['evidence']='v128local:1034dossiers/242editorialscenarios;Cobo9age-specificEnglishcurricula,OWISwinter4–16external,KAS2schoolgate,HeadStart5Englishcoregroups/Brighton2paths2026archives.WorldwideprioritycountryandgeneralENESRUscopepreserved;0fullyauditedcountries.'
    elif q['id']=='camp_full_pricing':q['evidence']='v128:53partialbudgets,50oldobjectsunchanged;OWISexternalfirst-timetwochildren140k+10kmaterials+30kregistration+18ktax=198kJPYplusunknownlunch/travel. Cobo3600onlyMatveyVEXafter9/onlyOscarSPIKEafter6+prereq,each8hnotfull-day. ArchivedKAS/Thaiquotesnot2027.'
    elif q['id']=='camp_calendar_2026_2027':q['evidence']='v128:6datedrows/17newfamilyICS. FiveCoboOct20–23ownSchedule withfourtimedlessons each;Hackathon12–14notfamilyICS. EmptySchedulesnotgenericweeks. OWISDec14–18day,archivedKAS/Thaisecondyearnotinvented.2991familyICS/104expo,alloldUID/contentpreserved.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=128]+[dict(version=128,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=19,new_calendar_rows=6,new_budget_scenarios=3,official_primary_retrieval_attempts=30,pdf_download_files=6,not_complete_worldwide=True,publication='prepared_local_not_published')]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=127','?v=128').replace('data-ui-version="127"','data-ui-version="128"');anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_азия_лагеря_v128.md" download>Азия · программы, цены и условия</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text();anchor='<a href="downloads/STEM_europe_camps_audit_v127.json"';link='<a href="downloads/STEM_asia_camps_audit_v128.json" download>Азия: подробная новая проверка ↓</a> · <a href="downloads/STEM_asia_camps_source_receipts_v128.json" download>Первичные источники ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps({k:audit[k] for k in ['version','events','programme_dossiers','official_dossier_urls','new_dossiers','budget_scenarios','budget_providers','family_ical','publication']}))
