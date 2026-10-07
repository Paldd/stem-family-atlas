"""Opened primary-source South America pass; run once against v16 / 1081 cards.

Website translations do not establish teaching language. Public LNR event data
is separate from its national championship eligibility and from team standings.
"""
import copy, datetime, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/catalog.json'
WORK = pathlib.Path('/Users/pal/.codex/workspaces/stem-family-atlas-work/south-america-v17')
d = json.loads(PATH.read_text())
DAY = '2026-10-01'
assert len(d['events']) == 1081 and d['completeness_audit']['version'] == 16
baseline = copy.deepcopy(d['completeness_audit']['counts'])
byid = {e['id']: e for e in d['events']}
new, updated = [], []

def source(url, title, proof):
    row = next((s for s in d['sources'] if s['url'] == url), None)
    if row: row.update(checked=DAY, evidence=proof)
    else: d['sources'].append(dict(url=url, title=title, checked=DAY, evidence=proof))

def update(id, **kw):
    e = byid[id]; e.update(checked=DAY, **kw)
    if id not in updated: updated.append(id)
    source(e['source'], e['title'], e['proof'])
    return e

def reference(e, url, label, proof):
    if not any(r['url'] == url for r in e.setdefault('references', [])):
        e['references'].append(dict(url=url, label=label))
    source(url, label, proof)

def add(id, block, title, country, city, url, **kw):
    assert id not in byid
    e = dict(id=id, block=block, title=title, country=country, region='Южная Америка', city=city,
        source=url, checked=DAY, start='', end='', deadline='', period='Следующие даты не объявлены',
        date_status='Не объявлено', age='Не опубликован', mat='Условно — правила конкретного набора уточнить',
        osc='Условно — правила конкретного набора уточнить', format='Формат уточнить',
        entry='Подтвердить действующий набор, детский и иностранный допуск у организатора.',
        gear='По действующему регламенту / программе', cost='Будущий тариф не объявлен',
        language='Язык занятий / судейства не опубликован; ES / EN подтвердить', languages=[],
        language_certainty='Язык сайта / перевода документа не доказывает язык занятий или интервью.',
        scope='local', level='Учебная программа' if block=='Лагеря' else 'Региональный старт',
        importance_reason='Редакционная оценка по формату и опубликованному охвату; не официальный мировой рейтинг.',
        reward='Учебный проект / сертификат; не международная победа' if block=='Лагеря' else 'Место и награда по протоколу выбранного этапа',
        priority='P2 — поездка после подтверждения допуска', status='Идея', action='Сверить конкретную смену / этап до планирования поездки.',
        themes=['robotics','coding','technology'], participation='day_camp' if block=='Лагеря' else 'team',
        admission_kind='program' if block=='Лагеря' else 'open_application', evidence_level='program' if block=='Лагеря' else 'event_page',
        references=[], related_ids=[], registration_status='Семья не зарегистрирована. Наличие формы не доказывает свободные места.',
        note='Возрастная совместимость и фактический приём иностранного ребёнка проверяются отдельно.', proof='Прочитан первичный источник.')
    e.update(kw)
    if e['start']: e['date_status']='Подтверждено'
    d['events'].append(e);byid[id]=e;new.append(id);source(url,title,e['proof'])
    return e

# Chile: individual pages take precedence over an earlier season announcement.
chile_home='https://torneorobotica.cl/'
old_chile='https://torneorobotica.cl/calendario-oficial-ruta-para-la-temporada-2026/'
for id,slug,city,gear in [
    ('C047','concepcion2026esc','Talcahuano · INACAP, Autop. Concepción–Talcahuano 7421','Rescate Inicial / Avanzado, Sumo, Baile robot'),
    ('C048','inacap-santiago-maipu2026','Santiago · INACAP Maipú, Av. Américo Vespucio 974','Rescate Inicial / Avanzado и Futbol Robot')]:
    e=update(id,source='https://torneorobotica.cl/torneos/'+slug+'/',city=city,gear=gear,
        age='Ученики educación básica / media; минимальный возраст и эквивалент иностранного класса уточнить',
        mat='Условно — нужна категория и подтверждение школьного / иностранного допуска',
        osc='Условно — статус educación básica и минимальный возраст не установлены',
        participation='team',admission_kind='school',evidence_level='event_page',languages=[],
        language='ES: местные материалы; язык инструктажа и судейства подтвердить',
        format='Страница: максимум 4 ученика + profesor/tutor; ниже до 6 лиц включая tutor — численное расхождение',
        entry='Школьный / клубный представитель подаёт команду. Самостоятельный семейный состав и иностранное учреждение требуют подтверждения.',
        cost='Главная страница описывает circuit как бесплатный; включение техники и текущие условия конкретного старта уточнить',
        proof='Прочитана индивидуальная страница этапа: день, адрес, educación básica / media, категории и разный максимум состава.',
        note='Две версии размера команды на странице не согласованы. Rescate Inicial / Avanzado назначается по предыдущим результатам. '+('OPEN перенесён в Santiago на 30 октября и не смешан с этим школьным этапом.' if id=='C047' else 'Основное описание даёт Futbol / Rescate, строка выбора всё ещё говорит Rescate / Sumo; нужную форму подтвердить.'))
    reference(e,chile_home,'Liga Chile · текущий календарь','Прочитан публичный календарь: OPEN перенесён на 30 октября в Santiago; школьные старты остаются отдельными.')
e=update('C049',start='2026-11-13',end='2026-11-13',period='',date_status='Подтверждено',
    source='https://torneorobotica.cl/torneos/inacap-puertomontt-2026/',city='Puerto Montt · INACAP, Padre Harter 125',
    age='Educación básica / media; точный минимальный возраст и эквивалент класса уточнить',
    mat='Условно — школьный / иностранный приём подтвердить',osc='Условно — школьную категорию и нижний возраст подтвердить',
    format='До 5 учеников + profesor/tutor; до 25 команд',team_max=5,participation='team',admission_kind='school',
    gear='Sumo, Baile robot, Rescate Inicial / Avanzado',languages=[],language='ES: материалы; судейство подтвердить',
    proof='Индивидуальная event page дважды указывает 13 ноября 2026, 10:00–16:00 и адрес; текущий homepage также даёт 13 ноября.',
    note='Ранняя новость от 21 апреля указывает 20 ноября. В календаре использовано 13 ноября по индивидуальной странице и текущему homepage; день подтвердить перед поездкой. Иностранный / семейный допуск ещё не подтверждён.')
reference(e,old_chile,'Ранняя сезонная новость · другая дата','Старое объявление: Puerto Montt 20 ноября; первичный конфликт сохранён, второе событие не создано.')
e=update('C051',title='Liga Robótica Chile · Internacional LATAM · следующее издание',
    participation='team',admission_kind='school',themes=['robotics','coding','technology'],languages=[],
    language='ES: правила 2026; язык будущего судейства подтвердить',
    historical_editions=[dict(year=2026,start='2026-09-04',end='2026-09-05',city='Santiago · Gimnasio Municipal Huechuraba')],
    proof='Повторно прочитана первичная event page: 4–5 сентября 2026, школьные команды до 5 учеников и tutor, опубликованные результаты; издание 2027 не объявлено.',
    note='2026 был международным школьным стартом. Название «2027» убрано: следующий год и точные даты официально ещё не установлены. Прошедшие дни не перенесены в будущий ICS.')
e=add('C807','Соревнования','Liga Robótica Chile · OPEN Santiago Maipú · 2026','Чили',
    'Santiago · INACAP Maipú, Av. Américo Vespucio 974','https://torneorobotica.cl/torneos/open-santiago-2026/',
    start='2026-10-30',end='2026-10-30',period='',age='Todo competidor: ученики, преподаватели и другие; допуск оператора 6 / 9 лет и иностранца уточнить',
    format='До 5 участников в команде, до 12 команд',team_max=5,
    mat='Условно — OPEN не устанавливает опубликованный нижний возраст; детский / иностранный допуск подтвердить',
    osc='Условно — OPEN не является подтверждением приёма шестилетнего оператора',
    entry='Заявка OPEN, а не escolar. Согласовать семейную команду, категорию, robot check-in и возраст оператора.',
    gear='По отдельным текущим bases OPEN; escolar Sumo / Rescate не перенесены автоматически',
    proof='Прочитаны individual OPEN page и homepage: 30 октября, Santiago Maipú, максимум 5 / 12.',
    related_ids=['C048'],note='Текст даёт начало 11:00, блок Calendario 12:00–15:00: точное время уточнить. Homepage сообщает перенос OPEN из Concepción 9 октября; старая individual Concepción page сохраняет старое место / дату, отдельный доступный старт 9 октября не создан.')
reference(e,'https://torneorobotica.cl/torneos/concepcion2026/','Прежняя OPEN page · конфликт переноса','Старая страница всё ещё даёт 9 октября Concepción; текущий homepage сообщает перенос на Santiago 30 октября.')
reference(e,chile_home,'Текущий calendar · перенос OPEN','Названо OPEN Todo competidor se movió a Santiago 30 Oct; отдельная новая OPEN page прочитана.')

# Chile RoboRAVE: local call + actual linked ES rules + parent portal levels.
rave_url='https://roborave.cl/eventos/'
rave_pdf='https://roborave.cl/wp-content/uploads/2026/09/Rules-RoboRAVE-International-Challenges-02-09-2026-V6.1-ES.pdf'
rave_ticket='https://goldenpass.cl/roborave-santiago-noviembre-2026/'
e=add('C808','Соревнования','RoboRAVE Santiago · объявленный классификационный старт 2026','Чили',
    'Santiago · площадка Por definir',rave_url,start='2026-11-19',end='2026-11-19',period='',scope='national',
    age='Портал roborave.xyz: ES 8–11; местный PDF использует Escuela Primaria / MS / HS / UP',
    mat='Условно — 9 лет соответствует ES 8–11; класс, местную категорию и иностранный приём подтвердить',
    osc='Нет по опубликованному ES 8–11; отдельная категория до 8 лет или исключение не объявлены',
    format='Команда своей школьной категории; размер по подтверждённым bases выбранного испытания',
    gear='Местная страница называет Line Following, SumoBot, a-MAZE-ing; платформу и лимиты по категории',
    entry='Локальная страница приглашает участников из страны и из-за рубежа. Получить письменное подтверждение категории ES, состава, площадки и заявленной связи с Houston 2027.',
    cost='GoldenPass: inscripción $20 000 + service fee; валюта / единица оплаты и гостевой билет уточняются',
    level='Чилийский квалификационный старт по заявлению местного организатора',
    reward='Результат старта; включение в рейтинг и квота Houston 2027 требуют подтверждённого протокола / положения',
    proof='Прочитаны roborave.cl home / eventos, ticket page с 19 ноября 09:00, связанный PDF и roborave.xyz с ES 8–11.',
    note='GoldenPass приветствует семьи, но отдельный детский гостевой билет не опубликован. Filename PDF V6.1, внутри V6.2; обложка 2026 / Japan, следующий раздел Houston 2027: редакцию местных правил уточнить. Чилийское обещание квоты не стало автоматически подтверждённым мировым финалом с датой.')
reference(e,rave_ticket,'GoldenPass · дата и оплата участия','Ноябрь 2026, 19 ноября 09:00, Por definir, inscripción 20 000 без service fee; подтверждённый билет семьи не оформлен.')
reference(e,rave_pdf,'Связанный первичный manual · V6.2 внутри','Прочитан PDF: Escuela Primaria; Line Following, SumoBot и a-MAZE-ing имеют разные ограничения; родители не выполняют заезды детей.')
reference(e,'https://www.roborave.xyz/','Портал из linked manual · возраст уровней','ES 8–11, MS 11–14, HS 14–18, UP 19–99; местное исключение для 6 лет не опубликовано.')

# Argentina LNR: all ten visible upcoming records from public calendar endpoints.
lnr_general='https://github.com/lnr-argentina/Reglamentos/blob/main/General/General.md'
lnr_teams='https://github.com/lnr-argentina/Reglamentos/blob/main/Equipos/Equipos.md'
rows=[]
for f in WORK.glob('lnr-eventos-*.json'):
    for row in json.loads(f.read_text()):
        if row.get('mostrar') and row.get('fecha_inicio','')>=DAY:rows.append(row)
rows.sort(key=lambda e:(e['fecha_inicio'],e['id']))
assert len(rows)==10 and len({r['id'] for r in rows})==10
lnr_ids=[]
for n,row in enumerate(rows,809):
    id='C'+str(n);lnr_ids.append(id)
    public_url='https://sistema.lnr-argentina.com.ar/api/sede/'+str(row['sede']['id'])+'/eventos?anio=2026'
    start=row['fecha_inicio']; cutoff=datetime.date.fromisoformat(start)-datetime.timedelta(days=2)
    cutoff_utc=datetime.datetime.combine(cutoff+datetime.timedelta(days=1),datetime.time(2,59),tzinfo=datetime.timezone.utc)
    final=row['tipo']=='FINAL';pre=row['tipo']=='PRE SEDE'
    e=add(id,'Соревнования','LNR Argentina · '+row['nombre']+' · 2026','Аргентина',
        row['localidad']+' · '+row['provincia']+' · '+row['sede']['nombre'],public_url,
        start=start,end=start,period='',scope='national' if final else 'regional',participation='individual',
        age='Общий регламент §5.1: без различия возраста и академического уровня; младший оператор / иностранная зона требуют оформления',
        mat='Условно — общий возраст не ограничен; технический и иностранный допуск конкретного этапа подтвердить',
        osc='Условно — общий возраст не ограничен; ребёнок должен сам выполнять разрешённые действия и пройти локальный допуск',
        format='Личный зачёт робота / категории; отдельный team championship не обязателен для одного испытания',
        entry='Личный профиль → зарегистрированный / проверенный робот → подтверждение участия в конкретном событии. Только финальный старт не даёт права на национальный титул без предыдущего zonal / interzonal.',
        deadline=str(cutoff),deadline_utc=cutoff_utc.isoformat().replace('+00:00','Z'),deadline_label='Подтверждение участия LNR',
        deadline_note='Общее правило §5.3: система закрывается в 00:00 America/Argentina/Buenos_Aires накануне события; последний момент — 23:59 двумя календарными днями ранее. Локальное исключение подтвердить. Проверка нового робота может занимать до 48 рабочих часов.',
        gear='Категории текущего этапа и их robot restrictions уточнить; все 9 дисциплин не обязательны для личного старта',
        level='Национальный финал LNR' if final else 'PRE SEDE · вне зачёта чемпионата' if pre else 'ZONAL · этап национальной LNR',
        reward='Локальный результат; PRE SEDE не приносит чемпионатных очков' if pre else 'Результат дисциплины и очки LNR по действующему регламенту',
        registration_status='Публичный status: '+row['estado']+'. '+('INSCRIPCION обозначает приём в системе; это не подтверждение свободной квоты или регистрации семьи.' if row['estado']=='INSCRIPCION' else 'CREADO означает созданное событие; открытый приём не подтверждён.'),
        proof='Прочитаны публичные данные отдельной sede: event id '+str(row['id'])+', дата, город, тип '+row['tipo']+' и status; отдельные General / Equipos rules прочитаны.',
        note=('PRE SEDE не засчитывается в текущий чемпионат. ' if pre else '')+'Иностранцы прямо упомянуты для interzonal; этот пункт не подтверждает их место в любой зоне. Личный национальный титул зависит от предыдущих стартов и зональных очков; team title имеет отдельные правила. Дата здесь не означает опубликованный полный day schedule.')
    reference(e,'https://lnr-argentina.com.ar/','LNR · публичный календарь 2026','Главная страница загружает public sede calendars; одиночное API/eventos не использовано вместо данных этих площадок.')
    reference(e,lnr_general,'LNR · общий регламент','§5.1–5.3: без возрастного / академического ограничения, robot verification до 48 рабочих часов, отдельная confirmation cutoff; §7: сезонный зачёт и финал.')
    reference(e,lnr_teams,'LNR · отдельный team championship','Минимум 2 человека и 2 активных робота; все 9 категорий для team title; это не возрастное правило личного старта.')

# Peru: a still-visible registration badge refers to August, not a new future event.
e=add('C819','Соревнования','INTERCON Perú · национальный конкурс робототехники · следующий выпуск','Перу',
    'Последний: Trujillo · UPAO Campus','https://www.intercon.org.pe/concurso-robotica/',
    age='Amateur: студенты / энтузиасты; нижний возраст и детская категория не установлены',
    participation='team',scope='national',evidence_level='historical_program',
    period='Прошедший 12–13 августа 2026; будущий выпуск не объявлен',
    historical_editions=[dict(year=2026,start='2026-08-12',end='2026-08-13',city='UPAO · Trujillo')],
    gear='Последний выпуск: MiniSumo Autónomo / RC, Combate 3D, Soccer, Seguidor Línea, PLC automation',
    entry='Дождаться нового вызова и прочитать возраст / minor operator / командные bases. Старая форма не доказывает новый приём.',
    cost='Прошедшая 2026 page: S/40 за modalidade; будущая цена не установлена',
    proof='Прочитаны primary page, registration page и её linked публичный config.js: 12–13 августа 2026, UPAO Trujillo, 6 amateur modalities.',
    note='Badge «Inscripciones abiertas» и доступный formulario остались после прошедшего события. Будущая дата не выдумана; возраст ребёнка не установлен по слову Amateur.')
reference(e,'https://www.intercon.org.pe/concurso-robotica/js/config.js','INTERCON · публичные данные страницы','Официальный frontend config содержит день августа, площадку, amateur disciplines и прошлые тарифы.')

# Camps: independently selectable weeks, actual weekdays, different age tracks.
programable='https://programable.com.ar/colonia-tecno-2027/'
week_starts=['2027-01-04','2027-01-11','2027-01-18','2027-01-25','2027-02-01','2027-02-08']
for id,track,age,mat,osc in [
    ('L147','Júnior','6–9 лет','Условно — в январе / феврале 2027 Матвею 9 или уже 10; группу определить по точному дню рождения','Да по возрасту 6–7 в 2027; язык / приём подтвердить'),
    ('L148','Sénior','10–13 лет','Условно — только если к выбранной неделе уже исполнилось 10; точный день рождения неизвестен','Нет — в 2027 максимум 7, минимум группы 10')]:
    sessions=[dict(date=str(datetime.date.fromisoformat(start)+datetime.timedelta(days=offset)),topic='Неделя '+str(i+1)+' · Robotics + Games',
        start_time='09:30',end_time='12:30',timezone='America/Argentina/Buenos_Aires',
        time_note='Альтернативный сменный выбор 15:30–18:30; утро и вечер не являются обязательным единым учебным днём.')
        for i,start in enumerate(week_starts) for offset in range(5)]
    e=add(id,'Лагеря','Programable · Colonia Tecnológica verano 2027 · '+track,'Аргентина',
        'Ramos Mejía · Av. Presidente Perón (ex Gaona) 319',programable,
        start='2027-01-04',end='2027-02-12',period='6 отдельных недель: 4–8 / 11–15 / 18–22 / 25–29 января, 1–5 / 8–12 февраля',
        age=age,mat=mat,osc=osc,format='Дневные независимые недели по 15 часов; до 12 учеников в группе; утро 09:30–12:30 или 15:30–18:30',
        sessions=sessions,date_scope='session_days',teaching_weeks=[dict(start=start,end=str(datetime.date.fromisoformat(start)+datetime.timedelta(days=4))) for start in week_starts],
        entry='Можно выбрать одну / несколько отдельных недель и один turn на каждую; подтвердить возрастную группу, преподавание ES / EN и допуск иностранного ребёнка.',
        gear='LEGO EV3, mBot, micro:bit, Makey Makey и создание игр; Sénior также Arduino. Собственный kit не требуется покупать без подтверждения.',
        themes=['robotics','coding','games','technology'],cost='На странице $95 000 за неделю / 15 часов; скидки за несколько недель. Валюту, итоговый счёт и материалы подтвердить.',
        proof='Прочитана официальная holiday page по публичному HTML: Verano 2027, 6 точных недель, 2 группы, часы, лимит 12 и weekly price.',
        note='Одна карточка возрастного потока содержит 30 реальных дней, не 40 календарных дней и не 60 часов в неделю. Утро / вечер выбирается, не складывается. ES сайт не подтверждает язык преподавания; смешанная группа 9 / 10 лет не обещана. Семья не зарегистрирована.')

troonic='https://troonic.com/troonic-camp-2027/'
for id,part,start,end in [('L149',1,'2027-01-04','2027-01-07'),('L150',2,'2027-02-01','2027-02-04')]:
    e=add(id,'Лагеря','Troonic Camp 2027 · объявленное окно группы '+str(part),'Перу',
        'Lima / Pachacámac · CPR Cardal; распределение площадок уточнить',troonic,
        start=start,end=end,period='',age='Общий camp 4–15; в camp list Robótica 6–11 (другие потоки 4–5 / 12–15)',
        mat='Да по возрасту 9–10 в 2027 для camp Robótica 6–11; конкретный поток подтвердить',
        osc='Да по возрасту 6–7 в 2027 для camp Robótica 6–11; конкретный поток подтвердить',
        format='Объявлено 4 full days понедельник–четверг; организация занятий в Lima и выезда в Pachacámac противоречива',
        date_scope='camp_window',entry='Получить единое расписание выбранной группы: площадка каждого дня, фактические часы, bus / питание / материалы и ES / EN.',
        gear='Camp list: LEGO 4–5, Robótica 6–11, Arduino / 3D 12–15; не переносить старые regular MINI KIDS / KIDS часы на camp',
        cost='Заголовок camp: US$700; состав тарифа и единицу на ребёнка / группу подтвердить. Старые FAQ S/750–800 не приняты за тариф 2027.',
        proof='Прочитана primary CAMP 2027 page: Group 1 4–7 января, Group 2 1–4 февраля, camp ages / full days / US$700; отдельно выявлен старый FAQ 2024.',
        note='Точные объявленные окна сохранены как окно смены. Разделы говорят о full days пн–чт и одновременно о пятничных автобусах / masterclasses; пятницы и отдельные teaching sessions не выдуманы. FAQ содержит даты 2024 и оферту 2023. Часы / фактическая структура / язык требуют подтверждения перед бронированием.')

e=add('L151','Лагеря','Academia LMAC Pasto · Vacaciones Tecnológicas · следующий набор','Колумбия',
    'Pasto · Calle 12A #41A-10','https://www.lmac-roboticaeducativa.com/vacaciones2026',
    age='5–14 в прошедшей программе 2026',mat='Условно — прошлый возраст подходит; новый набор подтвердить',osc='Условно — прошлый возраст подходит; новый набор подтвердить',
    period='Прошедший 16 июня–14 августа 2026; будущие каникулы не объявлены',evidence_level='historical_program',
    historical_editions=[dict(year=2026,start='2026-06-16',end='2026-08-14')],format='Дневные занятия по 2 часа; weekly package 5 дней в прошлом наборе',
    gear='LEGO Education / WeDo и самостоятельные учебные проекты',cost='Прошлая page: COP35 000 за 2 часа, COP150 000 за неделю, COP130 000 за дополнительную; новый тариф подтвердить',
    proof='Прочитана holiday page: 5–14, 2 часа, 16 июня–14 августа 2026; нижний блок ошибочно даёт старт июня 2025.',
    note='Конфликт 2025 / 2026 сохранён. Прошедший summer package не преобразован в декабрьский набор. Certificate participation не является конкурсной наградой.')
add('L152','Лагеря','MyRoboTech Tuluá · курсы на середину и конец года','Колумбия',
    'Tuluá · Calle 41 #22-57 B. Príncipe','https://www.myrobotech.com.co/cursos-vacacionales',
    age='Дети / молодёжь; диапазон этой holiday programme не опубликован',
    format='Каникулярная STEAM программа: robotica / programación; новые часы и длительность не опубликованы',
    entry='Запросить конкретную end-of-year смену, возраст обеих групп, язык, самостоятельный приём иностранцев и полный счёт.',
    proof='Прочитана primary Cursos Vacacionales page: mitad / final de año, robotics / programming, адрес Tuluá; будущие дни, возраст и язык не опубликованы.',
    note='Календарь школьных каникул Колумбии не использован вместо дат лагеря. Общая academy age range не перенесена на эту смену.')
e=add('L153','Лагеря','CampoAventuras Colombia · 30 дней с Digital Mission · набор закрыт','Колумбия',
    'Cartagena → Isla Tierra Bomba','https://campoaventuras.com/',start='2026-12-15',end='2027-01-13',period='',
    age='9–17 на начало 15 декабря 2026; нельзя исполниться 9 внутри смены или 18 до её конца',
    mat='Условно — нужен точный день рождения для 9 лет на 15 декабря; текущий набор уже закрыт',
    osc='Нет — в декабре 2026 максимум 6, минимум camp 9',participation='residential',priority='P4 — текущий набор закрыт',status='Закрыт: все 180 мест заняты',
    registration_status='Primary page: 180 мест заняты / 0 мест; отдельная форма уведомления о будущих лагерях не является заявкой на этот набор.',
    format='30-дневный residential; Digital Mission 7 дней входит в общий пакет, точные digital days не опубликованы',
    entry='Следить за новой 7 / 15 / 30-дневной convocatoria. Самостоятельная покупка Digital Mission и будущие дни не подтверждены.',
    gear='Учебные роботы, сенсоры и механизмы внутри Digital Mission',cost='Digital page: общий 30-дневный пакет COP18 000 000; отдельный 7-дневный STEM тариф не указан',
    proof='Прочитаны homepage / FAQ и Digital Mission: 9–17, дни полного camp, все места заняты; 7 дней digital входят в 30-дневный пакет.',
    note='Название Digital не означает 30 дней только STEM. Перевод сайта на EN / ES / другие языки не подтверждает преподавание; полный день EN / ES семьи сохранён отдельно. Закрытый вариант не включается в семейный ICS.')
reference(e,'https://campoaventuras.com/en/programas.php?mision=2','Digital Mission · часть полного пакета','7 дней учебной робототехники; общий пакет, отдельные даты и teaching language не названы.')
e=add('L154','Лагеря','Umake · Robótica Digital VEX · онлайн курс ES, следующий поток','Колумбия',
    'Онлайн · организатор Colombia','https://umake.com.co/courses/robotica-educatis-de-7-a-11-anos/',
    age='7–11 в опубликованном курсе',mat='Условно — возраст подходит, действующий новый поток ещё не объявлен',
    osc='Условно — в 2026 младше 7; новый поток возможен лишь после семилетия в 2027 при сохранении правил',
    participation='regular',scope='online',evidence_level='historical_program',
    period='Прошедший 15–26 апреля 2024; новые занятия не объявлены',historical_editions=[dict(year=2024,start='2024-04-15',end='2024-04-26')],
    languages=['ES'],language='ES — поле Idioma Español в опубликованном курсе; новый преподаватель / поток подтвердить',
    language_certainty='Язык подтверждён характеристикой программы, а не языком сайта; это подтверждение старого курса, будущий поток не объявлен.',
    format='Online live course: 10 lessons / 15 часов в прошлом потоке; каникулярный residential camp не заявлен',
    gear='VEXcode VR в браузере, компьютер / совместимый планшет, стабильный интернет',
    entry='Подтвердить новый live поток из Коста-Рики, возраст на старт, фактический часовой пояс и цену.',
    cost='На старой course page $130 000; будущую цену, валюту и условия подтвердить',
    proof='Прочитана course page: Público objetivo 7–11, поле Idioma Español, 10 lessons / 15h и конкретные даты апреля 2024.',
    note='Язык ES подтверждён для старой программы, открытого будущего набора пока нет. Доступный Add to cart не доказывает начало нового курса или места. VEXcode VR course не является VEX tournament / мировым award.')

# Rechecked existing holiday candidates: remove website-only language matches.
update('L050',languages=[],language='Teaching ES / EN будущей смены не подтверждено',
    language_certainty='Испанская holiday page не содержит явного языка преподавания.',
    cost='2026 page: $200 Basic / $250 Premium, IVA включён; валюту и новый счёт уточнить. Transport +USD50 / +USD60 расходятся.',
    proof='Повторно прочитан public HTML: 8–15, 3 недели 2026, 08:30–13:00, prices с дробной частью 00; language и будущие дни не опубликованы.',
    note='2026 дни не перенесены в 2027. На странице две цены transport; 75h + cierre не использованы для выдуманного daily calendar. Учебная сертификация не является медалью соревнования.')
update('L033',languages=[],language='Язык каникулярной смены ES / EN не установлен',
    language_certainty='Ранее найденный испанский product title не подтверждает язык преподавания holiday programme.',
    proof='Текущая product URL не дала читаемой программы (timeout); прежнее прочтение подтверждало holiday title, но не teaching language / days / ages.',
    note='Снята прежняя ES отметка без доказательства преподавания. Regular Bases 6–8 / Elemental 9+ не перенесены на holiday workshop; новый набор требует отдельной programme page.')

profiles={p['id']:p for p in d['league_guide']['profiles']}
chile=profiles['chile'];chile['event_ids'].append('C807')
chile.update(age_summary='Escolar: educación básica / media. OPEN: todo competidor; минимальный детский возраст и иностранное учреждение уточнить.',
    route='Школьная команда → regional → final по действующему порядку. OPEN Santiago 30 октября — отдельная заявка, не автоматическая мировая квота.',
    nuances=['OPEN Concepción 9 октября перенесён в Santiago Maipú 30 октября по текущему homepage; старый event page сохраняет старую дату.',
        'Puerto Montt: individual page и homepage 13 ноября против старого season announcement 20 ноября.',
        'У Concepción / Maipú Escolar численность 4 ученика + tutor против строки 6 лиц; для Maipú список Futbol / Rescate против строки Sumo требует подтверждения.',
        'Internacional LATAM 2026 прошёл 4–5 сентября; следующий выпуск не объявлен. Школьные классы братьев и приём команды Costa Rica неизвестны.'],
    evidence='Повторно прочитаны текущий homepage, 5 индивидуальных страниц и старый seasonal announcement; переносы / конфликтные maxima сохранены.')
chile['sources'] += [dict(title='Chile · индивидуальный OPEN',url=byid['C807']['source'],checked=DAY),dict(title='Puerto Montt · индивидуальная дата',url=byid['C049']['source'],checked=DAY)]
rave=profiles['roborave'];rave['event_ids'].append('C808')
rave['nuances'].append('Santiago 19 ноября 2026: локальная convocatoria заявляет иностранцев и Houston 2027, linked portal ES 8–11. Оскар 6 не проходит этот возраст; конкретная площадка и мировая квота не подтверждены. Не переносить правила одной локальной площадки на всю сеть.')
rave['sources'] += [dict(title='RoboRAVE Chile · local call',url=rave_url,checked=DAY),dict(title='RoboRAVE linked parent · levels',url='https://www.roborave.xyz/',checked=DAY)]
rave['categories'].append(dict(name='Santiago · Local ES',age=byid['C808']['age'],team=byid['C808']['format'],hardware=byid['C808']['gear'],entry=byid['C808']['entry'],age_rule='ES 8–11 на связанном портале; точное местное отсечение подтвердить.',language=byid['C808']['language'],note=byid['C808']['note'],event_id='C808',source=rave_url,checked=DAY))
d['league_guide']['profiles'].append(dict(id='lnr-argentina',name='Liga Nacional de Robótica · Argentina',group='regional',
    age_summary='Общий §5.1: без различия возраста / академического уровня; местный minor / иностранный допуск подтвердить',age_tags=['6','9','10-12','teen'],
    summary='Зональный национальный чемпионат роботов; личные дисциплины и отдельный team championship.',
    categories=[dict(name='Личный старт категории',age='Общие правила без возрастного различия',team='Личный robot entry; team championship отдельно',hardware='По категории / homologación',entry='User → checked robot → event confirmation',age_rule='Общий §5.1 плюс локальные minor rules',event_id='C809')],
    event_ids=lnr_ids,legacy_ids=[],route='Zonal / interzonal → финал. Только финал позволяет выступить, но не получить национальный титул без предыдущего старта; сезонное участие влияет на очки.',
    hardware='Собственный соответствующий робот; до 48 рабочих часов проверки',language='ES правила; местное общение / judging уточнить',
    importance='Аргентинская национальная сеть; название международного этапа не делает всю лигу мировым финалом.',strengths='Autonomous / controlled robot disciplines, seasonal standings.',
    requirements=['Зарегистрировать и проверить робот; отдельно подтвердить event attendance до системного cutoff.', 'Team title: минимум 2 человека / 2 активных робота и участие во всех 9 категориях. Это не минимум для личного старта.'],
    nuances=['PRE SEDE не приносит чемпионатных очков; сейчас 3 таких будущих старта.', 'Иностранцы явно названы для interzonal; выбранная zonal и членство иностранного ребёнка ещё требуют подтверждения.', 'Финал 7 ноября: local final result и сезонный национальный титул различаются.'],
    cost='Публичный общий тариф этого прохода не установлен; kit / travel отдельно.',award='Протокол категории / сезонный титул по правилам; не гарантированная международная медаль',
    sources=[dict(title='LNR · current calendar',url='https://lnr-argentina.com.ar/',checked=DAY),dict(title='General rules · official linked repo',url=lnr_general,checked=DAY),dict(title='Team championship · official linked repo',url=lnr_teams,checked=DAY)],
    evidence='Прочитаны General / Equipos из связанного официального repository и public sede calendars: 10 будущих event records, статусы / PRE SEDE отдельно.'))
d['league_guide'].update(version=17,checked=DAY,methodology='63 профиля семейств / лиг / программ; все 46 прежних маршрутов сохранены. Южная Америка дополнена первичными local calls; мировой охват частичный.')

focus=dict(name='Южная Америка · первый семейный проход',checked=DAY,status='partial',isos=['ARG','CHL','COL','PER','ECU'],
    family='Матвей 2017, Оскар 2020. Оба могут учиться на EN / ES весь день; точные дни рождения и классы неизвестны.',
    conclusion='Аргентина публикует конкретные учебные недели 2027. Расписание перуанских смен требует уточнения; чилийский OPEN перенесён. LNR допускает возраст без общего минимума, но приём детей из Коста-Рики нужно подтвердить для каждого этапа.',
    language_result='Язык семьи не заменяет язык программы. Новые Programable / Troonic / LMAC / MyRoboTech и текущий Ecuador camp не включены в ES / EN фильтр без прямого языка преподавания доказательства. Umake явно ES, но прочитан прошедший поток 2024, будущая дата неизвестна.',
    routes=[
        dict(name='Аргентина · 6 учебных недель января / февраля',detail='Programable: 4 января–12 февраля 2027, отдельные недели и утренние / вечерние занятия. Оскару Júnior 6–9; Матвею Júnior до 10-летия либо Sénior 10–13 после него. Точный язык занятий / иностранный приём подтвердить. В календаре только 30 учебных дней каждого возрастного потока.',ids=['L147','L148']),
        dict(name='Перу · объявленные окна и старый конкурс',detail='Troonic: 4–7 января и 1–4 февраля, camp Robótica 6–11. У обоих возраст подходит, однако распределение занятий между Lima / Pachacámac и пятничными поездками не согласована; ES / EN и реальную длительность уточнить. INTERCON page всё ещё показывает приём после августа: будущий старт без даты.',ids=['L149','L150','C819']),
        dict(name='Чили · OPEN и escolar различаются',detail='OPEN теперь Santiago Maipú 30 октября; по нижнему детскому возрасту и иностранцам нет подтверждения. Escolar Puerto Montt: 13 ноября по текущей странице этапа против старой новости 20 ноября. RoboRAVE Santiago: 19 ноября, ES 8–11 для Матвея; Оскар 6 младше опубликованного уровня.',ids=['C807','C049','C808','C047','C048','C051']),
        dict(name='LNR Argentina · личный старт и сезонный титул',detail='Добавлены все 10 видимых будущих этапов в публичном календаре площадок: 6 zonal, 3 PRE SEDE без чемпионатных очков и final 7 ноября. Общий регламент не различает возраст; новый робот требует проверки. Иностранный допуск zonal и родительское согласие подтвердить. Только финал не даёт национальный титул без предыдущего участия.',ids=lnr_ids),
        dict(name='Колумбия / Эквадор · открытая страница не равна набору',detail='LMAC и Ecuador Roboticamp описывают прошедшее лето; будущие даты не перенесены. MyRoboTech подтверждает holiday courses, но без новых дней / возрастов. CampoAventuras 15 декабря–13 января: уже все места заняты, 9+ на старт; Digital всего 7 дней внутри общего 30-дневного пакета. Umake ES course прошлый, не зимняя смена.',ids=['L151','L152','L153','L154','L050'])],
    open_questions=['Точные дни рождения для Programable 9 / 10 и CampoAventuras 9 на день старта; школьные классы для Chile / RoboRAVE.',
        'Programable / Troonic: преподавание ES / EN, окончательное расписание, приём детей из-за рубежа и материалы / питание.',
        'LNR: точный набор дисциплин каждой sede, детский оператор и consent, иностранная зона / сезонный зачёт; status CREADO не означает регистрацию.',
        'Chile: текущие team maxima / Maipú categories и час OPEN; новая international convocatoria.',
        'Colombia / Ecuador: новые December / January shifts, реальный язык занятий и возраст, без переноса старых летних оферт.',
        'Продолжить остальные страны Южной Америки и местные FIRST / WRO / VEX / независимые турниры; этот проход не завершает страновые аудиты.'])
a=d['completeness_audit'];a.update(version=17,checked=DAY,baseline=baseline,new_ids=new,new_profiles=['lnr-argentina'],updated_ids=updated,south_america_focus=focus,
    scope='Южная Америка: первично прочитаны 10 LNR этапов и общий / team регламент, чилийский перенос OPEN и local RoboRAVE, 4 датированных camp age tracks / windows 2027, holiday / online кандидаты и закрытый camp. Тайвань, Costa Rica / México и мировой незавершённый охват сохранены.')
issues=[
    dict(name='Liga Chile · перенос и размеры команды',status='Текущий calendar переносит OPEN на Santiago 30 октября, старая individual page Concepción 9 октября остаётся. Escolar 4 ученика + tutor против 6 лиц; Maipú Futbol против строки Sumo. Время OPEN 11:00 / 12:00 расходится.',official_alternative=chile_home),
    dict(name='Puerto Montt · 13 / 20 ноября',status='Использовано 13 ноября по individual page и текущему homepage; ранняя апрельская новость даёт 20 ноября. Второй фиктивный этап не создан.',official_alternative=byid['C049']['source']),
    dict(name='Troonic Camp · смешанные редакции',status='2027 header даёт две Mon–Thu группы; далее пятничные автобусы и masterclasses, regular FAQ 2024 / offer 2023. Только объявленные 4-дневные окна; пятницы / почасовой курс не выдуманы.',official_alternative=troonic),
    dict(name='RoboRAVE Chile · manual generation',status='Filename V6.1 против внутри V6.2; обложка Japan 2026 против раздела Houston 2027. ES 8–11 прочитан на связанном портале, возрастного исключения Oscar 6 не найдено.',official_alternative=rave_pdf),
    dict(name='После даты остаётся Inscripciones abiertas',status='INTERCON page относится к 12–13 августа 2026; Umake live course к апрелю 2024. Наличие формы / корзины не подтверждает новый набор.',official_alternative=byid['C819']['source']),
    dict(name='LMAC и TechLab Kids · историчность / доступ',status='LMAC summer page содержит start 2025 против programme 2026. TechLab Kids page сейчас timeout; повторное чтение не заявлено, неподтверждённый teaching ES tag снят.',official_alternative=byid['L151']['source'])]
a['source_issues']+=issues
a['caveats'] += ['Programable age tracks — две группы одной программы, 30 фактических учебных дней у каждой, не два независимых фестиваля.',
    'LNR 10 records включают 3 PRE SEDE и final. Возраст без общего минимума, местный иностранный допуск и право на национальный сезонный титул различаются.',
    'Camp windows Troonic сохранены как объявленные дни смены с видимым конфликтом структуры; daily sessions не придуманы. Closed CampoAventuras исключён из семейного ICS.']
a['known_backlog'].append(dict(kind='Южная Америка',name='Детский / иностранный приём и новые смены',reason='; '.join(focus['open_questions']),url=programable))
d.update(asof=DAY,source_count=len(d['sources']))
d['expansion_log'].append(dict(version=17,date=DAY,scope='South America primary family pass',added_ids=new,updated_ids=updated,notes=['All 1081 previous IDs, 62 previous profiles, 46 routes, Taiwan and CR/MX focus retained.', 'No invented future editions for INTERCON / LMAC / Ecuador / Umake.', 'Explicit ES course is historical, 2027 camp teaching language unknown.', 'LNR 10 visible upcoming records include 3 non-scoring PRE SEDE.']))
(ROOT/'data/south-america-audit-v17.json').write_text(json.dumps(dict(version=17,focus=focus,added_ids=new,updated_ids=updated,source_issues=issues),ensure_ascii=False,indent=2))
planpath=ROOT/'data/research-plan.json';plan=json.loads(planpath.read_text())
plan.update(updated=DAY,status='active',completeness_audit='data/audit-v17.json')
for r in plan['requirements']:
    if r['id']=='global_competitions':r['evidence']='v17: LNR 10 конкретных будущих event records, Chile OPEN relocation / RoboRAVE, historical-only Peru INTERCON. 63 профиля, все 46 прежних маршрутов сохранены. Полнота мира не подтверждена.'
    if r['id']=='camps':r['evidence']='v17: Argentina 2 age tracks / 6 недель / 30 фактических дней, Peru 2 announced camp windows с конфликтом расписания, Colombia historical / closed candidates. Teaching ES / EN отдельно, два прежних website-only ES tags сняты.'
    if r['id']=='eligibility':r['evidence']='v17: family 2017 / 2020 и full-day EN / ES сохранены; Programable требует дня 10-летия, Chile school equivalence, LNR minor / foreign local rules; RoboRAVE ES 8–11 исключает Oscar 6.'
plan['latest_validation']=dict(version='v17',status='pending',research_status='active')
plan['next_research'].insert(0,'South America: '+ '; '.join(focus['open_questions']))
planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2));PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2))
print(json.dumps(dict(added=len(new),total=len(d['events']),updated=updated,new_ids=new),ensure_ascii=False))
