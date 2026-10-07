"""Scoped Mexican category rules and current family workshops, not admissions."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = '6806c09f1c27be9c2d6b4f39b0e5271e01cf45d2'
CHECKED = '2026-10-06'
GOV = 'https://turismo.zacatecas.gob.mx/sera-zacatecas-sede-del-torneo-mexicano-de-robotica-2027/'
FMR = 'https://femexrobotica.org/fmr/eventos/'
RL = 'https://www.robofestmexico.org/'
GENERAL = RL+'_files/ugd/f2d401_2e803ec9fb70468bbb51b1fff166a77c.pdf'
PARADE = RL+'_files/ugd/70d3e0_8df3deb7b77a4f99aff12b05418187ca.pptx?dn=RoboParade2026_V2.pptx'
RUBRIC = RL+'_files/ugd/f2d401_daee873488eb48ebb1a034989e81806e.pdf'
DRONE = RL+'_files/ugd/70d3e0_3fa233123159488abc9f4bdca1f2bf28.pdf'
FOOTBALL = RL+'_files/ugd/70d3e0_ff05c3477db1422dacaf3615890bb630.pdf'
BAJA = 'https://www.bajabot.com/downloads/2026/convocatoria_05.pdf'
ARMADO = 'https://www.bajabot.com/downloads/2026/manuales/categoria_A.pdf'
SUMO = 'https://www.bajabot.com/downloads/2026/manuales/categoria_AA.pdf'
BEBRAS_API = 'https://cangurocr.org/api/bebras/pages/agenda'
BEBRAS_RULES = 'https://cangurocr.org/api/bebras/pages/reglamento'
MAKER = 'https://www.feriamaker.mx/talleres'
MAKER_API = 'https://script.google.com/macros/s/AKfycbzf4qXHd4sxN4BQXf1JqX36fUtV15kNXtV1xcrzItEkIktNpZhKaWMVNSeVZoo4DYQrnA/exec?accion=talleres'
RL_IDS = ['C'+str(i) for i in range(1159,1169)]
NEW_IDS = RL_IDS+['C1169']+['E'+str(i).zfill(3) for i in range(191,201)]
GUIDES = ['robofest-latam','bajabot']
LANG = 'Язык очного судейства/мастерской не указан прямо. Испанский текст правил или каталога не доказывает ES/EN поток; согласовать до поездки.'
LOCAL_AGE = 'Локальный PDF 2026: Junior от 6 до менее 15 лет. Обзор сайта использует 5–8 классы; рамки расходятся. Новый сезон 2027 и дата отсечения ещё не объявлены.'
LOCAL_GATE = 'Условный кандидат по локальной рамке 6–14 из правил 2026. Для следующего набора подтвердить возраст на его день, класс и самостоятельную работу; это не принятие заявки.'
LOCAL_COST = 'Взнос LATAM не установлен. В старом PDF p34 мировой взнос USD 100 + 10 за оформление, а p27 USD 90 относится к локальным US events. Эти суммы не являются ценой México или 2027. Робот, подготовка, перелёт и жильё отдельно.'
MIXED = 'Общий файл обозначен 2026, но содержит footer General Rules 2025 V2, таблицу RoboParade 2025 и прошлые даты. Локальная рамка 6–14 не переносится на LTU World 2027: там Junior 5–8 классы и отдельный Explorer 1–4. Дата LATAM 2027 не опубликована.'

def ref(title,url):
    return dict(label=title,url=url)

def source(title,url):
    return dict(title=title,url=url,checked=CHECKED)

def watch(ident,title,age,mat,osc,team,gear,url,note,block='Соревнования',city='Pachuca de Soto · Hidalgo · площадка нового сезона неизвестна',reward=None):
    return dict(id=ident,block=block,title=title,country='Мексика',region='Северная Америка',city=city,
        start='',end='',period='Следующий набор / 2027 не объявлен; ниже только опубликованная редакция 2026.',date_status='Необъявлено',deadline='',
        age=age,mat=mat,osc=osc,format=team,entry='Ждать новую convocatoria, подтвердить категорию, страну/школьные документы, взрослого наставника, язык, цену и самостоятельность. Заявка не отправлена.',
        gear=gear,language=LANG,languages=[],language_mode='unconfirmed',language_certainty=LANG,cost=LOCAL_COST,
        scope='regional',level='C — локальная дисциплина; следующий этап не объявлен',importance_reason='Отдельная дисциплина местного маршрута. LATAM/международное название не подтверждает мировой финал, личный допуск или результаты семьи.',
        reward=reward or 'Локальное место / award подтверждается итоговым протоколом; диплом участия, аккредитация и мировой приз различаются.',
        priority='P2 — подготовка после подтверждения нового сезона',action='Сверить следующую редакцию и точный возраст/класс, затем выбрать дисциплину и подготовить ребёнку самостоятельный проект.',
        source=url,references=[],proof='Прочитаны выбранные положения собственной опубликованной редакции 2026; это архив правил, а не расписание 2027.',
        checked=CHECKED,status='Идея',note=note,iso=['MEX'],themes=['robotics','coding','makers'],participation='team',evidence_level='historical_rules',
        rules_year=2026,next_season_status='unannounced',registration_status='Новый набор не опубликован; личный допуск/место/оплата не проверены.')

def category(e):
    return dict(name=e['title'],age=e['age'],team=e['format'],hardware=e['gear'],age_rule='Редакция 2026; отсечение, класс и правила следующего набора проверить заново.',
        event_id=e['id'],entry=e['entry'],language=e['language'],note=e['note'],source=e['source'],checked=CHECKED)

def polish(value):
    urls=[]
    def protect(match):
        urls.append(match.group());return '§'+str(len(urls)-1)+'§'
    value=re.sub(r'https?://[^\s]+',protect,value)
    value=re.sub(r'([А-Яа-яЁёA-Za-z])(\d)',r'\1 \2',value)
    value=re.sub(r'(\d)([А-Яа-яЁёA-Za-z])',r'\1 \2',value)
    value=re.sub(r'([А-Яа-яЁё])([A-Za-z])',r'\1 \2',value)
    value=re.sub(r'([A-Za-z])([А-Яа-яЁё])',r'\1 \2',value)
    value=re.sub(r'([:;·])(?=\S)',r'\1 ',value)
    value=re.sub(r'(\d{1,2}): (\d{2})\b',r'\1:\2',value)
    value=re.sub(r',(?=[А-Яа-яЁёA-Za-z])',r', ',value)
    value=re.sub(r'\bP ([0-4])\b',r'P\1',value)
    value=re.sub(r'\b(CP|C|E) (\d+)\b',r'\1\2',value)
    value=value.replace('v 135','v135')
    value=value.replace('3 D','3D')
    for a,b in [('EV 3','EV3'),('W 193','W193'),('MDF','MDF'),('RoboParade','RoboParade'),('Local 2026','Local 2026'),('нет нового','нет нового')]:
        value=value.replace(a,b)
    for i,url in enumerate(urls):value=value.replace('§'+str(i)+'§',url)
    return value

def profile(ident,name,age,tags,summary,rows,route,nuances,sources,award):
    return dict(id=ident,name=name,group='regional',age_summary=age,age_tags=tags,summary=summary,categories=[category(e) for e in rows],
        event_ids=[e['id'] for e in rows],legacy_ids=[],route=route,hardware='См. отдельную дисциплину: наборы, размеры и автономность не взаимозаменяемы.',language=LANG,
        importance='Дополнительный местный путь подготовки и результатов. Официального мирового рейтинга всей серии не установлено.',strengths=summary,
        requirements=['Подтвердить новый сезон, точную возрастную или школьную категорию и взрослого coach.',
            'Согласовать допуск семьи, учёбу за рубежом, язык защиты, оборудование и полный счёт.',
            'Сохранить протокол категории, team ID, состав и роль каждого; участие и призовой результат записывать отдельно.'],
        nuances=nuances,cost=LOCAL_COST,award=award,sources=sources,evidence='Первичные местные документы 2026 изучены выборочно 06.10.2026. Даты/набор 2027 и зачисление семьи не подтверждены.')

def enrich_v135(d):
    ev={e['id']:e for e in d['events']}
    t=ev['C043']
    t.update(start='2027-03-03',end='2027-03-06',period='',date_status='Подтверждено',city='Zacatecas · Palacio de Convenciones',venue='Palacio de Convenciones de Zacatecas',
        source=GOV,checked=CHECKED,proof='Официальное объявление Secturz/COZCyT от 18.06.2026: 3–6 марта 2027, Palacio de Convenciones. Календарь FMR подтверждает March 2027 и COZCyT; новая convocatoria с категориями не прочитана.',
        action='Следить за convocatoria TMR 2027 и возрастами конкретных категорий. Даты события точные; дедлайн, взнос, младший/иностранный допуск и возможный RoboCup отбор ещё неизвестны.',
        note='23 категории, около 300 команд и 1 200 участников в сообщении — прогноз организаторов, не фактический протокол. Даты TMR не означают допуск 6/9-летних ко всем дисциплинам. TMR 2026 завершён; взрослую Escuela de Invierno Veracruz не считать детским лагерем.',
        references=[ref('FMR · календарь 2027',FMR)],evidence_level='official_host_announcement',date_scope='festival_window')
    t.update(language=LANG,languages=[],language_mode='unconfirmed',language_certainty=LANG)
    b=ev['C064'];b.update(checked=CHECKED,priority='P0 — открыт набор',
        proof='06.10 перепроверены собственный public API agenda/rules и отображённые страницы. Регистрация 28.09–16.10, конкурс 09–13.11, публикация результатов 18.11. Главная страница по-прежнему 2.º Pre-Ecolier, регламент 3–6 primaria: расхождение не разрешено.',
        note='Возраст 9 лет не доказывает 3 класс. Проверьте https://cangurocr.org/bebras/reglamento и https://cangurocr.org/bebras; класс важнее паспортного возраста.',
        references=[ref('Agenda · первичные JSON данные',BEBRAS_API),ref('Reglamento · первичные JSON данные',BEBRAS_RULES),ref('Отображённая главная · 2.º grado','https://cangurocr.org/bebras/')])
    rows=[]
    specs=[
      ('Game · Building Bridges',5,'Любая разрешённая платформа; полностью автономный робот и неизвестные факторы в день состязания.', ['robotics','coding']),
      ('Exhibition · самостоятельный инженерный проект',5,'Любая платформа; собственный творческий автономный проект, проверка устойчивости к условиям освещения.', ['robotics','makers']),
      ('BottleSumo Junior',3,'Junior: LEGO NXT / EV3 / SPIKE Prime / Robot Inventor либо VEX IQ; частично неизвестная задача, не обычное RC сумо.', ['robotics','coding']),
      ('Unknown Mission Challenge Junior',4,'LEGO NXT / EV3 / SPIKE Prime / Robot Inventor либо VEX IQ; задача полностью неизвестна до старта.', ['robotics','coding']),
      ('RoboArts Junior',5,'Любая разрешённая робототехническая платформа; творческий проект, отдельные требования защиты.', ['robotics','art']),
      ('RoboMed Junior',5,'Любая разрешённая платформа; инженерный проект по отдельным правилам, не медицинская квалификация.', ['robotics','science']),
    ]
    for i,(name,n,gear,themes) in enumerate(specs):
        q=watch(RL_IDS[i],'Robofest LATAM · '+name+' · следующий набор',LOCAL_AGE,LOCAL_GATE,LOCAL_GATE,
            'До '+str(n)+' учеников и взрослый coach; нижний размер по выбранному регламенту ещё уточнить.',gear,GENERAL,
            MIXED+' Coaches не собирают робот и не пишут/редактируют код за участников (p13). Game/Exhibition имеют квалификационный путь; Open номинации согласует региональный директор. В файле <3 команд: нет призовых мест, возможна письменная аккредитация от 80%; p30 содержит отдельные национальные квоты. Ни одно условие не даёт автоматического права на World 2027.')
        q['themes']=themes;q['team_max']=n;q['historical_editions']=[dict(year=2026,start='2026-03-20',end='2026-03-21',source=GENERAL)]
        q['references']=[ref('Обзор категорий · иной grade порог',RL+'desafios'),ref('World LTU 2027 · отличающийся регламент','https://www.robofest.net/images/2627/General2027_V1.pdf')]
        rows.append(q)
    q=watch(RL_IDS[6],'Robofest LATAM · RoboParade · следующий младший набор','Локальная презентация 2026: 6–14 лет, не grade Junior LTU 2027.',LOCAL_GATE,LOCAL_GATE,
        '1–5 учеников + взрослый coach. Solo допустим, но teamwork оценивается ниже.',
        'Любой kit/язык кода; автономное следование линии в обе стороны, датчик остановки перед другим роботом; ширина ≤35 см, весь состав ≤60 см, скорость 7–16 см/с с отображением.',PARADE,
        'Рубрика 2026: checklist20%, design10% + объяснение скорости7%, art10%, features10%, teamwork10%, самостоятельность10%, письменная математика3%, два parade rounds по10%. Solo teamwork 1/2 из5. Презентация имеет имя V2, внутри V1.0 2026; Animal Kingdom относится к 2026. В World 2027 Explorer 1–4 классы и другая тема Fun and Games, не переносить локальный возраст автоматически.',
        reward='В презентации есть оценивание и trophies; конкретные призовые места подтверждать протоколом. Это отличается от простого диплома за посещение.')
    q.update(team_min=1,team_max=5,references=[ref('Официальная рубрика',RUBRIC),ref('Обзор · grade формулировки',RL+'desafios')],historical_editions=[dict(year=2026,start='2026-03-20',end='2026-03-21',source=GENERAL)]);rows.append(q)
    q=watch(RL_IDS[7],'Robofest LATAM · drones W193 · следующий набор','Конфликт 2026: страница Junior10–12/Senior13–18; PDF Junior9–14/Senior15–20.',
        'Условно: в 2027 Матвею 9–10, но нижний порог 9 или 10 расходится. Согласовать действующую редакцию.',
        'Нет по обеим опубликованным младшим рамкам 9+ или10+; в 2027 Оскару6–7.',
        '1–2 ученика + один coach; неизвестная миссия на месте, запрет помощи coach.',
        'Classic: коммерческий drone, например DJI, ≤25 см, 1S LiPo<4.5V; Unlimited своя безопасная сборка. Нужны ручное RC/app override, пластиковые пропеллеры, полёт <2 м.',DRONE,
        'PDF W193 V2 от20.02.2026, не регламент LTU World 2027. Заявление о Hong Kong July2026 — прошлое локальное обещание без проверенного внешнего допуска. >4 команд для призового отбора, <3 и75% для аккредитации; ситуация 3/4 команд не объяснена. 2027 даты/квота/цена неизвестны.')
    q.update(team_min=1,team_max=2,references=[ref('Страница с другим возрастом',RL+'copia-de-vcc')],international_circuit='W193 local claim; not LTU Robofest World category');rows.append(q)
    q=watch(RL_IDS[8],'Robofest LATAM · Robofútbol 3v3 W193 · следующий набор','Junior 8–14 лет на день соревнования; Senior15–19. Только редакция03.03.2026.',
        'Условно по 8–14, после новой редакции, подготовки команды и трёх роботов.',
        'Нет по Junior8+: в2027 Оскару6–7.',
        'До6 участников по формулировке PDF и один coach18+; три operating technicians. Уточнить, входит ли coach в max6.',
        'Три собственных RC робота 20×20×20 см /800 г, до4 моторов и1 контроллера каждый. Код управления участников, готовые RC apps запрещены; собственная сеть, общего Wi-Fi нет.',FOOTBALL,
        'PDF объявляет призы при >4 команд и W193 Hong Kong July2026; фраза «два первых» одновременно перечисляет 1/2/3 места. При <2 категория может не состояться. Число призов, 2027 приглашение и внешний регламент не подтверждены; это не автоматический LTU world route. Technical inspection включает объяснение проекта/кода; после test session связь с coach запрещена.')
    q.update(team_max=6,team_count_note='PDF max6; inclusion of adult coach not explicit',international_circuit='W193 local claim; not LTU Robofest World category');rows.append(q)
    q=watch(RL_IDS[9],'Robofest LATAM · Vision Centric Challenge · будущая старшая ступень','PDF2026: Senior15–19, Junior не указан.',
        'Нет по 15+ для текущего возраста.', 'Нет по 15+ для текущего возраста.',
        'До5 учеников + взрослый coach; региональный директор выбирает делегацию.',
        'Любая разрешённая платформа; vision задача объявляется по отдельным правилам.',GENERAL,
        MIXED+' Эта Senior дисциплина не означает право братьев участвовать в drone challenge с иной возрастной таблицей.')
    q.update(priority='P4 — будущая старшая ступень',team_max=5);rows.append(q)
    q=watch('E191','BajaBot · Armado de Robot · демонстрация для 1–3 классов','Только ученики 1–3 классов primaria; паспортный возраст не заменяет класс.',
        'Условно только при 1–3 классе в новом сезоне; при4+ выбирать Mini Sumo.',
        'Условно только при зачислении в1–3 класс; дошкольный возраст недостаточен.',
        '2–3 ученика 1–3 классов + один взрослый advisor; advisor максимум2 команды. Смешанные/независимые команды разрешены.',
        'LEGO Education набор временно предоставляет музей; вернуть после3 попыток. 30×20 см, высота свободная; сборка1 час, презентация3 минуты, трасса5 м.',ARMADO,
        'Convocatoria и manual p2: demonstration only, no competition awards, participation diploma. Но manual p8 перечисляет оценивание/поощрение за дизайн, время и выступление — внутреннее расхождение. До письменного разъяснения не считать призовым состязанием или мировой победой. Прошлый старт17.05.2026/дедлайн08.05 завершены; новый сезон неизвестен.',
        block='События',city='Tijuana · El Trompo, Museo Interactivo',reward='Диплом участия подтверждён; возможные специальные поощрения в p8 не установлены как соревновательные места.')
    q.update(participation='team',team_min=2,team_max=3,scope='local',level='D — учебная демонстрация',references=[ref('Convocatoria2026 · сроки и diploma',BAJA)],
        cost='Стоимость участия/входа неизвестна. Набор на день демонстрации предоставляет музей, он не остаётся у семьи; поездка/билеты/подготовка отдельно.',
        historical_editions=[dict(year=2026,start='2026-05-17',end='2026-05-17',deadline='2026-05-08',source=BAJA)],grade_level='Primaria Baja 1–3');rows.append(q)
    q=watch('C1169','BajaBot · Mini Sumo LEGO · следующий набор 4–6 классов','Только4–6 классы primaria, даже если ребёнок опытный/старше9.',
        'Условно только при4–6 классе в новом сезоне; точный класс неизвестен.',
        'Позднее: проверить4–6 класс; возраст6/7 сам по себе допуска не даёт.',
        '2–3 ученика4–6 классов + взрослый advisor; капитан фиксируется до старта, advisor максимум2 команды. Независимая команда допустима.',
        'Автономный LEGO NXT/EV3/SPIKE Prime/51515 из разрешённых комплектов, один контроллер; 20×20×20 см /2 кг. Bluetooth/Wi-Fi отключить, загрузкаUSB; стартовая задержка5 секунд, dojo77 см.',SUMO,
        'Convocatoria/p2 manual ограничивают4–6 класс. В p3 осталась фраза «3 grados de secundaria», в electronics section15151 против списка51515 — несогласованные шаблонные строки, не разрешение вторичной/новой платформы. Алгоритм предъявить судье; автономный бой до3 минут без вмешательства. 17.05.2026 и08.05.2026 прошли, 2027 не объявлен.',city='Tijuana · El Trompo, Museo Interactivo')
    q.update(team_min=2,team_max=3,scope='local',grade_level='Primaria Alta4–6',references=[ref('Convocatoria2026 · школьные документы/сроки',BAJA)],
        cost='Fee/вход неизвестны. Собственный разрешённый робот и ноутбук, подготовка и поездка отдельно; музейный набор Armado не обещан Mini Sumo.',historical_editions=[dict(year=2026,start='2026-05-17',end='2026-05-17',deadline='2026-05-08',source=BAJA)]);rows.append(q)
    workshop_specs=[
        ('E192','21','Máscaras Vivientes · arte e IA','2026-10-17','2026-10-18','Возраст не указан; «Ninguno» в требованиях не минимальный возраст.',
            'Проверить возраст, сопровождение и комфорт работы с гипсовой маской.','Проверить возраст, сопровождение и комфорт работы с гипсовой маской.',
            'Гипсовая маска лица, цифровая фотограмметрия и AI анимация с голосом; физическая маска и HD видео домой. Это творческий вводный workshop, не обучение AI-моделей.',
            '150; валюта в записи не указана.','17 октября15:00/16:00;18 октября12:00/13:00;1 час, capacity15.',['ai','art','makers']),
        ('E193','23','Mascotas del Mictlán · 3D figures','2026-10-17','2026-10-18','5+ лет; всё оборудование/материалы предоставляет ведущий.',
            'Условно подходит по5+; место и сопровождение уточнить.','Условно подходит по5+; место и сопровождение уточнить.',
            'Выбор и окраска готовой 3D фигурки +4 акриловых маркера домой. Знакомство с моделированием/постобработкой, не самостоятельная робототехника.',
            '70; валюта в записи не указана.','Дни17/18 октября; поле времени11:00 и14:00, привязку слотов ко дню проверить;0.5 часа, capacity10.',['technology','art','makers']),
        ('E194','24','Mi Primer Coche a Propulsión','2026-10-17','2026-10-17','8+ лет, без опыта/собственных инструментов.',
            'Условно подходит по8+; место уточнить.','Нет по8+: в2026 Оскару5–6.',
            'Машинка изMDF на воздушном шаре, давление, энергия, движение, действие/противодействие; машинка домой. Это физика/механика, не программируемый robot.',
            '275; валюта в записи не указана.','17 октября15:00;1.5 часа, capacity15.',['science','makers']),
        ('E195','28','FlatCat · карманный механический автомат','2026-10-18','2026-10-18','«Для детей», числовой минимум не указан.',
            'Уточнить возраст и сопровождение.','Уточнить возраст и сопровождение.',
            'Лазерный картон, шестерни и латунные крепления; движение рук от механической вкладки. Механизм домой, без программирования.',
            '50; валюта в записи не указана.','18 октября весь день;0.25 часа за занятие. Это15 минут, не15 часов или лагерь.',['makers','technology']),
        ('E196','29','Llavero robot · столярная сборка','2026-10-17','2026-10-18','Для детей, подростков и взрослых; числовой минимум неизвестен.',
            'Согласовать возраст и работу ручными инструментами.','Согласовать возраст и работу ручными инструментами.',
            'Деревянный брелок из бруска, винтов, шайб и цепочки; отвёртка/ручная пила. Робот образный, без электроники и автономного кода.',
            '50; валюта в записи не указана.','17/18 октября весь день;0.25 часа за занятие.',['makers','technology','art']),
        ('E197','31','Titerilandia · цифровые истории OctoStudio','2026-10-17','2026-10-18','«Для детей», числовой минимум неизвестен; телефон родителя/опекуна.',
            'Условный детский кандидат; точный возраст, место и язык уточнить.','Условный детский кандидат; точный возраст, место и язык уточнить.',
            'Пальчиковые куклы, командная история, показ и цифровой проект вOctoStudio, обмен видео. Требуется бесплатное приложение на телефоне родителя; установка не выполнялась.',
            '0 в каталоге мастерской; общий вход/транспорт/телефон и прочие затраты отдельно.','17 октября11:00;18 октября11:00/15:00 по порядку полей, привязку подтвердить;2 часа, capacity10.',['coding','games','art']),
        ('E198','32','Forja tu Mountsro robot · творческий образ','2026-10-17','2026-10-18','8–100 лет по каталогу.',
            'Условно подходит по8+; место уточнить.','Нет по8+: в2026 Оскару5–6.',
            'Творческая работа с образом эмоционального монстра. В описании не доказаны моторы, код или технический kit, хотя в названии robot.',
            '0 в каталоге мастерской; вход и поездка отдельно.','17/18 октября13:00;1 час, capacity10.',['art','makers']),
        ('E199','10','Crea tu robot de cartón · 12+','2026-10-18','2026-10-18','Примерно12+ из-за мелких/режущих деталей; не6/9.',
            'Нет по опубликованному ориентиру12+.','Нет по опубликованному ориентиру12+.',
            'Предсобранный картонный kit,LED и voice module; собери/соедини. Три дополнительные игры10MXN за попытку с фигурками-призами не международное соревнование.',
            '150 MXN за мастерскую; игры10 MXN отдельно.','18 октября12:00/13:00/14:00;1 час, capacity14.',['robotics','makers']),
        ('E200','4','Clicker / Charms · знакомство с3D печатью','','','5+ лет, без собственного оборудования/опыта.',
            'Условно подходит по5+; конкретный день/место неизвестны.','Условно подходит по5+; конкретный день/место неизвестны.',
            'Выбор и сборка брелкаClicker/Charms из готовых напечатанных деталей, персонализация. Это короткое makers знакомство.',
            'От $60; валюта и итог зависят от выбора и не подтверждены.','Поле дата пустое, todoElDia=true.0.2 часа в API; единицу/слот уточнить, не назначать автоматически17/18.',['makers','technology']),
    ]
    for ident,code,title,start,end,age,mat,osc,gear,cost,timing,themes in workshop_specs:
        q=watch(ident,'Feria Maker · '+title,age,mat,osc,'Короткая мастерская на ярмарке; состав/сопровождение по её требованиям.',gear,MAKER,
            timing+' Каталог и собственный public JSON, связанный страницей, проверены06.10.2026. Capacity — лимит, не свободное место. Пустая цена не означает бесплатно; язык и детский admission отдельно. Поле «robot» не устанавливает техническую сложность.',
            block='События',city='Ciudad de México · CENART · конкретная carpa/mesa по каталогу',reward='Сделанный предмет/цифровой проект; это не призовое место, олимпиада или мировой диплом.')
        q.update(start=start,end=end,date_status='Подтверждено' if start else 'Необъявлено',period='' if start else 'В каталоге Feria Maker2026; день этой мастерской не задан.',
            date_scope='workshop_window',cost=cost+' Это цена занятия, не полная семейная поездка; налоги/валюта/пакет проверить.',
            action='Выбрать слот мастерской, подтвердить возраст/сопровождение, язык, материал, точный счёт и место. Платёж/регистрация не выполнялись.',
            scope='local',level='D — практическая семейная мастерская',priority='P1 — близкое по дате семейное знакомство' if not mat.startswith('Нет') else 'P4 — позже по возрасту',
            entry='Открытый каталог Feria Maker. Проверить билет/слот и требования именно мастерской; регистрация семьи не выполнена.',
            themes=themes,participation='workshop',evidence_level='public_workshop_catalog',parent_event_id='E001',workshop_code=code,
            references=[ref('Публичные данные, используемые собственной страницей',MAKER_API)],proof='Прочитана выбранная запись public JSON и поля собственно каталога: дата/время, возраст, duration, price, capacity и требования. Это снимок расписания, не наличие места.',
            registration_status='Идея; актуальные места/бронь не проверены.')
        q.pop('rules_year');q.pop('next_season_status');rows.append(q)
    human_fields=['title','period','age','mat','osc','format','entry','gear','language','language_certainty','cost','level','importance_reason','reward','priority','action','proof','note','registration_status','grade_level','team_count_note']
    for e in rows+[t]:
        for key in human_fields:
            if isinstance(e.get(key),str):e[key]=polish(e[key])
        for r in e.get('references',[]):r['label']=polish(r['label'])
    assert [e['id'] for e in rows] == RL_IDS+['E191','C1169']+['E'+str(i) for i in range(192,201)]
    assert not any(e['id'] not in NEW_IDS and e.get('workshop_code') in {q.get('workshop_code') for q in rows if q.get('workshop_code')} and e.get('parent_event_id')=='E001' for e in d['events'])
    d['events']=[e for e in d['events'] if e['id'] not in NEW_IDS]+rows
    guide=d['league_guide'];guide['profiles']=[p for p in guide['profiles'] if p['id'] not in GUIDES]
    tmr=next(p for p in guide['profiles'] if p['id']=='tmr')
    tmr.update(route=t['entry'],language=LANG,evidence='Даты и место обновлены по официальному host announcement 18.06.2026; категории/дедлайн 2027 ещё неизвестны.')
    tmr['categories']=[category(t)]
    tmr['categories'][0]['age_rule']='TMR 2027: дата отсечения и школьная категория ещё не опубликованы в прочитанном host announcement; не использовать редакцию 2026 для допуска.'
    for title,url in [('Secturz/COZCyT · точные даты TMR2027',GOV),('FMR · March2027',FMR)]:
        if not any(s['url']==url for s in tmr['sources']):tmr['sources'].append(source(title,url))
    msg='v135 · TMR2027:3–6 марта,Palacio de Convenciones,Zacatecas. Апрель2026 и старую inscripción не использовать для заявки2027. Возраст/цена/deadline/world quota по новой convocatoria неизвестны.'
    msg=polish(msg)
    tmr['nuances']=[s for s in tmr['nuances'] if not s.startswith(('v135','v 135'))]
    if msg not in tmr['nuances']:tmr['nuances'].append(msg)
    for s in tmr['sources']:s['title']=s['title'].replace('C 043','C043')
    rf=next(p for p in guide['profiles'] if p['id']=='robofest')
    msg='v135 · México/LATAM2026 публикует локальные6–14 против grade5–8 overview, отдельные W193 drones/football и смешанный General2025/2026. Это не изменение правил LTU World2027; новый LATAM календарь/квота не объявлены. См. отдельный профиль robofest-latam.'
    msg=polish(msg)
    rf['nuances']=[s for s in rf['nuances'] if not s.startswith(('v135','v 135'))]
    if msg not in rf['nuances']:rf['nuances'].append(msg)
    for s in rf['sources']:s['title']=s['title'].replace('C 053','C053')
    guide['profiles'].append(profile('robofest-latam','Robofest LATAM · México · локальные дисциплины','Правила2026: многие Junior6–14; drones9–14 или10–12; football8–14; VCC15–19.2027 не объявлен.',
        ['6','9','10-12','teen','unknown'],'Автономные задачи и творческие проекты рядом с семейной базой; дисциплины LTU и W193 требуют разных маршрутов.',rows[:10],
        'Для следующего сезона сначала согласовать местную категорию и представительство México/CR. Для LTU пройти соответствующий qualifier или Open route через International Director; страна/квоты и правила2027 отдельно. Drones/football заявлены местно как W193, их внешний отбор не подтверждён.',
        [MIXED,'RoboParade rubric оценивает собственный код, объяснение скорости, математику и независимость детей; solo снижается по teamwork.',
         'Локальная аккредитация без3 команд/80% не призовое место. У W193 дронов другие75% и возрастной конфликт; не смешивать условия.',
         'Past2026:20–21 марта,Pachuca. About с10–11 марта SanMiguel без года относится к иной/неустановленной редакции.',
         'USD90 относится к US local; USD110 в p34 прошлого мирового оформления не подтверждает текущий LATAM fee2027.'],
        [source('General2026 · локальные возраст/команда/прошлые квоты',GENERAL),source('Обзор сайта · иной grade порог',RL+'desafios'),source('RoboParade2026 · презентация',PARADE),source('Рубрика',RUBRIC),source('Drone2026 · W193',DRONE),source('Drone page · возрастной конфликт',RL+'copia-de-vcc'),source('Football2026',FOOTBALL)],
        'Конкретный локальный приз только по протоколу. Отбор/аккредитация и диплом участия не world medal.'))
    guide['profiles'].append(profile('bajabot','BajaBot · Tijuana · младшая демонстрация и Mini Sumo','Armado:1–3 классы; Mini Sumo LEGO:4–6 классы. Нужен школьный уровень, не просто6/9 лет.',
        ['unknown'],'Музейный начальный командный формат и отдельное автономное LEGO сумо для старшей primaria.',[rows[10],rows[11]],
        'Независимая/межшкольная команда возможна в опубликованном2026 manual, при школьном подтверждении каждого и взрослого advisor. Сначала дождаться нового сезона. Связь сRobomatrix/RoboCup в образовательной цели не является автоматическим отбором.',
        ['17 мая2026 и срок8 мая прошли; в прочитанном сайте/документах2027 не объявлен.',
         'Armado p2 и convocatoria: only exhibition,diploma. Manual p8 перечисляет поощрения — противоречие сохраняется, призовые места не обещаны.',
         'Armado:2–3 ребёнка1–3 классов, временный музейный kit. MiniSumo:2–3 ребёнка4–6 классов, собственный робот.',
         'MiniSumo p3 шаблонно упоминает secundaria; основной grade4–6. В списке платформ15151/51515 расходятся: согласовать конкретный комплект.',
         'Не менее6 команд для активации категории или решение комитета. Опыт братьев не отменяет grade gate.'],
        [source('Convocatoria2026',BAJA),source('Armado manual',ARMADO),source('Mini Sumo LEGO manual',SUMO)],
        'Младшим participation diploma, возможные поощрения требуют разъяснения. Mini Sumo — состязание; мировой результат/квота не установлены.'))
    guide['profiles'][-1]['cost']='Цена участия и входа неизвестна. Для Armado музей предоставляет временный kit; для Mini Sumo собственный robot. Подготовка, транспорт и жильё отдельно; полного семейного счёта нет.'
    for p in guide['profiles']:
        if p['id'] not in GUIDES:continue
        for key in ['name','age_summary','summary','route','hardware','language','importance','strengths','cost','award','evidence']:
            p[key]=polish(p[key])
        for key in ['requirements','nuances']:p[key]=[polish(s) for s in p[key]]
        for s in p['sources']:s['title']=polish(s['title'])
    guide.update(version=135,checked=CHECKED)
    guide['methodology']=str(len(guide['profiles']))+' профиля лиг, семейств и программ; все '+str(guide['mapped_legacy_count'])+' прежних маршрутов сохранены. Бразильские форматы разделены, местные Robofest LATAM и BajaBot описаны по своим категориям. Мировой охват частичный.'
    old={s['url'] for s in d['sources']}
    for title,url in [('TMR2027 · официальный host',GOV),('FMR · официальный календарь',FMR),('Bebras · текущая agendaAPI',BEBRAS_API),('Bebras · rulesAPI',BEBRAS_RULES),('Feria Maker · каталог мастерских',MAKER),('Feria Maker · данные собственной страницы',MAKER_API)]+[(s['title'],s['url']) for p in guide['profiles'] if p['id'] in GUIDES for s in p['sources']]:
        if url not in old:d['sources'].append(dict(title=title,url=url,checked=CHECKED,evidence='Выбранные первичные условия; не полный сайт/страна или принятое участие.'));old.add(url)
    def item(ident,title,children,gate,step):
        return dict(id=ident,title=title,children=children,gate=gate,step=step)
    d['family_strategy']['nearby_participation_v135']=dict(version=135,checked=CHECKED,title='Следующие дисциплины и октябрьские мастерские',
        status='editorial_plan_unconfirmed_admission',scope='Новые local routes не заменяют текущий планv118, VEX/FLL и полный мировой поиск.',
        conclusion='Сейчас — школьный Bebras до16 октября и семейные мастерские Feria Maker17–18 октября. На2027 — TMR3–6 марта, а RoboParade/BottleSumo LATAM только после нового анонса. BajaBot выбирать по школьному классу и виду результата.',
        items=[item('C064','Bebras · сначала регистрация школы',['matvey'],'До16 октября;3–6 классы регламента,2-й требует разрешения.','Проверить класс Матвея и регистрацию школы вCosta Rica; возраст9 не заменяет3 класс.'),
         item('E193','3D фигурка · общий семейный опыт',['matvey','oscar'],'5+,17–18 октября;70 без указанной валюты, слоты11/14 уточнить.','Проверить слот, язык, полный вход/занятие; сделать и сохранить собственный предмет.'),
         item('E197','OctoStudio · истории и первый цифровой проект',['matvey','oscar'],'Для детей без numeric age;17–18 октября, мастерская0 в каталоге,2 часа.','Подтвердить minimum age и родительский телефон, слот и язык; результат — проект, не медаль.'),
         item('C043','TMR · точные даты на2027',['matvey','oscar'],'3–6 марта2027 вZacatecas. Младшие категории ещё неизвестны.','Дождаться2027 convocatoria, подтвердить детей, команду, бюджет и нужную дисциплину до бронирования.'),
         item('C1165','RoboParade · младший scored проект',['matvey','oscar'],'Local2026:6–14,1–5; даты/правила2027 ещё неизвестны.','Подготовить автономную линию, остановку, скорость на экране и роли детей. Местный возраст и LTU Explorer grade отдельно.'),
         item('C1161','BottleSumo · самостоятельный LEGO/VEX',['matvey','oscar'],'Local2026:6–14, до3; overview grade5–8 расходится.','Согласовать новую младшую группу и robot kit. Unknown task и собственный код важнее взрослой готовой сборки.'),
         item('E191','BajaBot · первый показ,1–3 классы',['matvey','oscar'],'2–3 ученика1–3 классов; музейный kit; новый набор неизвестен.','Проверить школьный уровень обоих. Diploma не призовая победа; противоречивые поощренияmanualp8 согласовать.'),
         item('C1169','BajaBot · Mini Sumo,4–6 классы',['matvey'],'2–3 ученика4–6 классов, собственный автономный LEGO.','Для Матвея рассмотреть только при нужном классе. Общее участие братьев вэтой категории пока не установлено.')],
        category_ids=RL_IDS+['E191','C1169'],workshop_ids=['E'+str(i) for i in range(192,201)],
        limits=['Новый LATAM/BajaBot2027 календарь не выведен из2026; эти карточки остаются без дат и не попадают вICS.',
            'Workshop0 / kitprovided не означают бесплатную полную поездку. Язык занятий/судейства новых вариантов пока не подтверждён.',
            'Сохранены мировой охват, лагеряEN/ES/RU, пансионы, школы, история результатов и долгие инженерные маршруты. Полностью изученных стран0.'])
    plan=d['family_strategy']['nearby_participation_v135']
    for key in ['title','scope','conclusion']:plan[key]=polish(plan[key])
    plan['limits']=[polish(s) for s in plan['limits']]
    for q in plan['items']:
        for key in ['title','gate','step']:q[key]=polish(q[key])
