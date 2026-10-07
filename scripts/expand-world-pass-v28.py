"""Add audited world/Caribbean routes and EN/ES learning, preserving prior records."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/catalog.json';d=json.loads(path.read_text())
assert len(d['events'])==1223 and d['completeness_audit']['version']==27
old={e['id'] for e in d['events']};new=[];profiles=[]

def event(id,title,country,region,city,source,age,mat,osc,entry,gear,
          start='',end='',deadline='',cost='Стоимость / действующий тариф уточнить',
          note='',block='Соревнования',priority='P2 — после проверки допуска',
          participation='team',evidence='event_page',languages=(),support=(),
          language='Язык занятий / судейства не установлен по языку сайта',
          mode=None,scope='international',date_scope='festival_window',period=''):
    e=dict(id=id,block=block,title=title,country=country,region=region,city=city,
        source=source,checked='2026-10-01',start=start,end=end or start,deadline=deadline,
        period=period,date_status='Подтверждено' if start else 'Не объявлено',
        age=age,mat=mat,osc=osc,format=participation,participation=participation,
        admission_kind='visitor' if participation=='visitor' else 'program' if block=='Лагеря' else 'open_application',
        entry=entry,gear=gear,cost=cost,language=language,languages=list(languages),
        support_languages=list(support),scope=scope,level='Профильная программа; возраст и масштаб отдельно',
        importance_reason='Редакционная оценка конкретного формата; не обещание допуска, медали или качества преподавания.',
        reward='Уровень результата и роль ребёнка проверять по протоколу; участие не равно призовому месту.' if block=='Соревнования' else 'Учебный результат / посещение; не соревновательная международная медаль',
        priority=priority,status='Идея',action='Проверить условия именно нового сезона, возраст / класс и доступ семьи до заявки или поездки.',
        evidence_level=evidence,references=[],note=note,
        registration_status='Семья не зарегистрирована; публикация страницы не подтверждает место.',
        proof='Прочитан первичный источник; неизвестные условия оставлены неизвестными.',
        language_certainty='Подтверждение относится к указанному учебному материалу / формату; англоязычная страница сама по себе не доказывает язык занятия.',
        date_scope=date_scope)
    e['themes']=['robotics','coding'] if block=='Соревнования' else ['technology']
    if mode:e['language_mode']=mode
    assert id not in old and not any(x['id']==id for x in new)
    new.append(e);return e

P4='P4 — будущая старшая ступень / младший допуск не подтверждён'
later='Нет для текущей младшей ступени; будущий путь'
launch='https://robonation.org/2027-season-launch/'

event('C885','RoboBoat 2027','США','Северная Америка','Sarasota · Nathan Benderson Park',
    'https://roboboat.org/programs/2027/','High School / College; ≥75% full-time students; минимум 3 участника',later,later,
    'Регистрация 01.10–01.12.2026; отдельный deadline материалов 13.01.2027.',
    'Автономное надводное судно; навигация, восприятие и управление.',
    '2027-02-18','2027-02-23','2026-12-01',cost='1 500 USD за команду; судно, поездка и жильё отдельно.',
    priority=P4,note='Team Handbook 2027 ещё COMING SOON. Даты подтверждены, полные технические правила не объявлены. Отдельный открытый kickoff в E136.')
event('C886','RoboSub 2027','США','Северная Америка','Irvine · Woollett Aquatics Center',
    'https://robosub.org/programs/2027/','High School / College; ≥75% full-time students; минимум 3 участника',later,later,
    'Регистрация 01.12.2026–01.04.2027; submission 23.06.2027.',
    'Автономный подводный аппарат и документация.',
    '2027-08-10','2027-08-15','2027-04-01',cost='1 750 USD за команду; аппарат и поездка отдельно.',
    priority=P4,note='Новая эволюция формата объявлена, но Team Handbook 2027 ещё не опубликован. Правила 2025 не названы правилами 2027. Открытый kickoff в E137.')
event('C887','Maritime RobotX Challenge 2026','Сингапур','Азия','The Promontory · Marina Bay',
    'https://robotx.org/programs/2026/','High School / College; ≥75% full-time students; нет минимального размера команды',later,later,
    'Регистрация и grant application закрыты. Путь существующих команд; новые семейные заявки не обещаны.',
    'Несколько автономных систем в морской среде; подробный handbook текущего издания.',
    '2026-11-08','2026-11-14',priority=P4,note='Закрытая регистрация не отменяет объявленные дни турнира. Вход семьи зрителями не установлен; не создавать из турнира подтверждённую детскую выставку.')
event('C888','SUAS 2027 · Student Unmanned Aerial Systems','США','Северная Америка','Tulsa · Skyway Range',
    'https://suas-competition.org/competitions','Студенческий / старший технический маршрут; правила возраста 2027 ещё не прочитаны',later,later,
    'Издание объявлено; полноценный регламент и приём 2027 уточнить на странице организатора.',
    'Автономная воздушная система; командная инженерия.',
    '2027-10-01','2027-10-04',priority=P4,evidence='event_page',note='Handbook на странице относится к 2026. Старые даты, eligibility и deadline не перенесены в новый год.')
for id,title,date in [('C889','Hello World','2027-07-26'),('C890','Dress Rehearsal','2027-08-23'),('C891','VRX Competition','2027-09-20')]:
    event(id,'Virtual RobotX 2027 · '+title,'Онлайн / мир','Онлайн / глобально','Виртуально',
        'https://robotx.org/programs/vrx-2027/','High School / College; параметры состава команды уточнить',later,later,
        'Регистрация 01.12.2026–15.07.2027; три отдельные контрольные даты, не ежедневный лагерь.',
        'Симуляция автономных систем surface / aerial / underwater; физический аппарат не обязателен.',
        date,date,'2027-07-15',cost='300 USD за регистрацию в соревнование; не по 300 за каждый этап.',
        priority=P4,note='Три записи — этапы одной программы. Условия детского участия не расширены с High School / College до 6 /9 лет; новый robotics simulator не является детской игрой.')
event('C892','IGVC 2027 · Intelligent Ground Vehicle Competition','США','Северная Америка','Rochester, Michigan · Oakland University',
    launch,'Автономные наземные системы; младшая категория / текущий eligibility не установлен',later,later,
    'Даты в первичном season launch. Регламент, team minimum и регистрация ещё требуют проверки.',
    'Автономная наземная машина; технический трек на будущее.',
    '2027-06-04','2027-06-08',priority=P4,note='По одному анонсу нельзя подтвердить детский допуск. Сайт IGVC не прочитан из-за ошибки проверки сертификата; проверку TLS не отключали.')
event('C893','IARC 2027 · International Aerial Robotics Competition','Мир','Онлайн / глобально','Место этапа уточнить',
    launch,'Исследовательская автономная авиация; возраст / состав новой команды не установлен',later,later,
    'Анонс указывает подачу заявок January–March 2027; конкретные даты и регламент не объявлены в прочитанном источнике.',
    'Автономная воздушная робототехника; будущий инженерный ориентир.',
    priority=P4,period='Подача заявок: январь–март 2027; точные дни неизвестны',
    note='Месячное окно не превращено в 01.01–31.03 и не экспортировано в календарь. Полноценный сайт IARC не прочитан; одно объявление не доказывает eligibility.')

dom_explore='https://www.fll-caribe-rd.org/copy-of-challenge'
dom_challenge='https://www.fll-caribe-rd.org/fll'
dom_foreign='https://www.fll-caribe-rd.org/international-teams-c19rs'
event('C894','FIRST LEGO League República Dominicana · Explore · следующий этап','Доминиканская Республика','Карибский регион','Santo Domingo',
    dom_explore,'Местная обзорная страница: 6–9; отсечение нового сезона и техника уточнить',
    'Условно: опубликовано 6–9; возраст на отсечение сезона и класс подтвердить',
    'Условно: опубликовано 6–9; новый сезон и иностранный вход подтвердить',
    'Связаться с FLL-Caribe / FUNDECITEC для категории нового сезона; письмо / заявка от семьи ещё не отправлены.',
    'LEGO-проект и совместная работа; аппаратная редакция нового сезона отдельно.',
    evidence='program',scope='national',note='Возраст 6–9 локального overview отличается от глобальной Explore 6–10. Тема BIOGLOW 2026–27 подтверждена на отдельной странице. Нет даты следующего фестиваля и нет подтверждения приёма команды из México / Costa Rica.',
    language='Для Caribbean Teams описаны English judge station и English ambassador; актуальный язык конкретного младшего формата уточнить.',support=['EN'])
event('C895','FIRST LEGO League República Dominicana · Challenge BIOGLOW 2026–27','Доминиканская Республика','Карибский регион','Santo Domingo',
    dom_challenge,'Локальный overview: 9–15; до 10 детей и минимум 1 coach',
    'Условно: 9–15; национальное отсечение и право иностранной команды подтвердить','Нет для Challenge 9–15; Explore отдельно в C894',
    'Школа, клуб или группа друзей могут создать команду; действующий приём и международную квоту согласовать с партнёром.',
    'Автономный LEGO robot game, проект и Core Values. Редакция оборудования сезона отдельно.',
    evidence='program',scope='national',note='На другой странице прямо объявлена тема BIOGLOW 2026–27. Старый мировой размер сети и даты финала апреля 2026 не приняты за новые условия. Foreign policy относится к Caribbean Teams, не к любой стране.',
    language='English judge station / ambassador для Caribbean Teams подтверждены в local foreign policy; остальное судейство / местный язык подтвердить.',support=['EN'])
for e in new[-2:]:e['references']=[{'url':dom_foreign,'label':'Caribbean teams · English support / foreign policy'},{'url':'https://www.fll-caribe-rd.org/desafo-anual','label':'Тема сезона 2026–27'}]
event('C896','FTC Jamaica · следующий национальный сезон','Ямайка','Карибский регион','Kingston · место следующего турнира уточнить',
    'https://jamaicarobotics.org/','Late middle school / high school; новые местные правила возраста уточнить',later,later,
    'Местный партнёр Jamaica Robotics; действующий season registration не подтверждён.',
    'FIRST Tech Challenge — старший роботизированный командный формат.',
    priority=P4,evidence='historical_program',scope='national',note='Текущая страница содержит даты 20–21 февраля 2026 и игру 2025–26. Они прошли и не стали новым финалом 2027. Доступ младшим и иностранной семейной команде не установлен.')
event('C897','FTC Trinidad & Tobago · BIOBUZZ 2026–27','Тринидад и Тобаго','Карибский регион','NIHERST · национальная программа',
    'https://www.niherst.gov.tt/scipop/first-tech-challenge.html','В индексированном официальном анонсе:12–18 и secondary / youth teams',later,later,
    'NIHERST указан как FIRST PDP; новый национальный календарь, fee и eligibility уточнить.',
    'FIRST Tech Challenge — проектирование и программирование командного робота.',
    priority=P4,scope='national',note='Официальный анонс 2026–27 найден в индексе, но полная страница отдаёт защитную заглушку. Поэтому не заявляем прочитанный регламент и не переносим дату турнира июня 2026.')
event('C898','FIRST LEGO League Trinidad & Tobago · следующий этап','Тринидад и Тобаго','Карибский регион','NIHERST · место финала уточнить',
    'https://niherst.gov.tt/scipop/fll-what-is-it.html','Локальная действующая возрастная категория не установлена; глобальная Challenge начинается с 9 /10 по стране',
    'Условно: местную Challenge и класс проверить','Нет подтверждённой категории Challenge в 6 лет; local Explore не найден',
    'NIHERST — локальный партнёр; нужно действующее объявление национального сезона и ответ об иностранной команде.',
    'Robot game, проект и Core Values; редакция набора сезона уточнить.',
    scope='national',evidence='historical_program',note='Наличие партнёра подтверждает маршрут, но не дату ближайшего турнира. Старые Superpowered / Masterpiece и расписание 2019–2020 не считаются новым календарём.')
event('C899','Barbados Robotics Innovation Challenge · Phase II final 2027','Барбадос','Карибский регион','Место очного финала уточнить у CSF',
    'https://caribbeanscience.org/bric/','Старше 15 и младше 30 на 1 января года Challenge; максимум 6 в команде',later,later,
    'Phase I design proposal завершилась 16.08.2026; Phase II для отобранных проектов. Новый открытый приём не обещан.',
    'Инженерный robot project; закупленные компоненты в сумме менее 5 000 USD.',
    '2027-08-13','2027-08-13',priority=P4,note='Финал будущий, а входная фаза завершена. Младший возраст не допускается. Полные правила регионального представительства проверить; нет гарантии призовых или допуска семьи.')
cso='https://caribbeanscience.org/cso/'
for id,title,date in [('C900','Computer Coding Olympiad','2027-01-13'),('C901','Robotics & Electronics Systems Olympiad','2027-01-14')]:
    event(id,'Caribbean STEM Olympiads 2027 · '+title,'Онлайн / CARICOM','Карибский регион','Виртуальный финал',
        cso,'13–15 /16–18 /19–21 на 01.01.2027; гражданство CARICOM или 4 года постоянного проживания',later,later,
        'Индивидуальный / независимый или командный проект; региональное право и отбор обязательны. Deadline30.11.2026.',
        'Социально полезный software project' if id=='C900' else 'Hardware-dominant robotics / electronics project',
        date,date,'2026-11-30',priority=P4,participation='individual_or_team',scope='regional',evidence='rules',
        note='Observer countries не входят в citizenship category. Детям 6/9 возраст закрыт. День защиты — для финалистов, не открытая регистрация; публичная церемония отдельно E135.')
event('C902','CoderZ League · следующий сезон не подтверждён','Онлайн / мир','Онлайн / глобально','Виртуальный robot simulator',
    'https://competition.gocoderz.com/fall-league/','Последняя датированная страница2023: Novice Grades4–6, Junior6–9, Pro7–12; FAQ содержит другие старые рамки',
    'Условно: класс и текущий сезон не подтверждены','Условно: новый минимальный класс не подтверждён; старый FAQ any grade не является текущим допуском',
    'Проверить новый season guide, платную лицензию и возможность семейной команды; старый registration banner не использовать как подтверждение открытого приёма.',
    'Blockly / Python в виртуальной робототехнике, компьютер и интернет; физический робот не обязателен.',
    evidence='historical_program',note='Fall / Spring страницы — 2023, root содержит 2022. FAQ смешивает 2020 и 2023 и suggested versus any grade. Даты и классы не перенесены автоматически на 2026–27.')

event('E135','Caribbean STEM Olympiads 2027 · публичная церемония наград','Онлайн / CARICOM','Карибский регион','Онлайн · 14:00–16:30 AST',cso,
    'Публичная церемония; семьи и друзья прямо приглашены',
    'Да как зритель; ссылка и сопровождение родителя отдельно','Да как зритель; это не участие в олимпиаде',
    'Следить за опубликованным порядком подключения к виртуальной церемонии.',
    'Просмотр проектов / церемонии; собственная заявка в соревнование не нужна.',
    '2027-01-17','2027-01-17',block='События',participation='visitor',scope='regional',priority='P3 — образовательное посещение',
    note='Олимпиада допускает13–21 с региональными условиями; зрительская церемония — отдельный открытый формат. Не промышленная выставка и не сертификат участия ребёнка в конкурсе.')
for id,title,date,source in [('E136','RoboBoat 2027 · открытый TeamTime kickoff','2026-10-22','https://roboboat.org/programs/2027/'),('E137','RoboSub 2027 · открытый TeamTime kickoff','2027-01-21','https://robosub.org/programs/2027/')]:
    event(id,title,'Онлайн / мир','Онлайн / глобально','Онлайн · 19:00 Eastern Time',source,
        'Open to all interested teams; отдельный возрастной gate зрителей не опубликован',
        'Условно: смотреть с родителем после проверки регистрации','Условно: открытый webinar не означает детскую соревновательную категорию',
        'Ссылка webinar / регистрация по официальной странице. Для RoboSub регистрация ещё coming soon.',
        'Введение в будущий автономный инженерный конкурс.',
        date,date,block='События',participation='visitor',priority='P3 — образовательное посещение',
        note='19:00 указан в Eastern Time. ICS напоминает о дне; точное время и ссылка в досье. Соревновательный возраст High School / College не перенесён на зрителей. Язык выступления и Zoom-вход с детьми уточнить.')
event('E138','Hour of AI / Hour of Code · семейное или школьное событие','Мир','Онлайн / глобально','Онлайн / своё локальное мероприятие',
    'https://code.org/cs/hour-of-ai','Учебные активности по классу; каждый tutorial имеет свою границу',
    'Условно: выбрать подходящий учебный модуль','Условно: выбрать младший coding-модуль; Mix & Move8+ не переносить на6 лет',
    'Можно изучать материалы или организовать своё занятие; регистрировать событие и аккаунты семья ещё не просила.',
    'Компьютер / планшет по модулю; часть курса имеет unplugged задания.',
    block='События',participation='visitor',evidence='program',languages=['EN','ES'],
    language='ES / EN учебные материалы по выбранному модулю; язык собственного занятия определяет организатор.',
    cost='Учебные материалы свободного доступа; локальное посещаемое событие может иметь свои условия.',
    note='Это образовательная кампания / мастер-класс, не лига или выставка компаний. Даты единого будущего фестиваля не установлены; годовой формат не заменён выдуманной неделей декабря. Программы L209 / L210 отдельно.')

event('L206','Barbados Junior Robotics Camp · следующий набор','Барбадос','Карибский регион','UWI Cave Hill · дневной формат',
    'https://caribbeanscience.org/barbados-junior-robotics-camp-2026/','2026:10–18; Level I10+ на01.07, II12+, III13+; новые cutoff отдельно',later,later,
    'CARICOM citizenship, либо родитель легально работает в Barbados ≥1 года; места и документы обязательны.',
    'Механизмы, роботы, микроконтроллеры; опыт определяет уровень.',
    block='Лагеря',participation='day_camp',evidence='historical_program',priority=P4,mode='unconfirmed',
    cost='2026: Non-CARICOM category1 000 USD; жильё и расходы ребёнка отдельно. Новый тариф не объявлен.',
    note='Будущий набор не найден. Tourist family не соответствует опубликованному исключению для non-CARICOM. Страница2026 называет Friday15August, но15.08.2026 — Saturday; эта неоднозначность не стала датами новой смены. Язык преподавания не выведен из English сайта.')
event('L207','WorldSkills Barbados Juniors · Future Skills Camp · следующий набор','Барбадос','Карибский регион','Дневной формат · провайдер места уточняет',
    'https://www.worldskillsbarbados.org.bb/campaigns/future-skills-camp-2026','10–16; разные недельные технологические направления',later,later,
    'Программа для молодых Barbadians; иностранный детский приём и новый сезон не установлены.',
    'В программе2026 есть aerial robotics, VR / XR и другие tech topics; не все недели посвящены роботам.',
    block='Лагеря',participation='day_camp',evidence='historical_program',priority=P4,mode='unconfirmed',
    note='Прошедшее окно6July–21August2026 не перенесено на2027. Таблица недель и deadlines отдельна. English сайта не доказывает язык занятия; новая смена и возраст на старт отдельно.')
event('L208','iD Tech Global Academies · Stanford · следующий набор','США','Северная Америка','Stanford campus · residential',
    'https://www.idtech.com/global-academies','Исторический оффер2025:13–17, EnglishB1+; не для6/9',later,later,
    'Следующий подтверждённый global cohort не найден; регистрация для конкретной новой смены не установлена.',
    'AI / Python / NVIDIA Jetson и portfolio project; исторический учебный формат.',
    block='Лагеря',participation='residential',evidence='historical_program',priority=P4,mode='primary',languages=['EN'],
    language='В оффере2025 EnglishB1+ и материалы наEnglish. Mandarin support явно подтверждён; Spanish support расходится между описанием instructors и FAQ.',
    cost='Исторический оффер2025:11 999 USD за13 дней /12 ночей. Это не цена подтверждённой смены2027.',
    note='Верхняя страница всё ещё содержит June22–August15,2025. Коммерческая программа на кампусе не является поступлением или университетским дипломом. Spanish не назначен языком курса по одному описанию персонала.')
event('L209','CodeAI · Mix & Move with AI · учебный проект','Мир','Онлайн / глобально','Онлайн · самостоятельный / родительский урок',
    'https://code.org/es-ES/mix-move-ai','8–18; Beginner; coding + творческий AI-урок',
    'Да по возрасту8–18; вводную сложность оценить','Нет по заявленному8+; младшие coding курсы отдельно L210',
    'Выбрать ES / EN в учебном интерфейсе; это не запись в очный лагерь.',
    'Устройство с браузером; визуальное программирование танца / музыки.',
    block='Лагеря',participation='regular',evidence='program',mode='bilingual',languages=['EN','ES'],
    language='Самостоятельный учебный материал доступен наEnglish / Spanish Latam / Spanish Spain; это не обещание живого преподавателя.',
    cost='Открытый учебный tutorial; не международная конкурсная заявка.',
    note='Пример AI-generations использует заранее созданные и проверенные варианты контента; это учебный механизм, а не live API или собственное обучение модели. Нет даты лагерной смены и медали.')
event('L210','CodeAI · CS Fundamentals · постоянная coding-подготовка','Мир','Онлайн / глобально','Онлайн · courses A–F / Express',
    'https://code.org/es/curriculum/computer-science-fundamentals','GradesK–5; help article указывает4–11; курс подобрать по классу / навыкам',
    'Да как кандидат в elementary coding; модуль и уровень выбрать','Да как кандидат в elementary coding; младший модуль выбрать',
    'Выбрать курс по классу, ES / EN и версию материалов; самостоятельный / родительский формат.',
    'Computer, Chromebook или tablet; Sprite Lab / Play Lab и unplugged задания.',
    block='Лагеря',participation='regular',evidence='program',mode='bilingual',languages=['EN','ES'],
    language='Curriculum прямо указываетEnglish / Spanish Latam / Spanish Spain. Языки конкретной версии проверить; RU из старого help article не автоматически подтверждён.',
    cost='Учебные материалы; коммерческий пансион / очная смена не предоставляются.',
    note='Это вводная постоянная учебная база, не лагерь и не соревнование. После трёх лет опыта может быть слишком просто: использовать диагностику / подходящие задания, не обещать международную награду.')
new[-2]['themes']=['ai','coding','games'];new[-1]['themes']=['coding','games','technology']

def profile(id,name,group,age,ids,summary,hardware,route,requirements,nuances,sources,tags=('teen','university')):
    assert not any(p['id']==id for p in d['league_guide']['profiles'])
    profiles.append(dict(id=id,name=name,group=group,age_summary=age,age_tags=list(tags),summary=summary,
        categories=[dict(name=name,age=age,team='По регламенту конкретного формата; см. карточки',hardware=hardware,
            age_rule='Школьная / возрастная граница относится к указанному источнику, не будущему обещанию',entry=route)],
        event_ids=ids,legacy_ids=[i for i in ids if i.startswith('C')],route=route,hardware=hardware,
        language='Точный язык программы / защиты указан в карточке; EN-страница не равна EN-преподаванию.',
        importance='Специализированный маршрут в мировом / региональном справочнике; не рейтинг всех школ или гарантия медали.',
        strengths=summary,requirements=requirements,nuances=nuances,cost='Тариф, техника и поездка по конкретной карточке; место не подтверждено.',
        award='Различать обучение / участие / оценённую награду / победу. Текущий официальный протокол обязателен.',
        sources=[dict(title=t,url=u,checked='2026-10-01') for t,u in sources],evidence='Первичные страницы прочитаны; ограничения и пробелы указаны в карточках.'))
profile('roboboat','RoboBoat · RoboNation','advanced','High School / College; не младшая6/9 категория',['C885','E136'],
    'Автономное надводное судно: восприятие, навигация и надёжная интеграция.', 'Собственный автономный ASV',
    'Старшая инженерная команда → опубликованная регистрация → документация → очные задачи.',
    ['≥75% full-time students; минимум3 участника в2027.','Разработка и документация — работа команды.'],
    ['Handbook2027 ещё не опубликован.','Открытый kickoff E136 не означает допуск младших в соревнование.'],[('RoboBoat2027','https://roboboat.org/programs/2027/')])
profile('robosub','RoboSub · RoboNation','advanced','High School / College; не младшая6/9 категория',['C886','E137'],
    'Автономная подводная робототехника: сенсоры, управление и испытания.', 'Собственный AUV',
    'Старшая команда → season registration → design documentation → испытание автономии.',
    ['≥75% full-time students; минимум3 в2027.'],['Новая эволюция объявлена, подробности разрабатываются.','Исторический middle-school состав2025 не является правилами2027.'],[('RoboSub2027','https://robosub.org/programs/2027/')])
profile('robotx','RobotX / Virtual RobotX · RoboNation','advanced','High School / College; физический и виртуальный пути',['C887','C889','C890','C891'],
    'Морская автономия нескольких систем; виртуальный путь позволяет изучать алгоритмы без физического флота.',
    'RobotX: multi-vehicle; VRX: simulation environment',
    'Старшая команда → RobotX или отдельный VRX → контрольные этапы своей программы.',
    ['Официальная eligibility обоих прочитанных изданий High School / College.'],
    ['RobotX2026 registration закрыта.','VRX2027 имеет три отдельные даты; это не трёхмесячный лагерь.'],[('RobotX2026','https://robotx.org/programs/2026/'),('VRX2027','https://robotx.org/programs/vrx-2027/')])
profile('suas','SUAS · Student Unmanned Aerial Systems','advanced','Старший инженерный маршрут; возраст2027 уточнить',['C888'],
    'Командная автономная авиация и сложная инженерная миссия.', 'Автономная воздушная система',
    'Подготовленная команда → handbook нового сезона → подтверждённая регистрация.',
    ['Прочитать полноценные правила2027 до определения состава и техники.'],
    ['Даты2027 опубликованы; linked handbook относится к2026.','Для детей6/9 прямой соревновательный путь не установлен.'],[('SUAS: сезоны','https://suas-competition.org/competitions')],tags=['unknown','teen','university'])
profile('igvc','IGVC · Intelligent Ground Vehicle Competition','advanced','Новый возрастной / командный регламент не прочитан',['C892'],
    'Автономные наземные транспортные системы как будущая инженерная специализация.', 'Автономная наземная машина',
    'Объявленные даты → чтение регламента → проверка eligible команды → заявка.',
    ['Младший допуск не подтверждать по одной странице season launch.'],
    ['Детальные правила и registration пока не проверены.'],[('RoboNation: dates2027',launch)],tags=['unknown','teen','university'])
profile('iarc','IARC · International Aerial Robotics Competition','advanced','Возраст / состав нового издания не установлен',['C893'],
    'Исследовательская автономная воздушная робототехника; долгосрочная специализация.', 'Авиационная автономия',
    'Регламент конкретного challenge → институциональная / инженерная команда → заявка.',
    ['Проверить действующий challenge, age / team composition.'],
    ['January–March2027 — окно подачи с неизвестными днями.','Не объявлен открытым детским соревнованием.'],[('RoboNation: season2027',launch)],tags=['unknown','teen','university'])
profile('bric','Barbados Robotics Innovation Challenge','regional','Строго >15 и <30 на1January; не для6/9',['C899'],
    'Инженерный robot project с расчётами и фазами разработки.', 'Hardware-dominant робот; бюджет компонентов ограничен',
    'Design proposal → отбор PhaseII → работа → опубликованный финал.',
    ['Максимум6 в команде.','Правила возраста и регионального входа обязательны.'],
    ['Дедлайн PhaseI прошёл; будущий финал не равен открытому набору.'],[('CSF:BRIC','https://caribbeanscience.org/bric/')])
profile('caribbean-stem','Caribbean STEM Olympiads','regional','13–15 /16–18 /19–21 на01.01; CARICOM citizen или4 года resident',['C900','C901','E135'],
    'Региональные software / robotics проекты; самостоятельная команда или независимый участник.', 'Software либо hardware-dominant проект',
    'Проверка регионального права → preliminaries → финалисты → online защита.',
    ['Возраст начинается с13.','Observer countries не входят в citizenship category.'],
    ['Для6/9 соревнование закрыто; E135 отдельно доступна зрителям.','Не любая международная семейная команда может подать заявку.'],[('CSO2027: текущая программа',cso)],tags=['teen','university'])
profile('coderz','CoderZ League · виртуальная робототехника','international','Исторические Grades4–6 /6–9 /7–12; новый сезон неизвестен',['C902'],
    'Blockly / Python и виртуальные роботы без закупки реального робота.', 'Браузер, интернет, симулятор',
    'Новый подтверждённый season guide → лицензия / team registration → virtual stages.',
    ['Согласовать конкретную школьную категорию и размер команды.'],
    ['Последние датированные Fall / Spring2023; root2022.','FAQ содержит противоречащие старые grade рамки: не считать любой класс одобренным.'],[('Fall: датированная страница','https://competition.gocoderz.com/fall-league/'),('FAQ: старые рамки','https://competition.gocoderz.com/faq/')],tags=['unknown','10-12','teen'])
profile('codeai','CodeAI / Hour of AI · учебная подготовка','ai','K–5 /4–11 дляCS Fundamentals; Mix & Move8+',['E138','L209','L210'],
    'EN / ES учебные материалы для coding и первых AI-проектов, с модулями по классу.', 'Браузер / планшет, иногда unplugged задания',
    'Выбор модуля и версии → самостоятельный проект → дальнейшая соревновательная лига.',
    ['Возраст, язык и сложность конкретного модуля смотреть отдельно.'],
    ['Это подготовка и образовательное событие, не международная лига.','Вводная программа может быть простой после3 лет соревнований.','RU не подтверждён по старому help article, когда текущая языковая страница говорит другое.'],[('CS Fundamentals: curriculum','https://code.org/es/curriculum/computer-science-fundamentals'),('Hour of AI','https://code.org/cs/hour-of-ai')],tags=['6','9','10-12'])

assert len(new)==27 and len(profiles)==10
by_id={e['id']:e for e in new}
for e in new:
    e['format']={'team':'Командное соревнование','individual_or_team':'Индивидуально или команда','visitor':'Образовательное посещение','day_camp':'Дневной лагерь','residential':'Программа с проживанием','regular':'Самостоятельная учебная программа'}.get(e['participation'],e['participation'])
for id in ['C897','C898']:
    by_id[id]['proof']='Проверен фрагмент официальной страницы в поисковом индексе. Полная текущая страница и регламент не прочитаны; условия входа требуют подтверждения.'
for id in ['C900','C901']:
    by_id[id]['age']='13–15 / 16–18 / 19–21 на 01.01.2027; гражданство CARICOM / CARICOM-Associate либо проживание в одной из этих стран 4 года подряд на 1 января'
for id in ['L209','L210']:
    by_id[id]['materials_only']=True
    by_id[id]['language_mode']='materials'
by_id['E138']['related_ids']=['L209','L210']
by_id['C892']['note']='Даты подтверждены в официальном анонсе RoboNation. Детальный регламент IGVC и младший допуск пока не проверены; доступны только сведения анонса.'
d['events']+=new;d['league_guide']['profiles']+=profiles
first=next(p for p in d['league_guide']['profiles'] if p['id']=='first')
first['event_ids']+=['C894','C895','C896','C897','C898'];first['legacy_ids']+=['C894','C895','C896','C897','C898']
first['nuances'].append('Доминиканский overview: Explore6–9 / Challenge9–15; local cutoff нового сезона отдельно. English policy — Caribbean Teams, не автоматическое одобрение México / Costa Rica.')
first['sources'].append(dict(title='FLL-Caribe: местные возрастные / иностранные правила',url=dom_foreign,checked='2026-10-01'))
d['league_guide'].update(version='2026-10-01 · v28',checked='2026-10-01')
for item in d['completeness_audit']['known_backlog']:
    if item.get('name','').startswith('RoboNation RoboSub'):
        item['reason']='v28:RoboBoat/Sub/RobotX/VRX/SUAS/IGVC/IARC добавлены; не все handbook2027 опубликованы. Возраст6/9 в старших форматах не расширен. EU robotics challenges и remaining autonomous leagues ещё не покрыты полностью.'
    if item.get('name','').startswith('Caribbean, Pacific'):
        item['reason']='v28:добавлены записи DOM/JAM/TTO/BRB и региональные CSO; eligibility и новые местные даты частичны. Fiji / Pacific primary child calendars и остальные острова остаются незакрытыми.'
d['completeness_audit']['source_issues'] += [
    dict(name='CoderZ League',status='Fall / Spring датированы2023, root2022, FAQ смешивает2020 /2023 и grade рамки. Новый сезон не объявлен подтверждённым.',official_alternative='https://competition.gocoderz.com/fall-league/'),
    dict(name='iD Tech Global Academies',status='Оффер2025 и13–17; Spanish instructor description расходится с Mandarin-only FAQ. Не смена2027 и не пансион для6/9.',official_alternative='https://www.idtech.com/global-academies'),
    dict(name='BJRC2026',status='Friday15August2026 не совпадает с календарём; новое окно не выведено из старой страницы. Туристический non-CARICOM вход не подтверждён.',official_alternative='https://caribbeanscience.org/barbados-junior-robotics-camp-2026/'),
    dict(name='NIHERST FTC',status='Полная страница отдаёт защитную заглушку; текущий сезон найден в официальном индексе. Прочитанный регламент не заявлен.',official_alternative='https://www.niherst.gov.tt/scipop/first-tech-challenge.html'),
    dict(name='IGVC / IARC',status='Новый season launch объявляет даты / окно; полноценные сайты не прочитаны. Технические ошибки доступа не обойдены отключением проверки сертификата.',official_alternative=launch)]
d['completeness_audit'].update(version=28,checked='2026-10-01',new_ids=[e['id'] for e in new],new_profiles=[p['id'] for p in profiles],updated_ids=[],
    conclusion='Частичный мировой каталог. v28:27 новых записей и10 профилей — автономные RoboNation, четыре карибских страны, EN/ES coding/AI и публичные образовательные события. Старшие / закрытые категории отделены от семейного участия.',
    scope='Мировые и региональные соревнования, будущие автономные системы, карибские местные пути, языки лагерей и самостоятельная подготовка. Полный мировой аудит продолжается.',
    validation={'version':28,'status':'pending'})
seen={s['url'] for s in d['sources']}
for e in new:
    if e['source'] not in seen:d['sources'].append(dict(url=e['source'],title=e['title'],evidence=e['proof']+' '+e['note']));seen.add(e['source'])
path.write_text(json.dumps(d,ensure_ascii=False,indent=2))
rp=ROOT/'data/research-plan.json';r=json.loads(rp.read_text())
r['latest_validation']={'version':28,'status':'local_checks_pending_publication_pending','scope':'27 additions /10 profiles, Caribbean and world autonomous pathways; preserved prior records and top picks.'}
r['requirements'].append(dict(id='world_caribbean_v28',requirement='Мировые автономные конкурсы, новые карибские маршруты и EN/ES учебные / посещаемые программы',status='partial_pass',evidence='27 карточек /10 профилей; старшие gate и stale sources обозначены.',remaining='Действующие регламенты2027, иностранный вход в local FLL, новые camp cohorts, остальные острова / Pacific и мировая полнота.'))
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print('Added27 records /10 profiles; prior events and top picks retained.')
