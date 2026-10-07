"""Apply the 30 September primary-source exhibition and holiday-program audit.

Network dates, actual host pages and unannounced programs retain different
evidence levels. This is an idempotent research migration, not a web scraper.
"""
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'data/catalog.json'
DAY = '2026-09-30'
NETWORK = 'https://makerfaire.com/upcoming-faires/'
d = json.loads(CATALOG.read_text())
if any(x.get('version') == 'v8' for x in d['expansion_log']):
    raise SystemExit('v8 already applied; use catalog.json for subsequent corrections')
assert len(d['events']) == 898, 'Expected the published v7 baseline'
before_ids = {x['id'] for x in d['events']}
countries = {c['iso']: c for c in d['countries']}
by_id = {x['id']: x for x in d['events']}
new_ids, updated_ids, sources = [], [], {}
next_num = {'E': 52, 'L': 90, 'C': 759}


def source(url, title, evidence='event_page', findings=''):
    sources[url] = dict(url=url, title=title, evidence=evidence, checked=DAY,
                        findings=findings)
    return url


def ref(url, label):
    return dict(url=url, label=label)


def add(prefix, title, iso, city, url, start='', end='', **extra):
    i = prefix + str(next_num[prefix]).zfill(3)
    next_num[prefix] += 1
    c = countries[iso]
    block = {'E': 'События', 'L': 'Лагеря', 'C': 'Соревнования'}[prefix]
    e = dict(id=i, block=block, title=title, country=c['country'], region=c['region'],
             city=city, start=start, end=end or start, period='' if start else 'Следующая дата не объявлена',
             date_status='Подтверждено' if start else 'Не объявлено', deadline='',
             age='Возраст конкретной активности не опубликован',
             mat='Условно: подтвердить допуск', osc='Условно: подтвердить допуск',
             format='Посещение с родителем' if prefix == 'E' else 'Дневная программа; проживание семьи отдельно',
             entry='Проверить текущие билеты / запись и ограничения выбранной активности',
             gear='Для посещения оборудование не нужно' if prefix == 'E' else 'Уточнить у организатора',
             language='Язык активности не подтверждён', languages=[],
             language_certainty='Язык сайта не подтверждает язык занятий или судейства; EN/ES поток требуется уточнить.',
             cost='Текущий тариф не опубликован на прочитанной странице',
             level='E — образовательное событие' if prefix == 'E' else 'D — обучение',
             scope='regional' if prefix == 'E' else 'local',
             importance_reason='Редакционная оценка по опубликованному формату и географии; не официальный рейтинг.',
             reward='Знакомство с технологиями; посещение не является соревновательной победой' if prefix == 'E' else 'Учебный проект; сертификат обучения не является международной победой',
             priority='P3 — при удобной поездке' if prefix == 'E' else 'P2 — после подтверждения смены и допуска',
             action='До бронирования получить возрастной допуск, язык, наличие мест и условия отмены',
             source=url, proof='Прочитана первичная страница; неизвестные условия указаны отдельно.',
             checked=DAY, status='Идея', note='', themes=['technology'],
             participation='visitor' if prefix == 'E' else 'day_camp',
             admission_kind='visitor' if prefix == 'E' else 'program',
             evidence_level='event_page' if prefix == 'E' else 'program')
    e.update(extra)
    d['events'].append(e)
    by_id[i] = e
    new_ids.append(i)
    return e


def update(i, **fields):
    by_id[i].update(fields, checked=DAY)
    updated_ids.append(i)


source(NETWORK, 'Maker Faire — upcoming network directory', 'catalog',
       '30 listed editions; 24 new cards, Rome and Taipei rechecked; this is one network, not all world exhibitions')

# The dates below are individually listed by the international network. Host
# pages are independently opened unless a failure is explicitly recorded.
maker_rows = [
    ('Maker Faire Vientiane 2026', 'LAO', 'Вьентьян', '2026-10-02', '2026-10-04', '',
     'Возраст / место по локальному регламенту пока не проверены', '', 'catalog',
     'Локальная ссылка из каталога https://makerbox.la/event/maker-faire-vientiane-2025/ вернула ошибку; 2025 в адресе не подтверждает правила 2026.'),
    ('Maker Faire Malta 2026', 'MLT', 'Калькара, Esplora Interactive Science Centre', '2026-10-02', '2026-10-04', 'https://malta.makerfaire.com/',
     'Семейный фестиваль; возраст мастер-класса уточнить', '', 'event_page', 'Билетная страница динамическая: тариф и наличие мест не прочитаны.'),
    ('Happy Valley Maker Faire 2026', 'USA', 'Bellefonte, Pennsylvania — Axemann Brewery / Titan Hollow', '2026-10-03', '2026-10-04', 'https://happyvalley.makerfaire.com/',
     'Семейное дневное посещение', 'Общий дневной вход бесплатный', 'event_page', 'Сб 11:00–17:00, Вс 11:00–15:00. After Dark в субботу 18:00–20:00 только для взрослых и не входит в семейный план. Robot combat — отдельные правила участников.'),
    ('Rocklin Maker Faire 2026', 'USA', 'Rocklin, California — Sierra College', '2026-10-03', '2026-10-03', 'https://rocklin.makerfaire.com/',
     'Семейное посещение; возраст мастер-класса отдельно', '', 'event_page', '10:00–15:00 по странице организатора.'),
    ('Maker Faire Leroy Merlin France 2026', 'FRA', 'Магазин / площадку Leroy Merlin уточнить', '2026-10-03', '2026-10-03', 'https://france.makerfaire.com/',
     'Детский допуск текущей площадки не проверен', '', 'catalog', 'Дата из международного каталога. Прочитанная локальная страница не подтверждает конкретный город и программу 2026.'),
    ('Maker Faire České Budějovice 2026', 'CZE', 'České Budějovice — Výstaviště, Národní pavilon Z', '2026-10-03', '2026-10-03', 'https://makerfaire.cz/ceske-budejovice/',
     'Детский билет 6–15; отдельные занятия по возрасту', '6–15 лет: 80 Kč онлайн / 100 Kč на месте; семейный 399 / 450 Kč', 'event_page', '10:00–17:00. Оскар в 6 лет попадает в платную группу 6–15, а не в бесплатную до 6. Пайка от 8 с сопровождением — 250 Kč; воздушный змей 6–12 — 200 Kč. Боевая робототехника имеет отдельную запись; её возраст не подтверждён.'),
    ('Electric City Maker Faire 2026', 'USA', 'Schenectady, New York — Union College', '2026-10-04', '2026-10-04', 'https://electriccity.makerfaire.com/',
     'Публичный фестиваль; K–12 welcome', 'Бесплатный вход', 'event_page', '11:00–16:00. Запись на посещение и ограничения отдельных активностей проверить на странице.'),
    ('Maker Faire Guangzhou 2026', 'CHN', 'Guangzhou — Huangpu', '2026-10-17', '2026-10-18', 'https://guangzhou.makerfaire.com/',
     'Детские правила конкретной площадки не опубликованы в прочитанном тексте', '', 'event_page', 'Даты подтверждены локальным анонсом. EN/ES активности и возрастные ограничения требуют проверки.'),
    ('Maker Faire Tübingen 2026', 'DEU', 'Tübingen — Shedhalle, Schlachthausstraße 9', '2026-10-17', '2026-10-17', 'https://ki-maker.space/angebote/events/makerfaire-tuebingen-2025-1',
     'Дети прямо приглашены организатором; мастер-классы отдельно', 'Бесплатный вход', 'event_page', '10:00–18:00. Несмотря на 2025 в URL, текст прямо объявляет 2026. Mini Maker стенд для детских проектов требует отдельного согласования; это не обещание награды.'),
    ('Baton Rouge Maker Faire 2026', 'USA', 'Baton Rouge, Louisiana — Main Library at Goodwood', '2026-10-17', '2026-10-17', 'https://batonrouge.makerfaire.com/',
     'Семейный фестиваль; возраст отдельных занятий уточнить', '', 'event_page', 'Участие со своим maker-проектом согласуется отдельно от обычного посещения.'),
    ('Louisville Maker Faire 2026', 'USA', 'Louisville, Kentucky — UofL Engineering Student Success and Research Building', '2026-10-17', '2026-10-17', 'https://louisville.makerfaire.com/',
     'Все возраста; семейное посещение', 'Бесплатный вход', 'event_page', 'Заявка на показ собственного проекта — отдельный маршрут, не соревновательная медаль.'),
    ('Maker Faire Brno 2026', 'CZE', 'Brno — Výstaviště Brno', '2026-10-17', '2026-10-18', 'https://makerfaire.cz/brno/',
     'Детский билет 6–15', 'Детский день 140–190 Kč; два дня 220–280 Kč; семейные тарифы отдельно', 'event_page', 'Сб 10:00–18:00, Вс 10:00–16:00. Цена зависит от предварительной покупки / входа на месте. Maker Challenge 17 октября — отдельный конкурс с неизвестным пока детским допуском.'),
    ('Maker Faire Luxembourg 2026', 'LUX', 'Rosport — Sports complex am Bongert', '2026-10-24', '2026-10-25', 'https://luxembourg.makerfaire.com/',
     'Семейный фестиваль; возраст мастер-класса уточнить', '', 'event_page', 'Оба дня 10:00–18:00. Это Rosport, не город Luxembourg. На странице сохранился список makers 2024; его нельзя выдавать за программу 2026.'),
    ('Downtown Columbia Maker Faire 2026', 'USA', 'Columbia, Maryland — The Chrysalis, Merriweather Park', '2026-10-25', '2026-10-25', 'https://downtowncolumbia.makerfaire.com/',
     'Семейное посещение; возраст мастер-класса отдельно', '', 'event_page', 'Публичный festival visit и заявка со стендом — разные способы участия.'),
    ('ITERA TEC — Maker Faire México 2026, конфликт дат', 'MEX', 'Кампус и площадку уточнить', '', '', 'https://www.innovactiongym.biz/itera',
     'Детский / иностранный допуск не подтверждён', '', 'catalog', 'Каталог сети: 29–30 октября 2026. Локальная страница: 19–20 ноября без года, с архивами 2022–2024. До ответа организатора точная дата не считается подтверждённой и не экспортируется в ICS.'),
    ('Maker Days Salzburg 2026', 'AUT', 'Salzburg — HTBLuVA', '2026-11-07', '2026-11-07', 'https://www.makerdays.at/',
     'Открыто всем возрастам; конкретное занятие отдельно', 'Бесплатный вход', 'event_page', '10:00–18:00. Дедлайн экспонентов 12 сентября уже прошёл; это не срок покупки visitor-билета.'),
    ('Maker Faire Mittleres Rheintal 2026', 'DEU', 'Bendorf — Sayner Hütte, 56170', '2026-11-07', '2026-11-08', 'https://makerspace-myk.de/makerfaire/',
     'Дети и подростки младше 18 проходят бесплатно', 'Взрослый 10 EUR плюс сбор; до 18 лет бесплатно', 'event_page', 'Показ проектов, робототехника, программирование и 3D-технологии; язык конкретной активности уточнить.'),
    ('Maker Faire Olomouc 2026', 'CZE', 'Olomouc — Výstaviště Flora, Pavilion A', '2026-11-15', '2026-11-15', 'https://makerfaire.cz/olomouc/',
     'Детский билет 6–15; мастер-классы отдельно', '6–15: 80 Kč онлайн / 100 Kč на месте; семейный 399 / 450 Kč', 'event_page', '10:00–17:00. Бесплатно только младше 6; Оскар в 6 лет уже в детском платном тарифе.'),
    ('Rochester Maker Faire 2026', 'USA', 'Rochester, New York — RIT Gordon Field House', '2026-11-21', '2026-11-21', 'https://rochester.makerfaire.com/',
     'Семейное публичное посещение', '', 'event_page', 'Публичная выставка 21 ноября. Student STEAM Fest 20 ноября — отдельная школьная программа, допуск семьи туда не установлен.'),
    ('Ogaki Mini Maker Faire 2026', 'JPN', 'Ogaki, Gifu — Softopia Japan Centre, Kagano 4-1-7', '2026-12-05', '2026-12-06', 'https://www.iamas.ac.jp/news/ogaki-mini-maker-faire-2026/',
     'Детский возраст / язык отдельных занятий пока не проверены', '', 'event_page', 'Даты и площадка объявлены IAMAS. Не подтверждены EN/ES программа и конкурсный допуск.'),
    ('Sarawak Maker Faire 2026', 'MYS', 'Sarawak; точную площадку подтвердить', '2026-12-08', '2026-12-12', 'https://www.makeramai.com/',
     'Детский регламент Faire ещё не найден', '', 'catalog', 'Даты только из каталога сети. Сайт Makeramai описывает makerspace в Plaza Merdeka, Kuching, но не подтверждает площадку и тариф Faire 2026. Бесплатный walk-around makerspace не перенесён на билет фестиваля.'),
    ('Kochi Maker Faire 2027', 'IND', 'Kochi; точную площадку подтвердить', '2027-01-23', '2027-01-24', 'https://tinkerhub.org/',
     'Детский регламент Faire ещё не найден', '', 'catalog', 'Дата по каталогу сети; прочитанный сайт TinkerHub описывает организацию, а не детальную программу Faire 2027.'),
    ('South Dallas Maker Faire 2027', 'USA', 'South Dallas по каталогу; площадку уточнить', '2027-03-06', '2027-03-06', '',
     'Детский регламент ещё не проверен', '', 'catalog', 'Каталог ведёт на https://fortworth.makerfaire.com/; локальная ссылка недоступна. South Dallas и Fort Worth нельзя считать подтверждённым одним адресом.'),
    ('Buffalo Maker Faire — Summer 2027', 'USA', 'Buffalo, New York — Nichols School', '', '', 'https://buffalo.makerfaire.com/',
     'Семейное посещение; тариф до 5 не распространяется на 6 и 9', 'Опубликован тариф USD 5; его применимость к изданию 2027 уточнить', 'event_page', 'Локальный анонс говорит Summer 2027, каталог сети — июнь. Точный день не опубликован. Не создаётся вымышленная дата календаря; прежний билетный checkout ещё не проверен.'),
]
maker_map = {}
for title, iso, city, start, end, host, age, cost, evidence, note in maker_rows:
    url = host or NETWORK
    if host:
        source(host, title + ' — прочитанная локальная страница', evidence)
    family = any(x in age for x in ['Семей', 'Детский билет', 'Открыто всем', 'Все возраста', 'K–12', 'Дети прямо', 'младше 18'])
    e = add('E', title, iso, city, url, start, end, age=age,
            cost=cost or 'Текущий тариф на прочитанной странице не установлен',
            mat='Да для посещения; активности отдельно' if family else 'Условно: подтвердить детский вход',
            osc='Да для посещения; активности отдельно' if family else 'Условно: подтвердить детский вход',
            themes=['technology', 'robotics'], evidence_level=evidence, note=note,
            references=[ref(NETWORK, 'Прочитанный каталог сети: дата издания')],
            proof='Дата по каталогу сети; локальная проверка и её пределы указаны в примечании.' if evidence == 'catalog' else 'Прочитаны каталог сети и локальная страница организатора.')
    maker_map[title] = e['id']
    if title.startswith('ITERA'):
        e.update(period='Каталог: 29–30.10.2026; локальный анонс: 19–20 ноября без года',
                 date_status='Конфликт источников', published_start='2026-10-29', published_end='2026-10-30',
                 priority='P2 — México, только после уточнения дат',
                 action='Получить у Innovaction Gym год, реальные дни, кампус и возрастной visitor gate; затем планировать поездку')
    if title.startswith('Buffalo'):
        e['period'] = 'Лето 2027; каталог указывает июнь; точный день не объявлен'

rome = source('https://makerfairerome.eu/biglietti/', 'Maker Faire Rome 2026 — tickets', findings='23–25 October; online-only tickets; under18/student tariff8EUR; family tariff not a whole-family total')
update('E005', source=rome, city='Рим — Gazometro, Via del Commercio 9–11',
       age='Посещение с родителем; до 18 есть детский тариф; активности отдельно',
       cost='Стандартный €13; до 18 / студенты €8; семейный тариф €8 — состав заказа проверить',
       entry='Билеты только онлайн; выбрать число взрослых и детей, потом слоты Junior Maker',
       language='IT материалы; EN/ES мастер-классы не подтверждены', languages=[],
       language_certainty='Английская версия сайта не подтверждает язык каждой Junior Maker активности.',
       proof='Прочитана текущая страница билетов 2026.', evidence_level='event_page',
       scope='international', importance_reason='Крупная международная maker-выставка; посещение не даёт конкурсного титула.',
       note='23–25 октября, 10:00–19:00. Тариф €8 не означает билет на всю семью за €8. Бесплатно младше 4, не для детей 6 и 9. Билет включает Junior Maker активности; возраст, слоты и язык уточнить.')
taipei = source('https://taipei.makerfaire.com/', 'Maker Faire Taipei — current page', 'catalog', 'Current page mostly images; detailed visitor rules not read')
update('E027', start='2026-10-24', end='2026-10-25', period='', date_status='Подтверждено',
       source=NETWORK, evidence_level='catalog', proof='Дни 24–25 октября 2026 опубликованы каталогом сети; локальный visitor регламент не подтверждён.',
       references=[ref(taipei, 'Локальная страница: программа преимущественно в изображениях')],
       note='Подтверждён день издания по каталогу, но не детские активности, площадка, EN/ES или свободные места. Иллюстрированные application guides не разобраны в этом проходе.')

# Additional family / industry exhibitions, with edition-specific child gates.
url = source('https://maker-faire.de/hannover/', 'Maker Faire Hannover 2027', findings='21–22 August2027; HCC; family event; new tickets not yet published')
add('E', 'Maker Faire Hannover 2027', 'DEU', 'Hannover — Hannover Congress Centrum, Theodor-Heuss-Platz 1–3', url,
    '2027-08-21', '2027-08-22', age='Семьи и дети прямо включены в программу',
    mat='Да для посещения; активности отдельно', osc='Да для посещения; активности отдельно',
    scope='international', themes=['technology', 'robotics', 'coding'],
    importance_reason='Крупный maker-фестиваль международной сети; его конкурсные активности проверяются отдельно.',
    note='Сб 10:00–18:00, Вс 10:00–17:00. Тарифы издания 2027 не опубликованы; цены 2026 не перенесены. EN/ES мастер-классы не подтверждены.')
penang = source('https://pisf.pscpen.com/', 'Penang Science Cluster — PISF2026', findings='SPICE venue and programs; some competition subpages still2025')
penang_date = source('https://www.mypenang.gov.my/view_events.php?id=SEFjMEtKdm9qTlVzK004WkJZM3NhUT09', 'Penang Global Tourism — PISF2026 date', findings='21–22Nov2026;09–17;SPICEArenaConcourse')
penang_public = source('https://pisf.pscpen.com/public/', 'PISF — public admission', findings='No public registration required; walk-in09–17; workshop and competition rules separate')
add('E', 'Penang International Science Fair 2026', 'MYS', 'Penang — SPICE Arena & Concourse', penang,
    '2026-11-21', '2026-11-22', themes=['ai', 'technology', 'robotics'], scope='international',
    age='Публичное посещение; возраст мастер-класса / конкурса отдельно',
    entry='Публичная зона: walk-in, предварительная регистрация не требуется; конкурсы и мастер-классы отдельно',
    cost='Нужна ли плата за выбранный мастер-класс, уточнить; отсутствие регистрации не доказывает бесплатность',
    note='09:00–17:00. Тема Innovation in the Age of AI. Страницы некоторых соревнований ещё относятся к 2025: их возраст и дедлайны не перенесены на 2026.',
    references=[ref(penang_date, 'Государственное туристическое бюро: дата и место 2026'), ref(penang_public, 'Правила public walk-in')])
hk = source('https://innocarnival.hk/en/About//', 'InnoCarnival Hong Kong2026 — About', findings='Oct24–Nov1;SciencePark;all activities free; public exhibits no admission registration')
hk_faq = source('https://innocarnival.hk/en/About/FAQ/Details/225', 'InnoCarnival — family account / workshops', findings='TypeA families/smallgroups/individuals; quota booking for workshops')
source('https://innocarnival.hk/en/About/FAQ/Details/220', 'InnoCarnival — general public access', findings='Public exhibit access distinct from workshop bookings')
add('E', 'InnoCarnival Hong Kong 2026', 'HKG', 'Гонконг — Hong Kong Science Park', hk,
    '2026-10-24', '2026-11-01', themes=['technology', 'robotics', 'ai'], scope='regional',
    age='Публичные экспозиции; возраст отдельных семейных мастер-классов проверить',
    mat='Да для публичного посещения; возраст занятия отдельно', osc='Да для публичного посещения; возраст занятия отдельно',
    cost='Все активности заявлены бесплатными; мастер-классы ограничены квотами',
    entry='На публичные экспозиции билет и регистрация не нужны. На workshop: аккаунт Type A для Families / Small Groups / Individuals и запись на слот',
    note='Выходные 10:00–18:00, будни 10:00–17:00. EN/ES преподавание и минимальный возраст конкретного workshop не установлены. На старый аккаунт до августа 2026 нельзя рассчитывать.',
    references=[ref(hk_faq, 'Запись семьи и ограничения мест')])
fil = source('https://www.fil.pt/wp-content/uploads/2026/01/Calendario_Elevadores_2026_vs-5-Jan-2026.pdf', 'FIL official2026 calendar — Lisboa Games Week', 'catalog', 'November19–22; public event; calendar subject to changes')
add('E', 'Lisboa Games Week 2026', 'PRT', 'Lisboa — FIL, Parque das Nações', fil,
    '2026-11-19', '2026-11-22', themes=['games', 'technology'], scope='international', evidence_level='catalog',
    age='Публичная выставка по календарю FIL; детские правила текущего выпуска не прочитаны',
    proof='Прочитан первичный календарь выставочного центра FIL; локальная программа и билеты требуют уточнения.',
    note='FIL предупреждает о возможных изменениях дат. Сайт с билетами не удалось прочитать; детский visitor gate, тарифы и EN/ES программа не подтверждены.')

gitex = source('https://www.gitex.com/', 'GITEX Global2026 — current dates', findings='SummitDec7;ExpoDec8–11; current2026 child visitor gate not established')
source('https://www.gitex.com/terms-and-conditions', 'GITEX Global — terms page', findings='Readable text insufficient for current child visitor policy')
update('E018', title='GITEX Global 2026 — выставка', start='2026-12-08', end='2026-12-11',
       source=gitex, city='Dubai — Dubai Exhibition Centre, Expo City Dubai', evidence_level='event_page',
       proof='Текущая первичная страница разделяет Summit 7 декабря и Expo 8–11 декабря.',
       note='7 декабря проходит Summit; выставка Expo — 8–11 декабря. Детский visitor gate 2026 не найден в читаемых условиях. Возраст в privacy policy не означает разрешение входа.',
       language='EN материалы; детская программа не подтверждена', languages=[],
       language_certainty='Англоязычная профессиональная программа не доказывает допустимость посещения детьми.')
asia = source('https://gitexasia.com/', 'GITEX AI Asia2027 — current edition', findings='29–30April2027,MarinaBaySands; child policy2027 not found')
asia_old = source('https://event.gitexasia.com/registration-confirmed', 'GITEX Asia2026 — historical admission notice', findings='Historical2026 notice trade/business professionals18+; not transferred as confirmed2027 policy')
add('E', 'GITEX AI Asia 2027', 'SGP', 'Singapore — Marina Bay Sands', asia,
    '2027-04-29', '2027-04-30', themes=['ai', 'technology', 'robotics'], scope='international',
    age='Политика 2027 не установлена; опубликованный notice 2026 был для 18+ trade / business',
    entry='Получить письменный visitor gate 2027 до покупки детского билета',
    note='Правило 18+ прочитано в confirmation странице 2026. Оно является предупреждением для планирования, но не выдаётся за подтверждённый регламент 2027.',
    references=[ref(asia_old, 'Историческая политика 2026, не текущий допуск 2027')])
eu = source('https://www.gitexeurope.com/faqs', 'GITEX AI Europe — current FAQ', findings='2026 trade/business18+; nextedition dates not announced; old21+ cache not current')
add('E', 'GITEX AI Europe — следующее издание', 'DEU', 'Berlin — площадку следующего издания уточнить', eu,
    period='Последнее издание 30.06–01.07.2026; следующие даты не объявлены',
    age='По опубликованному FAQ только trade / business, 18+', mat='Нет: опубликован допуск 18+', osc='Нет: опубликован допуск 18+',
    priority='P4 — дети младше опубликованного минимума', scope='international', themes=['ai', 'technology', 'robotics'],
    entry='Профессиональная выставка 18+; для семейного плана искать публичные события; правила нового издания перепроверить',
    note='Текущий FAQ указывает 18+, а не 21+ из старых результатов поиска. Новые дни 2027 не придуманы по ежегодной периодичности.')
africa = source('https://gitexafrica.com/faqs', 'GITEX Africa — admission FAQ', findings='Trade/business18+;16–17 only school/faculty;2027 dates not yet found')
source('https://gitexafrica.com/', 'GITEX Africa — nextedition announcement', findings='2027 context without exact future days')
add('E', 'GITEX Africa — следующее издание', 'MAR', 'Marrakech — площадку нового издания подтвердить', africa,
    period='Последнее издание 07–09.04.2026; будущие точные даты не объявлены',
    age='Trade / business, 18+; исключение 16–17 только с учебным заведением',
    mat='Нет: младше опубликованного минимума', osc='Нет: младше опубликованного минимума',
    priority='P4 — текущий детский возраст исключён', scope='international', themes=['ai', 'technology', 'robotics'],
    note='FAQ смешивает разделы прошлых лет. Общий возрастной gate указан, но новые даты 2027 и новая редакция условий требуют отдельной проверки.')

# A real local contest, without inventing eligibility or international status.
challenge = source('https://makerfaire.cz/maker-challenge/', 'Maker Challenge Brno2026 — competition rules', 'rules',
                   'Oct17 jury13–15;upcycle3Dparts;40x30x15cm;Prusa prize; age/team/foreign rules not stated')
brno = maker_map['Maker Faire Brno 2026']
contest = add('C', 'Maker Challenge Brno 2026 — upcycling / 3D project', 'CZE', 'Brno — Maker Faire, Výstaviště', challenge,
              '2026-10-17', '2026-10-17', evidence_level='rules', themes=['technology'],
              age='Минимальный возраст, иностранный приём и состав команды не указаны в прочитанных правилах',
              format='Показ рабочего проекта перед жюри; индивидуальный / командный формат уточнить',
              participation='unconfirmed_program', admission_kind='open_application', scope='local',
              gear='Переделать старый / выброшенный предмет в игрушку, игру или механизм; функциональные 3D-печатные части; габариты до 40×30×15 см',
              entry='Онлайн заявка с концепцией, затем принести действующий прототип; отдельно подтвердить возраст 6/9, команду, иностранный допуск и билет',
              cost='Стоимость конкурсной заявки не указана; visitor-билеты Faire по отдельному тарифу',
              level='C — местный конкурс проектов', reward='Приз Prusa 3D printer по оценке жюри; участие и победа зависят от принятой заявки и результата',
              priority='P2 — конкурс после подтверждения детского допуска',
              importance_reason='Судейский конкурс внутри регионального maker-фестиваля; не международный чемпионат.',
              note='17 октября 13:00–14:00 обход жюри, 14:00–14:30 обсуждение, 14:30–15:00 награждение. Дедлайн заявки не опубликован в прочитанном тексте. Критерии: креативность, механика, 3D-печать, игровой / интерактивный результат.',
              parent_event_id=brno, related_ids=[brno],
              sessions=[dict(date='2026-10-17', topic='Показ проектов и награждение', start_time='13:00', end_time='15:00', timezone='Europe/Prague')])
by_id[brno]['related_ids'] = [contest['id']]

# Nullspace: concrete dated groups are separate from the undated umbrella.
ns = 'https://sg.nullspace.co/centre-for-robotics-learning/'
robot = source(ns + 'lego-robotics-camp/', 'Nullspace LEGO Robotics Engineer — Dec2026 groups', 'program',
               'Five Dec21–24/Dec28–31 groups09:30–12;primary current page9–13;10hSGD520; no teaching-language confirmation')
ai = source(ns + 'generative-ai/', 'Nullspace Generative AI — Oct2026 workshops', 'program',
            'Nine single-day sessionsOct2/12/13;09:30–12;age9–14;SGD137.50')
policy = source(ns + 'centre-policy/', 'Nullspace — centre policy', 'program',
                'Equipment provided; cancellation72h;credit/refund conditions; no teaching-language confirmation')
ns_ids = []
for campus, name, first in [
        ('Rochester Mall', 'Ingenious', '2026-12-21'),
        ('Rochester Mall', 'Innovate', '2026-12-28'),
        ('Kallang Wave Mall', 'Innovate', '2026-12-28'),
        ('SAFRA Tampines', 'Ingenious', '2026-12-21'),
        ('SAFRA Tampines', 'Innovate', '2026-12-28')]:
    days = [(datetime.date.fromisoformat(first) + datetime.timedelta(days=n)).isoformat() for n in range(4)]
    e = add('L', f'Nullspace LEGO Robotics Engineer {name} — {campus}, December 2026', 'SGP', 'Singapore — ' + campus,
            robot, days[0], days[-1], age='9–13 по текущей странице; рекомендовано от 9',
            mat='Да по возрасту; язык и иностранный приём подтвердить', osc='Нет: рекомендовано от 9',
            format='4 дня × 2,5 часа, 09:30–12:00; без проживания',
            cost='SGD 520 за пакет 10 часов; условия кредитов / отмены отдельно',
            gear='LEGO MINDSTORMS EV3 и ноутбук предоставляются; робот не остаётся участнику',
            entry='Выбрать указанную группу в Parent Portal, проверить свободные места, иностранный приём и язык',
            language='EN сайт; язык преподавания не подтверждён', languages=[],
            themes=['robotics', 'coding'], related_ids=['L016'], registration_url='https://book.nullspace.co/',
            note='Новый ученик может начать без опыта. Страница указывает 9–13; другие обзорные программы 9–12 не подменяют возраст этой группы. Объявленный поток не означает свободное место. Отмена менее 72 часов может списать кредиты; refund policy проверить.',
            references=[ref(policy, 'Прочитанные условия занятий и отмены')],
            sessions=[dict(date=x, topic='LEGO Robotics Engineer ' + name, start_time='09:30', end_time='12:00', timezone='Asia/Singapore') for x in days])
    ns_ids.append(e['id'])
for campus, topic_list in [
        ('Rochester Mall', [('2026-10-02', 'AI Game Creator'), ('2026-10-12', 'AI Game Creator'), ('2026-10-13', 'AI Comic Story Creator')]),
        ('Kallang Wave Mall', [('2026-10-02', 'AI Comic Story Creator'), ('2026-10-12', 'AI Comic Story Creator'), ('2026-10-13', 'AI Game Creator')]),
        ('SAFRA Tampines', [('2026-10-02', 'AI Game Creator'), ('2026-10-12', 'AI Game Creator'), ('2026-10-13', 'AI Comic Story Creator')])]:
    for date, topic in topic_list:
        e = add('L', f'Nullspace {topic} — {campus}, {date}', 'SGP', 'Singapore — ' + campus, ai, date, date,
                age='9–14', mat='Да по возрасту; язык и иностранный приём подтвердить', osc='Нет: минимум 9',
                participation='holiday_workshop', format='Однодневный мастер-класс, 09:30–12:00, 2,5 часа',
                cost='SGD 137.50 за мастер-класс; возможна оплата course credits',
                themes=['ai', 'coding', 'games'] if 'Game' in topic else ['ai', 'technology'],
                entry='Отдельно записаться на этот день / филиал в Parent Portal; предыдущие курсы не обязательны',
                language='EN сайт; язык преподавания не подтверждён', languages=[], related_ids=['L016'],
                gear='AI-инструменты для игры / комикса; оснащение выбранного класса уточнить',
                note='Это один самостоятельный workshop, не многодневная смена. Иностранный приём, язык и свободное место пока не подтверждены.',
                sessions=[dict(date=date, topic=topic, start_time='09:30', end_time='12:00', timezone='Asia/Singapore')])
        ns_ids.append(e['id'])
little = source(ns + 'stem-little-explorer-class-5-6/', 'Nullspace Little Explorer — weekly5–6 FAQ', 'program',
                'Weekly1h;10sessionsSGD520;holiday-week camps specifically not offered;trial$5promotion/$55 conflict')
e = add('L', 'Nullspace STEM Little Explorer — регулярные занятия 5–6', 'SGP', 'Singapore — филиал и weekly слот выбрать', little,
        participation='regular', period='Еженедельные занятия продолжаются на каникулах; holiday camp для 5–6 не предлагается',
        age='5–6', mat='Нет: группа 5–6', osc='Да по возрасту; язык и иностранный приём подтвердить',
        format='Регулярное обучение; 1 час в неделю; 10 занятий в term',
        cost='SGD 520 за 10 занятий. Trial: на странице встречаются $5 promotional и $55 — актуальную цену подтвердить',
        gear='LEGO Technic / инженерные задания / Bee-Bot по программе',
        themes=['robotics', 'technology'], language='EN сайт; язык занятий не подтверждён', languages=[],
        entry='Запросить weekly / trial группу для 6-летнего ребёнка; подтвердить возможность короткой записи для иностранной семьи',
        note='FAQ прямо уточняет: weekly программа остаётся weekly во время каникул; week-long holiday camps для 5–6 нет. Не выдаётся за лагерь. Учебные milestone certificates не являются конкурсными победами.',
        related_ids=['L016'])
ns_ids.append(e['id'])
for slug, title, age, cost, period, gear, note in [
        ('minecraft-holiday-camp/', 'Minecraft Coding Holiday Camp', '9–12', 'SGD 825 за 15 часов',
         'Опубликованы только прошедшие June 2026; следующий поток не объявлен',
         'Minecraft Education / coding', 'Прошедшие июньские даты не перенесены на будущие каникулы. Формат 5 дней × 3 часа.'),
        ('buildup-series-3d-print-design-holiday-camp/', '3D Print Design Holiday Camp', '9–12', 'SGD 550 за заявленные 10 часов',
         'Опубликованы только прошедшие September 2026; следующий поток не объявлен',
         'Tinkercad, Bambu Studio / 3D design', 'Описание: 5 дней × 2 часа. Один прошлый диапазон 8–11 сентября содержит 4 дня; длительность новой группы требуется подтвердить.')]:
    url = source(ns + slug, 'Nullspace — ' + title, 'program', period)
    e = add('L', 'Nullspace — ' + title + ', следующий поток', 'SGP', 'Singapore — следующий филиал / слот уточнить', url,
            age=age, mat='Да по возрасту; будущий поток и язык подтвердить', osc='Нет: минимум 9', period=period,
            cost=cost, gear=gear, language='EN сайт; язык преподавания не подтверждён', languages=[],
            themes=['games', 'coding'] if 'Minecraft' in title else ['technology'], note=note,
            related_ids=['L016'])
    ns_ids.append(e['id'])
update('L016', age='LEGO Engineer 9–13; Generative AI 9–14; Little Explorer 5–6 — только weekly',
       period='Точные October AI / December LEGO группы вынесены в отдельные связанные карточки',
       language='EN материалы; язык преподавания каждой группы требуется подтвердить', languages=[],
       evidence_level='program', participation='unconfirmed_program', related_ids=ns_ids,
       note='Обзор провайдера, не дополнительная смена. Little Explorer 5–6 — регулярные занятия; программа Minecraft / 3D имеет только прошедшие даты. Английский сайт не является подтверждением EN преподавания.')

# Cobo publishes four camp-week windows and two age tracks. No campus/theme/time
# cross-product is invented where an actual availability grid is not published.
cobo = source('https://www.coboacademy.com/holiday-camps/index.asp', 'Cobo Academy — October2026 English camps', 'program',
              'English explicitly stated;four windowsOct5–9/12–16/20–23/26–30;ages6–8 and9–11;HKD4500/3600;chosen2hslot')
for first, last in [('2026-10-05', '2026-10-09'), ('2026-10-12', '2026-10-16'), ('2026-10-20', '2026-10-23'), ('2026-10-26', '2026-10-30')]:
    days = (datetime.date.fromisoformat(last) - datetime.date.fromisoformat(first)).days + 1
    for track, age, mat, osc, gear in [
            ('Junior', '6–8', 'Нет: Junior 6–8', 'Да по возрасту; наличие места и иностранный приём подтвердить',
             'По выбранной теме: LEGO WeDo / SPIKE, ScratchJr, Scratch, Codey Rocky, Tinkercad, Minecraft, AI'),
            ('Senior', '9–11', 'Да по возрасту; наличие места и иностранный приём подтвердить', 'Нет: Senior от 9',
             'По выбранной теме: VEX IQ, LEGO SPIKE, Python CodeCombat, Roblox Lua, Minecraft Java / Education Python, AI apps, 3D/VR')]:
        add('L', f'Cobo Academy {track} — October English Camp {first}', 'HKG', 'Гонконг — Wan Chai; Kowloon Tong по запросу', cobo,
            first, last, age=age, mat=mat, osc=osc,
            format=f'{days} {"дня" if days == 4 else "дней"} × 2 часа; выбрать утро 10:00–12:00 ИЛИ день 14:00–16:00; без проживания',
            cost=f'HKD {4500 if days == 5 else 3600} за {days}-дневный camp', gear=gear,
            language='EN — язык преподавания прямо указан организатором', languages=['EN'],
            language_certainty='На camp page прямо написано Medium of Instruction: English. Конкретный слот / тему подтвердить перед оплатой.',
            themes=['robotics', 'ai', 'coding', 'games'],
            entry='Выбрать Junior / Senior, неделю, тему, площадку и один 2-часовой слот; получить подтверждение свободного места и иностранных документов',
            venue='Wan Chai: 6/F Yam Tze Commercial Building, 23 Thomson Road. Kowloon Tong: 1/F HK Productivity Council, 78 Tat Chee Avenue — selected classes upon request.',
            note='Одна карточка означает неделю и возрастной поток, не гарантию каждой темы на каждой площадке. Сетка topic × campus × time не опубликована; варианты не размножены в фиктивные смены. 20–23 октября — 4 дня, не 5. Early-bird скидка до 30 сентября не является дедлайном регистрации.')

# Local Mexican candidates retain unannounced dates and language uncertainty.
logi = source('https://www.logiscool.com/mx/programs/lego-wedo-future', 'Logiscool México — LEGO WeDo camp6–9', 'program',
              'Ages6–9;in-person;equipmentprovided;nopreviousknowledge;futurecampdates/campus/language not stated')
add('L', 'Logiscool México — LEGO WeDo camp, будущая смена', 'MEX', 'Филиал в México выбрать и подтвердить', logi,
    age='6–9', mat='Да по возрасту; конкретную смену подтвердить', osc='Да по возрасту; конкретную смену подтвердить',
    themes=['robotics', 'coding'], priority='P1 — México, после объявления смены',
    entry='Запросить ближайший очный LEGO WeDo camp для 6 и 9 лет; подтвердить филиал, дни, язык и места',
    gear='LEGO WeDo и инструменты предоставляются; начальные знания не требуются',
    language='ES сайт; фактический язык выбранного филиала не подтверждён', languages=[],
    note='Точная будущая смена и цена на странице программы отсутствуют. Это кандидат, а не подтверждённый каникулярный слот; очный формат не заменён на online по старому общему каталогу.')
ciber = source('https://www.ciberbots.com.mx/services', 'Ciberbots Toluca — current holiday-program windows', 'program',
               'ChristmasDec2026,Easter2027,Summer2027;exactdays/ages/fees not published;regularcourse competitions restrictedschoolcourse')
for title, period, gear in [
        ('Christmas / Navidad 2026', 'Декабрь 2026; недели и точные дни не опубликованы', 'Робототехнические модели с рождественской темой'),
        ('Easter / Pascua 2027', 'Анонс Próximo 2027; точные дни не опубликованы', 'Mindstorms NXT / EV3, egg-механизмы по описанию'),
        ('Summer / Verano 2027', 'Анонс Próximo 2027; заявлены 4 недели, но даты не опубликованы', 'Mindstorms, WeDo, Boost, SPIKE, Arduino по выбранному уровню')]:
    add('L', 'Ciberbots Toluca — ' + title, 'MEX', 'Toluca — Paseo Matlazincas 2028, La Teresona', ciber,
        period=period, gear=gear, age='Возраст holiday camp не опубликован; регулярные классы имеют другие группы',
        themes=['robotics', 'coding'], priority='P1 — México, после объявления смены',
        entry='Запросить фактическую неделю, отдельные группы для 6 и 9, язык, стоимость и иностранный приём',
        language='ES материалы; язык каникулярной группы подтвердить', languages=[],
        note='Regular Preschool 4–6 / Beginner 7–8 / Basic 9–11 не перенесены автоматически на возраст лагеря. Competition route обозначен только для escolarizado курса: покупка holiday camp не обещает участие или медаль.')

assert before_ids <= {x['id'] for x in d['events']}
assert len(new_ids) == 61
assert len(d['events']) == 959
d['asof'] = DAY
corrections = [
    'GITEX Global expo dates corrected from Dec7–11 to Dec8–11; SummitDec7 distinguished',
    'Rome ticket tariffs and online-only booking; family8EUR not whole-family total; TaipeiOct24–25 network dates',
    'ITERA networkOct29–30 vs localNov19–20 without year: no confirmed calendar date',
    'Maker network dates are catalog evidence where host does not corroborate; failed hosts not labelled read',
    'Nullspace LEGO current page9–13;weekly5–6 not holidaycamp;English instruction not confirmed by English website',
    'Cobo explicit English and Junior6–8/Senior9–11; four actual weeks without invented topic/campus/slot combinations',
    'Penang2025 competition rules not rolled to2026; GITEX Asia2026 gate not claimed as2027 policy;Europe FAQ18+ not old21+',
    'Mexico holiday windows retained without invented exact dates, camp ages or Spanish teaching confirmation'
]
audit = dict(asof=DAY, baseline_records=898, added=len(new_ids), new_ids=new_ids,
             updated_ids=updated_ids, opened_primary_sources=list(sources.values()), corrections=corrections,
             unresolved=[
                 dict(topic='Maker Faire Vientiane / South Dallas', status='Host links failed; network dates only', sources=[NETWORK]),
                 dict(topic='ITERA México', status='Date conflict; organizer confirmation required', sources=[NETWORK, 'https://www.innovactiongym.biz/itera']),
                 dict(topic='Lisboa Games Week', status='FIL date read; child ticket / program not accessible', sources=[fil]),
                 dict(topic='Nullspace and Mexican camps', status='Specific teaching language and foreign short-stay admission not confirmed', sources=[robot, ai, logi, ciber]),
                 dict(topic='Exhibition games/AI contests', status='Visitor admission is not competition acceptance; child rules vary by activity', sources=[challenge, penang])
             ],
             limits='Counts include providers, editions, age tracks and actual sessions; not independent world festivals. No country is fully audited. All three worldwide research blocks remain in progress.')
(ROOT / 'data/audit-v8.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2))
source_index = {s['url']: s for s in d['sources']}
for s in sources.values():
    source_index[s['url']] = {k: s[k] for k in ['url', 'title', 'evidence', 'checked']}
d['sources'] = list(source_index.values())
d['source_count'] = len(d['sources'])
d['expansion_log'].append(dict(date=DAY, version='v8', baseline_records=898, added=len(new_ids),
                               events_total=len(d['events']), new_ids=new_ids, updated_ids=updated_ids,
                               corrections=corrections, sources=f'{len(sources)} opened primary resources; failures and unverified local gates retained'))
CATALOG.write_text(json.dumps(d, ensure_ascii=False, indent=2))
plan_path = ROOT / 'data/research-plan.json'
plan = json.loads(plan_path.read_text())
plan['status'] = 'active'
plan['updated'] = DAY
evidence = {
    'global_competitions': '759 cards. v8 adds Maker Challenge Brno Oct17 with actual jury schedule, prototype constraints and unknown age/team/foreign eligibility; remaining worldwide league audits still partial.',
    'camps': '118 cards. v8 adds Cobo8 English age/week options, Nullspace5 Decrobotics and9 OctAI workshops, regular5–6 and2 futureundated programs, MexicoWeDo and3Ciberbots windows. Exact availability and foreign admission remain unconfirmed.',
    'exhibitions': '82 cards. v8 adds24 Maker network editions plus Hannover2027, Penang, HongKongInnoCarnival, LisboaGamesWeek and3 GITEX edition/gate records. ITERA dates conflict; some network dates have no corroborating host rules.',
}
for row in plan['requirements']:
    if row['id'] in evidence:
        row['evidence'] = evidence[row['id']]
    if row['id'] == 'web':
        row['evidence'] = row['evidence'].replace('Существующий закрытый STEM Atlas', 'Опубликованный публичный STEM Atlas')
    if row['id'] in ['web', 'unified_database']:
        row['status'] = 'implemented_pending_v8_validation'
plan['latest_validation'] = dict(version='v8', records=959, baseline_ids_preserved=898,
                                 ui='pending', database='pending', research_status='active')
plan['next_research'].extend([
    'Cobo: exact topic/campus/time availability and foreign family entry. Nullspace: explicit teaching English and actual vacancies, not website language.',
    'México ITERA date conflict; Ciberbots exact holiday days/ages/language and Logiscool actual branch camps. Keep CostaRica/México/LATAM as priority.',
    'Maker network hosts and all other exhibition networks; worldwide game/AI/technology fairs and national calendars remain incomplete.'
])
plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2))
print(json.dumps(dict(records=len(d['events']), added=len(new_ids), updated=updated_ids,
                      opened_sources=len(sources), blocks={b: sum(e['block'] == b for e in d['events']) for b in ['Соревнования', 'События', 'Лагеря']}), ensure_ascii=False))
