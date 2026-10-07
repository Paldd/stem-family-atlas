"""Bounded family decision pass for Switzerland, Spain and France."""
import ast, copy, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORK=Path('/Users/pal/.codex/workspaces/stem-family-atlas-work')
CHECKED='2026-10-02'
p=ROOT/'data/catalog.json';d=json.loads(p.read_text())
assert d['completeness_audit']['version']==48 and len(d['events'])==1755
urls=json.loads((WORK/'urls-europe-family-fit-v49.json').read_text())
urls.update(json.loads((WORK/'urls-europe-family-fit-extra-v49.json').read_text()))
new=[];byid={e['id']:e for e in d['events']}
tree=ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text())
for name in ['ref','event']:
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
for number,title,key,themes in [(447,'Robotics & Engineering','ros_focus',('robotics','coding')),(448,'Informatics & Coding','ros_focus',('coding','games'))]:
    e=event(f'L{number}','Rosenberg Summer Camp 2027 · '+title,'Швейцария','St. Gallen · Höhenweg 60',urls[key],
      'Общий лагерь 6–18; минимальный возраст именно выбранного technical focus и младшую группу подтвердить.',
      'Условно: общий возраст подходит; technical focus, язык и уровень после трёх лет опыта подтвердить.',
      'Условно: общий возраст подходит; это не подтверждает место в младшей робототехнической группе.',
      'Выбрать пребывание минимум 2 недели и конкретный focus; подтвердить обе возрастные группы и технический EN до оплаты.',
      'Робот / собственный компьютер, основы кода; платформа и сложность не объявлены.' if number==447 else 'Свой website / app / game; конкретный язык кода и степень самостоятельности подтвердить.',
      block='Лагеря',participation='day_camp',scope='international',priority='P4 — технический язык и конкретная группа не подтверждены',
      cost="Standard от CHF 8450 / ребёнок / 2 недели; Special от CHF 9750. Двое: от CHF 16900 / 19500 соответственно, без подтверждённого семейного счёта.",
      note='Общее окно лагеря 27 июня–24 июля 2027; выбранная technical-неделя и реальный период пребывания не установлены. Не добавлен месячный технический курс в ICS. 25 уроков × 40 минут в неделю относится к selected course, а не доказанному объёму именно robotics. English / German language courses и EN Primary школы не подтверждают язык технической группы. Международный смешанный пансион, не доказанная подготовка к мировому финалу.',
      themes=themes,evidence='program',date_scope='camp_window')
    e.update(region='Европа',participation='residential',format='Международный лагерь с пансионом · минимум 2 недели',provider='Institut auf dem Rosenberg',period='Общее окно 27.06–24.07.2027; выбранные две / три / четыре недели и technical focus подтвердить')
    e['references']=[ref('Возраст общего лагеря',urls['ros_home']),ref('Пакеты и общий календарь 2027',urls['ros_camp']),ref('Минимум две недели; junior отдельно',urls['ros_faq'])]
for number,key,age,lang,hours in [(449,'fr_tka_junior2','5–6',True,'27 × 1 час'),(450,'fr_tka_primary2','7–9',False,'27 × 1.5 часа')]:
    e=event(f'L{number}','Tech Kids Academy · '+age+' · Niveau 2 · 2026/27','Франция','Paris 15e'+(' / Saint-Germain-en-Laye' if not lang else ''),urls[key],
      age+'; '+('карточка GSM / CP, описание suitability выделяет CP: класс согласовать.' if lang else 'CE2 / CM1; местный школьный класс отдельно от возраста.'),
      'Нет: выше границы 6 лет.' if lang else 'По возрасту подходит; язык FR сейчас не входит в указанные языки семьи.',
      'Условно: возраст 6 подходит; CP и допуск после внешнего опыта согласовать.' if lang else 'Нет: ниже минимального возраста 7.',
      'Регулярное обучение; согласовать уровень, точный слот и место. Это продолжение курса, а не конкурс или каникулы.',
      'Botzees, Smart Train, циклы / условия, первые Scratch / Piskel.' if lang else 'Codey Rocky: сенсоры, линия, препятствия; Scratch с переменными / клонами; моделирование 3D.',
      block='Лагеря',participation='day_camp',priority='P2 — младшая проба после проверки класса и уровня' if lang else 'P4 — продвинутый поток опубликован только на FR',
      language='Прямо указан Bilingue FR / EN: двуязычное обучение, не полностью английский поток.' if lang else 'Прямо указан Français. EN уровня 1 не перенесён на этот уровень 2.',languages=('FR','EN') if lang else ('FR',),
      cost='EUR 640 / год + EUR 45 за заказ нового ученика; текущий счёт и пробу согласовать.' if lang else 'От EUR 775 / год + EUR 45 за заказ нового ученика; выбранный слот и итоговый счёт подтвердить.',
      note='Сезон уже начался в сентябре 2026. '+hours+'; каникулы и праздники исключены, непрерывный год не экспортирован в ICS. Три года участия в соревнованиях не подтверждают автоматически этот уровень: нужен тест самостоятельной сборки / кода. Сертификат участия не международная награда. '+('Оператор выделяет опыт уровня 1; возможность зачесть внешнюю подготовку Оскара не подтверждена.' if lang else 'Более сложные занятия технически интересны Матвею, но EN / ES / RU этого потока не заявлены.'),
      themes=('robotics','coding','games'),evidence='program',date_scope='regular_program')
    e.update(region='Европа',participation='regular',format='Регулярная техническая группа · '+hours,provider='Tech Kids Academy',period='2026/27 · выбранный еженедельный слот согласовать',language_mode='bilingual' if lang else 'primary')
    e['references']=[ref('Младший уровень 1',urls['fr_tka_junior'])] if lang else [ref('Уровень 1 с отдельным EN-потоком',urls['fr_tka_primary'])]
d['events']+=new
school=dict(id='S052',name='Institut auf dem Rosenberg · Primary / Junior',iso='CHE',country='Швейцария',region='Европа',city='St. Gallen',school_type='private',
 curriculum='Primary от Grade 1; точную учебную программу и внешнюю аккредитацию младшего класса подтвердить.',ib_programmes=[],ages='Primary от Grade 1; точные даты рождения / размещение каждого ребёнка неизвестны.',instruction_languages=['EN'],
 language_note='Primary прямо обучается на английском; немецкий — enrichment для уровней от beginners до native. Язык конкретного Junior Robotics / лагерного focus подтвердить отдельно.',
 fit=dict(mat='candidate',osc='candidate',note='Кандидат на школьное поступление; неизвестны grade placement, место в классе и нынешней технической группе.'),boarding='yes',
 boarding_note='Школа с пансионом; минимальный boarding-возраст и дневной приём именно младших не установлены. Общий лагерь 6–18 не подтверждает постоянный пансион для Оскара.',
 programme='В списке Pre-School–Grade 5: Junior Robotics, Junior Game Development, Creative Technologies, Data Detectives, Future Makers Lab и Young Innovators: Founders Thinking. Grades 6–12 имеют отдельные старшие robotics / AI / enterprise courses.',
 labs='Каталог технических курсов подтверждён; оборудование младших, часы самостоятельной работы и конкретные платформы не установлены.',
 ai='Для младших опубликованы CREAII 360 и Data Detectives; это названия курсов, не доказанные AI-часы или соревновательная категория. Старший AI & Agentic Enterprise относится к Grades 6–12.',results=[],evidence='programme',
 admissions='Индивидуальное школьное assessment; подобрать класс и текущие co-curricular места. Оператор прямо предупреждает: курсы зависят от спроса и наличия.',
 cost='Полный школьный счёт 2026/27 не проверен. Лагерь Standard от CHF 8450 за ребёнка / 2 недели — отдельная цена, не tuition школы.',
 questions=['Какой класс и language assessment получит каждый ребёнок?','Есть ли сейчас Junior Robotics для их классов, кто coach, какие часы, платформа и язык?','Какая лига, код команды, junior results организатора за 3–5 сезонов и международная квота?','Возможны ли дневная проба и пансион в этом возрасте; каков полный годовой счёт?'],
 sources=[dict(title='Primary: EN и немецкий enrichment',url=urls['ros_primary'],claim='EN Primary от Grade 1',kind='school',checked=CHECKED),dict(title='Младшие и старшие технические группы',url=urls['ros_cocurricular'],claim='Pre-School–Grade 5 отдельно от Grades 6–12; availability gate',kind='school',checked=CHECKED),dict(title='Лагерный счёт отдельно от школы',url=urls['ros_camp'],claim='Summer 2027 packages, not school tuition',kind='school',checked=CHECKED)],
 checked=CHECKED,priority=2,research_status='partial',verification='Прочитаны первичные школьные страницы после JavaScript-render. Младшие мировые титулы и текущие места не установлены.')
d['schools'].append(school)
f=d['europe_focus'];f.update(version=49,checked=CHECKED,
 conclusion='Мой предварительный выбор для сезонной подготовки — Испания: язык семьи подходит, есть отдельные младшая и основная дорожки. Для короткой общей пробы сейчас — ABI Paris. Швейцария интересна EN-школами и VEX, но решение о базе зависит от реальной младшей команды и бюджета. Это оценка соответствия вашей семье, не мировой рейтинг стран.',
 comparison_note='Сравнение основано на возрасте, вашем EN / ES / RU, опубликованной технической программе и подтверждённых результатах. Свободные места, даты рождения, классы и иностранная квота пока неизвестны. Дорогой пансион сам по себе не доказывает результат команды.')
f['probe_scenarios']=[dict(id='season',label='Соревнования весь сезон',intro='Сначала найти наставника и устойчивую команду на сезон; школу подбирать вокруг этого маршрута.',countries=[
 dict(iso='ESP',verdict='Первый кандидат на пробный период',reason='WRO: Матвею Elementary, Оскару RoboBasic. Их общая Elementary-команда по нынешнему календарному правилу возможна в 2028–2029.',gate='RoboBasic ведёт в национальный финал; мировая категория и иностранная квота отдельно. Сезон 2027 ещё без полного календаря.',event_ids=['C910','C911'],school_ids=['S048','S041']),
 dict(iso='CHE',verdict='Конкретный VEX-наставник; местная команда',reason='Матвею EN/DE TechLabs Competition Lab; Оскару младшая группа. WRO Starter — местная ступень.',gate='Alpine 2027 не принимает нешвейцарские команды. Переезд / школа не означают автоматически регистрацию команды.',event_ids=['L330','L331','C549','C906'],school_ids=['S023','S033']),
 dict(iso='FRA',verdict='Проверить язык защиты и возраст площадки',reason='Матвею FLL / Coupe Junior; Оскару двуязычная техническая группа и младший проект.',gate='Nantes FLL начинается с 11. Tech Kids 7–9 Niveau 2 опубликован только на FR; EN уровня 1 этого не отменяет.',event_ids=['C916','C918','C1103','L449','L450'],school_ids=['S025','S047'])]),
 dict(id='holiday',label='Короткая проба для обоих',intro='Задача поездки — проверить самостоятельность, подход наставника и сложность после трёх лет опыта.',countries=[
 dict(iso='ESP',verdict='Проба у наставника; новые лагеря ещё уточнить',reason='Проверять ROBBO / Tecnoeduka по уровню. Это регулярные курсы, а не объявленные общие каникулярные смены.',gate='EISB Science July 2027 на EN, но опубликованные рождения 2012–2019 исключают Оскара 2020.',event_ids=['L378','L379','L396','L397','L421'],school_ids=['S049']),
 dict(iso='CHE',verdict='Отдельные младшие группы',reason='Ecolint Introduction подходит Оскару по возрасту; Матвею VEX. Rosenberg — ещё один пансионный кандидат на лето 2027.',gate='У Rosenberg не установлены technical EN и группа для каждого. Общая двухнедельная Standard-цена для двоих от CHF 16900.',event_ids=['L296','L292','L293','L447','L448'],school_ids=['S052']),
 dict(iso='FRA',verdict='Самая конкретная общая ближайшая проба',reason='ABI Haunted 26–30 октября 2026: Explorer 5–8 / Inventor 9–12, двуязычные механизмы, схемы и код.',gate='EUR 980 за двоих / неделю по опубликованному тарифу; жильё отдельно. Текущие места и более сложный проект Матвею подтвердить.',event_ids=['L230','L449'],school_ids=['S025'])]),
 dict(id='school',label='Английская постоянная школа',intro='Рекомендация условная: EN Primary, реальная младшая инженерная группа и место в команде проверяются отдельно.',countries=[
 dict(iso='ESP',verdict='ASV / Barcelona + внешний тренер',reason='ASV — EN/ES база; EISB Cambridge / английский Primary. Выбирать город по наставнику, языку класса и полному семейному счёту.',gate='Школьная программа не подтверждает нынешнее место в международной команде. В Barcelona язык региональной школы не предполагать испанским.',event_ids=['L179','C911'],school_ids=['S048','S049','S041']),
 dict(iso='CHE',verdict='IS Basel / ISZL / Rosenberg',reason='Rosenberg подтверждает EN Primary и Junior Robotics в Pre-School–Grade 5; IS Basel связан с VEX-средой.',gate='Rosenberg courses зависят от спроса и availability; годовая стоимость, младшие мировые результаты и boarding-возраст не установлены.',event_ids=['L330','L447'],school_ids=['S023','S033','S052']),
 dict(iso='FRA',verdict='ICS Paris / ABI; французский постепенно',reason='ICS имеет EN Primary; ABI — двуязычная база и реальная каникулярная проба. Предусмотреть школьную и техническую языковую адаптацию.',gate='Старшие robotics / AI и мировые результаты независимого клуба не являются результатом младшего класса выбранной школы.',event_ids=['L230','L356','L357','L450'],school_ids=['S047','S025'])])]
f['development_phases']=[
 dict(period='2026–2029',title='Самостоятельная инженерия и одна основная лига',detail='Матвей: собственная сборка, датчики, отладка, технический дневник и защита проекта. Оскар: механизмы, простые циклы / условия, самостоятельная младшая роль. Не ставить младшего в старшую категорию ради общей команды. Проверять каждый новый сезон: классы и birth-year cutoff меняются.'),
 dict(period='2030–2033',title='Углубление кода и собственный продукт',detail='Python по готовности, электроника, CAD, сбор данных и проверка качества AI. Одна главная лига плюс собственный проект с пользователями: проблема, прототип, тесты, улучшение. Старшие FTC / VEX / RoboCup — только по новым действующим правилам и готовности.'),
 dict(period='2034–2038',title='Сильная команда и исследовательский / предпринимательский трек',detail='Выбор специализации: автономные роботы, AI / computer vision, инженерный продукт или игры. История версий, измеримые тесты, авторский вклад, пользовательские интервью и бюджет проекта. Матвею в эти годы исполняется 17–21, Оскару 14–18: младшие возрастные лиги будут заканчиваться в разные годы; условия проверять ежегодно.')]
f['evidence_cards'].append(dict(title='Rosenberg: школьный EN и лагерный robotics — разные условия',detail='В Primary EN подтверждён. Junior Robotics перечислен для Pre-School–Grade 5; старший AI / Applied Robotics — Grades 6–12. Лагерь 2027 имеет технические focuses и общий возраст 6–18.',limit='Язык лагерной техники, младший boarding-возраст, действующий coach и мировые титулы младших не установлены. Camp price не школьная tuition.',event_ids=['L447','L448'],school_ids=['S052'],source_urls=[urls['ros_primary'],urls['ros_cocurricular'],urls['ros_camp']]))
f['evidence_cards'].append(dict(title='Франция: английский уровень 1 не распространяется на уровень 2',detail='Tech Kids 5–6 Niveau 2 — bilingual FR/EN, 27 часов за сезон. 7–9 Niveau 2 — только FR, 40.5 часа. Это существенно для детей с трёхлетним соревновательным опытом.',limit='Сначала тест уровня и класса. У младших suitability выделяет CP, общий заголовок GSM / CP. Полностью EN-преподавание и свободные места не обещаны.',event_ids=['L356','L357','L449','L450'],school_ids=[],source_urls=[urls['fr_tka_junior2'],urls['fr_tka_primary2']]))
f['family_picks'][4]['event_ids']+=['L447','L448'];f['family_picks'][4]['school_ids']+=['S052']
f['family_picks'][4]['gate']+=' Rosenberg: технический EN / младшие focus-группы не подтверждены; Standard для двоих от CHF 16900 за две недели.'
f['family_picks'][8]['event_ids']+=['L449','L450'];f['family_picks'][8]['gate']+=' Более сложный Tech Kids 7–9 Niveau 2 только FR; младший 5–6 Niveau 2 двуязычный.'
ch=next(c for c in f['countries']if c['iso']=='CHE');ch['school_ids'].append('S052');ch['event_ids']+=['L447','L448'];ch['school']+=' Rosenberg: EN Primary и Junior Robotics подтверждены отдельно; место и часы не установлены.'
fr=next(c for c in f['countries']if c['iso']=='FRA');fr['event_ids']+=['L449','L450'];fr['risk']+=' Niveau 2 Tech Kids 7–9 — только FR; bilingual 5–6 отдельно.'
for key in ['ros_primary','ros_cocurricular','ros_camp','fr_tka_junior2','fr_tka_primary2']:
    f['sources'].append(dict(title=key,url=urls[key],checked=CHECKED))
issues=[dict(name='Rosenberg primary JavaScript content',status='HTTP 200 source shell lacks body; primary pages rendered in anonymous Chrome, EN Primary and Junior Robotics read there.',official_alternative=urls['ros_primary']),dict(name='Rosenberg camp language / weekly track',status='General 6–18 and 2027 window do not prove each junior technical focus, its language or actual chosen weeks; no guessed dates exported.',official_alternative=urls['ros_faq']),dict(name='Tech Kids advanced language',status='7–9 Niveau 1 offers EN / FR, but Niveau 2 explicitly only FR. 5–6 Niveau 2 remains bilingual and has grade / prior-level conditions.',official_alternative=urls['fr_tka_primary2'])]
a=d['completeness_audit'];a['validation_previous']=copy.deepcopy(a['validation']);a.update(version=49,checked=CHECKED,scope='CHE/ESP/FRA family decision scenarios, junior course levels and Rosenberg school / camp gates',conclusion='4 новые учебные карточки и школьное досье; три интерактивных сценария выбора базы и маршрут 2026–2038. Даты и чужие языковые условия не перенесены предположением; мировой охват остаётся частичным.',new_ids=[e['id']for e in new],new_profiles=[],new_school_ids=['S052'],updated_ids=[],updated_profile_ids=[],validation=dict(version=49,status='pending',publication='pending'))
a['source_issues']+=issues
d['camp_focus'].update(version=49,checked=CHECKED,added_ids=[e['id']for e in new],updated_ids=[],conclusion='Rosenberg 2027 technical focuses с неустановленными языком / неделями; Tech Kids Niveau 2: младший bilingual, старший только FR.',validation=dict(version=49,status='pending'))
d['school_focus'].update(version=49,checked=CHECKED,conclusion='52 школьных досье; Rosenberg EN Primary / младшие технические курсы подтверждены, текущая команда и мировой титул младших не установлены.')
d['asof']=CHECKED;d['expansion_log'].append(dict(version=49,checked=CHECKED,scope='User-requested Switzerland / Spain / France family decision follow-up',added=4,new_schools=1,status='partial; worldwide objective preserved'))
known={s['url'] for s in d['sources']}
for key in ['ros_home','ros_camp','ros_focus','ros_faq','ros_primary','ros_cocurricular','fr_tka_junior2','fr_tka_primary2']:
    if urls[key] not in known:
        d['sources'].append(dict(url=urls[key],title='Семейный выбор Европа · '+key,checked=CHECKED,evidence='Прочитан первичный programme; школьный JS-контент дополнительно отрендерен. Язык и возраст конкретного трека раздельно.'))
        known.add(urls[key])
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
receipts=[]
read={'ros_home','ros_camp','ros_focus','ros_faq','wro_es_basic','wro_es_faq','robotech_home','robotech_history','robotech_share','first_2026','fr_abi','fr_tka_junior','fr_tka_primary','fr_tka_junior2','fr_tka_primary2'}
for name in ['receipt.json','receipt-extra.json']:
    for row in json.loads((WORK/'sources-europe-family-fit-v49'/name).read_text()):
        row.pop('path',None);row['primary_body_read']=row['name']in read
        if row['name']in ['ros_primary','ros_cocurricular']:row['limitation']='Relevant content is JavaScript-rendered; see rendered receipt, not HTTP status alone.'
        receipts.append(row)
rendered=json.loads((WORK/'sources-europe-family-fit-v49/receipt-rendered.json').read_text());assert all(r['read'] for r in rendered)
(ROOT/'data/europe-family-fit-source-receipts-v49.json').write_text(json.dumps(dict(version=49,checked=CHECKED,sources=receipts,rendered_sources=rendered,issues=issues),ensure_ascii=False,indent=2)+'\n')
rp=ROOT/'data/research-plan.json';r=json.loads(rp.read_text());r.update(updated=CHECKED,completeness_audit='data/audit-v49.json',latest_validation_previous=r['latest_validation'],latest_validation=dict(version=49,status='pending',publication='pending'))
r['research_passes'].append(dict(version=49,checked=CHECKED,scope='Requested deeper Switzerland / Spain / France family-fit comparison',status='implementation; validation pending',added=4,new_schools=1,new_history_results=0))
r['previous_goal_turn_classification']=dict(status='progress',evidence='v48 deployed; all80 anonymous live static hashes and UI verified;43cards,4profiles,2schools,4results delivered.',remaining='Full world scope and country audits remain active.')
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=49,added=len(new),schools=len(d['schools']),events=len(d['events'])),ensure_ascii=False))
