"""Append evidence-backed gaps found in the September 30 completeness audit."""
import json, pathlib, re, collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'data/catalog.json').read_text())
assert len(d['events'])==977, 'Run once against v11; do not overwrite later research'
before_ids={e['id'] for e in d['events']}; new_ids=[]; new_profiles=[]
DAY='2026-09-30'
def source(url,title,evidence='Официальная страница прочитана; границы проверки указаны в карточке'):
    if not any(s['url']==url for s in d['sources']):
        d['sources'].append(dict(url=url,title=title,evidence=evidence,checked=DAY))
def event(id,title,country,region,city,url,age,entry,gear,start='',end='',mat='Условно — допуск уточнить',osc='Условно — допуск уточнить',**kw):
    assert id not in before_ids and id not in new_ids
    e=dict(id=id,block='Соревнования',title=title,country=country,region=region,city=city,start=start,end=end or start,
        period='' if start else 'Следующий выпуск / этап: даты не подтверждены',date_status='Подтверждено' if start else 'Даты не объявлены',deadline='',
        age=age,mat=mat,osc=osc,format='Команда; размер по регламенту категории',entry=entry,gear=gear,
        language='Язык конкретного этапа и EN/ES-судейство уточнить',languages=[],cost='Оборудование, регистрация и поездка рассчитываются отдельно',
        level='Международная сеть; масштаб конкретного этапа указан отдельно',reward='Протокол и награда конкретного этапа; участие не гарантирует призовое место',
        priority='P2 — подготовка / поездка после проверки допуска',action='Проверить категорию, класс, состав команды и иностранный вход; получить условия текущего сезона.',
        source=url,references=[],proof='Прочитан первичный источник; точные даты и неизвестные условия разделены.',checked=DAY,status='Идея',note='',
        themes=['robotics','technology'],scope='international',participation='team',admission_kind='unknown',evidence_level='event_page',
        registration_status='Заявка семьи не подана; наличие даты не означает открытый набор',language_certainty='Перевод сайта не подтверждает язык судейства или помощи детям.')
    e.update(kw);d['events'].append(e);new_ids.append(id);source(url,title);return e
def profile(id,name,group,age,tags,summary,categories,ids,urls,route,nuances=(),evidence=None):
    assert not any(p['id']==id for p in d['league_guide']['profiles'])
    p=dict(id=id,name=name,group=group,age_summary=age,age_tags=tags,summary=summary,categories=categories,event_ids=ids,legacy_ids=[],route=route,
        hardware=' / '.join(dict.fromkeys(c['hardware'] for c in categories)),language='Язык международных материалов и местного судейства проверяется отдельно.',
        importance='Редакционный ориентир по компетенции и доступности; общего официального мирового рейтинга лиг нет.',strengths=summary,
        requirements=['Проверить правила именно выбранной категории и сезона.','Указать самостоятельный вклад каждого ребёнка и пройти предусмотренный отбор.'],
        nuances=list(nuances),cost='Регистрация, техника, наставник и поездка зависят от этапа; бюджет семьи не рассчитан.',
        award='Официальный результат и награда выбранного этапа. Отбор, участие и победа учитываются отдельно.',
        sources=[dict(title=t,url=u,checked=DAY) for t,u in urls],evidence=evidence or 'Первичный источник прочитан 30.09.2026. Допуск семьи и национальное представительство не подтверждены.')
    d['league_guide']['profiles'].append(p);new_profiles.append(id)
    for t,u in urls: source(u,t,evidence or 'Официальный источник прочитан 30.09.2026')
def cat(name,age,team,hardware,entry,age_rule='Возраст / класс по правилам конкретного этапа',**kw):
    return dict(name=name,age=age,team=team,hardware=hardware,entry=entry,age_rule=age_rule,**kw)

fg='https://first.global/fgc/';fgr='https://first.global/contact/'
event('C762','FIRST Global Challenge 2026 · Igniting Innovation','Южная Корея','Азия','Incheon',fg,'14–18 лет; одна национальная сборная страны',
    'Национальный партнёр выбирает одну сборную; свободной семейной заявки в мировой финал нет.','Комплект сезона FIRST Global',
    '2026-10-07','2026-10-10',mat='Нет — от 14 лет',osc='Нет — от 14 лет',admission_kind='qualifier',evidence_level='rules',references=[dict(url=fgr,label='Национальный отбор и возраст')],
    language='EN / ES: материалы игры; язык национального отбора отдельно',languages=['EN','ES'],note='Ближайший выпуск уже через неделю; это старшая траектория, не соревнование для детей 6/9.')
profile('firstglobal','FIRST Global Challenge','advanced','14–18 лет; одна сборная страны',['teen'],'Робототехнический турнир национальных сборных с ежегодной задачей.',
    [cat('National Team','14–18','Национальная команда','Комплект FIRST Global','Отбор национальным партнёром')],['C762'],[('Сезон 2026',fg),('FAQ: национальный отбор',fgr)],
    'Школьная команда → национальный партнёр → выбор сборной → FIRST Global.',('FIRST Global и FIRST Championship имеют разные процедуры входа.','Паспорт или проживание сами по себе не дают места в сборной.'))

fira='https://firaworldcup.org/news/fira-roboworld-cup-and-summit-2026-call-for-paper/'
event('C763','FIRA RoboWorld Cup · следующий сезон Youth','Мир','Мир','Место следующего выпуска не подтверждено',fira,'В сезоне 2026: U14 / U19; отсечка 30 июня. Правило следующего сезона ещё проверить.',
    'Через национальную chapter; где chapter нет — обращение в FIRA HQ с квалификационными материалами.','По дисциплине: Mission Impossible, автономные машины, дроны или гуманоиды',
    evidence_level='rules',admission_kind='qualifier',note='Подтверждённый выпуск 2026 в Markham, Canada, 17–21 июля уже прошёл. Даты 2027 не перенесены. В документах квалификации встречаются разные требования к объёму TDP — уточнить категорию.',
    historical_editions=[dict(start='2026-07-17',end='2026-07-21',city='Markham, Canada',source=fira)])
profile('fira','FIRA RoboWorld Cup / Youth','international','U14 / U19; в 2026 возраст на 30 июня',['6','9','10-12','teen'],
    'Сеть состязаний по автономным роботам, Mission Impossible, машинам, дронам и гуманоидам.',
    [cat('Youth U14 / U19','Младше 14 / 19 в сезоне 2026','Youth: база 2, до 4; coach','По дисциплине','Chapter / квалификация HQ','В 2026 — 30 июня; универсальный минимум не найден')],['C763'],[('Правила и квалификация 2026',fira)],
    'Выбрать дисциплину → chapter либо HQ → квалификация → международный этап.',('Возраст 6/9 не исключён верхней границей U14, но это не подтверждение допуска.','Правила будущего сезона и требования TDP уточняются; родители не входят в рабочую зону Youth.'))

urc='https://www.urc21.org/en/overview.php';urcr='https://www.urc21.org/en/pdf/2026_overview_robot_python_en.pdf'
event('C764','Universal Robotics Challenge · следующий выпуск','Япония','Азия','Osaka / онлайн; следующий формат уточнить',urc,'Early ≤9; Regular 10–12; Advanced 13+; preschool–junior high по описанию 2026',
    'Связаться с локальным партнёром URC; онлайн-квалификация к очному финалу Real Robotics. Отдельные Idea / Virtual divisions.','Совместимая Artec-платформа; Python division отдельно',
    participation='individual_or_team',format='Команда от 1 до 5 в опубликованном Python Division 2026; остальные регламенты отдельно',admission_kind='qualifier',evidence_level='rules',
    note='Финал Real Robotics 19 сентября 2026 уже прошёл. Публикация результатов 30 октября — не новый день соревнования. Правила 2027 ещё не найдены.',references=[dict(url=urcr,label='Python Division 2026: команды 1–5')],
    historical_editions=[dict(start='2026-09-19',end='2026-09-19',city='Osaka',source=urc)])
profile('urc','Universal Robotics Challenge (URC)','international','Early ≤9 · Regular 10–12 · Advanced 13+',['6','9','10-12','teen'],'Artec: реальные роботы, идеи и виртуальное программирование.',
    [cat('Real Robotics','Early ≤9 / 10–12 / 13+','Размер зависит от division','Artec / допустимый набор','Онлайн-отбор → Osaka'),cat('Python Division 2026','По отдельному регламенту','1–5','Python / робот','Через локального партнёра')],['C764'],[('Возраст и divisions 2026',urc),('Python: состав команды',urcr)],
    'Партнёр URC → выбрать division → самостоятельный робот / видео → квалификация → финал.',('Для 6 и 9 лет есть младшая категория; иностранный вход и отсечку возраста подтвердить.','World Finals 2026 уже прошёл; следующий год не датирован автоматически.'))

wrc='https://www.worldrobotconference.com/contest/regulations/2632.html'
event('C765','World Robot Contest · WRCT / WRCC / WRCF','Китай','Азия','Этап и город по дисциплине',wrc,'Нет общего детского возраста: возрастные группы определяет дисциплина.',
    'Официальные notices и регламент дисциплины; процедуры Trials / Championships / Finals различаются.','По дисциплине',evidence_level='rules',
    note='Китайское общество электроники (CIE). World Robot Contest, World Robot Conference/Expo и WRO — разные сущности. Будущий этап с подтверждённой датой пока не выбран.')
profile('wrc','World Robot Contest (CIE)','international','Возраст и состав по каждой дисциплине',['unknown'],'Китайская сеть Trials, Championships и Finals по роботам и ИИ.',
    [cat('WRCT / WRCC / WRCF','По дисциплине','По дисциплине','По регламенту','Официальное notice и регистрация')],['C765'],[('Устав CIE',wrc)],
    'Выбрать дисциплину и возрастную группу → выяснить иностранный вход → этап по official notice.',('Не объединять с WRO и входом зрителя на World Robot Expo.','Общий устав не доказывает доступность каждой дисциплины детям 6/9.'))

iaio='https://iaio-official.org/';iaior='https://www.iaio-official.org/wp-content/uploads/2024/06/IAIO-regulations.pdf'
event('C766','IAIO 2027 · International Artificial Intelligence Olympiad','Vietnam','Азия','Город ещё не объявлен',iaio,'Не старше 20 на 1 июля; школа secondary или ниже, национальный отбор; не tertiary ≥half-time',
    'Национальная делегация 1–4 contestants, отбор по программированию и решению задач. Условия представительства из S2.5.','Программирование / computing science; среда сезона',
    '2027-02-25','2027-03-02',mat='Условно — национальный отбор и готовность, практическая подростковая траектория',osc='Условно — национальный отбор и готовность, практическая подростковая траектория',
    themes=['ai','coding','technology'],participation='individual_or_team',format='Национальная делегация 1–4; формат раундов будет уточнён',admission_kind='qualifier',evidence_level='rules',
    language='EN — официальный рабочий язык IAIO',languages=['EN'],references=[dict(url=iaior,label='IAIO Regulations: S2.3–2.5')],
    note='IAIO и IOAI — отдельные олимпиады. В регламенте не найден универсальный нижний возраст, но национальная процедура может ограничивать допуск.')
profile('iaio','IAIO · International Artificial Intelligence Olympiad','advanced','≤20 на 1 июля; школа secondary или ниже',['teen','unknown'],'Международная олимпиада по computing science / AI с национальным отбором.',
    [cat('National delegation','≤20; secondary или ниже','1–4 contestants','Программирование','Национальный отбор','S2.5: школьный статус, учебная нагрузка и 1 июля')],['C766'],[('Вьетнам 2027',iaio),('IAIO Regulations',iaior)],
    'Программирование и задачи → национальная процедура → делегация → IAIO.',('Это отдельная организация от IOAI.','Обучение за рубежом / гражданство регулируются S2.5; разрешение семьи ещё не получено.'))

sp='https://seaperch.org/programs/2027-challenge/';spr='https://robonation.gitbook.io/seaperch-challenge-resources/section-1-competition-overview/1.1-eligibility-and-qualifying'
spc='https://robonation.gitbook.io/seaperch-challenge-resources/section-1-competition-overview/1.5-competition-classes'
event('C767','International SeaPerch Challenge 2027','США','Северная Америка','College Park, Maryland · University of Maryland',sp,'Elementary / middle / high school; класс и региональные условия подтвердить.',
    'Квота зарегистрированного регионального соревнования или Wild Card 1 декабря 2026 – 1 февраля 2027. Финальная регистрация только по приглашению.','Подводный ROV SeaPerch; класс по конструкции и школьной ступени',
    '2027-06-05','2027-06-06',admission_kind='qualifier',evidence_level='rules',deadline='2027-02-01',deadline_label='Wild Card: закрытие подачи',
    deadline_note='Wild Card — конкурс на приглашение, не купленное место. Точное время отсечки уточнить.',cost='Wild Card application $10, невозвратный; финал / техника / поездка отдельно',
    language='EN: официальные правила; формат поддержки семьи уточнить',languages=['EN'],references=[dict(url=spr,label='Elementary eligibility и Wild Card'),dict(url=spc,label='Классы; заголовок 2026 требует проверки версии')],
    note='Сезонная страница 2027 и handbook расходятся в сроке публикации regional list: ноябрь / до 1 декабря. Страница классов содержит заголовок 2026, хотя описывает 2028; редакцию класса 2027 подтвердить.')
profile('seaperch','SeaPerch / RoboNation','international','Elementary, middle, high school; по классу',['6','9','10-12','teen'],'Подводный ROV, испытания в бассейне и техническая документация.',
    [cat('Stock / Open','По школьной ступени и конструкции','Команда; текущий handbook','SeaPerch ROV','Региональная квота / Wild Card','Elementary допускаются; условия регионов различаются')],['C767'],[('Сезон 2027',sp),('Eligibility / Wild Card',spr),('Competition classes',spc)],
    'Собрать ROV → бассейн и документация → региональный отбор либо Wild Card → финал.',('Начальная школа включена в eligibility; класс каждого ребёнка всё равно нужен.','Wild Card — шанс получить приглашение; страница классов требует подтверждения редакции сезона.'))

mate='https://materovcompetition.org/scout';mater='https://materovcompetition.org/ranger';matew='https://materovcompetition.org/world-championship'
event('C768','MATE ROV · SCOUT: локальный вход для начальной школы','Мир','Мир','Регионального координатора ещё выбрать',mate,'SCOUT: K–4 / 5–8 / 9–12. K–4 только с одобрением regional coordinator.',
    'Школа, homeschool, club или community team → подтверждение регионального координатора → SCOUT.','Подводный ROV и правила безопасности SCOUT',evidence_level='rules',admission_kind='qualifier',
    references=[dict(url=mater,label='RANGER: уже 5–12 классы')],note='SCOUT — начальный региональный уровень. Участие в нём не даёт автоматического прохода в мировой RANGER / EXPLORER.')
event('C769','MATE ROV World Championship 2027','США','Северная Америка','Federal Way, Washington · Weyerhaeuser King County Aquatic Center',matew,'Класс финала уточнить: RANGER — 5–12 классы; SCOUT K–4 не приравнен к мировому допуску.',
    'Квалификация и приглашение по классу; проверить руководство 2027.','ROV класса финала', '2027-06-24','2027-06-26',mat='Условно — только если класс / квалификация разрешают',osc='Нет — SCOUT не является входом в этот финал',
    references=[dict(url=mater,label='RANGER eligibility'),dict(url=mate,label='SCOUT eligibility')],admission_kind='qualifier',note='Объявлены даты финала, но ни один ребёнок семьи не квалифицирован. Младший SCOUT и мировой финал разделены.')
profile('mate','MATE ROV Competition','international','SCOUT K–4 условно; RANGER 5–12 классы',['6','9','10-12','teen','university'],'Инженерный подводный робот, безопасность, испытания и защита проекта.',
    [cat('SCOUT','K–4 / 5–8 / 9–12','Команда','ROV SCOUT','Региональный этап','K–4: одобрение координатора'),cat('RANGER','5–12 классы','Команда','ROV RANGER','Региональная квалификация','По школьному классу')],['C768','C769'],[('SCOUT: младший вход',mate),('RANGER',mater),('Финал 2027',matew)],
    'SCOUT → подтвердить класс и освоить ROV → RANGER / другой класс → предусмотренный отбор → мировой этап.',('SCOUT не означает мировой допуск.','Для детей 6/9 сначала подтвердить начальную школу у регионального координатора.'))

icys='https://icysconference.com/'
event('C770','ICYS 2027 · research competition','Czechia','Европа','Hradec Kralove',icys,'14–18 лет, secondary school',
    'Национальная делегация / отбор; исследовательский доклад по computer science или другому научному направлению.','Собственное исследование и доклад','2027-04-18','2027-04-24',
    mat='Нет — от 14 лет',osc='Нет — от 14 лет',participation='individual',format='Индивидуальное исследование в делегации',themes=['coding','technology'],admission_kind='qualifier')
profile('icys','ICYS · Young Scientists','advanced','14–18 лет; secondary school',['teen'],'Индивидуальная научная работа; среди дисциплин есть computer science.',
    [cat('Research paper','14–18','Индивидуально / национальная делегация','Исследование и доклад','Национальный маршрут')],['C770'],[('Организатор: 2027',icys)],
    'Своё исследование → национальный координатор / отбор → ICYS.',('Не каждый робот-макет считается исследованием.','Сейчас это старшая траектория семьи.'))

parc='https://www.parcrobotics.org/'
event('C771','Pan-African Robotics Competition 2026 · Dakar','Senegal','Африка','Dakar',parc,'Tech: middle school; Makers / Stars: high school; Drone: middle / high; Engineers / AI: university / professionals',
    'Сезонная регистрация завершилась 15 июля; новый вход и возможные late exceptions не подтверждены.','По лиге PARC','2026-11-03','2026-11-07',
    mat='Нет — младшая лига указана как middle school',osc='Нет — младшая лига указана как middle school',admission_kind='qualifier',
    note='Даты прочитаны в official metadata и публичном приложении организатора. Есть 6 лиг, но ни срок, ни география сети не означают открытый зарубежный приём детей.')
profile('parc','PARC · Pan-African Robotics Competition','regional','Middle / high school; university / professionals',['10-12','teen','university'],'Панафриканская сеть с шестью лигами; финал 2026 в Dakar.',
    [cat('Tech / Drone','Middle school; Drone также high','Размер по лиге','Робот / дрон','Сезонный приём'),cat('Makers / Stars','High school','Размер по лиге','По лиге','Сезонный приём'),cat('Engineers / AI','University / professionals','Размер по лиге','По лиге','Сезонный приём')],['C771'],[('Организатор PARC 2026',parc)],
    'Подтвердить школьную ступень и зарубежную команду → выбрать лигу → сезонный приём → финал.',('Дедлайн 2026 уже прошёл.','Начальная школа отдельно не заявлена; дети 6/9 не помечены подходящими.'))

abu='https://www.abu.org.my/news/hong-kong-hosts-abu-robocon-2026-as-young-innovators-take-on-kung-fu-quest/'
event('C772','ABU Robocon · следующий сезон','Мир','Мир','Место и даты следующего сезона не подтверждены',abu,'Университетские команды; числовой предел возраста по будущему регламенту',
    'Национальный конкурс / участник через маршрут ABU broadcaster; университетская команда.','Два робота по игре сезона',mat='Нет — университетский уровень',osc='Нет — университетский уровень',
    note='Официальный отчёт: турнир 2026 прошёл 23 августа в Hong Kong. Даты 2027 не выведены из прошлогодних.',admission_kind='qualifier')
profile('abu','ABU Robocon','advanced','Университетские команды; национальный отбор',['university'],'Азиатско-тихоокеанский инженерный турнир университетов.',
    [cat('ABU Robot Contest','Университет','По регламенту сезона','Роботы игры сезона','Национальный маршрут ABU')],['C772'],[('Отчёт организатора 2026',abu)],
    'Университетская команда → национальный Robocon → представитель на ABU.',('Национальные Robocon и финал ABU — отдельные этапы.','Это дальняя университетская траектория; даты следующего сезона неизвестны.'))

ro='https://www.robo-one.com/en/';roevent='https://www.robo-one.com/en/roboones/index/93'
event('C773','ROBO-ONE certified · ROBO-FIGHT Hamamatsu 2027','Япония','Азия','Hamamatsu Science Museum',ro,'Возраст и детский оператор для этого certified event не подтверждены.',
    'Искать отдельное положение certified tournament и правила робота; запись календаря не доказывает возможность заявки семьи.','Двуногий робот по certified event rules','2027-01-16','2027-01-16',
    evidence_level='catalog',scope='regional',note='Дата есть в официальном календаре ROBO-ONE. Основной 45th ROBO-ONE 26–27 сентября 2026 уже завершён. EN-сайт / правила не гарантируют EN-судейство в Hamamatsu.')
profile('roboone','ROBO-ONE / Light / auto / Beginners','international','Единого детского возраста не подтверждено',['unknown'],'Состязания двуногих роботов и отдельные certified tournaments.',
    [cat('ROBO-ONE / Light / auto / Beginners','По положению','Оператор / команда по событию','Двуногий робот','Player registration и правила этапа')],['C773'],[('Календарь и направления',ro),('45th ROBO-ONE: завершён',roevent)],
    'Освоить двуногого робота → Beginners / certified event → правила и квалификация конкретного турнира.',('Возраст 6/9, безопасность и язык требуют ответа организатора.','Ссылка старого LATAM-домена при проверке открыла посторонний gambling-сайт; она не используется для регистрации.'))

rc='https://www.robocup.org/';rc27='https://2027.robocup.org/'
event('C774','RoboCup Major 2027 · Soccer / Rescue / @Home / Industrial','Германия','Европа','Nuremberg Exhibition Center',rc27,'Major: техническая квалификация и правила лиги; не детский RoboCupJunior.',
    'Call for participation конкретной Major league → техническая квалификация. Общий анонс не равен открытой заявке.','Робот по Major league','2027-06-17','2027-06-21',
    mat='Условно — младший участник и техническая квалификация не подтверждены',osc='Условно — младший участник и техническая квалификация не подтверждены',date_scope='festival_window',admission_kind='qualifier',
    event_group='robocup-2027',references=[dict(url=rc,label='Лиги федерации')],note='17–21 июня — общий период RoboCup. Расписание конкретной дисциплины и symposium отдельно; visitor days в E013 — 17–20 июня. Универсальный нижний возраст Major в общем анонсе не установлен; исследовательский уровень не является возрастным запретом.')
profile('robocupmajor','RoboCup Major · Soccer / Rescue / @Home / Industrial','advanced','Правила конкретной лиги; старшая исследовательская траектория',['teen','university','unknown'],
    'Автономные роботы и исследовательская квалификация; отдельное направление от Junior.',
    [cat(n,'По лиге','По лиге','Робот / платформа по лиге','Technical qualification') for n in ['RoboCupSoccer','RoboCupRescue','RoboCup@Home','RoboCupIndustrial']],['C774'],[('Федерация: направления',rc),('Общий период 2027',rc27)],
    'RoboCupJunior или исследовательский проект → сильная техническая команда → qualification выбранной Major league.',('KidSize обозначает размер гуманоидного робота, а не возраст ребёнка.','Медали Junior, Major и сертификат зрителя — разные результаты.'))
e=next(e for e in d['events'] if e['id']=='C041')
e.update(start='2027-06-17',end='2027-06-21',period='',date_status='Подтверждено',date_scope='festival_window',event_group='robocup-2027')
e.setdefault('references',[]).append(dict(url=rc27,label='RoboCup 2027: общий период 17–21 июня',checked=DAY))
e['proof']='Возрастной регламент сохранён из предыдущей проверки. Общий период RoboCup 2027 подтверждён официальным анонсом 30.09.2026; игровые дни Junior ещё уточнить.'
e['note']+=' Общий период RoboCup 17–21 июня подтверждён; точные игровые дни Junior ещё уточнить.'

aus='https://www.robocupjunior.org.au/'
event('C775','RoboCup Junior Australia · локальные Primary / Secondary','Австралия','Океания','Площадка следующего этапа не подтверждена',aus,'Primary / Secondary / Open — отдельные местные division; не универсальные 14+ мирового финала.',
    'Проверить следующий local / national event, primary division, возраст и приём иностранной команды.','По категории Rescue / Soccer / OnStage',scope='national',admission_kind='qualifier',
    note='На сайте организатора есть местные Primary и Secondary divisions. Не переносить мировой порог Junior на все локальные Australian formats.')
rcjp=next(g for g in d['league_guide']['profiles'] if g['id']=='rcj')
rcjp['event_ids'].append('C775');rcjp['sources'].append(dict(title='Местные дивизионы Australia',url=aus,checked=DAY))

# Existing entries absent from the dossier view are mapped without pretending
# every organizer was fetched again successfully in this audit.
for id,name,group,ids,tags in [
    ('marc','MARC Taiwan','regional',['C035'],['6','9','10-12']),('tirt','TIRT Taiwan','regional',['C036'],['6','9','10-12','teen']),
    ('brazil','OBR / CBR / LARC · Brazil','regional',['C046'],['9','10-12','teen','university']),
    ('chile','Liga Robótica Chile','regional',['C047','C048','C049','C050','C051'],['unknown']),
    ('technovation','Technovation Girls','ai',['C062'],['6','9','10-12','teen']),('rcube','Rcube Robotics League','regional',['C093'],['unknown'])]:
    es=[next(e for e in d['events'] if e['id']==v) for v in ids];e=es[0]
    profile(id,name,group,e['age'],tags,e['title'],[cat(e['title'],e['age'],e['format'],e['gear'],e['entry'])],ids,
        [('Источник существующей карточки',e['source'])],e['entry'],(e['note'] or 'Возраст, иностранный вход и текущий регламент проверяются по карточке.',),
        evidence='Профиль составлен из существующей карточки с её источниками и ограничениями. Этот аудит подтвердил связь с базой; повторная проверка всех правил не завершена.')
    if id=='technovation':
        p=d['league_guide']['profiles'][-1];p['age_tags']=['unknown','teen'];p['nuances'].insert(0,'Программа для девочек; мальчики Матвей и Оскар не подходят. Включена для полноты карты программ.')
    # Preserve the actual check date of reused evidence.
    d['league_guide']['profiles'][-1]['sources'][0]['checked']=e['checked']
    d['league_guide']['profiles'][-1]['sources'][0]['title']='Источник карточки · повторный аудит правил не завершён'
    for s in d['sources']:
        if s['url']==e['source'] and s.get('evidence')=='Официальный источник прочитан 30.09.2026':
            s.update(checked=e['checked'],evidence='Источник существующей карточки; повторная проверка правил в v12 не завершена.')

def expo(id,title,country,region,city,url,start,end,highlights,policy='confirm_children',policy_note='В прочитанном источнике нет ясного допуска для детей 6/9; получить ответ организатора до покупки билетов.',entry='Visitor registration / билет организатора; условия категории посетителя уточнить.',tier='global',refs=(),note=''):
    e=event(id,title,country,region,city,url,policy_note,entry,'Не нужен',start,end,
        mat='Нет — детям 6/9 нельзя' if policy=='adults_only' else 'Да — со взрослым; правила посетителя отдельно' if policy=='family' else 'Условно — допуск детей уточнить',
        osc='Нет — детям 6/9 нельзя' if policy=='adults_only' else 'Да — со взрослым; правила посетителя отдельно' if policy=='family' else 'Условно — допуск детей уточнить',
        block='События',format='Посетитель выставки / expo и conference',participation='visitor',admission_kind='visitor',level='Выставка компаний и технологий',
        reward='Демонстрации, общение и знакомство с технологиями; не соревновательная медаль',
        priority='P4 — детям нельзя, взрослый маршрут' if policy=='adults_only' else 'P3 — посещение при удобной поездке',
        action='Проверить пропуск, детское правило, программу демонстраций и список нужных экспонентов.',
        exhibition_tier=tier,visitor_policy=policy,visitor_policy_note=policy_note,adult_entry=entry,highlights=highlights,exhibitors=[],
        exhibitor_note='Наличие отраслей / expo подтверждено. Отдельный список компаний этого выпуска не проверен; участие прошлых экспонентов не гарантируется.',
        exhibitor_directory_url=url,importance_reason='Редакционный выбор по тематике, международному / региональному охвату и выставочной программе организатора; не официальный мировой рейтинг.',
        evidence_level='rules' if policy in ['family','adults_only'] else 'event_page',note=note,
        references=[dict(url=u,label=t) for t,u in refs],themes=['robotics','ai','technology'])
    for t,u in refs: source(u,t)
    return e
expo('E096','Expo Manufactura 2027','Мексика','Северная Америка','Monterrey · Cintermex','https://expomanufactura.com.mx/','2027-02-23','2027-02-25',
    ['Робототехника и автоматизация','Промышленное оборудование','Цифровое производство'],policy='adults_only',policy_note='Организатор: профессионалы отрасли старше 21 года. Детям 6/9 вход не подходит.',entry='Бесплатная регистрация профессионала отрасли старше 21 года.',tier='regional')
expo('E097','Smart Technology Expo 2026','Мексика','Северная Америка','Guadalajara · Expo Guadalajara','https://smarttechnologyexpo.mx/','2026-11-18','2026-11-20',
    ['Автоматизация и роботы','AI / Machine Learning','Дроны и Industry 4.0'],tier='regional',refs=[('Организатор IGECO','https://www.igeco.mx/')],note='Название / даты ITM из старых каталогов не приравнены автоматически к этому мероприятию.')
expo('E098','EXPOMAFE 2027','Brazil','Южная Америка','São Paulo Expo','https://www.expomafe.com.br/','2027-05-04','2027-05-08',
    ['Промышленные роботы','Автоматизация ячеек','3D printing / производство'],policy='adults_only',policy_note='До 16 лет вход запрещён даже с родителями. Есть исключение для технических школьных групп старше 14; дети 6/9 не подходят.',
    entry='Бесплатно для специалистов отрасли, пропуск и photo ID. Детский порог из FAQ.',tier='regional',refs=[('FAQ: возраст и посетители','https://www.expomafe.com.br/a-feira/faq-expomafe/')])
expo('E099','Australian Manufacturing Week 2027','Австралия','Океания','Melbourne · MCEC','https://australianmanufacturingweek.com.au/visit2027/','2027-05-11','2027-05-14',
    ['Автоматизация производства','Роботы и оборудование','Аддитивное производство'],policy='family',policy_note='Официальный visitor guide: дети / ученики до 15 лет только со взрослым. Взрослый вход рассчитан на trade personnel.',
    entry='Регистрация всех посетителей, badge и photo ID; бесплатно для trade personnel. Регистрация открывается в начале 2027.',tier='regional')
expo('E100','Africa Tech Festival 2026','ЮАР','Африка','Cape Town · CTICC','https://africatechfestival.com/','2026-11-17','2026-11-19',
    ['AI и enterprise technology','Связь / инфраструктура','Стартапы и выставочный зал'],tier='regional',note='AfricaCom, AfricaTech и сопутствующие треки учтены в одном фестивале, не как независимые поездки.')
expo('E101','AI Expo Africa 2026','ЮАР','Африка','Johannesburg · Sandton Convention Centre','https://aiexpoafrica.com/ai-expo-africa-2026-faq/','2026-10-28','2026-10-29',
    ['Enterprise AI','Automation','Vendor / Startup Expo'],tier='regional',entry='Платный delegate ticket; expo / conference / workshops по типу пропуска. Профессиональная аудитория, допуск детей неизвестен.')
expo('E102','VivaTech 2027','France','Европа','Paris · Expo Porte de Versailles','https://vivatech.com/','2027-06-16','2027-06-19',
    ['AI и hardware','Стартапы / технологии','Демонстрации и expo'],note='Даты 2027 подтверждены. Семейный / public day 2027 и детские билеты отдельно не подтверждены; не перенесены с выпуска 2026.')
expo('E103','World Summit AI Amsterdam 2026','Netherlands','Европа','Amsterdam · Taets Art & Event Park','https://worldsummit.ai/','2026-10-07','2026-10-08',
    ['AI решения','Поставщики и стартапы','Конференция + expo'],entry='Платный билет, права доступа по категории. Это профессиональный AI summit; детский допуск уточнить.')
expo('E104','World AI Cannes Festival 2027','France','Европа','Cannes · Palais des Festivals','https://waicf.com/','2027-02-10','2027-02-11',
    ['AI solution providers','Live demonstrations','Exhibition floor / AI Trail'],note='В 2027 организатор Informa и enterprise формат. Прошлый public / family day не перенесён автоматически.')
expo('E105','SPS Smart Production Solutions 2026','Германия','Европа','Nuremberg','https://sps.mesago.com/nuernberg/en/expo.html','2026-11-24','2026-11-26',
    ['Промышленная автоматизация','Industrial AI','Компоненты и управление'],policy='adults_only',policy_note='FAQ: дети от 14 лет со взрослым и билетом. Для 6/9 лет разрешённый вход не предусмотрен.',
    entry='Персональный online ticket. FAQ допускает сопровождаемых учеников от 14 лет.',refs=[('Tickets FAQ: children 14+','https://sps.mesago.com/nuernberg/en/expo/for_visitors/tickets.html')])
expo('E106','AI EXPO KOREA 2027','Южная Корея','Азия','Seoul · COEX Hall A','https://aiexpo.co.kr/전시회-개요/','2027-04-14','2027-04-16',
    ['AI solutions','AI infra / edge hardware','AI + robotics'],policy='adults_only',policy_note='Visitor guide: high school и младше строго ограничены, в том числе с родителем. Детей 6/9 не считать допущенными.',
    entry='B2B visitor registration; семинары отдельно. Детский вход ограничен даже в сопровождении.',refs=[('Visitor guide: возраст','https://aiexpo.co.kr/참관안내/')])
expo('E107','Automation Expo India 2027','India','Азия','Mumbai · B.E.C. Goregaon','https://www.automationindiaexpo.com/','2027-06-02','2027-06-05',
    ['Роботы / machine vision','Agentic AI / IIoT','Factory automation'],tier='regional',entry='Free visitor registration, пропуск организатора; профессиональная аудитория. Детский вход уточнить.')
expo('E108','LEAP / DeepFest 2027','Saudi Arabia','Азия','RECC Malham · Riyadh region','https://onegiantleap.com/','2027-04-12','2027-04-15',
    ['AI / DeepFest','Global tech brands','Стартапы и hardware'],policy='adults_only',policy_note='FAQ: 18+; дети не допускаются, детских пропусков нет.',entry='Профессиональный ticket 18+; категории выставки и conference по pass.',
    refs=[('FAQ: 18+, no children','https://onegiantleap.com/faq')],note='DeepFest проводится вместе с LEAP: один поездочный блок, не два независимых финала / выставки.')
expo('E109','Web Summit Lisbon 2026','Portugal','Европа','Lisbon','https://websummit.com/','2026-11-09','2026-11-12',
    ['Tech / AI стартапы','Партнёры и expo','Глобальная конференция'],note='Широкая tech conference с expo. Не специализированная выставка, где обязательно представлены все производители роботов.')
expo('E110','Web Summit Rio 2027','Brazil','Южная Америка','Rio de Janeiro · Riocentro','https://rio.websummit.com/','2027-06-14','2027-06-17',
    ['Стартапы / AI','Tech partners / expo','Латиноамериканский tech ecosystem'],tier='regional',note='Заголовок и приглашение 2027 дают 14–17 июня; на той же странице остался блок прошлогодних дат 2026. Он не используется как новый календарь.')
for id,season,start,end,city in [('E111','Autumn 2026','2026-11-11','2026-11-13','Makuhari Messe'),('E112','Spring 2027','2027-04-21','2027-04-23','Tokyo Big Sight')]:
    e=expo(id,'NexTech Week Tokyo · AI EXPO '+season,'Япония','Азия',city,'https://www.nextech-week.jp/hub/en-gb.html',start,end,
        ['AI EXPO','Digital human / emerging tech','Business solutions'],note='Форма Autumn 2026 не разрешает регистрацию младше 18 лет. Отдельное правило входа ребёнка с родителем и Spring 2027 ещё не подтверждено.',
        refs=[('Autumn: visitor registration','https://www.nextech-week.jp/autumn/en-gb/register.html')]);e['event_group']='nextech-tokyo'

for e in d['events']:
    if e['id'] in ['E100','E103','E104','E109','E110','E111','E112']:
        e['themes']=['ai','technology']

# Scope inventory, not a fictitious percentage of the entire world's events.
region_groups={
 'Северная Америка':['Северная Америка','Центральная Америка','Карибский регион'],
 'Южная Америка':['Южная Америка'],'Европа':['Европа'],'Африка':['Африка'],'Азия':['Азия'],'Океания':['Океания']}
country_iso={c['country']:c['iso'] for c in d['countries']};country_iso.update({c['en']:c['iso'] for c in d['countries']})
country_iso.update({'США':'USA','Южная Корея':'KOR','Коста-Рика':'CRI','Мексика':'MEX','Тайвань':'TWN','ЮАР':'ZAF','Австралия':'AUS','Германия':'DEU','Япония':'JPN','Vietnam':'VNM','Netherlands':'NLD'})
notes={
 'Северная Америка':'Сильный перекос в каталог VEX США. México / Costa Rica приоритетны, но полный список местных турниров, школ и заявок не закрыт.',
 'Южная Америка':'Много карточек Ecuador и региональных маршрутов Chile; Brazil, Perú и другие страны требуют местных этапов, квот и календарей.',
 'Европа':'Есть мировые финалы и ведущие выставки. Национальные FIRST / WRO / RoboCup и независимые школьные турниры по всем странам не перечислены полностью.',
 'Африка':'До расширения почти все соревнования были в South Africa. Добавлен PARC Senegal; Maghreb, East / West Africa и местные отборы остаются пробелами.',
 'Азия':'China, Taiwan, Japan, Korea и ряд сетей представлены. Не все дисциплины WRC / FIRA и этапы India / Southeast Asia / Middle East исследованы.',
 'Океания':'Есть Australia / New Zealand и младший маршрут RCJ Australia. Нет полного списка local tournaments / university events / Pacific islands.'}
continents=[]
for name,regions in region_groups.items():
    a=[e for e in d['events'] if e['region'] in regions];isos={i for e in a for i in e.get('iso',[]) or ([country_iso[e['country']]] if e['country'] in country_iso else [])}
    continents.append(dict(name=name,regions=regions,total=len(a),countries_with_records=len(isos),competitions=sum(e['block']=='Соревнования' for e in a),
        events=sum(e['block']=='События' for e in a),major_exhibitions=sum(bool(e.get('exhibition_tier')) for e in a),camps=sum(e['block']=='Лагеря' for e in a),
        status='Частично исследовано',remaining=notes[name]))
for p in d['league_guide']['profiles']:
    assert set(p['event_ids'])<=set(e['id'] for e in d['events'])
league_inventory=[]
for p in d['league_guide']['profiles']:
    a=[e for e in d['events'] if e['id'] in p['event_ids'] and e['block']=='Соревнования']
    league_inventory.append(dict(id=p['id'],name=p['name'],group=p['group'],event_ids=[e['id'] for e in a],cards=len(a),
        future_dated=sum(bool(e['start']) and e['end']>=DAY for e in a),status='Есть профиль и карточки; местный охват частичный' if a else 'Только профиль; календарь этапов не добавлен',
        source=p['sources'][0]['url'],new=p['id'] in new_profiles))
backlog=[
 dict(kind='Лиги / соревнования',name='MILSET Expo-Sciences / science project networks',reason='Разделить выставку проекта, оценённый конкурс и путь national delegation. Проверить технологии / robotics categories и школьный возраст.',url='https://milset.org/'),
 dict(kind='Лиги / соревнования',name='RoboNation RoboSub / RoboBoat / RobotX; EU robotics challenges',reason='Старшие автономные системы и отдельные финалы ещё не проаудированы. SeaPerch не заменяет эти лиги.',url='https://robonation.org/'),
 dict(kind='Лиги / соревнования',name='BattleBots / NHRL / combat robotics circuits',reason='Открытые турниры, весовые классы, возраст оператора и безопасность не покрыты полностью.',url='https://www.nhrl.io/'),
 dict(kind='Лиги / соревнования',name='Все национальные FIRST / WRO / VEX / RCJ qualifiers',reason='Наличие глобальной сети и national organizer не равно полному списку турниров каждой страны.',url='https://wro-association.org/about-wro/member-countries/'),
 dict(kind='Выставки',name='CIROS Shanghai / CHITEC Beijing',reason='Организатор и следующее издание ещё требуют первичного подтверждения. Даты из агрегаторов не включены.',url=''),
 dict(kind='Выставки',name='TechEx / AI & Big Data Expo: London, North America, Europe',reason='Старый домен ai-expo.net недоступен; текущий бренд, города и даты нужно сверить перед добавлением.',url=''),
 dict(kind='Выставки',name='Industrial Transformation México (ITM)',reason='Источник IGECO показывает Smart Technology Expo; старые ITM-каталоги дают другие даты. ITM не приравнен к STE без подтверждения.',url='https://www.igeco.mx/'),
 dict(kind='Выставки',name='ICRA / IROS exhibitions, MWC Shanghai / Doha, другие выпуски GITEX',reason='Конференции, выставочные зоны и отдельные города имеют разные visitor policies и календарные выпуски; полный сезонный ряд ещё не закрыт.',url=''),
 dict(kind='Страны',name='Caribbean, Pacific islands и страны без конкретных карточек',reason='Справочник стран — карта дальнейшего исследования. Не найдено в базе не означает, что соревнований в стране нет.',url='')]
expo_inventory=[dict(id=e['id'],name=e['title'],country=e['country'],region=e['region'],start=e['start'],end=e['end'],visitor_policy=e['visitor_policy'],source=e['source'],new=e['id'] in new_ids) for e in d['events'] if e.get('exhibition_tier')]
d['completeness_audit']=dict(version=12,checked=DAY,status='partial',conclusion='Нет: все лиги, все турниры и все крупные выставки мира пока не собраны. Присутствие шести континентов не доказывает полноту.',
    scope='Инвентаризация базы и поиск крупных пробелов по официальным источникам; календарные издания 2026–2027 и недатированные маршруты. Повторная проверка каждого старого источника не выполнена.',
    baseline=dict(cards=977,competition_cards=761,event_cards=95,camp_cards=121,league_profiles=41,major_exhibition_cards=36,countries_with_records=61,vex_cards=464),
    counts=dict(cards=len(d['events']),competition_cards=sum(e['block']=='Соревнования' for e in d['events']),event_cards=sum(e['block']=='События' for e in d['events']),
        camp_cards=121,league_profiles=len(league_inventory),major_exhibition_cards=len(expo_inventory),vex_cards=464),
    continents=continents,league_inventory=league_inventory,exhibition_inventory=expo_inventory,known_backlog=backlog,
    new_ids=new_ids,new_profiles=new_profiles,updated_ids=['C041'],
    caveats=['Число карточек включает отдельные дисциплины, этапы, выпуски и площадки; это не число независимых мировых лиг или уникальных фестивалей.',
        'Большая доля VEX не означает полноту остальных направлений или США.',
        'Карточка с датой не доказывает открытую регистрацию, возрастной допуск или национальную квоту.',
        'Антарктида: релевантный местный календарь не найден в рамках этого исследования; это не доказательство отсутствия всех мероприятий.',
        'Лагеря в этом проходе не расширялись; прежние 121 программы тоже не являются всеми лагерями мира.'],
    source_issues=[dict(name='ROBO-ONE LATAM',status='Старый домен перенаправляет на посторонний gambling-сайт; не использовать как регистрационный.',official_alternative=ro),
        dict(name='SeaPerch 2027',status='Handbook содержит смешанные заголовки сезона и разные сроки публикации regionals; версия класса требует уточнения.',official_alternative=sp),
        dict(name='FIRA qualification',status='Описание двухстраничной заявки и таблица шестистраничного TDP расходятся; подтвердить Youth category.',official_alternative=fira),
        dict(name='Повторный доступ к старым источникам',status='Некоторые страницы Brazil / Chile / iREX и CIROS не прочитались. Старые проверенные факты не получили новую фиктивную дату.',official_alternative='')])
d['league_guide']['version']=12
d['league_guide']['methodology']='Справочник содержит '+str(len(league_inventory))+' семейств и программ. Все 46 прежних маршрутов сохранены. Новые сети и ранее не показанные карточки добавлены; даты и границы подтверждения видны отдельно. Полный список всех лиг мира пока не подтверждён. Возрастной фильтр показывает кандидатов, а не принятую регистрацию.'
d['expansion_log'].append(dict(version=12,date=DAY,scope='Completeness audit across continents, leagues and major exhibitions',added_ids=new_ids,updated_ids=['C041'],notes=['Пробелы добавлены по первичным источникам; дальнейшие неизвестные направления опубликованы в completeness_audit.','Все прежние карточки и исходный аудит сохранены.']))
d['source_count']=len(d['sources'])
(ROOT/'data/catalog.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
(ROOT/'data/audit-v12.json').write_text(json.dumps(d['completeness_audit'],ensure_ascii=False,indent=2))
plan=json.loads((ROOT/'data/research-plan.json').read_text());plan['status']='active';plan['updated']=DAY
for r in plan['requirements']:
    if r['id']=='global_competitions':r['evidence']=f"v12: {d['completeness_audit']['counts']['competition_cards']} cards / {len(league_inventory)} guide profiles. Continental inventory and unresolved league / local qualifiers published; world completeness not established."
    if r['id']=='exhibitions':r['evidence']=f"v12: {d['completeness_audit']['counts']['event_cards']} event cards, {len(expo_inventory)} curated major exhibition cards. Added regional industry / AI expos across Africa, Latin America, Australia; adult / family gates recorded. Known missing series remain."
plan['completeness_audit']='data/audit-v12.json';(ROOT/'data/research-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2))
print(json.dumps(dict(added_cards=len(new_ids),new_profiles=len(new_profiles),counts=d['completeness_audit']['counts']),ensure_ascii=False))
