"""Bounded primary-source pass for UAE, Qatar, Oman and Saudi Arabia."""
import ast, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORK=Path('/Users/pal/.codex/workspaces/stem-family-atlas-work')
path=ROOT/'data/catalog.json';d=json.loads(path.read_text())
assert len(d['events'])==1625 and d['completeness_audit']['version']==42
CHECKED='2026-10-02';new=[];profiles=[];byid={e['id']:e for e in d['events']}
tree=ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text())
for name in ['ref','event','profile']:
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(ROOT/'scripts/expand-oceania-v29.py'),'exec'))
base_event=event;urls={};used=set()
for filename in ['urls-middleeast-v43.json','urls-middleeast-extra-v43.json','urls-middleeast-final-v43.json']:
    urls.update(json.loads((WORK/filename).read_text()))
def u(key):
    used.add(key);return urls[key]
def event(*args,**kwargs):
    mode=kwargs.get('participation','team')
    if mode=='regular':kwargs['participation']='day_camp'
    if mode=='individual':kwargs['participation']='individual_or_team'
    e=base_event(*args,**kwargs);e['region']='Азия'
    if mode=='regular':e.update(participation='regular',format='Регулярные занятия; жильё семьи отдельно')
    if mode=='individual':e.update(participation='individual',format='Индивидуальная работа ребёнка; сопровождение взрослого отдельно')
    return e
def category(name,age,team,hardware,entry,rule='Правило конкретного национального потока; новый сезон проверить отдельно'):
    return dict(name=name,age=age,team=team,hardware=hardware,entry=entry,age_rule=rule)

# Qatar: the linked PDF has explicit 2026 amendments that override broad school labels.
qc=u('qatar_categories');qg=u('qatar_guide')
qrows=[
('C1069','Explore','Grade 2–6; класс, не только возраст','Условно: Grade 2–6 и половина команды катарцы','Нет для текущего младшего маршрута: нужен Grade 2–6','2–4 ученика + coach; минимум половина команды — катарцы. На вводной странице есть противоречивое 2–8; подробное условие 2–4 требует финального подтверждения.','Исследовательский LEGO-проект и презентация; Explore признание проекта отдельно от рейтинговых матчей.'),
('C1070','Discovery','Kindergarten / Grade 1','Нет для обычной возрастной ступени; действующий класс неизвестен','Условно: Kindergarten / Grade 1 и половина команды катарцы','2–4 ученика + coach; минимум половина команды — катарцы; местный школьный канал.','Младший проект / модель; точный набор и правила выбранного выпуска уточнить.'),
('C1071','FIRST LEGO League Challenge','9–16 на дату соревнования','Условно: требуется уже исполненных 9 на дату и местная школьная команда','Нет: младше 9','3–7 учеников + 2 coach; минимум половина команды катарцы. Страница называет government-school teams; право частной / иностранной школы отдельно.','Автономный робот и инновационный проект; локальные правила не заменены международным возрастным диапазоном.'),
('C1072','VEX IQ','8–14; primary / preparatory','Условно: подходит по возрасту, местная школа / набор и иностранный допуск отдельно','Нет: младше 8','Школьная категория VEX IQ; точный размер команды и нынешнее правило резидентства / школьного отбора не установлены.','VEX IQ, матч и программирование; иностранная национальная квота не подтверждена.'),
('C1073','Sumo Beginner','9–12 по PDF, стр.51; Advanced 13–18','Условно: исполненные 9 и подтверждённая школьная команда','Нет: младше 9','PDF: 2–4 ученика + coach. Overview пишет 2 ученика и широкую primary ступень; конкретное обновление 2026 имеет более строгий возраст.','LEGO или VEX IQ; максимум 2.5kg, 20×20cm, высота 30cm при старте; регламент нового сезона отдельно.'),
('C1074','Line Tracing Beginner','8–12 по PDF, стр.89; Advanced 12–18','Условно: возраст подходит, местный / зарубежный допуск отдельно','Нет: младше 8','PDF: 2–3 участника. Overview пишет 2 + coach; итоговый состав требует подтверждения организатора.','Поправка 2026 заменяет VEX на mBot; нельзя привезти привычный набор, не проверив местное техническое правило.'),
('C1075','Ball Collect Beginner','8–13 по PDF, стр.69; Advanced 13–18, не университет','Условно: по возрасту подходит; команда / местный допуск отдельно','Нет: младше 8','Overview: 2 ученика + coach, до двух команд от школы; технический пакет уточняет возраст 8–13.','Автономный сбор цветных шаров; в Beginner фиксированное размещение, в Advanced рандомизация.'),
('C1076','Innovation Beginner','10–14 по поправке PDF, стр.43; Advanced 15–18','Нет сейчас: минимум 10; возможный будущий маршрут после проверки даты','Нет: минимум 10','PDF: Beginner 2–4 + coach; overview 1–2 без coach относится к иной / старой редакции. Использована более конкретная поправка 2026.','Работающий инженерный проект, исследование / программирование и защита; ежегодная тема устанавливается ассоциацией.'),
('C1077','Robot Arm','Сайт 12–18; связанный PDF, стр.3 — 10–18','Нет сейчас при обеих найденных редакциях; младше 10','Нет сейчас при обеих найденных редакциях','2 участника + coach. Конфликт нижней границы 10 / 12 не разрешён новым локальным письмом.','Автономная первая и управляемая вторая фазы; роботическая рука 30×30cm по связанному PDF.')]
for id,name,age,mat,osc,entry,gear in qrows:
    e=event(id,'Qatar Robotics & AI · '+name,'Катар','Doha · местный школьный отбор; следующий venue уточнить',qc,age,mat,osc,entry,gear,scope='national',
        priority='P4 — сейчас возраст не подходит' if id in ['C1076','C1077'] else 'P2 — местная школа и иностранный допуск требуют проверки',evidence='program',
        note='Даты следующего выпуска не объявлены в прочитанных материалах. Технический PDF ©2025 содержит отдельные поправки сезона 2026; их нельзя автоматически считать правилами 2027. Половина катарцев прямо указана для Explore / Discovery / FLL; не распространена без доказательства на остальные категории. Семейная туристическая заявка и национальная мировая квота не подтверждены.')
    e.update(period='Следующий сезон не датирован; прочитаны категории и поправки 2026',admission_kind='national_school',references=[ref('Связанный технический PDF: страницы и противоречия',qg)])
profile('qatar-robotics-ai','Qatar Robotics & AI · национальный школьный маршрут','national','Discovery KG/Grade1; Explore Grade2–6; FLL9–16; VEX IQ8–14; технические Beginner8/9+',
    'Это школьный национальный маршрут. Для обоих сначала нужны класс, местная школа, состав команды и право иностранного участника; туристический возрастной допуск не установлен.',
    [category('Discovery','KG / Grade1','2–4 +coach','Младший проект','Минимум половина команды катарцы'),category('Explore','Grade2–6','2–4 +coach; вводное 2–8 конфликтует','LEGO-проект','Минимум половина команды катарцы'),category('FLL Challenge','9–16 на дату','3–7 +2coach','Робот / innovation','Половина катарцы; government-school channel'),category('VEX IQ','8–14','Текущий состав уточнить','VEX IQ','Местная школьная категория'),category('Sumo / Line / Ball','9–12 /8–12 /8–13','PDF 2–4 /2–3 /overview2','LEGO/VEX IQ /mBot /ball robot','Поправки 2026 стр.51/89/69'),category('Innovation / Arm','10–14 /конфликт10–18vs12–18','2–4+coach /2+coach','Проект /роборука','Для детей6/9 сейчас не подходят')],
    [r[0] for r in qrows],['Местная школа и класс → действующий регламент → команда → national event → только подтверждённая квота Arab / World.'],
    ['Не менее половины катарцев в Explore / Discovery / FLL.','Уточнить конкретную школу, coach и иностранное представительство.','Новый школьный год и технический пакет 2027 ещё не установлены.'],
    ['PDF поправки с числовым возрастом имеют преимущество перед общим primary label.','VEX/Line/Sumo нельзя объединить в одну платформу.','Класс и точный день рождения нужны там, где считается возраст на дату.'],[('Организатор: категории',qc),('Технический PDF',qg)])

# UAE school-nominated challenge: submission is closed, November is only a month.
jb=u('jic_brief');jr=u('jic_rules');jf=u('jic_faq');jt=u('jic_tasks')
jrows=[('C1078','Category A','KG1–KG2','Нет при обычной возрастной ступени; класс неизвестен','Условно: только если школа подтверждает KG1–KG2','Коммуникация, логика и совместная творческая задача'),('C1079','Category B','Grade1–2','Условно только при Grade1–2; класс не установлен','Условно только при Grade1–2; класс не установлен','Логика, индивидуальная работа и групповое создание / презентация'),('C1080','Category C','Grade3–4','Условно только при Grade3–4; класс не установлен','Нет при обычной младшей ступени; нужен Grade3–4','Индивидуальная задача, групповая инженерия и рефлексия')]
for id,name,age,mat,osc,gear in jrows:
    e=event(id,'Junior Innovators Challenge UAE 2026 · '+name,'ОАЭ','Abu Dhabi · финальная площадка не указана в прочитанном пакете',jb,age,mat,osc,
        'Номинация через государственную или частную школу UAE; ребёнок зачислен в школу на дату регистрации. Самостоятельной туристической подачи нет. В government-school nomination 4 из5 должны быть Emirati.',gear,scope='national',priority='P4 — номинация 2026 уже закрыта',themes=('technology','coding'),languages=('EN','AR'),language='Номинационное видео допускается на английском или арабском; язык очных задач отдельно.',evidence='event_page',
        note='Регистрация 21мая–20сентября2026 завершена. Shortlist12октября относится к уже номинированным, не новому приёму. Очная фаза в ноябре2026 без точных дней; 150 selected +30 резерв. Каждая школа номинирует до5 в каждой из3 категорий. Это общий STEM challenge, не гарантированно робототехнический матч.')
    e.update(period='Ноябрь2026; точные дни очной фазы неизвестны. Приём закончился20сентября.',admission_kind='national_school',references=[ref('Соглашение / школьная номинация',jr),ref('FAQ: этапы и закрытый приём',jf),ref('Задачи по классам',jt)])
profile('jic-uae','Junior Innovators Challenge · UAE','national','KG1–KG2 /Grade1–2 /Grade3–4; школьные категории',
    'Младшие STEM-задачи по классам; семья не может заменить номинацию школы. Приём2026 закрыт, следующий сезон не объявлен.',
    [category('A','KG1–KG2','Индивидуальная и групповая части','Креативные задачи','Номинация UAE school'),category('B','Grade1–2','Индивидуальная и групповая части','Логика /инновация','Номинация UAE school'),category('C','Grade3–4','Индивидуальная и групповая части','Инженерный проект','Номинация UAE school')],
    [x[0] for x in jrows],['UAE school enrolment → nomination → review → shortlist → November on-site tasks.'],
    ['Школа подтверждает нынешний класс и зачисление.','До5 учеников в каждой категории от школы.','Срок нового приёма и семейное сопровождение отдельно.'],
    ['EN/AR video не доказывает тот же язык каждого очного задания.','12октября — shortlist, не deadline регистрации.','Общий STEM конкурс не является роболигой.'],[('Пакет challenge',jb),('Правила',jr),('FAQ',jf)])

# Oman: local Kids is explicitly outside the official world qualification.
ow=u('oman_season');og=u('oman_guide');cr=u('cheltenham_results')
orows=[('C1081','WRO Kids','6–9; местная неофициальная мировая категория','Условно: возраст подходит; следующий сезон и school/foreign entry отдельно','Условно: возраст подходит; следующий сезон и school/foreign entry отдельно','WeDo2.0, SPIKE Essential или VEX Go; местная задача; не переносить правила RoboMission'),('C1082','RoboMission Elementary','8–12; сезон2026: родившиеся2014–2018','Условно: 2017 в диапазоне; национальный иностранный допуск отдельно','Нет:2020 ниже Elementary','Автономные миссии; национальный вариант2026 имеет фиксированную расстановку, без international randomization'),('C1083','Future Innovators Elementary','8–12; сезон2026: родившиеся2014–2018','Условно:2017 в диапазоне; foreign quota и следующий сезон отдельно','Нет:2020 ниже Elementary','Инженерный проект; сертификаты WRO Learn Future Innovators /Ready for Season2026 требуются до judging')]
for id,name,age,mat,osc,gear in orows:
    e=event(id,'WRO Oman · '+name+' / следующий сезон','Оман','Muscat · национальный финал2026 hosted by Cheltenham Muscat',og,age,mat,osc,
        '2–3 ученика + coach; OMR10 за участника в руководстве2026. Иностранный туристический вход / резидентство и национальная мировая квота прямо не подтверждены.',gear,scope='national',evidence='historical_program',
        note='Регистрация2026:21февраля–31марта; Nationals6июня2026 уже прошёл. Даты и пакет2027 не объявлены в прочитанных источниках. WRO Kids6–9 прямо не является официальной international категорией и не даёт путь в World Final. National win /qualification не равны мировой победе.',cost='OMR10 за участника по пакету2026; новый тариф неизвестен.')
    e.update(period='Следующий сезон не датирован; Nationals6июня2026 — архив',admission_kind='national_school',historical_editions=[dict(start='2026-06-06',end='2026-06-06',note='Архив национального финала2026; не следующий набор',source=ow)],references=[ref('Регистрация, категории и guide',ow),ref('Школьный отчёт national2026',cr)])
profile('wro-oman','WRO Oman · Kids и мировой отбор','national','Kids6–9; Elementary8–12; Junior11–15; Senior14–19',
    'Младший Kids подходит обоим по возрасту, но не ведёт на мировой финал. Матвей отдельно рассматривает Elementary через национальные правила; иностранное представительство ещё не подтверждено.',
    [category('WRO Kids','6–9','2–3 +coach','WeDo2/SPIKE Essential/VEX Go','Локальный турнир; нет World Final qualification'),category('RoboMission Elementary','8–12','2–3 +coach','Автономные миссии','National2026 без randomization'),category('Future Innovators Elementary','8–12','2–3 +coach','Робопроект /WRO Learn','Сертификаты перед judging'),category('Junior /Senior','11–15 /14–19','2–3 +coach','По выбранной дисциплине','Будущая ступень; новый пакет отдельно')],
    [x[0] for x in orows],['Kids: местная практика.','Elementary: national registration → national result → подтверждённая квота World /Open.'],
    ['Coach и команда2–3; одно участие ученика в одной команде.','Подтвердить foreign /resident условия и право квоты.','Учебные сертификаты FI, оборудование и взнос согласно новому пакету.'],
    ['Возрастные годы2026 не выданы за2027.','Местный Kids не равен мировому чемпионату.','65 зарегистрированных команд и список школ не являются протоколом мировых призов.'],[('2026 official guide',og),('Национальный оператор',ow)])

# Saudi official Mawhiba page: two students for physical categories, one for local virtual.
sm=u('saudi_mawhiba')
srows=[('C1084','RoboMission Elementary','2ученика +coach','Автономный робот и миссии; national-to-world route только после допуска'),('C1085','Future Innovators Elementary','2ученика +coach','Робопроект с решением социальной /экологической проблемы'),('C1086','Local Sumo Elementary','2ученика +coach','Местное сумо; international WRO category /World quota не обещаны'),('C1087','Local Virtual RoboMission Elementary','1ученик +coach','Местная виртуальная программная задача; solo не означает прямой мировой отбор')]
for id,name,team,gear in srows:
    e=event(id,'WRO Saudi Arabia / Mawhiba · '+name,'Саудовская Аравия','Национальная платформа; venue финала отдельно',sm,'Elementary8–12; Junior11–15; Senior14–19',
        'Условно:2017 подходит по возрасту; новый набор / national representation отдельно','Нет:2020 младше8',
        team+'. Interest registration → introductory session → coach activates team on wrosaudi.com. Допуск иностранца / туристической семьи в national squad прямо не установлен.',gear,scope='national',
        priority='P4 — приём2026 закрыт; следующий сезон неизвестен',evidence='historical_program',participation='individual' if id=='C1087' else 'team',
        note='Прочитана официальная страница Mawhiba. Приём24августа–7сентября2026 закрыт, remote qualifiers20сентября, national final mid-October без точного дня. Не присвоено15октября. Local Sumo /Virtual и университетская18–22 ветка не представлены как World Final disciplines.')
    e.update(period='National2026: серединаоктября, точный день неизвестен; новый набор не объявлен',admission_kind='national_school')
profile('wro-saudi','WRO Saudi Arabia · Mawhiba','national','Elementary8–12; Junior11–15; Senior14–19; local university18–22',
    'Для Матвея найден Elementary, для Оскара опубликованные WRO категории начинаются слишком поздно. Приём2026 закрыт; открытая иностранная семейная заявка не доказана.',
    [category('RoboMission /Future Innovators','8–12 /11–15 /14–19','2+coach','Миссии /проект','Национальная активация coach'),category('Local Sumo','8–12 /11–15 /14–19','2+coach','Sumo robot','Местная категория'),category('Local Virtual','8–12 /11–15 /14–19','1+coach','Виртуальная задача','Местная категория'),category('Future Engineers /RoboSports','14–19 /11–15,14–19','2+coach','Авто /теннис','Не младшие6/9 категории')],
    [x[0] for x in srows],['Mawhiba interest → introductory session → national platform → qualifier → national final → только подтверждённая World quota.'],
    ['Текущий приём и статус иностранной семьи уточнить.','В физических категориях указано2 ученика; глобальное2–3 не перенесено.','Виртуальная local category:1+coach.'],
    ['Mid-October не стал датой15октября.','Регистрация интереса не равна активации команды.','Local award / university branch не выданы за детский World Final.'],[('Mawhiba: категории, состав и сезон',sm)],age_tags=('9','10-12','teen'))

ph=u('pma_hack')
e=event('C1088','Pure Minds / Boeing · Inter-School AI Hackathon2026–2027','ОАЭ','Школьные heats по UAE; venue Grand Final не установлен',ph,'14–16; все UAE schools','Нет:младше14','Нет:младше14',
    '1–2 ученика; до10команд от школы. Программа для UAE schools, регистрация школы; не туристическая семейная заявка.',
    'Построить AI app по общему brief в один день, затем представить жюри; предварительный код не допускается.',scope='national',participation='individual_or_team',priority='P4 — будущая подростковая ступень',cost='Участие бесплатно по FAQ; поездка и школа отдельно.',themes=('ai','coding'),
    note='Interest Sept–Nov2026, heats Oct–Nov2026, finalists December2026, Grand Final January2027; точных дней нет. No coding prerequisite не отменяет возраст14–16. Participation certificate отличается от top-three trophies/device prizes.')
e.update(period='Heats октябрь–ноябрь2026; Grand Final январь2027 без точных дней',admission_kind='national_school')

# Learning: distinguish explicit instruction, staff language support and old camps.
ft=u('fun_term')
e=event('L387','Fun Robotics Dubai · текущий STEM term и младшие группы','ОАЭ','Dubai · Al-Wasl Centre, Sheikh Zayed Road',ft,'6–16; уровень beginner–advanced',
    'Условно:9лет в общем диапазоне; Robotics Fun Club7–9 или3D8+ требуют текущего подтверждения','Условно:6лет в общем диапазоне; SPIKE Essential6–7 требует текущего подтверждения',
    'Сначала пробное занятие и конкретный EN-поток по уровню после трёх лет опыта; 5–15 детей в группе. Место / current FLL team не гарантированы.',
    'Robotics, coding, AI, games,3D, electronics/IoT; overview прямо предлагает Arabic & English.',block='Лагеря',participation='regular',languages=('EN','AR'),language='Билингвальные STEM-программы Arabic & English прямо заявлены; конкретную долю EN и группу подтвердить.',evidence='program',
    note='Current header:TERM1,5сентября–12ноября2026. Ниже остался TERM2 /Ramadan с группами Essential6–7, FunClub7–9, Prime10–12,3D8+, Minecraft8–10. Эти старые часы не перенесены на нынешний term. Join competitions like FLL — предложение пути, не доказательство текущего результата.')
e.update(language_mode='bilingual',period='Текущий TERM1:5сентября–12ноября2026; слоты текущей группы уточнить',date_scope='season_window',language_certainty='EN/AR прямо указаны для технических программ; конкретная группа /уровень отдельно.')
us=u('uwr_summer');uf=u('uwr_faq')
for id,name,age,mat,osc in [('L388','Cadets','5–7','Нет:9лет выше диапазона','Условно:6лет подходит в архивном потоке; новый набор неизвестен'),('L389','Pioneers','8–11','Условно:9лет подходит в архивном потоке; новый набор неизвестен','Нет:6лет ниже диапазона')]:
    e=event(id,'Unique World Robotics · Summer2026 '+name+' / архив','ОАЭ','Dubai · конкретный кампус /cohort уточнялся оператором',us,age,mat,osc,
        'Дневной поток, laptop/tablet, notebook,chargers,еда и вода. Новая смена2027 /winter и язык преподавания не установлены.',
        '9недель themed AI/robotics/coding/engineering/game projects; разные глубины Cadets/Pioneers.',block='Лагеря',priority='P4 — архивлетнейсмены',evidence='historical_program',themes=('robotics','coding','ai','games'),
        note='July–August2026 уже прошли. Маркетинговое enrolling now не стало действующим октябрьским набором. FAQ описывает оборудование, возраст и запись, но не подтверждает технический EN. EN Spring2026 другого продукта не перенесён на summer или будущую смену.')
    e.update(period='Июль–август2026; архив, новый поток не объявлен',references=[ref('FAQ: возраст /устройство /cohort',uf)])
ps=u('pure_summer')
for id,name,age,mat,osc,gear in [('L390','Little Explorers','4–6','Нет:выше6','Условно:6лет в архивном диапазоне; новый набор неизвестен','SPIKE Essential,WeDo2,KUBO,mTiny,ScratchJr'),('L391','Future Ready','7–9','Условно:9лет в архивном диапазоне; новый набор неизвестен','Нет:ниже7','Роботы, инженерия, Python и AI game week')]:
    e=event(id,'Pure Minds Dubai · Summer2026 '+name+' / архив','ОАЭ','ПятьDubaiплощадок, включаяMuseumoftheFuture',ps,age,mat,osc,
        'Новые dates/cohort и technical EN отдельно; Museum venue бронируется самим музеем, не общим camp form.',gear,block='Лагеря',priority='P4 — архивлетнегонабора',evidence='historical_program',themes=('robotics','coding','ai'),
        note='Прочитана текущая summer2026 page:6июля–28августа,Mon–Fri9:30–14:00. Период уже прошёл; язык EN прямо не указан. Museum ticket сам по себе не зачисление в STEM camp. Даты2027 не объявлены.')
    e.update(period='6июля–28августа2026; архив /nextcohortunknown',historical_editions=[dict(start='2026-07-06',end='2026-08-28',source=ps,note='Прошедшее окно летней программы')])
lf=u('lafolie_camp')
e=event('L392','La Folie × HandPrint · October camp со STEM и робототехникой','ОАЭ','Dubai · Al Wanes Street,Umm Suqeim1',lf,'Выбраннаягруппа6–12; отдельная3–5 не использована',
    'Условно:9лет подходит; EN технического занятия и место подтвердить','Условно:6лет подходит; EN технического занятия и место подтвердить',
    'Запись на неделю или выбранный день. Общая команда coaches говорит English/Arabic/French; язык именно Robotics session ещё не подтверждён.',
    'Смешанные arts,sports,STEM. В расписании6–12 HandPrint Robotics12октября12:15–13:00 и16октября11:30–12:15:90мин за неделю, не20часов робототехники.',
    block='Лагеря',start='2026-10-12',end='2026-10-16',priority='P3 — смешаннаясмена; technicalEN уточнить',date_scope='camp_window',
    language='English/Arabic/French прямо заявлены как языки большинства coaches; это поддержка, не доказанный основной язык Robotics.',
    cost='После28сентября:AED1350/ребёнок/неделя или290/день +5%VAT. Двое за полную неделю:AED2835 сVAT до дополнений. Earlybird1280 закончился27сентября.',
    note='Mon–Fri9–13; жильё семьи отдельно. По опубликованному расписанию робототехника дважды по45мин. Третьему sibling5%discount; для двух детей скидка не применена. Поддержка EN классифицирована отдельно от технического EN, пансион не заявлен.')
e.update(language_mode='support',support_languages=['EN','AR','FR'],language_support_scope='Большинство coaches оператора; конкретный Robotics coach /поток отдельно',period='12–16октября2026,9–13Dubai; robotics12и16октября',
    technical_sessions=[dict(date='2026-10-12',start_time='12:15',end_time='13:00',timezone='Asia/Dubai'),dict(date='2026-10-16',start_time='11:30',end_time='12:15',timezone='Asia/Dubai')])
pt=u('pma_saturday')
for id,name,age,mat,osc,gear in [('L393','Little Explorers','4–6','Нет:выше6','Условно:6лет подходит; язык и уровень отдельно','SPIKE Essential,моторы,сенсоры и инженерные задачи'),('L394','Future Ready','7–9','Условно:9лет подходит; язык и уровень отдельно','Нет:младше7','Роботы,3Dинженерия и AI for Young Minds'),('L395','FIRST LEGO League team stream','10–14 по программеоператора','Нет сейчас:оператор начинает этот поток с10; будущий кандидат','Нет:младше10','FLL робот, innovation project и judging;10–14localstream не заменён глобальным9–16')]:
    e=event(id,'Pure Minds Dubai · Saturday '+name, 'ОАЭ','Rove Downtown /Studio One,Dubai; конкретныйслот отдельно',pt,age,mat,osc,
        'Согласовать текущий90минутныйпрограммныйслот, technical language и место. Current header12сентября–14ноября2026; FLLслот требует seasoncommitment.',gear,
        block='Лагеря',participation='regular',priority='P4 — будущаявозрастнаяступень' if id=='L395' else 'P2 — регулярныйкандидат, языкподтвердить',themes=('robotics','coding','ai'),evidence='program',
        cost='Current header:AED1150per child per program,excl.VAT; sibling15%secondchild. Late-start,numberofsessions и итоговыйсчёт отдельно; старые595/NCFE2024 не использованы.',
        note='ТекущийTERM1header2026 имеет актуальныевозрасты иvenues. Нижняя часть страницы содержит TERMII2025,MediaOne иNCFE2024: эти старые даты /слоты не перенесены. Englishinstruction прямо не найден. FLLteamoffer не является доказательством мирового результата.')
    e.update(period='По субботам TERM1,12сентября–14ноября2026; текущий90минутныйслот подтвердить',date_scope='season_window')

# Correct two existing Dubai/Abu Dhabi camps rather than creating duplicates.
e=byid['L039'];e.update(checked=CHECKED,source=u('robogenz_camp'),languages=[],support_languages=[],language_mode='unconfirmed',
    language='Язык technicalinstruction не указан; Englishwebsite не доказывает ENлагерь.',language_certainty='ENтег снят до прямого подтверждения преподавания.',
    priority='P4 — архивлетнего2026набора',period='6июля–21августа2026,9–12; следующийнаборнеобъявлен',start='',end='',date_status='Не объявлено',evidence_level='historical_program',
    age='Лето2026:6–8 /9–15; новыегруппы отдельно',note='Прочитана actualsummerS2page. Summer2026закончился; новыйwinter/2027набор и языкнеустановлены.',references=[ref('Оператор: текущиесобытия',u('robogenz_events'))])
e=byid['L040'];e.update(checked=CHECKED,source=u('uwr_spring'),languages=['EN'],support_languages=[],language_mode='primary',
    language='Spring2026: прямоTaught in English. Это подтверждение архивного продукта; новые summer/winterпотоки отдельно.',language_certainty='ПрямойENдляSpring2026, не универсальнаяполитикаоператора.',
    priority='P4 — архивSpring2026',period='Spring2026;8учебныхдней, точныедатынановойстраниценеустановлены',start='',end='',date_status='Не объявлено',evidence_level='historical_program',
    age='Spring2026:Junior6–9 /Senior10+; nextcohortunknown',note='Двапроектныхэтапа,8дней. АрхивныйEnglishподтверждён; будущиедаты и место не объявлены. Не выдано за открытый октябрьский приём.')

# International expos: exact current dates, separate child gates.
ns=u('northstar');ai=u('ai_everything');af=u('ai_faq');ws=u('qatar_websummit');wv=u('qatar_venue');wt=u('qatar_websummit_terms')
for id,title,country,city,source,start,end,gear in [
    ('E173','Expand North Star2026','ОАЭ','Dubai Exhibition Centre,Expo City',ns,'2026-12-08','2026-12-10','Startups,AI,ventureecosystem ипредпринимательство'),
    ('E174','AI Everything Abu Dhabi2026','ОАЭ','ADNEC Centre,Abu Dhabi',ai,'2026-10-06','2026-10-07','AIenterprise,humanoids,agents,cloud/startups; взрослыеworkshops/hackathonотдельно'),
    ('E175','Web Summit Qatar2027','Катар','Doha Exhibition and Convention Center(DECC)',ws,'2027-01-31','2027-02-03','Techstartups,AI,робототехнологии/entrepreneurship; не детскийcontest')]:
    e=event(id,title,country,city,source,'Возрастпосетителя6/9 требуетотдельногодопуска','Условно:детскийвходнеподтверждён','Условно:детскийвходнеподтверждён',
        'Выбрать visitorbadge иполучить правило именно текущего выпуска для детей6/9; studentbadgeне является автоматическидетскимбилетом.',gear,block='События',start=start,end=end,scope='international',participation='visitor',priority='P3 — взрослыйвизит, детейуточнить',themes=('ai','technology','robotics'),
        note='Даты подтверждены первичныморганизатором. Наличиекомпаниинаспонсорскойстранице не гарантирует стенд. Наградапосетителю не обещана; детскаярегистрация не принята.')
    e.update(exhibition_tier='global',visitor_policy='confirm_children',visitor_policy_note='Правило6/9летне установлено; необходим ответ по конкретному выпуску.',adult_entry=e['entry'],highlights=[gear],exhibitor_note='Экспонентскийсписок проверять перед поездкой; все мировые компании не обещаны.',exhibitor_directory_url=source,level='Международная профессиональная tech-площадка; редакционная оценкамасштаба')
bynew={e['id']:e for e in new}
bynew['E173']['note']='8–10декабря2026,DubaiExhibitionCentre,ExpoCity,прямонаhome. GITEXExpo8–11декабря—отдельноеокно. СтарыйDubaiHarbour2025неперенесён. Детскийвходнеустановлен.'
bynew['E174'].update(references=[ref('FAQ:даты/ADNEC/EN',af)],languages=['EN'],language='FAQпрямоуказываетEnglishдляconferencesandcommunication.',
    note='FAQbodyиhomepage:6–7октября2026,ADNEC. FAQtitle5–7устарел; navigationExhibit2027не являетсядатой2027. Openinghoursнаhomeиразныхблокахрасходятся:точныйticket/slotподтвердить. Детскийвходнеподтверждён; studentpassнесталбилетом6/9.')
bynew['E175'].update(priority='P4 — QatarFAQ18+; детскаяисключительнаяквотане подтверждена',
    visitor_policy_note='QatarlocalVenueFAQ:over18. ОбщиеTerms§5.1 допускают youth4–17,но§5.1.3 оставляет решениекаждомуevent/year/location; исключениедляQatar2027неполучено.',
    note='Jan31–Feb3,2027,DECC подтверждены. YouthTicketв общихTerms не является разрешениемQatar6/9. Пока localFAQ18+ не изменён/исключение не подтверждено, не включён в семейный календарь. Во взросломкалендаревыставокостаётся.',references=[ref('QatarvenueиlocalchildFAQ',wv),ref('ОбщиеTerms§5.1 /5.1.3',wt)])
mv=u('museum_visit')
e=event('E176','Museum of the Future · семейная технологическая экспозиция','ОАЭ','Dubai · Museum of the Future',mv,'Семейныепосетители;4+платныйбилет,младше4free','Да по возрасту посетителя; ticket slot отдельно','Да по возрасту посетителя; ticket slot отдельно',
    'Датированныйвременнойбилет каждому; посещениесродителем. Daily10–19,lastentry17; availability конкретногослота отдельно.',
    'Постояннаяэкспозиция будущихтехнологий иинтерактивныезоны; это музей, не международнаяторговаявыставкавсехкомпаний.',block='События',scope='local',participation='visitor',priority='P3 — семейныймузейпридобнойпоездке',themes=('ai','technology','robotics'),
    cost='Текущаястраница:AED169/посетитель4+; оба ребёнкаAED338. Пример2взрослых+2детей:AED676до дополнений. Младше4freeнепримененоОскару.',note='Круглыйгод; конкретныеднислотане выбраны иICSдата не придумана. Ticketmuseumне означает campenrolment илисоревновательнуюнаграду.')
e.update(period='Постоянная экспозиция; дату /время посещения выбираетсемья',exhibition_tier='family_alternative',visitor_policy='family',visitor_policy_note='Официальнаястраницапрямоописываетдетскиебилеты;6/9в платнойкатегории4+.',adult_entry=e['entry'],highlights=['Интерактивнаясемейнаяэкспозициябудущего'],exhibitor_note='Музейнаяэкспозиция; реестркомпанийторговойвыставкинеприменим.',exhibitor_directory_url=mv)
e=byid['E018'];e.update(checked=CHECKED,source=u('gitex'),start='2026-12-08',end='2026-12-11',date_status='Подтверждено',city='Dubai Exhibition Centre,Expo City',
    note='Currenthomepage:Summit7декабря2026,Expo8–11декабря. СтарыйpresentationPDFNovember9–13неиспользован. Currentchildpolicy6/9неустановлена; старыйstudent16+несталправилом2026.',visitor_policy='confirm_children',visitor_policy_note='Детскийвход6/9текущегоизданиянеподтверждён.',references=[ref('Текущиетермины,числовойдетскийдопускне найден',u('gitex_terms'))])
e=byid['E108'];e.update(checked=CHECKED,source=u('leap'),start='2027-04-12',end='2027-04-15',date_status='Подтверждено',
    note='Homepageобъявляет12–15апреля2027,RECCMalham. ПоследнийопубликованныйFAQbodyещёсдатами2026,нопрямо18andover,childrennotpermitted,nochildpasses. Правила2027отдельно; текущийadultgateсохранён.',references=[ref('ОпубликованныйFAQ:18+,бездетскихбилетов',u('leap_faq'))],visitor_policy='adults_only',priority='P4 — детямнельзя,взрослыймаршрут',visitor_policy_note='ПоследнийопубликованныйFAQ:18+;детинедопускаются. Nexteditionpolicyотдельно.')

# Two school dossiers: one national result, one explicit English PYP STEAM option.
def school(id,name,iso,country,city,curriculum,ages,instruction,language_note,programme,results,sources,boarding='unknown',boarding_note='Пансионмладших6/9неподтверждён',cost='Актуальныйсчётдляобоихиextrasнеполучен'):
    s=dict(id=id,name=name,iso=iso,country=country,region='Азия',city=city,school_type='private',curriculum=curriculum,ib_programmes=[],ages=ages,instruction_languages=instruction,language_note=language_note,
        fit=dict(mat='candidate',osc='candidate',note='Школьнаямладшаяступеньесть; текущиекласс,место,наставникикомандуотдельно.'),boarding=boarding,boarding_note=boarding_note,programme=programme,labs='Конкретнаяплатформа иеженедельныечасыдляобоихнеустановлены.',ai='МладшийобязательныйAIтрек не подтверждён.',results=results,evidence='national_result' if results else 'programme',
        admissions='Подтвердитькласс,текущееместо,языковуюадаптациюидоступвнужнуюкоманду; школьноезачислениене гарантируетсоревновательныйсостав.',cost=cost,
        questions=['Какиеточныеклассы,местаязыковаяадаптациядляобоих?','Какойcurrentjuniorcoach,teamcode,платформа,часыиотбор?','Какиепротоколыпоследнихтрёхсезоновименноначальнойступени?','Какойполныйсемейныйсчёт иforeignnationalqualificationgate?'],sources=[dict(title=t,url=url,claim=c,kind='school',checked=CHECKED) for t,url,c in sources],checked=CHECKED,priority=2,research_status='partial',verification='Прочитанышкольныепервичныеисточники;безутверждениямировогорейтинга.')
    d['schools'].append(s);return s
cc=u('cheltenham_curriculum');cf=u('cheltenham_fees')
tri=dict(league='WRO',season='2026',stage='OmanNationalFinal6июня2026',award='1-еместоFutureInnovatorsJunior;qualificationWorld2026',team='TriAxis',source=cr,provenance='school_report',note='Grade9результат,непротоколмировойпобедыине младшаякоманда6/9.')
school('S042','Cheltenham Muscat','OMN','Оман','Muscat','Britishcurriculum;KG,Prep,IGCSE/A-level;IBне установлен','KG1–Grade12;primaryклассыопределяетшкола',[],
    'ПрочитаныEnglish/ArabiccoreиEALссылка,ноявныйосновнойязыквсехпредметоввэтихстраницахнеустановлен;ENне присвоенавтоматически.',
    'ШколаhostedWROOman2026:65команд14школ/университетов;11школьныхкоманд,включаяKids/Elementary/FIJunior. ПризTriAxisGrade9не доказывает нынешнююElementaryкомандупризовогоуровня.',[tri],
    [('ШкольныйотчётWRO2026',cr,'NationalFIJuniorпобеда;отдельнаяквалификацияWorld'),('Учебнаяступень',cc,'KG/Prep/IGCSE;ICTвпрограмме'),('Опубликованныетарифы',cf,'Grade1–3OMR5013;Grade4OMR5517;тарифныйгодвпрочитаннойтаблицене указан')],
    cost='Опубликованнаятaблица:Grade1–3OMR5013/год,Grade4OMR5517;примерGrade1+Grade4=OMR10530tuition,еслиэтиклассыпodтвердятся. Тарифныйгод,зачисление,transport/clubs/extrasиперсональныйсчётнужныотдельно.')
sp=u('sisd_primary');sb=u('sisd_boarding');sf=u('sisd_facilities')
s=school('S043','Swiss International Scientific School Dubai(SISD)','ARE','ОАЭ','Dubai · Al Jaddaf',
    'IBPYPGrade1–5;EnglishSTEAMstreamилиbilingualEN/FR,EN/DE', 'Primary6–11поexplicitpage;Grade1–5', ['EN'],
    'EnglishSTEAMstreamпрямоучитсянаEN;FR/DEдополнительныеязыки. Этошкольныйпоток,неподтверждениеENсоревновательногокружка.',
    'PYP STEAMstream,MIT-themedlearningchallenges;science/designfacilities. CurrentWRO/VEX/FLLjuniorteamcodeиworldpodiumнеустановлены.',[],
    [('PrimaryEnglishSTEAM',sp,'ПрямойENinstructionдляPrimary6–11'),('Facilities',sf,'Учебныепространства;наградинет'),('Boardingoptions',sb,'ПансионстартуетсGrade6;неусловиедляPrimary6/9')],boarding='yes',boarding_note='Full/weekly/flexi,начинаясGrade6. Детям6/9здесьрассматриваетсядневнаяшкола;возрастпансионане заменённа11безуточнениякласса.')
s['ib_programmes']=[dict(programme='PYP',status='school_report')]
h=d['school_history'];h['checked']=CHECKED
h['entities'].extend([dict(id='OMN-CHELTENHAM-TRIAXIS',name='CheltenhamMuscat · TriAxis',kind='school',country='Оман',age='teen',school_id='S042',note='ШкольныйотчётназвалGrade9учеников;nationalFIJuniorрезультат,не6/9доказательство.'),dict(id='OMN-ABA-DIGIBULLS',name='ABAOmanInternationalSchool · DigiBulls',kind='school',country='Оман',age='primary',school_id=None,note='ОрганизовавшаяCheltenhamназвалаABAвElementaryпобедителях. Текущаяшкола,coach,языки/приёмподробнонеаудированы.')])
h['results'].extend([dict(id='H134',entity_id='OMN-CHELTENHAM-TRIAXIS',year=2026,league='WRO',category='FutureInnovatorsJunior',stage='OmanNationalFinal6июня2026',award='1-еместо;World2026qualification',level='national_other',source=cr,team='TriAxis',team_id=None,provenance='school_report',note='Grade9. Мироваятитульнаяпобеда неустановлена;nationaljudgedawardиквалификацияотдельно.',checked=CHECKED),dict(id='H135',entity_id='OMN-ABA-DIGIBULLS',year=2026,league='WRO',category='RoboMissionElementary',stage='OmanNationalFinal6июня2026',award='1-еместо;World2026qualification',level='national_match',source=cr,team='DigiBulls',team_id=None,provenance='school_report',note='ПринимающаяшколаCheltenhamназвалаABAElementaryпобедителя;directorganizerprotocolидействующиймладшийнаставникне найден. Не worldwin.',checked=CHECKED)])

country_rows=[
('ARE','ОАЭ','КороткаяENпробаишкола','ДляобоихнайденcurrentFunRoboticsEN/ARoffer;крупныетехплощадкиинтереснывзрослым,детскийвходуточнять.', 'FunRobotics6–16;конкретная9-летняягруппавнижнемTERM2тексте требуетподтверждения. JICтолькопоместномушкольномуклассу.', 'FunRobotics6–16;Essential6–7указанвстаромблоке. PureMinds4–6regularкандидат бездоказанногоEN.', 'LaFolie12–16октября:90минробототехникивсмешаннойсмене,ENподдержкаstaff. Summer2026операторов—архив,будущиеwinter/2027не объявлены.', 'SISDPrimary6–11EnglishSTEAMпрямоподтверждён;пансионсGrade6. Juniorworldresultsэтойшколынеустановлены.', 'Dubai/AlJaddafдляшкольнойпробы;AlWaslCentreдляклуба;AbuDhabiдляAIexpo6–7октября.', 'LaFolieAED2835сVATзадвоих/полнуюнеделю;90минrobotics,не20часов. SISDиндивидуальныйсчётне получен.', 'JIC—schoolnomination/shortlist,неоткрытаяпоездка;campcertificatesиFLLofferне доказываютworldwins.', ['L387','L392','L393','L394','L395','C1078','C1079','C1080','C1088','E018','E173','E174','E176','L039','L040','L388','L389','L390','L391'],['jic-uae'],['S043']),
('OMN','Оман','МладшийWROбезобещанияworldquota','Kids6–9даётпрактикуобоим;МатвеюотдельноElementary8–12. Новыйseasonиforeignnationalentryнеподтверждены.', 'RoboMission/FIElementary8–12илиKids6–9;internationalquotaтолькопослеnationaleligibility.', 'Kids6–9;прямоlocal/nonofficialinternational. Elementary2026непроходит.', 'ДатированнаябудущаяEN/EScampсменавэтомпроходенеустановлена.', 'CheltenhamhostedNational2026;FIJuniorGrade9первое,младшаякоманда/ENflow6/9 отдельно.', 'Muscat:пробныйjuniorcoach/школа,затемnationalpack2027;датунетпридуманной.', 'OMR10заWROучастника2026;новыйвзноснеизвестен. ШкольныйпримерGrade1+4OMR10530tuition,еслиgradesподтвердятся;годтарифауточнить.', 'TriAxis—nationalFIJunior1st;ABA DigiBulls—nationalElementary1st;обаqualifyWorld2026,непобедилиWorldвэтомисточнике.', ['C1081','C1082','C1083'],['wro-oman'],['S042']),
('QAT','Катар','Сначалашколаинациональныегейты','УExplore/Discovery/FLLне менее половины команды должныбытькатарцами. ТехническийPDFсужаетBeginnerвозрасты.', 'VEXIQ8–14;Sumo9–12;Line8–12;Ball8–13. Exploreпослекласса;FLL9надату/состав/школьныйканал.', 'DiscoveryKG/Grade1условно;ExploreтолькопослеGrade2. TechnicalBeginner8/9+,Innovation10+—поканельзя.', 'БудущийtechnicalEN/EScampиприёмтуристическойсемьивэтомпроходенеустановлены.', 'ШкольныйканалScientificClubпроверен;отдельноепостоянноешкольноедосьесмладшимworldpodiumне добавлено.', 'Doha:вначалеlocaleligibility/класс/команда;WebSummitJan31–Feb3,2027длявзрослых,детскоеисключениеunknown.', 'Currentnationalfees/ticketиschoolfamilyquoteнеустановлены.', 'Overviewнепротокол;PDFдетализируетвозраст/платформы. Worldqualificationтолькоотexplicitquota.', [x[0] for x in qrows]+['E175'],['qatar-robotics-ai'],[]),
('SAU','СаудовскаяАравия','МатвеюбудущийElementary;выставкавзрослым','MawhibaимеетподробныйnationalWROпуть. Набор2026закрыт,иностраннаяквотанеустановлена.', 'Elementary8–12поage;physical2+coach,virtual1+coach;следующийнабор иforeignentryотдельно.', 'НетвопубликованныхWROcategories:минимум8. МладшийEN/ESпотокнедоказан.', 'Будущийподходящий6/9EN/EScampнеустановлен;Miskexistingдосьесохранено.', 'ExistingMiskschoolcandidateсохраняется;этотпроходне установилдругуюшколусjuniorworldwin.', 'Национальныйпакет2027послеанонса;LEAP12–15апреля2027,RECCMalham.', 'НовоеWROfee,schoolplaceиLEAPpassquoteнеполучены.', 'LocalSumo/VirtualнеpresentedкакWorlddiscipline;nationalresultнеworldtitle. LEAPlastFAQ18+.', [x[0] for x in srows]+['E108'],['wro-saudi'],['S021'])]
cs=[]
for iso,name,verdict,reason,mat,osc,camp,school_text,city,budget,result,ids,pids,sids in country_rows:
    cs.append(dict(iso=iso,name=name,verdict=verdict,reason=reason,mat=mat,osc=osc,camp=camp,school=school_text,city_route=city,budget=budget,results_check=result,event_ids=ids,profile_ids=pids,school_ids=sids,risk='Класс/место/языкконкретногопотока иforeignnationalquotaещёпроверяются. Не обещанывсемировыеивентыилилучшиешколынаосновеназванияSTEM.'))
f=dict(version=43,checked=CHECKED,title='ОАЭ,Оман,Катар,СаудовскаяАравия:маршрутысемьи',region_label='БЛИЖНИЙВОСТОК · ЧЕТЫРЕПРОВЕРЕННЫХНАПРАВЛЕНИЯ',heading='Школьныйотбор,учебнаяпробаивыставки.',
    family='Матвей2017,Оскар2020;обоимдоступныанглийский/испанский/русский. Точныеbirthday/classesнеизвестны;возрастнадатуикласссчитаютсяотдельно.',
    conclusion='МойпредварительныйвыбордлякороткойENпробы—DubaiFunRobotics;дляWROмладшейпрактики—OmanKids,безобещанияWorldFinal. ДляпереездаSISDимеетпрямойENPrimarySTEAM,ноjuniorcompetitioncoachещёне подтверждён. Эторасширениеатласа,основнойCostaRica/Mexicoмаршрутсохранён.',countries=cs,
    shortlist=[dict(title='Двое:ENtechnicalпроба',detail='FunRoboticscurrentTERM1Arabic/Englishдля6–16. НижнийстарыйTERM2scheduleнеиспользованкакcurrentbooking;согласоватьдвегруппыиуровеньпосле3летопыта.',event_ids=['L387']),dict(title='Не перепутатьcampинтенсивность',detail='LaFolieHandPrint12–16октября2026:две45минroboticsсессиивсмешаннойнеделе. StaffENsupportнеравенполностьюENroboticsinstruction.',event_ids=['L392']),dict(title='Крупныеплощадкиидетскиегейты',detail='AIAbuDhabi6–7октября;GITEX8–11/ExpandNorthStar8–10декабря. Вход6/9unknown;QatarWebSummitlocal18+ иLEAP18+. MuseumFuture—семейнаяальтернатива.',event_ids=['E174','E018','E173','E175','E108','E176'])],
    evidence_cards=[dict(title='Катар:поправкисильнееобщегословaPrimary',detail='PDF2026стр.51Sumo9–12;стр.89Line8–12иmBot;стр.69Ball8–13;стр.43Innovation10–14. Двабратаещёнеавтоматическиоднакоманда.',limit='Следующийregulation/foreignschoolentryещёнеполучен;Discovery/ExploreимеютдругиеgradesиQataricomposition.',event_ids=['C1073','C1074','C1075','C1076','C1070'],school_ids=[],source_urls=[qg,qc]),
    dict(title='Оман:национальныепобедыипутьмладших',detail='TriAxisCheltenhamGrade9—FIJunior1stNational;ABADigiBulls—Elementary1stNational;источникшкольныйотчёт. World2026qualification,неworldtitle.',limit='Kids6–9не имеетWorldFinalroute;ElementaryдляОскарапосленовогоageeligibility,foreignquotaunknown.',event_ids=['C1081','C1082','C1083'],school_ids=['S042'],source_urls=[cr,og]),
    dict(title='ШкольныйENнеподменяетrobotleaguecoach',detail='SISDпрямоEnglishPrimarySTEAM6–11;пансионсGrade6. JICтребуетUAEшкольнуюноминацию,приём2026закрыт.',limit='Primaryplace/тариф/наставник/currentteamcodeнеподтверждены;IBPYP school_report,непротоколпобеды.',event_ids=['C1078','C1079','C1080'],school_ids=['S043'],source_urls=[sp,sb,jr]),
    dict(title='QatarYouthTicket:общееусловиенедостаточно',detail='LocalvenueFAQговоритover18. Terms§5.1допускаетYouth4–17условно,но§5.1.3организаторвыбираетevent/year/location.',limit='ДляQatar2027нетподтверждённогодетскогоисключения;всемейномICSотсутствует. ВзрослыйвыставочныйICSсохраняетдату.',event_ids=['E175','E108'],school_ids=[],source_urls=[wv,wt,urls['leap_faq']])],
    steps=[dict(title='Начатьспробногоуровня',detail='После3летсоревнованийуточнитьсамостоятельноепрограммирование,механикуижурналиспытаний. Пробныйурокобоимважнеемаркетинговогоaccreditation.'),dict(title='Согласоватьшколу,затемкоманду',detail='Класс,местоишкольныйENне гарантируютleaguecoach/часы. Уnationalмаршрутовпроверитьcitizenship/residency,составикакуюстранукомандаможетпредставлять.'),dict(title='Выбратьконкретныйбилетилиcohort',detail='Новыйcamp2027неполучаетдату2026. Visitor/studentbadgeнеподтверждаетдетский6/9вход;сначалаpolicyименноэтоговыпуска,затемпоездка.')],
    limitations='Эточастичныйпроходчетырёхстран. Bahrain,Kuwait,Jordan,Israel,Turkeyидругиестранырегиона;всеновыелагеряиполный5–10летнийшкольныйрейтингещёнеаудированы. Наличие1660примернокарточекнеполныймировойохват.',sources=[])
f['limitations']='Это частичный проход четырёх стран. Бахрейн, Кувейт, Иордания, Израиль, Турция и другие страны региона, новые лагеря и полный школьный рейтинг за5–10лет ещё требуют проверки. Количество карточек не означает полный мировой охват.'

# Keep the Russian copy readable even where identifiers are technical.
import re
def readable(x):
    if isinstance(x,str):
        x=re.sub(r'([А-Яа-яЁё])([A-Za-z0-9])',r'\1 \2',x)
        x=re.sub(r'([A-Za-z0-9])([А-Яа-яЁё])',r'\1 \2',x)
        x=re.sub(r'([,;:])(\S)',r'\1 \2',x)
        return x
    if isinstance(x,list):return [readable(v) for v in x]
    if isinstance(x,dict):return {k:(v if k in ['id','source','url','entity_id','team_id','school_id','iso','start','end','deadline','checked','date','start_time','end_time','timezone'] or k.endswith('_url') else readable(v)) for k,v in x.items()}
    return x
new=[readable(e) for e in new];profiles=[readable(p) for p in profiles]
# Only these four old rows were audited in this pass.
updated=['L039','L040','E018','E108']
for id in updated:byid[id].update(readable(byid[id]))
for s in d['schools'][-2:]:s.update(readable(s))
for e in h['entities'][-2:]:e.update(readable(e))
for r in h['results'][-2:]:r.update(readable(r))
for key in sorted(used):
    f['sources'].append(dict(title='Первичный источник · '+key,url=urls[key],checked=CHECKED))
d['middleeast_focus']=readable(f);d['events'].extend(new);d['league_guide']['profiles'].extend(profiles);d['league_guide']['checked']=CHECKED
known={s['url'] for s in d['sources']}
for key in sorted(used):
    if urls[key] not in known:
        d['sources'].append(dict(url=urls[key],title='Первичный источник · '+key,evidence='Прочитан организатор / школа / связанный PDF; текущий и архивный сезон разделены',checked=CHECKED));known.add(urls[key])
a=d['completeness_audit'];a['validation_previous']=a.get('validation',{})
a.update(version=43,checked=CHECKED,status='Исследование продолжается',scope='ОАЭ/Оман/Катар/Саудовская Аравия: младшие national gates, языковая проверка, школьные результаты и крупные выставки',
    conclusion='33 новые карточки,4 национальных профиля,2 школьных досье и2 национальных результата. Возрастные противоречия Катара и местный18+WebSummit показаны отдельно; архивные лагеря не выданы за будущие. Мировой охват остаётся частичным.',
    new_ids=[e['id'] for e in new],new_profiles=[p['id'] for p in profiles],updated_ids=updated,new_school_ids=['S042','S043'],updated_profile_ids=[],validation=dict(version=43,status='pending',publication='pending'))
d['camp_focus'].update(version=43,checked=CHECKED,added_ids=[e['id'] for e in new if e['block']=='Лагеря'],updated_ids=updated[:2],conclusion='395 лагерных и учебных карточек. Current bilingual FunRobotics, EN staff support LaFolie и неизвестный технический язык других операторов разделены; summer2026 архивы не стали2027сменами.',validation=dict(version=43,status='pending'))
d['school_focus'].update(version=43,checked=CHECKED,conclusion='43 школьных досье. Cheltenham Muscat: национальный FIJunior результатGrade9; SISD: прямойEnglishPrimarySTEAM6–11,boardingсGrade6. Текущие junior coaches и world school ranking не установлены.')
assert len(new)==33 and len(profiles)==4
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rows=[]
for filename in ['receipt.json','receipt-extra.json','receipt-final.json']:
    rows+=json.loads((WORK/'sources-middleeast-v43'/filename).read_text())
receipt=dict(version=43,checked=CHECKED,scope='ARE/OMN/QAT/SAU primary-source bounded pass',fetches=[{k:r[k] for k in ['name','url','status','resolved','mime','bytes','sha256','error'] if k in r} for r in rows],used_names=sorted(used),
    alternate_web_opened=[dict(name=k,url=urls[k],read_via='web.run opened full page; failed direct HTTP retained') for k in ['fun_term','leap','leap_faq']],
    pdf_review=dict(url=qg,pages=99,relevant_pages=[3,43,51,69,89],cover_copyright=2025,amendments=2026,visual_pages=[1,51,89]),
    conflicts=['Qataroverviewvs2026PDFage/team/platform','QatarArm10–18PDFvs12–18overview','WebSummitQatarlocal18+vsconditionalglobalYouthTicket','FuncurrentTERM1vsoldTERM2/Ramadan','PMAcurrentTERM12026vsTERMII2025/NCFE2024','AIexpoFAQtitle5–7vsbody/home6–7Oct2026','GITEXcurrentDecvslegacyNovPDF','LEAP2027homepagevs2026FAQbody'],
    remaining='Foreign national quotas, actual cohorts/languages/places, rest of Middle East and full world scope')
(ROOT/'data/middleeast-source-receipts-v43.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
rp=ROOT/'data/research-plan.json';r=json.loads(rp.read_text());r.update(updated=CHECKED,status='active',completeness_audit='data/audit-v43.json')
r['latest_validation_previous']=r.get('latest_validation',{});r['latest_validation']=dict(version=43,status='local_checks_pending_publication_pending')
r['previous_goal_turn_classification']=dict(version=42,classification='progress',evidence='Published b167b3571e43b7df908f45ea45189dda792ad715; anonymous live QA and42 asset hashes matched; Europe family pass delivered, full-world objective continues.')
r['research_passes'].append(dict(version=43,checked=CHECKED,scope='ARE/OMN/QAT/SAU junior entry/camp language/school/exhibition pass',added_records=33,new_profiles=4,new_schools=2,history_added=2,status='partial',remaining='Rest of region, future cohorts, foreign quotas, school/coach places and full world scope'))
r['next_research'].insert(0,'Middle East v43: новые winter/summer2027 и technical language, foreign national quotas, реальное место младшей команды; Бахрейн/Кувейт/Иордания и остальные страны региона. Полная мировая цель сохраняется.')
for req in r['requirements']:
    if req['id']=='unified_database':req['evidence']='v43:1658cards /129profiles /43schools /135boundedresults; four-country MiddleEast view and previous regions; world partial.'
    elif req['id']=='camps':req['evidence']='v43:395 learning/camp cards; current bilingual technical instruction, staff support and unconfirmed language separated; archives not future cohorts.'
    elif req['id']=='exhibitions':req['evidence']='v43:176eventcards; NorthStar/AIAbuDhabi/WebSummitQatar added, MuseumFuture family alternative; local18+gates remain explicit.'
    elif req['id']=='permanent_schools':req['evidence']='v43:43dossiers; CheltenhamnationalFIJuniorGrade9; SISDexplicitEnglishPrimarySTEAM; juniorcoach/admission unknown.'
    elif req['id']=='school_retrospective':req['evidence']='v43:135boundedresults; twoOmannationalplacements/qualification separated fromworldwins; worldwide5–10year ranking partial.'
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=43,added=len(new),profiles=4,schools_added=2,history_added=2,records=len(d['events']),world_complete=False)))
