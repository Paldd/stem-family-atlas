"""Keep a reviewable record of selected primary clauses and local delivery limits."""
import collections, hashlib, json
from pypdf import PdfReader
from camp_europe_canada_v130 import ROOT, BASE, CHECKED, NEW, NEW_OFFERS

P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v130'
d=json.loads((ROOT/'data/catalog.json').read_text())
profiles={p['slug']:p for p in d['camp_programmes']['profiles']}
sources=[]
for f in sorted(P.glob('receipt-*.json')):
    for original in json.loads(f.read_text()):
        q=dict(original,checked=CHECKED,retrieval_method='direct_public_http',content_scope='Selected programme, age, language, price and contract clauses or source discovery; not a full site or country audit.')
        if q.get('status')==200:
            filename=q['key']+('.pdf' if (P/(q['key']+'.pdf')).exists() else '.html')
            body=(P/filename).read_bytes()
            assert len(body)==q['bytes'] and hashlib.sha256(body).hexdigest()==q['sha256']
            q.update(raw_filename=filename,body_snapshot_retained=True)
            q['content_status']='selected_pdf_clauses' if filename.endswith('.pdf') else 'selected_html_clauses_or_discovery'
            if q['key']=='suisse-downloads':
                q['content_status']='school_group_forms_discovery_only'
                q['resolution']='Group forms are not individual family terms. The individual summer downloads were followed separately; their linked terms explicitly remain2018.'
        else:
            q.update(body_snapshot_retained=False,content_status='retrieval_error_not_content_evidence')
            q['resolution']='No challenge or TLS-validation bypass. Three guessed paths returned404; relevant programme/parent links were then derived from own navigation. Concordia certificate-chain failures do not establish programme facts; no dossier was added.'
        sources.append(q)
assert len(sources)==37 and sum(q.get('status')==200 for q in sources)==32
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
publication=dict(status='prepared_local_not_published',project_id='appgprj_6abd44bca1348191809b7260dcb46d87',
    reason='Fresh native get_site checks in v130 returned SitesConnectorError: Sites project not found. Versions126–130 have no source-push, save or deployment receipt; no older credential was reused.',
    last_confirmed_published_version=125,last_confirmed_deployment_id='appgdep_6ac4ff3f3c7481918fe3d668d24574b0',last_confirmed_success_at='2026-10-06T14:02:09.803197+00:00',production_browser_qa=False)
blocks=collections.Counter(e['block'] for e in d['events'])
review=d['camp_programmes']['family_review']
audit=dict(version=130,asof=CHECKED,status='progress',scope='15programme dossiers in France/Spain/Canada, selected Swiss2027 fee/FAQ/term-discovery rechecks,50editorial family choices. Existing Asia/Americas/league/school/event work preserved; worldwide priority scope stays active.',
    events=len(d['events']),competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],camp_learning_records=blocks['Лагеря'],
    programme_dossiers=len(profiles),countries_with_dossiers=39,official_dossier_urls=d['camp_programmes']['counts']['source_urls'],editorial_scenarios=len(d['camp_programmes']['shortlist']),budget_scenarios=len(d['camp_planning']['offers']),
    new_dossiers=len(NEW),new_calendar_rows=2,new_budget_scenarios=2,unchanged_dossiers=1034,unchanged_event_objects=3775,unchanged_budget_objects=53,
    dossier_ids=[profiles[s]['id'] for s in NEW],new_calendar_ids=['CP1035-20261019-20261024','CP1038-20270823-20270827'],
    family_review_candidates=50,family_review_countries=16,operators_represented_in_new_dossiers=5,new_dossiers_are_not_unique_operator_count=True,
    source_retrieval_attempts=37,unique_requested_urls=37,direct_successful_retrievals=32,retrieval_errors=5,retained_body_receipts=32,
    pdf_files=2,pdf_text_pages_extracted=sum(len(PdfReader(f).pages) for f in P.glob('*.pdf')),visual_pdf_pages_checked=['AgoraLledo2026brochurepage6:twoTechnologybirth-yeargroups/English','AgoraLledo2026brochurepage11:feeunits/discountexclusions/deposit'],
    family_ical=2993,exhibition_ical=104,league_profiles=141,goal='active',worldwide_complete=False,fully_audited_countries=0,
    external_actions=external,publication=publication,verification={})
assert audit['pdf_text_pages_extracted']==16
for name in ['independent-check','functional-check']:
    if (P/(name+'.json')).exists():
        v=json.loads((P/(name+'.json')).read_text());assert v['status']=='passed' and v['version']==130;audit['verification'][name]=v
def write(stem,value):
    body=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'data'/f'{stem}.json').write_text(body)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(body)
write('europe-canada-camps-audit-v130',audit)
write('europe-canada-camps-source-receipts-v130',dict(version=130,asof=CHECKED,sources=sources,external_actions=external,
    pdf_text_pages_extracted=16,visual_pdf_pages_checked=audit['visual_pdf_pages_checked'],
    limits='37HTTP attempts/37requestedURLs/32retainedHTTP200 bodies/5errors. TwoPDFs16pages text-extracted;selectedclauses read,2pages visually reviewed. School-group terms and guessed404paths are not family-contract content evidence. No website, country, international quality ranking or personal admission is certified complete.'))
write('family-camp-selection-v130',review)
lines=['# Лагеря 2026–2027: Франция, Испания, Канада и швейцарский выбор',
    'Подготовлено локально 6 октября 2026. Версия130 ещё не опубликована: Sites возвращает «Sites project not found». Последняя подтверждённая публикация125.',
    'Добавлены15 досье программ пяти операторов/школ во Франции, Испании и Канаде. Теперь1049 досье в39 странах,50 вариантов семейного сравнения в16 странах и55 частичных смет. Досье отдельных программ не равны числу уникальных лагерей; это не мировой рейтинг.',
    'Матвей2017, Оскар2020; EN/ES/RU. В2027 им9–10 и6–7. Возрастная граница зависит от дня рождения/класса; предварительное соответствие не означает зачисление.',
    '## Что меняет семейный выбор',
    '- Швейцария: в семейную подборку добавлены Camp Suisse (пансион с 7 лет, дневной лагерь с 5 лет), младший Chantemerle для 6–11 лет и Helvetic Zug для 4–12 лет. Дневной и пансионный тарифы сравниваются отдельно; язык активностей проверяется по программе.',
    '- Франция: Enjoy для 6–10 лет — пансион с французским и английским. Полностью английская среда заявлена для подростков. Осенняя смена 19–24 октября 2026 стоит €820 с налогами на ребёнка, базовый пакет для двоих — €1 640. Зимние и весенние данные 2027 противоречивы.',
    '- Париж: Best of LBS, 23–27 августа 2027, €300 за 12,5 часа, группа 3–6 лет. Оскару подходит до семилетия; Матвей старше. Ссылка Grammar ведёт на закрытый архив 2026 для Collège. Новый летний набор по этому курсу ещё не подтверждён.',
    '- Испания: брошюра Agora Lledó прямо подтверждает английский технических потоков. Младшая Technology — для родившихся в 2020–2022, старшая — в 2014–2019; Mini Science — в 2017–2020. Это архив 2026: группы 2027 нужно проверить заново.',
    '- Канада: Ridley Junior Science для 4–7 лет, Dot/Dash и SPIKE для 7–10, старший SPIKE для 10–13. Пансион для 10–16 лет принимает иностранцев. Все прочитанные смены и тарифы относятся к 2026; английский технических занятий ещё не подтверждён.',
    '- Семейный отдых во Франции: Mas de Thau предлагает английскую поддержку и детский клуб до 12 лет. От €5 285 за неделю семьи из четырёх с полупансионом; год этого высокого сезонного тарифа не указан. Родители живут вместе с детьми.',
    '## Два новых расчёта',
    'Enjoy, осень 2026: €820 × 2 = €1 640 с налогами за базовый лагерь. Аванс €410 на ребёнка входит в €820. Дорогу и трансфер нужно оценить отдельно; действующие условия страхования и отмены ещё нужны.',
    'Best of LBS, август 2027: €300 только за Оскара, пять занятий по 2,5 часа, если ему ещё 6 лет. Матвей не включён. Жильё семьи, дорога и остальной день — дополнительные расходы.',
    '## Полные новые досье']
for iso in ['FRA','ESP','CAN']:
    pp=[profiles[s] for s in NEW if profiles[s]['iso']==iso]
    lines+=['### '+pp[0]['country']]
    for p in pp:
        lines += ['**'+p['id']+' · '+p['provider']+'**',
            'Возраст: '+p['age']+' Язык: '+p['language'],
            'Программа: '+p['programme'],
            'Когда: '+p['timing']['label'],
            'Цена: '+p['price']['label'],
            'Включено: '+p['price']['included']+' Доплаты: '+p['price']['extras'],
            'Оплата/отмена: '+p['price']['deposit'],
            'Проживание: '+p['accommodation'],
            'Матвей: '+p['family_fit']['matvey']['detail']+' Оскар: '+p['family_fit']['oscar']['detail'],
            'Источники: '+', '.join('['+s['title']+']('+s['url']+')' for s in p['sources'])+'. Досье: [открыть](../index.html?camp='+p['slug']+'#camps).']
lines+=['## Обнаруженные пробелы и расхождения']
lines += ['- '+g['provider']+': '+g['detail'] for g in d['camp_programmes']['gaps'][-6:]]
lines+=['## Проверка и полнота',
    '37 прямых запросов к публичным первичным страницам:32 сохранённых успешных ответа и5 ошибок. Из2PDF извлечён текст16страниц; прочитаны выбранные положения, визуально проверены2таблицы. Это не37полностью изученных сайтов. Сырые страницы и пустые формы сохраняются отдельно от публичного сайта.',
    'Сохраняются все3775 прежних событий,1034 прежних досье,53 прежние сметы,141лига, школы, результаты, маршруты и источники. Добавлены только2события с однозначными датами.2991 прежняя запись семейногоICS сохраняет исходные байты; новые2записи добавлены без массового обновленияDTSTAMP. ВыставочныйICS прежний.',
    'Мировая цель остаётся активной: все общие и тематические лагеря2026–27 наEN/ES/RU, дневные/пансионные/семейные; соревнования, лиги, выставки, постоянные школы и результаты5–10лет, инженерные и предпринимательские маршруты. Приоритетные CHE/FRA/ESP/Europe,TWN/SGP/KOR/JPN,USA/CAN,CRI/MEX/LATAM сохраняются. Полностью изученных стран0.']
from camp_europe_v127 import readable
(ROOT/'dist/downloads/STEM_лагеря_Европа_Канада_v130.md').write_text('\n\n'.join(readable(lines))+'\n')
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=130:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='v129 authoritative41familychoices/16countries,EnglishAI11+correction,source/independent/UIchecks,commit '+BASE+' and exact local archive. Publication unavailable; meaningful research continues.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='15programme dossiers/2datedrows/2budgets and50familychoices prepared locally; publication unavailable.'
plan['europe_canada_camps_v130']=audit;plan['current_publication']=publication
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks']:
        q['evidence']='v130local:1049dossiers/39countries/1602primaryURLs;15newFranceSpainCanadaprogrammes,Swissrechecks,50familychoices/16countries,55partialbudgets. Dates/fees/language/grade/contracts kept separate;0fullyauditedcountries,worldwidepriorityscopeactive.'
    elif q['id']=='unified_database':q['evidence']='v130local:3777events/1049dossiers/55partialbudgets in fullSQL/JSON;3775oldobjects/1034oldprofiles/53oldoffers preserved. No push/save/deployment receipt.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=130]+[dict(version=130,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=15,new_calendar_rows=2,new_budget_scenarios=2,official_primary_retrieval_attempts=37,not_complete_worldwide=True,publication='prepared_local_not_published')]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=129','?v=130').replace('data-ui-version="129"','data-ui-version="130"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"'
link='<a class="button secondary" href="downloads/STEM_лагеря_Европа_Канада_v130.md" download>Лагеря · Европа и Канада · подробный разбор</a>'
if link not in s:s=s.replace(anchor,link+'\n'+anchor)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text().replace('downloads/STEM_семейный_выбор_лагерей_v129.md','downloads/STEM_лагеря_Европа_Канада_v130.md');f.write_text(s)
print(json.dumps(dict(version=130,status='progress',new_dossiers=15,new_calendar_rows=2,family_review=50,source_attempts=37,publication=publication['status'])))
