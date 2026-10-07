"""Taiwan primary-source pass: admission, languages, separate disciplines.

Run once on v14. Future shifts are never derived from last year's timetable.
Birth years come from the user; grades, exact birthdays and language fluency
remain unknown. Local national selection is not an overseas open invitation.
"""
import copy, datetime, json, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/catalog.json'
d = json.loads(PATH.read_text())
DAY = '2026-10-01'
assert len(d['events']) == 1046 and d['completeness_audit']['version'] == 14
baseline = copy.deepcopy(d['completeness_audit']['counts'])
old_ids = {e['id'] for e in d['events']}
byid = {e['id']: e for e in d['events']}
new, updated = [], []

def source(url, title, evidence):
    s = next((s for s in d['sources'] if s['url'] == url), None)
    if s: s.update(checked=DAY, evidence=evidence)
    else: d['sources'].append(dict(url=url, title=title, evidence=evidence, checked=DAY))

def update(id, **kw):
    e = byid[id]
    e.update(checked=DAY, **kw)
    if id not in updated: updated.append(id)
    source(e['source'], e['title'], e['proof'])
    return e

def add(id, block, title, city, url, start='', end='', **kw):
    assert id not in old_ids | set(new)
    e = dict(id=id, block=block, title=title, country='Тайвань', region='Азия', city=city,
        source=url, references=[], checked=DAY, start=start, end=end or start,
        date_status='Подтверждено' if start else 'Даты не объявлены',
        period='' if start else 'Следующие точные дни не объявлены', deadline='',
        age='Возраст / школьный класс выбранной категории уточнить',
        mat='Условно — подтвердить класс и иностранный допуск; год рождения 2017',
        osc='Условно — подтвердить класс и иностранный допуск; год рождения 2020',
        format='Командная категория; состав уточнить', participation='team',
        entry='Выбрать категорию, получить подтверждение иностранного допуска и языка; проверить места до оплаты.',
        gear='Технический регламент конкретной дисциплины', cost='Действующую стоимость уточнить',
        language='Язык занятий / судейства не подтверждён', languages=[],
        language_certainty='Английский сайт или PDF не доказывают английское преподавание / судейство.',
        scope='regional', level='Региональный турнир / программа',
        importance_reason='Редакционная оценка содержания и пути допуска; общего мирового рейтинга нет.',
        reward='Конкурсный результат только по официальному протоколу',
        priority='P2 — поездка после проверки допуска', status='Идея',
        action='Подтвердить категорию, школьный статус, язык и действующий набор.',
        themes=['robotics','technology'], admission_kind='open_application', evidence_level='event_page',
        registration_status='Семья не зарегистрирована; дата не подтверждает наличие места.',
        proof='Прочитан первичный источник; неизвестные условия сохранены.', note='')
    e.update(kw)
    d['events'].append(e); byid[id]=e; new.append(id)
    source(url,title,e['proof'])
    return e

def ref(e, url, label, evidence):
    e.setdefault('references',[]).append(dict(url=url,label=label))
    source(url,label,evidence)

first_url = byid['C033']['source']
first_pdf = 'https://www.era.org.tw/main/wp-content/uploads/2026/09/' + urllib.parse.quote('2026-2027-FIRST機器人大賽-台灣選拔賽_簡章-1.pdf')
first_entry = 'Регистрация и оплата 01.10.2026 12:00 — 22.10.2026 23:59 Asia/Taipei. Для иностранной семьи отдельно подтвердить школу / клуб, право участвовать в тайваньском отборе и право международной квоты; возраст сам по себе этого не доказывает.'
first_note = 'Прочитан регламент v4 от 16.09.2026: школьные диапазоны в названиях Founders и возраст в разделе допуска указаны отдельно. Классы детей не сообщены. Оплата определяет очередность мест; форма без оплаты не завершает регистрацию. Условия иностранного входа и EN-судейства не опубликованы явно. Сначала подтверждение организатора, затем платеж.'
for id, age, team, mat, osc in [
    ('C033','6–10 лет, до 11-летия на день соревнования; название Founders Grades 2–4', (2,6),
     'Условно — 2017 год рождения подходит по возрасту; класс / иностранный вход подтвердить',
     'Условно — 2020 год рождения подходит по возрасту; класс / иностранный вход подтвердить'),
    ('C034','9–16 местный этап; 9–14 для международного представительства; Founders Grades 4–8', (5,10),
     'Условно — 2017 год рождения подходит по возрасту; класс / иностранный вход подтвердить',
     'Нет — 2020 год рождения: младше минимальных 9 лет в январе 2027')]:
    e=update(id, age=age, mat=mat, osc=osc, city='Kaohsiung · Social Education Center, 115 Xuefu Road, Xiaogang',
        format=f'Команда {team[0]}–{team[1]} детей + до 2 совершеннолетних наставников',
        team_min=team[0], team_max=team[1], entry=first_entry, cost='NT$1 800 за участника; льготы отдельных местных школ не перенесены на семью',
        deadline='2026-10-22', deadline_label='Регистрация и оплата FIRST Taiwan',
        deadline_utc='2026-10-22T15:59:00Z', deadline_note='23:59 Taiwan = 09:59 Costa Rica. Набор начался 01.10; лимит Explore 72 / Challenge 48 команд.',
        note=first_note + (' Explore прямо не имеет квоты Houston 2027; местное признание не обещает мировой медали.' if id=='C033' else ' Квоты Houston / других open events зависят от FIRST; тайваньское представительство семьи не подтверждено.'),
        proof='Повторно прочитаны регистрационная страница и все 10 страниц первичного v4: дни, возраст, команды, стоимость, окончание приёма и разные международные маршруты.')
    ref(e,first_pdf,'FIRST Taiwan 2026–2027 · регламент v4','10 страниц прочитаны: Explore без Houston quota; Challenge и MARC имеют разные возрастные / командные правила.')

# Keep the existing MARC ID for LOM; TM becomes a separate discipline, not a
# duplicate of a still-combined card. The same child may enter only one MARC.
e=update('C035', title='MARC Taiwan · LOM Elementary · 2027',
    age='Годы рождения 2016–2021, начальная школа; 2–3 участника и 1 взрослый наставник',
    mat='Условно — 2017 входит в 2016–2021; школа и иностранный вход уточнить',
    osc='Условно — 2020 входит в 2016–2021; школа и иностранный вход уточнить',
    city='Kaohsiung · Social Education Center, 115 Xuefu Road, Xiaogang',
    format='Команда 2–3 ребёнка + 1 совершеннолетний наставник', team_min=2, team_max=3,
    birth_start='2016-01-01', birth_end='2021-12-31', entry=first_entry,
    gear='MARC LOM: регламент и набор своей категории; FLL-набор не автоматически совместим',
    cost='NT$1 800 за участника; техника и поездка отдельно',
    deadline='2026-10-22', deadline_label='Регистрация и оплата MARC Taiwan', deadline_utc='2026-10-22T15:59:00Z',
    note='Два ребёнка подходят по году рождения и количеству игроков; школьный статус, уровень и иностранный вход требуют подтверждения. Один игрок может выбрать только один MARC — LOM либо TM; сочетание с FIRST допускается. Минимум 6 команд для проведения категории; лимит 24 Elementary команды и 2 от одной организации. Победителям описан путь MARC International, но право иностранной семьи на квоту не установлено. STEAM SQUAD Expedition проходит и 1 февраля: совместить целиком оба расписания нельзя.',
    proof='Прочитан v4 ERA: LOM Elementary рождения 2016–2021, команды 2–3, 01.02.2027; исключение двойного MARC и минимум категории.')
ref(e,first_pdf,'MARC LOM / TM: отдельные правила в v4','Годы рождения отличаются; выбор одного MARC на ребёнка; международная квота требует проверки.')
e=add('C779','Соревнования','MARC Taiwan · TM Elementary · 2027',byid['C035']['city'],first_url,'2027-02-01',
    age='Годы рождения 2015–2019, начальная школа; 2–3 игрока + 1 взрослый наставник',
    mat='Условно — 2017 входит в 2015–2019; иностранный допуск уточнить',
    osc='Нет — 2020 не входит в допустимые годы рождения 2015–2019',
    format='2–3 участника и взрослый наставник',team_min=2,team_max=3,
    birth_start='2015-01-01',birth_end='2019-12-31', entry=first_entry,
    gear='MARC TM: автономный и управляемый этапы, своя платформа / manual',
    cost='NT$1 800 за ребёнка; лимит 8 команд Elementary',
    deadline='2026-10-22',deadline_label='Регистрация и оплата MARC Taiwan',deadline_utc='2026-10-22T15:59:00Z',
    proof='Прочитан ERA v4: TM 2015–2019, 2–3 игрока, 01.02.2027, NT$1800; автономный этап до 30 секунд и управление до 90 секунд.',
    note='Оскар 2020 не может быть вторым игроком TM. Матвею понадобится другой партнёр. Один ребёнок не участвует одновременно в LOM и TM; C035 сохранён и теперь описывает только LOM. Международное название и победа не подтверждают семейную квоту.')
ref(e,first_pdf,'MARC TM · первичный регламент v4','Точные годы рождения и запрет двух MARC-дисциплин одному участнику.')

jbc='https://junior-botball-challenge-taiwan.github.io/'
add('C778','Соревнования','Junior Botball Challenge Taiwan · Taichung · 2026',
    'Taichung · Wagor International Conference Center, 328 Junfu 18th Road, Beitun',jbc,'2026-12-13',
    age='Младшие уровни и школьные группы; точный год рождения / класс по локальной категории не установлен',
    format='Задачи Junior Botball; конкретные составы команд по руководству',
    gear='Своя платформа / kit по правилам локального уровня; совместимость LEGO не подтверждена',
    period='Утром 09:00–12:15 школьные группы; 13:30–17:30 младшие уровни',
    proof='Прочитана страница SPARK: 13.12.2026, площадка, две части дня, младшие уровни и документы отдельной папкой.',
    reward='Сертификат выполненных задач; место / награда только по протоколу выбранного уровня',
    note='Доступность иностранцам, число игроков, стоимость, deadline и EN-судейство не подтверждены. Название сертификата «international future engineer» не превращает его в международную победу. Локальное обещание GCER USA July 2027 не сверено с KIPR; автоматическая квота / оплаченная поездка не обещаны.')

tirtbase='https://www.tirtpointsrace.org/Registration/Event/'
sumo_spec='https://www.tirtpointsrace.org/Files/Docs/EventDoc/ca28e72a-26a0-49fc-8bc6-8e26fac27c68/2026%20TIRT%20%E2%80%93%20Lightweight%20Sumo%20Robot%20Competition%20Robot%20Specifications.pdf'
sumo_rules='https://www.tirtpointsrace.org/Files/Docs/EventDoc/ca28e72a-26a0-49fc-8bc6-8e26fac27c68/2026TIRT-Lightweight%20Sumo%20Robots.pdf'
tirt_conflict='На event page deadline 18.10.2026, в английском регламенте 25.09.2026 с оговоркой возможного изменения. Не установлен приоритет версий: активный набор подтвердить до покупки перелёта.'
e=update('C036', mat='Условно — начальная школа и справка об обучении в своей стране; допуск подтвердить',
    osc='Условно — нужна начальная школа и справка; год рождения 2020 сам по себе не доказывает класс',
    format='Elementary команда максимум 3 ребёнка; минимальный состав подтвердить',team_max=3,
    deadline='2026-10-18',deadline_label='TIRT: срок страницы, конфликт с PDF', deadline_utc='',
    deadline_note=tirt_conflict, language='Английские PDF правил опубликованы; EN-судейство не подтверждено',languages=[],
    gear='Прочитанный EN spec May 01, 2026: модульная пластиковая основная конструкция, 15–25 см по каждой оси, ≤2500 г с батареей, питание ≤9V, автономность; 3D-печать вспомогательная. Не ограничено названием EV3.',
    entry='Правила допускают международные команды того же школьного уровня со справкой об обучении в своей стране. Подтвердить набор и актуальную техническую редакцию.',
    proof='Прочитаны страница категории, 14-страничный EN регламент и 10-страничный EN spec: иностранные школы, максимум 3, Nov8, size / weight / 9V / автономность; конфликт срока сохранён.',
    note=tirt_conflict+' В EN PDF смешаны даты обложки 2025 и тела 2026. Прочитанный spec помечен May 01, 2026; ранее записанная дата 30.09 не подтверждена как текущая редакция. Последнюю CN/EN редакцию согласовать. Радиоуправление запрещено; сопровождающий родитель без аккредитации coach не получает доступ в зону соревнования.')
ref(e,sumo_spec,'TIRT Sumo · EN technical specifications','Прочитаны 10 страниц: 15–25cm, 2500g, 9V, один controller, автономный ход, модульная основная конструкция.')
ref(e,sumo_rules,'TIRT Sumo · EN competition regulations','Международные школьные команды со справкой; conflicting September25 / October18 deadlines.')
tirt_new=[]
for id, slug, title, date, age, fmt, gear, osc, note in [
    ('C780','6efc92ac-a3bb-4007-ae58-75839130189d','Autonomous Vehicle Maker · Open Elementary','2026-11-07',
     'Elementary school; EN PDF отдельно пишет public elementary schools, иностранным нужна справка',
     'Команда максимум 3 игрока; минимум уточнить',
     'Автономная машинка по белой линии; пластиковые building blocks, длина <20см, ширина / высота <15см, один controller; 3D-печать только вспомогательная',
     'Условно — школьный уровень и зарубежную справку подтвердить',
     tirt_conflict+' EN PDF допускает international teams, но одновременно указывает public elementary schools: частная школа / homeschool требуют отдельного ответа. Открытый controller не означает свободный размер / конструкцию.'),
    ('C781','501f8579-ffbb-4d94-9ff5-bd11485ffc4a','TURBOT AI Smart Driving · Elementary L-1','2026-11-07',
     '7–12 лет по PDF V07; 1–3 игрока и один coach',
     '1–3 игрока + coach; школьные группы могут смешиваться',
     'Elementary: TURBOT AI smart car / TENCODE board; cross-grade использует Pixetto и другой technical route',
     'Нет — 2020 год рождения: в ноябре 2026 максимум 6 лет, минимум 7',
     'V07 указывает бесплатную онлайн-регистрацию; действующий набор и иностранный вход уточнить. Английское описание сайта не доказывает EN-судейство. Elementary решает избегание препятствий; задачи распознавания cross-grade не перенесены на L-1.'),
    ('C782','59738e20-8d39-4b38-b373-e30cb4be7d5e','Automation Shipping Challenge · J-2','2026-11-08',
     'Начальная / junior high school, mixed group; точный младший класс уточнить',
     '2–3 игрока: погрузчик, роботизированная рука, Probbie; два игрока допускаются PDF',
     'Свои forklift, robotic arm и Probbie robot; оснащение не обещано организатором',
     'Условно — начальная школа / школьная справка и иностранный допуск',
     'На странице описание команды из трёх, но EN rule допускает 2–3. При двух игроках оператор руки совмещает роль. Не переносить правила иностранного допуска Sumo на эту дисциплину без подтверждения.'),
    ('C783','54876e6e-aeb1-4d8a-9d9a-201ec0419d8b','Robot Soccer · Elementary T-1','2026-11-08',
     'Начальная школа, Elementary T-1; точный класс / состав по TEMI manual уточнить',
     'На поле три робота; это не подтверждает число детей в команде',
     'TEMI robot soccer equipment / правила от 11.06.2026; нужный kit уточнить',
     'Условно — школьный уровень / иностранный вход подтвердить',
     'Не путать с Humanoid Korfball C-3: там старшая школа / университет и детям не подходит. Прочитана именно страница Robot Soccer с T-1, а полный TEMI technical manual ещё не разобран.')]:
    e=add(id,'Соревнования','TIRT 2026 · '+title,'Taoyuan Arena · 1 Sanmin Road Section 1',tirtbase+slug,date,
        age=age,format=fmt,gear=gear,osc=osc,
        deadline='2026-10-18',deadline_label='TIRT: срок страницы; актуальность подтвердить',
        deadline_note=tirt_conflict if id=='C780' else 'Event page: 18.10.2026; точный час не опубликован.',
        cost='Регламент V07: регистрация бесплатно; техника / поездка отдельно' if id=='C781' else 'Действующий регистрационный тариф уточнить',
        themes=['robotics','ai','technology'] if id=='C781' else ['robotics','technology'],
        proof='Прочитана первичная event page с точной дисциплиной, группой, Nov7/Nov8, площадкой и Oct18. '+('Дополнительно прочитан связанный PDF правил.' if id!='C783' else 'Полный technical PDF ещё требует проверки.'),note=note)
    tirt_new.append(id)
    if id=='C781': e.update(team_min=1,team_max=3)
    if id=='C782': e.update(team_min=2,team_max=3)

for id, filename, label in [
    ('C780','2026TIRT-Autonomous Vehicle Maker Challenge - Open Group - Elementary School Student Group.pdf','TIRT Open Car · EN Elementary rules'),
    ('C781','2026TIRT_AI車輛挑戰賽V07.pdf','TIRT TURBOT · V07 rules'),
    ('C782','2026TIRT-Automation Shipping Challenge – Team Competition.pdf','TIRT Shipping · EN team rules')]:
    slug=byid[id]['source'].rsplit('/',1)[1]
    url='https://www.tirtpointsrace.org/Files/Docs/EventDoc/'+slug+'/'+urllib.parse.quote(filename)
    ref(byid[id],url,label,'Прочитан связанный первичный PDF: состав команды, оснащение и правила именно этой дисциплины.')

grg='https://global-robotics-games-taiwan.github.io/'
grg_ids=[]
for id,name,age,mat,osc,gear,note in [
    ('C784','Mission Robot 1','7–9 лет на локальной странице SPARK',
     'Условно — в 2026 возраст 9 подходит; для следующего этапа проверить отсечение, в 2027 исполняется 10',
     'Условно — только после 7-летия в 2027 и подтверждения следующего этапа; сейчас 6',
     'SPIKE Essential / WeDo 2.0; MR1 manual: автономная миссия, до 250мм куба',
     'Матвей и Оскар могут оказаться по разные стороны возрастной границы MR1 в 2027. Не считать общую семейную категорию доступной по текущим возрастам.'),
    ('C785','Mission Robot 2','10–12 лет на локальной странице SPARK',
     'Условно — только после нужного возрастного отсечения в 2027; сейчас 9',
     'Нет — 2020 год рождения, до 10-летия ещё несколько лет',
     'SPIKE Prime / EV3, правила MR2 выбранного сезона',
     'Возраст на дату либо календарный год отсечения не установлен. День этапа пока не опубликован; 2017 не даёт автоматического допуска ко всему 2027 сезону.'),
    ('C786','AIMS AI vision challenge','Противоречие местной страницы: 7–12 / 13–16 против Primary 9–12 / Secondary 12–17',
     'Условно — 2017 потенциально младшая группа; выбрать официальный возрастной вариант',
     'Нет по всем прочитанным младшим порогам 7/9 при текущих 6; будущий допуск требует нового manual',
     'Автономное распознавание и сбор зрелых плодов; AI vision kit / platform по AIMS manual',
     'Сохранён конфликт age bands на одной первичной странице. EN task rules не разрешили эту неоднозначность; нельзя выбирать удобный семье порог.'),
    ('C787','Open Project','От primary до high school; точные годы рождения / классы не объявлены в прочитанной странице',
     'Условно — школа, состав и иностранное участие требуют подтверждения',
     'Условно — нужен допуск конкретной младшей школьной группы',
     'Открытая проектная робототехника; видео и очная презентация, платформу / команду сверить',
     'Проектная программа, а не автоматическая глобальная медаль; критерии самостоятельного вклада и язык защиты уточнить.')]:
    add(id,'Соревнования','GRG Taiwan · '+name+' · следующий местный этап',
        'Город / площадка тайваньского этапа не объявлены',grg,
        age=age,mat=mat,osc=osc,gear=gear,
        period='На локальной странице GRG 2026 нет точных дней тайваньского этапа; следующий сезон не датирован',
        scope='regional',
        themes=['robotics','ai','coding'] if id=='C786' else ['robotics','coding'],
        proof='Прочитаны локальная страница SPARK и сайт глобального GRG: отдельные младшие категории и путь в Singapore; точных локальных дат нет.',
        note=note+' SPARK описывает рекомендацию / приоритетное приглашение Singapore и обязательную поездку своей группой. Прямая независимая регистрация зарубежной семьи через Taiwan не подтверждена. Singapore — место международного финала, не площадка этой тайваньской карточки.')
    grg_ids.append(id)
ref(byid['C784'],'https://global-robotics-games-taiwan.github.io/rules/mr1_rules_en.html','GRG MR1: EN task rules','Прочитаны задачи и SPIKE Essential / WeDo; локальный возраст не заменяет международного отсечения.')
ref(byid['C786'],'https://global-robotics-games-taiwan.github.io/rules/aims_rules_en.html','GRG AIMS: EN task rules','Прочитаны vision / picking tasks; конфликт возраста overview остаётся.')
source('https://www.globalroboticsgames.com/','GRG international organizer','Прочитана первичная глобальная страница: инициатива Developing Innovative Youth, международное событие Singapore; не подтверждает Taiwan dates / квоту иностранца.')

wro='https://www.era.org.tw/main/category/game/game-wro/wro-2026/'
wropdf='https://www.era.org.tw/main/wp-content/uploads/2026/06/'+urllib.parse.quote('2026年WRO國際奧林匹亞機器人暨MARC-AI全國總決賽計劃書_v3.1.pdf')
e=add('C788','Соревнования','WRO Taiwan · локальные отборы / national route · следующий сезон',
    'Тайвань: school cups / региональные этапы / national; дни и города следующего сезона уточнить',wro,
    age='2026 Elementary RoboMission / Future Innovators: рождения 2014–2018; правила следующего сезона не объявлены',
    mat='Условно — 2017 подходит старому Elementary диапазону; новый сезон и Taiwan school affiliation подтвердить',
    osc='Нет — 2020 не входит в прочитанный диапазон WRO Elementary 2026; следующую младшую категорию ещё проверить',
    format='2–3 игрока + взрослый coach; school / regional / online qualification в national',
    team_min=2,team_max=3, scope='national',admission_kind='qualifier',
    gear='RoboMission / Future Innovators по соответствующему manual; не смешивать с отдельным MARC',
    cost='В national2026 указана бесплатная регистрация; не подтверждён тариф будущего местного отбора',
    entry='ERA: school cup / regional / online selection → Taiwan national → мировая квота. Частные, государственные и foreign schools в Taiwan допускаются; семья из Costa Rica не равна ученикам foreign school в Taiwan.',
    historical_editions=[dict(start='2026-08-20',end='2026-08-23',venue='Ling Tung University, Chun-an campus',status='Прошло; не новая дата 2027')],
    proof='Прочитан национальный план v3.1 June18,2026, все 5 страниц: пути отбора, birth bands, команды2–3, включение foreign schools и обязательное Taiwan представительство победителей.',
    note='Дни national20–23.08.2026 уже прошли; даты2027 не выведены из прошлого года. Часть school cups имеет строгий county gate. Допуск foreign schools относится к местной школьной системе, не обещает вход туристам. Нельзя сменить national federation ради удобной квоты. Новый сезон и право семьи требуют отдельного подтверждения.')
ref(e,wropdf,'WRO Taiwan · national plan 2026 v3.1','Birth2014–2018 для Elementary2026; иностранные школы Taiwan,2–3, местный отбор и национальное представительство.')

# Exhibitions: exact new dates and edition-specific family admission.
smart='https://smartcity.org.tw/smartcity.php'
e=update('E024',start='2027-03-16',end='2027-03-19',date_status='Подтверждено',period='',
    city='Taipei · Taipei Nangang Exhibition Center Hall 2, 2 Jingmao 2nd Road',source=smart,
    age='Детский вход 2027 не найден в прочитанной первичной странице; подтвердить 6/9 со взрослым',
    mat='Условно — нужен детский пропуск / подтверждение 2027',osc='Условно — нужен детский пропуск / подтверждение 2027',
    proof='Прочитана первичная Smart City Expo page: 16–19.03.2027, Taipei Nangang Hall2, AI / resilient sustainable cities.',
    note='Статистика 2026 Taipei+Kaohsiung не является прогнозом состава стендов2027. Четыре дня Taipei не перенесены на Kaohsiung; точные Kaohsiung2027 и детский вход остаются в backlog.')
e['visitor_policy_note']=e['age'];e['adult_entry']=e['entry']
makerpdf='https://drive.google.com/file/d/1tSOKbL3xyif9TBvpySexVXpZAkYGtvGW/view?usp=drive_link'
e=update('E027',city='Taipei · POPOP Taipei, No.13 Sec.2 Nangang Road',
    age='Семейный вход. Бесплатно: ребёнок младше 6 лет ИЛИ рост ниже 115 см, с взрослым. Для возраста 6/9 сам по себе free age gate не выполнен.',
    mat='Да — семейный посетитель с взрослым; билет по тарифу',
    osc='Да — семейный посетитель с взрослым; бесплатно только если рост <115см, иначе билет',
    format='Семейный maker-фестиваль 24–25.10.2026, 10:30–17:30 Asia/Taipei',
    cost='Предпродажа: NT$250 один / NT$399 два early-bird. На месте: adult350 / student260 / group200. Доступность конкретного тарифа уточнить.',
    entry='Билет посетителя Maker Faire2026. Workshop / показ собственного проекта требуют отдельной записи и отбора; детский вход не включает автоматически платные занятия.',
    proof='Прочитан и визуально проверен текущий Application Guide2026: POPOP Nangang,24–25Oct10:30–17:30, билеты, under6 OR under115cm; описаны family/co-creation directions.',
    note='Площадка POPOP Taipei подтверждена руководством2026, не перенесена из старого выпуска. Оскар2020 в октябре2026 может быть5/6 до точного дня рождения; по сообщённому текущему возрасту6 бесплатность проверяется по росту, не обещана. Язык конкретного workshop, расходники и свободные места уточнить. Показ собственного проекта — отдельная заявка; не автоматическая победа.')
e.update(visitor_policy='family',visitor_policy_note=e['age'],adult_entry=e['entry'])
ref(e,makerpdf,'Maker Faire Taipei2026 · Application Guide','Визуально прочитана таблица текущего издания: POPOP, часы, тарифы, under6 OR under115cm. Общий exhibitor guide содержит реальные visitor admission условия.')
invent='https://www.inventaipei.com.tw/zh-tw/index.html'
inventgate='https://www.inventaipei.com.tw/zh-tw/menu/9AE53DD53E13DB84D0636733C6861689/info.html'
e=add('E129','События','Taiwan Innotech Expo · 2027','Taipei · площадку выпуска2027 подтвердить',invent,'2027-10-14','2027-10-16',
    age='2027 child policy ещё не опубликована в прочитанном тексте. Последнее правило2026: общий публичный вход, дети до12 включительно с родителем.',
    mat='Условно — семейное правило2026 положительное; подтвердить его для2027',
    osc='Условно — семейное правило2026 положительное; подтвердить его для2027',
    format='Посещение изобретательской / технологической выставки',participation='visitor',admission_kind='visitor',
    themes=['robotics','ai','technology'],scope='international',level='Крупная профильная международная выставка изобретений Taiwan',
    entry='Для общего посетителя проверить правила2027 и билет; foreign professional preregistrationQR+business card — другой маршрут, не обязательный статус ребёнка.',
    gear='Не требуется посетителю; участие в invention competition — отдельный регламент',
    reward='Посещение и знакомство с технологиями; visitor badge не даёт конкурсного результата',
    historical_editions=[dict(start='2026-09-17',end='2026-09-19',venue='Taipei World Trade Center Hall1',visitor_policy='12 и младше с родителем; общий публичный вход',status='Прошедший выпуск; не доказательство admission2027')],
    proof='Прочитаны главная с отдельным приглашением14–16.10.2027 и admission page2026: public visitors, age≤12 with parent, professional foreign route отдельно.',
    note='Date2027 подтверждена, но остальные страницы ещё содержат2026. ПлощадкаTWTC1 и детская policy описывают2026, не автоматически2027. Названия всех будущих компаний не установлены; прошлогодние стенды не гарантированы.')
e.update(exhibition_tier='regional',visitor_policy='confirm_children',visitor_policy_note=e['age'],adult_entry=e['entry'],
    highlights=['Изобретения и патентуемые технологии','AI и прикладные разработки','Научные / промышленно-технологические проекты'],
    exhibitors=[],exhibitor_note='Состав будущих стендов2027 не подтверждён; список2026 не перенесён.',
    exhibitor_directory_url=invent,event_group='Taiwan Innotech Expo')
ref(e,inventgate,'Taiwan Innotech Expo · admission2026','Общий публичный вход; age≤12сродителем. Подтверждение2027 требуется.')

# Camps: teaching English is explicit for these two winter providers, not
# inferred from the English-language UI. Availability and foreign intake unknown.
steam='https://steamsquad.io/en/camps/expedition27'
dates=['2027-01-21','2027-01-22','2027-01-25','2027-01-26','2027-01-27','2027-01-28','2027-01-29','2027-02-01','2027-02-02','2027-02-03']
topics=['Городские научные наблюдения','Механизмы и движение','Археология и инженерное наблюдение','Материалы и огонь','Вода и механизмы','Железнодорожные системы','Морская инженерия','Энергия','Животные и полёт','Финальное полевое исследование; маршрут зависит от погоды']
add('L142','Лагеря','STEAM SQUAD · Expedition27 · English winter camp',
    'Taipei · Beitou classroom, No.139 Sec.1 Zhongyang North Road',steam,'2027-01-21','2027-02-03',
    age='Рекомендуемый возраст8–12, не опубликованный жёсткий minimum. 10 учебных будней, выходные свободны.',
    mat='Да по рекомендуемому возрасту — 2017,9/10 в январе2027; иностранный приём и места уточнить',
    osc='Условно — 2020,6/7 в январе2027 ниже рекомендуемых8; нужна явная возрастная уступка',
    language='EN — английский язык занятий прямо указан провайдером',languages=['EN'],
    language_certainty='Подтверждён язык конкретной Expedition27; готовность ребёнка к целому дню EN не сообщена.',
    format='Дневной лагерь / полевые поездки:10будней09:00–17:30, только полный пакет; без проживания',
    participation='day_camp',admission_kind='program',scope='local',level='D — инженерное и научное каникулярное обучение',
    themes=['technology'], gear='Материалы включены; EasyCard и одежда / личные вещи для поездок',
    cost='NT$24000early bird /27000standard за10дней; материалы,обед,перекус,стандартные входы,страхование включены; транспортEasyCard примерно200/день дополнительно',
    deadline='2026-12-05',deadline_label='Expedition27: получение ранней оплаты',
    deadline_note='Early bird зависит от полученной оплаты до05.12; час не опубликован. Это не общий deadline регистрации. К05.01.2027 нужно минимум8 детей, иначе отмена/возврат.',
    entry='Уточнить иностранный приём, пригодность возраста и EN, свободное место; enquiry не резервирует пакет / скидку. Минимум8,максимум12 участников.',
    sessions=[dict(date=day,topic=topic,start_time='09:00',end_time='17:30',timezone='Asia/Taipei') for day,topic in zip(dates,topics)],
    reward='Инженерное обучение и проекты; не конкурсная медаль',
    proof='Прочитана конкретная Expedition27:21Jan–3Feb2027,10weekdays,EN,recommended8–12,Beitou,09–17:30,тариф и две контрольные даты.',
    note='Роботы и ИИ не гарантированы: это широкая science/engineering field expedition. Субботы/воскресенья21Jan–3Feb не являются учебными днями. В финале горный маршрут зависит от погоды. Даты пересекаются с MARC01Feb в Kaohsiung: полный10-дневный пакет и MARC целиком несовместимы. Участие или доверие провайдеру независимо семьёй не подтверждены.')
grove='https://thegrove.com.tw/seasonal-camps-2026-space-adventure/2027-winter-camp-ready-to-soar/'
groveform='https://forms.gle/BdYZKcEbnjSNLvG46'
e=add('L143','Лагеря','The Grove · Ready to Soar · English STEM winter2027',
    'Zhubei · The Grove; адрес выбранного класса подтвердить',grove,'2027-01-25','2027-01-29',
    age='Точный возраст и классы в первичной странице / форме не указаны; группа8 детей',
    mat='Условно — провайдер должен подтвердить приём2017 / EN уровень',
    osc='Условно — провайдер должен подтвердить приём2020 / EN уровень; младший возраст не заявлен',
    language='EN основной язык; местный помощник использует китайский',languages=['EN'],
    language_certainty='Форма конкретной2027смены: EnglishSTEM, американский английский основной, Chinese вспомогательный. EN-only поддержка иностранного ребёнка ещё не подтверждена.',
    format='5утренних дней09:00–12:00; дневная STEMпрограмма полёта,без проживания',
    participation='day_camp',admission_kind='program',scope='local',level='D — каникулярное инженерное обучение',themes=['technology'],
    entry='Согласовать возраст/уровеньEN обоих детей и иностранные документы. Форма→LINEconfirmation→NT$2000deposit резервирует место. Наличие места неизвестно.',
    cost='До16.10.2026: NT$7900+900materials=8800. С17.10:8800+900=9700. Deposit2000; детали включения депозита в общую сумму уточнить.',
    deadline='2026-10-16',deadline_label='The Grove: окончание раннего тарифа',
    deadline_note='Early bird, не окончание всего набора; точного часа нет. Отсутствие ребёнка не даёт компенсации / переноса по форме.',
    sessions=[dict(date=(datetime.date(2027,1,25)+datetime.timedelta(days=i)).isoformat(),topic='Инженерия полёта: проект дня по программе Ready to Soar',start_time='09:00',end_time='12:00',timezone='Asia/Taipei') for i in range(5)],
    gear='Материалы тарифицируются отдельноNT$900; ноутбук не заявлен',reward='5STEM-проектов / внутригрупповой показ; не международный турнир',
    proof='Прочитаны2027landingpage и связанная публичная форма без заполнения:25–29Jan,09–12,8детей,ENосновной/Chineseпомощь,два тарифа и депозит.',
    note='Это полётная STEMинженерия, не гарантированный robotics/AIcamp. Возраст не придуман из картинок / отзывов. Выходные30–31Jan можно отдельно рассматривать для FIRSTKaohsiung только после иностранного допуска; дорогаZhubei→Kaohsiung и отдых требуют отдельного планирования. Родительскую форму и платежи семья не отправляла.')
ref(e,groveform,'The Grove2027 · публичная registration form','Прочитаны будущие точные даты, часы, два тарифа,deposit,ENmain/Chineseassistant; числового возраста нет.')

typa='https://www.typa.org.tw/course/summer-camps/tech-camp/'
typareg='https://www.typa.org.tw/registration-information/'
e=add('L144','Лагеря','TYPA · Summer Tech Camp · следующий набор',
    'Taipei · TAS campus,800Zhongshan North Road Sec.6,Shilin',typa,
    age='Последний2026набор: Grades1–8 на Fall2026, отдельные1–2/3–4/5–8треки;2027правила ещё уточнить',
    format='Дневные STEMсмены;2026:Mon–Fri09:00–16:00,новые дни не объявлены',
    participation='day_camp',admission_kind='program',scope='local',level='D — робототехническое обучение',themes=['robotics','coding','technology'],
    language='EN кандидат; преподавание именно TechCamp прямо не подтверждено',languages=[],
    gear='Grades1–2механизмы/цепи;3–4роботы/micro:bit;5–8robotics; новое оснащение уточнить',
    cost='Исторический2026тарифNT$25000/неделя с обедом;2027тариф не объявлен',
    historical_editions=[dict(start='2026-06-08',end='2026-07-31',status='Прошедшие2026смены; не календарь2027')],
    entry='TYPAmembership,MasterRegistrationForm,копия иностранного паспорта. Expatriatecommunity всех национальностей приветствуется; туристический/короткий приём и возраст по классу подтвердить.',
    reward='Учебные проекты; не международная медаль',
    proof='Прочитаны конкретнаяSummerTechpage,brochure2026 и registrationpolicy:группы по классу,прошедшие смены,foreignpassport/membership. Будущих дней2027 и explicitENinstruction не найдено.',
    note='Не дублирует TAS SummerAcademyL021: TYPA — отдельныйmembershipprovider на том же кампусе. Английская страница и международная школа не доказывают ENконкретной смены. Membership semesterfeeNT$1600 не перенесён автоматически на summer. Класс каждого ребёнка неизвестен; age9 не равенGrade4.')
ref(e,typareg,'TYPA · membership / passport rules','Прочитано: foreignpassportcopy+MasterRegistrationForm+membership,семестровая регистрация отдельно; touristcampentry неизвестен.')
irobo='https://www.irobo.com.tw/summer-camp'
add('L145','Лагеря','iROBO 光點創意 · AI / LEGO holiday camps · следующий набор',
    'NewTaipei · Banqiao / Taichung · Zhongke; конкретный кампус выбрать',irobo,
    age='2026:младшие треки для risingGrades1–3,продвинутые3–6/older; следующий набор по классу уточнить',
    format='Дневные2/3-дневные STEMсмены;2026страница не подтверждает будущие2027даты',participation='day_camp',admission_kind='program',
    scope='local',level='D — робототехническое / AIобучение',themes=['robotics','ai','coding','technology'],
    language='EN/ESпреподавание не подтверждено; язык текста中文 не является обязательным языком занятия',languages=[],
    gear='Провайдер: многие курсы дают ноутбук иLEGO,некоторые требуют свойtablet/phone; своя coursepageрешает',
    entry='Выбрать具体будущую смену,age/grade,ENподдержку иforeignchildentry. Для risingGrade1без опыта провайдер рекомендует механические основы.',
    reward='Учебные проекты; не конкурсная победа',
    proof='Прочитан текущийSummerCampprimaryHTML:все2026смены очные,Banqiao/Zhongke,младшиеgrades1–3,AI/programming/LEGO иentryFAQ;2027не датировано.',
    note='Тайпейскиймаркетингназвания не меняетBanqiaoнаTaipeiCity:городNewTaipei. Ни дни2026,ни китайский текст,нигенеративный перевод сайта не доказывают новуюEN/ESсмену2027. Не включено вдатированныйICS.')
regular='https://www.typa.org.tw/course/activities/technology/'
e=add('L146','Лагеря','TYPA · регулярная подготовка LEGO / Young Inventors / VEXIQ',
    'Taipei · TAS campus,800Zhongshan North Road Sec.6',regular,
    age='ESM:Kindergarten;SPMBasic:Grades1–3;YoungInventors:L1Gr1–2/L2Gr2–4/L3Gr3–5;VEXIQ:Gr4–8+instructorconsent',
    format='Регулярные семестровые after-schoolклассы; не каникулярный лагерь',participation='regular',admission_kind='program',scope='local',
    gear='ESMмеханизмы / SPMLEGO;YoungInventorsL3micro:bit/CAD/3D;VEXIQсвойноутбукmin1024×768',
    language='ENкандидат; teachinglanguage конкретного уровня уточнить',languages=[],
    cost='По текущимcoursepages/semesterclass:ESM13000,SPMBasic14000,YoungInventors15200,VEXIQ16400NT$. Membershipотдельно;summerтарифы другие.',
    entry='Определить текущий класс обоих детей. Membership+foreignpassport; иностранный туристический/краткий доступ уточнить. ДляVEXIQconsentпреподавателя и ноутбук.',
    reward='Подготовка и проекты; регистрация в класс не регистрирует команду наVEXWorlds',
    proof='Прочитаны TYPAtechnology и отдельныеESM/SPMBasic/YoungInventors/VEXIQcoursepages:строгиеclassbands,тарифы,consent,ноутбук иweeklyschedule.',
    note='Оскару2020 может подойтиESMеслиKindergarten либоSPMеслиGrade1; возраст6 сам не определяеткласс. Матвей2017 не подтверждёнкакGrade4, поэтомуVEXIQне помечен доступным. YoungInventorsmicro:bitесть толькоL3;не переносить егонаK/Grade1. Сеткусеместра не превратитьв14-недельныйканикулярныйлагерь.')
for url,label in [
    ('https://www.typa.org.tw/course/activities/technology/lego-esm-early-simple-machines/','TYPA ESM · Kindergarten'),
    ('https://www.typa.org.tw/course/activities/technology/lego-spm-basic-simple-powered-machines/','TYPA SPM Basic · Grades1–3'),
    ('https://www.typa.org.tw/course/activities/technology/young-inventors/','TYPA Young Inventors · levels1–3'),
    ('https://www.typa.org.tw/course/activities/technology/lego-robot-challenge/','TYPA VEXIQ · Grades4–8 / instructorconsent'),
    (typareg,'TYPA membership / foreign passport')]:
    ref(e,url,label,'Прочитан соответствующийcourse/registrationpage;language instruction остаётся неизвестным.')

# User birth year resolves a previously conditional local option elsewhere.
update('L139',mat='Нет — 2017 год рождения: в декабре2026 максимум9, минимум курса10',
    action='С текущими годами рождения дети не подходят Makers10–12 в декабре2026; искать младший местный course.',
    note=byid['L139']['note']+' Пользователь сообщил2017/2020: возраст10 в декабре2026 для Матвея невозможен; прежняя условность снята.')

profiles={p['id']:p for p in d['league_guide']['profiles']}
profiles['juniorbotball']['event_ids'].append('C778')
profiles['juniorbotball']['nuances'].append('TaiwanDec13,2026:младшиегруппыесть,но точныйclass/kit/EN/foreignentry не подтверждены. Certificateнеравенмировойпобеде;GCER2027локальноеобещаниенесверено.')
profiles['juniorbotball']['sources'].append(dict(title='Taiwan SPARK local event',url=jbc,checked=DAY))
profiles['marc'].update(event_ids=['C035','C779'],summary='LOM и TM имеют разные birth-year gates и не совмещаются одним ребёнком.',
    categories=[dict(name=e['title'],age=e['age'],team=e['format'],hardware=e['gear'],entry=e['entry'],age_rule='Годы рождения вERA v4,не текущий возраст',event_id=e['id']) for e in [byid['C035'],byid['C779']]],
    nuances=['2017 подходитLOM/TM;2020 толькоLOM,при школе иforeignpermission.','Один ребёнок выбираетодинMARC;FIRSTможносочетать.','Квотаinternationalнепроверенадляforeignfamily;минимум6команддляLOM.'],
    sources=[dict(title='ERA v4 primaryregulation',url=first_pdf,checked=DAY)],evidence='ВесьERA v4 прочитан;годырождениясемьисообщеныпользователем.')
profiles['tirt'].update(event_ids=['C036']+tirt_new,
    summary='Открытые international школьные дисциплины Taoyuan:sumo/autonomouscar/TURBOT/logistics/soccer.',
    age_summary='Разные школьные уровни; TURBOTElementary7–12. Иностранный вход проверяется отдельно в каждой дисциплине.',
    hardware='Sumoмодульныйавтономный;OpenCarлиния;TURBOTспециальныйkit;Shippingсвои3типаоборудования;SoccerTEMI.',
    categories=[dict(name=byid[i]['title'],age=byid[i]['age'],team=byid[i]['format'],hardware=byid[i]['gear'],entry=byid[i]['entry'],age_rule='Школа/возраст иeditionrules',event_id=i) for i in ['C036']+tirt_new],
    requirements=['СправкаобычнойшколывсвоейстранеприinternationalentrySumo/OpenCar.','Актуальнаяtechnicalредакцияиразрешённыйkitсвоейсоревновательнойгруппы.'],
    nuances=[tirt_conflict,'TURBOT7–12:Оскар2020неподходитNov2026.','Праваparent/coach иvisitor различаются; сумоallowforeignнеавтоматическиforallTIRT.'],
    sources=[dict(title='TIRT specific event pages / rules',url=byid['C036']['source'],checked=DAY)],
    evidence='Страницы5дисциплин+ENSumo/OpenCar/Shipping иTURBOTV07прочитаны;разныеgatesсохранены.')
profiles['wro']['event_ids'].append('C788')
profiles['wro']['nuances'].append('Taiwan:foreignschoolsвместнойсистеме могут участвовать,но туристическаякомандаизCostaRicaнеполучаетавтоматическогоnationalвхода. National2026прошёл;2027днинеизвестны.')
profile=dict(id='grg',name='Global Robotics Games · GRG',group='international',
    age_summary='ЛокальноTaiwan:MR1 7–9/MR2 10–12/MR3 13–16;AIMSagebandsпротиворечивы;Openпоschoollevel',
    age_tags=['9','10-12','teen','unknown'],summary='АвтономныеLEGOмиссии,AIvisionипроектнаяробототехника;internationalфиналSingapore.',
    categories=[dict(name=byid[i]['title'],age=byid[i]['age'],team=byid[i]['format'],hardware=byid[i]['gear'],entry=byid[i]['entry'],age_rule='Localoverviewнеустанавливаетденьотсечения;сверитьseasonmanual',event_id=i) for i in grg_ids],
    event_ids=grg_ids,legacy_ids=[],route='Локальныйорганизатор/обучающийцентр→местныйэтап→рекомендация/приоритетSingapore;квотынеподтвержденыдляforeignсемьи.',
    hardware='MR1:SPIKEEssential/WeDo2;MR2/3:SPIKEPrime/EV3;AIMSvision;Opencustomproject',
    language='ENtaskrulesесть;Taiwanсудейство/обучениеENнеподтверждено',
    importance='Международнаядетскаяпрограмма;неприравненакWRO/FIRST/VEXкрупнейшимсетям.',
    strengths='Автономность,сенсоры,AIvision,проектнаязащита',
    requirements=['Выбратьточнуюкатегориюимануал;неприменятьобщийage7–16ккаждойдисциплине.','ИностранныйTaiwanвход,coach,командаитранспортгруппынуждаютсявподтверждении.'],
    nuances=['В2027Матвею10,Оскару7:однаMR1командаможетнеподходитьпоотсечению.','AIMSвнутреннийконфликтвозрастаостаётсяоткрыт.','ПапкасTaiwanвназваниинеозначаетTaiwanместомSingaporeфинала.'],
    cost='Тарифлокальногоэтапа/дальнейшейгрупповойпоездкинеподтверждён',award='Наградавыбранногоэтапапопротоколу;приглашениенеравномедали',
    sources=[dict(title='GRG international organizer',url='https://www.globalroboticsgames.com/',checked=DAY),dict(title='SPARK Taiwan local organizer',url=grg,checked=DAY)],
    evidence='Глобальнаяилокальнаяпервичныестраницыпрочитаны;неизвестныеlocalдаты/AIMSgatesявноотмечены.')
assert 'grg' not in profiles
d['league_guide']['profiles'].append(profile)
d['league_guide'].update(version=15,checked=DAY,methodology='62 профиля семейств,лиг и программ;46прежнихмаршрутовсохранены. Частичныймировойохват. Taiwanauditразделяетlocaladmission,национальнуюквоту,сезонныйвозрастиязык.')

# These local pathways have their own constraints; explain them in plain Russian.
profile.update(
    age_summary='На Тайване: MR1 7–9, MR2 10–12, MR3 13–16; AIMS имеет конфликт возрастных рамок; Open определяется школьным уровнем.',
    summary='Автономные LEGO-миссии, компьютерное зрение и проектная робототехника; международный финал в Сингапуре.',
    route='Местный организатор / учебный центр → локальный этап → рекомендация или приоритетное приглашение в Сингапур. Право иностранной семьи идти через Taiwan не подтверждено.',
    hardware='MR1: SPIKE Essential / WeDo 2.0. MR2 / MR3: SPIKE Prime / EV3. AIMS: компьютерное зрение; Open: собственный проект.',
    language='Английские тексты задач опубликованы; язык тайваньского судейства и занятий требует подтверждения.',
    importance='Международная детская программа; её локальный этап не приравнен к мировым финалам WRO / FIRST / VEX.',
    strengths='Автономность, сенсоры, компьютерное зрение и защита проекта',
    requirements=['Выбрать категорию и сезонный регламент; общий диапазон 7–16 не является допуском во все дисциплины.', 'Подтвердить иностранное участие, состав, наставника и условия групповой поездки.'],
    nuances=['В 2027 Матвею исполняется 10, Оскару 7: общая команда MR1 может не подходить по отсечению.', 'Противоречие возрастных рамок AIMS не разрешено.', 'Международный финал в Сингапуре не датирует местный этап на Тайване.'],
    cost='Местный тариф и стоимость дальнейшей групповой поездки не подтверждены',
    award='Награда по протоколу конкретного этапа; приглашение не является медалью',
    evidence='Прочитаны первичные глобальная и локальная страницы; неизвестные местные даты и конфликт AIMS сохранены.')
profiles['tirt'].update(
    summary='Школьные дисциплины Taoyuan: сумо, автономная машинка, TURBOT, логистика и роботизированный футбол.',
    age_summary='Разные школьные уровни. TURBOT Elementary: 7–12 лет; иностранный вход проверяется отдельно для каждой дисциплины.',
    hardware='Сумо: модульный автономный робот; Open Car: движение по линии; TURBOT: специальный набор; Shipping: три типа оборудования; Soccer: TEMI.',
    requirements=['Для международных Sumo / Open Car — подтверждение обучения в своей стране.', 'Проверить последнюю техническую редакцию и разрешённый набор своей группы.'],
    nuances=[tirt_conflict, 'Оскар 2020 года рождения не достигает 7 лет в ноябре 2026 и не подходит TURBOT.', 'Допуск иностранцев в сумо не переносится автоматически на все TIRT. Родитель, наставник и посетитель имеют разные права.'],
    evidence='Прочитаны пять страниц дисциплин, английские правила Sumo / Open Car / Shipping и TURBOT V07; технические и возрастные различия сохранены.')
profiles['marc'].update(
    summary='LOM и TM имеют разные годы рождения и не совмещаются одним ребёнком.',
    nuances=['Матвей 2017 подходит по году рождения LOM / TM; Оскар 2020 только LOM. Школьный статус и иностранный вход уточнить.', 'Один ребёнок выбирает одну MARC-дисциплину; сочетание с FIRST допускается.', 'Иностранная мировая квота не установлена. Для LOM нужно минимум шесть команд в категории.'],
    evidence='Прочитан полный ERA v4; годы рождения семьи сообщены пользователем.')
profiles['juniorbotball']['nuances'][-1]='Taiwan, 13 декабря 2026: младшие уровни опубликованы, но классы, набор, английский и иностранный приём ещё не подтверждены. Сертификат не является мировой победой; локальное обещание GCER 2027 не сверено с KIPR.'
profiles['wro']['nuances'][-1]='Тайвань: иностранные школы местной системы допускаются. Туристическая команда из Costa Rica не получает автоматического национального входа. National 2026 прошёл; дни 2027 неизвестны.'
d['league_guide']['methodology']='62 профиля семейств, лиг и программ; все 46 прежних маршрутов сохранены. Мировой охват частичный. Аудит Тайваня разделяет местный допуск, национальную квоту, сезонный возраст и язык.'

focus=dict(country='Тайвань',iso='TWN',checked=DAY,status='partial',
    family='Матвей2017/Оскар2020:в2027исполняется10/7. Точныеbirthday,текущийклассивозможностьполногоENднянесообщены.',
    conclusion='Найдены2будущиезимниеSTEMсменыс явныманглийским. У младшейсемьи нетподтверждённого общегоforeigncompetitionдопуска. Тайваньскийкалендарьостаётсячастичным.',
    routes=[
        dict(name='Зима2027 · лагерь и FIRST / MARC',
            detail='TheGrove25–29JanZhubei→возможныйпереездKaohsiungнаExplore30Jan/MARCLOM1Feb. УGroveнеопубликованвозраст;ERAнужноразрешениеиностраннойкоманде. ДляLOM оба birthyearподходят;TMОскарунеподходит. ДедлайнERA22Oct09:59CostaRica.',ids=['L143','C033','C034','C035','C779']),
        dict(name='Матвей · полный английский научно-инженерный лагерь',
            detail='Expedition27Taipei21Jan–3Feb,10будней. Рекомендованныйвозраст8–12подходит2017;Оскар2020ниже8. Полныйпакет пересекаетсяMARC1Febвдругомгороде;необещатьоба. Языковаяготовностьиforeignintakeуточняются.',ids=['L142']),
        dict(name='Ближайшие конкурсы2026 · Taoyuan / Taichung',
            detail='TIRT7–8Nov: Sumо/OpenCar имеют internationalschoolroute,но deadlinesразошлись. TURBOT7+Оскарумладше. JuniorBotball13Dec:младшиеуровниесть,ноage/kit/foreign/ENещёнеустановлены.',ids=['C036','C780','C781','C782','C783','C778']),
        dict(name='Семейные выставки · отдельно от профессиональных',
            detail='MakerFaire24–25Oct2026POPOP:семейныйвходподтверждён,freeunder6ORheight<115cm. Innotech14–16Oct2027:семейноеправило2026хорошее,2027подтвердить. SmartCity16–19Mar2027:Nangang2,childpolicyнеизвестна. TAIREX/TAIROS/Touchвозрастныегейтысохраняются.',ids=['E027','E129','E024','E020','E021','E022','E023','E117']),
        dict(name='Подготовка и дальнейшие сезоны',
            detail='TYPA/TASпроверятьпоклассу,membershipиforeignpassport;camp2027неанонсирован. iROBOмладшиеклассыесть,EN/ESнеподтверждён. GRGразделяет7–9/10–12,WROTaiwanнациональныйпуть требуетместнойшкольнойсвязи. На2027неподставленыдни2026.',ids=['L144','L145','L146','L021','C784','C785','C786','C787','C788','C086'])],
    open_questions=['Возраст иforeignintakeTheGrove;выбраннаягруппаENбезобязательногокитайского.','ИностраннаякомандаERA:регистрация,школа/класс,ENзащита,правонаквоту.','TIRTdeadline иlatestCN/ENtechnicalrules,schooldocumentэквивалент.','TYPA2027/ TAS2027смены;actualteachingEN,туристическийmembershipдоступ.','JBCfulllocalbrochure,GRG2027даты/agecutoff,AIMSконфликт.','KaohsiungSmartCity2027дни,FRCfamilywatchentry,AIEXPO2027анонс,COMPUTEX2027childpolicy.'],
    language_result='ПодтверждёнENвдвухконкретныхwinter2027программах;ESTaiwanлагерьвэтомпроходененайден. Это результатпоиска,неутверждениеоботсутствиивсехESпрограмм.',
    rejected_geographies=[dict(name='ENJOYAI Taiwanprovider2026',actual_country='Вьетнам',reason='СобытиеHanoi22.08.2026,неTaiwan;прошедшийoutboundtour.'),dict(name='BorneoIRT Taiwanprovider',actual_country='Малайзия',reason='Miri6–9May2026,неTaiwan;прошедшийтур.'),dict(name='NTHUIYRC2026',actual_country='США',reason='PhoenixJuly2026,неTaiwanлокальнаядата.')])
# Keep the family-facing country brief readable, with route assumptions explicit.
focus.update(
    family='Матвей — 2017, Оскар — 2020 год рождения. В 2027 году им исполняется 10 и 7 лет. Точные дни рождения, текущие классы и готовность к целому дню на английском пока неизвестны.',
    conclusion='Найдены две будущие зимние STEM-программы с явным английским языком. Общий допуск иностранной команды для обоих детей пока не подтверждён. Календарь Тайваня остаётся частичным.',
    language_result='Английский подтверждён в двух конкретных зимних программах 2027 года. Испанский STEM-лагерь на Тайване в этом проходе не найден; это не доказывает отсутствие всех таких программ.',
    open_questions=[
        'The Grove: возраст обоих детей, иностранный приём и поддержка без обязательного китайского.',
        'ERA: иностранная команда, школа / класс, английская защита и право международной квоты.',
        'TIRT: действующий дедлайн, последние CN / EN регламенты и эквивалент школьной справки.',
        'TYPA / TAS: реальные смены 2027, английское преподавание и доступ туристической семьи.',
        'Junior Botball: полный локальный регламент; GRG: даты, возрастное отсечение и конфликт AIMS.',
        'Выставки: Kaohsiung Smart City 2027, AI EXPO 2027, детские правила COMPUTEX / Innotech 2027 и семейный вход на FRC.'
    ],
    rejected_geographies=[
        dict(name='ENJOY AI · сайт тайваньского провайдера',actual_country='Вьетнам',reason='Hanoi, 22 августа 2026: зарубежный тур, прошедшее событие.'),
        dict(name='Borneo IRT · сайт тайваньского провайдера',actual_country='Малайзия',reason='Miri, 6–9 мая 2026: зарубежный тур, прошедшее событие.'),
        dict(name='NTHU IYRC 2026',actual_country='США',reason='Phoenix, июль 2026: не местное событие на Тайване.')])
for route, name, detail in zip(focus['routes'], [
    'Зима 2027 · лагерь и FIRST / MARC',
    'Матвей · полный день на английском',
    'Ближайшие конкурсы 2026 · Taoyuan / Taichung',
    'Семейные и профессиональные выставки',
    'Подготовка и дальнейшие сезоны'], [
    'The Grove: 25–29 января в Чжубэе. Затем можно рассмотреть переезд в Гаосюн на FLL Explore 30 января или MARC LOM 1 февраля. Возраст в лагере и иностранный конкурсный вход требуют подтверждения. Для LOM оба года рождения подходят; TM исключает Оскара. ERA: заявка и оплата до 22 октября, 09:59 по Коста-Рике.',
    'Expedition27: Тайбэй, 21 января — 3 февраля, десять будней. Рекомендуемые 8–12 лет подходят Матвею; Оскар младше диапазона. Полный пакет пересекается с MARC 1 февраля в другом городе. Возможность провести весь день на английском и иностранный приём нужно подтвердить.',
    'TIRT: 7–8 ноября. Для Sumo и Open Car описан вход иностранных школьных команд, но дедлайны расходятся. TURBOT начинается с 7 лет: Оскар не подходит в ноябре 2026. Junior Botball: 13 декабря; младшие уровни есть, однако точный возраст, набор, язык и зарубежный вход ещё не установлены.',
    'Maker Faire: 24–25 октября 2026, POPOP Taipei. Семейный вход подтверждён; бесплатность — младше 6 лет или рост ниже 115 см. Innotech: 14–16 октября 2027, детские правила следующего выпуска уточнить. Smart City: 16–19 марта 2027, Nangang Hall 2, детский пропуск неизвестен. Возрастные запреты TAIREX, TAIROS и Touch Taiwan сохранены.',
    'TYPA / TAS проверяются по классу, членству и иностранному паспорту; летние смены 2027 не подтверждены. У iROBO есть младшие треки, язык EN / ES неизвестен. GRG разделяет 7–9 и 10–12; путь WRO Taiwan предполагает местный школьный отбор. Даты 2026 не стали новым календарём 2027.'
]): route.update(name=name,detail=detail)

byid['L142'].update(
    age='Рекомендуемые 8–12 лет; это рекомендация, а не опубликованный жёсткий минимум. Десять учебных будней, выходные свободны.',
    format='Дневной лагерь с полевыми поездками: 10 будней, 09:00–17:30; только полный пакет, без проживания',
    cost='NT$24 000 early bird / NT$27 000 standard за 10 дней. Включены материалы, обед, перекус, стандартные входы и страхование; EasyCard примерно NT$200 в день дополнительно.',
    entry='Согласовать иностранный приём, возраст, готовность к EN и свободное место. Запрос информации не резервирует место или скидку. Минимум 8, максимум 12 участников.',
    deadline_note='Ранний тариф зависит от полученной оплаты до 5 декабря; час не опубликован. Это не общий срок регистрации. К 5 января 2027 нужно минимум 8 детей, иначе отмена и возврат.',
    note='Это широкая научно-инженерная программа, роботы и ИИ не гарантированы. Субботы и воскресенья свободны. Финальный горный маршрут зависит от погоды. Лагерь занимает 1 февраля, когда MARC проходит в Гаосюне: совместить весь пакет и этот турнир нельзя. Наличие места и иностранный приём не подтверждены.')
byid['L143'].update(
    title='The Grove · Ready to Soar · English STEM winter 2027',
    age='Точный возраст и классы не указаны в странице или форме; группа из 8 детей',
    format='Пять утренних дней, 09:00–12:00; инженерные проекты о полёте, без проживания',
    cost='До 16 октября 2026: NT$7 900 + 900 за материалы = 8 800. С 17 октября: NT$8 800 + 900 = 9 700. Депозит NT$2 000; включение депозита в общую сумму уточнить.',
    entry='Согласовать возраст обоих детей, уровень английского и иностранные документы. Форма → подтверждение в LINE → депозит NT$2 000 для резервирования. Свободные места неизвестны.',
    gear='Материалы: отдельные NT$900 в общей стоимости; ноутбук не заявлен',
    language='Английский основной; местный помощник использует китайский',
    language_certainty='В форме конкретной смены: английский основной, китайский вспомогательный. Поддержка ребёнка без китайского требует подтверждения.',
    reward='Пять STEM-проектов и показ внутри группы; не международная конкурсная награда',
    note='Программа инженерии полёта, робототехника и ИИ не гарантированы. Числовой возраст не опубликован. После 29 января можно рассмотреть отдельный переезд Чжубэй → Гаосюн на FIRST / MARC, если иностранный допуск подтвердят. Форма и платежи семьёй не отправлялись; пропуски не компенсируются по правилам провайдера.')
byid['L144'].update(
    age='Последний набор 2026: Grades 1–8 на осень 2026, отдельные треки 1–2 / 3–4 / 5–8. Условия 2027 ещё не объявлены.',
    format='Дневные STEM-смены; в 2026: понедельник — пятница, 09:00–16:00. Новые дни неизвестны.',
    cost='Исторический тариф 2026: NT$25 000 за неделю с обедом. Стоимость 2027 не объявлена.',
    gear='Grades 1–2: механизмы / цепи; 3–4: роботы / micro:bit; 5–8: робототехника. Оснащение нового набора уточнить.',
    entry='Членство TYPA, Master Registration Form и копия иностранного паспорта. Иностранное сообщество всех национальностей приветствуется; приём туристов на короткую смену и возраст по классу уточнить.',
    note='TYPA и TAS Summer Academy — разные программы на одном кампусе. Английский сайт не доказывает преподавание выбранной смены. Семестровый регистрационный взнос NT$1 600 не перенесён автоматически на летний лагерь. Классы детей неизвестны; возраст 9 не равен Grade 4. Смены июня — июля 2026 прошли; в ICS не добавлены.')
byid['L145'].update(
    title='iROBO 光點創意 · AI / LEGO holiday camps · следующий набор',
    age='В 2026: младшие треки для rising Grades 1–3, продвинутые 3–6 и старше. Классы следующего набора уточнить.',
    format='Дневные смены по 2 или 3 дня; страница 2026 не подтверждает будущие дни 2027',
    entry='Выбрать конкретную будущую смену, класс, поддержку EN и приём иностранного ребёнка. Для rising Grade 1 без опыта провайдер рекомендует механические основы.',
    gear='Многие курсы предоставляют ноутбук и LEGO; отдельным нужен свой планшет / телефон. Проверить страницу выбранного курса.',
    language='Преподавание на EN / ES не подтверждено; китайский текст сайта не устанавливает язык всех занятий',
    note='Banqiao находится в New Taipei, несмотря на маркетинговое название Taipei camp. Даты 2026 не перенесены в 2027. Язык сайта и автоматический перевод не доказывают EN / ES занятия. Без точных будущих дней нет события ICS.')
byid['L146'].update(
    title='TYPA · регулярная подготовка LEGO / Young Inventors / VEX IQ',
    age='ESM: Kindergarten; SPM Basic: Grades 1–3; Young Inventors: L1 Grades 1–2 / L2 2–4 / L3 3–5; VEX IQ: Grades 4–8 и согласие преподавателя',
    format='Регулярные семестровые занятия после школы; каникулярные смены проверяются отдельно',
    gear='ESM / SPM: механизмы LEGO. Young Inventors L3: micro:bit, CAD, 3D. VEX IQ: свой ноутбук, экран минимум 1024 × 768.',
    cost='За семестр и класс: ESM NT$13 000, SPM Basic 14 000, Young Inventors 15 200, VEX IQ 16 400. Членство отдельно; летние тарифы другие.',
    entry='Подтвердить класс каждого ребёнка. Членство и копия иностранного паспорта; туристический / краткий приём уточнить. Для VEX IQ нужно согласие преподавателя и ноутбук.',
    note='Оскару может подойти ESM при Kindergarten или SPM при Grade 1; год рождения не определяет класс. Класс Матвея неизвестен, поэтому VEX IQ не помечен доступным. micro:bit есть в Young Inventors L3; он не перенесён на Kindergarten. Семестровая сетка не превращена в каникулярный лагерь.')

# Add spacing to remaining mixed-script technical prose without touching URLs,
# IDs, dates, enumerations or language tags. Human edits above control meaning.
import re
def readable(value):
    value=re.sub(r'([А-Яа-яЁё])([A-Za-z0-9])',r'\1 \2',value)
    value=re.sub(r'([A-Za-z0-9])([А-Яа-яЁё])',r'\1 \2',value)
    value=re.sub(r'([,;:])(?=[А-Яа-яЁёA-Za-z])',r'\1 ',value)
    return value
prose_keys=['title','city','age','mat','osc','format','entry','gear','language','language_certainty','cost','level','importance_reason','reward','priority','action','proof','note','period','deadline_label','deadline_note','registration_status']
for id in new+updated:
    for key in prose_keys:
        if isinstance(byid[id].get(key),str): byid[id][key]=readable(byid[id][key])

for id in new:
    if byid[id]['block']=='Лагеря': byid[id]['evidence_level']='program'
for id in ['L142','L143']: byid[id]['date_scope']='session_days'

a=d['completeness_audit']
a.update(version=15,checked=DAY,baseline=baseline,new_ids=new,new_profiles=['grg'],updated_ids=updated,
    promoted_exhibition_ids=[],focused_country=focus,
    scope='УглублённыйTaiwanпроход:primaryPDFs,ENwintercamps2027,отдельныеMARC/TIRT/GRGкатегории,WROnationalgates,семейныйMakerFaire иInnotech2027. Полныймировой/Taiwanохватнеобъявлен.')
a['caveats'] += ['Годырождениясообщеныпользователем:2017/2020. Классы,дниbirthday иENготовностьнеустановлены.',
    'v15:Taiwan2будущиеwintercampEN,ноTheGroveвозрастнеуказан,Expedition27recommended8–12;никакогоESсдвигаизавтоперевода.',
    'TASиTYPAразныепрограммы;регулярныеклассыотделеныотканикул;2026летниесменынестали2027календарём.',
    'MARCLOMиTMразделены:2020годтолькоLOMпоbirthgate;одинребёноквыбираетоднуMARCдисциплину.',
    'TaiwanprovidersнаENJOY/Borneo/NTHUстраницахведуткмероприятиямVietnam/Malaysia/USA,неTaiwan. Датыинатсборные/отборыразличаются.']
a['source_issues'] += [dict(name='TIRT2026 · conflicting registration versions',status=tirt_conflict,official_alternative=byid['C036']['source']),
    dict(name='GRG Taiwan · AIMS age bands',status=byid['C786']['age'],official_alternative=grg),
    dict(name='Taiwan Innotech · mixed editions',status='Homepage14–16Oct2027,но admissionchild≤12сродителемот2026. Venue/childpolicy2027нельзяавтоматическиперенести.',official_alternative=inventgate)]
a['known_backlog'].append(dict(kind='Тайвань',name='Taiwan:оставшиесяlocalrulesиforeignentry',reason='; '.join(focus['open_questions']),url=first_url))
a['scope']='Углублённый аудит Тайваня: первичные регламенты, зимние EN-лагеря 2027, отдельные MARC / TIRT / GRG категории, национальный путь WRO, семейный Maker Faire и Innotech 2027. Полный охват Тайваня и мира пока не подтверждён.'
a['caveats'][-5:]=['Годы рождения сообщены пользователем: 2017 / 2020. Точные дни рождения, классы и готовность к целому дню на английском неизвестны.', 'В v15 найдены две будущие зимние программы на EN. The Grove не публикует возраст; Expedition27 рекомендует 8–12. Перевод сайта не является испанским преподаванием.', 'TAS и TYPA — разные программы. Регулярные занятия отделены от каникул; летние смены 2026 не перенесены в 2027.', 'MARC LOM и TM разделены: Оскар 2020 подходит по году рождения только LOM. Один ребёнок выбирает одну MARC-дисциплину.', 'Тайваньские провайдеры ENJOY / Borneo / NTHU описывают зарубежные события во Вьетнаме / Малайзии / США. Место провайдера не определяет место турнира.']
a['known_backlog'][-1]['name']='Тайвань: оставшиеся местные правила и иностранный вход'
a['source_issues'][-1]['status']='Главная объявила 14–16 октября 2027, но семейное правило для детей до 12 включительно со взрослым относится к 2026. Площадку и детский допуск 2027 нужно подтвердить.'
d['source_count']=len(d['sources']);d['asof']=DAY
d['expansion_log'].append(dict(version=15,date=DAY,scope='Taiwan deep primary-source eligibility / camps / exhibitions',added_ids=new,updated_ids=updated,
    notes=['Все1046прошлыезаписи/61профиль/46маршрутовсохранены.','C035сталLOM;TMотдельно,нетдвойногосчётаcombinedMARC.','Пользовательскиеbirthyearснялиложныйусловный10+допускCENFOTECDec2026.','Всеunknown2027дниосталисьпустыми;новыеENтегитолькоexplicitinstruction.']))
(ROOT/'data/taiwan-audit-v15.json').write_text(json.dumps(dict(version=15,focus=focus,added_ids=new,updated_ids=updated,
    source_issues=a['source_issues'][-3:],sources=[s for s in d['sources'] if s.get('checked')==DAY and any(x in s['url'] for x in ['typa','tirt','era.org','steamsquad','thegrove','inventaipei','smartcity','irobo','robotics-games','junior-botball','globalroboticsgames'])],
    additional_rejected=[dict(name='TCS MapleTechQuest2026',reason='ENесть,ноGrades5–7и3–7Aug2026прошли;future2027необъявлен.',source='https://tcs.ntpc.edu.tw/student-life/tcs-2026-summer-camp/tcsmapletechquest'),dict(name='TIRT Humanoid Korfball',reason='C-3HighSchool/Collegeнедетскаякатегория;футболT-1имеетдругуюстраницу.',source=tirtbase+'db5f96f1-4b4d-43a3-a219-b295e07b3c00')]),ensure_ascii=False,indent=2))
planpath=ROOT/'data/research-plan.json';plan=json.loads(planpath.read_text())
plan.update(updated=DAY,status='active',completeness_audit='data/audit-v15.json')
plan['family_context']=dict(matvey_birth_year=2017,oscar_birth_year=2020,source='Прямойответпользователя01.10.2026',exact_birthdays=None,school_grades=None,full_day_english_readiness=None)
for row in plan['requirements']:
    if row['id']=='global_competitions': row['evidence']='v15:Taiwan11новыхcompetitionкатегорий/путей,GRGпрофиль,раздельныеMARCLOM/TM,5TIRTкатегорийсразнымиgates.WROnationalместнаяшкола;foreignfamilyquotaнеподтверждена.'
    if row['id']=='camps': row['evidence']='v15:Taiwan5новыхпрограмм,изних2точныезимние2027сменысexplicitEN,2будущиелетниекандидатыи1regularподготовка. ВозрастTheGroveнеопубликован;Expeditionrecommended8–12;ESненайден.'
    if row['id']=='exhibitions': row['evidence']='v15:Innotech2027добавлен;SmartCityTaipei16–19Mar2027обновлён;MakerFairePOPOP24–25Oct2026familygate/тарифывизуальнопроверены. Всёмировоепокрытиечастичное.'
    if row['id']=='eligibility':
        row['evidence']='v15:birthyear2017/2020изпрямогоответа. MARCTMисключает2020;TURBOTNov2026исключает2020;L13910+Dec2026исключает2017. Классы/точныеbirthdays/ENreadyещёнеизвестны. ERAforeigndopusk,TIRTdeadline,GRGAIMSageконфликтоткрыты.'
        row['remaining']='Точныедниbirthday,классы,ENfull-dayreadiness,nationalfederation/foreignpermissions иактуальныеmanuals'
plan['latest_validation']=dict(version='v15',status='pending',research_status='active')
plan['next_research'].insert(0,'Taiwan: '+ '; '.join(focus['open_questions']))
planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2))
PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2))
print(json.dumps(dict(added=len(new),total=len(d['events']),updated=updated,new_ids=new),ensure_ascii=False))
