"""Local European supplement, primary receipts and preserved worldwide research plan."""
import collections,hashlib,json,subprocess
from camp_europe_v127 import ROOT,BASE,CHECKED,NEW,NEW_IDS
P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v127'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
cp=d['camp_programmes'];old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
before={q['slug']:q for q in b['camp_programmes']['profiles']};after={q['slug']:q for q in cp['profiles']}
assert len(after)==1015 and after.keys()-before.keys()==set(NEW) and all(after[k]==v for k,v in before.items())
assert len(now)==3769 and all(now[k]==v for k,v in old.items())
offers={q['id']:q for q in d['camp_planning']['offers']};assert len(offers)==50
assert all(offers[q['id']]==q for q in b['camp_planning']['offers']) and offers.keys()-{q['id'] for q in b['camp_planning']['offers']}==set(NEW_IDS)
sources=[]
for f in sorted(P.glob('receipt-*.json')):
    for x in json.loads(f.read_text()):
        q=dict(x,checked=CHECKED,retrieval_method=x.get('retrieval_method','direct_public_http'),content_scope='Selected camp dates, age, language, curriculum, boarding/equipment, price and contractual clauses. Not a full country or whole-site audit.')
        if q.get('status')==200:
            filename=q['key']+('.pdf' if (P/(q['key']+'.pdf')).exists() else '.html')
            raw=(P/filename).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
            q.update(raw_filename=filename,body_snapshot_retained=True)
            q.setdefault('content_status','selected_pdf_clauses' if filename.endswith('.pdf') else 'selected_html_clauses_or_discovery')
        else:q.update(body_snapshot_retained=False,content_status='retrieval_error_not_content_evidence',resolution='Python TLS issuer error; system curl with normal TLS validation returned the Space Camp landing, still no current full syllabus read.')
        sources.append(q)
assert len(sources)==30 and sum(q.get('status')==200 for q in sources)==28
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
blocks=collections.Counter(q['block'] for q in d['events'])
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT')
expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert (family,expo)==(2974,104)
publication=dict(status='prepared_local_not_published',project_id='appgprj_6abd44bca1348191809b7260dcb46d87',
    reason='Two fresh native get_site calls during v127 returned SitesConnectorError: Sites project not found. No fresh write credential, push, save or deployment for v126/v127.',
    last_confirmed_published_version=125,last_confirmed_deployment_id='appgdep_6ac4ff3f3c7481918fe3d668d24574b0',last_confirmed_success_at='2026-10-06T14:02:09.803197+00:00',production_browser_qa=False)
checks=[
    'Hopla Holiday PDF explicitly publishes autumnOct19–23, winterFeb15–19, springApr12–16 and four summer2027weeks. Age5+full09–16:30,3–4morningseparate,FR/ENbilingual,noEnglishminimum. Holidaymax12/min6 notWednesdaymax20. Lunch/snacksfamilyprovided. EUR290five-days,care2.50half-hour;family580andoptional100care are arithmetic,not fulltravelquote. PDFrefund≥15full/14–7half/<7none;failedminimum6operatorrefund. No form/payment/medical info entered.',
    'Hopla OutdoorJuly12–16 isfouractualdays July12/13/15/16:own14Julyholiday excluded fromtimedICS;five-day290not prorated. Nature/science/arboretumvisitplanned,not guaranteeddate. Winter/spring precise PDFdatesnew buttheir specificthemes not invented. GamesAugustnon-digitalgames not videogamecoding.',
    'LBS four own2027pages:Fairytales/BoostFeb8–12,London/BoostApr5–9;five explicitlyshown schoolsschedules each representedbykeyedvenuevariants=20datedrows. EUR300five2.5hourlessons=12.5h,nofullday/lunch/boarding. AM09:30–12/PM14–16:30 youngexceptMeudonAM;BoostallPM. Young3–6Oscaronlybefore7birthday,Matveynoteligible;BoostCE1–CM2classesunknown. Englishlessonsexplicit,notrobotics. Saturdayworkshops/footerotherweeksnotextrapolated.',
    'Village Kids8–12/Teens13–17 generalENcamp-life,optionalSpanishSchoolnotmainSpanishinstruction. Mediafilmwriting/editingnotcodingrobotics. Own1:5/85%native/medicalquality/Cambridgeclaims source-attributed,notindependentworldrank.2026datesJun28–Jul11/Jul12–25andfees2290/4460incl10%VATarchive,notnew2027.120siblingnotassignedtoOscarbelow8. ActualfourstarZenBalagares/collegeAsturiasnotallMadrid,roomgender/age/staffinterspersed,limitedlaundry4day,nofamilyday. Exactrefunddeadlineprivateagreementnotobtainedbymakingaccount.',
    'HIFwinter ownFeb10–20,2027,10–16,English,11days10nightsCHF4586. Appliedsnow/forces/mapsandoutdoors notsummerAIroboticsmodule. Matveyrequires10byFeb10,Oscarbelowminimum.300airportpick-upnotroundtrip;single500/1000,pocket50–100,insuranceandwintergearrentalunknownfullinvoice;specialistequipmentnotunconditionalallwintergear. Twinensuite/staffnight/UMsupport andlimitedeveningphones ownclaims,notinspectedguarantees. Currentwinterrefundnotpublicpage,summertermsnotcopied.',
    'FrenchColo own2027seasonJul4–Aug27 and weeklySunday17–Friday17rule:seasonwindow only,no inventedall-seasonresidence or31newdaily/weekdates. Samepage10–16versus11–16/collègeconflict:Matveyunknown,Oscarlater.10hENstandard765,currentundatedprice;premium910+10hENORriding. RidingENrequiresGalop3,beginnerFRnotautomaticEN.25Montaubanoneleg/50return,board/foodincludedroomtypeunknown. CGVgeneral≥33deposit/30daysbalance/35change,refund10/20/50/75/90/100retainedasgeneralpendingspecificcampcontract.2024insurancecostnot2027.',
    'CienciaSorolla own2026camp22Jun–17Jul archive only;onekit+PCperstudentclassuse,nottakehomepurchase. AIonlyESO,notallages;robotics/3D/gamedesignmaterialsrealcurriculum. Web6–18 versusPDFschool/birth2010–2019 gate unresolvedforOscar2020. WebBularas2vsPDF4/currentofficeotheraddress notmergedasvenue.234week/439two/614three/789four/day62 archived;170deposit andrefund2023in2026PDF notacceptednewcontract. ESdocumentsnotexplicitteacherlanguage;zero2027datedevent/quote.',
    'Tinker institutional offers FR/EN/ES canteach,notdirectfamilyadmission;250/studentmaterialoffer notfullbookablefamilycampprice. Springwrongfévrierandsummer2027heading2026bullets remain gap, no newdatedcamp. Cosmo/HIFsummer recheckedalreadyexistingnotduplicated. SpacePythonissuererrorversussystemcurl200Nextlanding notproof2027programme;oldcachedages/pricesnotinferred.',
    'All3741old eventobjects/999oldprogrammeobjects/48oldbudgetobjects preserved.16newdossiers over6operators,28datedrows/31familyICS additions,2partialbudgetoffers. Allcompetitions/exhibitions/schools/history/routes/prioritycountries andfullSQLite/JSONexports preserved. Worldwide goalactive,0fullyauditedcountries.'
]
audit=dict(version=127,asof=CHECKED,status='progress',scope='Selected European junior bilingual/English seasonal courses and residential programmes, with detailed Spanish technical archives. Not a worldwide census or independent global ranking.',
    events=len(now),competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],camp_learning_records=blocks['Лагеря'],programme_dossiers=len(after),countries_with_dossiers=39,
    official_dossier_urls=len({s['url'] for p in cp['profiles'] for s in p['sources']}),editorial_scenarios=len(cp['shortlist']),coverage_gaps=len(cp['gaps']),league_profiles=len(d['league_guide']['profiles']),
    budget_scenarios=50,budget_providers=26,budget_programme_dossiers=39,new_budget_scenarios=2,new_dossiers=16,new_dossier_slugs=NEW,
    new_programme_operators=['HoplaBoum','LittleBritishSchools','theVillage','HIF','AnglaisinFrance','CienciayRobotica'],updated_dossier_slugs=[],new_event_ids=sorted(now.keys()-old.keys()),
    unchanged_dossier_objects=999,unchanged_event_objects=3741,unchanged_prior_budget_objects=48,source_retrieval_attempts=30,direct_successful_bodies=28,retrieval_errors=2,
    pdf_download_files=3,pdf_text_pages_extracted=24,new_visual_pdf_checks=1,family_ical=family,exhibition_ical=expo,goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,publication=publication,checks=checks,verification={})
for name in ['independent-check.json','functional-check.json']:
    f=P/name
    if f.exists():
        q=json.loads(f.read_text());assert q['status']=='passed' and q['version']==127;audit['verification'][name.removesuffix('.json')]=q
def write(stem,v):
    t=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(t);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(t)
write('europe-camps-audit-v127',audit)
write('europe-camps-source-receipts-v127',dict(version=127,asof=CHECKED,scope=audit['scope'],sources=sources,pdf_download_files=3,pdf_text_pages_extracted=24,
    visual_pdf_pages_checked=[dict(filename='hopla-form.pdf',page=3)],external_actions=external,
    primary_reader_limits='30 direct attempts /28 HTTP200 includes discovery/rechecks/client-rendered landing, not28 fullcampwebsites. ThreePDF24pages textextracted;one selectedfee table visuallyread. RawHTML/PDF/text/imagesprivate. No forms,accounts,consent,messages,booking,payment.'))
lines=['# Европа: подробные программы лагерей, версия 127',
    'Подготовлено локально 6 октября 2026. Версии 126 и127 ещё не опубликованы: Sites возвращает «Sites project not found». Последняя подтверждённая публикация —125.',
    'Добавлены16 досье программ/сезонов у шести операторов,28 датированных карточек и31 запись календаря. Это не16 независимых лагерных организаций и не полный мировой рейтинг.',
    'Локальная база:1015 досье в39 странах;50 частичных семейных смет. Все3741 прежние карточки и999 досье сохранены. Весь реестр не перепроверен сегодня.',
    '## Что подходит семье',
    '- Оба вместе: HoplaBoum, дневной FR/EN,с5лет,свойlunchbox. Точные осень,зима,весна,лето;EUR580за двоих/5дней. Upperage иприём приезжейсемьи подтвердить.',
    '- Париж: Fairy/London3–6 толькоОскару до7лет;MatveyBoostCE1–CM2 толькоесли фактическийкласс подходит.300EUR/12,5часа,неполныйдень.',
    '- Швейцарская зима: HIF10–20февраля2027,EN,CHF4586,минимум10лет. Матвейтолькопосле10летназаезд;Оскарпока ниже10.',
    '- Испания: VillageKids8–12 ианглийскийMediaтрек — кандидатдляМатвея,новые2027даты/ценаещёнужны. Oscarпока младше8. Sorollaподробныйrobotics/game/3Dsyllabus2026,AIтолькоESO.',
    '- FrenchColo2027:ENпансион+опциональнаяезда,но возраст10/11расходится;допускМатвеянеподтверждён.',
    '## Подробные новые досье']
for slug in NEW:
    p=after[slug]
    lines += ['### '+p['provider'],p['country']+' · '+p['place'],'**Возраст:** '+p['age'],'**Программа:** '+p['programme'],
        '**Когда:** '+p['timing']['label'],'**Язык:** '+p['language'],'**Цена:** '+p['price']['label'],'**Включено:** '+p['price']['included'],
        '**Доплаты:** '+p['price']['extras'],'**Оплата и отмена:** '+p['price']['deposit'],'**Проживание:** '+p['accommodation'],
        '**Матвей:** '+p['family_fit']['matvey']['detail'],'**Оскар:** '+p['family_fit']['oscar']['detail'],
        'Источники: '+', '.join('['+s['title']+']('+s['url']+')' for s in p['sources'])]
lines += ['## Что ещё проверять','Свободные места, верхний возраст Hopla, договоры LBS/HIF/Village2027,новый Sorolla2027,текущий SpaceCampTürkiye. Технический язык не выводится из английского сайта. Рейтинг остаётся редакционным и объясняется в карточке.',
    'Мировая цель активна:соревнования,выставки,лагеря,школы,история результатов и семейные маршруты. Ни одна страна не признана полностью изученной.']
from camp_europe_v127 import readable
(ROOT/'dist/downloads/STEM_европа_лагеря_v127.md').write_text('\n\n'.join(readable(lines))+'\n')
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=127:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='v126localresearch/independent+UIchecks/commit '+BASE+';publicationunavailablebutmeaningfulresearchcontinues.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','budget_providers','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected European primary clauses and local build checked; v127 publication unavailable.'
plan['europe_camp_programme_audit_v127']=audit;plan['current_publication']=publication
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for q in plan['requirements']:
    if q['id']=='unified_database':q['evidence']='v127local:3769events/1015dossiers/39countries/1559primarydossierURLs;16newEuropeanprogrammevariants/28datedrows.3741oldevents/999dossiers/48oldofferspreserved. CompleteSQLite/JSON;publicationunavailable.'
    elif q['id'] in ['camps','family_top_picks']:q['evidence']='v127local:1015dossiers/239editorialscenarios;Hopla7exactseasons,LBS4courses5campuseseach,HIFwinter10–16, VillageENKids/Teens,FrenchColoageconflict,Sorolla2026curriculum. WorldwideprioritycountryandgeneralENESRUscopepreserved;0fullyauditedcountries.'
    elif q['id']=='camp_full_pricing':q['evidence']='v127:50partialbudgets,48oldobjectsunchanged;Hopla580twochildren/fivedays+optional100care+foodunknown;LBS300onlyMatvey12.5h/classgate. Outdoorfourdaysnoinventedproration,Village2026archive,FrenchColoundated765/910,HIFwinter4586+extras, Sorolla2023refundconflict.'
    elif q['id']=='camp_calendar_2026_2027':q['evidence']='v127:28newdatedrows/31familyICS additions.HoplaJuly14excluded:fourtimedlessonentriesinsteadoneweekevent.LBSvenuekeysavoidduplicateIDs;FrenchColoseasonwindownotlongresidentialevent;Spanisholdsummernotnew2027.2974familyICS/104expo,alloldUID/contentpreserved.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=127]+[dict(version=127,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=16,new_calendar_rows=28,new_budget_scenarios=2,official_primary_retrieval_attempts=30,pdf_download_files=3,not_complete_worldwide=True,publication='prepared_local_not_published')]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=126','?v=127').replace('data-ui-version="126"','data-ui-version="127"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_европа_лагеря_v127.md" download>Европа · подробные программы и условия</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text();anchor='<a href="downloads/STEM_americas_camps_audit_v126.json"'
link='<a href="downloads/STEM_europe_camps_audit_v127.json" download>Европа: программы и новые каникулы ↓</a> · <a href="downloads/STEM_europe_camps_source_receipts_v127.json" download>Первичные источники ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps({k:audit[k] for k in ['version','events','programme_dossiers','new_dossiers','budget_scenarios','family_ical','publication']}))
