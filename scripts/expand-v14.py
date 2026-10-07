"""Primary-source China / AI exhibitions and Costa Rica / Mexico pass.

Append once to v13. Marketing forecasts, old editions, visitor restrictions,
contradictory dates and unpublished teaching languages remain explicit.
"""
import copy, datetime, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/catalog.json'
d = json.loads(PATH.read_text())
DAY = '2026-10-01'
assert len(d['events']) == 1033 and d['completeness_audit']['version'] == 13, 'Run once against v13'
before = {e['id'] for e in d['events']}
baseline = copy.deepcopy(d['completeness_audit']['counts'])
new, updated = [], []
byid = {e['id']: e for e in d['events']}

def source(url, title, evidence):
    row = next((s for s in d['sources'] if s['url'] == url), None)
    if row:
        row.update(checked=DAY, evidence=evidence)
    else:
        d['sources'].append(dict(url=url, title=title, evidence=evidence, checked=DAY))

def add(id, block, title, country, region, city, url, start='', end='', **kw):
    assert id not in before | set(new)
    e = dict(id=id, block=block, title=title, country=country, region=region, city=city,
        start=start, end=end or start, period='' if start else 'Следующее издание / точные дни уточнить',
        date_status='Подтверждено' if start else 'Даты не объявлены', deadline='',
        age='Детский допуск не опубликован в прочитанном источнике',
        mat='Условно — подтвердить допуск ребёнка 9 лет', osc='Условно — подтвердить допуск ребёнка 6 лет',
        format='Посещение выставки' if block == 'События' else 'Дневная каникулярная программа',
        entry='Получить подтверждение допуска и выбрать конкретный билет / программу.',
        gear='Для входа оборудование не требуется' if block == 'События' else 'Оснащение выбранной программы уточнить',
        language='Язык выбранной активности и сопровождения семьи уточнить', languages=[],
        language_certainty='Язык сайта и автоматический перевод не подтверждают язык преподавания.',
        cost='Тариф и наличие мест уточнить', scope='national', level='Региональное событие',
        importance_reason='Редакционная оценка программы и географии; не официальный мировой рейтинг.',
        reward='Посещение / обучение; не соревновательная победа', priority='P2 — после проверки допуска',
        action='Уточнить детский допуск, нужные дни, язык и действующую регистрацию.', source=url, references=[],
        proof='Прочитана первичная страница; ограничения и неизвестные условия сохранены.',
        checked=DAY, status='Идея', note='', themes=['technology'],
        participation='visitor' if block == 'События' else 'day_camp',
        admission_kind='visitor' if block == 'События' else 'program',
        evidence_level='event_page' if block == 'События' else 'program',
        registration_status='Семья не записана; опубликованные даты не доказывают наличие мест.')
    e.update(kw)
    d['events'].append(e)
    new.append(id)
    source(url, title, e['proof'])
    return e

def curate(e, policy, highlights, tier='global'):
    e.update(exhibition_tier=tier, visitor_policy=policy, visitor_policy_note=e['age'],
        adult_entry=e['entry'], highlights=highlights, exhibitors=[],
        exhibitor_note='Список стендов выбранного выпуска не проверен. Прогноз, логотип или прошлогодний участник не гарантирует будущий стенд.',
        exhibitor_directory_url=e['source'], event_group=e['title'].split(' · ')[0])

# TechEx's three city editions have their own dates; colocated tracks are not
# counted as additional city exhibitions. Professional-only student policy is
# explicit in each FAQ, so these cannot be family calendar suggestions.
tech = [
    ('E120', 'AI & Big Data Expo Global / TechEx', '2027', 'Великобритания', 'Европа', 'London · Olympia London',
     'global', '2027-02-03', '2027-02-04', 'Free Expo Pass: выставка и бесплатные сцены; Gold — отдельный платный доступ'),
    ('E121', 'AI & Big Data Expo Europe / TechEx', '2026', 'Нидерланды', 'Европа', 'Amsterdam · RAI Amsterdam',
     'europe', '2026-10-19', '2026-10-20', 'Free Expo Pass: выставка и бесплатные сцены; Gold — отдельный платный доступ'),
    ('E122', 'AI & Big Data Expo North America / TechEx', '2027', 'США', 'Северная Америка', 'San José, California · McEnery Convention Center',
     'northamerica', '2027-06-16', '2027-06-17', 'FAQ: Free Expo Pass; Gold USD 999. Действующий тариф и продажу 2027 перепроверить')]
for id, brand, year, country, region, city, slug, start, end, cost in tech:
    e = add(id, 'События', brand + ' · ' + year, country, region, city,
        f'https://www.ai-expo.net/{slug}/visitor-faqs/', start, end,
        age='FAQ: только специалисты отрасли; студенты / школьники не допускаются в выставочные зоны и конференции',
        mat='Нет — школьники не допускаются по Student Policy', osc='Нет — школьники не допускаются по Student Policy',
        entry='Взрослому специалисту: оформить Free Expo Pass либо Gold. Соответствие профессиональному профилю и доступ к нужной сцене проверить.',
        cost=cost, scope='international', level='Крупная международная серия ИИ / корпоративных технологий',
        priority='P4 — только взрослый визит; детям 6 и 9 лет недоступно',
        themes=['ai', 'robotics', 'technology'],
        importance_reason='Международная серия TechEx с ИИ, данными и совместными индустриальными направлениями; один город / выпуск учитывается одной карточкой.',
        action='Планировать отдельный взрослый визит; детей не включать в бронь на основании бесплатного Expo Pass.',
        proof='Прочитан FAQ конкретного города: точные дни / площадка, типы билета и прямое исключение студентов из expo / theatres.',
        note='Это профессиональная выставка, а не детская лига или турнир. Co-located направления не размножены в отдельные выставки.')
    if slug == 'northamerica':
        e['note'] += ' San José здесь в California, США, не Costa Rica. В FAQ датам 2027 сопутствуют блок California 2026 и ссылка Speakers 2026; их компании / докладчики не перенесены автоматически в 2027.'
    curate(e, 'adults_only', ['AI и Big Data', 'TechEx и совместные технологические направления', 'Выставка и профессиональные конференции'])

e = add('E123', 'События', 'Tech Show London · 2027', 'Великобритания', 'Европа', 'London · Excel London',
    'https://www.techshowlondon.co.uk/attending/visitor-faqs', '2027-03-10', '2027-03-11',
    age='FAQ просит не приводить детей. Отдельный согласованный UEL student programme не даёт допуска детям 6 / 9 лет',
    mat='Нет — организатор просит не приводить детей', osc='Нет — организатор просит не приводить детей',
    entry='Взрослому: visitor registration / interest 2027. Бесплатно для buyers / end-users; service / solution providers могут требовать платный commercial delegate pass.',
    cost='Commercial providers: £199 + VAT до 31.12.2026; £249 + VAT до 09.03.2027; £299 + VAT с 10.03.2027. Free visitor — по профессиональной категории.',
    scope='international', level='Крупный профессиональный технологический комплекс',
    priority='P4 — взрослый визит; детям 6 и 9 лет недоступно', themes=['ai', 'technology'],
    importance_reason='Пять co-located направлений Cloud & AI, DevOps, cybersecurity, Big Data & AI и data centres; единый городской выпуск.',
    action='Проверить категорию взрослого посетителя и тариф; не использовать student exception как детский вход.',
    proof='Прочитан официальный visitor FAQ: 10–11.03.2027, Excel, child policy, commercial pricing и отдельное ограниченное UEL student programme.',
    note='Один комплекс из пяти шоу, а не пять независимых выставок. UEL students: согласование, второй день после 14:00; это не семейная программа. Список 2026 не подтверждает стенды 2027.')
curate(e, 'adults_only', ['Cloud и инфраструктура ИИ', 'Big Data & AI World', 'DevOps, cybersecurity и data centres'])

e = add('E124', 'События', 'HRIE Shanghai · Humanoid Robot & Robotics Industry Chain · 2026', 'Китай', 'Азия',
    'Shanghai · Shanghai New International Expo Centre, Pudong', 'https://www.humanoidrobotfair.cn/', '2026-12-09', '2026-12-11',
    entry='Visitor registration организатора; получить письменный ответ о входе детей 6 / 9 лет со взрослым, документах и стоимости.',
    scope='international', level='Специализированная китайская выставка с международным позиционированием',
    themes=['robotics', 'ai', 'technology'],
    importance_reason='Специализированная экспозиция гуманоидов и робототехнической цепочки в Shanghai. Заявленные размеры — прогноз организатора, не подтверждённая посещаемость.',
    proof='Прочитана официальная страница HRIE: 09–11.12.2026, SNIEC Pudong, организатор Golden Exhibition Group и тематика; детская политика не найдена.',
    note='400+ компаний и площадь 25 000 м² заявлены организатором как будущий масштаб; фактический список стендов не проверен. Отраслевой 金机奖 для компаний не является детскими медалями. Профессиональная аудитория сама по себе не доказывает запрет детям.')
curate(e, 'confirm_children', ['Гуманоидные и сервисные роботы', 'Приводы, сенсоры и компоненты', 'Демонстрации и промышленное применение'], 'regional')

e = add('E125', 'События', 'SIEAR Shanghai · Intelligent Robotics Industry Chain · 2027', 'Китай', 'Азия',
    'Shanghai · Shanghai World Expo Exhibition & Convention Center', 'https://www.siearexpo.com/', '2027-06-02', '2027-06-04',
    entry='Регистрация посетителя SIEAR; отдельно подтвердить возраст детей, сопровождение и язык доступных демо.',
    scope='international', level='Специализированная китайская выставка робототехнической индустрии', themes=['robotics', 'ai', 'technology'],
    importance_reason='Робототехническая цепочка, embodied AI и AI-модели; масштаб 300 компаний / 20 000 м² пока является прогнозом.',
    proof='Прочитаны официальные homepage и about SIEAR: 02–04.06.2027, площадка и организатор Donghao Lansheng; детский допуск не опубликован в прочитанном тексте.',
    references=[dict(url='https://www.siearexpo.com/?about/4', label='Организатор / описание SIEAR')],
    note='SIEAR, SIA, CIROS и HRIE — разные бренды. Обещанный масштаб и организации родительского CSITF не доказывают будущие стенды SIEAR или общий детский вход.')
curate(e, 'confirm_children', ['Intelligent robotics', 'Embodied AI и большие модели', 'Компоненты и промышленные решения'], 'regional')
source('https://www.siearexpo.com/?about/4', 'SIEAR: about / организатор', 'Прочитан about: Donghao Lansheng и партнёры SIEAR отделены от родительского CSITF.')

e = add('E126', 'События', 'SIA Shanghai · Automation & Robotics · 2027 · даты расходятся', 'Китай', 'Азия',
    'Shanghai · National Exhibition and Convention Center, Hongqiao', 'https://www.asia-sia.com/',
    period='2027: homepage 16–18 июня; страница регистрации 1–3 июля. Действующие дни не подтверждены.',
    date_status='Конфликт дат в первичных страницах', scope='international', themes=['robotics', 'ai', 'technology'],
    entry='Сначала получить от SIA единые даты выпуска 2027; затем подтвердить детский вход и visitor registration.',
    action='Не бронировать поездку по одному из двух календарных вариантов до ответа организатора.',
    importance_reason='Автоматизация, smart factory, гуманоиды и компоненты; профильная региональная подборка. Конфликт дат препятствует планированию поездки.',
    proof='Прочитаны две официальные страницы: homepage явно даёт 16–18.06.2027; заголовок visitor registration 2027 — 01–03.07.2027. Не выбрана произвольная дата.',
    references=[dict(url='https://www.asia-sia.com/article/vistform/k/1.html', label='Официальная регистрация: заголовок 1–3 июля 2027')],
    note='Дата оставлена пустой, поэтому SIA не выгружается в ICS. SIA не заменяет CIROS и не является SIEAR. Логотипы и прежние участники не гарантируют будущие стенды.')
curate(e, 'confirm_children', ['Промышленная автоматизация', 'Smart factory и гуманоиды', 'Сенсоры и компоненты'], 'regional')
source('https://www.asia-sia.com/article/vistform/k/1.html', 'SIA visitor registration 2027', 'Прочитан заголовок регистрации 2027: 1–3 июля; противоречит homepage 16–18 июня.')

chitec = 'https://www.chitec.cn/web/'
gov = 'https://www.beijing.gov.cn/fuwu/bmfw/sy/jrts/202604/t20260422_4602068.html'
e = add('E127', 'События', 'CHITEC Beijing · следующая China Beijing High-Tech Expo', 'Китай', 'Азия',
    'Beijing; следующую площадку подтвердить', chitec,
    period='2026 прошло 8–10 мая; следующее физическое издание ещё не объявлено в прочитанном источнике',
    date_status='Следующее издание не объявлено', scope='international', themes=['robotics', 'ai', 'technology'],
    entry='Дождаться нового объявления CHITEC / CCPIT Beijing и собственного visitor registration. Правила 2026 и онлайн-экспозиция не заменяют будущий физический билет.',
    importance_reason='Крупная комплексная high-tech expo Beijing; организатор сообщал о 800 компаниях и шести направлениях в прошедшем 2026 году. Будущий состав неизвестен.',
    proof='Прочитаны официальный сайт CHITEC и правительственная visitor notice для 2026; будущие даты и детский возраст не опубликованы.',
    references=[dict(url=gov, label='Beijing government: информация посетителю 2026')],
    historical_editions=[dict(year=2026, start='2026-05-08', end='2026-05-10', venue='National Convention Center, Beijing', status='Прошло; не будущая дата', source=gov)],
    action='Следить за новым официальным выпуском; запросить правила входа детей 6 / 9 лет, не переносить QR / ID процедуру 2026 без проверки.',
    note='Официальный источник устанавливает организатора CCPIT Beijing. Описание 800 компаний относится к 2026, не гарантирует следующий выпуск. Будущих дат нет в ICS.')
curate(e, 'confirm_children', ['High-tech экспозиция Beijing', 'Технологии и цифровые решения', 'Прошедший 2026 выпуск: шесть тематических зон'], 'regional')
source(gov, 'CHITEC 2026: Beijing government visitor notice', 'Прочитаны 8–10.05.2026 и регистрация посетителей; возраст детей и следующий выпуск не установлены.')

# A local visitor event and its university challenge are distinct roles.
cenfo = 'https://ucenfotec.ac.cr/expocenfo/'
e = add('E128', 'События', 'ExpoCENFO Costa Rica · технологии и VisionRover · 2026', 'Коста-Рика', 'Центральная Америка',
    'Коста-Рика; точную площадку ExpoCENFO подтвердить', cenfo, '2026-10-07',
    age='Местная технологическая / карьерная выставка. Допуск детей 6 / 9 лет как зрителей не опубликован.',
    format='Местная профессиональная / карьерная выставка и демонстрации; agenda с 08:00, expo / rover 09:00–12:00 и 13:00–15:00',
    scope='local', priority='P3 — местный визит после подтверждения допуска детей', themes=['robotics', 'ai', 'technology'],
    entry='Запросить visitor entry и площадку; уточнить, можно ли семье посмотреть VisionRover. Карьерная процедура / CV не является подтверждённой детской регистрацией.',
    related_ids=['C777'],
    proof='Прочитана ExpoCENFO: среда 07.10.2026, начало / agenda и отдельный VisionRover для студентов вузов.',
    note='Не отмечено как крупнейшая мировая выставка. Ребёнок-зритель и участник университетского конкурса имеют разный допуск; не нужно оформлять ребёнку карьерную заявку без указания организатора.')

add('C777', 'Соревнования', 'VisionRover Challenge · CENFOTEC Costa Rica · 2026', 'Коста-Рика', 'Центральная Америка',
    'В рамках ExpoCENFO; площадку уточнить', cenfo, '2026-10-07',
    deadline='2026-09-07', deadline_note='Опубликованный дедлайн регистрации / получения kit уже прошёл; это не будущий срок.',
    age='Активные студенты любых учреждений высшего образования Costa Rica',
    mat='Нет — требуется статус студента вуза', osc='Нет — требуется статус студента вуза',
    format='Робототехническая задача: два робота совместно перемещают три куба; состав команды уточнить',
    participation='team', admission_kind='direct', evidence_level='rules',
    entry='Только активные студенты вузов Costa Rica; регистрация по опубликованному дедлайну 07.09.2026 уже закрыта.',
    gear='Два взаимодействующих робота и computer vision; точную платформу / правила kit уточнить',
    scope='national', level='Университетский конкурс; не детская мировая лига', themes=['robotics', 'ai'],
    priority='P4 — возраст / статус не подходят семье; срок прошёл', reward='Конкурсный результат при допуске и победе; детям 6 / 9 недоступен',
    related_ids=['E128'], registration_status='Опубликованный срок регистрации прошёл; семья не подавала заявку',
    action='Для детей рассматривать только зрительский визит после отдельного разрешения ExpoCENFO.',
    proof='Первичная ExpoCENFO page прямо требует активных студентов высших учебных заведений CR и задаёт дедлайн 07.09.2026.',
    note='Два робота не означают команду из двух человек: число участников, возрастной минимум и оборудование не придуманы. Не включён в семейный ICS.')
profile = dict(id='visionrover-cenfotec', name='VisionRover Challenge · CENFOTEC', group='advanced',
    age_summary='Активные студенты вузов Costa Rica; детям 6 / 9 недоступно', age_tags=['university'],
    summary='Местная университетская программа computer vision и совместной работы роботов; не международная детская лига.',
    categories=[dict(name='VisionRover Challenge 2026', age='Студенты вузов CR', team='Размер команды не подтверждён',
        hardware='Два взаимодействующих робота; точную платформу уточнить', entry='Студенческий статус и регистрация до 07.09.2026', age_rule='Статус учащегося, не только возраст')],
    event_ids=['C777'], legacy_ids=[], route='Университетский статус CR → опубликованный call → kit / заявка → Challenge; текущая семья не соответствует.',
    hardware='Роботы и computer vision; kit / платформа требуют manual', language='Язык правил и поддержки участника уточнить',
    importance='Национальная университетская программа, не путь детей 6 / 9 в мировой финал.', strengths='Computer vision и координация роботов',
    requirements=['Активные студенты вузов Costa Rica.', '2026: опубликованный дедлайн уже прошёл.'],
    nuances=['Посещение ExpoCENFO зрителем не даёт конкурсного допуска.', 'Два робота не определяют размер команды.'],
    cost='Не подтверждён в прочитанном источнике', award='Конкурсный результат по правилам организатора',
    sources=[dict(title='ExpoCENFO / VisionRover: первичная страница', url=cenfo, checked=DAY)],
    evidence='Прочитан местный университетский call 2026; неподходящий возраст / статус обозначен явно.')
d['league_guide']['profiles'].append(profile)
d['league_guide'].update(version=14, checked=DAY,
    methodology='61 профиль семейств, лиг и отдельных конкурсных программ; все 46 прежних маршрутов сохранены. Это частичная мировая карта, а не 61 независимая международная лига. Возраст, статус, национальная квота и сезон проверяются отдельно.')

makers = 'https://ucenfotec.ac.cr/ecommerce/producto/ruta-makers-lab/'
add('L139', 'Лагеря', 'CENFOTEC · Ruta Makers Lab · декабрь 2026', 'Коста-Рика', 'Центральная Америка',
    'Коста-Рика; точную площадку CENFOTEC подтвердить', makers, '2026-12-07', '2026-12-11',
    age='10–12 лет; робототехника, maker design и прототипирование',
    mat='Условно — только если к 7 декабря исполнится 10; сейчас 9 лет', osc='Нет — минимум 10 лет',
    format='Очный дневной workshop: пять дней 10:00–12:00, всего 10 часов; без проживания',
    entry='Официальная запись CENFOTEC; подтвердить возраст на дату начала, конкретный кампус, язык преподавания и приём иностранного ребёнка.',
    themes=['robotics', 'technology'], level='D — каникулярное обучение', scope='local',
    priority='P1 — местный кандидат для Матвея после проверки возраста',
    language='ES кандидат: язык занятий прямо не подтверждён', languages=[],
    sessions=[dict(date=(datetime.date(2026,12,7)+datetime.timedelta(days=i)).isoformat(),
        topic='Ruta Makers Lab: робототехника и прототипирование; тема конкретного дня уточняется',
        start_time='10:00', end_time='12:00', timezone='America/Costa_Rica') for i in range(5)],
    proof='Прочитана текущая первичная course page: 7–11 декабря 2026, 10:00–12:00, 10 часов, 10–12 лет, modalidad presencial.',
    action='Проверить дату рождения Матвея, площадку, наличие мест и EN / ES преподавание перед записью.',
    note='Текущая первичная страница дважды указывает presencial. Поисковый кэш давал virtual en vivo; онлайн-участие не обещано. Испанский текст сайта / флаг перевода не доказывает язык занятий. Одновременная Ruta Explorador IA рассчитана на 14–16 и не подходит детям 6 / 9.')

cerebritos = 'https://www.cerebritosdelfuturo.com/'
add('L140', 'Лагеря', 'Cerebritos del Futuro · mini campamentos STEAM · будущую смену уточнить', 'Мексика', 'Северная Америка',
    'Playa del Carmen', cerebritos,
    age='Возраст holiday mini campamentos не опубликован в прочитанной странице',
    format='Утренние каникулярные mini camps; точные дни и часы новой смены не объявлены',
    period='Semana Santa / декабрь / лето; год и конкретная следующая смена требуют подтверждения',
    themes=['robotics', 'coding', 'technology'], priority='P1 — мексиканский кандидат после подтверждения возраста и языка',
    entry='Выбрать конкретную будущую holiday смену и запросить возраст 6 / 9, ES / EN, часы, стоимость и иностранный приём.',
    proof='Прочитана homepage школы Playa del Carmen: STEAM / robotics / 3D и утренние holiday mini camps; будущих точных дней, возраста и языка нет.',
    note='Расписание обычных вечерних классов 16:00–17:30 / 18:00–19:30 не перенесено на лагеря. Нет фиктивной декабрьской смены 2026 и нет события ICS.')

liota = 'https://liotacamps.com/'
add('L141', 'Лагеря', 'Liota Winter Camp · Yucatán · период 2026–2027, условия уточнить', 'Мексика', 'Северная Америка',
    'Conkal, Yucatán · Calle 18 101; место зимней смены подтвердить', liota,
    period='Опубликован период 17.12.2026–04.01.2027; фактические дни занятий не подтверждены',
    date_status='Период опубликован; расписание противоречиво',
    age='Возраст конкретной Winter Camp не указан; общие отзывы / спортивные U10–U14 не являются правилами STEM-лагеря',
    format='Кандидат дневной зимней программы; операционные дни и часы уточнить',
    themes=['technology'], cost='Провайдер публикует MX$3 200 early bird до 30.11.2026 и MX$4 000 regular; состав периода / тарифа требует уточнения',
    priority='P2 — мексиканский кандидат с противоречивым расписанием',
    language='EN / ES кандидат; язык именно Winter Camp не подтверждён', languages=[],
    entry='Проверить организатора LIOTA, площадку Winter Camp, возраст 6 / 9, язык, фактические дни и условия возврата до оплаты.',
    planned_windows=[dict(label='Winter Camp: опубликованный период', start='2026-12-17', end='2027-01-04',
        status='Провайдер одновременно называет это 4 неделями; интервал содержит 19 календарных дней. Дни занятий уточнить.')],
    proof='Прочитано публичное описание текущего сайта провайдера: Winter Camp, период, STEM / arte / deportes / tecnología и тариф. Противоречие 19 дней против 4 weeks сохранено.',
    note='В описании 17 декабря – 4 января одновременно указано 4 weeks; без уточнения нельзя считать это четырьмя учебными неделями. Общая сетка 09:00–13:00, отзывы о билингвальности и другие программы не доказывают расписание / язык зимней смены. Числовой возраст не найден; спортивный FTI Bowl не включён как STEM-турнир. Период не выгружается в ICS.')

# Rechecked current local competition page; no duplicate MakeX city event.
byid['C020'].update(checked=DAY,
    proof='Повторно прочитана официальная CreativaKids MakeX page: 27–29.11.2026, 11 категорий и разные visitor / competitor registrations. Детальные прежние ограничения сохранены.')
updated.append('C020')
source('https://www.creativakids.com/makex.php', 'MakeX México 2026: повторная проверка',
    '27–29.11.2026 и 11 категорий подтверждены; visitor ticket не является заявкой участника. Прежние дисциплины не продублированы.')
source('https://ucenfotec.ac.cr/ecommerce/producto/ruta-explorador-ia/', 'CENFOTEC Ruta Explorador IA: неподходящий возраст',
    'Прочитан первичный HTML: 7–11.12.2026, presencial, 14–16 лет. Не превращено в детский AI-лагерь 6 / 9 и не перенесено правило Makers 10–12.')

a = d['completeness_audit']
a.update(version=14, checked=DAY, baseline=baseline, new_ids=new,
    new_profiles=['visionrover-cenfotec'], updated_ids=updated, promoted_exhibition_ids=[],
    scope='Повторный аудит мировой полноты; новый проход по профессиональным AI expo, Shanghai / Beijing и местным Costa Rica / México holiday programmes. Все прежние карточки сохранены; по каждой стране полный календарь не закрыт.')
a['known_backlog'] = [x for x in a['known_backlog'] if x['name'] not in [
    'CIROS Shanghai / CHITEC Beijing', 'TechEx / AI & Big Data Expo: London, North America, Europe']]
a['known_backlog'] += [
    dict(kind='Выставки', name='CIROS Shanghai: действующий организатор / следующий выпуск',
        reason='Старая CIROS invitation / агрегаторные даты не подтверждают новый выпуск. SIA, SIEAR и HRIE — другие бренды и не закрывают CIROS.', url=''),
    dict(kind='Выставки', name='Shanghai SIA и Beijing CHITEC: будущие точные даты / детский допуск',
        reason='SIA2027: две официальные страницы дают разные дни. CHITEC: организатор установлен, 2026 прошло, следующий выпуск не объявлен. Оба исключены из календарного экспорта до подтверждения дат.', url=chitec)]
for gap in a['known_backlog']:
    if gap['name'] == 'Costa Rica / México: будущие ES/EN каникулы':
        gap['reason'] = 'CENFOTEC Makers 7–11.12.2026 подтверждён очно, но только для 10–12 лет; EN / ES не подтверждён. Ciberbots / Cerebritos: точные дни неизвестны; у Liota зимний период из 19 дней назван четырьмя неделями. Допуск обоих детей и иностранный приём требуют дальнейшей проверки.'
a['caveats'] = [s for s in a['caveats'] if not s.startswith('Добавлено 16 датированных смен')] + [
    'В v14 добавлены восемь карточек профильных / крупных выставок и одно местное событие; это издания / площадки, а не восемь доказанно крупнейших мировых брендов.',
    'Четыре новые профессиональные выставки исключают детей 6 / 9. Они есть в отдельном выставочном календаре, но отсутствуют в семейном ICS.',
    'Прогноз количества компаний и площади не равен подтверждённому списку будущих стендов. Co-located направления учитываются одной городской выставкой.',
    'CENFOTEC Makers 10–12: текущий возраст Матвея 9 не доказывает допуск на декабрь. Новые кандидаты лагерей не имеют подтверждённого языка EN / ES.',
    'Следующее CHITEC и конфликтующий SIA не получили вымышленных будущих дат. Liota holiday window не стал календарём ежедневных занятий.']
a['source_issues'] += [
    dict(name='SIA Shanghai 2027: официальный конфликт дат', status='Главная: 16–18 июня 2027; заголовок регистрации: 1–3 июля 2027. Конфликт не разрешён: точных дней нет в календаре.', official_alternative='https://www.asia-sia.com/article/vistform/k/1.html'),
    dict(name='TechEx North America: смешанные годы', status='Дни 16–17.06.2027 и площадка подтверждены FAQ. Speakers 2026 / California 2026 не использованы как состав 2027.', official_alternative='https://www.ai-expo.net/northamerica/visitor-faqs/'),
    dict(name='TechEx Student Policy и Tech Show London child gate', status='Каждый TechEx FAQ исключает студентов из expo / theatres; Tech Show просит не приводить детей. Четыре карточки только для взрослых не обещают семейный вход.', official_alternative='https://www.techshowlondon.co.uk/attending/visitor-faqs'),
    dict(name='Liota Winter Camp: период против длительности', status='Период 17.12.2026–04.01.2027 содержит 19 календарных дней, но назван четырьмя неделями. Возраст и язык конкретной смены неизвестны; период не экспортирован в ICS.', official_alternative=liota),
    dict(name='CENFOTEC Makers modality / соседний AI course', status='Текущая страница Makers: очно, 10–12 лет; поисковый кэш с virtual не принят. Explorador IA: 14–16 лет, не подходит детям 6 / 9. Перевод сайта не доказывает язык занятий.', official_alternative=makers)]
d['source_count'] = len(d['sources'])
d['asof'] = DAY
d['expansion_log'].append(dict(version=14, date=DAY, scope='China / AI professional exhibitions and Costa Rica / Mexico programmes',
    added_ids=new, updated_ids=updated, promoted_exhibition_ids=[],
    notes=['Все 1033 прежние карточки сохранены; четыре новых взрослых выставки имеют явное исключение детей.',
        'Будущие CHITEC / SIA даты и Liota ежедневные занятия не придуманы. Новый university programme не объявлен детской лигой.']))
PATH.write_text(json.dumps(d, ensure_ascii=False, indent=2))

planpath = ROOT / 'data/research-plan.json'
plan = json.loads(planpath.read_text())
plan.update(updated=DAY, status='active', completeness_audit='data/audit-v14.json')
for r in plan['requirements']:
    if r['id'] == 'global_competitions':
        r['evidence'] = 'v14: 777 карточек соревнований / 61 профиль семейств и программ. VisionRover только для студентов вузов Costa Rica; дети 6 / 9 исключены. MakeX México повторно проверен без дубликата. Все мировые / национальные отборы ещё не собраны.'
    if r['id'] == 'camps':
        r['evidence'] = 'v14: 141 карточка лагерей / программ. Costa Rica Makers 7–11 декабря 2026 очно, 10–12 лет; México Cerebritos без дат; Liota 19 календарных дней названы четырьмя неделями. EN / ES новых смен не подтверждён; все 138 прежних карточек сохранены.'
    if r['id'] == 'exhibitions':
        r['evidence'] = 'v14: 128 карточек событий / 75 изданий крупных и профильных выставок. Добавлены три города TechEx, Tech Show London, HRIE, SIEAR, SIA, CHITEC. Четыре только для взрослых; SIA с конфликтом дат, будущее CHITEC без даты; местный ExpoCENFO отдельно.'
    if r['id'] == 'eligibility':
        r['evidence'] = 'v14: профессиональный допуск выставок и студенческий статус конкурса исключают детей. Makers 10–12 условно для Матвея 9; язык новых лагерей неизвестен. Конфликты SIA и Liota не разрешены. Квоты, даты рождения, классы и заявки остаются частично проверенными.'
plan['latest_validation'] = dict(version='v14', status='pending', research_status='active')
plan['next_research'].insert(0, 'Уточнить конфликт официальных дат SIA Shanghai, следующий CHITEC и действующий CIROS; допуск детей 6 / 9 на HRIE / SIEAR. Costa Rica Makers: возраст на дату, площадка, язык. México Liota: реальные дни / возраст / EN или ES; Cerebritos: следующая смена. Продолжить поиск лиг и национальных календарей на всех континентах.')
planpath.write_text(json.dumps(plan, ensure_ascii=False, indent=2))
print(json.dumps(dict(added=len(new), total=len(d['events']), added_ids=new), ensure_ascii=False))
